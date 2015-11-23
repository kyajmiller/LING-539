"""
Kya Miller
LING 539 Assignment 5
Q1 - Reads in sents_source.txt and sents_target.txt as input files, prints the number of words in each sentence to
output.txt. Calculates sentence alignment between sents_source and sents_target, and prints the output to console.
"""


def getSentenceWordCount(sentence):
    # return number of words in sentence
    words = sentence.split(' ')
    return len(words)


def doWordCountsExerciseAndPrintToOutputFile(sourceSentences, targetSentences):
    # open output file
    outputFile = open('output.txt', 'w')

    headerString = 'Sentence\tNumber Of Words\n'
    outputFile.write(headerString)

    # get num words for each source sentence and target sentence, print to output file
    for i in range(len(sourceSentences)):
        numWords = getSentenceWordCount(sourceSentences[i])
        outputString = 's%s\t\t\t%s\n' % (i + 1, numWords)
        outputFile.write(outputString)
    outputFile.write('---------------------------\n')
    for i in range(len(targetSentences)):
        numWords = getSentenceWordCount(targetSentences[i])
        outputString = 't%s\t\t\t%s\n' % (i + 1, numWords)
        outputFile.write(outputString)

    outputFile.close()


def doWordCountsExerciseAndPrintToConsole(sourceSentences, targetSentences):
    # basically do same thing as previous function, but print output to console instead
    headerString = 'Sentence\tNumber Of Words'
    print(headerString)
    for i in range(len(sourceSentences)):
        numWords = getSentenceWordCount(sourceSentences[i])
        outputString = 's%s\t\t\t%s' % (i + 1, numWords)
        print(outputString)
    print('---------------------------')
    for i in range(len(targetSentences)):
        numWords = getSentenceWordCount(targetSentences[i])
        outputString = 't%s\t\t\t%s' % (i + 1, numWords)
        print(outputString)


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
                sentenceAlignmentStringsTable[j][i] = '0'
            # everything else, calculate the minimum alignment cost and strings using the getMinimumAlignment function
            else:
                minimumAlignmentCost, minimumAlignmentStrings = getMinimumAlignment(i, j, sentenceAlignmentTable,
                                                                                    sourceSentencesLengths,
                                                                                    targetSentencesLengths)
                # set table values to appropriate values so can feed back into the function
                sentenceAlignmentTable[j][i] = minimumAlignmentCost
                sentenceAlignmentStringsTable[j][i] = minimumAlignmentStrings

    # flip the tables so that the i values are columns and the j values are rows, will allow to iterate through the
    # j rows and find the minimum alignment, couldn't do that before
    flippedAlignmentTable = [z for z in zip(*sentenceAlignmentTable)]
    flippedAlignmentStringsTable = [z for z in zip(*sentenceAlignmentStringsTable)]

    return flippedAlignmentTable, flippedAlignmentStringsTable


