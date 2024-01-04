class KnowledgeBase:
    def __init__(self):
        self.knowledge_base = set()

    def update(self, percept, value):
        if value:
            if percept not in self.knowledge_base:
                self.knowledge_base.add(percept)
        else:
            if percept in self.knowledge_base:
                self.knowledge_base.remove(percept)

    def check(self, percept):
        return percept in self.knowledge_base
