from lib.states.States import *
import pygame
from lib.Constants import *
from lib.components.Text import *
from lib.Connection import PlayerInput
import pdb
import lib.Globals

class Menu(States):

    def __init__(self):
        States.__init__(self)
        self.menu_state = PLAYER_NUMBER_MENU_STATE
        self.next = 'client game'

    def update(self, dt):
        player_input = PlayerInput()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC pressed
                    self.quit = True
                    return

                if self.menu_state == PLAYER_NUMBER_MENU_STATE:  # player number select

                    try:
                        # Set the player count based on the key pressed
                        Globals.PLAYER_COUNT = int(pygame.key.name(event.key))
                    except ValueError:
                        # Value was not an int so just return and wait for a real int
                        return

                    # Bound the player count (can add more later)
                    if Globals.PLAYER_COUNT != 1:
                        Globals.PLAYER_COUNT = 2

                    # Move to the next menu state
                    self.menu_state = LEVEL_SELECT_MENU_STATE

                elif self.menu_state == LEVEL_SELECT_MENU_STATE:  # level select

                    try:
                        # Get the value of the key pressed and cast to int
                        Globals.CURRENT_LEVEL = int(pygame.key.name(event.key))
                    except ValueError:
                        # Value was not an int so just return and wait for a real int
                        return

                    # add 10 if LSHIFT is pressed
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        Globals.CURRENT_LEVEL += 10

                    # start the game
                    Globals.GAME_JUST_STARTED = True
                    player_input.start_game()
                    player_input.set_starting_level(Globals.CURRENT_LEVEL)
                    player_input.set_player_count(Globals.PLAYER_COUNT)
                    # go to the menu where the user chooses the number of players after quitting the game
                    self.menu_state = PLAYER_NUMBER_MENU_STATE

                    self.done = True


    def draw(self, screen):
        screen.fill((150, 150, 150))
        title_string = 'TETRISN\'T'
        subtitle_string = 'not a tetris game'

        if self.menu_state == PLAYER_NUMBER_MENU_STATE: # player number select
            text.draw(screen, title_string, 'LARGE', (WINDOW_WIDTH//2, WINDOW_HEIGHT//4), (0, 160, 0))
            text.draw(screen, subtitle_string, 'SMALL', (WINDOW_WIDTH//2, WINDOW_HEIGHT*2//4), (0, 120, 0))

            single_string = 'Press 1 for single player'
            multi_string = 'Press 0 for multi player'
            text.draw(screen, single_string, 'SMALL', (WINDOW_WIDTH*1//4, WINDOW_HEIGHT*3//4), (150, 0, 0))
            text.draw(screen, multi_string, 'SMALL', (WINDOW_WIDTH*3//4, WINDOW_HEIGHT*3//4), (150, 0, 0))
        elif self.menu_state == LEVEL_SELECT_MENU_STATE: # level select
            text.draw(screen, title_string, 'LARGE', (WINDOW_WIDTH//2, WINDOW_HEIGHT//4), (0, 160, 0))
            text.draw(screen, subtitle_string, 'SMALL', (WINDOW_WIDTH//2, WINDOW_HEIGHT*2//4), (0, 120, 0))

            level_string_line1 = 'Enter the starting level\'s number'
            level_string_line2 = 'Hold LSHIFT to add 10'
            text.draw(screen, level_string_line1, 'SMALL', (WINDOW_WIDTH*1//2, WINDOW_HEIGHT*3//4 - 15), (150, 0, 0))
            text.draw(screen, level_string_line2, 'SMALL', (WINDOW_WIDTH*1//2, WINDOW_HEIGHT*3//4 + 15), (150, 0, 0))

        pygame.display.update()
