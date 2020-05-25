class States(object):

    def __init__(self):
        self.just_started = True
        self.done = False
        self.next = None
        self.quit = False
        
        
    def switch(self, state):
        self.next = state
        self.done = True