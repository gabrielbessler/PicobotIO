# Map Class

import Wall
import Item
import Picobot
import random
class Map(object):
    
    # map constructor with type
    def __init__(self, mapType):
        self.start1 = [0,0,1]
        self.start2 = [20, 20, 2]
        self.map = generate(mapType)

    # return map
    def getMap():
        self.map[start1[0], start1[1]] = [1, Picobot(start1[2], [])]
        self.map[start2[0], start2[1]] = [2, Picobot(start2[2], [])]
        # checkConsistent(self.map)
        return self.map
    
    # generate Map
    def generate(mapType):
        size = 20
        column = [[0, null] for x in range(size)]
        board = [column for x in range(size)]
        if mapType == "default":
            return board
        if mapType == "type1":
            for i in range(size/2 - size/10, size/2 + size/10):
                for j in range(size/2 - size/10, size/2 + size/10):
                    board[i][j] = [0, Wall()]
            return board
        if mapType == "random":
            for i in range(size):
                for j in range(size):
                    randNum = random.randint(1, 101)
                    if randNum < 21:
                        board[i][j] = [0, Wall()]
            return board


    # return a string with the surroundings
    def getSurroundings(xPos, yPos):
        if self.map[xPos, yPos + 1][1] == Wall():
            north = "x"
        else:
            north = "_"
        if self.map[xPos - 1, yPos][1] == Wall():
            west = "x"
        else: 
            west = "_"
        if self.map[xPos + 1, yPos][1] == Wall():
            east = "x"
        else:
            east = "_"
        if self.map[xPos, yPos - 1][1] == Wall():
            south = "x"
        else:
            south = "_"
        surroundings = north + south + east + west
        return surroundings

    # return the map's size
    def getSize():
        return this.size

    # check consistent map
    '''
    def checkConsistent(map):
    '''
