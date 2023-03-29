class Box:
    position=(0,0)
    holding=None
    health=None
    storage=None
    def __init__(self, pos:tuple, h_system, s_system):
        self.position=pos
        self.health=h_system
        self.storage=s_system
        self.interact = self.put
    def put(self, actor):
        item = actor.holding
        if not self.holding and item:
            self.holding = item
            if item.id == '#flashlight':
                item.force += 1
            actor.holding = None
            return True
        elif not item and self.holding:
            cache = self.holding
            if cache.id == '#flashlight':
                cache.force -= 1
            self.holding = None
            actor.holding = cache
            return True
        else:
            return False
    def run(self):
        if self.holding:
            self.holding.run()
            self.holding.position = self.position