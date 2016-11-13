from hlt import *
from networking import *

myID, gameMap = getInit()
sendInit("Reul0")

while True:
    moves = []
    gameMap = getFrame()
    shuffled_cardinals = (NORTH, EAST)
    if (bool(int((random.random() * 2)))):
        shuffled_cardinals = shuffled_cardinals[::-1]
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            if gameMap.getSite(Location(x, y)).owner == myID:
                movedPiece = False
                for d in CARDINALS:
                    if gameMap.getSite(Location(x, y), d).owner != myID:
                        if gameMap.getSite(Location(x, y), d).strength < gameMap.getSite(Location(x, y)).strength:
                            moves.append(Move(Location(x, y), d))
                        else:
                            moves.append(Move(Location(x, y), STILL))

                        movedPiece = True
                        break

                if not movedPiece and gameMap.getSite(Location(x, y)).strength < gameMap.getSite(Location(x, y)).production * 5:
                    moves.append(Move(Location(x, y), STILL))
                    movedPiece = True

                if not movedPiece:
                    for d in CARDINALS:
                        if  gameMap.getSite(Location(x,y), d).owner != myID and gameMap.getSite(Location(x,y), d).strength < 255:
                            moves.append(Move(Location(x, y), d))
                            movedPiece = True
                            break

                if not movedPiece:
                    for d in shuffled_cardinals:
                        if  gameMap.getSite(Location(x,y), d).owner == myID and gameMap.getSite(Location(x,y), d).strength < 255:
                            moves.append(Move(Location(x, y), d))
                            movedPiece = True
                            break


                if not movedPiece:
                    moves.append(Move(Location(x, y), random.choice((NORTH, SOUTH, WEST, EAST)))) 
                    movedPiece = True
    sendFrame(moves)

