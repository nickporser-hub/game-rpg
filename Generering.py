import os
import msvcrt
import random
import time
import winsound

os.system("cls")

seed = random.randint(0, 999)
# PLAYER PROPERTIES:
class Player:
    def __init__(self, health, strength, lvl):
        self.health = health
        self.defense = 0      
        self.strength = strength
        self.lvl = lvl
        # Inventory
        self.inventory = []
        self.equipped = []
        self.max_inventory = 5
        self.max_equipped = 2


player = Player(5, 1, 1)

# MONSTER PROPERTIES:
class Monster:
    def __init__(self, health, strength):
        self.health = health
        self.strength = strength 
monster = Monster(1, 1)

def print_boss():    # Mall för fight (För bossar)
    print("\n꧁ 𓆩༺✧༻𓆪 ꧂꧁ 𓆩༺✧༻𓆪 ꧂     BOSSE PERSSON    ꧁ 𓆩༺✧༻𓆪 ꧂꧁ 𓆩༺✧༻𓆪 ꧂")
    print("\n👹 BOSS \t HP:", (monster.health * "❤️ "), "\t Strength:", (monster.strength * "💪"))
    print("______________________________________________________________________________________")
    print("\n🤺 Player \t HP:", (PlayerInFight_health * "❤️ "), "\t Defense:", (player.defense * "🛡️ "), "\t Strength:",(player.strength * "💪"))
    print("______________________________________________________________________________________")
    print("\nPress [SPACE] on 🟩 to attack.")
    print("")

def print_monster():    # Mall för fight
    print("👹 Monster \t HP:", (monster.health * "❤️ "), "\t Strength:", (monster.strength * "💪"))
    print("______________________________________________________________________________________")
    print("\n🤺 Player \t HP:", (PlayerInFight_health * "❤️ "), "\t Defense:", (player.defense * "🛡️ "),"\t Strength:",(player.strength * "💪"))
    print("______________________________________________________________________________________")
    print("\nPress [SPACE] on 🟩 to attack.")
    print("")

def battle(subFacX, subFacY):   # Funktion för fight
    global isOnEnemy
    if isOnEnemy:
        
        os.system("cls")
        global PlayerInFight_health
        PlayerInFight_health = player.health

        if player.lvl < 5:
            monster.health = player.health + random.randint(-2, 2)
            monster.strength = random.randint(1, 2)
            print_monster()
        elif 5 < player.lvl < 10:
            monster.health = player.health + random.randint(-3, 3)
            monster.strength = random.randint(2, 3)
            print_monster()
        elif player.lvl == 5:      # BOSS 1
            monster.health = 10
            print_boss()
        elif player.lvl == 10:     # BOSS 2
            monster.health = 20
            print_boss()


        global fight_bar, fight_bar_original, i        # Player attack
        fight_bar_original = ["⬜","⬜","⬜","⬜","⬜","⬜","🟨","🟨","🟩","🟨","🟨","⬜","⬜","⬜","⬜","⬜","⬜"]
        battle_over = False

        while battle_over == False: # loopar fight bar
            for i in range(len(fight_bar_original)):     # updaterar fight bar

                os.system("cls")    # Sätter nästa bit som röd fyrkant
                if player.lvl == 5 or player.lvl == 10:
                    print_boss()
                else:
                    print_monster()
                fight_bar = fight_bar_original.copy()
                fight_bar[i] = "🟥"
                print("".join(fight_bar))

                # SPELARENS TUR:
                player_turn = True
                start = time.time()     # Startar intervall klocka
                while time.time() - start < 0.2:  # 0.2 sek fönster
                    if msvcrt.kbhit() and player_turn == True:
                        key = msvcrt.getwch()
                        if key == " ":
                            if fight_bar_original[i] == "🟨":
                                print("Hit!")
                                monster.health -= player.strength     # Skadar monster
                            elif fight_bar_original[i] == "🟩":
                                print("Critical Hit!")
                                monster.health -= (player.strength + 2)     # +2 skada på monster
                            else:
                                print("Miss...")
                            player_turn = False
                            time.sleep(1)
                    time.sleep(0.01)
        
                # MONSTRETS TUR:
                if player_turn == False:
                    dmg = monster.strength

                    #Defense träff
                    if player.defense > 0:
                        absorbed = min(dmg, player.defense)
                        dmg -= absorbed
                        player.defense -= absorbed

                        #gör defense skada som sen förstör itemet
                        for eq in list(player.equipped):
                            if "defense" in eq.attributes:
                                eq.durability -= absorbed        # defense attack skadar items durability
                                if eq.durability <= 0:
                                    print(f"[{eq.name} broke!]")
                                    RemoveItemStats(eq)
                                    player.equipped.remove(eq)
                                    time.sleep(1)

                    #det som är kvar går till hp.
                    PlayerInFight_health -= dmg

                # Kollar om spelaren har förlorat/vunnit fighten
                if monster.health <= 0:
                    os.system("cls")
                    if player.lvl == 10:
                        print("YOU HAVE KILLED BOSSE! YOU WIN")
                        print("🏆  CONGRATULATIONS!  🏆")
                        print("________________________________")
                        print("Creativ Director: Vidar, Nick, Ted")
                        print("")
                        time.sleep(1)
                        print("Game Designer: Ted, Nick, Vidar")
                        print("")
                        time.sleep(1)
                        print("Lead Developer: Nick, Ted, Vidar")
                        print("")
                        time.sleep(1)
                        print("Lead programer: Ted, Vidar, Nick")
                        print("")
                        time.sleep(1)
                        print("Art Director: Berg, Lyder, Porsér")
                        print("")
                        time.sleep(1)
                        print("Music Composer: Porsér, Lyder, Berg")
                        print("")
                        time.sleep(1)
                        print("Special thanks to: Holger, clashmästaren(CasperKing), Lyder family, Mr Howard, Goldbarren, Shafootie, Goldklumpen, Rohgold, Luca Baldantoni, and YOU!")
                        print("")
                        time.sleep(5)
                        exit()
                    print("🎖️   YOU WON! 🎖️   [+1 lvl]")
                    player.lvl += 1
                    time.sleep(1)
                    battle_over = True
                    break
                elif PlayerInFight_health <= 0:
                    os.system("cls")
                    print("🪦  YOU LOST 🪦   [-1❤️ ]")
                    player.health -= 1
                    time.sleep(1)
                    battle_over = True
                    break

        isOnEnemy = False
        os.system("cls")
        chunk(subFacX, subFacY)

