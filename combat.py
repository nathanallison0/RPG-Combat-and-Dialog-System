import os, sys, classes

inputSpacing = 0

tabs = 2

inputLine = classes.inputLine

messageLine = inputLine

sys.path.insert(1, os.getcwd())

abilitiesDir = os.path.join(os.getcwd(), "abilities")

abilitiesDirItems = os.listdir(abilitiesDir)

abilityFNames = list()
for item in abilitiesDirItems:
    if item.endswith(".py") and not item.split(".")[0].isupper():
        abilityFNames.append(item[:-3])

def getAbility(abilityFileName, isClass = True):
    sys.path[1] = abilitiesDir
    os.chdir("abilities")
    
    module = __import__(abilityFileName)

    os.chdir("../")
    sys.path[1] = os.getcwd()
  
    if isClass:
        return getattr(module, "Ability")()
    else:
        return module
        

abilities = [getAbility(abilityFName) for abilityFName in abilityFNames]

class Combat:
    def __init__(self):
        self.end = False
        self.notifs = list()

    def prompt(self, promptText, constraint = None):
        global inputSpacing
        
        promptLines = promptText.split("\n")
        
        while True:
            constrPromptText = str()
            
            for i in range(len(promptLines)):
                promptLine = promptLines[i]
                
                if promptLine != "":
                    constrPromptText += (" " * inputSpacing)
                constrPromptText += promptLine

                if i != len(promptLines) - 1:
                    constrPromptText += "\n"
                
            print(constrPromptText, end="")
            if promptText.endswith("\n"):
                print(" " * inputSpacing, end="")
            inp =  input(inputLine)
            
            if not constraint is None:
                try:
                    constraint(inp)
                except:
                    continue
                break
            else:
                break
        inputSpacing += tabs
        return inp
    
    def selection(self, itemsList, promptText="", itemsInfo=None):
        promptStringConstr = str()

        if promptText != "":
            promptStringConstr += promptText + "\n"

        for i in range(len(itemsList)):
            promptStringConstr += f" {i + 1}. {itemsList[i]}\n"

        def listRangeConstraint(item, theList = itemsList, itemsInfo = itemsInfo):
            isHelp = item.endswith("?")
            item = item.rstrip("?")
            try:
                item = int(item)
            except:
                itemLower = item.lower()
                theListLower = [listItem.lower() for listItem in theList]
                if itemLower in theListLower:
                    valid = True
                    item = theListLower.index(itemLower)
            else:
                if item in range(1, len(theList) + 1):
                    valid = True
                    item -= 1

            if valid:
                if isHelp:
                    if itemsInfo is not None:
                        print(f"Help ({theList[item]}):")
                        print(itemsInfo[item])
                        print()
                    else:
                        print("No information availible!")
                    raise Exception()
            else:
                raise Exception()
                    

        promptInput = self.prompt(promptStringConstr, constraint = listRangeConstraint)

        try:
            promptInput = int(promptInput)
        except:
            return [listItem.lower() for listItem in itemsList].index(promptInput.lower())
        else:
            return promptInput - 1
            
    def notif(self, message):
        self.notifs.append(message)

class Instance:
    def __init__(self):
        self.active = True

def printStats(being):
    print(f"{being.name}:")
    for line in being.stats().split("\n"):
        print(f"| {line}")

def endOnDeath(combat):
    condition = combat.opponent.health <= 0
    if condition:
        combat.notif(f"{combat.opponent.name} was defeated!")
    return condition

def enterCombat(player, opponent, endCondition = endOnDeath):
    combat = Combat()
    combat.turn = 1
    combat.player = player
    combat.opponent = opponent

    combatState = getAbility("COMBATSTATE", isClass=False)

    combatState.start(combat)

    newFuncs = combatState.functions(combat)
    for name, obj in newFuncs.items():
            combat.__setattr__(name, obj)
    
    instanceMemory = dict()

    while True:
        global inputSpacing
        inputSpacing = 0

        endCombat = endCondition(combat)

        if combat.turn > 1:
            [print(inputLine + message) for message in combat.notifs]
            print()

        if endCombat or combat.end:
            break

        combat.notifs = list()
        
        printStats(combat.opponent)
        print()
        printStats(combat.player)
        print()

        activeAbilities = list()
        inactiveAbilities = list()
        for ability in abilities:
            if ability.active:
                activeAbilities.append(ability)
            else:
                inactiveAbilities.append(ability)

        if len(inactiveAbilities) != 0:
            print("\nINACTIVE:")
            for ability in inactiveAbilities:
                print(f" {ability.name}")
            print()

        selectionInput = combat.selection([ability.name for ability in activeAbilities],
                                          promptText="You can:",
                                          itemsInfo = [ability.description for ability in activeAbilities])

        usingAbility = activeAbilities[selectionInput]

        newInstance = Instance()
        
        usingAbility.use(combat, newInstance)

        for abilityName, instances in instanceMemory.items():
            for ability in abilities:
                if ability.name == abilityName:
                    instancesLen = len(instances)
                    for i in range(instancesLen):
                        if len(instances) != instancesLen:
                            i -= 1
                            instancesLen -= 1
                        instance = instances[i]
                        if instance.active:
                            ability.turn(combat, instance)
                        else:
                            instanceMemory[abilityName].pop(i)
                    break

        if newInstance.active:
            instanceMemory[usingAbility.name] = instanceMemory.get(usingAbility.name, list()) + [newInstance]

        if not combat.end and not opponent.health < 0:
            player.health -= 5
            combat.notif(f"{opponent.name} used Speed Kick!")
            combat.notif(f"Pow! 5 damage to {player.name}!")

        combatState.turn(combat)

        for _ in range(3):
            print()

        combat.turn += 1

    return combat.player, combat.opponent
