# Picobot Class

class Picobot(object):

    # constructor
    def __init__(self, L, rules):
        self.xPos = L[0]
        self.yPos = L[1]
        self.color = L[2]
        rules = [[0, "_xx_", "N", 0],[0, "__x_", "N", 0], [0, "x_x_", "W", 1], [1, "x___", "S", 2], [2, "____", "S", 2]]
        self.ruleList = rules
        self.currentState = 0

    def getDir(self, surroundings):
        for rule in self.ruleList:
            print(rule)
            if self.currentState == rule[0]:
                print('ok')
                matches = True
                for x in range(0,4):
                    if surroundings[x] != rule[1][x] and rule[1][x] != '*':
                        matches = False
                print(matches)
                if matches:
                    print('2')
                    self.currentState = rule[3]
                    return rule[2]
        return


    def __repr__(self):
        return "Picobot(" + str(self.color) + ")"
