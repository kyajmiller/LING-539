"""
Kya Miller
LING 539 Assignment 1
Q3A - Calculates the entropy from the sum of the rolls of two 4-sided dice. Both dice are fairly weighted.
Also includes the entropy of the separate die in a commented section.
"""

from __future__ import division
import math


def calculateEntropy(listOfProbabilities):
    sum = 0
    for probability in listOfProbabilities:
        sum += probability * math.log(probability, 2)

    return -sum


'''
dice1Entropy = calculateEntropy([0.25, 0.25, 0.25, 0.25])
dice2Entropy = calculateEntropy([0.25, 0.25, 0.25, 0.25])
sumEntropy = dice1Entropy + dice2Entropy
print("The sum of the entropies of two fairly weighted dice: %s" % sumEntropy)
'''

totalSumsEntropy = calculateEntropy([1 / 16, 2 / 16, 3 / 16, 4 / 16, 3 / 16, 2 / 16, 1 / 16])
print("The entropy of the sums of two fairly weighted dice: %s" % totalSumsEntropy)
