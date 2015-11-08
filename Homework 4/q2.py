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


def getDefaultTaggerAccuracy(testingSet):
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


def getRegexpTaggerAccuracy(testingSet):
    untaggedSentences = [[taggedWord[0] for taggedWord in sentence] for sentence in testingSet]
    goldPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in testingSet]

    # regular expressions adopted from nltk RegexepTagger documentation
    regexes = [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),  # cardinal numbers
               (r'(The|the|A|a|An|an)$', 'AT'),  # articles
               (r'.*able$', 'JJ'),  # adjectives
               (r'.*ness$', 'NN'),  # nouns formed from adjectives
               (r'.*ly$', 'RB'),  # adverbs
               (r'.*s$', 'NNS'),  # plural nouns
               (r'.*ing$', 'VBG'),  # gerunds
               (r'.*ed$', 'VBD'),  # past tense verbs
               (r'.*', 'NN')  # nouns (default)
               ]
    regexpTagger = RegexpTagger()

# create training and testing sets of tagged sentences
taggedSentences = treebank.tagged_sents()

totalSentences = len(taggedSentences)
sizeOfTrainingSet = int(math.ceil(totalSentences * 0.9))
sizeOfTestingSet = int(totalSentences - sizeOfTrainingSet)

trainingSet = taggedSentences[:sizeOfTrainingSet]

testingSet = taggedSentences[-sizeOfTestingSet:]

# get default tagger accuracy
defaultTaggerAccuracy = getDefaultTaggerAccuracy(testingSet)
