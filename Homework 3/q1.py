"""
Kya Miller
LING 539 Assignment 3
Q1 - Reads in sentences from sents_in.txt and returns the probability of each sentence. Uses a bigram model trained on
the browntag corpus and Lidstone smoothing. lambda = 1/100,000. Different from previous models in that it uses actual
conditional probabilities.

To get conditional probability:
p(cat|the) = p(the cat)/p(the)
"""

from __future__ import division
import re
from collections import Counter


def makeFrequencyList(tokensList):
    # uses Counter module to make a frequency dictionary. Takes list of words/pos tokens as argument. Returns list of
    # tokens with their counts in descending order.
    frequencyDict = Counter()
    for token in tokensList:
        frequencyDict[token] += 1

    return frequencyDict.most_common()


# open browntag_nolines.txt as input
filein = open('browntag_nolines.txt', 'r')
brownTagLineByLine = [line.strip() for line in filein]
filein.close()

wordsUnigrams = []
wordsBigrams = []

# now read in line by line to get unigrams and sentence specific bigrams
for line in brownTagLineByLine:
    wordsPOSTags = line.split(' ')

    # declare separate lists to generate bigrams and trigrams
    lineWordsUnigramsToMakeBigrams = ['#']

    # splits each word_posTag on underscore '_'. Sometimes there are multiple underscores in the token, so will redo the
    # split if find second underscore. Append word portion to wordsUnigrams.
    for token in wordsPOSTags:
        splitWordPOS = token.split('_', 1)
        if len(splitWordPOS) == 2:
            word = splitWordPOS[0]
            tag = splitWordPOS[1]
            if re.search('_', tag):
                resplit = tag.split('_', 1)
                word = '%s%s' % (word, resplit[0])
                tag = resplit[1]
            wordsUnigrams.append(word)
            lineWordsUnigramsToMakeBigrams.append(word)

    # append appropriate number of # to bigrams and trigrams lists
    lineWordsUnigramsToMakeBigrams.append('#')

    # create bigrams and trigrams using string interpolation and append to appropriate lists
    for i in range(len(lineWordsUnigramsToMakeBigrams) - 1):
        wordsBigrams.append('%s\t%s' % (lineWordsUnigramsToMakeBigrams[i], lineWordsUnigramsToMakeBigrams[i + 1]))

# make frequency lists using previously declared function
unigramsFrequencyList = makeFrequencyList(wordsUnigrams)
bigramsFrequencyList = makeFrequencyList(wordsBigrams)
