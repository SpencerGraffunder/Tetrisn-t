from server.states.state import *
from common.components.tile import *  # Import like this to avoid having to do Tile. before everything
from common.components.piece import *
from common.components.player import *
import random
from collections import deque
import server.globals as g
from common.components.text import *
from common.game_state import GameState
from server.connection import Connection
from common.player_input import PlayerInput
from common.player_input import *
from server.constants import *
from server.clearing_line import *


class Game(State):
    def __init__(self):
        State.__init__(self)

        self.input = PlayerInput(None)
        self.das_threshold = 0
        self.spawn_delay_threshold = 10
        self.paused = False
        self.fall_threshold = FALL_DELAY_VALUES[0]
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
        self.clear_flag = False
        self.has_leveled_up = False

    def reset(self, player_input):
        g.state = GameState()

        g.state.board_width = (4 * g.state.player_count) + 6
        # Fill board with empty tiles
        g.state.board = [[Tile() for _ in range(g.state.board_width)] for _ in range(g.state.board_height+BOARD_HEIGHT_BUFFER)]

        # For testing multiplayer line clear

        for row in self.state.board[10:]:
            for tile_index, tile in enumerate(row):
                if tile_index < 12:
                    row[tile_index] = Tile(PieceType.I.value)

        g.state.current_level = player_input.starting_level
        # find the greatest level less than CURRENT_LEVEL in FALL_DELAY_VALUES and set the speed to that level's speed
        x = g.state.current_level
        while x >= 0:
            if x in FALL_DELAY_VALUES.keys():
                self.fall_threshold = FALL_DELAY_VALUES[x]
                break
            x -= 1
        self.lines_cleared = 10 * g.state.current_level
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
        self.clearing_lines = []
        self.clear_flag = False
        self.has_leveled_up = False


        # split the board into PLAYER_COUNT equal sections (using floats), find the middle of the section we care about using the average, and round to nearest column
        for player in g.state.players:
            player.spawn_column = int(((g.state.board_width / g.state.player_count) * player.player_number + (g.state.board_width / g.state.player_count) * (

    def do_event(self, event, player_number):

        if event.control == ControlType.QUIT:
            self.switch('lobby')

        # player controls: move and rotate
        for player in g.state.players:
            if player_number == player.player_number:
                if event.type == EventType.KEY_DOWN:

                    if g.state.players[player_number].active_piece is not None:
                        if event.control == ControlType.CCW:
                            if g.state.players[player_number].active_piece.can_rotate(g.state.board, g.state.players, Rotation.CCW):
                                g.state.players[player_number].active_piece.rotate(Rotation.CCW)
                                g.state.time_to_rotate = False
                        if event.control == ControlType.CW:
                            if g.state.players[player_number].active_piece.can_rotate(g.state.board, g.state.players, Rotation.CW):
                                g.state.players[player_number].active_piece.rotate(Rotation.CW)
                                self.time_to_rotate = False

                    if event.control == ControlType.LEFT:
                        g.state.players[player_number].is_move_left_pressed = True
                        g.state.players[player_number].das_threshold = 0
                        g.state.players[player_number].das_counter = 0
                        # if the other direction is being held, set this direction to override it; if not, it's False anyways
                        g.state.players[player_number].is_move_right_pressed = False
                    if event.control == ControlType.RIGHT:
                        g.state.players[player_number].is_move_right_pressed = True
                        g.state.players[player_number].das_threshold = 0
                        g.state.players[player_number].das_counter = 0
                        # if the other direction is being held, set this direction to override it; if not, it's False anyways
                        g.state.players[player_number].is_move_left_pressed = False
                    if event.control == ControlType.DOWN:
                        g.state.players[player_number].is_move_down_pressed = True
                        g.state.players[player_number].down_counter = 0

                if event.type == EventType.KEY_UP:
                    if event.control == ControlType.LEFT:
                        g.state.players[player_number].is_move_left_pressed = False
                    if event.control == ControlType.RIGHT:
                        g.state.players[player_number].is_move_right_pressed = False
                    if event.control == ControlType.DOWN:
                        g.state.players[player_number].is_move_down_pressed = False

    def lock_piece(self, player_number):
        piece_locked_into_another_piece = False
        max_row_index = 0

        for location in g.state.players[player_number].active_piece.locations:

            # Check if locked into another piece, which means game over
            if g.state.board[location[1]][location[0]].tile_type != TileType.BLANK:
                piece_locked_into_another_piece = True

            # Set tile type to the piece's tile type if single player, else set it to the player number
            if g.state.player_count == 1:
                tile_type = g.state.players[player_number].active_piece.tile_type
            else:
                tile_type = player_number

            g.state.board[location[1]][location[0]] = Tile(tile_type)
            if location[1] > max_row_index:
                max_row_index = location[1]

        # this was some weird frame data stuff based on emulating the 1989 NES version of Tetris (the wiki didn't go quite in-depth enough)
        if g.state.players[player_number].active_piece.piece_type == PieceType.I:
            g.state.players[player_number].spawn_delay_threshold = ((max_row_index+2)//4)*2+10
        else:
            g.state.players[player_number].spawn_delay_threshold = ((max_row_index+3)//4)*2+10

        # Keep track of if a line can be cleared to set the player's state
        was_line_added_to_list = False

        # Add all clearable lines to list
        for row_index, row in enumerate(g.state.board):
            can_clear = True
            for tile in row:
                if tile.tile_type == TileType.BLANK:
                    can_clear = False
            if can_clear:
                was_line_added_to_list = True
                line_in_clearing_lines = False
                for line in self.clearing_lines:
                    if line.board_index == row_index:
                        line_in_clearing_lines = True
                if not line_in_clearing_lines:
                    self.clearing_lines.append(ClearingLine(player_number, row_index, 20))

        # If a piece was added to clearing_lines
        if was_line_added_to_list:
            g.state.players[player_number].state = TetrisState.CLEAR
        else:
            g.state.players[player_number].state = TetrisState.SPAWN_DELAY

        g.state.players[player_number].active_piece = None
        if piece_locked_into_another_piece:
            for player in g.state.players:
                player.state = TetrisState.DIE

    def clear_lines(self):

        # Split the lines into two lists: those being cleared this frame, and others.
        future_clearing_lines = []
        present_clearing_lines = []
        for line in self.clearing_lines:
            line.decrement_counter()
            if line.counter <= 0:
                present_clearing_lines.append(line)
            else:
                future_clearing_lines.append(line)

        # Shift all the future lines down if they're above the present line
        for clearing_line in present_clearing_lines:
            for shifting_line in future_clearing_lines:
                if clearing_line.board_index > shifting_line.board_index:
                    shifting_line.board_index += 1

        # Clear the lines from the board
        for line in present_clearing_lines:
            # Pop the cleared line from the board
            g.state.board.pop(line.board_index)
            # Create a new line of blank tiles
            new_line = [Tile() for j in range(g.state.board_width)]
            # Append the new line to the beginning of the board
            g.state.board = [new_line] + g.state.board

        # Set clearing_lines to the list that doesn't contain cleared lines
        self.clearing_lines = future_clearing_lines

        # Update score

        present_lines_cleared = len(present_clearing_lines)
        self.state.score += SCORING_VALUES[present_lines_cleared] * (self.state.current_level + 1)

        # Update lines cleared and level
        if not self.has_leveled_up:
            if self.lines_cleared + present_lines_cleared >= 10 * (min(self.state.player_count, 3) + 2 * self.state.current_level):
                self.state.current_level += 1
                self.has_leveled_up = True
                # Set speed
                x = self.state.current_level
                while x >= 0:
                    if x in FALL_DELAY_VALUES.keys():
                        self.fall_threshold = FALL_DELAY_VALUES[x]
                        break
                    x -= 1
        else:
            if self.lines_cleared % (10 * self.level_up_calculation_player_count) + present_lines_cleared >= 10 * self.level_up_calculation_player_count:
                self.state.current_level += 1
                # Set speed
                x = self.state.current_level
                while x >= 0:
                    if x in FALL_DELAY_VALUES.keys():
                        self.fall_threshold = FALL_DELAY_VALUES[x]
                        break
                    x -= 1

        self.lines_cleared += present_lines_cleared
        print(self.lines_cleared)

    def update(self):

        while g.connection.player_inputs:
            self.input = g.connection.get_player_input()

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
        for player_number in range(g.state.player_count):
            if g.state.players[player_number].is_move_left_pressed or g.state.players[player_number].is_move_right_pressed:
                g.state.players[player_number].das_counter += 1

        self.clear_lines()

        # STATES SECTION START
        for player_number in range(g.state.player_count):
            player = g.state.players[player_number]

            if player.state == TetrisState.SPAWN:

                # if the game just started or the next piece can spawn into the board (only checking other players' pieces, not the piece tiles on the board)
                if player.next_piece is None or player.next_piece.can_move(g.state.board, g.state.players, None) == MoveAllowance.CAN:

                    player.spawn_delay_counter += 1

                    # Spawn piece
                    # RNG piece choice decision
                    if player.next_piece_type is None:
                        active_piece_type = random.choice([PieceType.I, PieceType.O, PieceType.T, PieceType.L, PieceType.J, PieceType.Z, PieceType.S])
                    else:
                        active_piece_type = player.next_piece.piece_type
                    player.next_piece_type = random.choice([PieceType.I, PieceType.O, PieceType.T, PieceType.L, PieceType.J, PieceType.Z, PieceType.S])
                    # Reroll the piece type if there are two in a row
                    if player.next_piece_type == active_piece_type:
                        player.next_piece_type = random.choice([PieceType.I, PieceType.O, PieceType.T, PieceType.L, PieceType.J, PieceType.Z, PieceType.S])
                    player.active_piece = Piece(active_piece_type, player_number, player.spawn_column, g.state.player_count)  # this puts the active piece in the board
                    player.next_piece = Piece(player.next_piece_type, player_number, player.spawn_column, g.state.player_count)  # this puts the next piece in the next piece box
                    player.state = TetrisState.PLAY
                    player.fall_counter = 0
                    player.spawn_delay_counter = 0

            if player.state == TetrisState.PLAY:
                # Move piece logic
                if player.is_move_left_pressed or player.is_move_right_pressed:

                    # see if the das counter is above the das threshold, which is one of three values given the player count based on if the key was just pressed (das_threshold == 0), else
                    # {if first das threshold was passed for that l/r keypress (das_threshold == DAS_VALUES[g.state.player_count][1]), else (das_threshold == DAS_VALUES[g.state.player_count][0])}
                    # this way the first time the button is pressed, the piece moves (and if there's a piece in the way and then there isn't, it moves)
                    # furthermore, once the initial nonzero das_threshold (DAS_VALUES[g.state.player_count][1]) is passed, then das_threshold becomes smaller (DAS_VALUES[g.state.player_count][0])
                    # so that the piece moves faster after the player surely wants the game to start moving the piece for them

                    # special case: if a direction is held for a long time and the active piece is against another piece (either placed or another player's piece), the das_counter shouldn't be reset
                    # if the piece can move again because the input is being made for auto shift, so if das_counter == 0, we want to just subtract 1 off das_threshold unless it comes within
                    # DAS_VALUES[g.state.player_count][0] of DAS_VALUES[g.state.player_count][1], in which case we want it to be DAS_VALUES[g.state.player_count][1] - DAS_VALUES[g.state.player_count][0]

                    # the special case's code also makes it work to buffer auto shift during a piece's spawn delay time or a line clear animation
                    if player.das_counter > player.das_threshold:
                        move_direction = None
                        if player.is_move_left_pressed:
                            move_direction = Direction.LEFT
                        elif player.is_move_right_pressed:
                            move_direction = Direction.RIGHT
                        # if the piece can move, move it and do DAS stuff
                        if player.active_piece.can_move(g.state.board, g.state.players, move_direction) == MoveAllowance.CAN:
                            player.active_piece.move(move_direction)
                            # make sure das_threshold is no longer zero for this move input and set das_counter back accordingly
                            if player.das_threshold == 0:
                                player.das_threshold = DAS_VALUES[g.state.player_count][1]
                                # set das_counter as explained in the special case
                                if player.das_counter + DAS_VALUES[g.state.player_count][0] > DAS_VALUES[g.state.player_count][1]:
                                    player.das_counter = DAS_VALUES[g.state.player_count][1] - DAS_VALUES[g.state.player_count][0]
                                else:
                                    player.das_counter -= 1
                            else:
                                player.das_threshold = DAS_VALUES[g.state.player_count][0]
                                player.das_counter = 0

                if player.is_move_down_pressed:
                    player.down_counter += 1

                    if player.down_counter > 2:
                        if player.is_move_down_pressed:
                            if player.active_piece.can_move(g.state.board, g.state.players, Direction.DOWN) == MoveAllowance.CAN:
                                player.active_piece.move(Direction.DOWN)
                                player.fall_counter = 0
                            elif player.active_piece.can_move(g.state.board, g.state.players, Direction.DOWN) == MoveAllowance.CANT_BOARD:
                                self.lock_piece(player_number)
                            elif player.active_piece.can_move(g.state.board, g.state.players, Direction.DOWN) == MoveAllowance.CANT_PIECE:
                                pass

                            player.down_counter = 0

                player.fall_counter += 1

                if player.fall_counter >= self.fall_threshold and player.active_piece is not None:
                    if player.active_piece.can_move(g.state.board, g.state.players, Direction.DOWN) == MoveAllowance.CANT_BOARD:
                        self.lock_piece(player_number)
                    elif player.active_piece.can_move(g.state.board, g.state.players, Direction.DOWN) == MoveAllowance.CAN:
                        player.active_piece.move(Direction.DOWN)
                    elif player.active_piece.can_move(g.state.board, g.state.players, Direction.DOWN) == MoveAllowance.CANT_PIECE:
                        pass
                    player.fall_counter = 0

            if player.state == TetrisState.CLEAR:
                is_being_cleared = False
                for line in self.clearing_lines:
                    if line.player_number == player.player_number:
                        is_being_cleared = True
                if not is_being_cleared:
                    player.state = TetrisState.SPAWN_DELAY

            elif player.state == TetrisState.SPAWN_DELAY:
                player.spawn_delay_counter += 1

                player.is_move_down_pressed = False

                if player.spawn_delay_counter > player.spawn_delay_threshold:
                    player.state = TetrisState.SPAWN

            if player.state == TetrisState.DIE:
                self.die_counter += 1
                # wait 2 seconds
                if self.die_counter >= 120:
                    for player in g.state.players:
                        player.state = TetrisState.GAME_OVER

            if player.state == TetrisState.GAME_OVER:
                g.state.game_over = True
                g.connection.add_game_state(g.state)
                self.switch('lobby')

        g.connection.add_game_state(g.state)
