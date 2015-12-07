"""
Kya Miller
LING 539 Assignment 6 - Final Project
Q1 -
"""
from __future__ import division
import nltk
import re
import pickle
import loadTrec


def getData():
    filenameMessagePrefix = 'data\inmail.'
    emailTexts, vectors = loadTrec.loadMessages(filenameMessagePrefix, 3000)

    trainingEmails = emailTexts[:1000]
    trainingVectors = vectors[:1000]
    trainingData = [trainingEmails, trainingVectors]

    developmentEmails = emailTexts[1000:2000]
    developmentVectors = vectors[1000:2000]
    developmentData = [developmentEmails, developmentVectors]

    testingEmails = emailTexts[2000:]
    testingVectors = vectors[2000:]
    testingData = [testingEmails, testingVectors]

    return trainingData, developmentData, testingData


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
'''


def separateTrainingSpamFromHam(trainingEmails, trainingVectors, trainingLabels):
    spamEmails = []
    spamVectors = []

    hamEmails = []
    hamVectors = []

    for i in range(len(trainingEmails)):
        if trainingLabels[i] == loadTrec.SPAM_MESSAGE:
            spamEmails.append(trainingEmails[i])
            spamVectors.append(trainingVectors[i])
        else:
            hamEmails.append(trainingEmails[i])
            hamVectors.append(trainingVectors[i])

    spam = [spamEmails, spamVectors]
    ham = [hamEmails, hamVectors]

    return spam, ham


def calculateMaxCosineSimilarity(emailVector, spamHamVectors):
    cosineSimilarities = []
    for i in range(len(spamHamVectors)):
        cs = loadTrec.cosine(emailVector, spamHamVectors[i])
        cosineSimilarities.append(cs)
    return max(cosineSimilarities)


def cosineSimilarityToSpamMessages(emailVector):
    spamEmails, spamVectors = trainingSpam
    return calculateMaxCosineSimilarity(emailVector, spamVectors)


def cosineSimilarityToHamMessages(emailVector):
    hamEmails, hamVectors = trainingHam
    return calculateMaxCosineSimilarity(emailVector, hamVectors)


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


def createFeatureSet(emailText, vector):
    features = {}
    features['tooLongSequences'] = areThereReallyLongSequences(emailText)
    features['isAboutED'] = checkForErectileDysfunction(emailText)
    features['isAboutHealth'] = checkForHealth(emailText)
    features['isAboutMoney'] = checkForMoney(emailText)
    features['hasHTML'] = doesHTMLExist(emailText)
    features['cosineSimilarityToSpam'] = cosineSimilarityToSpamMessages(vector)
    features['cosineSimilarityToHam'] = cosineSimilarityToHamMessages(vector)
    return features


def trainNaiveBayesClassifier():
    trainingFeatures = [createFeatureSet(emailText, vector) for [emailText, vector] in
                        zip(trainingEmails, trainingVectors)]
    trainingSet = [(features, label) for features, label in zip(trainingFeatures, trainingLabels)]

    nbClassifier = nltk.NaiveBayesClassifier.train(trainingSet)

    classifierSaveFile = open('trainedNBClassifier', 'wb')
    pickle.dump(nbClassifier, classifierSaveFile)
    classifierSaveFile.close()


def loadSavedClassifier():
    classifierSaveFile = open('trainedNBClassifier', 'rb')
    nbClassifier = pickle.load(classifierSaveFile)
    classifierSaveFile.close()
    return nbClassifier


def displayMostInformativeFeatures(howmany=None):
    nbClassifier = loadSavedClassifier()
    if howmany:
        nbClassifier.show_most_informative_features(howmany)
    else:
        nbClassifier.show_most_informative_features()


def testNBClassifier(evaluationData, evaluationLabels):
    emails, vectors = evaluationData
    evaluationFeaturesLists = [createFeatureSet(emailText, vector) for [emailText, vector] in zip(emails, vectors)]
    evaluationSet = [(features, label) for features, label in zip(evaluationFeaturesLists, evaluationLabels)]

    nbClassifier = loadSavedClassifier()
    classifierAccuracy = nltk.classify.accuracy(nbClassifier, evaluationSet)
    predictedLabels = [nbClassifier.classify(featureSet) for featureSet in evaluationFeaturesLists]

    totalGoldSpam = 0
    totalGoldHam = 0
    totalPredictedSpam = 0
    totalPredictedHam = 0
    spamAsSpam = 0
    spamAsHam = 0
    hamAsHam = 0
    hamAsSpam = 0

    for predicted, gold in zip(predictedLabels, evaluationLabels):
        # check if things that should have been labeled spam...
        if gold == loadTrec.SPAM_MESSAGE:
            totalGoldSpam += 1
            # are correctly labeled spam
            if predicted == loadTrec.SPAM_MESSAGE == gold:
                spamAsSpam += 1
                totalPredictedSpam += 1
            # or incorrectly labeled ham
            elif predicted == loadTrec.NORMAL_MESSAGE:
                spamAsHam += 1
                totalPredictedHam += 1
        # check if things that should have been labeled ham...
        elif gold == loadTrec.NORMAL_MESSAGE:
            totalGoldHam += 1
            # are correctly labeled ham
            if predicted == loadTrec.NORMAL_MESSAGE == gold:
                hamAsHam += 1
                totalPredictedHam += 1
            # or incorrectly labeled spam
            elif predicted == loadTrec.SPAM_MESSAGE:
                hamAsSpam += 1
                totalPredictedSpam += 1

    trueSpamPercentage = spamAsSpam / totalPredictedSpam * 100
    falseSpamPercentage = hamAsSpam / totalPredictedSpam * 100
    falseHamPercentage = spamAsHam / totalPredictedHam * 100
    trueHamPercentage = hamAsHam / totalPredictedHam * 100

    print 'Classified as Spam\t%s (%.2f)\t%s (%.2f)\t%s' % (
    spamAsSpam, trueSpamPercentage, hamAsSpam, falseSpamPercentage, totalPredictedSpam)
    print 'Classified as Ham\t%s (%.2f)\t%s (%.2f)\t%s' % (
    spamAsSpam, falseHamPercentage, hamAsHam, trueHamPercentage, totalPredictedHam)
    print 'Total accuracy: %.2f' % classifierAccuracy



trainingLabels, developmentLabels, testingLabels = getGoldLabels()
trainingData, developmentData, testingData = getData()
trainingEmails, trainingVectors = trainingData
trainingSpam, trainingHam = separateTrainingSpamFromHam(trainingData[0], trainingData[1], trainingLabels)

# trainNaiveBayesClassifier()

print('\n')
print('Performance on dev.\tTrue Spam\tTrue Normal\tTotal')
testNBClassifier(developmentData, developmentLabels)

print('Performance on test\tTrue Spam\tTrue Normal\tTotal')
testNBClassifier(testingData, testingLabels)
