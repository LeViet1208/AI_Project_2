class KnowledgeBase:
    def __init__(self, world_size):
        self.percept_reason = { 'B': 'P', 'S': 'W' }
        self.world_size = world_size
        self.knowledge_base = [[{'P': False, 'W': False, 'B': False, 'S': False, 'Safe': False} for _ in range(world_size)] for _ in range(world_size)]

    def update(self, position, percept, status):
        x, y = position
        print('Update', position, percept, status)
        new_dict = dict(self.knowledge_base[x][y])
        new_dict[percept] = status
        self.knowledge_base[x][y] = new_dict
        if percept == 'Safe' and status:
            self.update(position, 'P', False)
            self.update(position, 'W', False)

    def get_percept_safe(self, position):
        x, y = position
        return self.knowledge_base[x][y]['Safe']
    
    def get_percept_pit(self, position):
        x, y = position
        return self.knowledge_base[x][y]['P']
    
    def get_percept_wumpus(self, position):
        x, y = position
        return self.knowledge_base[x][y]['W']
    
    def get_percept_breeze(self, position):
        x, y = position
        return self.knowledge_base[x][y]['B']
    
    def get_percept_stench(self, position):
        x, y = position
        return self.knowledge_base[x][y]['S']