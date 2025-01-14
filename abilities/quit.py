class Ability:
    def __init__(self):
        self.name = "Quit"
        self.description = "Exits the battle!"
        self.active = True
    
    def use(self, combat, instance):
        combat.end = True
        combat.notif(f"{combat.player.name} left the battle!")
        
    def turn(self, combat, instance):
        instance.active = False
