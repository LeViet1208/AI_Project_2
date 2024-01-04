from input_holder import InputHolder

# Instances of this class are used to hold the visible world for the agent
class VisibleWorld:
    def __init__(self, input_holder):
        self.input_holder = input_holder

        self.world_size = self.input_holder.world_size

    def on_move(self, row, col):
        pass

    def on_kill_wumpus(self, row, col):
        pass

    def draw(self):
        for i in range(self.world_size):
            for j in range(self.world_size):
                print(' ' + self.input_holder.world_array[i][j] + '   ', end='')
            print()