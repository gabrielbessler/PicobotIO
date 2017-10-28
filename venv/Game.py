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
        surr1 = self.map.getSurroundings(self.bot1.xPos,self.bot1.yPos)
        surr2 = self.map.getSurroundings(self.bot2.xPos,self.bot2.yPos)
        bot1Dir = self.bot1.getDir(self.map.getSurroundings(self.bot1.xPos,self.bot1.yPos))
        bot2Dir = self.bot2.getDir(self.map.getSurroundings(self.bot2.xPos,self.bot2.yPos))
        if bot1Dir == 'N' and surr1[0] != "x":
            self.map.map[self.bot1.yPos][self.bot1.xPos] = [1,0]
            self.bot1.yPos -= 1
            self.map.map[self.bot1.yPos][self.bot1.xPos][1] = self.bot1
        elif bot1Dir == 'S' and surr1[1] != "x":
            self.map.map[self.bot1.yPos][self.bot1.xPos] = [1,0]
            self.bot1.yPos += 1
            self.map.map[self.bot1.yPos][self.bot1.xPos][1] = self.bot1
        elif bot1Dir == 'E' and surr1[2] != "x":
            self.map.map[self.bot1.yPos][self.bot1.xPos] = [1,0]
            self.bot1.xPos += 1
            self.map.map[self.bot1.yPos][self.bot1.xPos][1] = self.bot1
        elif bot1Dir == 'W' and surr1[3] != "x":
            self.map.map[self.bot1.yPos][self.bot1.xPos] = [1,0]
            self.bot1.xPos -= 1
            self.map.map[self.bot1.yPos][self.bot1.xPos][1] = self.bot1

        if bot2Dir == 'N' and surr2[0] != "x":
            self.map.map[self.bot2.yPos][self.bot2.xPos] = [2,0]
            self.bot2.yPos -= 1
            self.map.map[self.bot2.yPos][self.bot2.xPos][1] = self.bot2
        elif bot2Dir == 'S' and surr2[1] != "x":
            self.map.map[self.bot2.yPos][self.bot2.xPos] = [2,0]
            self.bot2.yPos += 1
            self.map.map[self.bot2.yPos][self.bot2.xPos][1] = self.bot2
        elif bot2Dir == 'E' and surr2[2] != "x":
            self.map.map[self.bot2.yPos][self.bot2.xPos] = [2,0]
            self.bot2.xPos += 1
            self.map.map[self.bot2.yPos][self.bot2.xPos][1] = self.bot2
        elif bot2Dir == 'W' and surr2[3] != "x":
            self.map.map[self.bot2.yPos][self.bot2.xPos] = [2,0]
            self.bot2.xPos -= 1
            self.map.map[self.bot2.yPos][self.bot2.xPos][1] = self.bot2

        self.map.p1.yPos = self.bot1.yPos
        self.map.p1.xPos = self.bot1.xPos
        self.map.p2.yPos = self.bot2.yPos
        self.map.p2.xPos = self.bot2.xPos


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