def getMinimumAlignment(i, j, sentenceAlignmentTable, sourceSentencesLengths, targetSentencesLengths):
    # calculates the minimum alignment cost and the possible alignment types for that cost, returns the cost and the
    # alignmentType

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
    # get the index of the alignmentType
    allAlignmentCosts = [alignment01, alignment10, alignment11, alignment12, alignment21, alignment22]

    # if the alignment value is the same as the minimum alignment cost, get the index of that value, then grab the
    # alignmentType with the same index and append it to the list
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
        if i > 0:
            # ignore the first row since that's the i = 0 row, doesn't give any real alignment information
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
            alignmentTypes = sentenceAlignmentTypes[k]
            # calculate how many source sentences match with how many target sentences
            numSourceSents, numTargetSents = processAlignmentTypes(alignmentTypes[0])

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
    sourceGroupAlignmentsConvertToStrings = [['s%s' % (index + 1) for index in sourceGroup] for sourceGroup in
                                             sourceSentenceAlignmentGroups]
    targetGroupAlignmentConvertToStrings = [['t%s' % (index + 1) for index in targetGroup] for targetGroup in
                                            targetSentenceAlignmentGroups]

    # print the aligned sentences
    print('SourceSentences\tTargetSentences')
    for sourceGroup, targetGroup in zip(sourceGroupAlignmentsConvertToStrings, targetGroupAlignmentConvertToStrings):
        print('%s\t\t\t\t%s' % (' '.join(sourceGroup), ' '.join(targetGroup)))


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

    # basically do what the function says
    doWordCountsExerciseAndPrintToConsole(sourceSentences, targetSentences)
    print('\n')

    # get source and target sentences lengths so won't have to keep calling the functions later
    sourceSentencesLengths = [getSentenceWordCount(sentence) for sentence in sourceSentences]
    targetSentencesLengths = [getSentenceWordCount(sentence) for sentence in targetSentences]

    # calculate sentence alignment
    sentenceAlignmentTable, alignmentTypesTable = calculateSentenceAlignment(sourceSentences, targetSentences,
                                                                             sourceSentencesLengths,
                                                                             targetSentencesLengths)

    # print the sentenceAlignmentTable to console
    targetRowHeaderList = []
    targetRowHeaderList.append('0')
    for i in range(len(targetSentences)):
        targetRowHeaderList.append('t%s' % (i + 1))

    print('Sentence Alignment Table')
    print('\t%s' % '\t'.join(targetRowHeaderList))

    for i in range(len(sentenceAlignmentTable)):
        if i == 0:
            sentenceTag = '0'
        else:
            sentenceTag = 's%s' % i
        currentRowJoinToString = '\t'.join([str(item) for item in sentenceAlignmentTable[i]])
        formattedCurrentRow = '%s\t%s' % (sentenceTag, currentRowJoinToString)
        print(formattedCurrentRow)

    # print the alignment cost and alignmentTypes, displays only the first item in each alingment types list for the sake of
    # clarity and prettiness, not an accurate representation of the possibilities
    print('\n')
    print('Sentence Alignment Table With First Alignment Possibility')
    print('\t%s' % '\t\t'.join(targetRowHeaderList))

    for i in range(len(sentenceAlignmentTable)):
        if i == 0:
            sentenceTag = '0'
        else:
            sentenceTag = 's%s' % i
        currentRowCosts = [str(item) for item in sentenceAlignmentTable[i]]
        currentRowAlignmentTypes = [alignmentTypesList[0] for alignmentTypesList in alignmentTypesTable[i]]
        costAndTypes = ['%s/%s' % (cost, alignmentType) for cost, alignmentType in
                        zip(currentRowCosts, currentRowAlignmentTypes)]
        currentRowJoinToString = '\t'.join(costAndTypes)
        formattedCurrentRow = '%s\t%s' % (sentenceTag, currentRowJoinToString)
        print(formattedCurrentRow)

    print('\n')
    getAlignedSentences(sentenceAlignmentTable, alignmentTypesTable, sourceSentences, targetSentences)


# read in sents_source.txt, store sentences in array
sourceSentencesFileIn = open('sents_source.txt', 'r')
sourceSentencesFile = [line.strip() for line in sourceSentencesFileIn.readlines()]
sourceSentencesFileIn.close()

# read in sents_target.txt, store sentences in array
targetSentencesFileIn = open('sents_target.txt', 'r')
targetSentencesFile = [line.strip() for line in targetSentencesFileIn.readlines()]
targetSentencesFileIn.close()

# do word counts exercise for sents_source.txt and sents_target.txt
doWordCountsExerciseAndPrintToOutputFile(sourceSentencesFile, targetSentencesFile)

# source sentences and target sentences from the lecture
sourceSentencesLecture = ['I call for two statements.',
                          'First, as the Minister will be aware, last month the Welsh Senate of Older People e-mailed all Assembly Members concerning the P is for People campaign to raise awareness of the lack of public toilet provision in Wales, and it attached its latest research urging all Assembly Members to bring this to the attention of the Welsh Government.',
                          'It would therefore be appreciated if we could have a statement from the Welsh Government accordingly.']
targetSentencesLecture = ['Galwaf am ddau ddatganiad.',
                          "Yn gyntaf, fel y bydd y Gweinidog yn gwybod, y mis diwethaf anfonodd Senedd Pobl H^yn Cymru e-bost at holl Aelodau'r Cynulliad ynghylch yr ymgyrch P am 'Pobl' i godi ymwybyddiaeth o'r diffyg darpariaeth toiledau cyhoeddus yng Nghymru.",
                          "Atodwyd eu hymchwil ddiweddaraf er mwyn annog holl Aelodau'r Cynulliad i dynnu sylw Llywodraeth Cymru at y mater.",
                          'Byddwn yn ddiolchgar felly pe gallem gael datganiad gan Lywodraeth Cymru yn unol ^a hynny.']

# do the alignment experiment with the lecture sentences
print('Sentence Alignment Experiment Using Sentences From Lecture\n')
doSentenceAlignmentExperiment(sourceSentencesLecture, targetSentencesLecture)

print('\n')
print('-------------------------')

# do the sentence alignment experiment with the sents_source and sents_target info as input
print('Sentence Alignment Experiment Using sents_source.txta and sents_target.txt\n')
doSentenceAlignmentExperiment(sourceSentencesFile, targetSentencesFile)
