import os
import msvcrt
import random
import time


os.system("cls")


seed = random.randint(0, 999)


def Battle():
    print("enemy found")
    #choice = input("what do you want to do")


gridSizeX = 8
gridSizeY = 10


chunkSize = [[0 for _ in range(gridSizeX + 1)] for _ in range(gridSizeY + 1)]
#blockY = [16]
#blockX = [16]
xPos = 1
yPos = 1


isOnEnemy = False
isBesideDoor = False


def chunk(subFactorX, subFactorY):
    wall = "#  "
    block = "   "
    enemy = "e  "
    doorY = "|  "
    doorX = "─  "
    player = "P  "
    rand = random.Random(seed)
    global isOnEnemy
    global isBesideDoor


    for i in range(gridSizeY + 1): # Y axel
        blockRowX = ""


        for j in range(gridSizeX + 1): # X axel


            finalPrint = ""
            randBlock = rand.randint(0, 10)


            # bestämmer om blocktypen är en enemy
            if randBlock <= 9:
                finalPrint = block
            else:
                finalPrint = enemy


            # bestämmer blocktypen som ska printas
            if i == int(gridSizeY / 2) and j == 0 or i == int(gridSizeY / 2) and j == gridSizeX:
                finalPrint = doorY
            elif j == int(gridSizeX / 2) and i == 0 or j == int(gridSizeX / 2) and i == gridSizeY:
                finalPrint = doorX
            elif i == gridSizeY or j == gridSizeX or i == 0 or j == 0:
                finalPrint = wall
           
            chunkSize[i][j] = finalPrint
           
            playerPos = chunkSize[yPos + subFactorY][xPos + subFactorX]
            doorCloseX = chunkSize[yPos + subFactorY][xPos + subFactorX + 1] == doorY or chunkSize[yPos + subFactorY][xPos + subFactorX - 1] == doorY
            doorCloseY = chunkSize[yPos + subFactorY + 1][xPos + subFactorX] == doorX or chunkSize[yPos + subFactorY - 1][xPos + subFactorX] == doorX


            if playerPos == enemy:
                isOnEnemy = True
            elif doorCloseX:
                isBesideDoor = True
            elif doorCloseY:
                isBesideDoor = True


            chunkSize[yPos + subFactorY][xPos + subFactorX] = player
            blockRowX += chunkSize[i][j]


        print(blockRowX)
   
chunk(0, 0)


subFacY = 0
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
   
    if isOnEnemy == True:
        Battle()
        isOnEnemy = False


    time.sleep(1 / 100)
