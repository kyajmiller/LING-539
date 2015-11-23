"""
Kya Miller
LING 539 Assignment 5
Q2 - Adapts the sentence alignment experiment from q1.py to find the sentence alignment between part2_english_sents_source.txt
and part2_french_sents_target.txt sentences. Consults with the gold alignments described in part2_alignment_key.txt in
order to gauge accuracy.
"""
from __future__ import division


def getSentenceWordCount(sentence):
    # return how many words are in the sentence
    words = sentence.split(' ')
    return len(words)


def calculateSentenceAlignment(sourceSentences, targetSentences, sourceSentencesLengths, targetSentencesLengths):
    # the j=0 row and i=0 column are the first row and first column, makes sense for indices
    # decided to set it up so that i is along the columns and j is down the rows
    # initialize sentenceAlignmentTable, set everything to empty string
    sentenceAlignmentTable = [[0 for i in range(len(sourceSentences) + 1)] for j in range(len(targetSentences) + 1)]

    # initialize the alignment types table, this is where the alignment types will live
    sentenceAlignmentTypesTable = [['' for i in range(len(sourceSentences) + 1)] for j in
                                     range(len(targetSentences) + 1)]

    # iterate through rows
    for j in range(len(sentenceAlignmentTable)):
        currentRow = sentenceAlignmentTable[j]
        # iterate through columns
        for i in range(len(currentRow)):
            # set 0,0 to 0
            if j == 0 and i == 0:
                sentenceAlignmentTable[j][i] = 0
                sentenceAlignmentTypesTable[j][i] = '0'
            # everything else, calculate the minimum alignment cost and alignment types using the getMinimumAlignment function
            else:
                minimumAlignmentCost, minimumAlignmentTypes = getMinimumAlignment(i, j, sentenceAlignmentTable,
                                                                                  sourceSentencesLengths,
                                                                                  targetSentencesLengths)
                # set table values to appropriate values so can feed back into the function
                sentenceAlignmentTable[j][i] = minimumAlignmentCost
                sentenceAlignmentTypesTable[j][i] = minimumAlignmentTypes

    # flip the tables so that the i values are columns and the j values are rows, will allow to iterate through the
    # j rows and find the minimum alignment, couldn't do that before
    flippedAlignmentTable = [z for z in zip(*sentenceAlignmentTable)]
    flippedAlignmentTypesTable = [z for z in zip(*sentenceAlignmentTypesTable)]

    return flippedAlignmentTable, flippedAlignmentTypesTable


def getMinimumAlignment(i, j, sentenceAlignmentTable, sourceSentencesLengths, targetSentencesLengths):
    # calculates the minimum alignment cost and the possible alignment types for that cost, returns the cost and the
    # alignment strings

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
    # get the index of the alignment type
    allAlignmentCosts = [alignment01, alignment10, alignment11, alignment12, alignment21, alignment22]

    # if the alignment value is the same as the minimum alignment cost, get the index of that value, then grab the
    # alignment type with the same index and append it to the list
    minimumAlignmentTypes = []
    for k in range(len(allAlignmentCosts)):
        if allAlignmentCosts[k] == minimumAlignmentCost:
            minimumAlignmentTypes.append(alignmentPossibilities[k])

    return minimumAlignmentCost, minimumAlignmentTypes


