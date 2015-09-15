__author__ = 'Kya'

brownTagNoLines = open('browntag_nolines.txt', 'r')
brownTagNoLines = brownTagNoLines.read()

tokensPOSTagged = brownTagNoLines.split(' ')
wordsOnly = []
posTagsOnly = []

wordsFrequencyDict = {}
posTagsFrequencyDict = {}
wordsAndPOSTagFrequencyDict = {}

for token in tokensPOSTagged:
    splitWordPOS = token.split('_', 1)
    wordsOnly.append(splitWordPOS[0])
    posTagsOnly.append(splitWordPOS[1])

    if token not in wordsAndPOSTagFrequencyDict.iterkeys():
        wordsAndPOSTagFrequencyDict[token] = 1
    else:
        wordsAndPOSTagFrequencyDict[token] += 1

for word in wordsOnly:
    if word not in wordsFrequencyDict.iterkeys():
        wordsFrequencyDict[word] = 1
    else:
        wordsFrequencyDict[word] += 1

for posTag in posTagsOnly:
    if posTag not in posTagsFrequencyDict.iterkeys():
        posTagsFrequencyDict[posTag] = 1
    else:
        posTagsFrequencyDict[posTag] += 1

print(wordsFrequencyDict[0])
print(posTagsFrequencyDict[0])
print(wordsAndPOSTagFrequencyDict[0])
