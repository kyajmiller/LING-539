"""
Kya Miller
LING 539 Assignment 5
Q1 - Reads in sents_source.txt and sents_target.txt as input files, prints the number of words in each sentence to
output.txt. Calculates sentence alignment between sents_source and sents_target, and prints the output to console.
"""


def getSentenceWordCount(sentence):
    words = sentence.split(' ')
    return len(words)


def doWordCountsForSourceSentencesAndPrintToOutput(sourceSentences):
    for i in range(len(sourceSentences)):
        numWords = getSentenceWordCount(sourceSentences[i])
        outputString = 's%s\t\t\t%s\n' % (i + 1, numWords)
        outputFile.write(outputString)


def doWordCountsForTargetSentencesAndPrintToOutput(targetSentences):
    for i in range(len(targetSentences)):
        numWords = getSentenceWordCount(targetSentences[i])
        outputString = 't%s\t\t\t%s\n' % (i + 1, numWords)
        outputFile.write(outputString)


def getMinimumAlignment(i, j, sentenceAlignmentTable, sourceSentencesLengths, targetSentencesLengths):
    # calculates the minimum alignment cost and the possible alignment types for that cost, returns the cost and the
    # strings

    # list of possible alignments, needed list so can have indices for later
    alignmentPossibilities = ['0:1', '1:0', '1:1', '1:2', '2:1', '2:2']

    # initialize alignment values to empty string, necessary to have some value here even if null for later
    alignment01, alignment10, alignment11, alignment12, alignment21, alignment22 = '', '', '', '', '', ''

    # declare an empty list of valid alignments, if the current i and j values are legal for the alignment possibility,
    # the calculated cost is appended here so can later get minimum cost value
    validAlignments = []

    # calculate possible costs of alignment
    if j - 1 >= 0:
        alignment01 = sentenceAlignmentTable[j - 1][i] + abs(targetSentencesLengths[j - 1] - 0)
        validAlignments.append(alignment01)
    if i - 1 >= 0:
        alignment10 = sentenceAlignmentTable[j][i - 1] + abs(sourceSentencesLengths[i - 1] - 0)
        validAlignments.append(alignment10)
    if i - 1 >= 0 and j - 1 >= 0:
        alignment11 = sentenceAlignmentTable[j - 1][i - 1] + abs(
            sourceSentencesLengths[i - 1] - targetSentencesLengths[j - 1])
        validAlignments.append(alignment11)
    if i - 1 >= 0 and j - 2 >= 0:
        alignment12 = sentenceAlignmentTable[j - 2][i - 1] + abs(sourceSentencesLengths[i - 1] - (
            targetSentencesLengths[(j - 1) - 1] + targetSentencesLengths[j - 1]))
        validAlignments.append(alignment12)
    if i - 2 >= 0 and j - 1 >= 0:
        alignment21 = sentenceAlignmentTable[j - 1][i - 2] + abs(
            (sourceSentencesLengths[(i - 1) - 1] + sourceSentencesLengths[i - 1]) - targetSentencesLengths[j - 1])
        validAlignments.append(alignment21)
    if i - 2 >= 0 and j - 2 >= 0:
        alignment22 = sentenceAlignmentTable[j - 2][i - 2] + abs(
            (sourceSentencesLengths[(i - 1) - 1] + sourceSentencesLengths[i - 1]) - (
                targetSentencesLengths[(j - 1) - 1] + targetSentencesLengths[j - 1]))
        validAlignments.append(alignment22)

    # get minimum value of valid alignment costs
    minimumAlignmentCost = min(validAlignments)

    # make a list of all the values, both valid and empty - this lets you get the index of the minimum value so you can
    # get the index of the alignment string
    allAlignmentCosts = [alignment01, alignment10, alignment11, alignment12, alignment21, alignment22]

    # if the alignment value is the same as the minimum alignment cost, get the index of that value, then grab the
    # alignment string with the same index and append it to the list
    minimumAlignmentStrings = []
    for k in range(len(allAlignmentCosts)):
        if allAlignmentCosts[k] == minimumAlignmentCost:
            minimumAlignmentStrings.append(alignmentPossibilities[k])

    return minimumAlignmentCost, minimumAlignmentStrings


