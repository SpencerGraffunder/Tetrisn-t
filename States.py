class States(object):

	player_count = 0
	board_width = 14
	current_level = 0

	def __init__(self):
		self.just_started = True
		self.done = False
		self.next = None
		self.quit = False
		self.previous = None