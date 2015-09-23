"""
Kya Miller
LING 539 Assignment 1
Q2A - Modifies the MonteHall simulation from Q2A to take arguments for the number of total doors and the number of doors
opened for the switching experiment. Runs simulations for 3-10 total doors and 2-5 opened doors, returns probabilities
in a fancy table.
"""

from __future__ import division
import random


class MonteHall(object):
    def __init__(self, numIterations, numTotalDoors, numOpenedDoors):
        self.BadDoor = 0
        self.WinningDoor = 1

        self.numIterations = numIterations
        self.numTotalDoors = numTotalDoors
        self.numOpenedDoors = numOpenedDoors

        # finalScoreNormal = self.RunExperimentNoSwitch()
        # finalScoreSwitch = self.RunExperimentSwitch()

        # print("Final Score after %s iterations with no switching: %s" % (self.numIterations, finalScoreNormal))

        # print("Final Score after %s iterations with switching: %s" % (self.numIterations, finalScoreSwitch))

    def InitializeDoorValues(self):
        doorValues = [self.BadDoor] * self.numTotalDoors
        randomWinningDoor = random.randint(0, self.numTotalDoors - 1)
        doorValues[randomWinningDoor] = self.WinningDoor
        return doorValues

    def ChooseDoor(self):
        return random.randint(0, self.numTotalDoors - 1)

    def OpenBadDoors(self, doorValues, chosenDoor):
        openedDoorsList = []
        for i in range(0, self.numOpenedDoors):
            randomDoor = random.randint(0, self.numTotalDoors - 1)
            done = False
            while not done:
                if randomDoor != chosenDoor and doorValues[
                    randomDoor] == self.BadDoor and randomDoor not in openedDoorsList:
                    done = True
                else:
                    randomDoor = random.randint(0, self.numTotalDoors - 1)

            openedDoorsList.append(randomDoor)

        return openedDoorsList

    def SwitchDoors(self, chosenDoor, openedDoorsList):
        available = True
        unavailable = False
        doors = [available] * self.numTotalDoors
        doors[chosenDoor] = unavailable
        for openedDoor in openedDoorsList:
            doors[openedDoor] = unavailable

        for i in range(0, self.numTotalDoors):
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

        print("Final Score for non-switching experiment after %s iterations with %s total doors: %s" % (
            self.numIterations, self.numTotalDoors, finalScore))

        # return finalScore

    def RunExperimentSwitch(self):
        numCorrect = 0

        if self.numOpenedDoors <= self.numTotalDoors - 2:
            for i in range(0, self.numIterations):
                doorValues = self.InitializeDoorValues()
                chosenDoor = self.ChooseDoor()
                openDoorsList = self.OpenBadDoors(doorValues, chosenDoor)
                switchDoor = self.SwitchDoors(chosenDoor, openDoorsList)

                if self.CheckIfWinningDoor(doorValues, switchDoor):
                    numCorrect += 1
        else:
            print("Not enough total doors to support the number of opened doors.")

        finalScore = (float(numCorrect) / float(self.numIterations)) * 100

        print("Final Score for switching experiment after %s iterations with %s total doors and %s opened doors: %s" % (
            self.numIterations, self.numTotalDoors, self.numOpenedDoors, finalScore))

        # return finalScore


MonteHall(10000, 4, 2).RunExperimentNoSwitch()
MonteHall(10000, 4, 2).RunExperimentSwitch()
