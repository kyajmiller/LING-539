__author__ = 'Kya'
import q1a

sentsInFile = open('sents_in.txt', 'r')
sentsInData = sentsInFile.readlines()
sentsInData = [sentence.strip() for sentence in sentsInData]

wordsFrequencySortedList = q1a.makeWordsSortedList()
