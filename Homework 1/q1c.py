"""
Kya Miller
LING 539 Assignment 1
Q1C - Plots the frequency of untagged words from the browntag corpus versus their word rank, then draws a line of best fit
according to Zipf's Law.
"""

import q1a
import matplotlib.pyplot as plt
import math

'''
-plot points by putting in the rank by the distribution
xscale('log')
yscale('log')
pyplot.scatter
makes line by .plot
'''


def plot_points():
    plt.figure(1)
    plt.scatter(rankX, frequencyY)
    plt.xlabel("rank")
    plt.ylabel("frequency")
    plt.xscale('log')
    plt.yscale('log')
    plt.show()


def plot_line():
    plt.figure(2)
    plt.plot(rankX, frequencyY, 'r')
    plt.xlabel('rank')
    plt.ylabel('frequency')
    plt.xscale('log')
    plt.yscale('log')
    plt.show()


wordsFrequencySortedList = q1a.makeWordsSortedList()
rankByFrequency = [[i + 1, wordsFrequencySortedList[i][1]] for i in range(len(wordsFrequencySortedList))]

rankX = [rank for rank, frequency in rankByFrequency]
frequencyY = [frequency for rank, frequency in rankByFrequency]

plot_points()
plot_line()
