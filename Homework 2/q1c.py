"""
Kya Miller
LING 539 Assignment 2
Q1C - Prints a log/log graph of Zipf's law for unsmoothed bigrams and smoothed bigrams using the Lidstone smoothign from
q1b.py.
"""

from q1a import *
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


bigramsFrequencySortedList = makeBigramsSortedList()
plotUnsmoothedZipfsLogLog()
