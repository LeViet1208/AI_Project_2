from class_agent import Agent
from class_knowledgebase import KnowledgeBase

class WumpusWorldGame:
    def __init__(self, input_holder):
        self.n = input_holder.world_size
        self.array = [['' for _ in range(self.n)] for _ in range(self.n)]
        self.agent = Agent(self.n)
        self.knowledge_base = KnowledgeBase(self.n)
        for i in range(self.n):
            for j in range(self.n):
                self.array[i][j] = input_holder.world_array[self.n - i - 1][j]
                if self.array[i][j] == 'A':
                    self.agent.position = (i, j)
                elif self.array[i][j] == 'W':
                    self.knowledge_base.update((i, j), 'S')
                elif self.array[i][j] == 'P':
                    self.knowledge_base.update((i, j), 'B')
        