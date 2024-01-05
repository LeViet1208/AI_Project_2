from termcolor import cprint
from input_holder import InputHolder

# Instances of this class are used to hold the visible world for the agent
class VisibleWorld:
    def __init__(self, input_holder):
        self.input_holder = input_holder
        self.world_size = self.input_holder.world_size

        self.visited = [[False for i in range(self.world_size)] for j in range(self.world_size)]
        self.curr_x, self.curr_y = 0, 0

        self.world = [['' for i in range(self.world_size)] for j in range(self.world_size)]
        self.init_world()

    def on_move(self, x, y):
        self.visited[x][y] = True
        self.world[self.curr_x][self.curr_y] = self.world[self.curr_x][self.curr_y].replace('A', '')
        self.world[x][y] = 'A' if self.world[x][y] == '' else self.world[x][y] + 'A'
        self.curr_x = x
        self.curr_y = y

    def on_shoot_arrow(self, x, y):
        if (self.world[x][y] != 'W'):
            return

        self.world[x][y] = ''
        
        # Check adjacent cells
        if x > 0:
            self.remove_stench(x - 1, y)
        if x < self.world_size - 1:
            self.remove_stench(x + 1, y)
        if y > 0:
            self.remove_stench(x, y - 1)
        if y < self.world_size - 1:
            self.remove_stench(x, y + 1)

    def draw(self):
        for i in range(self.world_size):
            # Print y ordinates
            y_ordinate = self.world_size - i
            print(str(y_ordinate) + '  ' if y_ordinate < 10 else str(y_ordinate) + ' ', end='')
            for j in range(self.world_size):
                cell = ''
                if self.visited[i][j]:
                    cell = 'O' if self.world[i][j] == '' else self.world[i][j]
                else:
                    cell = 'X'
                filler = 4 - len(cell) # 4 is the max length of a cell
                cell = cell + ' ' * filler + ' '

                for c in cell:
                    if c == 'A':
                        cprint('A', 'magenta', end='')
                    elif c == 'G':
                        cprint('G', 'yellow', end='')
                    elif c == 'B':
                        cprint('B', 'red', end='')
                    elif c == 'S':
                        cprint('S', 'green', end='')
                    else:
                        print(c, end='')
            print()
        # Print x ordinates
        print('  ' if self.world_size < 10 else '   ', end='')
        for i in range(self.world_size):
            x_ordinate = i + 1
            print(str(x_ordinate), end='    ')
        print()

    # Utility functions
    # -----------------
    def init_world(self):
        for i in range(self.world_size):
            for j in range(self.world_size):
                self.world[i][j] = '' if self.input_holder.world_array[i][j] == '-' else self.input_holder.world_array[i][j]
                if self.world[i][j] == 'A':
                    self.curr_x = i
                    self.curr_y = j

        # Mark cells as stench or breeze
        for i in range(self.world_size):
            for j in range(self.world_size):
                # Check adjacent cells
                if self.world[i][j] == 'P':
                    if i > 0:
                        self.add_breeze(i - 1, j)
                    if i < self.world_size - 1:
                        self.add_breeze(i + 1, j)
                    if j > 0:
                        self.add_breeze(i, j - 1)
                    if j < self.world_size - 1:
                        self.add_breeze(i, j + 1)

                elif self.world[i][j] == 'W':
                    if i > 0:
                        self.add_stench(i - 1, j)
                    if i < self.world_size - 1:
                        self.add_stench(i + 1, j)
                    if j > 0:
                        self.add_stench(i, j - 1)
                    if j < self.world_size - 1:
                        self.add_stench(i, j + 1)
    
    def add_breeze(self, x, y):
        if self.world[x][y] != 'W' and self.world[x][y] != 'P':
            cell = ''
            if self.world[x][y] == '':
                cell = 'B'
            elif 'B' not in self.world[x][y]:
                cell = self.world[x][y] + 'B'
            else:
                cell = self.world[x][y]
            self.world[x][y] = cell

    def add_stench(self, x, y):
        if self.world[x][y] != 'W' and self.world[x][y] != 'P':
            cell = ''
            if self.world[x][y] == '':
                cell = 'S'
            elif 'S' not in self.world[x][y]:
                cell = self.world[x][y] + 'S'
            else:
                cell = self.world[x][y]
            self.world[x][y] = cell

    def remove_stench(self, x, y):
        isStench = False
        # Check adjacent cells
        if x > 0:
            isStench |= self.world[x - 1][y] == 'W'
        if x < self.world_size - 1:
            isStench |= self.world[x + 1][y] == 'W'
        if y > 0:
            isStench |= self.world[x][y - 1] == 'W'
        if y < self.world_size - 1:
            isStench |= self.world[x][y + 1] == 'W'
        if not isStench and 'S' in self.world[x][y]:
            self.world[x][y] = self.world[x][y].replace('S', '')
