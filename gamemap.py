import random
import math
import copy

STILL = 0
NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4

DIRECTIONS = [a for a in range(0, 5)]
CARDINALS = [a for a in range(1, 5)]

ATTACK = 0
STOP_ATTACK = 1

class GameMap:
    def __init__(self, width = 0, height = 0, numberOfPlayers = 0):
        self.width = width
        self.height = height
        self.contents = []

        for y in range(0, self.height):
            row = []
            for x in range(0, self.width):
                row.append(Site(0, 0, 0, x, y))
            self.contents.append(row)

    def inBounds(self, l):
        return l.x >= 0 and l.x < self.width and l.y >= 0 and l.y < self.height

    def getDistance(self, l1, l2):
        dx = abs(l1.x - l2.x)
        dy = abs(l1.y - l2.y)
        if dx > self.width / 2:
            dx = self.width - dx
        if dy > self.height / 2:
            dy = self.height - dy
        return dx + dy

    def getAngle(self, l1, l2):
        dx = l2.x - l1.x
        dy = l2.y - l1.y

        if dx > self.width - dx:
            dx -= self.width
        elif -dx > self.width + dx:
            dx += self.width

        if dy > self.height - dy:
            dy -= self.height
        elif -dy > self.height + dy:
            dy += self.height
        return math.atan2(dy, dx)

    def getLocation(self, loc, direction):
        l = copy.deepcopy(loc)
        if direction != STILL:
            if direction == NORTH:
                if l.y == 0:
                    l.y = self.height - 1
                else:
                    l.y -= 1
            elif direction == EAST:
                if l.x == self.width - 1:
                    l.x = 0
                else:
                    l.x += 1
            elif direction == SOUTH:
                if l.y == self.height - 1:
                    l.y = 0
                else:
                    l.y += 1
            elif direction == WEST:
                if l.x == 0:
                    l.x = self.width - 1
                else:
                    l.x -= 1
        return l

    def getSite(self, l, direction = STILL):
        l = self.getLocation(l, direction)
        return self.contents[l.y][l.x]

    def move(self, loc, direction):
        self.contents[loc.y][loc.x]

    def getDirectionTo(self, from_cell, to_cell):
        if to_cell.y > from_cell.y:
            return NORTH
        elif to_cell.y < from_cell.y:
            return SOUTH
        elif to_cell.x < from_cell.x:
            return EAST
        elif to_cell.x > from_cell.x:
            return WEST

        return STILL


class Move:
    def __init__(self, loc=0, direction=0):
        self.loc = loc
        self.direction = direction


class Location:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "Location({},{})".format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))


class Site:
    def __init__(self, owner=0, strength=0, production=0, x = -1, y = -1):
        self.owner = owner
        self.strength = strength
        self.production = production
        self.x = x
        self.y = y
