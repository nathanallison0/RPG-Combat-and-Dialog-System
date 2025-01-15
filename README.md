## RPG Combat and Dialog System

A Python imitation of a Role-Playing Game battle system that allows for the easy creation of abilities for the player to use, \
plus a dialog system that uses formatted text files to simulate interactions with non-player characters.

## Features:
 - Defined combat system that uses customizable python files to define the player's abilities
 - COMBATSTATE.py file to define functions to be used across all ability files and to monitor the combat during each turn
 - Dialog system that reads from text files formatted in a tree that support text variables (ex. the player's name)

## Combat system:
When the player enters combat, ability files are read from the `abilities` directory. \
Each file has an ability name, description, and `use` and `turn` methods. The functionality of the ability comes from those two methods. Both
methods take two arguments: `combat` and `instance`. \
\
**The `use` method:**
Called every time the ability is used. Generally used to deal damage for single-use abilities. \
**The `turn` method:**
Called every turn for each active instance of the ability. \
**The `combat` argument:**
A class that contains the statistics about the combat in progress, like the player and enemy health and the number of turns passed. \
**The `instance` argument:**
Controls the ability's instance memory. This argument has only one attribute, `active`. As long as `active` is true, the combat system
will keep running the ability's `turn` method with its unique `instance` argument. Attributes can be added to the `instance` argument and
will be maintained until the unique instance of the ability becomes inactive. \
**Usage:**
When an ability is used by the user, a unique instance is stored in program memory. This instance is passed to the `instance` argument for
both the `use` and `turn` methods. Then, the combat system will call the ability's `turn` method with that instance as long as the instance
remains active. Multiple instances can be active at once. \
**Example:**
```python
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
        if combat.turn == instance.turnUsed + 2:
            # Give notification
            combat.notif("A terrible force descends from the heavens...")
            # Deal damage
            combat.damageOpponent(range(13, 16), sfx="kaboom")
            # Make ability usable again
            self.active = True
            # Deactivate instance
            instance.active = False
```
This ability, when used, will wait two turns, then deal a random amount of damage between 13 and 16 to the opponent.

## Dialog system:
The player can interact with other entities in a dialog tree system. The other entity says something to the player and the player
is prompted with options of what they can respond with. Each response leads to the entity saying something else, and the process repeats
until the end of the dialog is reached. Recursion is used to implement this. \
\
Each dialog is read from text files with the .dlg extension in the `dialogues` folder. These files are formatted as a tree, with each response
prefixed with a dash and each inner statement by the entity spaced out with an extra five spaces. Dialogues can contain text variables and
return statements, which can be used to change things in the game based on the results of the dialog. \
\
**Text variables:**
Attriblutes of either the player or the entity, `player` and `self` respectfully. Dot notation is used. Ex: `player.name`. \
**Return statements:**
  Returns a string of text back to the main game, ex. `return success`. The text of the return statement is programatically returned by the
  `doDlg()` method as a string. \
**Example:**
```
  "Hello, I'm " self.name "."
  -"Hi, I'm " + player.name ". How are you doing?"
       "I'm doing well, thanks."
       return friend
  -"Get out of my way, I'm busy."
       "That's rude."
       return wasRude
  -"[leave]"
```
## How to use:
- Clone this repository: `git clone https://github.com/nathanallison0/RPG-Combat-and-Dialog-System.git`
- Run the game: `python game.py`
