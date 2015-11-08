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


def calculateSentenceProbability(sentence):
    words = sentence.split(' ')

# declare starting probabilities, transitions and emissions matrices
startingProbabilities = [0.15, 0.25, 0.2, 0.25, 0.15]

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

# dictionaries for matrix indices
transitionsMappingDictionary = {'t1': 0, 't2': 1, 't3': 2, 't4': 3, 't5': 4}
emissionsMappingDictionary = {'t1': 0, 't2': 1, 't3': 2, 't4': 3, 't5': 4, 'w1': 0, 'w2': 1, 'w3': 2, 'w4': 3}

# read in q1_in.txt, get sentences, close file
fileIn = open('q1_in.txt', 'r')
sentences = fileIn.readlines()
fileIn.close()

for sentence in sentences:
    calculateSentenceProbability(sentence)
