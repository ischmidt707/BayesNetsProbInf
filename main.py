from Network import *
from VarElim import *
from Gibbs import *


class Main():

    def __init__(self):
        self.result = [] # store tuples of network name, query node name, algorithm name, evidence tag, & resulting marginal distributions for each trial run

    def main(self):
        aNet = Network("alarm.bif")
        a1 = VarElim("HYPOVOLEMIA", [], aNet)
        a1.solve()

        a2 = VarElim("HYPOVOLEMIA", [['HRBP','LOW'],['CO','LOW'],['BP','HIGH']], aNet)


main = Main()
main.main()
