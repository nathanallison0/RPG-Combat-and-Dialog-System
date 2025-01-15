class Ability:
    def __init__(self):
        self.name = "Doom"
        self.description = "Insane damage will hit the enemy in two turns!"
        self.active = True
    
    def use(self, combat, instance):
        # Store the turn the ability was used on
        instance.turnUsed = combat.turn
        # Give notification
        combat.notif(f"{combat.player.name} fortells an impending doom!")
        # Make ability ususable
        self.active = False
        
    def turn(self, combat, instance):
        # If two turns have passed since the ability was used...
        if instance.turnUsed + 2 == combat.turn:
            # Give notification
            combat.notif("A terrible force descends from the heavens...")
            # Deal damage
            combat.damageOpponent(range(13, 16), sfx="kaboom")
            # Make ability usable again
            self.active = True
            # Deactivate instance
            instance.active = False