import random
import logging
import sys

from hlt import *
from networking import *
from operator import itemgetter

logging.basicConfig(filename='matheussampaio_bot.log', filemode='w', level=logging.DEBUG)

myID, gameMap = getInit()
sendInit("MatheusSampaio")

STILL = 0
NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4

def main():
    while True:
        moves = []
        gameMap = getFrame()

        for y in range(gameMap.height):
            for x in range(gameMap.width):
                current_cell = gameMap.getSite(Location(x, y))

                if current_cell.owner == myID:
                    moves.append(get_movement(x, y, current_cell))

        sendFrame(moves)

def get_cell(x, y, direction):
    return (gameMap.getSite(Location(x, y), direction), direction)

def get_movement(x, y, current_cell):
    north_cell = get_cell(x, y, NORTH)
    east_cell = get_cell(x, y, EAST)
    south_cell = get_cell(x, y, SOUTH)
    west_cell = get_cell(x, y, WEST)

    todos_vizinhos = [ north_cell, east_cell, south_cell, west_cell ]

    vizinhos_inimigos = [ vizinho for vizinho in todos_vizinhos if vizinho[0].owner != myID ]

    if not vizinhos_inimigos:
        return fortalece_alguem(current_cell, todos_vizinhos)

    cell = min(vizinhos_inimigos, key=lambda c: c[0].strength)

    if cell[0].strength <= current_cell.strength:
        logging.info('atacando {}'.format(cell[1]))

        return Move(Location(x, y), cell[1])

    return Move(Location(x, y), STILL)


def fortalece_alguem(current_cell, todos_vizinhos):
    todos_vizinhos = sorted(todos_vizinhos, key=lambda c: c[0].strength)

    for vizinho in todos_vizinhos:
        if vizinho[0].owner == myID and vizinho[0].strength < 255:
            logging.info('fortalecendo {}'.format(vizinho[1]))
            return Move(Location(x, y), vizinho[1])

    logging.info('fortalecendo random')
    return Move(Location(x, y), random.shuffle(DIRECTIONS)[0])

if __name__ == "__main__":
    try:
        logging.info("startando")
        main()
    except Exception as e:
        logging.error(e)
        sys.exit(1)
