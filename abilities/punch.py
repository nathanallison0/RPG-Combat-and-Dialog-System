class Ability:
    def __init__(self):
        self.name = "Punch"
        self.description = "Use your fist to smack the opponent in the face\nand deliver pain!"
        self.active = True
    
    def use(self, combat, instance):
        combat.damageOpponent(range(4, 6), sfx="smack")
        
    def turn(self, combat, instance):
        instance.active = False

