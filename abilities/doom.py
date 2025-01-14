class Ability:
    def __init__(self):
        self.name = "Doom"
        self.description = "Insane damage will hit the enemy in two turns!"
        self.active = True
    
    def use(self, combat, instance):
        instance.turnUsed = combat.turn
        combat.notif(f"{combat.player.name} fortells an impending doom!")
        self.active = False
        
    def turn(self, combat, instance):
        if instance.turnUsed + 2 == combat.turn:
            combat.notif("A terrible force descends from the heavens...")
            combat.damageOpponent(range(13, 16), sfx="kaboom")
            self.active = True
            instance.active = False
            