def calculateSentenceAlignment(sourceSentences, targetSentences, sourceSentencesLengths, targetSentencesLengths):
    # the j=0 row and i=0 column are the first row and first column, makes sense for indices
    # decided to set it up so that i is along the columns and j is down the rows
    # initialize sentenceAlignmentTable, set everything to empty string
    sentenceAlignmentTable = [[0 for i in range(len(sourceSentences) + 1)] for j in range(len(targetSentences) + 1)]

    # initialize the alignment string table, this is where the strings will live
    sentenceAlignmentStringsTable = [['' for i in range(len(sourceSentences) + 1)] for j in
                                     range(len(targetSentences) + 1)]

    # iterate through rows
    for j in range(len(sentenceAlignmentTable)):
        currentRow = sentenceAlignmentTable[j]
        # iterate through columns
        for i in range(len(currentRow)):
            # set 0,0 to 0
            if j == 0 and i == 0:
                sentenceAlignmentTable[j][i] = 0
                sentenceAlignmentStringsTable[j][i] = None
            # everything else, calculate the minimum alignment cost and strings using the getMinimumAlignment function
            else:
                minimumAlignmentCost, minimumAlignmentStrings = getMinimumAlignment(i, j, sentenceAlignmentTable, sourceSentencesLengths, targetSentencesLengths)
                # set table values to appropriate values so can feed back into the function
                sentenceAlignmentTable[j][i] = minimumAlignmentCost
                sentenceAlignmentStringsTable[j][i] = minimumAlignmentStrings

    # flip the tables so that the i values are columns and the j values are rows, will allow to iterate through the
    # j rows and find the minimum alignment, couldn't do that before
    flippedAlignmentTable = [z for z in zip(*sentenceAlignmentTable)]
    flippedAlignmentStringsTable = [z for z in zip(*sentenceAlignmentStringsTable)]

    return flippedAlignmentTable, flippedAlignmentStringsTable


def getAlignedSentences(sentenceAlignmentTable, alignmentStringsTable, sourceSentences, targetSentences):
    print('SourceSentences\tTargetSentences')
    sentenceAlignmentStrings = []
    for i in range(len(sentenceAlignmentTable)):
        if i > 0:
            currentSentenceAlignments = sentenceAlignmentTable[i]
            currentSentenceAlignmentStrings = alignmentStringsTable[i]
            minimumAlignment = min(currentSentenceAlignments)
            minimumAlignmentString = ''
            for j in range(len(currentSentenceAlignments)):
                if currentSentenceAlignments[j] == minimumAlignment:
                    minimumIndex = j
                    minimumAlignmentString = currentSentenceAlignmentStrings[minimumIndex]

            sentenceAlignmentStrings.append(minimumAlignmentString)

    targetSentencesCounter = 0
    sourceSentencesCounter = 0

    sourceSentenceAlignmentGroups = []
    targetSentenceAlignmentGroups = []

    for k in range(len(sourceSentences)):
        if k == sourceSentencesCounter:
            alignmentString = sentenceAlignmentStrings[k]
            numSourceSents, numTargetSents = processAlignmentStrings(alignmentString[0])

            alignedSourceSentencesList = []
            sourceSentencesIndexList = []

            for l in range(numSourceSents):
                if sourceSentencesCounter < len(sourceSentences):
                    alignedSourceSentencesList.append(sourceSentences[sourceSentencesCounter])
                    sourceSentencesIndexList.append(sourceSentencesCounter)
                    sourceSentencesCounter += 1
            sourceSentenceAlignmentGroups.append(sourceSentencesIndexList)

            alignedTargetSentencesList = []
            targetSentencesIndexList = []
            for m in range(numTargetSents):
                if targetSentencesCounter < len(targetSentences):
                    alignedTargetSentencesList.append(targetSentences[targetSentencesCounter])
                    targetSentencesIndexList.append(targetSentencesCounter)
                    targetSentencesCounter += 1
            targetSentenceAlignmentGroups.append(targetSentencesIndexList)

    sourceGroupAlignmentStrings = [['s%s' % (index + 1) for index in sourceGroup] for sourceGroup in
                                   sourceSentenceAlignmentGroups]
    targetGroupAlignmentStrings = [['t%s' % (index + 1) for index in targetGroup] for targetGroup in
                                   targetSentenceAlignmentGroups]
    for sourceGroup, targetGroup in zip(sourceGroupAlignmentStrings, targetGroupAlignmentStrings):
        print('%s\t\t\t\t%s' % (' '.join(sourceGroup), ' '.join(targetGroup)))


