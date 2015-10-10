"""
Kya Miller
LING 539 Assignment 2
Q2 - Finds all of the words from the browntag corpus whose occurences as NN, JJ, or VB is at least 100, then calculates
the entropy of each of those words. Includes a function that prints out these words in order of decreasing entropy,
and shows the unsmoothed count of the associated POS tags.
"""

from __future__ import division
import re
import math
from collections import Counter


def makeWordsTagsSortedFrequencyDict(wordsTagList):
    # uses Counter module to make a frequency dictionary. Takes list of words/pos tokens as argument. Returns dict.
    frequencyDict = Counter()
    for word in wordsTagList:
        frequencyDict[word] += 1

    return frequencyDict


def calculateEntropy(listOfProbabilities):
    # calculates entropy. That's it.
    sum = 0
    for probability in listOfProbabilities:
        sum += probability * math.log(probability, 2)

    return -sum


def calculateWordEntropy(word):
    # calculates word entropy! Gets probabilities of each form of the word, feeds them into calculateEntropy function.
    totalFrequency = wordsMoreThan100FrequencyDict[word]
    wordFreqNN = 0
    wordFreqVB = 0
    wordFreqJJ = 0

    if word in frequencyDictNN:
        wordFreqNN += frequencyDictNN[word]
    else:
        wordFreqNN = 0.01
        totalFrequency += 0.01

    if word in frequencyDictVB:
        wordFreqVB += frequencyDictVB[word]
    else:
        wordFreqVB = 0.01
        totalFrequency += 0.01

    if word in frequencyDictJJ:
        wordFreqJJ += frequencyDictJJ[word]
    else:
        wordFreqJJ = 0.01
        totalFrequency += 0.01

    NNProb = wordFreqNN / totalFrequency
    VBProb = wordFreqVB / totalFrequency
    JJProb = wordFreqJJ / totalFrequency

    entropy = calculateEntropy([NNProb, VBProb, JJProb])
    return entropy


def printOutputTable():
    # prints the output. It's not really a table. Formatted with tabs.
    for word in sortedWordEntropyList:
        wordFreqNN = 0
        wordFreqVB = 0
        wordFreqJJ = 0
        actualWord = word[0]
        entropy = word[1]

        if actualWord in frequencyDictNN:
            wordFreqNN += frequencyDictNN[actualWord]
        if actualWord in frequencyDictVB:
            wordFreqVB += frequencyDictVB[actualWord]
        if actualWord in frequencyDictJJ:
            wordFreqJJ += frequencyDictJJ[actualWord]

        formattedString = '%s\tEntropy: %s\tNN: %s\tVB: %s\tJJ: %s\n' % (
            actualWord, entropy, wordFreqNN, wordFreqVB, wordFreqJJ)
        outputFile.write(formattedString)


# open browntag_nolines to get data
filein = open('browntag_nolines.txt', 'r')
brownTagNoLines = filein.read()
filein.close()

# open output file because why not
outputFile = open('zeroentropy.txt', 'w')

# get counts for words that appear either as NN, VB, or JJ
print("Getting word POS counts...")
wordsPOSTags = brownTagNoLines.split(' ')
wordsNNTag = []
wordsVBTag = []
wordsJJTag = []
allWords = []

for token in wordsPOSTags:
    # split token into word/tag
    splitWordPOS = token.split('_', 1)
    if len(splitWordPOS) == 2:
        word = splitWordPOS[0]
        tag = splitWordPOS[1]
        if re.search('_', tag):
            # redo the split in case of wonky ones
            resplit = tag.split('_', 1)
            word = '%s%s' % (word, resplit[0])
            tag = resplit[1]

        # put words in appropriate lists
        allWords.append(word)
        if tag == 'NN':
            wordsNNTag.append(word)
        elif tag == 'VB':
            wordsVBTag.append(word)
        elif tag == 'JJ':
            wordsJJTag.append(word)

# distinct word list
distinctWords = list(set(allWords))

# make frequency dictionaries for each relevant POS tag, contains word : count for that tag
print('Creating frequency dictionaries...')
frequencyDictNN = makeWordsTagsSortedFrequencyDict(wordsNNTag)
frequencyDictVB = makeWordsTagsSortedFrequencyDict(wordsVBTag)
frequencyDictJJ = makeWordsTagsSortedFrequencyDict(wordsJJTag)

# make frequency dict for words that appear more than total in the previous lists
print('Getting words that appear more than 100 times...')
wordsMoreThan100FrequencyDict = Counter()

for word in distinctWords:
    wordTotalFrequency = 0
    # check to see if word in POS frequency dictionaries, append count
    if word in frequencyDictNN.iterkeys():
        wordTotalFrequency += frequencyDictNN[word]
    if word in frequencyDictVB.iterkeys():
        wordTotalFrequency += frequencyDictVB[word]
    if word in frequencyDictJJ.iterkeys():
        wordTotalFrequency += frequencyDictJJ[word]

    if wordTotalFrequency >= 100:
        # only add words with more than 100... yeah
        wordsMoreThan100FrequencyDict[word] = wordTotalFrequency

wordsMoreThan100FrequencySortedList = wordsMoreThan100FrequencyDict.most_common()

# calculate entropies now, like the print says
print('Calculating word entropies...')

# dictionary of word : entropy
wordEntropyDict = Counter()
for word in wordsMoreThan100FrequencySortedList:
    # actually get the entropy
    wordOnly = word[0]
    entropy = calculateWordEntropy(wordOnly)
    wordEntropyDict[wordOnly] = entropy

# sort the word : entropy in descending order
sortedWordEntropyList = wordEntropyDict.most_common()

# print thangs to ouput file
print('Preparing to print output...')
printOutputTable()

outputFile.close()
