"""
Kya Miller
LING 539 Assignment 3
Q3 - Finds percentage of words which have multiple POS tags in the browntag corpus. Then, given a training/testing split
percentage, the program learns the most likely POS tag for a given word and then calculates the percentage of words and
sentences correctly tagged in the testing set.
"""

from __future__ import division
import re
import math
from collections import Counter


def getPercentageOfWordsWithMoreThanOnePOSTag():
    wordsPOSTagsDict = getWordsPOSTagsDict(brownTagLineByLine)

    wordsMoreThanOnePOS = 0
    for word in wordsPOSTagsDict:
        if len(wordsPOSTagsDict[word][0]) > 1:
            wordsMoreThanOnePOS += 1

    percentWordsMoreThanOnePOS = (wordsMoreThanOnePOS / len(wordsPOSTagsDict)) * 100
    return percentWordsMoreThanOnePOS


def trainAndTestNaiveTagger(trainingPercentage):
    trainingPercentageInteger = trainingPercentage * 100
    testingPercentage = 1 - trainingPercentage

    # calculate how many lines should be in training and testing
    numTotalLines = len(brownTagLineByLine)
    numTrainingLines = math.ceil((numTotalLines * trainingPercentage))
    numTestingLines = numTotalLines - numTrainingLines

    # use slicing to get the training and testing sets
    trainingSet = brownTagLineByLine[:numTrainingLines]
    testingSet = brownTagLineByLine[-numTestingLines:]


def getWordsPOSTagsDict(setOfLines):
    # first just read in browntag stuff and get unique words and unigrams in a list
    wordsDict = Counter()
    posDict = Counter()

    # get unique words and unigrams, establish words dictionary
    for line in setOfLines:
        wordsPOSTags = line.split(' ')

        for token in wordsPOSTags:
            splitWordPOS = token.split('_', 1)
            if len(splitWordPOS) == 2:
                word = splitWordPOS[0]
                tag = splitWordPOS[1]
                if re.search('_', tag):
                    resplit = tag.split('_', 1)
                    word = '%s%s' % (word, resplit[0])
                    tag = resplit[1]
                word = word.lower()
                wordsDict[word] += 1
                posDict[tag] += 1

    # now that we have the dictionary of words, clear out the entries to make room for lists of POS tags
    # each entry has two lists, first list is pos tags, second list is count
    wordsPOSTagsDict = {word: [[], []] for word in wordsDict}

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
                    tag = resplit[1]
                word = word.lower()
                if tag not in wordsPOSTagsDict[word][0]:
                    wordsPOSTagsDict[word][0].append(tag)
                    wordsPOSTagsDict[word][1].append(1)
                else:
                    tagIndex = wordsPOSTagsDict[word][0].index(tag)
                    wordsPOSTagsDict[word][1][tagIndex] += 1

    return wordsPOSTagsDict


def getMostCommonPOSTagPerWord(trainingSet):
    wordsPOSTagsDict = getWordsPOSTagsDict(trainingSet)

    wordsMostCommonPOSTagList = []
    for word in wordsPOSTagsDict:
        mostCommonPOSTagIndex = wordsPOSTagsDict[word][1].index(max(wordsPOSTagsDict[word][1]))
        mostCommonPOSTag = wordsPOSTagsDict[word][0][mostCommonPOSTagIndex]
        wordsMostCommonPOSTagList.append([word, mostCommonPOSTag])

    return wordsMostCommonPOSTagList

# open browntag_nolines.txt as input
filein = open('browntag_nolines.txt', 'r')
brownTagLineByLine = [line.strip() for line in filein]
filein.close()

print('Percentage of words with more than one POS tag: %.2f percent' % getPercentageOfWordsWithMoreThanOnePOSTag())
