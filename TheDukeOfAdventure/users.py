import gamedb

class Character():

    def __init__(self, user_id, name, level, stat_points,
                 max_hp, current_hp, fight, body, spirit):
        self.user_id = user_id
        self.name = name
        self.level = level
        self.stat_points = stat_points
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.fight = fight
        self.body = body
        self.spirit = spirit

    def __str__(self):
        s = ("user_id = {0}\nname = {1}\nlevel = {2}\n"
             "stat_points = {3}\nmax_hp = {4}\ncurrent_hp = {5}\n"
             "fight = {6}\nbody = {7}\nspirit = {8}\n")
        return s.format(self.user_id, self.name, self.level, self.stat_points,
                 self.max_hp, self.current_hp, self.fight,
                 self.body, self.spirit)

    def getValues(self):
        return (self.user_id, self.name, self.level, self.stat_points,
                self.max_hp, self.current_hp, self.fight,
                self.body, self.spirit)

#end Character

# Dictionary of all characters in the game.
# TODO: Intelligently figure out which characters to have in
#       memory at a given time if space becomes a problem (it shouldn't).
characters = {}

# Loads all characters from database in gamedb to characters.
def loadAllCharacters():
    res = gamedb.getAllCharacters()

    for c in res:
        characters[c[0]] = Character(*c)

    print("Loaded {0} Characters".format(len(characters)))

# Saves all character information to the database in gamedb.
def saveAllCharacters():
    vals = []
    for uid, c in characters.items():
        vals.append(c.getValues())

    gamedb.saveAll(vals)
    print("Saved {0} Characters".format(len(characters)))

# Returns a Character using the user ID.
def getCharacterById(user_id: str):
    return characters.get(user_id, None)

# Returns whether or not a character already exists with the argument name.
def nameExists(name: str):
    for k, v in characters.items():
        if v.name.lower() == name.lower():
            return True

    return False

# Attempts to replace a character's name with a new one.
def setCharacterName(user_id: str, newName: str):
    char = characters.get(user_id, None)

    if char is None:
        return None
    elif nameExists(newName):
        return False
    else:
        char.name = newName
        return True
