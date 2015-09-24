"""
Kya Miller
LING 539 Assignment 1
Q2C - Modifies the MonteHall simulation from Q2A to take arguments for the number of total doors and the number of doors
opened for the switching experiment. Runs simulations for 3-10 total doors and 2-5 opened doors, returns probabilities
in a fancy table. Further modified from Q2B to have two winning doors instead of just one.
"""

from __future__ import division
import random
from prettytable import PrettyTable


class MonteHall(object):
    def __init__(self, numIterations, numTotalDoors, numOpenedDoors):
        self.BadDoor = 0
        self.WinningDoor = 1

        self.numIterations = numIterations
        self.numTotalDoors = numTotalDoors
        self.numOpenedDoors = numOpenedDoors

    def InitializeDoorValues(self):
        doorValues = [self.BadDoor] * self.numTotalDoors
        randomWinningDoor1 = random.randint(0, self.numTotalDoors - 1)
        randomWinningDoor2 = random.randint(0, self.numTotalDoors - 1)
        done = False
        while not done:
            if randomWinningDoor2 != randomWinningDoor1:
                done = True
            else:
                randomWinningDoor2 = random.randint(0, self.numTotalDoors - 1)
        doorValues[randomWinningDoor1] = self.WinningDoor
        doorValues[randomWinningDoor2] = self.WinningDoor
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

        finalScore = (numCorrect / self.numIterations) * 100

        return finalScore

    def RunExperimentSwitch(self):
        if self.numOpenedDoors <= self.numTotalDoors - 3:
            numCorrect = 0

            for i in range(0, self.numIterations):
                doorValues = self.InitializeDoorValues()
                chosenDoor = self.ChooseDoor()
                openDoorsList = self.OpenBadDoors(doorValues, chosenDoor)
                switchDoor = self.SwitchDoors(chosenDoor, openDoorsList)

                if self.CheckIfWinningDoor(doorValues, switchDoor):
                    numCorrect += 1

            finalScore = (numCorrect / self.numIterations) * 100
            return finalScore
        elif self.numOpenedDoors == self.numTotalDoors - 2:
            return '100.00'
        else:
            return '//'


def RunNonSwitchingExperiments():
    noSwitchTable = PrettyTable(['k', '3', '4', '5', '6', '7', '8', '9', '10'])
    noSwitchTable.add_row(
        ['', MonteHall(10000, 3, 2).RunExperimentNoSwitch(), MonteHall(10000, 4, 2).RunExperimentNoSwitch(),
         MonteHall(10000, 5, 2).RunExperimentNoSwitch(), MonteHall(10000, 6, 2).RunExperimentNoSwitch(),
         MonteHall(10000, 7, 2).RunExperimentNoSwitch(), MonteHall(10000, 8, 2).RunExperimentNoSwitch(),
         MonteHall(10000, 9, 2).RunExperimentNoSwitch(), MonteHall(10000, 10, 2).RunExperimentNoSwitch()])

    print("Results for NonSwitching Experiments after 10,000 iterations:")
    print noSwitchTable


def RunSwitchingExperiments():
    switchTable = PrettyTable(['s, k', '3', '4', '5', '6', '7', '8', '9', '10'])
    switchTable.add_row(
        ['2', MonteHall(10000, 3, 2).RunExperimentSwitch(), MonteHall(10000, 4, 2).RunExperimentSwitch(),
         MonteHall(10000, 5, 2).RunExperimentSwitch(), MonteHall(10000, 6, 2).RunExperimentSwitch(),
         MonteHall(10000, 7, 2).RunExperimentSwitch(), MonteHall(10000, 8, 2).RunExperimentSwitch(),
         MonteHall(10000, 9, 2).RunExperimentSwitch(), MonteHall(10000, 10, 2).RunExperimentSwitch()])
    switchTable.add_row(
        ['3', MonteHall(10000, 3, 3).RunExperimentSwitch(), MonteHall(10000, 4, 3).RunExperimentSwitch(),
         MonteHall(10000, 5, 3).RunExperimentSwitch(), MonteHall(10000, 6, 3).RunExperimentSwitch(),
         MonteHall(10000, 7, 3).RunExperimentSwitch(), MonteHall(10000, 8, 3).RunExperimentSwitch(),
         MonteHall(10000, 9, 3).RunExperimentSwitch(), MonteHall(10000, 10, 3).RunExperimentSwitch()])
    switchTable.add_row(
        ['4', MonteHall(10000, 3, 4).RunExperimentSwitch(), MonteHall(10000, 4, 4).RunExperimentSwitch(),
         MonteHall(10000, 5, 4).RunExperimentSwitch(), MonteHall(10000, 6, 4).RunExperimentSwitch(),
         MonteHall(10000, 7, 4).RunExperimentSwitch(), MonteHall(10000, 8, 4).RunExperimentSwitch(),
         MonteHall(10000, 9, 4).RunExperimentSwitch(), MonteHall(10000, 10, 4).RunExperimentSwitch()])
    switchTable.add_row(
        ['5', MonteHall(10000, 3, 5).RunExperimentSwitch(), MonteHall(10000, 4, 5).RunExperimentSwitch(),
         MonteHall(10000, 5, 5).RunExperimentSwitch(), MonteHall(10000, 6, 5).RunExperimentSwitch(),
         MonteHall(10000, 7, 5).RunExperimentSwitch(), MonteHall(10000, 8, 5).RunExperimentSwitch(),
         MonteHall(10000, 9, 5).RunExperimentSwitch(), MonteHall(10000, 10, 5).RunExperimentSwitch()])

    print("Results for Switching Experiments after 10,000 iterations:")
    print switchTable


RunNonSwitchingExperiments()
print("\n")
RunSwitchingExperiments()
