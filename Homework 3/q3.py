"""
Kya Miller
LING 539 Assignment 3
Q3 - Finds percentage of words which have multiple POS tags in the browntag corpus. Then, given a training/testing split
percentage, the program learns the most likely POS tag for a given word and then calculates the percentage of words and
sentences correctly tagged in the testing set.
"""

import re
from collections import Counter

# open browntag_nolines.txt as input
filein = open('browntag_nolines.txt', 'r')
brownTagLineByLine = [line.strip() for line in filein]
filein.close()

wordsUnigrams = []
posTagsUnigrams = []

wordsNumTagsDict = Counter()

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
            wordsUnigrams.append(word)
            posTagsUnigrams.append(tag)
