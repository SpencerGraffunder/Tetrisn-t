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
import pdb


class Game(State):
    def __init__(self):
        State.__init__(self)

        self.state = GameState()
        self.input = PlayerInput()
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

        self.reset(self.input)

    def reset(self, player_input):
        self.state = GameState()
        self.state.player_count = player_input.player_count

        self.state.board_width = (4 * self.state.player_count) + 6
        # Fill board with empty tiles
        self.state.board = [[Tile() for _ in range(self.state.board_width)] for _ in range(g.board_height+BOARD_HEIGHT_BUFFER)]

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

        self.state.players = [Player(x, self.state.board_width) for x in range(self.state.player_count)]
        for player in self.state.players:
            player.spawn_column = int(((self.state.board_width / self.state.player_count) * player.player_number + (self.state.board_width / self.state.player_count) * (player.player_number + 1)) / 2)

    def do_event(self, event):

        if event.type == pygame.QUIT:
            self.switch('lobby')
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKQUOTE:
                pdb.set_trace()

        for player_number in range(self.state.player_count):
            if event.type == pygame.KEYDOWN:

                if self.state.players[player_number].active_piece is not None:
                    if event.key == KEYBINDINGS[player_number][KEYBINDING_CCW]:
                        if self.state.players[player_number].active_piece.can_rotate(self.state.board, self.state.players, ROTATION_CCW):
                            self.state.players[player_number].active_piece.rotate(ROTATION_CCW)
                            self.state.time_to_rotate = False
                    if event.key == KEYBINDINGS[player_number][KEYBINDING_CW]:
                        if self.state.players[player_number].active_piece.can_rotate(self.state.board, self.state.players, ROTATION_CW):
                            self.state.players[player_number].active_piece.rotate(ROTATION_CW)
                            self.time_to_rotate = False

                if event.key == KEYBINDINGS[player_number][KEYBINDING_LEFT]:
                    self.state.players[player_number].is_move_left_pressed = True
                    self.state.players[player_number].das_threshold = 0
                    self.state.players[player_number].das_counter = 0
                if event.key == KEYBINDINGS[player_number][KEYBINDING_RIGHT]:
                    self.state.players[player_number].is_move_right_pressed = True
                    self.state.players[player_number].das_threshold = 0
                    self.state.das_counter = 0
                if event.key == KEYBINDINGS[player_number][KEYBINDING_DOWN]:
                    self.state.players[player_number].is_move_down_pressed = True
                    self.state.players[player_number].down_counter = 0

            if event.type == pygame.KEYUP:
                if event.key == KEYBINDINGS[player_number][KEYBINDING_LEFT]:
                    self.state.players[player_number].is_move_left_pressed = False
                    self.state.players[player_number].das_counter = 0
                if event.key == KEYBINDINGS[player_number][KEYBINDING_RIGHT]:
                    self.state.players[player_number].is_move_right_pressed = False
                    self.state.players[player_number].das_counter = 0
                if event.key == KEYBINDINGS[player_number][KEYBINDING_DOWN]:
                    self.state.players[player_number].is_move_down_pressed = False
                    self.state.players[player_number].das_counter = 0

    def lock_piece(self, player_number):

        piece_locked_into_another_piece = False
        max_row_index = 0
        for location in self.state.players[player_number].active_piece.locations:
            if self.state.board[location[1]][location[0]].tile_type != TILE_TYPE_BLANK:
                piece_locked_into_another_piece = True
            self.state.board[location[1]][location[0]] = Tile(self.state.players[player_number].active_piece.tile_type)
            if location[1] > max_row_index:
                max_row_index = location[1]

        if self.state.players[player_number].active_piece.piece_type == PIECE_TYPE_I:
            self.state.players[player_number].spawn_delay_threshold = ((max_row_index+2)//4)*2+10
        else:
            self.state.players[player_number].spawn_delay_threshold = ((max_row_index+1+2)//4)*2+10

        self.state.players[player_number].active_piece = None
        if not piece_locked_into_another_piece:
            self.state.players[player_number].player_state = TETRIS_STATE_CHECK_CLEAR
        else:
            for player in self.state.players:
                player.player_state = TETRIS_STATE_DIE

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
                self.do_event(event)

        if self.paused:
            return
        for player_number in range(self.state.player_count):

            if self.state.players[player_number].player_state == TETRIS_STATE_SPAWN:

                if self.state.players[player_number].next_piece is None or self.state.players[player_number].next_piece.can_move(self.state.board, self.state.players, None) == CAN_MOVE:

                    self.state.players[player_number].spawn_delay_counter += 1

                    if self.state.players[player_number].spawn_delay_counter > self.state.players[player_number].spawn_delay_threshold:

                        # Spawn piece
                        # RNG piece choice decision
                        if self.state.players[player_number].next_piece_type is None:
                            active_piece_type = random.choice([PIECE_TYPE_I, PIECE_TYPE_O, PIECE_TYPE_T, PIECE_TYPE_L, PIECE_TYPE_J, PIECE_TYPE_Z, PIECE_TYPE_S])
                        else:
                            active_piece_type = self.state.players[player_number].next_piece.piece_type
                        self.state.players[player_number].next_piece_type = random.choice([PIECE_TYPE_I, PIECE_TYPE_O, PIECE_TYPE_T, PIECE_TYPE_L, PIECE_TYPE_J, PIECE_TYPE_Z, PIECE_TYPE_S])
                        if self.state.players[player_number].next_piece_type == active_piece_type:
                            self.state.players[player_number].next_piece_type = random.choice([PIECE_TYPE_I, PIECE_TYPE_O, PIECE_TYPE_T, PIECE_TYPE_L, PIECE_TYPE_J, PIECE_TYPE_Z, PIECE_TYPE_S])
                        self.state.players[player_number].active_piece = Piece(active_piece_type, player_number, self.state.players[player_number].spawn_column)  # this puts the active piece in the board
                        self.state.players[player_number].next_piece = Piece(self.state.players[player_number].next_piece_type, player_number, self.state.players[player_number].spawn_column)  # this puts the next piece in the next piece box
                        self.state.players[player_number].player_state = TETRIS_STATE_PLAY
                        self.state.players[player_number].fall_counter = 0
                        self.state.players[player_number].spawn_delay_counter = 0

            if self.state.players[player_number].player_state == TETRIS_STATE_PLAY:
                # Move piece logic
                if self.state.players[player_number].is_move_left_pressed or self.state.players[player_number].is_move_right_pressed:
                    self.state.players[player_number].das_counter += 1

                    if self.state.players[player_number].das_counter > self.state.players[player_number].das_threshold:
                        if self.state.players[player_number].is_move_left_pressed:
                            if self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, DIRECTION_LEFT) == CAN_MOVE:
                                self.state.players[player_number].active_piece.move(DIRECTION_LEFT)
                                self.state.players[player_number].das_counter = 0
                                if self.state.players[player_number].das_threshold == 0:
                                    self.state.players[player_number].das_threshold = DAS_VALUES[self.state.player_count][1]
                                else:
                                    self.state.players[player_number].das_threshold = DAS_VALUES[self.state.player_count][0]
                        if self.state.players[player_number].is_move_right_pressed:
                            if self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, DIRECTION_RIGHT) == CAN_MOVE:
                                self.state.players[player_number].active_piece.move(DIRECTION_RIGHT)
                                self.state.players[player_number].das_counter = 0
                                if self.state.players[player_number].das_threshold == 0:
                                    self.state.players[player_number].das_threshold = DAS_VALUES[self.state.player_count][1]
                                else:
                                    self.state.players[player_number].das_threshold = DAS_VALUES[self.state.player_count][0]

                if self.state.players[player_number].is_move_down_pressed:
                    self.state.players[player_number].down_counter += 1

                    if self.state.players[player_number].down_counter > 2:
                        if self.state.players[player_number].is_move_down_pressed:
                            if self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, DIRECTION_DOWN) == CAN_MOVE:
                                self.state.players[player_number].active_piece.move(DIRECTION_DOWN)
                                self.state.players[player_number].fall_counter = 0
                            elif self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, DIRECTION_DOWN) == CANT_MOVE_BOARD:
                                self.lock_piece(player_number)
                            elif self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, DIRECTION_DOWN) == CANT_MOVE_PIECE:
                                pass

                            self.state.players[player_number].down_counter = 0

                self.state.players[player_number].fall_counter += 1

                if self.state.players[player_number].fall_counter >= self.fall_threshold and self.state.players[player_number].active_piece is not None:
                    if self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, DIRECTION_DOWN) == CANT_MOVE_BOARD:
                        self.lock_piece(player_number)
                    elif self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, DIRECTION_DOWN) == CAN_MOVE:
                        self.state.players[player_number].active_piece.move(DIRECTION_DOWN)
                    elif self.state.players[player_number].active_piece.can_move(self.state.board, self.state.players, DIRECTION_DOWN) == CANT_MOVE_PIECE:
                        pass
                    self.state.players[player_number].fall_counter = 0

            elif self.state.players[player_number].player_state == TETRIS_STATE_CHECK_CLEAR:
                # Store all lines that can be cleared
                self.state.players[player_number].lines_to_clear = []

                self.state.players[player_number].is_move_down_pressed = False

                # Add all clearable lines to list
                for row_index, row in enumerate(self.state.board):
                    can_clear = True
                    for tile in row:
                        if tile.tile_type == TILE_TYPE_BLANK:
                            can_clear = False
                    if can_clear:
                        for player in self.state.players:
                            if self.state.player_count > 1:
                                if player != self.state.players[player_number]:
                                    if row_index not in player.lines_to_clear:
                                        self.state.players[player_number].lines_to_clear.append(row_index)
                            else:
                                self.state.players[player_number].lines_to_clear.append(row_index)

                if len(self.state.players[player_number].lines_to_clear) > 0:
                    self.state.players[player_number].player_state = TETRIS_STATE_CLEAR
                    self.state.players[player_number].clear_animation_counter = 0
                elif len(self.state.players[player_number].lines_to_clear) == 0:
                    self.state.players[player_number].player_state = TETRIS_STATE_SPAWN_DELAY

            if self.state.players[player_number].player_state == TETRIS_STATE_CLEAR:
                animation_length = self.spawn_delay_threshold + 20
                self.state.players[player_number].clear_animation_counter += 1

                if self.state.players[player_number].clear_animation_counter >= animation_length:
                    # Move upper lines down
                    for line in self.state.players[player_number].lines_to_clear:
                        self.state.board.pop(line)
                        self.state.board = deque(self.state.board)
                        self.state.board.appendleft([Tile() for _ in range(self.state.board_width)])
                        self.state.board = list(self.state.board)

                    num_lines = len(self.state.players[player_number].lines_to_clear)
                    new_lines_to_clear = []

                    if self.state.player_count > 1:
                        for player in self.state.players:
                            if player != self.state.players[player_number]:
                                for line_index in player.lines_to_clear:
                                    for line_to_clear in self.state.players[player_number].lines_to_clear:
                                        if line_index < line_to_clear:
                                            new_lines_to_clear.append(line_index + num_lines)
                                        else:
                                            new_lines_to_clear.append(line_index)

                        self.state.players[(player_number + 1) % 2].lines_to_clear = new_lines_to_clear

                    # Score the points
                    if num_lines != 0:
                        if num_lines == 1:
                            self.state.score += 40 * (self.state.current_level + 1)
                        elif num_lines == 2:
                            self.state.score += 100 * (self.state.current_level + 1)
                        elif num_lines == 3:
                            self.state.score += 300 * (self.state.current_level + 1)
                        elif num_lines == 4:  # BOOM Tetrisn't for Jeffn't
                            self.state.score += 1200 * (self.state.current_level + 1)

                        self.lines_cleared += len(self.state.players[player_number].lines_to_clear)
                        if self.lines_cleared // 10 >= self.state.current_level + 1:
                            self.state.current_level += 1

                        if self.state.current_level in FALL_DELAY_VALUES.keys():
                            self.fall_threshold = FALL_DELAY_VALUES[self.state.current_level]

                    self.state.players[player_number].player_state = TETRIS_STATE_SPAWN
                    self.state.players[player_number].lines_to_clear = []

            elif self.state.players[player_number].player_state == TETRIS_STATE_SPAWN_DELAY:
                self.state.players[player_number].spawn_delay_counter += 1

                if self.state.players[player_number].spawn_delay_counter > self.spawn_delay_threshold:
                    self.state.players[player_number].player_state = TETRIS_STATE_SPAWN

            if self.state.players[player_number].player_state == TETRIS_STATE_DIE:
                self.die_counter += 1
                if self.die_counter >= 120:  # wait 2 seconds
                    for player in self.state.players:
                        player.player_state = TETRIS_STATE_GAME_OVER

            if self.state.players[player_number].player_state == TETRIS_STATE_GAME_OVER:
                self.state.game_over = True
                connection.set_state(self.state)
                self.switch('lobby')

        connection.set_state(self.state)