from basestats import __baseStats__

class Desk(__baseStats__):
    position=(0,0)
    holding=None
    health=None
    storage=None
    def __init__(self, pos=tuple):
        self.position = pos
        self.interact = self.put
    def put(self, *a):
        pass

class Abajour(__baseStats__):
    position=(0,0)
    holding=None
    health=None
    storage=None
    def __init__(self, pos:tuple, h_system, s_system):
        self.position=pos
        self.health=h_system
        self.storage=s_system()
        self.storage.configure_length(1)
        self.interact = self.put
    def put(self, actor):
        item = actor.holding
        if self.storage.get_free_slots() and item:
            self.storage.add_item(item)
            if item.id == '#flashlight':
                item.force += 0.5
            actor.holding = None
            return True
        elif not item and len(self.storage.holding):
            cache = self.storage.holding[0]
            if cache.id == '#flashlight':
                cache.force -= 0.5
            self.storage.remove_item_by_pos(0)
            actor.holding = cache
            return True
        else:
            return False
    def run(self):
        if len(self.storage.holding):
            self.storage.holding[0].run()
            self.storage.holding[0].position = self.position

class Door(__baseStats__):
    def __init__(self, pos:tuple, map_ref, target:tuple, sentido_de_atravessamento:int=0):
        """sentido_de_atravessamento 0 para portas que serão trespassadas caminhando na horizontal
1 para portas que serão trespassadas caminhando na vertical"""
        self.sentido_de_atravessamento=sentido_de_atravessamento
        self.position=pos
        self.target=target
        self.state=False #False to closed True to open
        self.interact=self.switch
        self.map_ref=map_ref
    def switch(self,actor):
        self.state=not self.state
        actor.cathcd=10
        return True
    def run(self):
        relative_target=self.position#(self.position[0]+self.target[0], self.position[1]+self.target[1])
        a = self.map_ref.get_full_spaces(self)
        b = [relative_target]
        for i in range(-7,8):
            k=list(relative_target)
            k[self.sentido_de_atravessamento]+=i/8
            b.append(tuple(k))
        result=True
        for i in b:
            if i in a:
                result=False
        if not self.state and result:
            self.intangible=False # close door
            self.invisible=False
        if self.state:
            self.intangible=True # open door
            self.invisible=True