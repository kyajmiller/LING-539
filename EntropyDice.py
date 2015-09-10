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


# main program
diceSides = 6
diceP_x = makeDiceP_x(diceSides)
print("P_x: %s" % diceP_x)
print("Entropy of %s sided dice: %s bits" % (diceSides, entropy(diceP_x)))
