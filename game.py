import classes, combat

player = classes.Player({
    "name": input("Enter the name of your adventurer: "),
    "health": 100,
    "maxHealth": 100
    })

npc = classes.Entity({
    "name": "Forest Ogre",
    "health": 50,
    "maxHealth": 50
    })


def saveCombat(opponent):
    global player
    (player, opponent) = combat.enterCombat(player, opponent)

print()
result = npc.doDlg(player, "example")

if result == "fight":
    saveCombat(npc)
elif result == "success":
    print("You got into the sacred wood!")
elif result == "fail":
    print("Fail! You didn't get into the wood.")