def stats():        # visa stats
    os.system("cls")
    print("STATS")
    print("________________________________________")
    print("")
    print("HP:", (player.health * "❤️ "), "[", str(player.health), "]")
    print("")
    print("Defense:", (player.defense * "🛡️ "), "[", str(player.defense), "]")
    print("")
    print("Strength:", (player.strength * "💪"), "[", str(player.strength), "]")
    print("")
    print("Level:", str(player.lvl))
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            if key.lower() == "e":
                os.system("cls")
                break



def defeat():
    if player.health <= 0:
        for i in range(3, -1, -1):
            os.system("cls")
            print("🪦  PLAYER DEFEATED 🪦")
            print("________________________________________")
            print("\nYou have 0 hearts left...")
            print("\nEnding game in:", i)
            winsound.Beep(1000, 300)    # funnyyy hahhahaha
            time.sleep(1)
        exit()


def help_list(key):    # Hjälp lista med spelar kommandon.
    if key.lower() == "h":
        os.system("cls")
        print("🎮  List of game controls 🎮")
        print("________________________________________")
        print("\n[W/A/S/D] to move character")
        print("\n[E] to open/close player stats")
        print("\n[I] to open/close inventory")
        print("\n[Enter] to enter door")
        print("\n[Space] to attack monster")
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getwch()
                if key.lower() == "h":
                    os.system("cls")
                    break

def levelup():      # Låter spelaren välja upgrade vid levelup.
    player.lvl += 1
    os.system("cls")
    print("⭐ LEVEL UP!⭐")
    print("\nChoose level up:")
    print("\n[H] Health / [S] Strength")
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            if key.lower() == "h":
                player.health += 1
                print("+1 ❤️")
                time.sleep(0.5)
                break
            elif key.lower() == "s":
                player.strength += 1
                print("+1 💪")
                time.sleep(0.5)
                break

lockedDoor = "left"

lockedDoor = "left"
roomNumber = 0
def Door(key):
    global lockedDoor, subFacX, subFacY, seed, roomNumber, deadEnemies

    if key.lower() == "\r":

        if isBesideLeftDoor:
            if lockedDoor != "left":
                seed = random.randint(0, 999)
                subFacX += gridSizeX -2
                os.system("cls")
                roomNumber += 1
                chunk(subFacX, subFacY)
                lockedDoor = "right"
                deadEnemies = set()
            else: print("door seems locked")
        elif isBesideTopDoor:
            if lockedDoor != "top":
                seed = random.randint(0, 999)
                subFacY += gridSizeY -2
                os.system("cls")
                roomNumber += 1
                chunk(subFacX, subFacY)
                lockedDoor = "bottom"
                deadEnemies = set()
            else: print("door seems locked")
        elif isBesideRightDoor:
            if lockedDoor != "right":
                seed = random.randint(0, 999)
                subFacX -= gridSizeX -2
                os.system("cls")
                roomNumber += 1
                chunk(subFacX, subFacY)
                lockedDoor = "left"
                deadEnemies = set()
            else: print("door seems locked")
        elif isBesideBottomDoor:
            if lockedDoor != "bottom":
                seed = random.randint(0, 999)
                subFacY -= gridSizeY -2
                os.system("cls")
                roomNumber += 1
                chunk(subFacX, subFacY)
                lockedDoor = "top"
                deadEnemies = set()
            else: print("door seems locked")

