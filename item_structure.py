class Flashlight:
    state = True
    position = (0, 0)
    def adjust_light(self):
        self.lightpoints[self]=self.position
    def __init__(self, lightpoints, pos=(0, 0)):
        self.position = pos
        self.lightpoints=lightpoints
        self.run = self.adjust_light