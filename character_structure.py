from functools import partial

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
    catchcd=0
    animations=False
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
    
    def move_direction( self, direction:str ):
        a = [0, 0]
        a[direction[0]]= direction[1]
        self.move_pos(a)
        return self.position

    def move_pos( self, vetor:tuple ):
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
            items.append(self.holding)
            self.holding = None
            self.catchcd=10
    
    def lance(self):
        self.actions[0]()

    def run(self):
        if self.animations:
            result = choice_for_animation(self.direction_for_rotate)
            print(self.direction_for_rotate)
            #self.left = result[1]
            if type(result) == int:
                self.degrees = result
                self.current_animation.rodando = True
            else: self.current_animation.rodando = False
            self.current_animation.run()
            self.image = self.current_animation.retorna_quadro()
        self.last_position = self.position
        self.catchcd-=1
        if self.holding:
            self.holding.run()
            self.holding.position = self.position