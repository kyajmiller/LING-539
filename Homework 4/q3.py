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
    plt.xlabel("training percentage")
    plt.ylabel("performance - % correct")
    plt.title("Performance Vs Training Data Size for HMM Tagger")
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

# print output to console
print("Training Percentage\tPercentage Tagged Correctly")
print("1 percent\t\t\t%.2f" % hmmAccuracy1)
print("2 percent\t\t\t%.2f" % hmmAccuracy2)
print("3 percent\t\t\t%.2f" % hmmAccuracy3)
print("4 percent\t\t\t%.2f" % hmmAccuracy4)
print("5 percent\t\t\t%.2f" % hmmAccuracy5)
print("10 percent\t\t\t%.2f" % hmmAccuracy10)
print("25 percent\t\t\t%.2f" % hmmAccuracy25)
print("50 percent\t\t\t%.2f" % hmmAccuracy50)
print("75 percent\t\t\t%.2f" % hmmAccuracy75)
print("90 percent\t\t\t%.2f" % hmmAccuracy90)

# print output in graph form
plotPerformanceVsTrainingSize()
