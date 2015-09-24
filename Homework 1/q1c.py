"""
Kya Miller
LING 539 Assignment 1
Q1C - Plots the frequency of untagged words from the browntag corpus versus their word rank, then draws a line of best fit
according to Zipf's Law.
"""

import q1a
import matplotlib.pyplot as plt

'''
-plot points by putting in the rank by the distribution
xscale('log')
yscale('log')
pyplot.scatter
makes line by .plot
'''

wordsFrequencySortedList = q1a.makeWordsSortedList()
rankByFrequency = [[i + 1, wordsFrequencySortedList[i][1]] for i in range(len(wordsFrequencySortedList))]

rankX = [rank for rank, frequency in rankByFrequency]
frequencyY = [frequency for rank, frequency in rankByFrequency]

print(rankX[:10])
print(frequencyY[:10])
