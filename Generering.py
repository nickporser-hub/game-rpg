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

player = Player

monster = Monster

def battle(subFacX, subFacY):   # Funktion för fight
    #global isOnEnemy
    if Public.isOnEnemy:
        
        os.system("cls")
        #global PlayerInFight_health
        player.inFightHealth = player.health

        if player.lvl < 5:
            monster.health = player.health + random.randint(-2, 2)
            monster.strength = random.randint(1, 2)
            Funktioner.print_monster()
        elif 5 < player.lvl < 10:
            monster.health = player.health + random.randint(-3, 3)
            monster.strength = random.randint(2, 3)
            Funktioner.print_monster()
        elif player.lvl == 5:      # BOSS 1
            monster.health = 10
            Funktioner.print_boss()
        elif player.lvl == 10:     # BOSS 2
            monster.health = 20
            Funktioner.print_boss()

        global fight_bar, fight_bar_original, i        # Player attack
        fight_bar_original = ["⬜","⬜","⬜","⬜","⬜","⬜","🟨","🟨","🟩","🟨","🟨","⬜","⬜","⬜","⬜","⬜","⬜"]
        battle_over = False

        while battle_over == False: # loopar fight bar
            for i in range(len(fight_bar_original)):     # updaterar fight bar

                os.system("cls")    # Sätter nästa bit som röd fyrkant
                if player.lvl == 5 or player.lvl == 10:
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
                                    Funktioner.RemoveItemStats(eq)
                                    player.equipped.remove(eq)
                                    time.sleep(1)

                    #det som är kvar går till hp.
                    player.inFightHealth -= dmg

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
                elif player.inFightHealth <= 0:
                    os.system("cls")
                    print("🪦  YOU LOST 🪦   [-1❤️ ]")
                    player.health -= 1
                    time.sleep(1)
                    battle_over = True
                    break

        Public.isOnEnemy = False
        os.system("cls")
        chunk(subFacX, subFacY)



lockedDoor = "left"
roomNumber = 0
def Door(key):
    global lockedDoor, subFacX, subFacY, seed, roomNumber, deadEnemies

    if key == "\r":

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
    rand = random.Random(seed)
    global roomNumber, isBesideTopDoor, isBesideBottomDoor, isBesideLeftDoor, isBesideRightDoor, deadEnemies
    
    for x in range(gridSizeY + 1): # Y axel
        blockRowX = ""

        for y in range(gridSizeX + 1): # X axel

            finalPrint = ""
            randBlock = rand.randint(0, 20)
            
            # bestämmer om blocktypen är en enemy
            if roomNumber % 2 != 0:
                if randBlock <= 19:
                    finalPrint = block
                else:
                    if (x, y) in deadEnemies:
                        finalPrint = block
                    else:
                        finalPrint = enemy
            else:
                if (x, y) in deadEnemies:#använder en vektor2 för att ta position och bedöma om chistan är tagen
                     finalPrint = block
                else:
                    if x == int(gridSizeY / 2) and y == int(gridSizeX / 2):
                        finalPrint = chest
                    else:
                        finalPrint = block
                   
            # bestämmer blocktypen som ska printas
            if x == int(gridSizeY / 2) and y == 0 or x == int(gridSizeY / 2) and y == gridSizeX:
                finalPrint = doorY
            elif y == int(gridSizeX / 2) and x == 0 or y == int(gridSizeX / 2) and x == gridSizeY:
                finalPrint = doorX
            elif x == gridSizeY or y == gridSizeX or x == 0 or y == 0:
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

            if playerPos == chest:
                Public.isOnChest = True
                deadEnemies.add((playerPosY, playerPosX))

            #end of tile checks
            
            chunkSize[yPos + subFactorY][xPos + subFactorX] = player
            blockRowX += chunkSize[x][y]

        print(blockRowX)
    print("\nPress [H] for help")
   
chunk(0, 4)

#startPos
subFacY = 4
subFacX = 0

isInMenu = False   # fortsätt med detta nästa gång

while True:
    key = ""
    if msvcrt.kbhit() and isInMenu == False: # isInMenu fixa sen
        key = msvcrt.getwch().lower()

        if key == "w":
            subFacY -= 1
            if yPos + subFacY < 1:
                subFacY = 0
            else:
                os.system("cls")
                chunk(subFacX, subFacY)
        elif key == "s":
            subFacY += 1
            if yPos + subFacY > gridSizeY -1:
                subFacY = gridSizeY -2
            else:
                os.system("cls")
                chunk(subFacX, subFacY)
        elif key == "d":
            subFacX += 1
            if xPos + subFacX > gridSizeX -1:
                subFacX = gridSizeX -2
            else:
                os.system("cls")
                chunk(subFacX, subFacY)
        elif key == "a":
            subFacX -= 1
            if xPos + subFacX < 1:
                subFacX = 0
            else: 
                os.system("cls")
                chunk(subFacX, subFacY)

        # --- Inventory ---
        elif key == "i":
            Funktioner.inventory()
            os.system("cls")
            chunk(subFacX, subFacY)

        Door(key)
        battle(subFacX, subFacY)
    
    Funktioner.stats(key, subFacX, subFacY)
    Funktioner.Chest(key, subFacX, subFacY)
    Funktioner.defeat()
    Funktioner.help_list(key, subFacX, subFacY)  # HJÄLP

    if Public.exitingMenu == True:
        chunk(subFacX, subFacY)
        Public.exitingMenu = False

    time.sleep(1 / 100) # sleep för prestanda