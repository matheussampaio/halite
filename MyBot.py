import time
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
            self.player_sites = []

            self.game_map = getFrame()
            start_time = time.time()

            for y in range(self.game_map.height):
                for x in range(self.game_map.width):
                    if self.game_map.contents[y][x].owner != self.my_id:
                        self.enemies_locations.append(Location(x, y))
                    else:
                        self.player_sites.append(self.game_map.contents[y][x])

            self.player_sites = sorted(self.player_sites, key=lambda s: s.strength, reverse=True)

            while len(self.player_sites):
                current_site = self.player_sites.pop()
                movement = self.get_movement(current_site)
                moves.append(movement)

                if movement != STILL:
                    self.player_sites = sorted(self.player_sites, key=lambda s: s.strength, reverse=True)

                if time.time() - start_time > 0.9:
                    logging.info("AVOIDING TIMEOUT!! %d", len(self.player_sites))

                    for site in self.player_sites:
                        moves.append(Move(Location(site.x, site.y), STILL))

                    break

            sendFrame(moves)


    def get_cell(self, x, y, direction):
        return (self.game_map.getSite(Location(x, y), direction), direction)


    def get_movement(self, current_site):
        north_cell = self.get_cell(current_site.x, current_site.y, NORTH)
        east_cell = self.get_cell(current_site.x, current_site.y, EAST)
        south_cell = self.get_cell(current_site.x, current_site.y, SOUTH)
        west_cell = self.get_cell(current_site.x, current_site.y, WEST)

        todos_vizinhos = [north_cell, east_cell, south_cell, west_cell]

        vizinhos_inimigos = [vizinho for vizinho in todos_vizinhos if vizinho[0].owner != self.my_id]

        # ATTACK!
        if vizinhos_inimigos:
            enemy_with_max_production = min(vizinhos_inimigos, key=lambda v: v[0].strength)

            if enemy_with_max_production[0].strength <= current_site.strength:
                return Move(Location(current_site.x, current_site.y), enemy_with_max_production[1])
            else:
                return Move(Location(current_site.x, current_site.y), STILL)

        # WEAK, STILL!
        if current_site.strength < current_site.production * 5:
            return Move(Location(current_site.x, current_site.y), STILL)

        # MOVE
        closest_enemy = min(self.enemies_locations, key=lambda enemy: self.game_map.getDistance(Location(current_site.x, current_site.y), enemy))

        direction = self.game_map.getDirectionTo(closest_enemy, Location(current_site.x, current_site.y))
        return Move(Location(current_site.x, current_site.y), direction)


if __name__ == "__main__":
    try:
        logging.info("startando")
        Main()
    except:
        logging.exception("Oops:")

