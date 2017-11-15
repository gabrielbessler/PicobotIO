class Picobot(object):

    # constructor
    def __init__(self, L, rules):
        '''
        Create a new picobot given L, where L is a list of the form
        [x position, y position, color]
        and a set of rules for he picobot
        '''
        self.xPos = L[0]
        self.yPos = L[1]
        self.color = L[2]
        self.ruleList = rules
        self.currentState = 0

    def getDir(self, surroundings):
        '''
        Calculates what direction Picobot should go in given its surroundings
        and using the picobot's ruleList
        '''
        for rule in self.ruleList:
            if self.currentState == rule[0]:
                matches = True
                for i in range(0, 4):
                    if surroundings[i] != rule[1][i] and rule[1][i] != '*':
                        matches = False
                if matches:
                    self.currentState = rule[3]
                    return rule[2]

    def __repr__(self):
        '''
        Returns a representation of the picobot that can be displayed on the board
        '''
        return "Picobot(" + str(self.color) + ")"
