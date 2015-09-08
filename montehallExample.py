__author__ = 'Kya'
from random import randint

class MonteHall(object):
    def __init__(self, numIterations):
        self.GoatDoorInit = 0
        self.WinningDoorInit = 1
        self.OpenDoorInit = 2

        self.numIterations = numIterations

        finalScoreNormal = self.doExperimentNormal()
        finalScoreSwitch = self.doExperimentSwitch()

        print("Final Score after %s iterations normal: %s" % (self.numIterations, finalScoreNormal))

        print("Final Score after %s iterations experiment: %s" % (self.numIterations, finalScoreSwitch))

    def initWinningDoor(self):
        doorValues = [self.GoatDoorInit] * 3
        winningDoor = randint(0,2)
        doorValues[winningDoor] = self.WinningDoorInit
        return doorValues

    def chooseDoor(self):
        return randint(0,2)

    def openNonWinningDoor(self, doorValues, chosenDoor):
        randIdx = randint(0,2)
        done = 0
        while (done == 0):
            if randIdx != chosenDoor and doorValues[randIdx] == self.GoatDoorInit:
                done = 1
            else:
                randIdx = randint(0,2)

        return randIdx

    def doSwitch(self, chosenDoor, openedDoor):
        available = 1
        unavailable = -1
        doors = [available] * 3
        doors[chosenDoor] = unavailable
        doors[openedDoor] = unavailable

        for i in range(0, 3):
            if doors[i] == available:
                return i

    def isCorrect(self, doorValues, chosenDoor):
        if doorValues[chosenDoor] == self.WinningDoorInit:
            return 1
        else:
            return 0

    def doExperimentNormal(self):
        numCorrect = 0

        for i in range(0, self.numIterations):
            doorValues = self.initWinningDoor()
            chosenDoor = self.chooseDoor()
            openDoor = self.openNonWinningDoor(doorValues, chosenDoor)

            score = self.isCorrect(doorValues, chosenDoor)
            numCorrect = numCorrect + score

            if score == 1:
                print("Win!")
            else:
                print("Lose!")

        finalScore = (float(numCorrect) / float(self.numIterations)) * 100

        return finalScore


    def doExperimentSwitch(self):
        numCorrect = 0

        for i in range(0, self.numIterations):
            doorValues = self.initWinningDoor()
            chosenDoor = self.chooseDoor()
            openDoor = self.openNonWinningDoor(doorValues, chosenDoor)
            switchDoor = self.doSwitch(chosenDoor, openDoor)

            score = self.isCorrect(doorValues, switchDoor)
            numCorrect = numCorrect + score

            if score == 1:
                print("Win!")
            else:
                print("Lose!")

        finalScore = (float(numCorrect) / float(self.numIterations)) * 100

        return finalScore

MonteHall(10000)

