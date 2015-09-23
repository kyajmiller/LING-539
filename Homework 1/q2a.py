"""
Kya Miller
LING 539 Assignment 1
Q2A - Stimulates the Monty Hall problem; when run, shows the results of a stimulation for n = 10,000 samples.
"""

from __future__ import division
import random


class MonteHall(object):
    def __init__(self, numIterations):
        self.BadDoor = 0
        self.WinningDoor = 1

        self.numIterations = numIterations

        finalScoreNormal = self.RunExperimentNoSwitch()
        finalScoreSwitch = self.RunExperimentSwitch()

        print("Final Score after %s iterations with no switching: %s" % (self.numIterations, finalScoreNormal))

        print("Final Score after %s iterations with switching: %s" % (self.numIterations, finalScoreSwitch))

    def InitializeDoorValues(self):
        doorValues = [self.BadDoor] * 3
        randomWinningDoor = random.randint(0, 2)
        doorValues[randomWinningDoor] = self.WinningDoor
        return doorValues

    def ChooseDoor(self):
        return random.randint(0, 2)

    def OpenBadDoor(self, doorValues, chosenDoor):
        randomDoor = random.randint(0, 2)
        done = False
        while not done:
            if randomDoor != chosenDoor and doorValues[randomDoor] == self.BadDoor:
                done = True
            else:
                randomDoor = random.randint(0, 2)

        return randomDoor

    def SwitchDoors(self, chosenDoor, openedDoor):
        available = True
        unavailable = False
        doors = [available] * 3
        doors[chosenDoor] = unavailable
        doors[openedDoor] = unavailable

        for i in range(0, 3):
            if doors[i]:
                return i

    def CheckIfWinningDoor(self, doorValues, chosenDoor):
        if doorValues[chosenDoor] == self.WinningDoor:
            return True
        else:
            return False

    def RunExperimentNoSwitch(self):
        numCorrect = 0

        for i in range(0, self.numIterations):
            doorValues = self.InitializeDoorValues()
            chosenDoor = self.ChooseDoor()

            if self.CheckIfWinningDoor(doorValues, chosenDoor):
                numCorrect += 1

        finalScore = (float(numCorrect) / float(self.numIterations)) * 100

        return finalScore

    def RunExperimentSwitch(self):
        numCorrect = 0

        for i in range(0, self.numIterations):
            doorValues = self.InitializeDoorValues()
            chosenDoor = self.ChooseDoor()
            openDoor = self.OpenBadDoor(doorValues, chosenDoor)
            switchDoor = self.SwitchDoors(chosenDoor, openDoor)

            if self.CheckIfWinningDoor(doorValues, switchDoor):
                numCorrect += 1

        finalScore = (float(numCorrect) / float(self.numIterations)) * 100

        return finalScore


MonteHall(10000)
