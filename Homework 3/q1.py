"""
Kya Miller
LING 539 Assignment 3
Q1 - Reads in sentences from sents_in.txt and returns the probability of each sentence. Uses a bigram model trained on
the browntag corpus and Lidstone smoothing. lambda = 1/100,000. Different from previous models in that it uses actual
conditional probabilities.

To get conditional probability:
p(cat|the) = p(the cat)/p(the)
"""

from __future__ import division
import re
from collections import Counter


def makeFrequencyList(tokensList):
    # uses Counter module to make a frequency dictionary. Takes list of words/pos tokens as argument. Returns list of
    # tokens with their counts in descending order.
    frequencyDict = Counter()
    for token in tokensList:
        frequencyDict[token] += 1

    return frequencyDict.most_common()


def calculateLidstoneSmoothingProb(bigramCount):
    # calculates and returns the probability of a bigram after Lidstone smoothing.
    # lidstone = bigramCount + lambda / numActualBigrams + numPossibleBigrams * lambda

    lamb = 1 / 100000

    lidstone = (bigramCount + lamb) / (totalBigramsCount + (totalPossibleBigrams * lamb))

    return lidstone


def doSentenceProbabilityLidstoneSmoothing(sentenceBigrams):
    # get the probability of the sentence using the conditional probabilities of the bigrams.
    # conditional probability = lidstoneSmoothedProb(bigram) / normalProb(firstUnigram)
    sentenceProb = 1
    for bigram in sentenceBigrams:
        # get those conditional probabilities

        # get probability of first unigram in the bigram
        bigramParts = bigram.split(' ')
        firstPart = bigramParts[0]
        if firstPart in unigramsProbabilitiesDict.iterkeys():
            firstPartProb = unigramsProbabilitiesDict[firstPart]

            # get the lidstone smoothed probability of the bigram
            if bigram in bigramsFrequencyDict.iterkeys():
                bigramFrequencyCount = bigramsFrequencyDict[bigram]
                bigramProb = calculateLidstoneSmoothingProb(bigramFrequencyCount)
            else:
                bigramProb = calculateLidstoneSmoothingProb(0)

            conditionalProb = bigramProb / firstPartProb
            sentenceProb *= conditionalProb

    return sentenceProb


# open browntag_nolines.txt as input
filein = open('browntag_nolines.txt', 'r')
brownTagLineByLine = [line.strip() for line in filein]
filein.close()

# open sents_in.txt as sentence prob input
sentenceFileIn = open('sents_in.txt', 'r')
sentsInData = sentenceFileIn.readlines()
sentenceFileIn.close()

wordsUnigrams = []
wordsBigrams = []

# now read in line by line to get unigrams and sentence specific bigrams
for line in brownTagLineByLine:
    wordsPOSTags = line.split(' ')

    # declare separate lists to generate bigrams and trigrams
    lineWordsUnigramsToMakeBigrams = ['#']

    # go ahead and add word boundary things to the total unigrams list for later prob stuff
    wordsUnigrams.append('#')

    # splits each word_posTag on underscore '_'. Sometimes there are multiple underscores in the token, so will redo the
    # split if find second underscore. Make word lowercase for case stuff. Append word portion to wordsUnigrams.
    for token in wordsPOSTags:
        splitWordPOS = token.split('_', 1)
        if len(splitWordPOS) == 2:
            word = splitWordPOS[0]
            word = word.lower()
            tag = splitWordPOS[1]
            if re.search('_', tag):
                resplit = tag.split('_', 1)
                word = '%s%s' % (word, resplit[0])
                word = word.lower()
                tag = resplit[1]
            wordsUnigrams.append(word)
            lineWordsUnigramsToMakeBigrams.append(word)

    # create bigrams and trigrams using string interpolation and append to appropriate lists
    for i in range(len(lineWordsUnigramsToMakeBigrams) - 1):
        wordsBigrams.append('%s %s' % (lineWordsUnigramsToMakeBigrams[i], lineWordsUnigramsToMakeBigrams[i + 1]))

# make frequency lists using previously declared function
unigramsFrequencyList = makeFrequencyList(wordsUnigrams)
bigramsFrequencyList = makeFrequencyList(wordsBigrams)

# make dictionary of unigram probabilities
totalUnigramsCount = 0
for unigram in unigramsFrequencyList:
    totalUnigramsCount += unigram[1]

unigramsProbabilitiesDict = {unigram[0]: unigram[1] / totalUnigramsCount for unigram in unigramsFrequencyList}

# calculate total possible bigrams for B value
totalUniqueUnigrams = len(unigramsFrequencyList)
totalPossibleBigrams = totalUniqueUnigrams * totalUniqueUnigrams

# calculate the count of seen bigrams for N value
totalBigramsCount = 0
for bigram in bigramsFrequencyList:
    totalBigramsCount += bigram[1]

# create a dictionary for bigram frequency
bigramsFrequencyDict = {bigram[0]: bigram[1] for bigram in bigramsFrequencyList}

# do sentence probabilities
for sentence in sentsInData:
    sentence = sentence.strip()

    sentenceWords = sentence.split(' ')
    sentenceUnigramsToMakeBigrams = ['#']

    for word in sentenceWords:
        sentenceUnigramsToMakeBigrams.append(word)

    sentenceBigrams = ['%s %s' % (sentenceUnigramsToMakeBigrams[i], sentenceUnigramsToMakeBigrams[i + 1]) for i in
                       range(len(sentenceUnigramsToMakeBigrams) - 1)]

    sentenceProb = doSentenceProbabilityLidstoneSmoothing(sentenceBigrams)

    print('Sentence: %s' % sentence)
    print('Probability: %s' % sentenceProb)
