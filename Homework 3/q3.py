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
    # calculates the percentage of words with more than one part of speech tag. Calls function to get words and their lists
    # of pos tags; if the word has more than one pos tag, increments count by one
    wordsPOSTagsDict = getWordsPOSTagsDict(brownTagLineByLine)

    wordsMoreThanOnePOS = 0
    for word in wordsPOSTagsDict:
        if len(wordsPOSTagsDict[word][0]) > 1:
            wordsMoreThanOnePOS += 1

    percentWordsMoreThanOnePOS = (wordsMoreThanOnePOS / len(wordsPOSTagsDict)) * 100
    return percentWordsMoreThanOnePOS


def trainAndTestNaiveTagger(trainingPercentage):
    # big function to control testing and training of the Naive Tagger
    # convert training percentage to integer for pretty printing, not important
    trainingSplitInteger = int(trainingPercentage * 100)
    testingSplitInteger = int(100 - trainingSplitInteger)

    print('Preparing sets for %s/%s split...' % (trainingSplitInteger, testingSplitInteger))

    # calculate how many lines should be in training and testing
    numTotalLines = len(brownTagLineByLine)
    numTrainingLines = int(math.ceil((numTotalLines * trainingPercentage)))
    numTestingLines = numTotalLines - numTrainingLines

    # use slicing to get the training and testing sets
    trainingSet = brownTagLineByLine[:numTrainingLines]
    testingSet = brownTagLineByLine[-numTestingLines:]

    # do training
    print('Beginning training on %s%s of corpus...' % (trainingSplitInteger, '%'))
    mostCommonPOSTagsPerWord = getMostCommonPOSTagPerWord(trainingSet)

    # do testing
    print('Testing Naive tagger on %s%s of corpus...' % (testingSplitInteger, '%'))
    percentageWordsTaggedCorrectly, percentageSentencesTaggedCorrectly = testNaiveTagger(mostCommonPOSTagsPerWord,
                                                                                         testingSet)
    # write to file
    formattedString = '%s/%s\t\t%.2f%s\t\t\t\t\t%.2f%s\n' % (
    trainingSplitInteger, testingSplitInteger, percentageWordsTaggedCorrectly, '%', percentageSentencesTaggedCorrectly,
    '%')
    outputFile.write(formattedString)
    print('Complete.')


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
                if tag not in wordsPOSTagsDict[word][0]:
                    wordsPOSTagsDict[word][0].append(tag)
                    wordsPOSTagsDict[word][1].append(1)
                else:
                    tagIndex = wordsPOSTagsDict[word][0].index(tag)
                    wordsPOSTagsDict[word][1][tagIndex] += 1

    return wordsPOSTagsDict


def getMostCommonPOSTagPerWord(trainingSet):
    # calls previous function, gets list of words + pos tags, uses counts to figure out which tag is the most common
    # for the word, returns list of words with their most common tag
    wordsPOSTagsDict = getWordsPOSTagsDict(trainingSet)

    wordsMostCommonPOSTagList = []
    for word in wordsPOSTagsDict:
        mostCommonPOSTagIndex = wordsPOSTagsDict[word][1].index(max(wordsPOSTagsDict[word][1]))
        mostCommonPOSTag = wordsPOSTagsDict[word][0][mostCommonPOSTagIndex]
        wordsMostCommonPOSTagList.append([word, mostCommonPOSTag])

    return wordsMostCommonPOSTagList


def testNaiveTagger(mostCommonPOSTagsPerWord, testingSet):
    # test the Naive tagger using the trained list of most common pos tags per word and the testing set lines
    # split up into words list and pos tags list
    trainedWordsList = [wordPOSPairing[0] for wordPOSPairing in mostCommonPOSTagsPerWord]
    trainedPOSList = [wordPOSPairing[1] for wordPOSPairing in mostCommonPOSTagsPerWord]

    totalWords = 0
    totalWordMatches = 0

    totalSentences = 0
    totalSentenceMatches = 0

    # iterate line by line through testing set
    for line in testingSet:
        sentenceWords = 0
        sentenceWordMatches = 0
        totalSentences += 1

        wordsPOSTags = line.split(' ')

        # split tokens between words and tags
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
                totalWords += 1
                sentenceWords += 1

                # check if word in training set (THIS IS WHY THIS THING IS SO SLOW OMG)
                # if you don't do the check, then it's going to throw key errors left and right. Pls send help.
                if word in trainedWordsList:
                    wordIndex = trainedWordsList.index(word)
                    correctPOSTag = trainedPOSList[wordIndex]
                    # if tag matches, then yay
                    if tag == correctPOSTag:
                        totalWordMatches += 1
                        sentenceWordMatches += 1

        #see how many entire sentences are matches
        if sentenceWords == sentenceWordMatches:
            totalSentenceMatches += 1

    # get percentages and return
    percentageWordsTaggedCorrectly = (totalWordMatches / totalWords) * 100
    percentageSentencesTaggedCorrectly = (totalSentenceMatches / totalSentences) * 100

    return percentageWordsTaggedCorrectly, percentageSentencesTaggedCorrectly


# open browntag_nolines.txt as input
filein = open('browntag_nolines.txt', 'r')
brownTagLineByLine = [line.strip() for line in filein]
filein.close()

# get percentage of words with more than one tag
print('Percentage of words with more than one POS tag: %.2f percent' % getPercentageOfWordsWithMoreThanOnePOSTag())

# open output file
outputFile = open('niave_tagger.txt', 'w')
outputFile.write('Train/Test\tWordsTaggedCorrectly\tEntireSentencesTaggedCorrectly\n')

# do the things
trainAndTestNaiveTagger(0.75)
trainAndTestNaiveTagger(0.50)
trainAndTestNaiveTagger(0.10)
trainAndTestNaiveTagger(0.01)
