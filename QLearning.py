import numpy as np
import random
import raceTrack

class QLearning:
    def __init__(self, rTrack):
        self.track = rTrack
        self.raceTrack = self.track.getTrack()
        self.actions = [(0,0), (0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,1), (1,-1), (-1,-1)]
        self.qTable = np.zeros((rTrack.getXSize(),rTrack.getYsize(), len(self.actions)))
        self.velocity = [0,0]
        self.restart = False
        self.cost = 0
        self.startLocations = self.getStart()
        self.crossed = False
        self.totalCost = 0

    def getStart(self):
        startLocations = []
        for x in range(len(self.raceTrack)):
                for y in range(len(self.raceTrack[x])):
                    for val in self.raceTrack[x][y]:
                        if val == 'S':
                            startLocations.append((x,y))
        return startLocations

    def updateQ(self, action, x, y, alpha, gamma, newX, newY, newA, reward):
        self.qTable[x][y][self.actions.index(action)] = self.qTable[x][y][self.actions.index(action)] + \
                                                        alpha*(reward + gamma*self.qTable[newX][newY][self.actions.index(newA)] -
                                                               self.qTable[x][y][self.actions.index(action)])

    def applyAction(self, x, y, selectedAction):
        newLocation = [x,y]
        if random.uniform(0,1) < 0.2:
            for x in range(abs(self.velocity[0])):
                newLocation[0]+= 1*np.sign(self.velocity[0])
                isvalid = self.track.racerPosition(newLocation[0], newLocation[1])
                if isvalid == "Finished Track":
                    self.crossed = True
                if isvalid == "Hit Wall":
                    if self.restart:
                        self.track.restartRace()
                        return self.getStart()
                    else:
                        newLocation[0]-=1 * np.sign(self.velocity[0])
                        self.velocity = (0,0)
                        return newLocation
            for y in range(abs(self.velocity[1])):
                newLocation[1] += 1 * np.sign(self.velocity[1])
                isvalid = self.track.racerPosition(newLocation[0], newLocation[1])
                if isvalid == "Finished Track":
                    self.crossed = True
                if isvalid == "Hit Wall":
                    if self.restart:
                        self.track.restartRace()
                        return self.getStart()
                    else:
                        newLocation[1] -= 1 * np.sign(self.velocity[1])
                        self.velocity = (0,0)
                        return newLocation
        else:
            self.velocity = [self.velocity[0]+ selectedAction[0], self.velocity[1]+ selectedAction[1]]
            for v in range(2):
                if self.velocity[v] > 5:
                    self.velocity[v] = 5
                elif self.velocity[v] < -5:
                    self.velocity[v] = 5
            for x in range(abs(self.velocity[0])):
                newLocation[0] += 1*np.sign(self.velocity[0])
                isvalid = self.track.racerPosition(newLocation[0], newLocation[1])
                if isvalid == "Finished Track":
                    self.crossed = True
                if isvalid == "Hit Wall":
                    if self.restart:
                        self.track.restartRace()
                        return self.getStart()
                    else:
                        newLocation[0] -= 1*np.sign(self.velocity[0])
                        self.velocity = (0, 0)
                        return newLocation
            for y in range(abs(self.velocity[1])):
                newLocation[1] += 1 * np.sign(self.velocity[1])
                isvalid = self.track.racerPosition(newLocation[0], newLocation[1])
                if isvalid == "Finished Track":
                    self.crossed = True
                if isvalid == "Hit Wall":
                    if self.restart:
                        self.track.restartRace()
                        return self.getStart()
                    else:
                        newLocation[1] -= 1 * np.sign(self.velocity[1])
                        self.velocity = [0, 0]
                        return newLocation
        return newLocation

    def reward(self):
        if self.crossed:
            return 0
        else:
            self.totalCost += 1
            return -1

    def selectAction(self, x, y):
        if random.uniform(0, 1) < 0.2:
            return self.actions[random.choice(range(len(self.actions)))]
        else:
            return self.actions[self.qTable[x][y].argmax()]

    def qLearning(self, runs):
        for i in range(runs):
            location = random.choice(self.startLocations)
            a = self.selectAction(location[0], location[1])
            while not self.crossed:
                newLocation = self.applyAction(location[0], location[1], a)
                newA = self.selectAction(location[0], location[1])
                reward = self.reward()
                self.updateQ(a, location[0], location[1], 0.5, 0.8, newLocation[0], newLocation[1], newA, reward)
                location = newLocation
                a = newA
            print(self.totalCost)
            self.totalCost = 0
            self.crossed = False
            self.velocity = (0,0)
            self.track.printTrack()
            self.track.restartRace()


qLearn = raceTrack.RaceTrack()
qLearn.createTrack("L-track.txt")
temp = QLearning(qLearn)
temp.qLearning(15)