from Node import *


# uses the fact dictionaries are ordered, so need Python 3.6+


class Network():

    # init network
    def __init__(self, filename):
        self.nodes = {}
        self.factors = {}
        self.name = filename[:-4]
        self.loadBNet(filename)
        self.popChildren()

    # method to load network from a .BIF file
    def loadBNet(self, filename):
        file = open(filename, "r")
        for line in file:
            sep = line.split(" ")
            if sep[0] == "variable":  # start process of assigning new node
                self.nodes[sep[1]] = Node(sep[1])  # the keys in self.nodes are the variable names
                nline = file.readline()  # move to next line to read in possible values
                nextsplit = nline.split(" ")
                try:
                    while True:
                        nextsplit.remove('')
                except ValueError:
                    pass
                count = int(nextsplit[3])
                for i in range(count):
                    val = nextsplit[i + 6].replace(",", '')
                    self.nodes[sep[1]].possValues.append(val)
            if sep[0] == "probability":  # start to populate CPD
                cur = self.nodes[sep[2]]
                for i in range(4, len(sep) - 2):
                    par = sep[i].replace(',', '')
                    cur.parents.append(par)
                num = len(cur.parents)
                broken = False
                while not broken:
                    probline = file.readline()
                    probline = probline.split(" ")
                    try:
                        while True:
                            probline.remove('')
                    except ValueError:
                        pass
                    if probline[0] == "table":  # only occurs in file when node has 0 parents
                        cur.CPD["always"] = []
                        for i in range(1, len(probline)):
                            val = probline[i].replace(",", '')
                            val = float(val.replace(";\n", ''))  # this is not good coding
                            cur.CPD[("always")].append(val)
                        broken = True
                    elif probline[0] == "}\n":  # reaches end of list of values so break
                        broken = True
                    else:  # means we are populating CPD of something with parents now
                        valkey = []
                        for i in range(num):
                            var = probline[i].replace("(", '')
                            var = var.replace(")", '')
                            valkey.append(var)
                        valkey = tuple(valkey)  # apparently cant use lists as dict keys so convert to tuple
                        cur.CPD[valkey] = []
                        for i in range(num, len(probline)):
                            val = probline[i].replace(",", '')
                            val = float(val.replace(";\n", ''))  # this is not good coding
                            cur.CPD[valkey].append(val)
        # in theory this should be all we need to import everything
        # somehow make factors list for variable elimination? idk how tf that works

    def popChildren(self):
        for node in self.nodes.values():
            for i in node.parents:
                self.nodes[i].children.append(node.name)

    def loadEvidence(self, evidence):
        for n in evidence:
            self.nodes[n[0]].value = n[1]



if __name__ == "__main__":
    testnet = Network("alarm.bif")
    for node in testnet.nodes.values():
        print(node.name)
        print(node.parents)
        print(node.children)
        print(node.CPD)
