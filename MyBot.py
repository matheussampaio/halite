import logging
from operator import itemgetter

# from site import Site
from gamemap import *
from networking import getInit, sendInit, getFrame, sendFrame

logging.basicConfig(filename='MyBot.log', filemode='w', level=logging.DEBUG)

class Main():

    def __init__(self):
        self.my_id, self.game_map = getInit()

        sendInit("MatheusSampaio")

        self.run()


    def run(self):
        while True:
            moves = []
            self.enemies_locations = []

            self.game_map = getFrame()

            for y in range(self.game_map.height):
                for x in range(self.game_map.width):
                    if self.game_map.contents[y][x].owner != self.my_id:
                        self.enemies_locations.append(Location(x, y))

            for y in range(self.game_map.height):
                for x in range(self.game_map.width):
                    current_cell = self.game_map.getSite(Location(x, y))

                    if current_cell.owner == self.my_id:
                        moves.append(self.get_movement(x, y, current_cell))

            sendFrame(moves)


    def get_cell(self, x, y, direction):
        return (self.game_map.getSite(Location(x, y), direction), direction)


    def get_movement(self, x, y, current_cell):
        north_cell = self.get_cell(x, y, NORTH)
        east_cell = self.get_cell(x, y, EAST)
        south_cell = self.get_cell(x, y, SOUTH)
        west_cell = self.get_cell(x, y, WEST)

        todos_vizinhos = [north_cell, east_cell, south_cell, west_cell]

        vizinhos_inimigos = [vizinho for vizinho in todos_vizinhos if vizinho[0].owner != self.my_id]

        # WEAK, STILL!
        if current_cell.strength < current_cell.production * 5:
            logging.info("WAIT %d,%d (%d) : %d", x, y, current_cell.production, STILL)
            return Move(Location(x, y), STILL)

        # ATTACK!
        if vizinhos_inimigos:
            enemy_with_max_production = min(vizinhos_inimigos, key=lambda v: v[0].strength)

            if enemy_with_max_production[0].strength < current_cell.strength:
                logging.info("Attack %d,%d (%d): %d", x, y, current_cell.production, enemy_with_max_production[1])
                return Move(Location(x, y), enemy_with_max_production[1])
            else:
                logging.info("Can't Attack %d,%d (%d): %d", x, y, current_cell.production, STILL)
                return Move(Location(x, y), STILL)


        # MOVE
        closest_enemy = min(self.enemies_locations, key=lambda enemy: self.game_map.getDistance(Location(x, y), enemy))

        direction = self.game_map.getDirectionTo(closest_enemy, Location(x, y))
        logging.info("MOVE %d,%d -> %d, %d: %d", x, y, closest_enemy.x, closest_enemy.y, direction)
        return Move(Location(x, y), direction)


if __name__ == "__main__":
    try:
        logging.info("startando")
        Main()
    except:
        logging.exception("Oops:")

