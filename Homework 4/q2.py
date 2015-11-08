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
    # gets the accuracy of the DefaultTagger

    # get untagged sentences and gold POS tags
    untaggedSentences = [[taggedWord[0] for taggedWord in sentence] for sentence in testingSet]
    goldPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in testingSet]

    # declare tagger; honestly this is unncessary, as every tag is going to be 'NN' so we could really just skip this
    # altogether
    # I went with NN as it was the default value shown in the ntlk DefaultTagger documentation, completely arbitrary
    defaultTagger = DefaultTagger('NN')
    defaultTaggedSentences = defaultTagger.tag_sents(untaggedSentences)

    # calculate accuracy
    totalTags = 0
    matches = 0
    # iterate through sentences
    for sentencePOSTags in goldPOSTags:
        # iterate through tags
        for individualPOSTag in sentencePOSTags:
            totalTags += 1
            # if the gold tag is NN, then match
            if individualPOSTag == 'NN':
                matches += 1

    accuracy = (matches / totalTags) * 100
    return accuracy


def getRegexpTaggerAccuracy(testingSet):
    # gets the accuracy of the RegexpTagger

    # get untagged sentences and gold POS tags
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

    # declare tagger
    regexpTagger = RegexpTagger(regexes)

    # test tagger and get predicted POS tags
    regexpTaggedSentences = regexpTagger.tag_sents(untaggedSentences)
    regexpTaggedSentencesPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in regexpTaggedSentences]

    # calculate and return accuracy
    return calculateAccuracy(goldPOSTags, regexpTaggedSentencesPOSTags)


def getUnigramTaggerAccuracy(trainingSet, testingSet):
    # trains and returns the accuracy of the UnigramTagger

    # get untagged sentences and gold POS tags
    testingUntaggedSentences = [[taggedWord[0] for taggedWord in sentence] for sentence in testingSet]
    testingGoldPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in testingSet]

    # train tagger
    unigramTagger = UnigramTagger(trainingSet)

    # test tagger and get predicted POS tags
    unigramTaggedSentences = unigramTagger.tag_sents(testingUntaggedSentences)
    unigramTaggedSentencesPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in unigramTaggedSentences]

    # calculate and return accuracy
    return calculateAccuracy(testingGoldPOSTags, unigramTaggedSentencesPOSTags)


def getNgramTaggerAccuracy(n, trainingSet, testingSet):
    # trains and returns the accuracy of the NgramTagger given a value of n

    # get untagged sentences and gold POS tags
    testingUntaggedSentences = [[taggedWord[0] for taggedWord in sentence] for sentence in testingSet]
    testingGoldPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in testingSet]

    # train tagger
    ngramTagger = NgramTagger(n, trainingSet)

    # test tagger and get predicted POS tags
    ngramTaggedSentences = ngramTagger.tag_sents(testingUntaggedSentences)
    ngramTaggedSentencesPOSTags = [[taggedWord[1] for taggedWord in sentence] for sentence in ngramTaggedSentences]

    # calculate and return accuracy
    return calculateAccuracy(testingGoldPOSTags, ngramTaggedSentencesPOSTags)


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
print('POS Tagger\t\t\t% Correct on Penn Treebank Test Set')
print(defaultFormattedString)
print(regexpFormattedString)
print(unigramFormattedString)
print(bigramFormattedString)
print(trigramFormattedString)
