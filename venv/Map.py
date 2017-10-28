# Map Class

from Wall import Wall
from Item import Item
from Picobot import Picobot
import random
class Map():

    # map constructor with type
    def __init__(self, mapType):
        self.start1 = [1,1,1]
        self.start2 = [18, 18, 2]
        self.map = self.generate(mapType)
        self.p1 = Picobot(self.start1, [])
        self.p2 = Picobot(self.start2, [])
        self.map[1][1] = [1, self.p1]
        self.map[18][18] = [2, self.p2]
        self.size = 20

    # generate Map
    def generate(self, mapType):
        size = 20
        board =[[[0, 0] for x in range(size)] for y in range(size)]
        if mapType == "default":
            return board
        if mapType == "type1":
            for i in range(0, 20):
                w = Wall()
                board[0][i] = [0, w]
                board[19][i] = [0, w]
                board[i][0] = [0, w]
                board[i][19] = [0, w]
            for i in range(8, 12):
                for j in range(8, 12):
                    w = Wall()
                    board[i][j] = [0, w]
            return board
        if mapType == "random":
            for i in range(size):
                for j in range(size):
                    randNum = random.randint(1, 101)
                    if randNum < 21:
                        board[i][j] = [0, Wall()]
            return board


    # return a string with the surroundings
    def getSurroundings(self, xPos, yPos):
        print(yPos, xPos)
        if self.map[yPos + 1][xPos][1] == Wall():
            north = "x"
        else:
            north = "_"
        if self.map[yPos][xPos - 1][1] == Wall():
            west = "x"
        else:
            west = "_"
        if self.map[yPos][xPos + 1][1] == Wall():
            east = "x"
        else:
            east = "_"
        if self.map[yPos - 1][xPos][1] == Wall():
            south = "x"
        else:
            south = "_"
        surroundings = north + south + east + west
        return surroundings

    # return the map's size
    def getSize(self):
        return self.size

    # returns the map
    def getMap(self):
        tempMap = self.map
        for i in range(20):
            for j in range(20):
                tempMap[i][j][1] = str(self.map[i][j][1])
        return tempMap

    # check consistent map
    '''
    def checkConsistent(map):
    '''
