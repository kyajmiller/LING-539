__author__ = 'Kya'
from collections import Counter

filein = open('browntag_nolines.txt', 'r')
brownTagNoLines = filein.read()
filein.close()

tagOutputFile = open('freqout_tag.txt', 'w')
wordOutputFile = open('freqout_word.txt', 'w')
taggedWordOutputFile = open('freqout_taggedword.txt', 'w')

wordsPOSTagged = brownTagNoLines.split(' ')
wordsOnlyList = []
posTagsOnlyList = []

for token in wordsPOSTagged:
    splitWordPOS = token.split('_', 1)
    wordsOnlyList.append(splitWordPOS[0])
    posTagsOnlyList.append(splitWordPOS[1])

wordsAndPOSTagFrequencyDict = Counter()

for wordAndPOSTag in wordsPOSTagged:
    wordsAndPOSTagFrequencyDict[wordAndPOSTag] += 1

wordsPOSTagsFrequencySorted = wordsAndPOSTagFrequencyDict.most_common()

for wordPOSTag in wordsPOSTagsFrequencySorted:


# for word in wordsPOSTagsFrequencySorted[:10]:
#    print word[0], '\t', word[1]

wordsFrequencyDict = Counter()
for word in wordsOnlyList:
    wordsFrequencyDict[word] += 1
wordsFrequencySorted = wordsFrequencyDict.most_common()
#print(wordsFrequencyDict)

posTagsFrequencyDict = Counter()
for posTag in posTagsOnlyList:
    posTagsFrequencyDict[posTag] += 1
posTagsFrequencySorted = posTagsFrequencyDict.most_common()
#print(posTagsFrequencyDict)
