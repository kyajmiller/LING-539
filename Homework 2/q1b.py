"""
Kya Miller
LING 539 Assignment 2
Q1B - Reads in sentences from sents_in.txt and prints the probability of that sentence based on three models: unigram
model where unknown words have probability 1.0; bigram model with Laplace smoothing; bigram model with Lidstone
smoothing.
"""

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
brownTagNoLines = filein.read()
filein.close()

# tokenize input file on whitespace to get individual words_posTags. Declare words and list to be populated.
wordsPOSTags = brownTagNoLines.split(' ')
wordsUnigrams = []

# splits each word_posTag on underscore '_'. Sometimes there are multiple underscores in the token, so will redo the
# split if find second underscore. Append word part wordsUnigrams.
for token in wordsPOSTags:
    splitWordPOS = token.split('_', 1)
    word = splitWordPOS[0]
    tag = splitWordPOS[1]
    if re.search('_', tag):
        resplit = tag.split('_', 1)
        word = '%s%s' % (word, resplit[0])
        tag = resplit[1]
    wordsUnigrams.append(word)

# create bigrams list using string interpolation
wordsBigrams = ['%s\t%s' % (wordsUnigrams[i], wordsUnigrams[i + 1]) for i in range(len(wordsUnigrams) - 1)]

# make frequency lists using previously declared function
unigramsFrequencyList = makeFrequencyList(wordsUnigrams)
bigramsFrequencyList = makeFrequencyList(wordsBigrams)

# get total unigrams count
totalUnigrams = 0
for unigram in unigramsFrequencyList:
    totalUnigrams += unigram[1]

# get total bigrams count
totalBigrams = 0
for bigram in bigramsFrequencyList:
    totalBigrams += bigram[1]
