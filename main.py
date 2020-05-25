import pygame
import pdb
from Constants import *
from copy import copy
from States import *
from Main_Menu import *
from Level_Selection_Menu import *
from Pause_Menu import *
from Game import *
from Game_Over import *
import sys
from Control import *
from Text import *

pygame.init()
program = Control()

state_dict = {
    'main menu'            : Main_Menu(),
    'level selection menu' : Level_Selection_Menu(),
    'pause menu'           : Pause_Menu(),
    'game'                 : Game(),
    'game over'            : Game_Over()
}

# logo = pygame.image.load('iconsmall.bmp')
# pygame.display.set_icon(logo)
pygame.display.set_caption('Tetrisn\'t')
program.setup_states(state_dict, 'main menu')
text.load_fonts()
program.main_game_loop()
pygame.quit()
sys.exit()