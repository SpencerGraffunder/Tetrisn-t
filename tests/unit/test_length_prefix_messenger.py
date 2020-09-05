import errno

import pytest
import socket


from unittest.mock import MagicMock

from common.length_prefix_messenger import LengthPrefixMessenger


TEST_STR = "Test"


@pytest.fixture()
def mock_connection_messenger():
    # Create a mock socket class so we can mock out send/recv since with socket
    # they are properties and can't be mocked properly
    class Mocket:
        def send(self, buff):
            pass

        def recv(self, n):
            pass

        def setblocking(self, blocking):
            assert not blocking

    return LengthPrefixMessenger(Mocket())


@pytest.fixture()
def messenger_pair():
    a_conn, b_conn = socket.socketpair(socket.AF_INET, socket.SOCK_STREAM)

    messenger_a = LengthPrefixMessenger(a_conn)
    messenger_b = LengthPrefixMessenger(b_conn)

    return messenger_a, messenger_b


def test_send_multiple_messages(messenger_pair):
    msgr_a, msgr_b = messenger_pair

    msgs = [str(i) for i in range(50)]

    for msg in msgs:
        msgr_a.send(msg)
        msgr_b.send(msg)

    assert msgr_a.get_msgs() == msgs
    assert msgr_b.get_msgs() == msgs

    assert msgr_a.get_msgs() == []
    assert msgr_b.get_msgs() == []


def test_send_one_way_messages(messenger_pair):
    msgr_a, msgr_b = messenger_pair

    msgs = [str(i) for i in range(1000000, 1000100)]

    for msg in msgs:
        msgr_a.send(msg)

    assert msgr_b.get_msgs() == msgs

    assert msgr_a.get_msgs() == []
    assert msgr_b.get_msgs() == []


def test_send_and_get_interwoven(messenger_pair):
    msgr_a, msgr_b = messenger_pair

    msgs = [str(i) for i in range(1000000, 1000100)]

    a_msgs = []
    b_msgs = []
    for msg in msgs:
        msgr_a.send(msg)
        msgr_b.send(msg)

        # Test letting some messages build up
        if int(msg) % 3 == 0:
            a_msgs.extend(msgr_a.get_msgs())
            assert msgs[:len(a_msgs)] == a_msgs
            b_msgs.extend(msgr_b.get_msgs())
            assert msgs[:len(b_msgs)] == b_msgs

    assert not msgr_a.send()
    assert not msgr_b.send()

    # Get any potential remaining messages if msg did not end divisible by 3
    a_msgs.extend(msgr_a.get_msgs())
    b_msgs.extend(msgr_b.get_msgs())

    assert a_msgs == msgs
    assert b_msgs == msgs

    assert msgr_a.get_msgs() == []
    assert msgr_b.get_msgs() == []


def test_send_and_read_empty_msgs(messenger_pair):
    msgr_a, msgr_b = messenger_pair

    for _ in range(100):
        assert not msgr_a.send()
        assert not msgr_b.send()
        assert msgr_a.get_msgs() == []
        assert msgr_b.get_msgs() == []


def test_partial_msg(messenger_pair):
    msgr_a, msgr_b = messenger_pair

    msg = LengthPrefixMessenger.pack_msg(TEST_STR)

    # Partition the message and send in two chunks
    for i in range(len(msg)):
        msgr_a.send_buff.extend(msg[:i])
        msgr_a.send()
        assert msgr_b.get_msgs() == []

        msgr_a.send_buff.extend(msg[i:])
        msgr_a.send()
        assert msgr_b.get_msgs() == [TEST_STR]


def test_partial_send_return_true(mock_connection_messenger):
    mock_connection_messenger.conn.send = MagicMock(return_value=len(TEST_STR))
    assert mock_connection_messenger.send(TEST_STR), \
        "Send did not return True when failing to send all of the data"


@pytest.mark.parametrize("exception_errno", [errno.EAGAIN, errno.EWOULDBLOCK])
def test_raise_non_blocking_exception(mock_connection_messenger, exception_errno):
    e = socket.error()
    e.args = (exception_errno,)

    mock_connection_messenger.conn.send = MagicMock(side_effect=e)
    assert mock_connection_messenger.send(TEST_STR), \
        "Send did not return True after non-blocking errors"

    mock_connection_messenger.conn.recv = MagicMock(side_effect=e)
    assert mock_connection_messenger.get_msgs() == [], \
        "Get msgs did not return empty list after non-blocking errors"


def test_raise_unexpected_exception(mock_connection_messenger):
    exc_msg = "Injected exception"
    e = InterruptedError(exc_msg)

    # Test send
    mock_connection_messenger.conn.send = MagicMock(side_effect=e)
    with pytest.raises(InterruptedError, match=exc_msg):
        mock_connection_messenger.send(TEST_STR)

    # Test get_msgs
    mock_connection_messenger.conn.recv = MagicMock(side_effect=e)
    with pytest.raises(InterruptedError, match=exc_msg):
        mock_connection_messenger.get_msgs()
