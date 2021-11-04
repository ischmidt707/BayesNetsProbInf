from Node import *

class Network():

    def __init__(self, filename):
        self.nodes = {}
        self.factors = {}
        self.name = filename
        self.loadBNet(filename)

    def loadBNet(self, filename):
        pass