def getAlignedSentences(sentenceAlignmentTable, alignmentTypesTable, sourceSentences, targetSentences):
    # calculates and returns which sentences align with which other sentences

    # iterate through the rows/sentences of the sentenceAlignmentTable to find the minimum alignment cost for that
    # sentence in order to get the proper alignment type, which is then used to match up the sentences
    sentenceAlignmentTypes = []
    for i in range(len(sentenceAlignmentTable)):
        # ignore the first row since that's the i = 0 row, doesn't give any real alignment information
        if i > 0:
            # get the alignment costs and the alignment types associated with those costs
            currentSentenceAlignments = sentenceAlignmentTable[i]
            currentSentenceAlignmentTypes = alignmentTypesTable[i]
            # get the minimum cost value
            minimumAlignment = min(currentSentenceAlignments)
            minimumAlignmentType = ''
            # get the alignment type associated with the minimum cost by matching indices, there can be multiple
            for j in range(len(currentSentenceAlignments)):
                if currentSentenceAlignments[j] == minimumAlignment:
                    minimumIndex = j
                    minimumAlignmentType = currentSentenceAlignmentTypes[minimumIndex]

            sentenceAlignmentTypes.append(minimumAlignmentType)

    # keep track of how many source sentences matched up, keep going until run out of source sentences
    targetSentencesCounter = 0
    sourceSentencesCounter = 0

    sourceSentenceAlignmentGroups = []
    targetSentenceAlignmentGroups = []

    # iterate through the source sentences
    for k in range(len(sourceSentences)):
        # check that it's not working on a sentence that's already been matched
        if k == sourceSentencesCounter:
            alignmentType = sentenceAlignmentTypes[k]
            # calculate how many source sentences match with how many target sentences
            numSourceSents, numTargetSents = processAlignmentTypes(alignmentType[0])

            # initialize list of which source sentences go with which target sentences
            alignedSourceSentencesList = []
            sourceSentencesIndexList = []

            # append appropriate number of source sentences to the list, increment sourceSentencesCounter so don't reuse
            # source sentences
            for l in range(numSourceSents):
                if sourceSentencesCounter < len(sourceSentences):
                    alignedSourceSentencesList.append(sourceSentences[sourceSentencesCounter])
                    sourceSentencesIndexList.append(sourceSentencesCounter)
                    sourceSentencesCounter += 1
            sourceSentenceAlignmentGroups.append(sourceSentencesIndexList)

            # do the same thing for target sentences
            alignedTargetSentencesList = []
            targetSentencesIndexList = []
            for m in range(numTargetSents):
                if targetSentencesCounter < len(targetSentences):
                    alignedTargetSentencesList.append(targetSentences[targetSentencesCounter])
                    targetSentencesIndexList.append(targetSentencesCounter)
                    targetSentencesCounter += 1
            targetSentenceAlignmentGroups.append(targetSentencesIndexList)

    # turn sentence indexes into sentence numbers, add s or t to denote if source or target
    sourceGroupAlignmentConvertToStrings = [['s%s' % (index + 1) for index in sourceGroup] for sourceGroup in
                                            sourceSentenceAlignmentGroups]
    targetGroupAlignmentConvertToStrings = [['t%s' % (index + 1) for index in targetGroup] for targetGroup in
                                            targetSentenceAlignmentGroups]

    # print the aligned sentences
    print('SourceSentences ---> TargetSentences')
    for sourceGroup, targetGroup in zip(sourceGroupAlignmentConvertToStrings, targetGroupAlignmentConvertToStrings):
        print('%s ---> %s' % (' '.join(sourceGroup), ' '.join(targetGroup)))

    return sourceGroupAlignmentConvertToStrings, targetGroupAlignmentConvertToStrings


def processAlignmentTypes(alignmentType):
    # convert alignment types into numSourceSents and numTargetSents
    numSourceSents = 0
    numTargetSents = 0
    if alignmentType == '0:1':
        numSourceSents = 0
        numTargetSents = 1
    elif alignmentType == '1:0':
        numSourceSents = 1
        numTargetSents = 0
    elif alignmentType == '1:1':
        numSourceSents = 1
        numTargetSents = 1
    elif alignmentType == '1:2':
        numSourceSents = 1
        numTargetSents = 2
    elif alignmentType == '2:1':
        numSourceSents = 2
        numTargetSents = 1
    elif alignmentType == '2:2':
        numSourceSents = 2
        numTargetSents = 2
    return numSourceSents, numTargetSents


