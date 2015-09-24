"""
Kya Miller
LING 539 Assignment 1
Q3B - Calculates the entropy from the sum of the rolls of two 4-sided dice. The dice are unfairly weighted.
I wasn't sure if the problem wanted the separate entropies of each dice added together, or the entropy of the probabilities
of getting each possible sum from the two dice rolls (2-8), so I did both.
"""

from __future__ import division
import math


def calculateEntropy(listOfProbabilities):
    sum = 0
    for probability in listOfProbabilities:
        sum += probability * math.log(probability, 2)

    return -sum


dice1Entropy = calculateEntropy([0.4, 0.2, 0.2, 0.2])
dice2Entropy = calculateEntropy([0.1, 0.1, 0.7, 0.1])
sumEntropy = dice1Entropy + dice2Entropy
print("The sum of the entropies of two unfairly weighted dice: %s" % sumEntropy)

totalSumsEntropy = calculateEntropy([0.04, 0.06, 0.32, 0.22, 0.22, 0.16, 0.02])
print("The entropy of the sums of two unfairly weighted dice: %s" % totalSumsEntropy)
