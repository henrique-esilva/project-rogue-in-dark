from functools import partial

def choice_for_animation(idle, front, back, right, pos_now, pos_ago):
    rel = (pos_now[0] - pos_ago[0], pos_now[1] - pos_ago[1])
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
    return 0

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

    def __init__( self, position:tuple, h_system, stg_system ):
        self.position = position
        self.last_position = position
        self.health = h_system
        self.storage = stg_system

        self.actions = (
            (
            partial(self.move_pos, ( 0,-1)),
            partial(self.move_pos, ( 0, 1)),
            partial(self.move_pos, (-1, 0)),
            partial(self.move_pos, ( 1, 0))
            ),
        )

    def back_to_last_position( self ):
        self.position = self.last_position
    
    def move_pos( self, vetor:tuple ):
        self.position = (
            self.position[0]+vetor[0]/8,
            self.position[1]+vetor[1]/8
        )
        return self.position
    
    def catch( self, items ):
        if self.catchcd>0:
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
            result = choice_for_animation(self.animations.idle, self.animations.front, self.animations.back, self.animations.right, self.position, self.last_position)
            #self.current_animation = result[0]
            #self.left = result[1]
            self.degrees = result
            self.current_animation.run()
            self.image = self.current_animation.retorna_quadro()
        #self.last_position = self.position
        self.catchcd-=1
        if self.holding:
            self.holding.run()
            self.holding.position = self.position