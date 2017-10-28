import Picobot
import Map

class Game(object):
    def __init__(bot1, bot2, map):
        """constructor for Game given two Picobots and a map"""
        self.bot1 = bot1;
        self.bot2 = bot2;
        self.map = map;
    
    def update():
        """update the positions of the bots"""
        bot1Dir = bot1.getDirection(self.map.getSurroundings(bot1.x,bot1.y))
        bot2Dir = bot2.getDirection(self.map.getSurroundings(bot2.x,bot2.y))
        if bot1Dir == 'N':
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 1
                    self.map.map[x-1][y][0] = 0
                    self.map.map[x-1][y][1] = bot1
        elif bot1Dir == 'S':
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 1
                    self.map.map[x+1][y][0] = 0
                    self.map.map[x+1][y][1] = bot1
        elif bot1Dir == 'E':
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 1
                    self.map.map[x][y+1][0] = 0
                    self.map.map[x][y+1][1] = bot1
        else:
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 1
                    self.map.map[x][y-1][0] = 0
                    self.map.map[x][y-1][1] = bot1
        if bot2Dir == 'N':
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 2
                    self.map.map[x-1][y][0] = 0
                    self.map.map[x-1][y][1] = bot2
        elif bot2Dir == 'S':
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 2
                    self.map.map[x+1][y][0] = 0
                    self.map.map[x+1][y][1] = bot2
        elif bot2Dir == 'E':
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 2
                    self.map.map[x][y+1][0] = 0
                    self.map.map[x][y+1][1] = bot2
        else:
            for x in range(0,self.map.getSize()):
                for y in range(0,self.map.getSize()):
                    self.map.map[x][y][0] = 2
                    self.map.map[x][y-1][0] = 0
                    self.map.map[x][y-1][1] = bot2


