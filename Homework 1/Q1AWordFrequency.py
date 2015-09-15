__author__ = 'Kya'
from collections import Counter

brownTagNoLines = open('browntag_nolines.txt', 'r')
brownTagNoLines = brownTagNoLines.read()

wordsPOSTagged = brownTagNoLines.split(' ')
wordsOnlyList = []
posTagsOnlyList = []
wordsAndPOSTagsList = []

for token in wordsPOSTagged:
    splitWordPOS = token.split('_', 1)
    wordsOnlyList.append(splitWordPOS[0])
    posTagsOnlyList.append(splitWordPOS[1])

wordsAndPOSTagFrequencyDict = Counter()
for wordAndPOSTag in wordsPOSTagged:
    wordsAndPOSTagFrequencyDict[wordAndPOSTag] += 1
wordsPOSTagsFrequencySorted = wordsAndPOSTagFrequencyDict.most_common()
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
