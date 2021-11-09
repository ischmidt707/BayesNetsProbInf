class Factor():

    def __init__(self, vars, truTable):
        self.vars = vars
        self.truTable = truTable

    def normalize(self):
        sumValues = 0
        for key, value in self.truTable:
            sumValues += value
        for key, value in self.truTable:
            self.truTable[key] = value / sumValues