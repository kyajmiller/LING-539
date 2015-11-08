"""
Kya Miller
LING 539 Assignment 4
Q1 - Simulates a simple Hidden Markov Model for a 4 word, 5 POS tag (state) language.
{w1, w2, w3, w4}, {t1, t2, t3, t4, t5}
Reads in example sentences from q1_in.txt and calculates the probabilities of those sentences using the forward
algorithm. The output is the sentence, the probability, and the runtime in the form of exhaustive cycles, forward
cycles, and the difference between them.

CyclesExhaustive = numStates^len(sentence)
CyclesForward = 2 * numStates^2 * len(sentence)

starting probabilities matrix
        t1      t2      t3      t4      t5
start   0.15    0.25    0.20    0.25    0.15

transitions matrix
    t1      t2      t3      t4      t5
t1  0.2     0.2     0.2     0.2     0.2
t2  0.1     0.15    0.5     0.15    0.1
t3  0.3     0.1     0.3     0.1     0.2
t4  0.4     0.05    0.1     0.4     0.05
t5  0.2     0.3     0.1     0.1     0.3

emissions matrix
    w1      w2      w3      w4
t1  0.25    0.25    0.25    0.25
t2  0.3     0.2     0.3     0.2
t3  0.3     0.1     0.3     0.3
t4  0.1     0.2     0.3     0.4
t5  0.2     0.3     0.2     0.3
"""
from __future__ import division
import math


def calculateSentenceProbabilityForwardAlgorithm(sentence):
    # uses the forward algorithm to calculate sentence probabilities

    # get sentence words
    words = sentence.split(' ')

    # declare array of totalStateProbabilities, which is the probability of the sentence up to the current word
    totalStateProbabilities = []

    # iterate through the words
    for i in range(len(words)):
        # array of current state probabilities
        currentStateProbabilities = []

        # get emissions matrix index for current word
        currentWord = words[i]
        currentWordEmissionsIndex = emissionsMappingDictionary[currentWord]

        # iterate through each state to get the probability of transitioning to that state and the emissions prob for
        # the current word in that state
        for j in range(len(states)):

            # if on the first word, the probability to the current state is the starting probability
            if i == 0:
                probabilityToBeInCurrentState = startingProbabilities[j]

            # otherwise, the probability to be in the current state is the sum of the products of the probabilities to
            # be in a given previous state times the probability of transitioning from that state to the current one
            else:
                probabilityToBeInCurrentState = sum(
                    totalStateProbabilities[k] * transitionsMatrix[k][j] for k in range(len(states)))

            # the current state probability is the probability to be in the current state times the emissions
            # probability for the current word
            currentStateProbabilities.append(
                emissionsMatrix[j][currentWordEmissionsIndex] * probabilityToBeInCurrentState)

        totalStateProbabilities = currentStateProbabilities

    # the sentence probability is the sum of the probabilities to be in the most recent state
    sentenceProb = sum(totalStateProbabilities)
    return sentenceProb


def calculateRunTime(sentence):
    # calculates the runtime of the HMM forward algorithm, returning the exhaustive number of cycles and the number of
    # cycles that the forward algorith does

    # get sentence words in order to get sentence length
    words = sentence.split(' ')
    sentenceLength = len(words)

    # get the number of states in the HMM
    numStates = len(states)

    # the exhaustive number of cycles is numStates^sentenceLength
    cyclesExhaustive = math.pow(numStates, sentenceLength)

    # the number of cycles for the forward algorithm is 2 * numStates^2 * sentenceLength
    cyclesForward = 2 * math.pow(numStates, 2) * sentenceLength

    # the time difference is the multiplicative difference between the cyclesExhaustive and the cyclesForward;
    # calculated as cylesExhaustive / cyclesForward
    timeDifference = cyclesExhaustive / cyclesForward

    return cyclesExhaustive, cyclesForward, timeDifference

# declare starting probabilities, transitions and emissions matrices
startingProbabilities = [0.15, 0.25, 0.2, 0.25, 0.15]

states = ['t1', 't2', 't3', 't4', 't5']

transitionsMatrix = [
    [0.2, 0.2, 0.2, 0.2, 0.2],
    [0.1, 0.15, 0.5, 0.15, 0.1],
    [0.3, 0.1, 0.3, 0.1, 0.2],
    [0.4, 0.05, 0.1, 0.4, 0.05],
    [0.2, 0.3, 0.1, 0.1, 0.3]
]

emissionsMatrix = [
    [0.25, 0.25, 0.25, 0.25],
    [0.3, 0.2, 0.3, 0.2],
    [0.3, 0.1, 0.3, 0.3],
    [0.1, 0.2, 0.3, 0.4],
    [0.2, 0.3, 0.2, 0.3]
]

# mapping dictionary from words to emissions matrix indices
emissionsMappingDictionary = {'w1': 0, 'w2': 1, 'w3': 2, 'w4': 3}

# read in q1_in.txt, get sentences, close file
fileIn = open('q1_in.txt', 'r')
sentences = fileIn.readlines()
fileIn.close()

tablesTitleString = 'prob\tcyclesExhaustive\tcyclesForward\ttimeDifference\tsentence\n\n'
print(tablesTitleString)

for sentence in sentences:
    sentence = sentence.strip()
    sentenceProb = calculateSentenceProbabilityForwardAlgorithm(sentence)
    cyclesExhaustive, cyclesForward, timeDifference = calculateRunTime(sentence)
    formattedString = '%s\t%s\t%s\t%sX\t%s\n' % (
        sentenceProb, cyclesExhaustive, cyclesForward, timeDifference, sentence)
    print(formattedString)
