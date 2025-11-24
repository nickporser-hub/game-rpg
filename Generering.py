import os
import msvcrt
import random
import time

#class Movement:
os.system("cls")

seed = random.randint(0, 999)

def Battle(key):
    global isOnEnemy
    if isOnEnemy:
        print("enemy found")
    isOnEnemy = False

lockedDoor = "left"
def Door(key):
    global lockedDoor, subFacX, subFacY, seed

    if key.lower() == "\r":

        if isBesideLeftDoor:
            if lockedDoor != "left":
                seed = random.randint(0, 999)
                subFacX += gridSizeX -2
                os.system("cls")
                chunk(subFacX, subFacY)
                lockedDoor = "right"
            else: print("door seems locked")
        elif isBesideTopDoor:
            if lockedDoor != "top":
                seed = random.randint(0, 999)
                subFacY += gridSizeY -2
                os.system("cls")
                chunk(subFacX, subFacY)
                lockedDoor = "bottom"
            else: print("door seems locked")
        elif isBesideRightDoor:
            if lockedDoor != "right":
                seed = random.randint(0, 999)
                subFacX -= gridSizeX -2
                os.system("cls")
                chunk(subFacX, subFacY)
                lockedDoor = "left"
            else: print("door seems locked")
        elif isBesideBottomDoor:
            if lockedDoor != "bottom":
                seed = random.randint(0, 999)
                subFacY -= gridSizeY -2
                os.system("cls")
                chunk(subFacX, subFacY)
                lockedDoor = "top"
            else: print("door seems locked")

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

def chunk(subFactorX, subFactorY):
    wall = "#  "
    block = "   "
    enemy = "e  "   
    doorY = "|  "
    doorX = "─  "
    player = "P  "
    chest = "¤  "
    rand = random.Random(seed)
    global isOnEnemy, isBesideTopDoor, isBesideBottomDoor, isBesideLeftDoor, isBesideRightDoor, isOnChest
    randRoom = rand.randint(0, 1)
    

    for i in range(gridSizeY + 1): # Y axel
        blockRowX = ""

        for j in range(gridSizeX + 1): # X axel

            finalPrint = ""
            randBlock = rand.randint(0, 20)
            

            # bestämmer om blocktypen är en enemy
            if randRoom < 1:
                if randBlock <= 19:
                    finalPrint = block
                else:
                    finalPrint = enemy
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
                #enemyPos = chunkSize[yPos + subFactorY][xPos + subFactorX]

            if playerPos == chest:
                isOnChest = True

            #end of tile checks
            
            chunkSize[yPos + subFactorY][xPos + subFactorX] = player
            blockRowX += chunkSize[i][j]

        print(blockRowX)

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
        
        Door(key) # functioner kallas när en tangent pressas
        Battle(key)

    time.sleep(1 / 100)