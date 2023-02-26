class Box:
    position=(0,0)
    holding=None
    health=None
    storage=None
    def __init__(self, pos:tuple, h_system, s_system):
        self.position=pos
        self.health=h_system
        self.storage=s_system
    def put(self, item):
        if not self.holding:
            self.holding = item
            return None
        elif not item:
            cache = self.holding
            self.holding = None
            return cache
    def run(self):
        pass