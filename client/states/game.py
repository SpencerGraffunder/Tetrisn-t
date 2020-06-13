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
import resources.tile_maker
from client.globals import *


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
        self.sprites[TileType.BLANK] = pygame.image.load(
            os.path.join(wd, 'resources', 'backgroundblock.bmp')).convert()

        n_joysticks = pygame.joystick.get_count()
        joysticks = [pygame.joystick.Joystick(i) for i in range(n_joysticks)]
        for joy in joysticks:
            joy.init()

        # Shift keyboard controls to assign controllers to players first
        for i in range(n_joysticks):
            g.keybindings[i+n_joysticks] = g.keybindings[i]
            del g.keybindings[i]

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
            # Exit is pressed (?)
            if pygame_event.type == pygame.QUIT:
                self.quit = True
                event_type = EventType.SPECIAL
                control_type = ControlType.QUIT
                new_event = Event(event_type, control_type)
                player_inputs[0].add_event(new_event)
            # Exit is not pressed
            else:
                # keyboard
                if pygame_event.type == pygame.KEYDOWN or pygame_event.type == pygame.KEYUP:
                    # For each player
                    for player in self.state.players:
                        if player.player_number in g.keybindings.keys():
                            event_type = None
                            control_type = None
                            if pygame_event.type == pygame.KEYUP:
                                event_type = EventType.KEY_UP
                            elif pygame_event.type == pygame.KEYDOWN:
                                event_type = EventType.KEY_DOWN
                            # Get the binding dict for this player
                            dict_control_type = g.keybindings[player.player_number]
                            # If the key pressed is in the dict
                            if pygame_event.key in dict_control_type:
                                control_type = dict_control_type[pygame_event.key]
                            if event_type is not None and control_type is not None:
                                new_event = Event(event_type, control_type)
                                player_inputs[player.player_number].add_event(new_event)
                                self.do_event(new_event)
                # controller dpad
                elif pygame_event.type == pygame.JOYBUTTONDOWN or pygame_event.type == pygame.JOYBUTTONUP:
                    for player in self.state.players:
                        event_type = None
                        control_type = None
                        if player.player_number == pygame_event.joy:
                            if pygame_event.type == pygame.JOYBUTTONUP:
                                event_type = EventType.KEY_UP
                            elif pygame_event.type == pygame.JOYBUTTONDOWN:
                                event_type = EventType.KEY_DOWN
                            if pygame_event.button == 0:
                                control_type = ControlType.CCW
                            elif pygame_event.button == 1:
                                control_type = ControlType.CW
                            if event_type is not None and control_type is not None:
                                new_event = Event(event_type, control_type)
                                player_inputs[player.player_number].add_event(new_event)
                # controller joystick
                elif pygame_event.type == pygame.JOYHATMOTION:
                    for player in self.state.players:
                        event_type = None
                        control_type = None
                        if player.player_number == pygame_event.joy:
                            x, y = pygame_event.value
                            if x == 0 and y == 0:
                                event_type = EventType.KEY_UP
                                for ct in [ControlType.RIGHT, ControlType.LEFT, ControlType.DOWN]:
                                    new_event = Event(event_type, ct)
                                    player_inputs[player.player_number].add_event(new_event)
                                break
                            else:
                                event_type = EventType.KEY_DOWN
                            if x == 1:
                                control_type = ControlType.RIGHT
                            elif x == -1:
                                control_type = ControlType.LEFT
                            elif y == -1:
                                control_type = ControlType.DOWN
                            if event_type is not None and control_type is not None:
                                new_event = Event(event_type, control_type)
                                player_inputs[player.player_number].add_event(new_event)
                else:
                    return

        for player_input in player_inputs:
            connection.add_input(player_input)

        self.state = connection.get_state()
        g.player_count = self.state.player_count

        g.tile_size = g.window_height // self.state.board_height
        if self.state.game_over:
            self.switch('game over menu')

    def draw(self, screen):

        # background
        screen.fill((150, 150, 150))
        centering_offset = (g.window_width - (g.tile_size * self.state.board_width)) // 2

        # board
        for row_index, tile_row in enumerate(self.state.board[2:]):
            for col_index, tile in enumerate(tile_row):
                # empty tiles
                if tile.tile_type == TileType.BLANK:
                    scaled_image = pygame.transform.scale(self.sprites[tile.tile_type], (g.tile_size, g.tile_size))
                # piece tiles
                else:
                    scaled_image = pygame.transform.scale(g.tile_surfaces[tile.tile_type], (g.tile_size, g.tile_size))
                # draw
                screen.blit(scaled_image, (col_index*g.tile_size+centering_offset, row_index*g.tile_size))

        # active pieces and next pieces
        for player in self.state.players:

            # Draw active piece
            if player.active_piece is not None:
                for location in player.active_piece.locations:
                    scaled_image = pygame.transform.scale(g.tile_surfaces[player.active_piece.tile_type], (g.tile_size, g.tile_size))
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

        # for the first half of the players (including the center one for an odd number) draw the next piece on the left column
        if player_number <= (g.player_count - 1) // 2:
            x_offset = screen_center_x - (((self.state.board_width // 2) + 3) * g.tile_size) # draw on the left
            y_offset = player_number * 4 * g.tile_size
        # draw the rest down the right column, backways for symmetry
        else:
            x_offset = screen_center_x + (((self.state.board_width // 2) + 3) * g.tile_size) # draw on the right
            y_offset = ((g.player_count - (g.player_count - 1) // 2) - (player_number - (g.player_count - 1) // 2 + 1)) * 4 * g.tile_size # (num players on right side) minus (right side player index add 1) for reverse order

        for i, tile in enumerate(player.next_piece.locations):
            scaled_image = pygame.transform.scale(g.tile_surfaces[player.next_piece.tile_type], (g.tile_size, g.tile_size))
            screen.blit(scaled_image, (x_offset+((tile[0]-player.spawn_column)*g.tile_size), (tile[1])*g.tile_size+y_offset))
