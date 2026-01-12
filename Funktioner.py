import os
import msvcrt
import time
import random
import winsound
from Publics import Public
from Publics import Monster
from Publics import Player

################## Public.inFightHealth uppdateras bara i början av battle functionen #####################

def print_monster():    # Mall för fight
    print("👹 Monster \t HP:", (Monster.health * "❤️ "), "\t Strength:", (Monster.strength * "💪"))
    print("______________________________________________________________________________________")
    print("\n🤺 Player \t HP:", (Player.inFightHealth * "❤️ "), "\t Defense:", (Player.defense * "🛡️ "),"\t Strength:",(Player.strength * "💪"))
    print("______________________________________________________________________________________")
    print("\nPress [SPACE] on 🟩 to attack.")
    print("")

def print_boss():    # Mall för fight (För bossar)
    print("\n꧁ 𓆩༺✧༻𓆪 ꧂꧁ 𓆩༺✧༻𓆪 ꧂     BOSSE PERSSON    ꧁ 𓆩༺✧༻𓆪 ꧂꧁ 𓆩༺✧༻𓆪 ꧂")
    print("\n👹 BOSS \t HP:", (Monster.health * "❤️ "), "\t Strength:", (Monster.strength * "💪"))
    print("______________________________________________________________________________________")
    print("\n🤺 Player \t HP:", (Player.inFightHealth * "❤️ "), "\t Defense:", (Player.defense * "🛡️ "), "\t Strength:",(Player.strength * "💪"))
    print("______________________________________________________________________________________")
    print("\nPress [SPACE] on 🟩 to attack.")
    print("")


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


isInChest = False
def Chest(key, subFacX, subFacY):
    global isInChest
    if Public.isOnChest and isInChest == False:
        isInChest = True
        os.system("cls")
        print("You found a chest! Press [T] to open it.")

    if key == "t" and Public.isOnChest:
        os.system("cls")
        found_item = random.choice(möjliga_item)
        print(f"You found a {found_item.name}!")        #väljer ett item och säger vilket

        if len(Player.inventory) < Player.max_inventory:
            Player.inventory.append(found_item.name)
        else:
            print("But your inventory is full!")                #om ditt inventory är fullt
            print("Do you want to drop an item to make space? (Y/N)")
            while True:
                if msvcrt.kbhit():
                    choice = msvcrt.getwch()
                    if choice.lower() == "y":       #om du säger att du vill byta ut ett item
                        inventory()
                        if len(Player.inventory) < Player.max_inventory:
                            Player.inventory.append(found_item.name)
                            print(f"You picked up the {found_item.name}.")
                        else:
                            print("You still don't have enough space.")
                        break
                    elif choice.lower() == "n":
                        print("You left the item in the chest.")
                        break

        isInChest = False    
        Public.isOnChest = False                
        time.sleep(1)
        os.system("cls")
        Public.exitingMenu = True
        #Player.chunk(subFacX, subFacY)

def item_stats(item):
    if "defense" in item.attributes:
        Player.defense += item.attributes["defense"]   

    if "strength" in item.attributes:
        Player.strength += item.attributes["strength"]

#gör så att stats tas bort när item tas av
def RemoveItemStats(item):
    if "defense" in item.attributes:
        leftover= item.attributes["defense"]
        Player.defense -= min(Player.defense, leftover)
    if "strength" in item.attributes:
        Player.strength -= item.attributes["strength"]

def inventory():

    def refresh():
        os.system("cls")


        print("Inventory:")
        for i, itemName in enumerate(Player.inventory, start=1):
            for itm in möjliga_item:
                if itm.name == itemName:
                    stats = ", ".join(f"{k}+{v}" for k, v in itm.attributes.items())    #k= str/helth    v= värde, +2
                    break
            print(f"{i}. {itemName:<7}  {stats}")


        print("________________________________________")

        print("Equipped:")
        for i, item in enumerate(Player.equipped, start=1):
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

            if key == "i":   #stänger inventory fält
                os.system("cls")
                break

            elif key == "u":        #på med unequip mode
                print("Chose an item to unequip.")
                unequip_mode = True

            elif unequip_mode and key.isdigit():
                index = int(key) - 1
                if 0 <= index < len(Player.equipped):     #unequipar item
                    item = Player.equipped.pop(index)
                    RemoveItemStats(item)

                    if len(Player.inventory) < Player.max_inventory:
                        Player.inventory.append(item.name)
                    else:
                        Player.equipped.append(item)
                else:
                    print("Invalid item number to unequip.")
                unequip_mode = False
                refresh()

            elif key.isdigit() and not unequip_mode:
                index = int(key) - 1
                if 0 <= index < len(Player.inventory):
                    itemName = Player.inventory[index]

                    for itm in möjliga_item:
                        if itm.name == itemName:

                            if len(Player.equipped) >= Player.max_equipped:
                                break
                            
                            item_stats(itm)
                            Player.equipped.append(itm)
                            Player.inventory.remove(itemName)
                            break
                refresh()

            elif key in shift_num:
                index = shift_num[key]
                if 0 <= index < len(Player.inventory):
                    itemName = Player.inventory.pop(index)   #drop item
                refresh()

isInStats = False
def stats(key, subFacX, subFacY):        # visa stats
    global isInStats
    if key == "e":
        if isInStats == False:
            isInStats = True
            os.system("cls")
            print("STATS")
            print("________________________________________")
            print("")
            print("HP:", (Player.health * "❤️ "), "[", str(Player.health), "]")
            print("")
            print("Defense:", (Player.defense * "🛡️ "), "[", str(Player.defense), "]")
            print("")
            print("Strength:", (Player.strength * "💪"), "[", str(Player.strength), "]")
            print("")
            print("Level:", str(Player.lvl))
        elif isInStats == True:
            isInStats = False
            os.system("cls")
            Public.exitingMenu = True

isInHelp = False
def help_list(key, subFacX, subFacY):    # Hjälp lista med spelar kommandon.
    global isInHelp

    if key == "h": 
        if isInHelp == True:
            isInHelp = False
            os.system("cls")
            Public.exitingMenu = True
        elif isInHelp == False:
            isInHelp = True
            os.system("cls")
            print("🎮  List of game controls 🎮")
            print("________________________________________")
            print("\n[W/A/S/D] to move character")
            print("\n[E] to open/close player stats")
            print("\n[I] to open/close inventory")
            print("\n[Enter] to enter door")
            print("\n[Space] to attack monster")

def defeat():
    if Player.health <= 0:
        for i in range(3, -1, -1):
            os.system("cls")
            print("🪦  PLAYER DEFEATED 🪦")
            print("________________________________________")
            print("\nYou have 0 hearts left...")
            print("\nEnding game in:", i)
            winsound.Beep(1000, 300)    # funnyyy hahhahaha
            time.sleep(1)
        exit()

def levelup():      # Låter spelaren välja upgrade vid levelup.
    Player.lvl += 1
    os.system("cls")
    print("⭐ LEVEL UP!⭐")
    print("\nChoose level up:")
    print("\n[H] Health / [S] Strength")
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            if key == "h":
                Player.health += 1
                print("+1 ❤️")
                time.sleep(0.5)
                break
            elif key == "s":
                Player.strength += 1
                print("+1 💪")
                time.sleep(0.5)
                break