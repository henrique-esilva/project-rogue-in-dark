class HealthSystem:
    atual_health = 10
    maximum_health = 10

    living = True

    actions_on_death = []

    def main( self ):
        if self.atual_health <= 0:
            self.atual_health=0
            self.living=False

    def take_damage( self, damage:int or float ):
        self.atual_health -= damage
        self.main()

    def adjustments( self ):
        if self.maximum_health < 1:
            self.maximum_health = 1
        if self.atual_health > self.maximum_health:
            self.atual_health = self.maximum_health

    def increase_maximum_health( self, value:int ):
        self.maximum_health += value
        self.adjustments()