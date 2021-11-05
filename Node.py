class Node():

    def __init__(self, name):

        self.name = name
        self.possValues = []
        self.value = ""
        self.parents = []
        self.children = []
        self.CPD = {}