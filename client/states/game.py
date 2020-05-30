import pygame
from client.states.state import *
import sys
import os
from common.components.tile import *  # Import like this to avoid having to do Tile. before everything
from common.components.piece import *
import client.globals as g
from common.components.text import *
from common.connection import connection
from common.player_input import *
import pdb


class Game(State):
    def __init__(self):
        State.__init__(self)

        self.state = connection.get_state()

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
        if event.control == ControlType.PAUSE:
            pause_input = PlayerInput(None)
            pause_input.pause_game()
            connection.add_input(pause_input)
            self.switch('pause menu')

    def update(self):
        player_inputs = []
        for player in self.state.players:
            player_inputs.append(PlayerInput(player.player_number))

        # For each of the events in pygame
        for pygame_event in pygame.event.get():

            event_type = None
            control_type = None

            # Exit is pressed (?)
            if pygame_event.type == pygame.QUIT:
                self.quit = True
                event_type = EventType.SPECIAL
                control_type = ControlType.QUIT
                new_event = Event(event_type, control_type)
                player_inputs[0].add_event(new_event)

            # Exit is not pressed
            else:

                # Get the event type
                if pygame_event.type == pygame.KEYUP:
                    event_type = EventType.KEY_UP
                elif pygame_event.type == pygame.KEYDOWN:
                    event_type = EventType.KEY_DOWN
                else: return

                # For each player
                for player in self.state.players:

                    # Get the binding dict for this player
                    dict_control_type = g.keybindings[player.player_number]

                    # If the key pressed is in the dict
                    if pygame_event.key in dict_control_type:
                        control_type = dict_control_type[pygame_event.key]

                        # Make the event object and add it to the list
                        new_event = Event(event_type, control_type)
                        player_inputs[player.player_number].add_event(new_event)
                        self.do_event(new_event)

        for player_input in player_inputs:
            connection.add_input(player_input)

        self.state = connection.get_state()
        g.player_count = self.state.player_count
        g.tile_size = (4 * self.state.player_count) + 6

        g.tile_size = min(g.window_width, g.window_height) // max(self.state.board_width, self.state.board_height)
        if self.state.game_over:
            self.switch('game over menu')

    def draw(self, screen):

        screen.fill((150, 150, 150))

        centering_offset = (g.window_width - (
                    g.tile_size * self.state.board_width)) // 2

        for row_index, tile_row in enumerate(self.state.board[2:]):
            for col_index, tile in enumerate(tile_row):
                scaled_image = pygame.transform.scale(
                    self.sprites[tile.tile_type],
                    (g.tile_size, g.tile_size))
                screen.blit(scaled_image, (col_index*g.tile_size+centering_offset, row_index*g.tile_size))

        for player in self.state.players:

            # Draw active piece
            if player.active_piece is not None:
                for location in player.active_piece.locations:
                    scaled_image = pygame.transform.scale(
                        self.sprites[player.active_piece.tile_type],
                        (g.tile_size, g.tile_size))
                    screen.blit(scaled_image, (location[0] * g.tile_size + centering_offset, (location[1] - BOARD_HEIGHT_BUFFER) * g.tile_size))

            # Draw next piece
            if player.player_number is not None and player.next_piece is not None:
                self.draw_next_piece(screen, player.player_number)

        # display score
        score_title = 'Score:'
        text.draw(screen, score_title, 'SMALL', (g.window_width - (4 * g.tile_size), (self.state.board_height - 3) * g.tile_size), (0, 128, 0))

        score_val = str(self.state.score)
        text.draw(screen, score_val, 'SMALL', (g.window_width - (4 * g.tile_size), (self.state.board_height - 2) * g.tile_size), (0, 128, 0))

        # display level
        level_str = str(self.state.current_level)
        text.draw(screen, level_str, 'SMALL', (g.window_width - (4 * g.tile_size), (self.state.board_height - 4) * g.tile_size), (0, 128, 0))

        pygame.display.update()

    def draw_next_piece(self, screen, player_number):

        screen_center_x = g.window_width // 2
        player = self.state.players[player_number]

        if player_number % 2 == 0:
            # should be drawn on the left
            x_offset = screen_center_x - (
                        ((self.state.board_width // 2) + 3) * g.tile_size)
        else:
            # draw on the right
            x_offset = screen_center_x + (
                        ((self.state.board_width // 2) + 3) * g.tile_size)

        y_offset = (player_number // 2) * ((7) * g.tile_size)

        for tile in player.next_piece.locations:
            scaled_image = pygame.transform.scale(self.sprites[player.next_piece.tile_type], (g.tile_size, g.tile_size))
            screen.blit(scaled_image, (x_offset+((tile[0]-player.spawn_column)*g.tile_size), (tile[1])*g.tile_size+y_offset))
