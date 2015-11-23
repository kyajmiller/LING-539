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
headerString = 'Sentence\tNumberOfWords'
outputFile.write(headerString)
