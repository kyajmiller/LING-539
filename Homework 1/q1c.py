"""
Kya Miller
LING 539 Assignment 1
Q1C - Plots the frequency of untagged words from the browntag corpus versus their word rank, then draws a line of best fit.
Attempts to figure out the constant of Zipf's Law from log values of frequency and rank.
"""

import q1a
import numpy
import matplotlib.pyplot as plt


def estimateZipfsLawConstantFromLogValues():
    total = 0
    numItems = len(logY)

    for i in range(len(logY)):
        frequency = logY[i]
        rank = logX[i]
        product = frequency * rank
        total += product

    constant = total / numItems
    print("Estimated Zipf's Law Constant: %s" % constant)
    return None


def plotPointsAndLineOfBestFit():
    plt.scatter(logX, logY)
    plt.plot(logX, numpy.poly1d(numpy.polyfit(logX, logY, 1))(logX), 'r')
    plt.xlabel('rank')
    plt.ylabel('frequency')
    plt.show()

wordsFrequencySortedList = q1a.makeWordsSortedList()

rankX = [i + 1 for i in range(len(wordsFrequencySortedList))]
frequencyY = [wordsFrequencySortedList[i][1] for i in range(len(wordsFrequencySortedList))]

logX = [numpy.log10(x) for x in rankX]
logY = [numpy.log10(y) for y in frequencyY]

plotPointsAndLineOfBestFit()
estimateZipfsLawConstantFromLogValues()
