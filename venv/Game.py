import Picobot
import Map

class Game(object):
    def __init__(self, map):
        """constructor for Game given two Picobots and a map"""
        self.bot1 = map.p1
        self.bot2 = map.p2
        self.map = map

    def update(self):
        """update the positions of the bots"""
        bot1Dir = self.bot1.getDir(self.map.getSurroundings(self.bot1.xPos,self.bot1.yPos))
        bot2Dir = self.bot2.getDir(self.map.getSurroundings(self.bot2.xPos,self.bot2.yPos))
        if bot1Dir == 'N':
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 1
                    self.map.map[x-1][y][0] = 0
                    self.map.map[x-1][y][1] = self.bot1
        elif bot1Dir == 'S':
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 1
                    self.map.map[x+1][y][0] = 0
                    self.map.map[x+1][y][1] = self.bot1
        elif bot1Dir == 'E':
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 1
                    self.map.map[x][y+1][0] = 0
                    self.map.map[x][y+1][1] = self.bot1
        else:
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 1
                    self.map.map[x][y-1][0] = 0
                    self.map.map[x][y-1][1] = self.bot1
        if bot2Dir == 'N':
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 2
                    self.map.map[x-1][y][0] = 0
                    self.map.map[x-1][y][1] = self.bot2
        elif bot2Dir == 'S':
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 2
                    self.map.map[x+1][y][0] = 0
                    self.map.map[x+1][y][1] = self.bot2
        elif bot2Dir == 'E':
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 2
                    self.map.map[x][y+1][0] = 0
                    self.map.map[x][y+1][1] = self.bot2
        else:
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 2
                    self.map.map[x][y-1][0] = 0
                    self.map.map[x][y-1][1] = self.bot2

    # scoring function
    def getScore(self):
        score1 = 0
        score2 = 0
        for x in range(20):
            for y in range(20):
                if self.map.map[x][y][0] == 1:
                    score1 += 1
                if self.map.map[x][y][0] == 2:
                    score2 += 1
        return [score1, score2]
