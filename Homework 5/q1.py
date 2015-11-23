"""
Kya Miller
LING 539 Assignment 5
Q1 - Reads in sents_source.txt and sents_target.txt as input files, prints the number of words in each sentence to
output.txt. Calculates sentence alignment between sents_source and sents_target, and prints the output to console.
"""


def getSentenceWordCount(sentence):
    words = sentence.split(' ')
    return len(words)


def doWordCountsForSourceSentencesAndPrintToOutput():
    for i in range(len(sourceSentences)):
        numWords = getSentenceWordCount(sourceSentences[i])
        outputString = 's%s\t\t\t%s\n' % (i + 1, numWords)
        outputFile.write(outputString)


def doWordCountsForTargetSentencesAndPrintToOutput():
    for i in range(len(targetSentences)):
        numWords = getSentenceWordCount(targetSentences[i])
        outputString = 't%s\t\t\t%s\n' % (i + 1, numWords)
        outputFile.write(outputString)


def getMinimumAlignment(i, j):
    pass


def doSentenceAlignment():
    # the j=0 row and i=0 column are the first row and first column, makes sense for indices
    # decided to set it up so that i is along the columns and j is down the rows
    # initialize sentenceAlignmentTable, set everything to empty string
    sentenceAlignmentTable = [['' for i in range(len(sourceSentences) + 1)] for j in range(len(targetSentences) + 1)]

    for j in range(len(sentenceAlignmentTable)):
        currentRow = sentenceAlignmentTable[j]
        for i in range(len(currentRow)):
            currentItem = currentRow[i]
            if j == 0 and i == 0:
                sentenceAlignmentTable[j][i] = 0

    return sentenceAlignmentTable


# read in sents_source.txt, store sentences in array
sourceSentencesFileIn = open('sents_source.txt', 'r')
sourceSentences = [line.strip() for line in sourceSentencesFileIn.readlines()]
sourceSentencesFileIn.close()

# read in sents_target.txt, store sentences in array
targetSentencesFileIn = open('sents_target.txt', 'r')
targetSentences = [line.strip() for line in targetSentencesFileIn.readlines()]
targetSentencesFileIn.close()

# open output file
outputFile = open('output.txt', 'w')
headerString = 'Sentence\tNumber Of Words\n'
outputFile.write(headerString)

# get num words for each source sentence and target sentence, print to output file
doWordCountsForSourceSentencesAndPrintToOutput()
outputFile.write('---------------------------\n')
doWordCountsForTargetSentencesAndPrintToOutput()

# calculate sentence alignment
calculatedSentenceAlignmentTable = doSentenceAlignment()
for row in calculatedSentenceAlignmentTable: print(row)
