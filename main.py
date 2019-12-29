import pygame
import pdb
from tetrisnt_enums import *
from copy import copy
from States import *
from Menu import *
from Game import *
import sys
from Control import *
from DRAW_TEXT import *

pygame.init()
program = Control()

state_dict = {
	'menu': Menu(),
	'game': Game()
}

logo = pygame.image.load('iconsmall.bmp')
pygame.display.set_icon(logo)
pygame.display.set_caption('Tetrisn\'t')
program.setup_states(state_dict, 'game')
text.load_fonts()
program.main_game_loop()
pygame.quit()
sys.exit()