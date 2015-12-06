"""
Kya Miller
LING 539 Assignment 6 - Final Project
Q1 -
"""
import nltk
import re


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
    if re.search('<HTML>', emailText):
        return True
    else:
        return False


def hasTooLongSequences(emailText):
    # checks for emails that have super long sequences of jumbled text. Simply checks for the existence of 'words' with
    # a length longer than 50 characters
    words = ' '.split(emailText)
    tooLong = False
    for word in words:
        if len(word) > 50:
            tooLong = True
    return tooLong


def createFeatureSet(emailText):
    features = {}
    features['has_HTML'] = doesHTMLExist(emailText)
    features['has_tooLongSequences'] = hasTooLongSequences(emailText)
    return features


trainingLabels, developmentLabels, testingLabels = getGoldLabels()
trainingData = getTrainingData(trainingLabels)
trainingData = [[createFeatureSet(emailText), label] for [emailText, label] in trainingData]
for features, label in trainingData:
    print features, label
developmentData = getDevelopmentData(developmentLabels)
testingData = getTestingData(testingLabels)
