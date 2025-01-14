import os, time

inputLine = "> "

def isClass(var, nameOfClass):
    varType = str(type(var))
    return varType.startswith("<class") and varType.endswith(f".{nameOfClass}'>")

def strList(inputList: list):
    returnString = str()
    for i in range(len(inputList)):
        returnString += (str(inputList[i]) + (", " if len(inputList) - 1 != i else "") if inputList[i] != "" else "")

    return returnString

def strListRec(inputList):
    return strList([
    (
        strListRec(item) if str(type(item)) == "<class 'list'>"
        else item
    )
    for item in inputList
    ])


class Place:
    def __init__(self, name, description, entities, movements, items, actions):
        self.name = name
        self.description = description
        self.entities = entities
        self.movements = movements
        self.items = items
        self.actions = actions

    def describe(self):
        print(f"""You are in ({self.name})
{self.description}
Beings: {strList([entity.name for entity in self.entities])}
Items: {strList([item.name for item in self.items])}
You can: {strListRec([self.actions, self.movements])}""")

    def __str__(self):
        return f"""Class Place ({name}):
Entities: {self.entities}
Movements: {self.movements}
Items: {self.items}
Actions: {self.actions}
Description:
{self.description}"""


class Movement:
    def __init__(self, placeTo, locked, hidden):
        self.placeTo = placeTo
        self.locked = locked
        self.hidden = hidden

    def __str__(self):
        return f"""Class Movement:
Goes to: {self.placeTo}
Locked: {locked}
Hidden: {hidden}"""


class Dialogue:
    def __init__(self, actions, responses):
        self.actions = actions
        self.responses = responses

    def __str__(self):
        return f"""Dialogue class
    Actions: {strList(self.actions)}
    Responses: {strList(self.responses)}"""


class Response:
    def __init__(self, responseQuote, dialogue):
        self.responseQuote = responseQuote
        self.dialogue = dialogue


class Return:
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"Return action message {self.message}"



class Being:
    def __init__(self, stats):
        """Registered attrs:
name: name of being, str
health: health of being, int
maxHealth: max health of being, int"""
        for name, attr in stats.items():
            self.__setattr__(name, attr)

    def stats(self):
        return f"""Health: {self.health}/{self.maxHealth}"""


