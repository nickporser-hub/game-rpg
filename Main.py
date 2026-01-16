import os
import msvcrt
import random
import time
import Funktioner
from Publics import Public
from Publics import Player
from Publics import Monster

os.system("cls")

seed = random.randint(0, 999)

def trap():
    if Public.isOnTrap:
        Player.health -= 1
    Public.isOnTrap = False

boss1Killed = False
def battle():   # Funktion för fight
    global boss1Killed
    if Public.isOnEnemy:
        
        os.system("cls")
        #global PlayerInFight_health
        Player.inFightHealth = Player.health

        if Player.lvl < 5:
            Monster.health = 5 + random.randint(-2, 2)
            Monster.strength = random.randint(1, 2)
            Funktioner.print_monster()
        elif 5 < Player.lvl < 10 and boss1Killed: 
            Monster.health = 7 + random.randint(-3, 3)
            Monster.strength = random.randint(2, 3)
            Funktioner.print_monster()
        elif Player.lvl >= 10 and boss1Killed:     # BOSS 2
            Monster.health = 20
            Funktioner.print_boss()
        elif Player.lvl >= 5:      # BOSS 1
            Monster.health = 10
            Funktioner.print_boss()

        global fight_bar, fight_bar_original, i        # Player attack
        fight_bar_original = ["⬜","⬜","⬜","⬜","⬜","⬜","🟨","🟨","🟩","🟨","🟨","⬜","⬜","⬜","⬜","⬜","⬜"]
        battle_over = False

        while battle_over == False: # loopar fight bar
            for i in range(len(fight_bar_original)):     # updaterar fight bar

                # Avrundar alla tal till 2 decimaler
                Monster.health = round(Monster.health, 2)
                Monster.strength = round(Monster.strength, 2)
                Player.inFightHealth = round(Player.inFightHealth, 2)
                Player.strength = round(Player.strength, 2)
                Player.defense = round(Player.defense, 2)

                os.system("cls")    # Sätter nästa bit som röd fyrkant
                if Player.lvl >= 5 and boss1Killed == False or Player.lvl >= 10:
                    Funktioner.print_boss()
                else:
                    Funktioner.print_monster()
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
                                Monster.health -= Player.strength     # Skadar monster
                            elif fight_bar_original[i] == "🟩":
                                print("Critical Hit!")
                                Monster.health -= (Player.strength + 2)     # +2 skada på monster
                            else:
                                print("Miss...")
                            player_turn = False
                            time.sleep(0.5)
                    time.sleep(0.01)
        
                # MONSTRETS TUR:
                if player_turn == False:
                    dmg = Monster.strength

                    #Defense träff
                    if Player.defense > 0:
                        absorbed = min(dmg, Player.defense)
                        dmg -= absorbed
                        Player.defense -= absorbed

                        #gör defense skada som sen förstör itemet
                        for eq in list(Player.equipped):
                            if "defense" in eq.attributes:
                                eq.durability -= absorbed        # defense attack skadar items durability
                                if eq.durability <= 0:
                                    print(f"[{eq.name} broke!]")
                                    Funktioner.RemoveItemStats(eq)
                                    Player.equipped.remove(eq)
                                    time.sleep(1)

                    #det som är kvar går till hp.
                    Player.inFightHealth -= dmg

                # Kollar om spelaren har förlorat/vunnit fighten
                if Monster.health <= 0:
                    os.system("cls")
                    if Player.lvl >= 5:
                        boss1Killed = True

                    if Player.lvl >= 10:
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
                        print("Music Composer: Lyder")
                        print("")
                        time.sleep(1)
                        print("Special thanks to: Holger, clashmästaren(CasperKing), Lyder family, Mr Howard, Goldbarren, Shafootie, Goldklumpen, Rohgold, Luca Baldantoni, and YOU!")
                        print("")
                        time.sleep(5)
                        exit()
                    print("🎖️   YOU WON! 🎖️   [+1 lvl]")
                    Funktioner.level_up()
                    time.sleep(1)
                    battle_over = True
                    break
                elif Player.inFightHealth <= 0:
                    os.system("cls")
                    print("🪦  YOU LOST 🪦   [-1❤️ ]")
                    Player.health -= 1
                    time.sleep(1)
                    battle_over = True
                    break

        Public.isOnEnemy = False
        os.system("cls")
        Public.exitingMenu = True

