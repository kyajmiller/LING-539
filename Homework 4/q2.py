"""
Kya Miller
LING 539 Assignment 4
Q2 - Imports a portion of the Penn Treebank as available through nltk and uses the first 90% as training data and the
remaining 10% as testing data. Tests the performance of various nltk taggers using the training and testing data.
"""

from nltk.corpus import treebank
import math

untaggedSentences = treebank.sents()
taggedSentences = treebank.tagged_sents()

totalSentences = len(untaggedSentences)
sizeOfTrainingSet = int(math.ceil(totalSentences * 0.9))
sizeOfTestingSet = int(totalSentences - sizeOfTrainingSet)

trainingSetUntagged = untaggedSentences[:sizeOfTrainingSet]
trainingSetTagged = taggedSentences[:sizeOfTrainingSet]

testingSetUntagged = untaggedSentences[-sizeOfTestingSet:]
testingSetTagged = taggedSentences[-sizeOfTestingSet:]