class Entity(Being):
    def __init__(self, stats):
        super().__init__(stats)

    def __str__(self):
        return(f"""Entity object
    Name: {self.name}
    Health: {self.health}/{self.maxHealth}""")

    def interperetQuote(self, quote, player):
        originalQuote = quote
        concatenators = list()

        iterations = 0
        while quote != "":
            quote = quote.strip()
            if quote[0] == "\"":
                quote = quote[1:]
                concatenators.append(quote[:quote.index("\"")])
                quote = quote[quote.index("\"") + 1:]
            else:
                if " " in quote and "\"" in quote:
                    if quote.index(" ") < quote.index("\""):
                        currentConcatenator = quote[:quote.index(" ")]
                    else:
                        currentConcatenator = quote[:quote.index("\"")]
                elif " " in quote:
                    currentConcatenator = quote[:quote.index(" ")]
                elif "\"" in quote:
                    currentConcatenator = quote[:quote.index("\"")]
                else:
                    currentConcatenator = quote

                commandLevels = currentConcatenator.split(".")

                if commandLevels[0] == "player":
                    concatenators.append(str(player.__dict__[commandLevels[1]]))
                elif commandLevels[0] == "self":
                    concatenators.append(str(self.__dict__[commandLevels[1]]))
                else:
                    raise TypeError(f"Unknown variable {commandLevels[0]} on quote {originalQuote}")

                quote = quote[len(currentConcatenator) + 1:]

                iterations += 1
                if iterations == 30:
                    raise TypeError("30 iterations reached on concatonating quote")

        concatenators = "".join(concatenators)

        return concatenators

    def constructDlg(self, textDlgLines, player, indentation):
        indentationLen = 4
        
        # Gets list of quotes
        actionsList = list()

        def isQuote(line):
            dlgReserved = ("-", "return")
            
            line = line.lstrip()
            for command in dlgReserved:
                if line.startswith(command):
                    return False
            return True

        while len(textDlgLines) > 0:
            if isQuote(textDlgLines[0]):
                actionsList.append(self.interperetQuote(textDlgLines.pop(0), player))
            elif textDlgLines[0].lstrip().startswith("return"):
                actionsList.append(Return(textDlgLines[0].lstrip()[7:]))
                return Dialogue(actionsList, list())
            else:
                break

        if len(textDlgLines) == 0:
            return Dialogue(actionsList, list())

        responseIndexes = list()
        for i in range(len(textDlgLines)):
            line = textDlgLines[i]

            if line.startswith((" " * indentation) + "-"):
                responseIndexes.append(i)

        iterationCount = 0

        dimensionalResponses = list()
        for responseIndexI in range(len(responseIndexes)):
            responseIndex = responseIndexes[responseIndexI]
            response = self.interperetQuote(textDlgLines[responseIndex].lstrip()[1:], player)
            if len(responseIndexes) != responseIndexI + 1:
                dimensionalResponses.append(Response(response, textDlgLines[responseIndex + 1:responseIndexes[responseIndexI + 1]]))
            else:
                dimensionalResponses.append(Response(response, textDlgLines[responseIndex + 1:]))

        return Dialogue(
            actionsList, [
                Response( responseObj.responseQuote, self.constructDlg(responseObj.dialogue, player, indentation + indentationLen) )
                for responseObj in dimensionalResponses
                ]
            )

    def getAndConstructDlg(self, player, dlgName):
        with open(os.path.join("dialogues", f"{dlgName}.dlg")) as f:
            text = f.read()
            textLines = text.split("\n")
            return self.constructDlg(textLines, player, 0)

    def runDialogue(self, player, dlg: Dialogue):
        playerLine = f"{player.name}:"
        
        counts = 0
        for action in dlg.actions:
            counts += 1

            if isinstance(action, Return):
                print()
                return action.message

            if counts == 1:
                print(f"{self.name}:")

            print(f"> {action}")

        if counts > 0:
            print()
        
        if len(dlg.responses) == 0:
            return None
        elif len(dlg.responses) == 1:
            print(playerLine)
            print(f"{inputLine}{dlg.responses[0].responseQuote}")
            print()
            return self.runDialogue(player, dlg.responses[0].dialogue)

        userInputInt = -1
        userInputStr = None

        while (userInputInt - 1 not in range(len(dlg.responses))) and (userInputStr not in [response.responseQuote for response in dlg.responses]):
            print(playerLine)
            for i in range(len(dlg.responses)):
                print(f" {i + 1}. {dlg.responses[i].responseQuote}")

            userInputStr = input(inputLine)

            try:
                userInputInt = int(userInputStr)
            except:
                userInputInt = -1

            print()

        return self.runDialogue(player, dlg.responses[(userInputInt - 1) if userInputInt != -1 else (dlg.responses.index(userInputStr))].dialogue)

    def doDlg(self, player, dlgName):
            dlg = self.getAndConstructDlg(player, dlgName)
            return self.runDialogue(player, dlg)

def printDlgRaw(dialogue: Dialogue, tab, levelsDeep = 0):
    for action in dialogue.actions:
        print(f"{tab * (levelsDeep)}{action}")
    for response in dialogue.responses:
        print(f"{tab * levelsDeep}Response: {response.responseQuote}")
        printDlgRaw(response.dialogue, tab, levelsDeep + 1)



class Player(Being):
    def __init__(self, stats):
        super().__init__(stats)
        
    def __str__(self):
        return f"""Player object
    Name: {self.name}
    Health: {self.health}/{self.maxHealth}"""

