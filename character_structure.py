from functools import partial
from math import copysign

def choice_for_animation(rel):
    if rel[0] < 0:
        if rel[1] < 0:
            return 45
        if rel[1] > 0:
            return 135
        return 90
    if rel[0] > 0:
        if rel[1] < 0:
            return 315
        if rel[1] > 0:
            return 225
        return 270
    if rel[1] > 0:
        return 180
    if rel[1] < 0:
        return 0
    return None

# default class for create an character with self-own actions
class character:
    # equipment
    # storage
    # actions, behavior
    # behavior may be changed by equipment
    # Ex.: use an item, will be avaliable only if you have some
    # action of using an item will be defined by this item

        # change to HealthSystem class; this may be affected by your equipment
    health = int()

        # change to Storage class
    storage   = []

        # change to an Behavior class; this will content the on_event actions
        # and may be affected by your Equipment and HealthSystem
    behavior  = ()

    last_position = (0, 0)
    position =  (0, 0)
    holding = None
    catchcd=0 # cooldown for catch items
    animation=False
    left = 0
    degrees = 0
    direction_for_rotate = (0,0)

    def __init__( self, position:tuple, h_system, stg_system ):
        self.position = position
        self.last_position = position
        self.health = h_system
        self.storage = stg_system

        self.actions = (
        partial(self.move_pos, ( 0,-1)),
        partial(self.move_pos, ( 0, 1)),
        partial(self.move_pos, (-1, 0)),
        partial(self.move_pos, ( 1, 0))
        )

    def back_to_last_position( self ):
        self.position = self.last_position
    
    def move_direction( self, direction:tuple ):
        self.last_position=self.position
        a = [0, 0]
        a[direction[0]]= direction[1]
        self.move_pos(a)
        return self.position

    def move_pos( self, vetor:tuple ):
        self.last_position=self.position
        self.position = (
            self.position[0]+vetor[0]/4,
            self.position[1]+vetor[1]/4
        )
        return self.position
    
    def catch( self, items ):
        if self.catchcd > 0:
            return None
        if not self.holding:
            for item in items:
                dist = ((self.position[0]-item.position[0])**2 + (self.position[1]-item.position[1])**2)**0.5
                if dist <= 1:
                    self.holding = item
                    items.remove(item)
                    self.catchcd = 10
                    break
        else:
            self.holding.arredondar_pos()
            items.append(self.holding)
            self.holding = None
            self.catchcd=10
    
    def lance(self):
        self.actions[0]()

    def run(self):
        if self.animation:
            result = choice_for_animation(self.direction_for_rotate)
            if type(result) == int:
                self.degrees = result
                self.animation.rodando = True
            else: self.animation.rodando = False
            self.animation.run()
            self.image = self.animation.retorna_quadro()
        self.last_position = self.position
        if self.catchcd > 0:
            self.catchcd-=1
        if self.holding:
            self.holding.run()
            self.holding.position = self.position

class Standard_Ghost(character):
    # this vetor control the character movimentation
    # first element is 0->horizontal, 1->vertical
    # second element is the steps counter
    # third element is how much tiles will move
    # and last is 1 to down/right and -1 to up/left
    # this is also a counter
    counting_steps = [1, 0, 6, 1/2]

    def lance( self ):
        response=self.move_direction((self.counting_steps[0], self.counting_steps[3]))
        self.counting_steps[1] += self.counting_steps[3]/4
        a = [0, 0]
        a[self.counting_steps[0]] += self.counting_steps[3]
        self.direction_for_rotate=tuple(a)
        if self.counting_steps[1] == self.counting_steps[2]:
            self.counting_steps[3] = copysign(self.counting_steps[3], -1)
        if self.counting_steps[1] == 0:
            self.counting_steps[3] = copysign(self.counting_steps[3], 1)
        return response
    
    def back_to_last_position(self):
        diff=self.last_position[self.counting_steps[0]]-self.position[self.counting_steps[0]]
        super().back_to_last_position()
        self.counting_steps[1] += diff
        if self.counting_steps[1] == self.counting_steps[2]:
            self.counting_steps[3] = copysign(self.counting_steps[3], -1)
        if self.counting_steps[1] == 0:
            self.counting_steps[3] = copysign(self.counting_steps[3], 1)