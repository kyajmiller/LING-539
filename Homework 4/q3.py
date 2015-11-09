"""
Kya Miller
LING 539 Assignment 4
Q3 - Evaluates the performance of nltk's HiddenMarkovModelTagger. Imports a portion of the Penn Treebank as available
through nltk and uses the last 10% as testing data with various sized portions of the remaining corpus as training data.
"""

from __future__ import division
from nltk.corpus import treebank
from nltk.tag import HiddenMarkovModelTrainer
import math
import matplotlib.pyplot as plt


def trainAndTestHiddenMarkovModelTagger(trainingSetPercentage):
    trainingSet = createTrainingSet(trainingSetPercentage)
    testingUntaggedSentences = [[taggedWord[0] for taggedWord in sentence] for sentence in testingSet]
    testingGoldPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in testingSet]

    hmmTrainer = HiddenMarkovModelTrainer()
    trainedHMMTagger = hmmTrainer.train_supervised(trainingSet)

    hmmPredictedPaths = [trainedHMMTagger.best_path(sentence) for sentence in testingUntaggedSentences]

    return calculateAccuracy(testingGoldPOSTags, hmmPredictedPaths)


def calculateAccuracy(goldPOSTags, predictedPOSTags):
    # calculates the total percentage of matches between the gold and predicted POS tags
    totalTags = 0
    matches = 0

    # iterate through each sentence
    for i in range(len(goldPOSTags)):
        goldSentencePOSTags = goldPOSTags[i]
        predictedSentencePOSTags = predictedPOSTags[i]
        # iterate through each tag
        for j in range(len(goldSentencePOSTags)):
            totalTags += 1
            individualGoldPOSTag = goldSentencePOSTags[j]
            individualPredictedPOSTag = predictedSentencePOSTags[j]
            if individualGoldPOSTag == individualPredictedPOSTag:
                matches += 1

    accuracy = (matches / totalTags) * 100
    return accuracy


def createTrainingSet(percentage):
    sizeOfTrainingSet = int(math.ceil(totalSentences * percentage))
    trainingSet = taggedSentences[:sizeOfTrainingSet]
    return trainingSet


def plotPerformanceVsTrainingSize():
    x = [1, 2, 3, 4, 5, 10, 25, 50, 75, 90]
    y = [hmmAccuracy1, hmmAccuracy2, hmmAccuracy3, hmmAccuracy4, hmmAccuracy5, hmmAccuracy10, hmmAccuracy25,
         hmmAccuracy50, hmmAccuracy75, hmmAccuracy90]
    plt.scatter(x, y)
    plt.show()


# create testing set from last 10% of tagged sentences
taggedSentences = treebank.tagged_sents()

totalSentences = len(taggedSentences)
sizeOfTestingSet = int(math.ceil(totalSentences * 0.1))
testingSet = taggedSentences[-sizeOfTestingSet:]

# get accuracy of HMM tagger given training sets of various sizes
hmmAccuracy1 = trainAndTestHiddenMarkovModelTagger(0.01)
hmmAccuracy2 = trainAndTestHiddenMarkovModelTagger(0.02)
hmmAccuracy3 = trainAndTestHiddenMarkovModelTagger(0.03)
hmmAccuracy4 = trainAndTestHiddenMarkovModelTagger(0.04)
hmmAccuracy5 = trainAndTestHiddenMarkovModelTagger(0.05)
hmmAccuracy10 = trainAndTestHiddenMarkovModelTagger(0.10)
hmmAccuracy25 = trainAndTestHiddenMarkovModelTagger(0.25)
hmmAccuracy50 = trainAndTestHiddenMarkovModelTagger(0.50)
hmmAccuracy75 = trainAndTestHiddenMarkovModelTagger(0.75)
hmmAccuracy90 = trainAndTestHiddenMarkovModelTagger(0.90)

plotPerformanceVsTrainingSize()
