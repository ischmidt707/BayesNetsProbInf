from Network import *
from Node import *
from queue import Queue
from Factor import *


class VarElim():

    def __init__(self, query, evidence, net):
        self.X = query
        self.e = evidence
        self.net = net
        self.result = 0
        self.order = []
        self.factors = []

    def isHidden(self, var):
        return var != self.X and var not in self.e

    def sumOut(self):
        pass

    def pwProd(self):
        pass

    def orderTopo(self):
        q = Queue(0)
        vis = 0  # count of visited nodes

        for var in self.net.nodes.values():
            var.inDeg = len(var.parents)
            if(var.inDeg == 0):
                q.put_nowait(var)

        while not q.empty():
            cur = q.get_nowait()
            self.order.append(cur)
            vis += 1
            for c in cur.children:
                c.inDeg -= 1
                if(c.inDeg == 0):
                    q.put_nowait(c)

    def makeFactor(self, var):
        variables = []
        if(var not in self.e):
            variables.append(var)
        for p in var.parents:
            variables.append(p)

        if(var in self.e):
            
        self.factors.append(Factor(variables))


    def solve(self):
        for var in reversed(self.order):  # We will use a reverse topological ordering
            if(not self.isHidden(var)):  # make sure the node is relevant (query, evidence, or ancestor)
                var.used = True
            else:
                for c in var.children:
                    if(c.used):
                        var.used = True
                        break

            if(var.used):


        return self.result