class Item:
    def __init__(self, name, attributes, durability=3):
        self.name = name
        self.attributes = attributes
        self.durability = durability

    def stats(self):
        return self.attributes


möjliga_item= [
    Item("Sword", {"strength": 1}, durability=1),
    Item("Shield", {"defense": 1}, durability=1),
    Item("Helmet", {"defense": 2}, durability=2),
    Item("Brimstone", {"strength": 2}, durability=2),
    Item("Ted bear", {"defense":3}, durability=3)
    ]



def item_stats(item):
    if "defense" in item.attributes:
        player.defense += item.attributes["defense"]   

    if "strength" in item.attributes:
        player.strength += item.attributes["strength"]

#gör så att stats tas bort när item tas av
def RemoveItemStats(item):
    if "defense" in item.attributes:
        leftover= item.attributes["defense"]
        player.defense -= min(player.defense, leftover)
    if "strength" in item.attributes:
        player.strength -= item.attributes["strength"]





def inventory():

    def refresh():
        os.system("cls")


        print("Inventory:")
        for i, itemName in enumerate(player.inventory, start=1):
            for itm in möjliga_item:
                if itm.name == itemName:
                    stats = ", ".join(f"{k}+{v}" for k, v in itm.attributes.items())    #k= str/helth    v= värde, +2
                    break
            print(f"{i}. {itemName:<7}  {stats}")


        print("________________________________________")

        print("Equipped:")
        for i, item in enumerate(player.equipped, start=1):
            stats = ", ".join(f"{k}+{v}" for k, v in item.attributes.items())
            print(f"{i}. {item.name:<7}  {stats}")

        print("")
        print("Press number to equip item          Hold Shift+number to drop item")
        print("Press u+number to unequip item      Press i to close inventory")
    refresh()

    shift_num = {       #shift +nummer
        '!': 0,
        '"': 1,
        "#": 2,
        "¤": 3,
        "%": 4,
    }

    unequip_mode = False


    while True:
        if msvcrt.kbhit():
            key = msvcrt.getwch()

            if key.lower() == "i":   #stänger inventory fält
                os.system("cls")
                break

            elif key.lower() == "u":        #på med unequip mode
                print("Chose an item to unequip.")
                unequip_mode = True

            elif unequip_mode and key.isdigit():
                index = int(key) - 1
                if 0 <= index < len(player.equipped):     #unequipar item
                    item = player.equipped.pop(index)
                    RemoveItemStats(item)

                    if len(player.inventory) < player.max_inventory:
                        player.inventory.append(item.name)
                    else:
                        player.equipped.append(item)
                else:
                    print("Invalid item number to unequip.")
                unequip_mode = False
                refresh()

            elif key.isdigit() and not unequip_mode:
                index = int(key) - 1
                if 0 <= index < len(player.inventory):
                    itemName = player.inventory[index]

                    for itm in möjliga_item:
                        if itm.name == itemName:

                            if len(player.equipped) >= player.max_equipped:
                                break
                            
                            item_stats(itm)
                            player.equipped.append(itm)
                            player.inventory.remove(itemName)
                            break
                refresh()

            elif key in shift_num:
                index = shift_num[key]
                if 0 <= index < len(player.inventory):
                    itemName = player.inventory.pop(index)   #drop item
                refresh()

def Chest(key):
    global isOnChest
    if isOnChest:
        os.system("cls")
        print("You found a chest! Press [T] to open it.")
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getwch()
                if key.lower() == "t":
                    os.system("cls")
                    found_item = random.choice(möjliga_item)
                    print(f"You found a {found_item.name}!")        #väljer ett item och säger vilket

                    if len(player.inventory) < player.max_inventory:
                        player.inventory.append(found_item.name)
                    else:
                        print("But your inventory is full!")                #om ditt inventory är fullt
                        print("Do you want to drop an item to make space? (Y/N)")
                        while True:
                            if msvcrt.kbhit():
                                choice = msvcrt.getwch()
                                if choice.lower() == "y":       #om du säger att du vill byta ut ett item
                                    inventory()
                                    if len(player.inventory) < player.max_inventory:
                                        player.inventory.append(found_item.name)
                                        print(f"You picked up the {found_item.name}.")
                                    else:
                                        print("You still don't have enough space.")
                                    break
                                elif choice.lower() == "n":
                                    print("You left the item in the chest.")
                                    break

                    time.sleep(1)
                    isOnChest = False
                    os.system("cls")
                    chunk(subFacX, subFacY)
                    break

    isOnChest = False


