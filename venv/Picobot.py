# Picobot Class

def Picobot(object):

    # constructor
    def __init__(xPos, yPos, rules):
        self.xPos = xPos
        self.yPos = yPos
        self.ruleList = rules
        self.currentState = 0
    
    def getDir(surroundings):
        for rule in rules:
            if self.currentState == rule[0] and surroundings == rule[1]:
                self.currentState = rule[3]
                return rule[2]
        return
        


