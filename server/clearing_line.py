

class ClearingLine:
    def __init__(self, player_number, board_index, counter):
        self.player_number = player_number
        self.board_index = board_index
        self.counter = counter

    def decrement_counter(self):
        self.counter -= 1
