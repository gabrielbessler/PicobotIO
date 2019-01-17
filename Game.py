from random import randint
from Item import Item


class Game:
    '''
    Contains all of the information for a particular match (instance of the game),
    including boardstate and player positions
    '''
    def __init__(self, map, item_delay=10):
        '''
        Constructor for Game given two Picobots and a map
        '''
        self.bot1 = map.p1
        self.bot2 = map.p2
        self.map = map
        self.item_delay = item_delay
        self.curr_num_items = 0

    def update(self):
        '''
        Uses the direction and current position of both players to update their
        positions on the map
        '''
        # Get the surroundings of both players
        surr1 = self.map.getSurroundings(self.bot1.xPos, self.bot1.yPos)
        surr2 = self.map.getSurroundings(self.bot2.xPos, self.bot2.yPos)

        # Get the directions of both players
        bot_1_dir = self.bot1.getDir(self.map.getSurroundings(self.bot1.xPos,
                                                              self.bot1.yPos))
        bot_2_dir = self.bot2.getDir(self.map.getSurroundings(self.bot2.xPos,
                                                              self.bot2.yPos))

        # Updates the position for player 1
        if bot_1_dir == 'N' and surr1[0] != "x":
            self.map.map[self.bot1.yPos][self.bot1.xPos] = [1, 0]
            self.bot1.yPos -= 1
            self.map.map[self.bot1.yPos][self.bot1.xPos][1] = self.bot1
        elif bot_1_dir == 'S' and surr1[1] != "x":
            self.map.map[self.bot1.yPos][self.bot1.xPos] = [1, 0]
            self.bot1.yPos += 1
            self.map.map[self.bot1.yPos][self.bot1.xPos][1] = self.bot1
        elif bot_1_dir == 'E' and surr1[2] != "x":
            self.map.map[self.bot1.yPos][self.bot1.xPos] = [1, 0]
            self.bot1.xPos += 1
            self.map.map[self.bot1.yPos][self.bot1.xPos][1] = self.bot1
        elif bot_1_dir == 'W' and surr1[3] != "x":
            self.map.map[self.bot1.yPos][self.bot1.xPos] = [1, 0]
            self.bot1.xPos -= 1
            self.map.map[self.bot1.yPos][self.bot1.xPos][1] = self.bot1

        # Update the position for player 2
        if bot_2_dir == 'N' and surr2[0] != "x":
            self.map.map[self.bot2.yPos][self.bot2.xPos] = [2, 0]
            self.bot2.yPos -= 1
            self.map.map[self.bot2.yPos][self.bot2.xPos][1] = self.bot2
        elif bot_2_dir == 'S' and surr2[1] != "x":
            self.map.map[self.bot2.yPos][self.bot2.xPos] = [2, 0]
            self.bot2.yPos += 1
            self.map.map[self.bot2.yPos][self.bot2.xPos][1] = self.bot2
        elif bot_2_dir == 'E' and surr2[2] != "x":
            self.map.map[self.bot2.yPos][self.bot2.xPos] = [2, 0]
            self.bot2.xPos += 1
            self.map.map[self.bot2.yPos][self.bot2.xPos][1] = self.bot2
        elif bot_2_dir == 'W' and surr2[3] != "x":
            self.map.map[self.bot2.yPos][self.bot2.xPos] = [2, 0]
            self.bot2.xPos -= 1
            self.map.map[self.bot2.yPos][self.bot2.xPos][1] = self.bot2

        # Save the changes in position to the map
        self.map.p1.yPos = self.bot1.yPos
        self.map.p1.xPos = self.bot1.xPos
        self.map.p2.yPos = self.bot2.yPos
        self.map.p2.xPos = self.bot2.xPos

    def getScore(self):
        '''
        Counts the numbers of squares that each player currently
        has colored on the map
        Returns the scores in [player1score, player2score]
        '''
        score1 = 0
        score2 = 0
        for x in range(20):
            for y in range(20):
                if self.map.map[x][y][0] == 1:
                    score1 += 1
                if self.map.map[x][y][0] == 2:
                    score2 += 1
        return [score1, score2]

    def spawn_item(self):
        '''
        Spawns at an item at a random location on the screen
        '''
        r = randint(1, self.item_delay)
        if r == 1:
            new_item = Item(1)
            x_spawn = randint(0, 19)
            y_spawn = randint(0, 19)
            obj = self.map.map[x_spawn][y_spawn][1]
            if obj != "Wall()":
                self.curr_num_items += 1
                # make sure that the tile stays the same color,
                # but spawn in the new item
                L = [self.map.map[x_spawn][y_spawn][0], new_item]
                self.map.map[x_spawn][y_spawn] = L