lockedDoor = "left"
roomNumber = 0
def Door(key):
    global lockedDoor, playerPosX, playerPosY, seed, roomNumber, deadEnemies

    if key == "\r":

        if isBesideLeftDoor:
            if lockedDoor != "left":
                seed = random.randint(0, 999)
                playerPosX += gridSizeX -2
                os.system("cls")
                roomNumber += 1
                deadEnemies = set()
                chunk(playerPosX, playerPosY)
                lockedDoor = "right"
            else: print("door seems locked")
        elif isBesideTopDoor:
            if lockedDoor != "top":
                seed = random.randint(0, 999)
                playerPosY += gridSizeY -2
                os.system("cls")
                roomNumber += 1
                deadEnemies = set()
                chunk(playerPosX, playerPosY)
                lockedDoor = "bottom"
            else: print("door seems locked")
        elif isBesideRightDoor:
            if lockedDoor != "right":
                seed = random.randint(0, 999)
                playerPosX -= gridSizeX -2
                os.system("cls")
                roomNumber += 1
                deadEnemies = set()
                chunk(playerPosX, playerPosY)
                lockedDoor = "left"
            else: print("door seems locked")
        elif isBesideBottomDoor:
            if lockedDoor != "bottom":
                seed = random.randint(0, 999)
                playerPosY -= gridSizeY -2
                os.system("cls")
                roomNumber += 1
                deadEnemies = set()
                chunk(playerPosX, playerPosY)
                lockedDoor = "top"
            else: print("door seems locked")

gridSizeX = 8
gridSizeY = 10

chunkSize = [[0 for _ in range(gridSizeX + 1)] for _ in range(gridSizeY + 1)]
xPos = 1
yPos = 1

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
    trap = "X  "
    rand = random.Random(seed)
    global roomNumber, isBesideTopDoor, isBesideBottomDoor, isBesideLeftDoor, isBesideRightDoor, deadEnemies
    
    for x in range(gridSizeY + 1): # Y axel
        blockRowX = ""

        for y in range(gridSizeX + 1): # X axel
            
            finalPrint = ""
            randBlock = rand.randint(0, 20)
            
            # bestämmer om blocktypen är en enemy
            if roomNumber % 2 != 0:
                if randBlock <= 1:
                    if (x, y) in deadEnemies:
                        finalPrint = block
                    else:
                        finalPrint = trap
                elif randBlock <= 19:
                    finalPrint = block
                else:
                    if (x, y) in deadEnemies:
                        finalPrint = block
                    else:
                        finalPrint = enemy
            else:
                if (x, y) in deadEnemies:#vektor2 för att ta position och bedöma om chistan är tagen
                    finalPrint = block
                else:
                    if x == int(gridSizeY / 2) and y == int(gridSizeX / 2): # mittenBlock coords
                        finalPrint = chest
                    else:
                        finalPrint = block
                   
            # bestämmer blocktypen som ska printas
            # i mitten och längs väggen ger en dörr
            if x == int(gridSizeY / 2) and y == 0 or x == int(gridSizeY / 2) and y == gridSizeX: 
                finalPrint = doorY
            elif y == int(gridSizeX / 2) and x == 0 or y == int(gridSizeX / 2) and x == gridSizeY:
                finalPrint = doorX
            elif x == gridSizeY or y == gridSizeX or x == 0 or y == 0: # genererar en vägg längs kanten
                finalPrint = wall
            
            chunkSize[x][y] = finalPrint
            
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
                Public.isOnEnemy = True
                deadEnemies.add((playerPosY, playerPosX))
            
            if playerPos == trap:
                Public.isOnTrap = True
                deadEnemies.add((playerPosY, playerPosX))

            if playerPos == chest:
                Public.isOnChest = True
                deadEnemies.add((playerPosY, playerPosX))

            #end of tile checks
            
            chunkSize[playerPosY][playerPosX] = player
            blockRowX += chunkSize[x][y]

        print(blockRowX)
    print("\nPress [H] for help")
    if Public.isOnChest:
        print("\nPress [T] to open the chest")
    if Public.isOnTrap:
        print("\nYou stepped on a trap and took one damage")
   


#startPos
playerPosY = 4
playerPosX = 0

chunk(playerPosX, playerPosY)

def Movement(key):
    global playerPosX, playerPosY
    if key == "w":
        playerPosY -= 1
        if yPos + playerPosY < 1:
            playerPosY = 0
        else:
            os.system("cls")
            chunk(playerPosX, playerPosY)
    elif key == "s":
        playerPosY += 1
        if yPos + playerPosY > gridSizeY -1:
            playerPosY = gridSizeY -2
        else:
            os.system("cls")
            chunk(playerPosX, playerPosY)
    elif key == "d":
        playerPosX += 1
        if xPos + playerPosX > gridSizeX -1:
            playerPosX = gridSizeX -2
        else:
            os.system("cls")
            chunk(playerPosX, playerPosY)
    elif key == "a":
            playerPosX -= 1
            if xPos + playerPosX < 1:
                playerPosX = 0
            else: 
                os.system("cls")
                chunk(playerPosX, playerPosY)

while True:
    key = ""
    if msvcrt.kbhit():
        key = msvcrt.getwch().lower()

        if Public.isOnChest == False:
            Movement(key)

        # --- Inventory ---
        if key == "i":
            Funktioner.inventory()
            os.system("cls")
            chunk(playerPosX, playerPosY)

        Door(key)
        battle()
        trap()
    
    Funktioner.stats(key)
    Funktioner.Chest(key)
    Funktioner.defeat()
    Funktioner.help_list(key)  # HJÄLP

    if Public.exitingMenu or key == "\x1b":
        os.system("cls")
        chunk(playerPosX, playerPosY)
        Public.exitingMenu = False

    time.sleep(1 / 100) # sleep för prestanda