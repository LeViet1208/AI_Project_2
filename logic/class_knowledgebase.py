class KnowledgeBase:
    def __init__(self, world_size):
        self.world_size = world_size
        self.knowledge_base = [[set() for _ in range(world_size)] for _ in range(world_size)]

    def update(self, position, percept):
        x, y = position
        t = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        for i in t:
            if 0 <= x + i[0] < self.world_size and 0 <= y + i[1] < self.world_size:
                self.knowledge_base[x + i[0]][y + i[1]].update(percept)

    def get_percepts(self, position):
        x, y = position
        return self.knowledge_base[x][y]