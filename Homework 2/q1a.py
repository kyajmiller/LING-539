"""
Kya Miller
LING 539 Assignment 2
Q1A - Writes 100 most frequent unigrams, bigrams, and trigrams with their counts in descending order to output file
ngram_frequencies.txt in a simple table. Does the same thing for POS tags and saves to same file. The outputs are formatted
using tabs.
"""

import re
from collections import Counter


def makeTop100List(tokensList):
    # uses Counter module to make a frequency dictionary. Takes list of words/pos tokens as argument. Returns list of
    # top 100 most common tokens with their counts in descending order.
    frequencyDict = Counter()
    for token in tokensList:
        frequencyDict[token] += 1

    return frequencyDict.most_common(100)


def makeFrequencyList(tokensList):
    # uses Counter module to make a frequency dictionary. Takes list of words/pos tokens as argument. Returns list of
    # tokens with their counts in descending order.
    frequencyDict = Counter()
    for token in tokensList:
        frequencyDict[token] += 1

    return frequencyDict.most_common()


# open ngram_frequencies.txt as output file
outputFile = open('ngram_frequencies.txt', 'w')

# open browntag_nolines.txt as input
filein = open('browntag_nolines.txt', 'r')
brownTagLineByLine = [line.strip() for line in filein]
filein.close()

wordsUnigrams = []
posTagsUnigrams = []
wordsBigrams = []
wordsTrigrams = []
posTagsBigrams = []
posTagsTrigrams = []

# now read in line by line to get unigrams and sentence specific bigrams + trigrams
for line in brownTagLineByLine:
    wordsPOSTags = line.split(' ')

    # declare separate lists to generate bigrams and trigrams
    lineWordsUnigramsToMakeBigrams = ['#']
    linePOSTagsUnigramsToMakeBigrams = ['#']
    lineWordsUnigramsToMakeTrigrams = ['#', '#']
    linePOSTagsUnigramsToMakeTrigrams = ['#', '#']

    # splits each word_posTag on underscore '_'. Sometimes there are multiple underscores in the token, so will redo the
    # split if find second underscore. Append split parts to wordsUnigrams and posTagsUnigrams as appropriate.
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
            lineWordsUnigramsToMakeTrigrams.append(word)
            posTagsUnigrams.append(tag)
            linePOSTagsUnigramsToMakeBigrams.append(tag)
            linePOSTagsUnigramsToMakeTrigrams.append(tag)

    # append appropriate number of # to bigrams and trigrams lists
    lineWordsUnigramsToMakeBigrams.append('#')
    linePOSTagsUnigramsToMakeBigrams.append('#')
    lineWordsUnigramsToMakeTrigrams.append('#')
    lineWordsUnigramsToMakeTrigrams.append('#')
    linePOSTagsUnigramsToMakeTrigrams.append('#')
    linePOSTagsUnigramsToMakeTrigrams.append('#')

    # create bigrams and trigrams using string interpolation and append to appropriate lists
    for i in range(len(lineWordsUnigramsToMakeBigrams) - 1):
        wordsBigrams.append('%s\t%s' % (lineWordsUnigramsToMakeBigrams[i], lineWordsUnigramsToMakeBigrams[i + 1]))

    for i in range(len(lineWordsUnigramsToMakeTrigrams) - 2):
        wordsTrigrams.append('%s\t%s\t%s' % (lineWordsUnigramsToMakeTrigrams[i], lineWordsUnigramsToMakeTrigrams[i + 1],
                                             lineWordsUnigramsToMakeTrigrams[i + 2]))

    for i in range(len(linePOSTagsUnigramsToMakeBigrams) - 1):
        posTagsBigrams.append('%s\t%s' % (linePOSTagsUnigramsToMakeBigrams[i], linePOSTagsUnigramsToMakeBigrams[i + 1]))

    for i in range(len(linePOSTagsUnigramsToMakeTrigrams) - 2):
        posTagsTrigrams.append(
            '%s\t%s\t%s' % (linePOSTagsUnigramsToMakeTrigrams[i], linePOSTagsUnigramsToMakeTrigrams[i + 1],
                            linePOSTagsUnigramsToMakeTrigrams[i + 2]))


# make top 100 lists using previously declared function
wordsUnigramsTop100List = makeTop100List(wordsUnigrams)
wordsBigramsTop100List = makeTop100List(wordsBigrams)
wordsTrigramsTop100List = makeTop100List(wordsTrigrams)

posUnigramsTop100List = makeTop100List(posTagsUnigrams)
posBigramsTop100List = makeTop100List(posTagsBigrams)
posTrigramsTop100List = makeTop100List(posTagsTrigrams)

# write results to output file with some formatting.
outputFile.write('Top 100 Unigrams (words)')
outputFile.write('\n--------\n')

for unigram in wordsUnigramsTop100List:
    formattedString = '%s\t%s\n' % (unigram[0], unigram[1])
    outputFile.write(formattedString)

outputFile.write('\n\n')
outputFile.write('Top 100 Bigrams (words)')
outputFile.write('\n--------\n')

for bigram in wordsBigramsTop100List:
    formattedString = '%s\t%s\n' % (bigram[0], bigram[1])
    outputFile.write(formattedString)

outputFile.write('\n\n')
outputFile.write('Top 100 Trigrams (words)')
outputFile.write('\n--------\n')

for trigram in wordsTrigramsTop100List:
    formattedString = '%s\t%s\n' % (trigram[0], trigram[1])
    outputFile.write(formattedString)

outputFile.write('\n\n')
outputFile.write('Top 100 Unigrams (pos)')
outputFile.write('\n--------\n')

for unigram in posUnigramsTop100List:
    formattedString = '%s\t%s\n' % (unigram[0], unigram[1])
    outputFile.write(formattedString)

outputFile.write('\n\n')
outputFile.write('Top 100 Bigrams (pos)')
outputFile.write('\n--------\n')

for bigram in posBigramsTop100List:
    formattedString = '%s\t%s\n' % (bigram[0], bigram[1])
    outputFile.write(formattedString)

outputFile.write('\n\n')
outputFile.write('Top 100 Trigrams (pos)')
outputFile.write('\n--------\n')

for trigram in posTrigramsTop100List:
    formattedString = '%s\t%s\n' % (trigram[0], trigram[1])
    outputFile.write(formattedString)

outputFile.close()
