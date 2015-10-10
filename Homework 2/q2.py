"""
Kya Miller
LING 539 Assignment 2
Q2 - Finds all of the words from the browntag corpus whose occurences as NN, JJ, or VB is at least 100, then calculates
the entropy of each of those words. Includes a function that prints out these words in order of decreasing entropy,
and shows the unsmoothed count of the associated POS tags.
"""
import re

filein = open('browntag_nolines.txt', 'r')
brownTagNoLines = filein.read()
filein.close()

wordsPOSTags = brownTagNoLines.split(' ')
wordsNNTag = []
wordsVBTag = []
wordsJJTag = []
allWords = []

for token in wordsPOSTags:
    splitWordPOS = token.split('_', 1)
    if len(splitWordPOS) == 2:
        word = splitWordPOS[0]
        tag = splitWordPOS[1]
        if re.search('_', tag):
            resplit = tag.split('_', 1)
            word = '%s%s' % (word, resplit[0])
            tag = resplit[1]

        allWords.append(word)
        if tag == 'NN':
            wordsNNTag.append(word)
        elif tag == 'VB':
            wordsVBTag.append(word)
        elif tag == 'JJ':
            wordsJJTag.append(word)
