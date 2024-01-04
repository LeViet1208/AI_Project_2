import collections
import random
from agent import Agent
from knowledgebase import KnowledgeBase
from inputholder import InputHolder

ff = open('output_process.txt', 'w')

class WumpusWorldGame:
    def __init__(self, input_holder):
        self.n = input_holder.world_size
        self.t = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        self.score = 0
        self.array = [['' for i in range(self.n)] for j in range(self.n)]
        self.agent = Agent([0, 0])
        self.expanded_list = []
        self.visited = [[False for i in range(self.n)] for j in range(self.n)]
        self.shooted = [[False for i in range(self.n)] for j in range(self.n)]
        self.path = []
        self.knowledge_base = [[KnowledgeBase() for i in range(self.n)] for j in range(self.n)]
        #return 
        for i in range(self.n):
            for j in range(self.n):
                self.array[i][j] = input_holder.world_array[i][j]
                if self.array[i][j] == 'A':
                    self.agent.set_position([i, j])
                
    def get_percepts(self, x, y):
        self.knowledge_base[x][y].update('Safe', True)
        self.knowledge_base[x][y].update('W', False)
        self.knowledge_base[x][y].update('P', False)
        for i in self.t:
            ix = x + i[0]
            iy = y + i[1]
            if 0 <= ix < self.n and 0 <= iy < self.n:
                if self.array[ix][iy] == 'W':
                    self.knowledge_base[x][y].update('S', True)
                if self.array[ix][iy] == 'P':
                    self.knowledge_base[x][y].update('B', True)

    def expand_tile(self, position):
        x, y = position[0], position[1]
        tt = len(self.expanded_list) - 1
        while tt >= 0:
            if self.expanded_list[tt] == position:
                self.expanded_list.pop(tt)
            tt -= 1
        self.get_percepts(x, y)
        self.visited[x][y] = True

        for i in self.t:
            ix = x + i[0]
            iy = y + i[1]
            if 0 <= ix < self.n and 0 <= iy < self.n:
                if not self.visited[ix][iy] and [ix, iy] not in self.expanded_list:
                    self.expanded_list.append([ix, iy])
                    if not self.knowledge_base[x][y].check('S') and not self.knowledge_base[x][y].check('B'):
                        self.knowledge_base[ix][iy].update('Safe', True)
                    else:
                        if self.knowledge_base[x][y].check('S'):
                            self.knowledge_base[ix][iy].update('W', True)
                        if self.knowledge_base[x][y].check('B'):
                            self.knowledge_base[ix][iy].update('P', True)

    def bfs(self, start, end):
        print('--------------Begin BFS--------------')
        if start == end:
            return []
        q = collections.deque()
        q.append(start)
        visited = [[False for i in range(self.n)] for j in range(self.n)]
        traced = [[[-1, -1] for i in range(self.n)] for j in range(self.n)]
        visited[start[0]][start[1]] = True
        while len(q) > 0:
            node = q.popleft()
            print(node)
            for i in self.t:
                ix = node[0] + i[0]
                iy = node[1] + i[1]
                if 0 <= ix < self.n and 0 <= iy < self.n:
                    if not visited[ix][iy] and (self.visited[ix][iy] or [ix, iy] == end):
                        visited[ix][iy] = True
                        traced[ix][iy] = node
                        q.append([ix, iy])
                        if [ix, iy] == end:
                            path = []
                            while [ix, iy] != start:
                                path.append([ix, iy])
                                ix, iy = traced[ix][iy]
                            path.reverse()
                            return path
        return None
    
    ###Mahattan distance between position and escape tile ([0, 0])
    def heuristic(self, position):
        return position[0] + position[1]
    
    def rdc(self):
        return random.randint(0, 100) % 2 == 1

    def choose_action(self):
        ###Choose a safe tile nearest with current tile
        print('Current position: ', self.agent.get_position())
        print('Expanded list: ', self.expanded_list)
        choose = None
        cost = -1
        path = []
        for i in self.expanded_list:
            if self.knowledge_base[i[0]][i[1]].check('Safe'):
                ipath = self.bfs(self.agent.get_position(), i)
                print('------------------End BFS------------------')
                if ipath == None:
                    print('Error: No path found in ', i)
                    continue
                icost = len(ipath) * -10
                if cost == -1 or icost > cost or (icost == cost and self.heuristic(i) < self.heuristic(choose)):
                    choose = i
                    cost = icost
                    path = ipath
        
        if choose != None:
            print('Choose: ', choose, 'type 1', 'path: ', path, 'cost: ', cost)
            return [1, choose], path
        
        ###If not safe tile can expand, try to kill wumpus on Stench tile
        for i in self.expanded_list:
            if self.knowledge_base[i[0]][i[1]].check('W') and not self.shooted[i[0]][i[1]]:
                ipath = self.bfs(self.agent.get_position(), i)
                print('------------------End BFS------------------')
                if ipath == None:
                    print('Error: No path found in ', i)
                    continue
                icost = len(ipath) * -10 - 100
                if cost == -1 or icost > cost or (icost == cost and self.heuristic(i) < self.heuristic(choose)):
                    choose = i
                    cost = icost
                    path = ipath
        
        if choose != None:
            print('Choose: ', choose, 'type 2', 'path: ', path)
            return [2, choose], path
        
        ###If not safe tile just go to tile with lowest cost and heuristic
        for i in self.expanded_list:
            ipath = self.bfs(self.agent.get_position(), i)
            print('------------------End BFS------------------\n\n')
            if ipath == None:
                print('Error: No path found in ', i)
                continue
            icost = len(ipath) * -10
            if cost == -1 or icost > cost or (icost == cost and self.heuristic(i) < self.heuristic(choose)) or (icost == cost and self.heuristic(i) == self.heuristic(choose) and self.rdc()):
                choose = i
                cost = icost
                path = ipath

        if choose != None:
            print('Choose: ', choose, 'type 3', 'path: ', path)
            return [1, choose], path
        else:
            print('Error: No action found')
            return None
        
    def move_agent(self, position, path):
        for i in path:
            self.score -= 10
            self.path.append([1, i])

        self.agent.set_position(position)
        cur = self.array[position[0]][position[1]]
        if cur == 'W' or cur == 'P':
            self.agent.dead()
            self.score -= 10000
            self.path.append([6, position])
        else:
            if cur == 'G':
                self.score += 1000
                self.array[position[0]][position[1]] = '-'
                self.path.append([3, position])

            if position == [0, 0]:
                self.score += 10
                self.path.append([5, position])
                return 
            
            self.expand_tile(position)

    def check_breeze_nearly(self, position):
        for i in self.t:
            ix = position[0] + i[0]
            iy = position[1] + i[1]
            if 0 <= ix < self.n and 0 <= iy < self.n:
                if self.visited[ix][iy] and not self.knowledge_base[ix][iy].check('B'):
                    return True

    def check_stench(self, x, y):
        if not self.knowledge_base[x][y].check('S'):
            return
        
        ###Check if there is a Wumpus adjacent Stench tile
        for i in self.t:
            ix = x + i[0]
            iy = y + i[1]
            if 0 <= ix < self.n and 0 <= iy < self.n:
                if self.array[ix][iy] == 'W':
                    return
        
        ###If no Wumpus adjacent, mark not Stench
        self.knowledge_base[x][y].update('S', False)

    def shoot(self, position, path):
        ###Move to tile Stench tile
        for i in range(0, len(path) - 1):
            self.score -= 10
            self.path.append([1, path[i]])

        self.agent.set_position(position)
        self.shooted[position[0]][position[1]] = True
        self.path.append([2, position])
        self.score -= 100

        if self.array[position[0]][position[1]] == 'W' or self.check_breeze_nearly(position):
            self.knowledge_base[position[0]][position[1]].update('Safe', True)


        if self.array[position[0]][position[1]] == 'W':
            self.array[position[0]][position[1]] = '-'
            self.knowledge_base[position[0]][position[1]].update('Safe', True)
            self.path.append([4, position])
        self.knowledge_base[position[0]][position[1]].update('W', False)    

        for i in self.t:
            ix = position[0] + i[0]
            iy = position[1] + i[1]
            if 0 <= ix < self.n and 0 <= iy < self.n and [ix, iy] in self.expanded_list:
                self.check_stench(ix, iy)

    def solve(self):

        self.expand_tile(self.agent.get_position())

        while len(self.expanded_list) > 0:
            action, path = self.choose_action()
            ff.write(str(action) + '\n')
            if action == None:
                return None
            
            if action[0] == 1:
                self.move_agent(action[1], path)
            elif action[0] == 2:
                self.shoot(action[1], path)
            else:
                print('Error: Invalid action')
                return None
            
            if self.agent.is_dead():
                print('Agent is dead')
                return self.score
            if self.agent.is_escape():
                print('Agent is escape')
                return self.score
            
            

####Test
input_holder = InputHolder('test/map5.txt')              
game = WumpusWorldGame(input_holder)
score = game.solve()  
ff.close()
f = open('output.txt', 'w')
for i in game.path:
    f.write(str(i) + '\n')
f.close()
print(score)
