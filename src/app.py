import os
import time
from wpwgame import WumpusWorldGame
from inputholder import InputHolder

class App:
    def __init__(self, file_name):
        self.input_holder = InputHolder(file_name)
        self.game = WumpusWorldGame(self.input_holder)

        self.num_rows, self.num_cols = self.input_holder.world_size, self.input_holder.world_size

    def on_execute(self):
        while(True):
            self.draw()

    def draw(self):
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                print(' ' + self.input_holder.world_array[i][j] + '   ', end='')
            print()
