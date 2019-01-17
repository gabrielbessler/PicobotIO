import random
from Wall import Wall
from Picobot import Picobot


class Map():
    '''
    Stores all of the tiles in an instance of the game
    '''
    def __init__(self, mapType):
        '''
        Creates a new map and then poulates it using mapType
        '''
        # BUG: make sure that start1 and start2 are correctly updated
        self.start1 = [1, 1, 1]
        self.start2 = [18, 18, 2]
        self.map = self.generate(mapType)
        self.p1 = Picobot(self.start1, [])
        self.p2 = Picobot(self.start2, [])
        self.map[1][1] = [1, self.p1]
        self.map[18][18] = [2, self.p2]
        self.size = 20

    def generate(self, map_type):
        '''
        Given a map type, initialises a new map in the type of the 2D list
        '''
        size = 20
        board = [[[0, 0] for x in range(size)] for y in range(size)]
        w = [0, Wall()]
        for i in range(0, 20):
            board[0][i] = w
            board[19][i] = w
            board[i][0] = w
            board[i][19] = w

        if map_type == "type1":
            for i in range(8, 12):
                for j in range(8, 12):
                    board[i][j] = w
            self.start1 = [1, 1, 1]
            self.start2 = [18, 18, 2]
        elif map_type == "random":
            for i in range(size):
                for j in range(size):
                    rand_num = random.randint(1, 101)
                    if rand_num < 21:
                        board[i][j] = w
        elif map_type == "diamond":
            for i in range(1, 9):
                for j in range(1, 10-i):
                    board[i][j] = w
                    board[19 - i][j] = w
                    board[i][19 - j] = w
                    board[19 - i][19 - j] = w
            self.start1 = [1, 9, 1]
            self.start2 = [18, 10, 2]
        elif map_type == "islands":
            for i in range(3, 7):
                for j in range(3, 7):
                    board[i][j] = w
            for i in range(13, 17):
                for j in range(13, 17):
                    board[i][j] = w
            for i in range(13, 17):
                for j in range(3, 7):
                    board[i][j] = w
            for i in range(3, 7):
                for j in range(13, 17):
                    board[i][j] = w
            self.start1 = [1, 1, 1]
            self.start2 = [18, 18, 2]
        return board

    def getSurroundings(self, x_pos, y_pos):
        '''
        Return a string with the surroundings of a given x_pos, y_pos
        '''
        # TODO: shorten this by using a for loop
        if self.map[y_pos-1][x_pos][1] == "Wall()":
            north = "x"
        else:
            north = "_"
        if self.map[y_pos][x_pos-1][1] == "Wall()":
            west = "x"
        else:
            west = "_"
        if self.map[y_pos][x_pos + 1][1] == "Wall()":
            east = "x"
        else:
            east = "_"
        if self.map[y_pos+1][x_pos][1] == "Wall()":
            south = "x"
        else:
            south = "_"
        surroundings = north + south + east + west
        return surroundings

    def get_sze(self):
        '''
        Returns the map's size
        '''
        return self.size

    def getMap(self):
        '''
        Returns a representation of the map where each object is converted
        to its string representation
        '''
        temp_map = self.map
        for i in range(20):
            for j in range(20):
                temp_map[i][j][1] = str(self.map[i][j][1])
        return temp_map

    def check_consistent(self, map):
        '''
        TODO: check if the map is consistent
        '''
