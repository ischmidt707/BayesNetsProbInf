from Network import *


class Gibbs():

    def __init__(self, query, net, evidence):
        self.query = query
        self.net = net
        self.evidence = evidence
        self.result = 0

        self.net.loadEvidence(self.e)

        self.e = []
        for l in evidence:
            self.e.append(self.getNode(l[0]))

    def getNode(self, name):
        return self.net.nodes[name]

    def solve(self):
        return self.result
