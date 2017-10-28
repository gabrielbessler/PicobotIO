# Picobot Class

class Picobot(object):

    # constructor
    def __init__(self, L, rules):
        self.xPos = L[0]
        self.yPos = L[1]
        self.color = L[2]
        self.ruleList = rules
        self.currentState = 0

    def getDir(self, surroundings):
        for rule in self.ruleList:
            if self.currentState == rule[0] and surroundings == rule[1]:
                self.currentState = rule[3]
                return rule[2]
        return


    def __repr__(self):
        return "Picobot(" + str(self.color) + ")"
