class Public:
    isOnEnemy = False
    isOnChest = False
    exitingMenu = False
    deadEnemies = set()
    inFightHealth = 0

# PLAYER PROPERTIES:
class Player:
    health = 5
    defense = 0      
    strength = 1
    lvl = 1
    # Inventory
    inventory = []
    equipped = []
    max_inventory = 5
    max_equipped = 2
    inFightHealth = 0

# MONSTER PROPERTIES:
class Monster:
    health = 0
    strength = 0 
