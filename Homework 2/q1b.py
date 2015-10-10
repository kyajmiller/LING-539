"""
Kya Miller
LING 539 Assignment 2
Q1B - Reads in sentences from sents_in.txt and prints the probability of that sentence based on three models: unigram
model where unknown words have probability 1.0; bigram model with Laplace smoothing; bigram model with Lidstone
smoothing.
"""

from __future__ import division
from q1a import *


def doSentenceProbabilityUnigramModel(sentence):
    # calculates and returns the probability of the sentence using a unigram model. If a unigram does not appear in the
    # unigramsProbabilitiesDict, it is assigned a probability of 1.0.
    sentenceWords = sentence.split(' ')
    sentenceProb = 1
    unknownWordProb = 1
    for word in sentenceWords:
        if word in unigramsProbabilitiesDict.iterkeys():
            sentenceProb *= unigramsProbabilitiesDict[word]
        else:
            sentenceProb *= unknownWordProb

    return sentenceProb


def doSentenceProbabilityBigramsLaplaceSmoothing(sentence):
    # calculates and returns the probability of the sentence using a bigram model with Laplace smoothing.
    # laplace = frequency(bigram) + 1 / numActualBigrams + numPossibleBigrams.
    sentenceWords = sentence.split(' ')
    sentenceBigrams = ['%s %s' % (sentenceWords[i], sentenceWords[i + 1]) for i in range(len(sentenceWords) - 1)]
    sentenceProb = 1
    laplaceUnknownBigramProb = 1 / (totalSeenBigrams + totalPossibleBigrams)

    for bigram in sentenceBigrams:
        if bigram in bigramsFrequencyDict.iterkeys():
            laplaceBigramProb = (bigramsFrequencyDict[bigram] + 1) / (totalSeenBigrams + totalPossibleBigrams)
            sentenceProb *= laplaceBigramProb
        else:
            sentenceProb *= laplaceUnknownBigramProb

    return sentenceProb


def calculateLidstoneSmoothingProb(bigramCount):
    # calculates and returns the probability of a bigram after Lidstone smoothing.
    # lidstone = bigramCount + alpha / numActualBigrams + numPossibleBigrams * lambda

    # estimations of alpha and lambda, shouldn't be too far from alpha = 0.5 and lambda = 1 / 100000
    # I personally like 1 / 1,000,000 (1e-6) because every smoothing algorith I've done always seems to have the best
    # lambda value as that.
    # I choose lambda = 1 / 10,000,000 (1e-7) which is the smallest lambda value whereafter decreasing the value by an
    # order of magnitude started having diminishing returns. The smaller values do have a slightly higher probability,
    # but barely
    alpha = 0.65
    lamb = 1 / 10000000

    lidstone = (bigramCount + alpha) / (totalSeenBigrams + (totalPossibleBigrams * lamb))

    return lidstone


def doSentenceProbabilityBigramsLidstoneSmoothing(sentence):
    # calculates and returns the probability of the sentence using a bigram model with Lidstone smoothing.
    # lidstone = frequency(bigram) + A / numActualBigrams + numPossibleBigrams * lambda

    sentenceWords = sentence.split(' ')
    sentenceBigrams = ['%s %s' % (sentenceWords[i], sentenceWords[i + 1]) for i in range(len(sentenceWords) - 1)]
    sentenceProb = 1

    for bigram in sentenceBigrams:
        if bigram in bigramsFrequencyDict.iterkeys():
            bigramCount = bigramsFrequencyDict[bigram]
            prob = calculateLidstoneSmoothingProb(bigramCount)
            sentenceProb *= prob
        else:
            prob = calculateLidstoneSmoothingProb(0)
            sentenceProb *= prob

    return sentenceProb

# open sents_in.txt as input for testing
sentsInFile = open('sents_in.txt', 'r')
sentsInData = sentsInFile.readlines()
sentsInFile.close()

# make frequency lists using previously declared function
unigramsFrequencyList = makeFrequencyList(wordsUnigrams)
bigramsFrequencyList = makeFrequencyList(wordsBigrams)

# get total unigrams count
totalUnigrams = 0
for unigram in unigramsFrequencyList:
    totalUnigrams += unigram[1]

# get total seen bigrams count
totalSeenBigrams = 0
for bigram in bigramsFrequencyList:
    totalSeenBigrams += bigram[1]

# calculate total possible bigrams
totalPossibleBigrams = totalSeenBigrams * totalSeenBigrams

# create dictionary of unigrams and their probabilities; do same for bigrams
unigramsProbabilitiesDict = {unigram[0]: unigram[1] / totalUnigrams for unigram in unigramsFrequencyList}

# even though the bigramsFrequencyList works okay, trying to iterate through tuples by value is obnoxious. Easier to
# iterate through dictionary keys.
bigramsFrequencyDict = {bigram[0]: bigram[1] for bigram in bigramsFrequencyList}

# do sentence probabilities
for sentence in sentsInData:
    sentence = sentence.strip()
    unigramsProb = doSentenceProbabilityUnigramModel(sentence)
    laplaceProb = doSentenceProbabilityBigramsLaplaceSmoothing(sentence)
    lidstoneProb = doSentenceProbabilityBigramsLidstoneSmoothing(sentence)

    print "Sentence: %s" % sentence
    print "Probability (Unigrams): %s; Probability (Laplace): %s; Probability (Lidstone): %s" % (
    unigramsProb, laplaceProb, lidstoneProb)
