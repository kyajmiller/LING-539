"""
Kya Miller
LING 539 Assignment 1
Q1B - Reading in sentences from sents_in.txt, prints to console the probabilities of those sentences given the word
probabilities from the browntag corpus
"""

from __future__ import division
import q1a


def doSentenceProbability(sentence):
    sentenceWords = sentence.split(' ')
    sentenceProb = 1
    wordsNotInCorpus = []
    for word in sentenceWords:
        if word in wordsProbabilitiesDict.iterkeys():
            sentenceProb = sentenceProb * wordsProbabilitiesDict[word]
        else:
            wordsNotInCorpus.append(word)
            sentenceProb = 0

    print "Sentence: %s; Probability: %s" % (sentence, sentenceProb)
    if sentenceProb == 0:
        print "\tWord(s) not found: %s" % ' ,'.join(wordsNotInCorpus)

sentsInFile = open('sents_in.txt', 'r')
sentsInData = sentsInFile.readlines()
sentsInFile.close()

sentsInData = [sentence.strip() for sentence in sentsInData]

wordsFrequencySortedList = q1a.makeWordsSortedList()

totalWords = 0
for word in wordsFrequencySortedList:
    totalWords += word[1]

wordsProbabilitiesDict = {word[0]: word[1] / totalWords for word in wordsFrequencySortedList}
wordsList = [word[0] for word in wordsFrequencySortedList]

for sentence in sentsInData:
    doSentenceProbability(sentence)
