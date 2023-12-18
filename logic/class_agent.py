class Agent:
    def __init__(self, start_position):
        self.position = start_position
        self.orientation = [0, 0]

    def perceive_environment(self):
        # Implement perception logic based on the world map
        pass

    def update_knowledge_base(self, percepts):
        # Implement knowledge base update logic
        pass

    def decide_next_action(self):
        # Implement decision-making logic
        pass

    def perform_action(self, action):
        # Implement action execution logic
        pass

    def calculate_new_position(self):
        # Implement logic to calculate the new position based on orientation
        pass

    def get_adjacent_rooms(self, x, y):
        # Implement logic to get adjacent rooms
        pass