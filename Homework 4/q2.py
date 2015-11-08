"""
Kya Miller
LING 539 Assignment 4
Q2 - Imports a portion of the Penn Treebank as available through nltk and uses the first 90% as training data and the
remaining 10% as testing data. Tests the performance of various nltk taggers using the training and testing data.
"""

from __future__ import division
from nltk.corpus import treebank
import math
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

    accuracy = (matches / totalTags) * 100
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
    regexpTagger = RegexpTagger(regexes)

    regexpTaggedSentences = regexpTagger.tag_sents(untaggedSentences)
    regexpTaggedSentencesPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in regexpTaggedSentences]

    return calculateAccuracy(goldPOSTags, regexpTaggedSentencesPOSTags)


def getUnigramTaggerAccuracy(trainingSet, testingSet):
    testingUntaggedSentences = [[taggedWord[0] for taggedWord in sentence] for sentence in testingSet]
    testingGoldPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in testingSet]

    unigramTagger = UnigramTagger(trainingSet)
    unigramTaggedSentences = unigramTagger.tag_sents(testingUntaggedSentences)
    unigramTaggedSentencesPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in unigramTaggedSentences]

    return calculateAccuracy(testingGoldPOSTags, unigramTaggedSentencesPOSTags)


def getNgramTaggerAccuracy(n, trainingSet, testingSet):
    testingUntaggedSentences = [[taggedWord[0] for taggedWord in sentence] for sentence in testingSet]
    testingGoldPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in testingSet]

    ngramTagger = NgramTagger(n, trainingSet)
    ngramTaggedSentences = ngramTagger.tag_sents(testingUntaggedSentences)
    ngramTaggedSentencesPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in ngramTaggedSentences]

    return calculateAccuracy(testingGoldPOSTags, ngramTaggedSentencesPOSTags)


def calculateAccuracy(goldPOSTags, predictedPOSTags):
    totalTags = 0
    matches = 0

    for i in range(len(goldPOSTags)):
        goldSentencePOSTags = goldPOSTags[i]
        predictedSentencePOSTags = predictedPOSTags[i]
        for j in range(len(goldSentencePOSTags)):
            totalTags += 1
            individualGoldPOSTag = goldSentencePOSTags[j]
            individualPredictedPOSTag = predictedSentencePOSTags[j]
            if individualGoldPOSTag == individualPredictedPOSTag:
                matches += 1

    accuracy = (matches / totalTags) * 100
    return accuracy


# create training and testing sets of tagged sentences
taggedSentences = treebank.tagged_sents()

totalSentences = len(taggedSentences)
sizeOfTrainingSet = int(math.ceil(totalSentences * 0.9))
sizeOfTestingSet = int(totalSentences - sizeOfTrainingSet)

trainingSet = taggedSentences[:sizeOfTrainingSet]
testingSet = taggedSentences[-sizeOfTestingSet:]

# get default tagger accuracy
defaultTaggerAccuracy = getDefaultTaggerAccuracy(testingSet)
defaultFormattedString = 'DefaultTagger\t\t%.2f percent' % defaultTaggerAccuracy

# get regexp tagger accuracy
regexpTaggerAccuracy = getRegexpTaggerAccuracy(testingSet)
regexpFormattedString = 'RegexpTagger\t\t%.2f percent' % regexpTaggerAccuracy

# get unigram tagger accuracy
unigramTaggerAccuracy = getUnigramTaggerAccuracy(trainingSet, testingSet)
unigramFormattedString = 'UnigramTagger\t\t%.2f percent' % unigramTaggerAccuracy

# get ngram tagger accuracy where n = 2
bigramTaggerAccuracy = getNgramTaggerAccuracy(2, trainingSet, testingSet)
bigramFormattedString = 'NgramTagger(n=2)\t%.2f percent' % bigramTaggerAccuracy

# get ngram tagger accuracy where n = 3
trigramTaggerAccuracy = getNgramTaggerAccuracy(3, trainingSet, testingSet)
trigramFormattedString = 'NgramTagger(n=3)\t%.2f percent' % trigramTaggerAccuracy

# print output to console
print('POS Tagger\t\t% Correct on Penn Treebank Test Set')
print(defaultFormattedString)
print(regexpFormattedString)
print(unigramFormattedString)
print(bigramFormattedString)
print(trigramFormattedString)
