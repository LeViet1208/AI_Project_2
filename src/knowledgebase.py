class KnowledgeBase:
    def __init__(self, world_size):
        tdict = {'P': False, 'W': False, 'B': False, 'S': False, 'Safe': False}
        self.percept_reason = { 'B': 'P', 'S': 'W' }
        self.world_size = world_size
        self.knowledge_base = [[tdict for _ in range(world_size)] for _ in range(world_size)]

    def update(self, position, percept, status):
        x, y = position
        self.knowledge_base[x][y][percept] = status

    def get_percept_safe(self, position):
        x, y = position
        return self.knowledge_base[x][y]['Safe'] or (not self.get_percept_pit(position) and not self.get_percept_wumpus(position))
    
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