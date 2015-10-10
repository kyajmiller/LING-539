"""
Kya Miller
LING 539 Assignment 2
Q1C - Prints a log/log graph of Zipf's law for unsmoothed bigrams and smoothed bigrams using the Lidstone smoothign from
q1b.py. This imports both q1a.py and q1b.py.
"""

import re
import numpy
import matplotlib.pyplot as plt
from collections import Counter


def getBigramsList():
    # open browntag_nolines.txt as input
    filein = open('browntag_nolines.txt', 'r')
    brownTagLineByLine = [line.strip() for line in filein]
    filein.close()

    wordsUnigrams = []
    wordsBigrams = []

    # now read in line by line to get unigrams and sentence specific bigrams + trigrams
    for line in brownTagLineByLine:
        wordsPOSTags = line.split(' ')

        # declare separate lists to generate bigrams and trigrams
        lineWordsUnigramsToMakeBigrams = ['#']

        # splits each word_posTag on underscore '_'. Sometimes there are multiple underscores in the token, so will redo the
        # split if find second underscore.
        for token in wordsPOSTags:
            splitWordPOS = token.split('_', 1)
            if len(splitWordPOS) == 2:
                word = splitWordPOS[0]
                tag = splitWordPOS[1]
                if re.search('_', tag):
                    resplit = tag.split('_', 1)
                    word = '%s%s' % (word, resplit[0])
                    tag = resplit[1]
                wordsUnigrams.append(word)
                lineWordsUnigramsToMakeBigrams.append(word)

        # append appropriate number of # to bigrams and trigrams lists
        lineWordsUnigramsToMakeBigrams.append('#')

        # create bigrams and trigrams using string interpolation and append to appropriate lists
        for i in range(len(lineWordsUnigramsToMakeBigrams) - 1):
            wordsBigrams.append('%s\t%s' % (lineWordsUnigramsToMakeBigrams[i], lineWordsUnigramsToMakeBigrams[i + 1]))

    return wordsBigrams


def makeBigramsFrequencyList(wordsBigrams):
    bigramsFrequencyDict = Counter()
    for bigram in wordsBigrams:
        bigramsFrequencyDict[bigram] += 1

    return bigramsFrequencyDict.most_common()


def plotUnsmoothedZipfsLogLog():
    rankX = [i + 1 for i in range(len(bigramsFrequencySortedList))]
    frequencyYUnsmoothed = [bigramsFrequencySortedList[i][1] for i in range(len(bigramsFrequencySortedList))]

    logX = [numpy.log10(x) for x in rankX]
    logY = [numpy.log10(y) for y in frequencyYUnsmoothed]

    plt.figure()
    plt.plot(logX, logY, 'r')
    plt.xlabel('rank')
    plt.ylabel('frequency')
    plt.title('Log/Log Graph Unsmoothed Bigrams')


def plotLidstoneSmoothedZipfsLogLog():
    rankX = [i + 1 for i in range(len(bigramsFrequencySortedList))]
    frequencyYSmoothed = [bigramsFrequencySortedList[i][1] + alpha for i in range(len(bigramsFrequencySortedList))]

    # add data for the first and last ranked unseen bigram
    rankX.append(unseenBigramRankFirst)
    rankX.append(unseenBigramsRankLast)
    frequencyYSmoothed.append(unseenBigramFrequency)
    frequencyYSmoothed.append(unseenBigramFrequency)

    logX = [numpy.log10(x) for x in rankX]
    logY = [numpy.log10(y) for y in frequencyYSmoothed]

    plt.figure()
    plt.plot(logX, logY, 'r')
    plt.xlabel('rank')
    plt.ylabel('frequency')
    plt.title('Log/Log Graph Lidstone Smoothed Bigrams')


# get the bigrams; reads in the browntag corpus, gets the bigrams, and uses the Counter module to
# create a dictionary of the counts; uses makeBigramsFrequencyList function to return a list of the counts in descending order
bigramsFrequencySortedList = makeBigramsFrequencyList(getBigramsList())

# get total seen bigrams count
totalSeenBigrams = 0
for bigram in bigramsFrequencySortedList:
    totalSeenBigrams += bigram[1]

# calculate total possible bigrams
totalPossibleBigrams = totalSeenBigrams * totalSeenBigrams

# calculate how many unseen bigrams there are
totalUnseenBigrams = totalPossibleBigrams - totalSeenBigrams

# each unseen bigram has a count of 0.65, the same as the alpha value from q1b.py Lidstone model.
alpha = 0.65
unseenBigramFrequency = alpha

# get the rank of the first and last unseen bigrams
unseenBigramRankFirst = totalSeenBigrams + 1
unseenBigramsRankLast = totalPossibleBigrams

plotUnsmoothedZipfsLogLog()
plotLidstoneSmoothedZipfsLogLog()
plt.show()
