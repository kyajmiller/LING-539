__author__ = 'Kya'
import math


def entropy(p_x):
    sum = 0
    for px in p_x:
        sum += px * math.log(px, 2)

    return -sum


def makeDiceP_x(numSides):
    dist = [1 / float(numSides)] * numSides
    return dist


def doDiceEntropy(diceSides):
    diceP_x = makeDiceP_x(diceSides)
    print("P_x: %s" % diceP_x)
    print("Entropy of %s sided dice: %s bits" % (diceSides, entropy(diceP_x)))


def doDiceEntropyManual(diceP_x):
    print("P_x: %s Entropy %s" % (diceP_x, entropy(diceP_x)))

# main program
'''
doDiceEntropy(6)
doDiceEntropy(4)
doDiceEntropy(20)
'''

doDiceEntropyManual([0.25, 0.25, 0.25, 0.25])
doDiceEntropyManual([0.4, 0.2, 0.2, 0.2])
doDiceEntropyManual([0.55, 0.15, 0.15, 0.15])
doDiceEntropyManual([0.7, 0.1, 0.1, 0.1])
doDiceEntropyManual([0.85, 0.05, 0.05, 0.05])
doDiceEntropyManual([0.97, 0.01, 0.01, 0.01])
