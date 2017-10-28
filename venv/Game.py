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
            self.map.map[bot1.xPos][bot1.yPos][0] = 1
            self.map.map[x-1][y][1] = self.bot1
        elif bot1Dir == 'S':
            self.map.map[bot1.xPos][bot1.yPos][0] = 1
            self.map.map[x+1][y][1] = self.bot1
        elif bot1Dir == 'E':
            self.map.map[bot1.xPos][bot1.yPos][0] = 1
            self.map.map[x][y+1][1] = self.bot1
        else:
            self.map.map[bot1.xPos][bot1.yPos][0] = 1
            self.map.map[x][y-1][1] = self.bot1
        if bot2Dir == 'N':
            self.map.map[bot2.xPos][bot2.yPos][0] = 1
            self.map.map[x-1][y][1] = self.bot2
        elif bot2Dir == 'S':
            self.map.map[bot2.xPos][bot2.yPos][0] = 1
            self.map.map[x+1][y][1] = self.bot2
        elif bot2Dir == 'E':
            self.map.map[bot2.xPos][bot2.yPos][0] = 1
            self.map.map[x][y+1][1] = self.bot2
        else:
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 2
                    self.map.map[x][y-1][0] = 0
                    self.map.map[x][y-1][1] = self.bot2
        print(self.map.map)

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