def doSentenceAlignmentExperiment(sourceSentences, targetSentences):
    # do the three parts of the sentence alignment experiment for the given input and print three tables with
    # calculated data to the console

    # get source and target sentences lengths so won't have to keep calling the functions later
    sourceSentencesLengths = [getSentenceWordCount(sentence) for sentence in sourceSentences]
    targetSentencesLengths = [getSentenceWordCount(sentence) for sentence in targetSentences]

    # calculate sentence alignment
    calculatedSentenceAlignmentTable, alignmentTypesTable = calculateSentenceAlignment(sourceSentences, targetSentences,
                                                                                       sourceSentencesLengths,
                                                                                       targetSentencesLengths)

    # calculate which source sentences match with which target sentences
    sourceGroupAlignments, targetGroupAlignments = getAlignedSentences(calculatedSentenceAlignmentTable,
                                                                       alignmentTypesTable,
                                                                       sourceSentences, targetSentences)

    # calculate accuracy - how many matches / total
    numAlignmentGroups = 0
    numTotalMatches = 0
    for predictedSourceSentencesGroup, predictedTargetSentencesGroup, goldSourceSentencesGroup, goldTargetSentencesGroup in zip(
            sourceGroupAlignments, targetGroupAlignments, goldSourceSentencesAlignmentGroups,
            goldTargetSentencesAlignmentGroups):
        numAlignmentGroups += 1
        if sorted(predictedSourceSentencesGroup) == sorted(goldSourceSentencesGroup) and sorted(
                predictedTargetSentencesGroup) == sorted(goldTargetSentencesGroup):
            numTotalMatches += 1

    totalMatchAccuracy = (numTotalMatches / numAlignmentGroups) * 100

    # print result to console
    print('\nPercentage of matched alignment groups: %s' % totalMatchAccuracy)


# open source sentences file
sourceSentencesFileIn = open('part2_english_sents_source.txt', 'r')
sourceSentences = [line.strip() for line in sourceSentencesFileIn.readlines()]
sourceSentencesFileIn.close()

# open target sentences file
targetSentencesFileIn = open('part2_french_sents_target.txt', 'r')
targetSentences = [line.strip() for line in targetSentencesFileIn.readlines()]
targetSentencesFileIn.close()

# open gold alignment key file
goldSentenceAlignmentsFileIn = open('part2_alignment_key.txt', 'r')
goldSentenceAlignmentsUnpacked = [line.strip() for line in goldSentenceAlignmentsFileIn.readlines()]
goldSentenceAlignmentsFileIn.close()

goldSourceSentencesAlignmentGroups = []
goldTargetSentencesAlignmentGroups = []
goldAlignmentTypes = []

# iterate through the unpacked alignments
for unpackedAlignment in goldSentenceAlignmentsUnpacked:
    # split line into alignment groups and alignment type, append alignment type to goldAlignmentTypes list
    separateGroupsAlignmentType = unpackedAlignment.split(';', 1)
    groups = separateGroupsAlignmentType[0].strip()
    alignmentType = separateGroupsAlignmentType[1].strip()
    goldAlignmentTypes.append(alignmentType)

    # split alignment groups into source and target group string
    separateAlignmentGroups = groups.split('-', 1)
    sourceAlignmentGroups = separateAlignmentGroups[0].strip()
    targetAlignmentGroups = separateAlignmentGroups[1].strip()

    # split source group string into list of sentences, append list to goldSourceSentencesAlignmentGroups
    sourceAlignmentGroupsList = sourceAlignmentGroups.split(', ')
    goldSourceSentencesAlignmentGroups.append(sourceAlignmentGroupsList)

    # do the same for target group, append to appropriate list
    targetAlignmentGroupsList = targetAlignmentGroups.split(', ')
    goldTargetSentencesAlignmentGroups.append(targetAlignmentGroupsList)

# do the experiment
doSentenceAlignmentExperiment(sourceSentences, targetSentences)
