import collections
from agent import Agent
from knowledgebase import KnowledgeBase
from inputholder import InputHolder

class WumpusWorldGame:
    def __init__(self, input_holder):
        self.n = input_holder.world_size
        self.score = 0
        self.array = [['' for i in range(self.n)] for j in range(self.n)]
        self.agent = Agent([0, 0])
        self.percepts = [[set() for i in range(self.n)] for j in range(self.n)]
        self.visited = [[False for i in range(self.n)] for j in range(self.n)]
        self.shooted = [[False for i in range(self.n)] for j in range(self.n)]
        self.safed = []
        self.path = []
        self.knowledge_base = KnowledgeBase(self.n)
        #return 
        for i in range(self.n):
            for j in range(self.n):
                self.array[i][j] = input_holder.world_array[self.n - i - 1][j]
                if self.array[i][j] == 'A':
                    self.agent.set_position([i, j])
                t = [[0, 1], [1, 0], [0, -1], [-1, 0]]
                if self.array[i][j] == 'W' or self.array[i][j] == 'P':
                    p = 'S' if self.array[i][j] == 'W' else 'B'
                    for k in t:
                        if 0 <= i + k[0] < self.n and 0 <= j + k[1] < self.n:
                            self.percepts[i + k[0]][j + k[1]].add(p)

    def find_action(self, action_deque):
        x, y = self.agent.get_position()
        percepts = self.percepts[x][y]
        t = [[0, -1], [-1, 0], [0, 1], [1, 0]]

        if not percepts:
            ### If there is no percept, then the adjacent rooms are safe    
            for i in t:
                if 0 <= x + i[0] < self.n and 0 <= y + i[1] < self.n:
                    if not self.visited[x + i[0]][y + i[1]]:
                        action_deque.append([1, [x + i[0], y + i[1]]])
                        self.knowledge_base.update([x + i[0], y + i[1]], 'Safe', True)
                        self.safed.append([x + i[0], y + i[1]])
        else:
            ### Find all rooms that has percept Stench and try to kill the Wumpus nearby
            for i in t:
                ix = x + i[0]
                iy = y + i[1]
                if 0 <= ix < self.n and 0 <= iy < self.n and not self.visited[ix][iy] and not self.knowledge_base.get_percept_safe([ix, iy]) and not self.shooted[ix][iy]:
                    action_deque.append([2, [ix, iy]])

            for i in self.safed:
                if i != [x, y] and self.knowledge_base.get_percept_stench(i):
                    for j in t:
                        ix = i[0] + j[0]
                        iy = i[1] + j[1]
                        if 0 <= ix < self.n and 0 <= iy < self.n and not self.knowledge_base.get_percept_safe([ix, iy]) and not self.shooted[ix][iy]:
                            action_deque.append([2, [ix, iy]])
        
        ### If there no action can be found, then the unknown risk is Pit => Just try to go straight (No solution)
        if not action_deque:
            for i in t:
                ix = x + i[0]
                iy = y + i[1]
                if 0 <= ix < self.n and 0 <= iy < self.n and not self.visited[ix][iy]:
                    action_deque.append([1, [ix, iy]])

    def get_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def go_in_safe(self, pos):
        ###BFS from current position to the position need to go
        x, y = self.agent.get_position()
        t = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        deque = collections.deque([])
        deque.append([x, y])
        visited = [[False for _ in range(self.n)] for _ in range(self.n)]
        trace = [[[] for _ in range(self.n)] for _ in range(self.n)]

        while deque:
            u = deque.popleft()
            for i in t:
                ix = u[0] + i[0]
                iy = u[1] + i[1]
                if 0 <= ix < self.n and 0 <= iy < self.n and self.visited[ix][iy] and not visited[ix][iy]:
                    if [ix, iy] == pos:
                        path = []
                        while [ix, iy] != [x, y]:
                            path.append([ix, iy])
                            ix, iy = trace[ix][iy]
                        path.append([x, y])
                        path = path[::-1]
                        return path
                    visited[ix][iy] = True
                    deque.append([ix, iy])
                    trace[ix][iy] = u
        return []
    
    def agent_move(self, pos, action_deque):
        ###If the destination is not adjacent to the current position, then go in safe
        if self.get_distance(self.agent.get_position(), pos) > 1:
            path = self.go_in_safe(pos)
            if not path:
                return False
            
            for i in path:
                self.path.append([1, i])
                self.score -= 10
        else:
            self.score -= 10

        self.agent.set_position(pos)
        self.visited[pos[0]][pos[1]] = True

        a = self.array[pos[0]][pos[1]]
        p = self.percepts[pos[0]][pos[1]]
        if a == 'W' or a == 'P':
            self.agent.die()
            self.score -= 10000
            return False
        elif a == 'G':
            self.score += 1000
        elif pos == [0, 0]:
            self.score += 10
            return True
        
        if p:
            for i in p:
                self.knowledge_base.update(pos, i, True)
                per = self.knowledge_base.percept_reason[i]
                t = [[0, -1], [-1, 0], [0, 1], [1, 0]]
                for j in t:
                    ix = pos[0] + j[0]
                    iy = pos[1] + j[1]
                    if 0 <= ix < self.n and 0 <= iy < self.n and not self.visited[ix][iy] and not self.knowledge_base.get_percept_safe([ix, iy]):
                        self.knowledge_base.update([ix, iy], per, True)
        else:
            t = [[0, -1], [-1, 0], [0, 1], [1, 0]]
            for i in t:
                ix = pos[0] + i[0]
                iy = pos[1] + i[1]
                if 0 <= ix < self.n and 0 <= iy < self.n and not self.visited[ix][iy]:
                    action_deque.insert(0, [1, [ix, iy]])
                    self.knowledge_base.update([ix, iy], 'Safe', True)
                    self.safed.append([ix, iy])

        return True

    def agent_shoot(self, pos, action_deque):
        t = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        ### If shoot the tile not adjacent to the current position, choose a tile adjacent to the destination and has breeze (if can)
        if self.get_distance(self.agent.get_position(), pos) != 1:
            d = []
            for i in t:
                ix = pos[0] + i[0]
                iy = pos[1] + i[1]
                if 0 <= ix < self.n and 0 <= iy < self.n and self.knowledge_base.get_percept_safe([ix, iy]):
                    if not d:
                        d = [ix, iy]
                    else:
                        if self.knowledge_base.get_percept_breeze(d) and not self.knowledge_base.get_percept_breeze([ix, iy]):
                            d = [ix, iy]
            if not d:
                return False

            path = self.go_in_safe(d)
            for i in path:
                self.path.append([1, i])
                self.score -= 10
            self.agent.set_position(d)
        
        self.shooted[pos[0]][pos[1]] = True
        self.score -= 100
        self.path.append([2, pos])

        if self.array[pos[0]][pos[1]] == 'W':
            self.path.append([4, pos])
            self.array[pos[0]][pos[1]] = '-'
            for i in t:
                ix = pos[0] + i[0]
                iy = pos[1] + i[1]
                if 0 <= ix < self.n and 0 <= iy < self.n:
                    self.knowledge_base.update([ix, iy], 'S', False)
                    self.percepts[ix][iy].remove('S')
            self.knowledge_base.update(pos, 'W', False)
            self.knowledge_base.update(pos, 'Safe', True)
            self.safed.append(pos)
            action_deque.append([1, pos])
        elif not self.knowledge_base.get_percept_breeze(self.agent.get_position()):
            self.knowledge_base.update(pos, 'W', False)
            self.knowledge_base.update(pos, 'Safe', True)
            self.safed.append(pos)
            action_deque.append([1, pos])

    def perform_action(self, action, action_deque):
        self.path.append(action)
        act, pos = action
        if act == 1:
            return self.agent_move(pos, action_deque)
        elif act == 2:
            return self.agent_shoot(pos, action_deque)
            
        return False

    def solve(self):
        action_deque = collections.deque([])

        self.visited[self.agent.get_position()[0]][self.agent.get_position()[1]] = True
        while True:
            if self.agent.is_dead() or self.agent.is_escape():
                return self.score
            
            if action_deque:
                act = action_deque.popleft()
                self.perform_action(act, action_deque)
            else:
                self.find_action(action_deque)


####Test
input_holder = InputHolder('input.txt')
game = WumpusWorldGame(input_holder)
f = open('output.txt', 'w')
f.write(str(game.solve()))
for i in game.path:
    f.write('\n' + str(i[0]) + ' ' + str(i[1][0]) + ' ' + str(i[1][1]))
f.close()