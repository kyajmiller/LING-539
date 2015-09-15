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

wordsPOSTagsFrequencyDict = Counter()
for wordPOSTag in wordsPOSTagged:
    wordsPOSTagsFrequencyDict[wordPOSTag] += 1
wordsPOSTagsFrequencySorted = wordsPOSTagsFrequencyDict.most_common()

for taggedWord in wordsPOSTagsFrequencySorted:
    formattedString = '%s \t %s \n' % (taggedWord[0], taggedWord[1])
    taggedWordOutputFile.write(formattedString)

wordsFrequencyDict = Counter()
for word in wordsOnlyList:
    wordsFrequencyDict[word] += 1
wordsFrequencySorted = wordsFrequencyDict.most_common()

for word in wordsFrequencySorted:
    formattedString = '%s \t %s \n' % (word[0], word[1])
    wordOutputFile.write(formattedString)

posTagsFrequencyDict = Counter()
for posTag in posTagsOnlyList:
    posTagsFrequencyDict[posTag] += 1
posTagsFrequencySorted = posTagsFrequencyDict.most_common()

for posTag in posTagsFrequencySorted:
    formattedString = '%s \t %s \n' % (posTag[0], posTag[1])
    tagOutputFile.write(formattedString)
