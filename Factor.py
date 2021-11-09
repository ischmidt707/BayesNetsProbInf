class Factor():

    def __init__(self, vars, truTable):
        self.vars = vars
        self.truTable = truTable

    def normalize(self):
        sumValues = 0
        for key in self.truTable:
            sumValues += sum(self.truTable[key])
        for key in self.truTable:
            for i in range(len(self.truTable[key])):
                self.truTable[key][i] = self.truTable[key][i] / sumValues