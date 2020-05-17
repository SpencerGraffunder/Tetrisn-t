import pygame
import pdb
from Constants import *
from copy import copy
from States import *
from Menu import *
from Game import *
from Game_Over import *
import sys
from Control import *
from Text import *

pygame.init()
program = Control()

state_dict = {
	'menu': Menu(),
	'game': Game(),
	'game over': Game_Over()
}

# logo = pygame.image.load('iconsmall.bmp')
# pygame.display.set_icon(logo)
pygame.display.set_caption('Tetrisn\'t')
program.setup_states(state_dict, 'menu')
text.load_fonts()
program.main_game_loop()
pygame.quit()
sys.exit()