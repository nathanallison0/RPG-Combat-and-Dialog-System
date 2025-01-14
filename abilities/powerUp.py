class Ability:
    def __init__(self):
        self.name = "Power Up"
        self.power = 2.5
        self.description = f"Applies {self.power}x damage multiplier!"
        self.active = True
    
    def use(self, combat, instance):
        combat.damageMultiplier *= self.power
        instance.turnUsed = combat.turn
        combat.notif(f"{combat.player.name} powered up to {combat.damageMultiplier}x power!")
        self.active = False
        
    def turn(self, combat, instance):
        if instance.turnUsed + 2 == combat.turn:
            self.active = True
            instance.active = False
