import pygame
from lib.states.States import *
import sys
import os
from lib.components.Tile import *  # Import like this to avoid having to do Tile. before everything
from lib.components.Piece import *
from lib.components.Player import *
import random
from collections import deque
import lib.Globals as Globals
import lib.Constants as Constants
from lib.components.Text import *
from lib.Connection import PlayerInput



class ClientGame(States):
    def __init__(self):

        States.__init__(self)

        self.next = 'main menu'

        self.das_threshold = 0
        self.spawn_delay_threshold = 10
        self.state = Globals.connection.get_state()

        self.sprites = {}
        # load sprites
        if getattr(sys, 'frozen', False):
            # if running from a single executable, get some path stuff to make it work
            wd = sys._MEIPASS
        else:
            wd = ''
        # Load sprites from image files and convert for performance
        self.sprites[TILE_TYPE_BLANK] = pygame.image.load(
            os.path.join(wd, 'resources', 'backgroundblock.bmp')).convert()
        self.sprites[TILE_TYPE_IOT] = pygame.image.load(
            os.path.join(wd, 'resources', 'IOTblock.bmp')).convert()
        self.sprites[TILE_TYPE_JS] = pygame.image.load(
            os.path.join(wd, 'resources', 'JSblock.bmp')).convert()
        self.sprites[TILE_TYPE_LZ] = pygame.image.load(
            os.path.join(wd, 'resources', 'LZblock.bmp')).convert()

    def do_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKQUOTE:
                pdb.set_trace()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_input = PlayerInput()
                pause_input.pause_game()
                Globals.connection.add_input(pause_input)
                self.switch('pause menu')


    def update(self, dt):
        player_input = PlayerInput()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            player_input.add_event(event)
            self.do_event(event)

        Globals.connection.add_input(player_input)
        self.state = Globals.connection.get_state()
        if self.state.game_over:
            self.switch('game over')

    def draw(self, screen):
        screen.fill((150, 150, 150))

        centering_offset = (Constants.WINDOW_WIDTH - (
                    self.state.tile_size * self.state.board_width)) // 2

        for row_index, tile_row in enumerate(self.state.board[2:]):
            for col_index, tile in enumerate(tile_row):
                scaled_image = pygame.transform.scale(
                    self.sprites[tile.tile_type],
                    (self.state.tile_size, self.state.tile_size))
                screen.blit(scaled_image, (
                col_index * self.state.tile_size + centering_offset,
                row_index * self.state.tile_size))

        for player in self.state.players:

            # to determine spawn positions
            if self.state.board_width % 2 == 0:  # even board width
                center = self.state.board_width // 2
            elif self.state.board_width % 2 == 1:  # odd board width
                center = (self.state.board_width + 1) // 2

            # Draw active piece
            if player.active_piece != None:
                for location in player.active_piece.locations:
                    scaled_image = pygame.transform.scale(
                        self.sprites[player.active_piece.tile_type],
                        (self.state.tile_size, self.state.tile_size))
                    screen.blit(scaled_image, (
                    location[0] * self.state.tile_size + centering_offset,
                    (location[1] - BOARD_HEIGHT_BUFFER) * self.state.tile_size))

            # Draw next piece
            if player.player_number != None and player.next_piece != None:
                self.draw_next_piece(screen, player.player_number)

        # display score
        score_title = 'Score:'
        text.draw(screen, score_title, 'SMALL', (
        (Constants.WINDOW_WIDTH) - (4 * self.state.tile_size),
        (Globals.BOARD_HEIGHT - 3) * self.state.tile_size), (0, 128, 0))

        score_val = '%d' % (self.state.score)
        text.draw(screen, score_val, 'SMALL', (
        (Constants.WINDOW_WIDTH) - (4 * self.state.tile_size),
        (Globals.BOARD_HEIGHT - 2) * self.state.tile_size), (0, 128, 0))

        # display level
        level_str = 'Level: %d' % (self.state.current_level)
        text.draw(screen, level_str, 'SMALL', (
        (Constants.WINDOW_WIDTH) - (4 * self.state.tile_size),
        (Globals.BOARD_HEIGHT - 4) * self.state.tile_size), (0, 128, 0))

        pygame.display.update()

    def draw_next_piece(self, screen, player_number):

        screen_center_x = Constants.WINDOW_WIDTH // 2
        player = self.state.players[player_number]

        if player_number % 2 == 0:
            # should be drawn on the left
            x_offset = screen_center_x - (
                        ((self.state.board_width // 2) + (3)) * self.state.tile_size)
        else:
            # draw on the right
            x_offset = screen_center_x + (
                        ((self.state.board_width // 2) + (3)) * self.state.tile_size)

        y_offset = (player_number // 2) * ((7) * self.state.tile_size)

        for tile in player.next_piece.locations:
            scaled_image = pygame.transform.scale(
                self.sprites[player.next_piece.tile_type],
                (self.state.tile_size, self.state.tile_size))
            screen.blit(scaled_image,
                        (x_offset+((tile[0]-player.spawn_column)*self.state.tile_size),
                         (tile[1])*Globals.TILE_SIZE+y_offset))
