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


def getMinimumAlignment(i, j, sentenceAlignmentTable):
    alignmentPossibilities = ['0:1', '1:0', '1:1', '1:2', '2:1', '2:2']

    alignment01, alignment10, alignment11, alignment12, alignment21, alignment22 = 0, 0, 0, 0, 0, 0

    validAlignments = []

    if j - 1 >= 0:
        alignment01 = sentenceAlignmentTable[j - 1][i] + abs(getSentenceWordCount(targetSentences[j + 1]) - 0)
        validAlignments.append(alignment01)
    if i - 1 >= 0:
        alignment10 = sentenceAlignmentTable[j][i - 1] + abs(getSentenceWordCount(sourceSentences[i + 1]) - 0)
        validAlignments.append(alignment10)
    if i - 1 >= 0 and j - 1 >= 0:
        alignment11 = sentenceAlignmentTable[j - 1][i - 1] + abs(
            getSentenceWordCount(sourceSentences[i + 1]) - getSentenceWordCount(targetSentences[j + 1]))
        validAlignments.append(alignment11)
    if i - 1 >= 0 and j - 2 >= 0:
        alignment12 = sentenceAlignmentTable[j - 2][i - 1] + abs(getSentenceWordCount(sourceSentences[i + 1]) - (
        getSentenceWordCount(targetSentences[(j - 1) + 1]) + getSentenceWordCount(targetSentences[j + 1])))
        validAlignments.append(alignment12)
    if i - 2 >= 0 and j - 1 >= 0:
        alignment21 = sentenceAlignmentTable[j - 1][i - 2] + abs((getSentenceWordCount(
            sourceSentences[(i - 1) + 1]) + getSentenceWordCount(sourceSentences[i + 1])) - getSentenceWordCount(
            targetSentences[j + 1]))
        validAlignments.append(alignment21)
    if i - 2 >= 0 and j - 2 >= 0:
        alignment22 = sentenceAlignmentTable[j - 2][i - 2] + abs(
            (getSentenceWordCount(sourceSentences[(i - 1) + 1]) + getSentenceWordCount(sourceSentences[i + 1])) - (
            getSentenceWordCount(targetSentences[(j - 1) + 1]) + getSentenceWordCount(targetSentences[j + 1])))
        validAlignments.append(alignment22)

    minimumAlignmentCost = min(validAlignments)
    allAlignmentCosts = [alignment01, alignment10, alignment11, alignment12, alignment21, alignment22]

    minimumAlignmentStrings = []
    for k in range(len(allAlignmentCosts)):
        if allAlignmentCosts[k] == minimumAlignmentCost:
            minimumAlignmentStrings.append(alignmentPossibilities[k])

    return minimumAlignmentCost, minimumAlignmentStrings


def doSentenceAlignment():
    # the j=0 row and i=0 column are the first row and first column, makes sense for indices
    # decided to set it up so that i is along the columns and j is down the rows
    # initialize sentenceAlignmentTable, set everything to empty string
    sentenceAlignmentTable = [['' for i in range(len(sourceSentences) + 1)] for j in range(len(targetSentences) + 1)]
    sentenceAlignmentStringsTable = [['' for i in range(len(sourceSentences) + 1)] for j in
                                     range(len(targetSentences) + 1)]
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

# get source and target sentences lengths so won't have to keep calling the functions later
sourceSentencesLengths = [getSentenceWordCount(sentence) for sentence in sourceSentences]
targetSentencesLengths = [getSentenceWordCount(sentence) for sentence in targetSentences]

# calculate sentence alignment
calculatedSentenceAlignmentTable = doSentenceAlignment()
for row in calculatedSentenceAlignmentTable: print(row)
print(len(calculatedSentenceAlignmentTable))
print(len(calculatedSentenceAlignmentTable[0]))
