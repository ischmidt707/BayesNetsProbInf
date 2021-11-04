from Network import *


class VarElim():

    def __init__(self, query, net, evidence):
        self.query = query
        self.net = net
        self.evidence = evidence
        self.result = 0
        self.ordering = 0

    def sumout(self):
        pass

    def multfactors(self):
        pass

    def solve(self):
        return self.result
