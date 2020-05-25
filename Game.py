import pygame
from States import *
import sys
import os
from Tile import * # Import like this to avoid having to do Tile. before everything
from Piece import *
from Player import *
import random
from collections import deque
import Globals
from Constants import *
from Text import *

class Game(States):

    def __init__(self):

        States.__init__(self)

        self.next = 'pause menu'

        self.das_threshold = 0
        self.spawn_delay_threshold = 10

        self.sprites = {}
        # load sprites
        if getattr(sys, 'frozen', False):
            # if running from a single executable, get some path stuff to make it work
            wd = sys._MEIPASS
        else:
            wd = ''
        # Load sprites from image files and convert for performance
        self.sprites[TILE_TYPE_BLANK] = pygame.image.load(os.path.join(wd,'backgroundblock.bmp')).convert()
        self.sprites[TILE_TYPE_IOT]   = pygame.image.load(os.path.join(wd,'IOTblock.bmp')).convert()
        self.sprites[TILE_TYPE_JS]    = pygame.image.load(os.path.join(wd,'JSblock.bmp')).convert()
        self.sprites[TILE_TYPE_LZ]    = pygame.image.load(os.path.join(wd,'LZblock.bmp')).convert()

        self.reset()


    def reset(self):

        # Fill board with empty tiles
        self.board = [[Tile() for j in range(Globals.BOARD_WIDTH)] for i in range(Globals.BOARD_HEIGHT+BOARD_HEIGHT_BUFFER)]

        # find the greatest level less than CURRENT_LEVEL in FALL_DELAY_VALUES and set the speed to that level's speed
        x = Globals.CURRENT_LEVEL
        while x >= 0:
            if x in FALL_DELAY_VALUES.keys():
                self.fall_threshold = FALL_DELAY_VALUES[x]
                break
            x -= 1
        self.last_lock_position = 0
        self.lines_cleared = 10 * Globals.CURRENT_LEVEL
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

        self.players = [Player(x, Globals.BOARD_WIDTH) for x in range(Globals.PLAYER_COUNT)]


    def do_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKQUOTE:
                pdb.set_trace()

        for player_number in range(Globals.PLAYER_COUNT):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next = 'pause menu'
                    self.done = True

                if self.players[player_number].active_piece != None:
                    if event.key == KEYBINDINGS[player_number][KEYBINDING_CCW]:
                        if self.players[player_number].active_piece.can_rotate(self.board, self.players, ROTATION_CCW):
                            self.players[player_number].active_piece.rotate(ROTATION_CCW)
                            self.time_to_rotate = False
                    if event.key == KEYBINDINGS[player_number][KEYBINDING_CW]:
                        if self.players[player_number].active_piece.can_rotate(self.board, self.players, ROTATION_CW):
                            self.players[player_number].active_piece.rotate(ROTATION_CW)
                            self.time_to_rotate = False

                if event.key == KEYBINDINGS[player_number][KEYBINDING_LEFT]:
                    self.players[player_number].is_move_left_pressed = True
                    self.players[player_number].das_threshold = 0
                    self.players[player_number].das_counter = 0
                if event.key == KEYBINDINGS[player_number][KEYBINDING_RIGHT]:
                    self.players[player_number].is_move_right_pressed = True
                    self.players[player_number].das_threshold = 0
                    self.players[player_number].das_counter = 0
                if event.key == KEYBINDINGS[player_number][KEYBINDING_DOWN]:
                    self.players[player_number].is_move_down_pressed = True
                    self.players[player_number].down_counter = 0
                    self.players[player_number].das_counter = 0

            if event.type == pygame.KEYUP:
                if event.key == KEYBINDINGS[player_number][KEYBINDING_LEFT]:
                    self.players[player_number].is_move_left_pressed = False
                    self.players[player_number].das_counter = 0
                if event.key == KEYBINDINGS[player_number][KEYBINDING_RIGHT]:
                    self.players[player_number].is_move_right_pressed = False
                    self.players[player_number].das_counter = 0
                if event.key == KEYBINDINGS[player_number][KEYBINDING_DOWN]:
                    self.players[player_number].is_move_down_pressed = False


    def lock_piece(self, player_number):

        piece_locked_into_another_piece = False
        max_row_index = 0
        for location in self.players[player_number].active_piece.locations:
            if self.board[location[1]][location[0]].tile_type != TILE_TYPE_BLANK:
                piece_locked_into_another_piece = True
            self.board[location[1]][location[0]] = Tile(self.players[player_number].active_piece.tile_type)
            if location[1] > max_row_index:
                max_row_index = location[1]

        if self.players[player_number].active_piece.piece_type == PIECE_TYPE_I:
            self.players[player_number].spawn_delay_threshold = ((max_row_index+2)//4)*2+10
        else:
            self.players[player_number].spawn_delay_threshold = ((max_row_index+1+2)//4)*2+10

        self.players[player_number].active_piece = None
        if piece_locked_into_another_piece == False:
            self.players[player_number].player_state = TETRIS_STATE_CHECK_CLEAR
        else:
            for player in self.players:
                player.player_state = TETRIS_STATE_DIE


    def update(self, dt):

        if Globals.GAME_JUST_STARTED:
            self.reset()
            Globals.GAME_JUST_STARTED = False

        for player_number in range(Globals.PLAYER_COUNT):

            if self.players[player_number].player_state == TETRIS_STATE_SPAWN:

                if self.players[player_number].next_piece == None or self.players[player_number].next_piece.can_move(self.board, self.players, None) == CAN_MOVE:

                    self.players[player_number].spawn_delay_counter += 1

                    if self.players[player_number].spawn_delay_counter > self.players[player_number].spawn_delay_threshold:

                        # Spawn piece
                        # RNG piece choice decision
                        if self.players[player_number].next_piece_type == None:
                            active_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
                        else:
                            active_piece_type = self.players[player_number].next_piece.piece_type
                        self.players[player_number].next_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
                        if self.players[player_number].next_piece_type == active_piece_type:
                            self.players[player_number].next_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
                        self.players[player_number].active_piece = Piece(active_piece_type, player_number, self.players[player_number].spawn_column) # this puts the active piece in the board
                        self.players[player_number].next_piece   = Piece(self.players[player_number].next_piece_type, player_number, self.players[player_number].spawn_column) # this puts the next piece in the next piece box
                        self.players[player_number].player_state = TETRIS_STATE_PLAY
                        self.players[player_number].fall_counter = 0
                        self.players[player_number].spawn_delay_counter = 0

            if self.players[player_number].player_state == TETRIS_STATE_PLAY:
                # Move piece logic
                if self.players[player_number].is_move_left_pressed or self.players[player_number].is_move_right_pressed:
                    self.players[player_number].das_counter += 1

                    if self.players[player_number].das_counter > self.players[player_number].das_threshold:
                        if self.players[player_number].is_move_left_pressed:
                            if self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_LEFT) == CAN_MOVE:
                                self.players[player_number].active_piece.move(DIRECTION_LEFT)
                                self.players[player_number].das_counter = 0
                                if self.players[player_number].das_threshold == 0:
                                    self.players[player_number].das_threshold = DAS_VALUES[Globals.PLAYER_COUNT][1]
                                else:
                                    self.players[player_number].das_threshold = DAS_VALUES[Globals.PLAYER_COUNT][0]
                        if self.players[player_number].is_move_right_pressed:
                            if self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_RIGHT) == CAN_MOVE:
                                self.players[player_number].active_piece.move(DIRECTION_RIGHT)
                                self.players[player_number].das_counter = 0
                                if self.players[player_number].das_threshold == 0:
                                    self.players[player_number].das_threshold = DAS_VALUES[Globals.PLAYER_COUNT][1]
                                else:
                                    self.players[player_number].das_threshold = DAS_VALUES[Globals.PLAYER_COUNT][0]

                if self.players[player_number].is_move_down_pressed:
                    self.players[player_number].down_counter += 1

                    if self.players[player_number].down_counter > 2:
                        if self.players[player_number].is_move_down_pressed:
                            if self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_DOWN) == CAN_MOVE:
                                self.players[player_number].active_piece.move(DIRECTION_DOWN)
                                self.players[player_number].fall_counter = 0
                            elif self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_DOWN) == CANT_MOVE_BOARD:
                                self.lock_piece(player_number)
                            elif self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_DOWN) == CANT_MOVE_PIECE:
                                pass

                            self.players[player_number].down_counter = 0

                self.players[player_number].fall_counter += 1

                if self.players[player_number].fall_counter >= self.fall_threshold and self.players[player_number].active_piece != None:
                    if   self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_DOWN) == CANT_MOVE_BOARD:
                        self.lock_piece(player_number)
                    elif self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_DOWN) == CAN_MOVE:
                        self.players[player_number].active_piece.move(DIRECTION_DOWN)
                    elif self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_DOWN) == CANT_MOVE_PIECE:
                        pass
                    self.players[player_number].fall_counter = 0


            elif self.players[player_number].player_state == TETRIS_STATE_CHECK_CLEAR:
                # Store all lines that can be cleared
                self.players[player_number].lines_to_clear = []

                self.players[player_number].is_move_down_pressed = False

                # Add all clearable lines to list
                for row_index, row in enumerate(self.board):
                    can_clear = True
                    for tile in row:
                        if tile.tile_type == TILE_TYPE_BLANK:
                            can_clear = False
                    if can_clear:
                        for player in self.players:
                            if Globals.PLAYER_COUNT > 1:
                                if player != self.players[player_number]:
                                    if row_index not in player.lines_to_clear:
                                        self.players[player_number].lines_to_clear.append(row_index)
                            else:
                                self.players[player_number].lines_to_clear.append(row_index)

                if len(self.players[player_number].lines_to_clear) > 0:
                    self.players[player_number].player_state = TETRIS_STATE_CLEAR
                    self.players[player_number].clear_animation_counter = 0
                elif len(self.players[player_number].lines_to_clear) == 0:
                    self.players[player_number].player_state = TETRIS_STATE_SPAWN_DELAY

            if self.players[player_number].player_state == TETRIS_STATE_CLEAR:
                animation_length = self.spawn_delay_threshold + 20
                self.players[player_number].clear_animation_counter += 1

                if self.players[player_number].clear_animation_counter >= animation_length:
                    # Move upper lines down
                    for line in self.players[player_number].lines_to_clear:
                        self.board.pop(line)
                        self.board = deque(self.board)
                        self.board.appendleft([Tile() for j in range(Globals.BOARD_WIDTH)])
                        self.board = list(self.board)

                    num_lines = len(self.players[player_number].lines_to_clear)
                    new_lines_to_clear = []

                    if Globals.PLAYER_COUNT > 1:
                        for player in self.players:
                            if player != self.players[player_number]:
                                for line_index in player.lines_to_clear:
                                    for line_to_clear in self.players[player_number].lines_to_clear:
                                        if line_index < line_to_clear:
                                            new_lines_to_clear.append(line_index + num_lines)
                                        else:
                                            new_lines_to_clear.append(line_index)

                        self.players[(player_number + 1) % 2].lines_to_clear = new_lines_to_clear

                    # Score the points
                    if num_lines != 0:
                        if num_lines == 1:
                            self.score += 40 * (Globals.CURRENT_LEVEL + 1)
                        elif num_lines == 2:
                            self.score += 100 * (Globals.CURRENT_LEVEL + 1)
                        elif num_lines == 3:
                            self.score += 300 * (Globals.CURRENT_LEVEL + 1)
                        elif num_lines == 4: # BOOM Tetrisn't for Jeffn't
                            self.score += 1200 * (Globals.CURRENT_LEVEL + 1)

                        self.lines_cleared += len(self.players[player_number].lines_to_clear)
                        if self.lines_cleared // 10 >= Globals.CURRENT_LEVEL + 1:
                            Globals.CURRENT_LEVEL += 1

                        if Globals.CURRENT_LEVEL in FALL_DELAY_VALUES.keys():
                            self.fall_threshold = FALL_DELAY_VALUES[Globals.CURRENT_LEVEL]

                    self.players[player_number].player_state = TETRIS_STATE_SPAWN
                    self.players[player_number].lines_to_clear = []

            elif self.players[player_number].player_state == TETRIS_STATE_SPAWN_DELAY:
                self.players[player_number].spawn_delay_counter += 1

                if self.players[player_number].spawn_delay_counter > self.spawn_delay_threshold:
                    self.players[player_number].player_state = TETRIS_STATE_SPAWN

            if self.players[player_number].player_state == TETRIS_STATE_DIE:
                self.die_counter += 1
                if self.die_counter >= 120: # wait 2 seconds
                    for player in self.players:
                        player.player_state = TETRIS_STATE_GAME_OVER

            if self.players[player_number].player_state == TETRIS_STATE_GAME_OVER:
                self.next = 'game over'
                self.done = True


    def draw(self, screen):

        screen.fill((150, 150, 150))

        centering_offset = (Globals.WINDOW_WIDTH - (Globals.TILE_SIZE * Globals.BOARD_WIDTH)) // 2

        for row_index, tile_row in enumerate(self.board[2:]):
            for col_index, tile in enumerate(tile_row):
                scaled_image = pygame.transform.scale(self.sprites[tile.tile_type], (Globals.TILE_SIZE, Globals.TILE_SIZE))
                screen.blit(scaled_image, (col_index * Globals.TILE_SIZE + centering_offset, row_index * Globals.TILE_SIZE))

        for player in self.players:

            # to determine spawn positions
            if Globals.BOARD_WIDTH % 2 == 0: # even board width
                center = Globals.BOARD_WIDTH // 2
            elif Globals.BOARD_WIDTH % 2 == 1: # odd board width
                center = (Globals.BOARD_WIDTH+1) // 2

            # Draw active piece
            if player.active_piece != None:
                for location in player.active_piece.locations:
                    scaled_image = pygame.transform.scale(self.sprites[player.active_piece.tile_type], (Globals.TILE_SIZE, Globals.TILE_SIZE))
                    screen.blit(scaled_image, (location[0] * Globals.TILE_SIZE + centering_offset, (location[1] - BOARD_HEIGHT_BUFFER) * Globals.TILE_SIZE))

            # Draw next piece
            if player.player_number != None and player.next_piece != None:
                self.draw_next_piece(screen, player.player_number)

        # display score
        score_title = 'Score:'
        text.draw(screen, score_title, 'SMALL', ((Globals.WINDOW_WIDTH) - (4 * Globals.TILE_SIZE), (Globals.BOARD_HEIGHT - 3) * Globals.TILE_SIZE), (0, 128, 0))

        score_val = '%d' % (self.score)
        text.draw(screen, score_val,   'SMALL', ((Globals.WINDOW_WIDTH) - (4 * Globals.TILE_SIZE), (Globals.BOARD_HEIGHT - 2) * Globals.TILE_SIZE), (0, 128, 0))

        # display level
        level_str = 'Level: %d' % (Globals.CURRENT_LEVEL)
        text.draw(screen, level_str,   'SMALL', ((Globals.WINDOW_WIDTH) - (4 * Globals.TILE_SIZE), (Globals.BOARD_HEIGHT - 4) * Globals.TILE_SIZE), (0, 128, 0))


    def draw_next_piece(self, screen, player_number):

        screen_center_x = Globals.WINDOW_WIDTH // 2
        player = self.players[player_number]

        if player_number%2 == 0:
            # should be drawn on the left
            x_offset = screen_center_x-(((Globals.BOARD_WIDTH//2)+(3))*Globals.TILE_SIZE)
        else:
            # draw on the right
            x_offset = screen_center_x+(((Globals.BOARD_WIDTH//2)+(3))*Globals.TILE_SIZE)

        y_offset = (player_number//2)*((7)*Globals.TILE_SIZE)

        for tile in player.next_piece.locations:
            scaled_image = pygame.transform.scale(self.sprites[player.next_piece.tile_type], (Globals.TILE_SIZE, Globals.TILE_SIZE))
            screen.blit(scaled_image, (x_offset+((tile[0]-player.spawn_column)*Globals.TILE_SIZE), (tile[1])*Globals.TILE_SIZE+y_offset))