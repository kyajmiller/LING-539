"""
Kya Miller
LING 539 Assignment 2
Q2 - Finds all of the words from the browntag corpus whose occurences as NN, JJ, or VB is at least 100, then calculates
the entropy of each of those words. Includes a function that prints out these words in order of decreasing entropy,
and shows the unsmoothed count of the associated POS tags.
"""
import re
from collections import Counter


def makeWordsTagsSortedFrequencyDict(wordsTagList):
    frequencyDict = Counter()
    for word in wordsTagList:
        frequencyDict[word] += 1

    sortedList = frequencyDict.most_common()
    sortedFrequencyDict = {sortedWord[0]: sortedWord[1] for sortedWord in sortedList}
    return sortedFrequencyDict

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

distinctWords = list(set(allWords))

frequencyDictNN = makeWordsTagsSortedFrequencyDict(wordsNNTag)
frequencyDictVB = makeWordsTagsSortedFrequencyDict(wordsVBTag)
frequencyDictJJ = makeWordsTagsSortedFrequencyDict(wordsJJTag)

wordTotalFrequencyDict = Counter()

for word in distinctWords:
    wordTotalFrequency = 0
    if word in frequencyDictNN.iterkeys():
        wordTotalFrequency += frequencyDictNN[word]
    if word in frequencyDictVB.iterkeys():
        wordTotalFrequency += frequencyDictVB[word]
    if word in frequencyDictJJ.iterkeys():
        wordTotalFrequency += frequencyDictJJ[word]

    if wordTotalFrequency >= 100:
        wordTotalFrequencyDict[word] = wordTotalFrequency

sortedWordsFrequencyList = wordTotalFrequencyDict.most_common()
