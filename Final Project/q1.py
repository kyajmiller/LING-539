"""
Kya Miller
LING 539 Assignment 6 - Final Project
Q1 -
"""
import nltk
import re
import pickle
import loadTrec


def getData():
    pass


def getGoldLabels():
    filenameIndex = 'index.txt'
    goldLabels = loadTrec.loadGoldIndex(filenameIndex, 3000)
    trainingLabels = goldLabels[:1000]
    developmentLabels = goldLabels[1000:2000]
    testingLabels = goldLabels[2000:]
    return trainingLabels, developmentLabels, testingLabels


'''
def getGoldLabels():
    goldDataFileIn = open('goldData/index.txt', 'r')
    goldDataLines = goldDataFileIn.readlines()
    goldDataFileIn.close()

    goldDataLabels = []
    for line in goldDataLines[:3000]:
        splitLine = line.split(' ', 1)
        label = splitLine[0].lower()
        goldDataLabels.append(label)

    trainingGoldLabels = goldDataLabels[:1000]
    developmentGoldLabels = goldDataLabels[1000:2000]
    testingGoldLabels = goldDataLabels[2000:3000]

    return trainingGoldLabels, developmentGoldLabels, testingGoldLabels
'''


def getEmailText(emailLines):
    emailText = ''
    done = False
    while not done:
        for i in range(len(emailLines)):
            if emailLines[i].startswith('Lines:'):
                emailText = ' '.join(emailLines[i + 1:])
                done = True
    return emailText


def getTrainingData(trainingLabels):
    trainingData = []
    for i in range(1000):
        trainingEmailFileIn = open('trainingData/inmail.%s' % (i + 1), 'r')
        trainingEmailLines = trainingEmailFileIn.readlines()
        trainingEmailFileIn.close()
        trainingData.append([getEmailText(trainingEmailLines), trainingLabels[i]])
    return trainingData


def getDevelopmentData(developmentLabels):
    developmentData = []
    startNumber = 1000
    for i in range(1000):
        developmentEmailFileIn = open('developmentData/inmail.%s' % (startNumber + i + 1), 'r')
        developmentEmailLines = developmentEmailFileIn.readlines()
        developmentEmailFileIn.close()
        developmentData.append([getEmailText(developmentEmailLines), developmentLabels[i]])
    return developmentData


def getTestingData(testingLabels):
    testingData = []
    startNumber = 2000
    for i in range(1000):
        testingEmailFileIn = open('testingData/inmail.%s' % (startNumber + i + 1), 'r')
        testingEmailLines = testingEmailFileIn.readlines()
        testingEmailFileIn.close()
        testingData.append([getEmailText(testingEmailLines), testingLabels[i]])
    return testingData


def doesHTMLExist(emailText):
    if re.search('<html>', emailText.lower()):
        return True
    else:
        return False


def areThereReallyLongSequences(emailText):
    # checks for emails that have super long sequences of jumbled text. Simply checks for the existence of 'words' with
    # a length longer than 50 characters
    words = emailText.split(' ')
    tooLong = False
    for word in words:
        if len(word) > 50:
            if 'http' not in word:
                tooLong = True
    return tooLong


def checkForErectileDysfunction(emailText):
    # check for words involving erectile dysfunction
    edWords = ['viagra', 'cialis', 'levitra', 'v i a g r a', 'c i a l i s', 'l e v i t r a', 'manhood', 'small', 'area',
               'perform', 'inches', 'pill', 'length', 'big', 'libido', 'orgasm', 'fix', 'drug']
    edCounter = 0
    for word in edWords:
        if re.findall(word, emailText.lower()):
            edCounter += len(re.findall(word, emailText.lower()))

    return edCounter


def checkForHealth(emailText):
    # check for words involving weight loss
    weightLossOrHealthWords = ['fat', 'fit', 'weight', 'food', 'loss', 'growing', 'pound', 'kilo', 'health', 'eat',
                               'ate', 'overweight', 'slender', 'energy', 'lose', 'pill', 'anti-aging', 'youth',
                               'prescription', 'drug', 'quality', 'stimulate', 'hormone', 'appetite', 'natural',
                               'losing', 'substance']
    healthCounter = 0
    for word in weightLossOrHealthWords:
        if re.findall(word, emailText.lower()):
            healthCounter += len(re.findall(word, emailText.lower()))

    return healthCounter


def checkForMoney(emailText):
    # check for words involving money or ordering things or money scams
    moneyWords = ['money', 'order', 'buy', 'dollar', 'today', 'transaction', 'commission', 'earn', 'cash', 'payment',
                  'bank', 'receipt', 'work', 'work from home', 'capital', 'pay', 'ship', 'cheap', 'discount', 'price',
                  'delivery', 'refinance', 'property', 'finance']
    moneyCounter = 0
    for word in moneyWords:
        if re.findall(word, emailText.lower()):
            moneyCounter += len(re.findall(word, emailText.lower()))

    return moneyCounter


def createFeatureSet(emailText):
    features = {}
    features['HTML'] = doesHTMLExist(emailText)
    features['tooLongSequences'] = areThereReallyLongSequences(emailText)
    features['isAboutED'] = checkForErectileDysfunction(emailText)
    features['isAboutHealth'] = checkForHealth(emailText)
    features['isAboutMoney'] = checkForMoney(emailText)
    return features


def trainNaiveBayesClassifier(trainingData):
    nbClassifier = nltk.NaiveBayesClassifier.train(trainingData)
    classifierSaveFile = open('trainedNBClassifier', 'wb')
    pickle.dump(nbClassifier, classifierSaveFile)
    classifierSaveFile.close()


def loadSavedClassifier():
    classifierSaveFile = open('trainedNBClassifier', 'rb')
    nbClassifier = pickle.load(classifierSaveFile)
    classifierSaveFile.close()
    return nbClassifier


def testNBClassifier(evaluationData):
    nbClassifier = loadSavedClassifier()
    classifierAccuracy = nltk.classify.accuracy(nbClassifier, evaluationData)
    return classifierAccuracy


# trainingLabels, developmentLabels, testingLabels = getGoldLabels()
trainingLabels, developmentLabels, testingLabels = getGoldLabels()
'''
trainingData = getTrainingData(trainingLabels)
trainingData = [(createFeatureSet(emailText), label) for [emailText, label] in trainingData]
developmentData = getDevelopmentData(developmentLabels)
developmentData = [(createFeatureSet(emailText), label) for [emailText, label] in developmentData]
testingData = getTestingData(testingLabels)
testingData = [(createFeatureSet(emailText), label) for [emailText, label] in testingData]

trainNaiveBayesClassifier(trainingData)
classifierAccuracyOnDevelopmentData = testNBClassifier(developmentData)
print classifierAccuracyOnDevelopmentData
'''
