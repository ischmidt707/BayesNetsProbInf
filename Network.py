from Node import *


class Network():

    # init network
    def __init__(self, filename):
        self.nodes = {}
        self.factors = {}
        self.name = filename[:-4]
        self.loadBNet(filename)

    # method to load network from a .BIF file
    def loadBNet(self, filename):
        file = open(filename, "r")
        for line in file:
            sep = line.split(" ")
            if sep[0] == "variable":  # start process of assigning new node
                self.nodes[sep[1]] = Node(sep[1])
                next = file.readline()  # move to next line to read in possible values
                nextsplit = next.split(" ")
                count = int(nextsplit[3])
                for i in range(count):
                    val = nextsplit[i + 6].replace(",", '')
                    self.nodes[sep[1]].possValues.append(val)
            if sep[0] == "probability":  # start to populate CPD
                cur = self.nodes(sep[2])


if __name__ == "__main__":
    testnet = Network("alarm.bif")
