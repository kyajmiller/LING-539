"""
Kya Miller
LING 539 Assignment 2
Q1C - Prints a log/log graph of Zipf's law for unsmoothed bigrams and smoothed bigrams using the Lidstone smoothign from
q1b.py. This imports both q1a.py and q1b.py.
"""

from q1a import *
from q1b import *
import numpy
import matplotlib.pyplot as plt


def plotUnsmoothedZipfsLogLog():
    rankX = [i + 1 for i in range(len(bigramsFrequencySortedList))]
    frequencyY = [bigramsFrequencySortedList[i][1] for i in range(len(bigramsFrequencySortedList))]

    logX = [numpy.log10(x) for x in rankX]
    logY = [numpy.log10(y) for y in frequencyY]

    plt.figure()
    plt.scatter(logX, logY)
    plt.plot(logX, logY, 'r')
    plt.xlabel('rank')
    plt.ylabel('frequency')
    plt.title('Log/Log Graph Unsmoothed Bigrams')
    plt.show()


# get the bigrams count from q1a.py; reads in the browntag corpus, gets the bigrams, and uses the Counter module to
# create a dictionary of the counts; uses makeFrequencyList function to return a list of the counts in descending order
bigramsFrequencySortedList = makeFrequencyList(wordsBigrams)

# calculate how many unseen bigrams there are
unseenBigramsCount = totalPossibleBigrams - totalSeenBigrams

# each unseen bigram has a count of 0.65, the same as the alpha value from q1b.py Lidstone model.
unseenBigramCount = 0.65

# get the rank of the first and last unseen bigrams
unseenBigramRankFirst = totalSeenBigrams + 1
unseenBigramsRankLast = totalPossibleBigrams


plotUnsmoothedZipfsLogLog()
