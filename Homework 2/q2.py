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
    frequencyDict = Counter()
    for word in wordsTagList:
        frequencyDict[word] += 1

    return frequencyDict


def calculateEntropy(listOfProbabilities):
    sum = 0
    for probability in listOfProbabilities:
        sum += probability * math.log(probability, 2)

    return -sum


def calculateWordEntropy(word):
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

filein = open('browntag_nolines.txt', 'r')
brownTagNoLines = filein.read()
filein.close()

outputFile = open('zeroentropy.txt', 'w')

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

distinctWords = list(set(allWords))

frequencyDictNN = makeWordsTagsSortedFrequencyDict(wordsNNTag)
frequencyDictVB = makeWordsTagsSortedFrequencyDict(wordsVBTag)
frequencyDictJJ = makeWordsTagsSortedFrequencyDict(wordsJJTag)

wordsMoreThan100FrequencyDict = Counter()

for word in distinctWords:
    wordTotalFrequency = 0
    if word in frequencyDictNN.iterkeys():
        wordTotalFrequency += frequencyDictNN[word]
    if word in frequencyDictVB.iterkeys():
        wordTotalFrequency += frequencyDictVB[word]
    if word in frequencyDictJJ.iterkeys():
        wordTotalFrequency += frequencyDictJJ[word]

    if wordTotalFrequency >= 100:
        wordsMoreThan100FrequencyDict[word] = wordTotalFrequency

wordsMoreThan100FrequencySortedList = wordsMoreThan100FrequencyDict.most_common()

wordEntropyDict = Counter()
for word in wordsMoreThan100FrequencySortedList:
    wordOnly = word[0]
    entropy = calculateWordEntropy(wordOnly)
    wordEntropyDict[wordOnly] = entropy

sortedWordEntropyList = wordEntropyDict.most_common()

for word in sortedWordEntropyList:
    wordFreqNN = 0
    wordFreqVB = 0
    wordFreqJJ = 0

    if word in frequencyDictNN:
        wordFreqNN += frequencyDictNN[word]
    if word in frequencyDictVB:
        wordFreqVB += frequencyDictVB[word]
    if word in frequencyDictJJ:
        wordFreqJJ += frequencyDictJJ[word]

    formattedString = '%s\tNN: %s\tVB: %s\tJJ: %s' % (word, wordFreqNN, wordFreqVB, wordFreqJJ)
    outputFile.write(formattedString)