gridSizeX = 8
gridSizeY = 10

chunkSize = [[0 for _ in range(gridSizeX + 1)] for _ in range(gridSizeY + 1)]
xPos = 1
yPos = 1

isOnEnemy = False
isOnChest = False
isBesideTopDoor = False
isBesideBottomDoor = False
isBesideLeftDoor = False
isBesideRightDoor = False
deadEnemies = set()

def chunk(subFactorX, subFactorY):
    wall = "#  "
    block = "   "
    enemy = "e  "   
    doorY = "|  "
    doorX = "─  "
    player = "P  "
    chest = "¤  "
    rand = random.Random(seed)
    global roomNumber, isOnEnemy, isBesideTopDoor, isBesideBottomDoor, isBesideLeftDoor, isBesideRightDoor, isOnChest, deadEnemies
    
    for i in range(gridSizeY + 1): # Y axel
        blockRowX = ""

        for j in range(gridSizeX + 1): # X axel

            finalPrint = ""
            randBlock = rand.randint(0, 20)
            
            # bestämmer om blocktypen är en enemy
            if roomNumber % 2 != 0:
                if randBlock <= 19:
                    finalPrint = block
                else:
                    if (i, j) in deadEnemies:#fixa detta kan inte skriva [i][j] 
                        finalPrint = block
                    else:
                        finalPrint = enemy
            else:
                if (i, j) in deadEnemies:#använder en vektor2 för att ta position och bedöma om chistan är tagen
                     finalPrint = block
                else:
                    if i == int(gridSizeY / 2) and j == int(gridSizeX / 2):
                        finalPrint = chest
                    else:
                        finalPrint = block
                   
            # bestämmer blocktypen som ska printas
            if i == int(gridSizeY / 2) and j == 0 or i == int(gridSizeY / 2) and j == gridSizeX:
                finalPrint = doorY
            elif j == int(gridSizeX / 2) and i == 0 or j == int(gridSizeX / 2) and i == gridSizeY:
                finalPrint = doorX
            elif i == gridSizeY or j == gridSizeX or i == 0 or j == 0:
                finalPrint = wall
            
            chunkSize[i][j] = finalPrint
            
            #tile checks
            playerPos = chunkSize[yPos + subFactorY][xPos + subFactorX]

            playerPosX = xPos + subFactorX
            playerPosY = yPos + subFactorY
            
            tileAbove = chunkSize[playerPosY - 1][playerPosX]
            tileBelow = chunkSize[playerPosY + 1][playerPosX]
            tileLeft = chunkSize[playerPosY][playerPosX - 1]
            tileRight = chunkSize[playerPosY][playerPosX + 1]

            isBesideTopDoor = tileAbove == doorX
            isBesideBottomDoor = tileBelow == doorX      
            isBesideLeftDoor = tileLeft == doorY
            isBesideRightDoor = tileRight == doorY
                
            if playerPos == enemy:
                isOnEnemy = True
                deadEnemies.add((playerPosY, playerPosX))

            if playerPos == chest:
                isOnChest = True
                deadEnemies.add((playerPosY, playerPosX))

            #end of tile checks
            
            chunkSize[yPos + subFactorY][xPos + subFactorX] = player
            blockRowX += chunkSize[i][j]

        print(blockRowX)
    print("\nPress [H] for help")
   
chunk(0, 4)

subFacY = 4
subFacX = 0

while True:
    if msvcrt.kbhit():
        key = msvcrt.getwch()

        if key.lower() == "w":
            subFacY -= 1
            if yPos + subFacY < 1:
                subFacY = 0
            else:
                os.system("cls")
                chunk(subFacX, subFacY)
        elif key.lower() == "s":
            subFacY += 1
            if yPos + subFacY > gridSizeY -1:
                subFacY = gridSizeY -2
            else:
                os.system("cls")
                chunk(subFacX, subFacY)
        elif key.lower() == "d":
            subFacX += 1
            if xPos + subFacX > gridSizeX -1:
                subFacX = gridSizeX -2
            else:
                os.system("cls")
                chunk(subFacX, subFacY)
        elif key.lower() == "a":
            subFacX -= 1
            if xPos + subFacX < 1:
                subFacX = 0
            else: 
                os.system("cls")
                chunk(subFacX, subFacY)

        # --- Stats ---
        elif key.lower() == "e":
            stats()
            os.system("cls")
            chunk(subFacX, subFacY)

        # --- Inventory ---
        elif key.lower() == "i":
            inventory()
            os.system("cls")
            chunk(subFacX, subFacY)

        help_list(key)  # HJÄLP
        Door(key)
        battle(subFacX, subFacY)
        Chest(key)
    defeat()

    time.sleep(1 / 100)