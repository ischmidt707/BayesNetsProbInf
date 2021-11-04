from Network import *

class Gibbs():

    def __init__(self, query, net, evidence):
        self.query = query
        self.net = net
        self.evidence = evidence
        self.result = 0

    def solve(self):
        return self.result