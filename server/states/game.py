from server.states.state import *
from common.components.tile import *  # Import like this to avoid having to do Tile. before everything
from common.components.piece import *
from common.components.player import *
import random
from collections import deque
import server.globals as g
from common.components.text import *
from common.connection import GameState
from common.connection import connection
from common.connection import PlayerInput
from common.player_input import *
from server.constants import *
from server.clearing_line import *


class Game(State):
    def __init__(self):
        State.__init__(self)

        self.state = GameState()
        self.input = PlayerInput(None)
        self.das_threshold = 0
        self.spawn_delay_threshold = 10
        self.paused = False
        self.fall_threshold = FALL_DELAY_VALUES[0]
        self.last_lock_position = 0
        self.lines_cleared = 0
        self.die_counter = 0
        self.down_counter = 0
        self.is_move_right_pressed = False
        self.is_move_left_pressed = False
        self.is_move_down_pressed = False
        self.fall_counter = 0
        self.time_to_move = False
        self.time_next_move = 0
        self.time_next_fall = 0
        self.time_next_rotate = 0
        self.das_counter = 0
        self.score = 0
        self.time_to_rotate = False
        self.clearing_lines = []

        self.reset(self.input)

    def reset(self, player_input):
        self.state = GameState()
        self.state.player_count = player_input.player_count

        self.state.board_width = (4 * self.state.player_count) + 6
        # Fill board with empty tiles
        self.state.board = [[Tile() for _ in range(self.state.board_width)] for _ in range(self.state.board_height+BOARD_HEIGHT_BUFFER)]

        # find the greatest level less than CURRENT_LEVEL
        # in FALL_DELAY_VALUES and set the speed to that level's speed
        self.state.current_level = player_input.starting_level
        x = self.state.current_level
        while x >= 0:
            if x in FALL_DELAY_VALUES.keys():
                self.fall_threshold = FALL_DELAY_VALUES[x]
                break
            x -= 1
        self.last_lock_position = 0
        self.lines_cleared = 10 * self.state.current_level
        self.die_counter = 0
        self.down_counter = 0
        self.is_move_right_pressed = False
        self.is_move_left_pressed = False
        self.is_move_down_pressed = False
        self.fall_counter = 0
        self.time_to_move = False
        self.time_next_move = 0
        self.time_next_fall = 0
        self.time_next_rotate = 0
        self.das_counter = 0
        self.score = 0
        self.paused = False

        self.state.players = [Player(x) for x in range(self.state.player_count)]

        # split the board into PLAYER_COUNT equal sections (using floats), find the middle of the section we care about using the average, and favor right via the columns being index by 0
        for player in self.state.players:
            player.spawn_column = int(((self.state.board_width / self.state.player_count) * player.player_number + (self.state.board_width / self.state.player_count) * (player.player_number + 1)) / 2)

    def do_event(self, event, player_number):

        if event.control == ControlType.QUIT:
            self.switch('lobby')

        # player controls: move and rotate
        for player in self.state.players:
            if player_number == player.player_number:
                if event.type == EventType.KEY_DOWN:

                    if self.state.players[player_number].active_piece is not None:
                        if event.control == ControlType.CCW:
                            if self.state.players[player_number].active_piece.can_rotate(self.state.board, self.state.players, Rotation.CCW):
                                self.state.players[player_number].active_piece.rotate(Rotation.CCW)
                                self.state.time_to_rotate = False
                        if event.control == ControlType.CW:
                            if self.state.players[player_number].active_piece.can_rotate(self.state.board, self.state.players, Rotation.CW):
                                self.state.players[player_number].active_piece.rotate(Rotation.CW)
                                self.time_to_rotate = False

                    if event.control == ControlType.LEFT:
                        self.state.players[player_number].is_move_left_pressed = True
                        self.state.players[player_number].das_threshold = 0
                        self.state.players[player_number].das_counter = 0
                        # if the other direction is being held, set this direction to override it; if not, it's already False anyways
                        self.state.players[player_number].is_move_right_pressed = False
                    if event.control == ControlType.RIGHT:
                        self.state.players[player_number].is_move_right_pressed = True
                        self.state.players[player_number].das_threshold = 0
                        self.state.players[player_number].das_counter = 0
                        # if the other direction is being held, set this direction to override it; if not, it's already False anyways
                        self.state.players[player_number].is_move_left_pressed = False
                    if event.control == ControlType.DOWN:
                        self.state.players[player_number].is_move_down_pressed = True
                        self.state.players[player_number].down_counter = 0

                if event.type == EventType.KEY_UP:
                    if event.control == ControlType.LEFT:
                        self.state.players[player_number].is_move_left_pressed = False
                    if event.control == ControlType.RIGHT:
                        self.state.players[player_number].is_move_right_pressed = False
                    if event.control == ControlType.DOWN:
                        self.state.players[player_number].is_move_down_pressed = False

    def lock_piece(self, player_number):

        piece_locked_into_another_piece = False
        max_row_index = 0
        for location in self.state.players[player_number].active_piece.locations:
            if self.state.board[location[1]][location[0]].tile_type != TileType.BLANK:
                piece_locked_into_another_piece = True
            if self.state.player_count == 1:
                tile_type = self.state.players[player_number].active_piece.tile_type
            else:
                tile_type = player_number
            self.state.board[location[1]][location[0]] = Tile(tile_type)
            if location[1] > max_row_index:
                max_row_index = location[1]

        # this was some weird frame data stuff determined based on emulating the 1989 NES version of Tetris (the wiki didn't go quite in-depth enough)
        if self.state.players[player_number].active_piece.piece_type == PieceType.I:
            self.state.players[player_number].spawn_delay_threshold = ((max_row_index+2)//4)*2+10
        else:
            self.state.players[player_number].spawn_delay_threshold = ((max_row_index+3)//4)*2+10

        # Add all clearable lines to list
        for row_index, row in enumerate(self.state.board):
            can_clear = True
            for tile in row:
                if tile.tile_type == TileType.BLANK:
                    can_clear = False
            if can_clear:
                line_in_clearing_lines = False
                for line in self.clearing_lines:
                    if line.board_index == row_index:
                        line_in_clearing_lines = True
                if not line_in_clearing_lines:
                    self.clearing_lines.append(ClearingLine(player_number, row_index, 20))
                    self.state.players[player_number].player_state = TetrisState.CLEAR
            else:
                self.state.players[player_number].player_state = TetrisState.SPAWN

        self.state.players[player_number].active_piece = None
        if piece_locked_into_another_piece:
            for player in self.state.players:
                player.player_state = TetrisState.DIE

    def clear_lines(self):

        # Keep track of lines that need to be cleared this tick
        lines_to_remove = []

        # Loop through lines in lines to clear
        for i, line in enumerate(self.clearing_lines):

            # Decrement the animation counter on the line
            line.decrement_counter()

            # If the counter is done
            if line.counter <= 0:
                # Add the line to the remove list
                lines_to_remove.append(line.board_index)
                # Set the player's state to spawn
                self.state.players[line.player_number].player_state = TetrisState.SPAWN

        for line_index in lines_to_remove:
            self.state.board.pop(line_index)
            temp_board = deque(self.state.board)
            new_line = [Tile() for j in range(self.state.board_width)]
            temp_board.appendleft(new_line)
            self.state.board = list(temp_board)

        for line in lines_to_remove:
            for i, clearing_line in enumerate(self.clearing_lines):
                if clearing_line.board_index == line:
                    self.clearing_lines.pop(i)

    def update(self):

        while connection.inputs:
            self.input = connection.get_input()

            if self.input.new_game:
                self.reset(self.input)

            if self.input.pause:
                self.paused = True
            if self.input.resume:
                self.paused = False

            if self.paused:
                return

            for event in self.input.events:
                self.do_event(event, self.input.player_number)

        if self.paused:
            return

        # increment das_counter if a move key is pressed (it's reset to zero each time a key is pressed down)
        for player_number in range(self.state.player_count):
            if self.state.players[player_number].is_move_left_pressed or self.state.players[player_number].is_move_right_pressed:
                self.state.players[player_number].das_counter += 1

        self.clear_lines()

        # STATES SECTION START
        for player_number in range(self.state.player_count):

            if self.state.players[player_number].player_state == TetrisState.SPAWN:

                # if the game just started or the next piece can spawn into the board (only checking other players' pieces, not the piece tiles on the board)
                if self.state.players[player_number].next_piece is None or self.state.players[player_number].next_piece.can_move(self.state.board, self.state.players, None) == MoveAllowance.CAN:

                    self.state.players[player_number].spawn_delay_counter += 1

                    if self.state.players[player_number].spawn_delay_counter > self.state.players[player_number].spawn_delay_threshold:

                        # Spawn piece
                        # RNG piece choice decision
                        if self.state.players[player_number].next_piece_type is None:
                            active_piece_type = random.choice([PieceType.I, PieceType.O, PieceType.T, PieceType.L, PieceType.J, PieceType.Z, PieceType.S])
                        else:
                            active_piece_type = self.state.players[player_number].next_piece.piece_type
                        self.state.players[player_number].next_piece_type = random.choice([PieceType.I, PieceType.O, PieceType.T, PieceType.L, PieceType.J, PieceType.Z, PieceType.S])
                        if self.state.players[player_number].next_piece_type == active_piece_type:
                            self.state.players[player_number].next_piece_type = random.choice([PieceType.I, PieceType.O, PieceType.T, PieceType.L, PieceType.J, PieceType.Z, PieceType.S])
                        self.state.players[player_number].active_piece = Piece(active_piece_type, player_number, self.state.players[player_number].spawn_column)  # this puts the active piece in the board
                        self.state.players[player_number].next_piece = Piece(self.state.players[player_number].next_piece_type, player_number, self.state.players[player_number].spawn_column)  # this puts the next piece in the next piece box
                        self.state.players[player_number].player_state = TetrisState.PLAY
                        self.state.players[player_number].fall_counter = 0
                        self.state.players[player_number].spawn_delay_counter = 0

            if self.state.players[player_number].player_state == TetrisState.PLAY:
                # Move piece logic
                if self.state.players[player_number].is_move_left_pressed or self.state.players[player_number].is_move_right_pressed:

                    # see if the das counter is above the das threshold, which is one of three values given the player count based on if the key was just pressed (das_threshold == 0), else
                    # {if first das threshold was passed for that l/r keypress (das_threshold == DAS_VALUES[self.state.player_count][1]), else (das_threshold == DAS_VALUES[self.state.player_count][0])}
                    # this way the first time the button is pressed, the piece moves (and if there's a piece in the way and then there isn't, it moves)
                    # furthermore, once the initial nonzero das_threshold (DAS_VALUES[self.state.player_count][1]) is passed, then das_threshold becomes smaller (DAS_VALUES[self.state.player_count][0])
                    # so that the piece moves faster after the player surely wants the game to start moving the piece for them

                    # special case: if a direction is held for a long time and the active piece is against another piece (either placed or another player's piece), the das_counter shouldn't be reset
                    # if the piece can move again because the input is being made for auto shift, so if das_counter == 0, we want to just subtract 1 off das_threshold unless it comes within
                    # DAS_VALUES[self.state.player_count][0] of DAS_VALUES[self.state.player_count][1], in which case we want it to be DAS_VALUES[self.state.player_count][1] - DAS_VALUES[self.state.player_count][0]

                    # the special case's code also makes it work to buffer auto shift during a piece's spawn delay time or a line clear animation
                    if self.state.players[player_number].das_counter > self.state.players[player_number].das_threshold:
                        if self.state.players[player_number].is_move_left_pressed:
                            if self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, Direction.LEFT) == MoveAllowance.CAN:
                                self.state.players[player_number].active_piece.move(Direction.LEFT)
                                # make sure das_threshold is no longer zero for this move input and set das_counter back accordingly
                                if self.state.players[player_number].das_threshold == 0:
                                    self.state.players[player_number].das_threshold = DAS_VALUES[self.state.player_count][1]
                                    # set das_counter as explained in the special case
                                    if self.state.players[player_number].das_counter + DAS_VALUES[self.state.player_count][0] > DAS_VALUES[self.state.player_count][1]:
                                        self.state.players[player_number].das_counter = DAS_VALUES[self.state.player_count][1] - DAS_VALUES[self.state.player_count][0]
                                    else:
                                        self.state.players[player_number].das_counter -= 1
                                else:
                                    self.state.players[player_number].das_threshold = DAS_VALUES[self.state.player_count][0]
                                    self.state.players[player_number].das_counter = 0
                        if self.state.players[player_number].is_move_right_pressed:
                            if self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, Direction.RIGHT) == MoveAllowance.CAN:
                                self.state.players[player_number].active_piece.move(Direction.RIGHT)
                                # make sure das_threshold is no longer zero for this move input
                                if self.state.players[player_number].das_threshold == 0:
                                    self.state.players[player_number].das_threshold = DAS_VALUES[self.state.player_count][1]
                                    # set das_counter as explained in the special case and set das_counter back accordingly
                                    if self.state.players[player_number].das_counter + DAS_VALUES[self.state.player_count][0] > DAS_VALUES[self.state.player_count][1]:
                                        self.state.players[player_number].das_counter = DAS_VALUES[self.state.player_count][1] - DAS_VALUES[self.state.player_count][0]
                                    else:
                                        self.state.players[player_number].das_counter -= 1
                                else:
                                    self.state.players[player_number].das_threshold = DAS_VALUES[self.state.player_count][0]
                                    self.state.players[player_number].das_counter = 0

                if self.state.players[player_number].is_move_down_pressed:
                    self.state.players[player_number].down_counter += 1

                    if self.state.players[player_number].down_counter > 2:
                        if self.state.players[player_number].is_move_down_pressed:
                            if self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, Direction.DOWN) == MoveAllowance.CAN:
                                self.state.players[player_number].active_piece.move(Direction.DOWN)
                                self.state.players[player_number].fall_counter = 0
                            elif self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, Direction.DOWN) == MoveAllowance.CANT_BOARD:
                                self.lock_piece(player_number)
                            elif self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, Direction.DOWN) == MoveAllowance.CANT_PIECE:
                                pass

                            self.state.players[player_number].down_counter = 0

                self.state.players[player_number].fall_counter += 1

                if self.state.players[player_number].fall_counter >= self.fall_threshold and self.state.players[player_number].active_piece is not None:
                    if self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, Direction.DOWN) == MoveAllowance.CANT_BOARD:
                        self.lock_piece(player_number)
                    elif self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, Direction.DOWN) == MoveAllowance.CAN:
                        self.state.players[player_number].active_piece.move(Direction.DOWN)
                    elif self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, Direction.DOWN) == MoveAllowance.CANT_PIECE:
                        pass
                    self.state.players[player_number].fall_counter = 0

            if self.state.players[player_number].player_state == TetrisState.CLEAR:
                pass

            elif self.state.players[player_number].player_state == TetrisState.SPAWN_DELAY:
                self.state.players[player_number].spawn_delay_counter += 1

                if self.state.players[player_number].spawn_delay_counter > self.state.players[player_number].spawn_delay_threshold:
                    self.state.players[player_number].player_state = TetrisState.SPAWN

            if self.state.players[player_number].player_state == TetrisState.DIE:
                self.die_counter += 1
                if self.die_counter >= 120:  # wait 2 seconds
                    for player in self.state.players:
                        player.player_state = TetrisState.GAME_OVER

            if self.state.players[player_number].player_state == TetrisState.GAME_OVER:
                self.state.game_over = True
                connection.set_state(self.state)
                self.switch('lobby')

        connection.set_state(self.state)
