import os
import time
from visible_world import VisibleWorld
from wpwgame import WumpusWorldGame
from input_holder import InputHolder

class App:
    def __init__(self, file_name):
        self.input_holder = InputHolder(file_name)
        self.visible_world = VisibleWorld(self.input_holder)

        self.game = WumpusWorldGame(self.input_holder)

    def on_execute(self):
        while(True):
            time.sleep(1)
            self.output()

    def analyze_path(self):
        pass

    def output(self):
        os.system('clear')
        self.visible_world.draw()
