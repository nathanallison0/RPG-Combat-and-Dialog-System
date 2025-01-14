class Ability:
    def __init__(self):
        self.name = "Nothing"
        self.description = "Nothing!"
        self.active = True
    
    def use(self, combat, instance):
        combat.notif(f"{combat.player.name} did nothing!")
        
    def turn(self, combat, instance):
        instance.active = False
