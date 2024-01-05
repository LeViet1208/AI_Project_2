import os
import time
from visible_world import VisibleWorld
from wpwgame import WumpusWorldGame
from input_holder import InputHolder

class App:
    def __init__(self, file_name):
        self.input_holder = InputHolder(file_name)
        self.visible_world = VisibleWorld(self.input_holder)
        self.world_size = self.input_holder.world_size

        self.game = WumpusWorldGame(self.input_holder)
        self.path = self.game.path
        self.score = self.game.solve()

        ff = open('output.txt', 'w')
        ff.write(str(self.score) + '\n')
        for i in range(len(self.path)):
            ff.write(str(self.path[i]) + '\n')
        ff.close()

        # Hold the console log at the current step
        self.console_log = ''

        self.hasAgentEscaped = False

    def on_execute(self):
        for i in range(len(self.path)):
            self.draw()
            self.analyze_path(i)
            time.sleep(3)

        if self.hasAgentEscaped:
            print('Agent has escaped!')
        else:
            print('Agent has died!')
        print('Score: ' + str(self.score))

    def analyze_path(self, index):
        step = self.path[index]
        row, col = step[1][0], step[1][1]

        # Convert row, col to x, y
        x, y = col + 1, self.world_size - row

        # Move
        if step[0] == 1:
            self.visible_world.on_move(row, col)
            self.console_log = 'Agent has moved to ' + str(x) + ' ' + str(y)

        # Shoot
        elif step[0] == 2:
            self.visible_world.on_shoot_arrow(row, col)
            self.console_log = 'Agent has shot to ' + str(x) + ' ' + str(y)

            # Comment 2 dòng này để xem kết quả của việc bắn và thấy được việc nhảy cóc
            self.visible_world.on_move(row, col)
            self.console_log = self.console_log + '\nAgent has moved to ' + str(x) + ' ' + str(y)

        # Take gold
        elif step[0] == 3:
            self.console_log = 'Agent has taken gold from ' + str(x) + ' ' + str(y)

        # Kill Wumpus
        elif step[0] == 4:
            self.console_log = 'Agent has killed Wumpus in ' + str(x) + ' ' + str(y)

        # Escape
        elif step[0] == 5:
            self.hasAgentEscaped = True

        # Die
        elif step[0] == 6:
            self.hasAgentEscaped = False

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.visible_world.draw()
        print(self.console_log)
