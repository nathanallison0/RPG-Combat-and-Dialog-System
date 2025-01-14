import random

def functions(combat):
    #Add functions here
    def damageOpponent(damage, doNotif=True, sfx=None, doMultiplier=True, doCrit=True):
        critChanceDigits = len(str(combat.critChance).split(".")[-1])

        try:
            iter(damage)
            damage = random.choice(damage)
        except:
            pass

        baseDamage = damage

        crit = round(random.random(), critChanceDigits) <= combat.critChance
        if crit:
            damage *= combat.critMultiplier

        if doMultiplier:
            damage *= combat.damageMultiplier
            if combat.damageMultiplier != 1:
                combat.damageMultiplier = 1

        damage = int(damage)

        combat.opponent.health -= damage

        if doNotif:
            notif = str()
            if sfx is not None:
                if damage > baseDamage * 1.5:
                    notif += sfx.upper()
                else:
                    notif += f"{sfx[0].upper()}{sfx[1:]}"

                if damage < baseDamage * 0.8:
                    notif += "."
                else:
                    notif += "!"
                notif += " "

            notif += f"{damage} damage to {combat.opponent.name}!"

            combat.notif(notif)
            if crit:
                combat.notif("It's super effective!")
                    
    def poisonOpponent():
        combat.opponentTurnPoisoned = (combat.opponentTurnPoisoned[1], combat.turn)
        combat.notif(f"{combat.opponent.name} was poisoned!")

    #Don't touch unless you know what you're doing!
    return locals().copy()

def start(combat):
    combat.opponentTurnPoisoned = (None, None)
    combat.damageMultiplier = 1
    combat.critChance = 0.1
    combat.critMultiplier = 2

def turn(combat):
    for turn in combat.opponentTurnPoisoned:
        if turn is not None:
            if 0 < combat.turn - turn <= 3:
                combat.damageOpponent(2, doNotif=False, doMultiplier=False, doCrit=False)
                combat.notif(f"{combat.opponent.name} took 2 poison damage!")
                break
