'''
Kya Miller
LING 539 Assignment 1
Q1A - Writes frequency information of words, part of speech tags, and tagged words to three separate text files
'''

import re
from collections import Counter


def makeTaggedWordsSortedList():
    taggedWordsFrequencyDict = Counter()
    for taggedWord in wordsPOSTags:
        taggedWordsFrequencyDict[taggedWord] += 1

    return taggedWordsFrequencyDict.most_common()


def makeWordsSortedList():
    wordsFrequencyDict = Counter()
    for word in wordsOnlyList:
        wordsFrequencyDict[word] += 1

    return wordsFrequencyDict.most_common()


def makePOSTagsSortedList():
    posTagsFrequencyDict = Counter()
    for posTag in posTagsOnlyList:
        posTagsFrequencyDict[posTag] += 1

    return posTagsFrequencyDict.most_common()


filein = open('browntag_nolines.txt', 'r')
brownTagNoLines = filein.read()
filein.close()

tagOutputFile = open('freqout_tag.txt', 'w')
wordOutputFile = open('freqout_word.txt', 'w')
taggedWordOutputFile = open('freqout_taggedword.txt', 'w')

wordsPOSTags = brownTagNoLines.split(' ')
wordsOnlyList = []
posTagsOnlyList = []

for token in wordsPOSTags:
    splitWordPOS = token.split('_', 1)
    word = splitWordPOS[0]
    tag = splitWordPOS[1]
    if re.search('_', tag):
        resplit = tag.split('_', 1)
        word = '%s%s' % (word, resplit[0])
        tag = resplit[1]
    wordsOnlyList.append(word)
    posTagsOnlyList.append(tag)

taggedWordsSortedList = makeTaggedWordsSortedList()

for taggedWord in taggedWordsSortedList:
    formattedString = '%s \t %s \n' % (taggedWord[0], taggedWord[1])
    taggedWordOutputFile.write(formattedString)

wordsSortedList = makeWordsSortedList()

for word in wordsSortedList:
    formattedString = '%s \t %s \n' % (word[0], word[1])
    wordOutputFile.write(formattedString)

posTagsSortedList = makePOSTagsSortedList()

for posTag in posTagsSortedList:
    formattedString = '%s \t %s \n' % (posTag[0], posTag[1])
    tagOutputFile.write(formattedString)

tagOutputFile.close()
taggedWordOutputFile.close()
wordOutputFile.close()
