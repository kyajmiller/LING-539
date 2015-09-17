"""
Kya Miller
LING 539 Assignment 1
Q1B - Reading in sentences from sents_in.txt, prints to console the probabilities of those sentences given the word
probabilities from the browntag corpus
"""

from __future__ import division
import q1a

sentsInFile = open('sents_in.txt', 'r')
sentsInData = sentsInFile.readlines()
sentsInData = [sentence.strip() for sentence in sentsInData]

wordsFrequencySortedList = q1a.makeWordsSortedList()

totalWords = 0
for word in wordsFrequencySortedList:
    totalWords += word[1]

wordsProbabilities = [(word[0], word[1] / totalWords) for word in wordsFrequencySortedList]
