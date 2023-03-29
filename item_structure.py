from math import sin, pi

class ItemStats:
    type = 'item'
    id = '#'
    position = (0, 0)
    def arredondar_pos(super, vetor=(0, 0)):
        super.position = (int(super.position[0]+0.5 +vetor[0]), int(super.position[1]+0.5 +vetor[1]))

class Flashlight(ItemStats):
    flutuaction = 0
    id = '#flashlight'
    state = True
    force = -3
    position = (0, 0)
    tasks=[]
    def adjust_light(self):
        self.lightpoints[self]=self.position
    def get_flutuaction(self):
        return sin(self.flutuaction/16*pi)
    def cintilar(self):
        if self.flutuaction<32:
            self.flutuaction +=1
        else:
            self.flutuaction =0
    def run(self):
        for task in self.tasks:
            task()
    def __init__(self, lightpoints, pos=(0, 0)):
        self.position = pos
        self.lightpoints=lightpoints
        self.tasks.append(self.adjust_light)
        self.tasks.append(self.cintilar)