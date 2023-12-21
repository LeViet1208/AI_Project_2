class Agent:
    def __init__(self, start_position):
        self.position = start_position
        self.die = False

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position
    
    def dead(self):
        self.die = True
    
    def is_escape(self):
        return self.position == [0, 0]
    
    def is_dead(self):
        return self.die