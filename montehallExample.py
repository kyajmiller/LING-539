__author__ = 'Kya'
from random import randint

#Global Constraints
GoatDoorInit = 0
WinningDoorInit = 1
OpenDoorInit = 2

def initWinningDoor():
    doorValues = [GoatDoorInit] * 3
    winningDoor = randint(0,2)
    doorValues[winningDoor] = WinningDoorInit
    return doorValues

def chooseDoor():
    return randint(0,2)

def openNonWinningDoor(doorValues, chosenDoor):
    randIdx = randint(0,2)
    done = 0
    while (done == 0):
        if randIdx != chosenDoor and doorValues[randIdx] == GoatDoorInit:
            done = 1
        else:
            randIdx = randint(0,2)

    return randIdx

def doSwitch(chosenDoor, openedDoor):
    available = 1
    unavailable = -1
    doors = [available] * 3
    doors[chosenDoor] = unavailable
    doors[openedDoor] = unavailable

    for i in range(0, 3):
        if doors[i] == available:
            return i

def isCorrect(doorValues, chosenDoor):
    if doorValues[chosenDoor] == WinningDoorInit:
        return 1
    else:
        return 0

def doExperimentNormal(numIterations):
    numCorrect = 0

    for i in range(0, numIterations):
        doorValues = initWinningDoor()
        chosenDoor = chooseDoor()
        openDoor = openNonWinningDoor(doorValues, chosenDoor)

        score = isCorrect(doorValues, chosenDoor)
        numCorrect = numCorrect + score

        if score == 1:
            print("Win!")
        else:
            print("Lose!")

    finalScore = (float(numCorrect) / float(numIterations)) * 100

    return finalScore


def doExperimentSwitch(numIterations):
    numCorrect = 0

    for i in range(0, numIterations):
        doorValues = initWinningDoor()
        chosenDoor = chooseDoor()
        openDoor = openNonWinningDoor(doorValues, chosenDoor)
        switchDoor = doSwitch(chosenDoor, openDoor)

        score = isCorrect(doorValues, switchDoor)
        numCorrect = numCorrect + score

        if score == 1:
            print("Win!")
        else:
            print("Lose!")

    finalScore = (float(numCorrect) / float(numIterations)) * 100

    return finalScore

#Main Program
n = 10000
finalScoreNormal = doExperimentNormal(n)
finalScoreSwitch = doExperimentSwitch(n)

print("Final Score after %s iterations normal: %s" % (n, finalScoreNormal))

print("Final Score after %s iterations experiment: %s" % (n, finalScoreSwitch))