def processAlignmentStrings(alignmentString):
    # convert alignment strings into numSourceSents and numTargetSents
    numSourceSents = 0
    numTargetSents = 0
    if alignmentString == '0:1':
        numSourceSents = 0
        numTargetSents = 1
    elif alignmentString == '1:0':
        numSourceSents = 1
        numTargetSents = 0
    elif alignmentString == '1:1':
        numSourceSents = 1
        numTargetSents = 1
    elif alignmentString == '1:2':
        numSourceSents = 1
        numTargetSents = 2
    elif alignmentString == '2:1':
        numSourceSents = 2
        numTargetSents = 1
    elif alignmentString == '2:2':
        numSourceSents = 2
        numTargetSents = 2
    return numSourceSents, numTargetSents


def doSentenceAlignmentExperiment(sourceSentences, targetSentences):
    # get source and target sentences lengths so won't have to keep calling the functions later
    sourceSentencesLengths = [getSentenceWordCount(sentence) for sentence in sourceSentences]
    targetSentencesLengths = [getSentenceWordCount(sentence) for sentence in targetSentences]

    # calculate sentence alignment
    calculatedSentenceAlignmentTable, stringsTable = calculateSentenceAlignment(sourceSentences, targetSentences, sourceSentencesLengths, targetSentencesLengths)

    # print the sentenceAlignmentTable to console
    targetRowHeaderList = []
    targetRowHeaderList.append('0')
    for i in range(len(targetSentencesFile)):
        targetRowHeaderList.append('t%s' % (i + 1))

    print('Sentence Alignment Table')
    print('\t%s' % '\t'.join(targetRowHeaderList))

    for i in range(len(calculatedSentenceAlignmentTable)):
        if i == 0:
            sentenceTag = '0'
        else:
            sentenceTag = 's%s' % i
        currentRowString = '\t'.join([str(item) for item in calculatedSentenceAlignmentTable[i]])
        formattedCurrentRow = '%s\t%s' % (sentenceTag, currentRowString)
        print(formattedCurrentRow)

    # get sentence alignment strings
    print('\n')
    getAlignedSentences(calculatedSentenceAlignmentTable, stringsTable, sourceSentences, targetSentences)



# read in sents_source.txt, store sentences in array
sourceSentencesFileIn = open('sents_source.txt', 'r')
sourceSentencesFile = [line.strip() for line in sourceSentencesFileIn.readlines()]
sourceSentencesFileIn.close()

# read in sents_target.txt, store sentences in array
targetSentencesFileIn = open('sents_target.txt', 'r')
targetSentencesFile = [line.strip() for line in targetSentencesFileIn.readlines()]
targetSentencesFileIn.close()

# open output file
outputFile = open('output.txt', 'w')
headerString = 'Sentence\tNumber Of Words\n'
outputFile.write(headerString)

# get num words for each source sentence and target sentence, print to output file
doWordCountsForSourceSentencesAndPrintToOutput(sourceSentencesFile)
outputFile.write('---------------------------\n')
doWordCountsForTargetSentencesAndPrintToOutput(targetSentencesFile)

# do the sentence alignment experiment with the sents_source and sents_target info as input
doSentenceAlignmentExperiment(sourceSentencesFile, targetSentencesFile)






