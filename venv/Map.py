# Map Class

import random
from Wall import Wall
from Item import Item
from Picobot import Picobot

class Map():

    # map constructor with type
    def __init__(self, mapType):
        '''

        '''
        self.start1 = [1,1,1]
        self.start2 = [18,18,2]
        self.map = self.generate(mapType)
        self.p1 = Picobot(self.start1, [])
        self.p2 = Picobot(self.start2, [])
        self.map[1][1] = [1, self.p1]
        self.map[18][18] = [2, self.p2]
        self.size = 20

    # generate Map
    def generate(self, mapType):
        '''
        Given a map type, initialises a new map in the type of the 2D list
        '''
        size = 20
        board =[[[0, 0] for x in range(size)] for y in range(size)]
        w = [0, Wall()]
        for i in range(0, 20):
                board[0][i] = w
                board[19][i] = w
                board[i][0] = w
                board[i][19] = w
        if mapType == "type1":
            for i in range(8, 12):
                for j in range(8, 12):
                    board[i][j] = w
            self.start1 = [1, 1, 1]
            self.start2 = [18, 18, 2]
        if mapType == "random":
            for i in range(size):
                for j in range(size):
                    rand_num = random.randint(1, 101)
                    if rand_num < 21:
                        board[i][j] = w
        if mapType == "diamond":
            for i in range(1, 9):
                for j in range(1, 10-i):
                    board[i][j] = w
                    board[19 - i][j] = w
                    board[i][19 - j] = w
                    board[19- i][19 - j] = w
            self.start1 = [1, 9, 1]
            self.start2 = [18, 10, 2]

        if mapType == "islands":
            for i in range(3, 7):
                for j in range(3, 7):
                    board[i][j] = w
            for i in range(13, 17):
                for j in range(13, 17):
                    board[i][j] = w
            for i in range(13, 17):
                for j in range(3,7):
                    board[i][j] = w
            for i in range(3, 7):
                for j in range(13, 17):
                    board[i][j] = w
            self.start1 = [1, 1, 1]
            self.start2 = [18, 18, 2]
        return board

    # return a string with the surroundings
    def getSurroundings(self, xPos, yPos):

        if self.map[yPos-1][xPos][1] == "Wall()":
            north = "x"
        else:
            north = "_"
        if self.map[yPos][xPos-1][1] == "Wall()":
            west = "x"
        else:
            west = "_"
        if self.map[yPos][xPos + 1][1] == "Wall()":
            east = "x"
        else:
            east = "_"
        if self.map[yPos+1][xPos][1] == "Wall()":
            south = "x"
        else:
            south = "_"
        surroundings = north + south + east + west
        return surroundings

    def getSize(self):
        '''
        Returns the map's size
        '''
        return self.size

    def getMap(self):
        '''
        Returns a representation of the map where each object is converted
        to its string representation
        '''
        tempMap = self.map
        for i in range(20):
            for j in range(20):
                tempMap[i][j][1] = str(self.map[i][j][1])
        return tempMap

    def checkConsistent(self, map):
        '''
        TODO: check if the map is consistent
        '''
        pass
