class Ability:
    def __init__(self):
        self.name = "Poisoned Dagger"
        self.description = "Slice your opponent and try to poison them!"
        self.active = True
    
    def use(self, combat, instance):
        combat.damageOpponent(range(3, 5), sfx="slash")
        combat.poisonOpponent()
        
    def turn(self, combat, instance):
        instance.active = False


