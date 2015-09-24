"""
Kya Miller
LING 539 Assignment 1
Q1C - Plots the frequency of untagged words from the browntag corpus versus their word rank, then draws a line of best fit
according to Zipf's Law.
"""

import q1a
import numpy
import matplotlib.pyplot as plt


def plot_points():
    plt.figure(1)
    plt.scatter(rankX, frequencyY)
    plt.xlabel("rank")
    plt.ylabel("frequency")
    plt.xscale('log')
    plt.yscale('log')
    plt.show()


def plotPointsLogAlreadyFigured():
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

# plot_points()
plotPointsLogAlreadyFigured()
