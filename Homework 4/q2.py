"""
Kya Miller
LING 539 Assignment 4
Q2 - Imports a portion of the Penn Treebank as available through nltk and uses the first 90% as training data and the
remaining 10% as testing data. Tests the performance of various nltk taggers using the training and testing data.
"""

from __future__ import division
from nltk.corpus import treebank
import math
import nltk
from nltk.tag import DefaultTagger
from nltk.tag import RegexpTagger
from nltk.tag import UnigramTagger
from nltk.tag import NgramTagger


def useDefaultTagger(testingSet):
    untaggedSentences = [[taggedWord[0] for taggedWord in sentence] for sentence in testingSet]
    goldPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in testingSet]

    defaultTagger = DefaultTagger('NN')
    defaultTaggedSentences = defaultTagger.tag_sents(untaggedSentences)

    totalTags = 0
    matches = 0
    for sentencePOSTags in goldPOSTags:
        for individualPOSTag in sentencePOSTags:
            totalTags += 1
            if individualPOSTag == 'NN':
                matches += 1

    accuracy = matches / totalTags
    return accuracy



untaggedSentences = treebank.sents()
taggedSentences = treebank.tagged_sents()

totalSentences = len(untaggedSentences)
sizeOfTrainingSet = int(math.ceil(totalSentences * 0.9))
sizeOfTestingSet = int(totalSentences - sizeOfTrainingSet)

trainingSetUntagged = untaggedSentences[:sizeOfTrainingSet]
trainingSetTagged = taggedSentences[:sizeOfTrainingSet]

testingSetUntagged = untaggedSentences[-sizeOfTestingSet:]
testingSetTagged = taggedSentences[-sizeOfTestingSet:]

useDefaultTagger(testingSetTagged)
