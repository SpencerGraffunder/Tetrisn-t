import pygame
import pdb
from lib.Constants import *
from copy import copy
from lib.states.States import *
from threading import Thread
from lib.states.Menu import *
from lib.states.ClientGame import ClientGame
from lib.states.Game_Over import *
import sys
from lib.states.Control import *
from lib.components.Text import *

class Client:
	def __init__(self):
		pygame.init()
		self.program = Control()

		self.state_dict = {
			'menu': Menu(),
			'client game': ClientGame(),
			'game over': Game_Over()
		}

	def start(self):
			"""
		client_thread = Thread(target=self.client_loop)
		client_thread.start()

	def client_loop(self):
		try:"""
			pygame.display.set_caption('Tetrisn\'t')
			self.program.setup_states(self.state_dict, 'menu')
			text.load_fonts()
			self.program.main_game_loop()
			pygame.quit()
			sys.exit()
			"""
		except Exception as e:
			print(e)
	       """