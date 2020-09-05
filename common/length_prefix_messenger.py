import errno
import socket
import struct

ENCODING_SCHEME = 'utf-8'
READ_SIZE = 4096
INT_BYTES = 4


class LengthPrefixMessenger:
    """
    This class provides a non-blocking API on top of raw socket connections to
    handle passing complete messages across the connection. We achieve this
    by starting each message with 4 bytes, representing the length of the
    remainder of the message.

    For example, say we wanted to send the message "hello". This has 5
    characters, so the message would start with 4 bytes, representing 5,
    followed by the byte string representation of "hello". For simplicity sake,
    you could imagine this string being sent looking like "5hello". In reality,
    the 5 will be taking up the first 4 bytes and "hello" will be encoded
    to bytes using utf-8.

    Note, this class does not handle reestablishing a connection that may have
    been dropped. A server connection manager will have to handle that.
    """
    def __init__(self, conn):
        self.conn = conn
        self.conn.setblocking(False)
        self.recv_buff = bytearray()
        self.remaining_msg_len = 0
        self.send_buff = bytearray()

    def send(self, msg=''):
        """
        Attempt to send the message, if provided, and send any previously unsent
        data.

        :param msg: optional message to send
        :return: True if we have remaining data to send
        :raises socket.error: if the socket encountered an unexpected error
        """
        if msg:
            packed_msg = LengthPrefixMessenger.pack_msg(msg)
            self.send_buff.extend(packed_msg)

        try:
            # I ran some testing really quick, and I was able to send around
            # 650 messages that were 4096 bytes long before hitting a
            # socket.error. If we see this run into a blocking exception, we
            # might want to investigate how much network traffic we are sending.
            bytes_sent = self.conn.send(self.send_buff)
            self.send_buff = self.send_buff[bytes_sent:]

        except socket.error as e:
            err = e.args[0]
            # Since we are using non-blocking calls, the socket's buffer might
            # be full at the moment, so the data will need to be re-sent later
            if err != errno.EAGAIN and err != errno.EWOULDBLOCK:
                raise e

        return bool(self.send_buff)

    def get_msgs(self):
        """
        Read complete messages from our network connection.

        :return: list of strings of complete messages
        :raises socket.error: if the socket encountered an unexpected error
        """
        try:
            data = self.conn.recv(READ_SIZE)
            self.recv_buff.extend(bytearray(data))

        except socket.error as e:
            err = e.args[0]
            # Since we are using non-blocking calls, there might just not be
            # any data available in the socket's buffer yet. If this isn't an
            # error from not blocking, let's raise it
            if err != errno.EAGAIN and err != errno.EWOULDBLOCK:
                raise e

        return [msg for msg in iter(self.__parse_msg_from_buff, None)]

    def __parse_msg_from_buff(self):
        if self.remaining_msg_len == 0 and len(self.recv_buff) >= INT_BYTES:
            msg_len = self.recv_buff[:INT_BYTES]
            self.recv_buff = self.recv_buff[INT_BYTES:]
            self.remaining_msg_len = struct.unpack("!I", msg_len)[0]

        if len(self.recv_buff) >= self.remaining_msg_len != 0:
            msg = self.recv_buff[:self.remaining_msg_len]
            self.recv_buff = self.recv_buff[self.remaining_msg_len:]
            self.remaining_msg_len = 0
            return msg.decode(ENCODING_SCHEME)
        else:
            return None

    @staticmethod
    def pack_msg(msg):
        """
        Pack a string message into a byte array, prefixed with the length.

        :param msg: string to pack into byte array prefixed with the length
        :return: msg packed into byte array, starting with 4 bytes for the length
        """
        packed = bytearray(struct.pack("!I", len(msg)))
        packed.extend(bytearray(msg.encode(ENCODING_SCHEME)))
        return packed
