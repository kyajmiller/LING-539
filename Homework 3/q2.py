"""
Kya Miller
LING 539 Assignment 3
Q2 - Simulates a simple Hidden Markov Model for a 3 word, 3 POS tag language. {w1, w2, w3}, {tag1, tag2, tag3}
Finds all possible 3 word sentences. Finds most probable tag sequence for each sentence.
Saves output and emission/transmission probabilities to hmm_output.txt.
"""

import itertools


def getAllSentences():
    # the words list needs to have w1 and w2 repeated after w3, or else itertools won't consider a combination where
    # w1 or w2 can appear after w3
    words = ['w1', 'w2', 'w3', 'w2', 'w1']
    allSentencesObject = itertools.combinations_with_replacement(words, 3)

    # however, because it still counts those repeated w1 and w2 as separate objects, you will get repeats. So filter
    # out the repeats.
    allSentencesFilteredList = []
    for sentence in allSentencesObject:
        if sentence not in allSentencesFilteredList:
            allSentencesFilteredList.append(sentence)

    return allSentencesFilteredList


def getAllPossiblePaths():
    # this works exactly the same as the getAllSentences function, just has a different list.
    states = ['tag1', 'tag2', 'tag3', 'tag2', 'tag1']
    allPathsObject = itertools.combinations_with_replacement(states, 3)

    allPathsFiltered = []
    for path in allPathsObject:
        if path not in allPathsFiltered:
            allPathsFiltered.append(path)

    return allPathsFiltered
