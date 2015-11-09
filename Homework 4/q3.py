"""
Kya Miller
LING 539 Assignment 4
Q3 - Evaluates the performance of nltk's HiddenMarkovModelTagger. Imports a portion of the Penn Treebank as available
through nltk and uses the last 10% as testing data with various sized portions of the remaining corpus as training data.
"""

from __future__ import division
from nltk.corpus import treebank
from nltk.tag import HiddenMarkovModelTagger
from nltk.tag import HiddenMarkovModelTrainer
import math


def trainAndTestHiddenMarkovModelTagger(trainingSet):



def createTrainingSet(percentage):
    sizeOfTrainingSet = int(math.ceil(totalSentences * percentage))
    trainingSet = taggedSentences[:sizeOfTrainingSet]
    return trainingSet


# create testing set from last 10% of tagged sentences
taggedSentences = treebank.tagged_sents()

totalSentences = len(taggedSentences)
sizeOfTestingSet = int(math.ceil(totalSentences * 0.1))
testingSet = taggedSentences[-sizeOfTestingSet:]

# create training sets of various sizes
trainingSet1 = createTrainingSet(0.01)
trainingSet2 = createTrainingSet(0.02)
trainingSet3 = createTrainingSet(0.03)
trainingSet4 = createTrainingSet(0.04)
trainingSet5 = createTrainingSet(0.05)
trainingSet10 = createTrainingSet(0.10)
trainingSet25 = createTrainingSet(0.25)
trainingSet50 = createTrainingSet(0.50)
trainingSet75 = createTrainingSet(0.75)
trainingSet90 = createTrainingSet(0.90)
