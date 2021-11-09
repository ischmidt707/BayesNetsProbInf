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

    def sumOut(self, var):
        newFactors = []  # This will eventually replace self.factors
        vFactors = []  # List of factors that need summing out
        for f in self.factors:
            if var in f.vars:
                vFactors.append(f)
            else:
                newFactors.append(f)

        for f in vFactors:
            variables = []
            for v in f.vars:
                if(v.name != var.name):
                    variables.append(v)

            # Generate a new empty truth table
            newTruTable = {}
            tableDims = []

            for v in variables:
                if v.value == "":
                    tableDims.append(len(v.possValues))
                    rows = rows * len(v.possValues)
                else:
                    tableDims.append(1)

            counters = []
            for v in tableDims:
                counters.append(0)
            for row in range(rows):
                rowKey = []
                for v in range(len(counters)):
                    rowKey.append(variables[v].possValues[counters[v]])
                tuple(rowKey)
                newTruTable[rowKey] = []

                if (row == rows - 1):  # that was the last row, so exit loop
                    break

                i = -1
                counters[i] += 1  # keep track of truth table values via a list of counters
                while (counters[i] == tableDims[i]):
                    counters[i] = 0
                    i -= 1
                    counters[i] += 1

            # Fill out values of new truth table, as list items to be added
            for key in newTruTable:
                for oldKey, oldValue in f.truTable:
                    if all(v in oldKey for v in key):
                        newTruTable[key].append(oldValue)

                # Sum list items together to get the new values
                sumOf = 0
                for val in newTruTable[key]:
                    sumOf = sumOf + val
                newTruTable[key] = sumOf
            newFactors.append(Factor(variables, newTruTable))  # Add new summed out factor into factors

        self.factors = newFactors  # Replace old list of factors with new list

    def pwProd(self, f1, f2):

        # List out union of variables from each factor
        variables = []
        for v in f1.vars:
            variables.append(v)
        for v in f2.vars:
            if v not in variables:
                variables.append(v)

        # Generate a new empty truth table
        newTruTable = {}
        tableDims = []

        for v in variables:
            if v.value == "":
                tableDims.append(len(v.possValues))
                rows = rows * len(v.possValues)
            else: tableDims.append(1)

        counters = []
        for v in tableDims:
            counters.append(0)
        for row in range(rows):
            rowKey = []
            for v in range(len(counters)):
                rowKey.append(variables[v].possValues[counters[v]])
            tuple(rowKey)
            newTruTable[rowKey] = []

            if(row == rows-1):  # that was the last row, so exit loop
                break

            i = -1
            counters[i] += 1  # keep track of truth table values via a list of counters
            while(counters[i] == tableDims[i]):
                counters[i] = 0
                i -= 1
                counters[i] += 1
        # ^ Done creating empty valued truth table ^

        # Fill out values of new truth table, as list items
        for key in newTruTable:
            for oldKey, oldValue in {**f1.truTable, **f2.truTable}:  # iterate through both Factor's tables
                if all(v in key for v in oldKey):
                    newTruTable[key].append(oldValue)

            # Multiply list items together to get the new values
            prod = 1
            for val in newTruTable[key]:
                prod = prod * val
            newTruTable[key] = prod



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
        variables = []  # will create a factor with list of dependent variables and a truth table
        truTable = {}

        tableDims = []
        rows = 1

        variables.append(var)
        for p in var.parents:
            variables.append(p)

        for v in variables:
            if v.value == "":
                tableDims.append(len(v.possValues))
                rows = rows * len(v.possValues)
            else: tableDims.append(1)

        counters = []
        for v in tableDims:
            counters.append(0)
        for row in range(rows):
            rowKey = []
            for v in range(len(counters)):
                rowKey.append(variables[v].possValues[counters[v]])
            tuple(rowKey)
            truTable[rowKey] = var.CPD[rowKey]

            if(row == rows-1):  # that was the last row, so exit loop
                break

            i = -1
            counters[i] += 1  # keep track of truth table values via a list of counters
            while(counters[i] == tableDims[i]):
                counters[i] = 0
                i -= 1
                counters[i] += 1

        self.factors.append(Factor(variables, truTable))


    def solve(self):
        self.orderTopo()
        for var in reversed(self.order):  # We will use a reverse topological ordering
            if(not self.isHidden(var)):  # make sure the node is relevant (query, evidence, or ancestor)
                var.used = True
            else:
                for c in var.children:
                    if(c.used):
                        var.used = True
                        break

            if(var.used):
                self.makeFactor(var)
                if(self.isHidden((var))):
                    self.sumOut(var)


        return self.result
