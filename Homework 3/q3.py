"""
Kya Miller
LING 539 Assignment 3
Q3 - Finds percentage of words which have multiple POS tags in the browntag corpus. Then, given a training/testing split
percentage, the program learns the most likely POS tag for a given word and then calculates the percentage of words and
sentences correctly tagged in the testing set.
"""

from __future__ import division
import re
from collections import Counter

# open browntag_nolines.txt as input
filein = open('browntag_nolines.txt', 'r')
brownTagLineByLine = [line.strip() for line in filein]
filein.close()

# first just read in browntag stuff and get unique words and unigrams in a list
wordsUnigrams = []
posTagsUnigrams = []

wordFrequencyDict = Counter()

# get unique words and unigrams, establish words dictionary
for line in brownTagLineByLine:
    wordsPOSTags = line.split(' ')

    for token in wordsPOSTags:
        splitWordPOS = token.split('_', 1)
        if len(splitWordPOS) == 2:
            word = splitWordPOS[0]
            tag = splitWordPOS[1]
            if re.search('_', tag):
                resplit = tag.split('_', 1)
                word = '%s%s' % (word, resplit[0])
                word = word.lower()
                tag = resplit[1]
            wordFrequencyDict[word] += 1
            if word not in wordsUnigrams:
                wordsUnigrams.append(word)
            if tag not in posTagsUnigrams:
                posTagsUnigrams.append(tag)

# now that we have the dictionary of words, clear out the entries to make room for lists of POS tags
wordsPOSTagsDict = wordFrequencyDict[:]
for word in wordsPOSTagsDict:
    wordsPOSTagsDict[word] = []

# then cycle back through the browntag stuff and populate the dictionary with lists of pos tags
for line in brownTagLineByLine:
    wordsPOSTags = line.split(' ')

    for token in wordsPOSTags:
        splitWordPOS = token.split('_', 1)
        if len(splitWordPOS) == 2:
            word = splitWordPOS[0]
            tag = splitWordPOS[1]
            if re.search('_', tag):
                resplit = tag.split('_', 1)
                word = '%s%s' % (word, resplit[0])
                word = word.lower()
                tag = resplit[1]
            if tag not in wordFrequencyDict[word]:
                wordsPOSTagsDict[word].append(tag)

wordsMoreThanOnePOS = 0
for word in wordsPOSTagsDict:
    if len(wordsPOSTagsDict[word]) > 1:
        wordsMoreThanOnePOS += 1

percentWordsMoreThanOnePOS = (wordsMoreThanOnePOS / len(wordsUnigrams)) * 100
print(len(wordsUnigrams))
print(wordsMoreThanOnePOS)
