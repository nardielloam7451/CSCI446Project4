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

    def getStart(self):
        startLocations = []
        for x in range(len(self.raceTrack)):
            if 'S' in self.raceTrack[x]:
                for y in range(len(self.raceTrack[x])):
                    if self.raceTrack[x][y] == 'S':
                        startLocations.append((x,y))
        return startLocations

    def updateQ(self, action, x, y, alpha, gamma, newX, newY):
        self.qTable[x][y][action] = self.qTable[x][y][action] + \
                                    alpha*(self.reward(action, x, y)+
                                           gamma*np.max(self.qTable[newX][newY])- self.qTable[x][y][action])

    def applyAction(self, x, y, selectedAction):
        newLocation = (x,y)
        if random.uniform(0,1) < 0.2:
            for x in range(self.velocity[0]):
                newLocation[0]+= 1
                isvalid = self.track.racerPosition(newLocation[0], newLocation[1])
                if isvalid == "Finished Track":
                    self.crossed = True
                if isvalid == "Hit Wall":
                    if self.restart:
                        self.track.restartRace()
                        return self.getStart()
                    else:
                        newLocation[0]-=1
                        self.velocity = (0,0)
                        return newLocation
            for y in range(self.velocity[1]):
                newLocation[1] += 1
                isvalid = self.track.racerPosition(newLocation[0], newLocation[1])
                if isvalid == "Finished Track":
                    self.crossed = True
                if isvalid == "Hit Wall":
                    if self.restart:
                        self.track.restartRace()
                        return self.getStart()
                    else:
                        newLocation[1] -= 1
                        self.velocity = (0,0)
                        return newLocation
        else:
            self.velocity = [self.velocity[0]+ selectedAction[0], self.velocity[1]+ selectedAction[1]]
            for v in range(2):
                if self.velocity[v] > 5:
                    self.velocity[v] = 5
            for x in range(self.velocity[0]):
                newLocation[0] += 1
                isvalid = self.track.racerPosition(newLocation[0], newLocation[1])
                if isvalid == "Finished Track":
                    self.crossed = True
                if isvalid == "Hit Wall":
                    if self.restart:
                        self.track.restartRace()
                        return self.getStart()
                    else:
                        newLocation[0] -= 1
                        self.velocity = (0, 0)
                        return newLocation
            for y in range(self.velocity[1]):
                newLocation[1] += 1
                isvalid = self.track.racerPosition(newLocation[0], newLocation[1])
                if isvalid == "Finished Track":
                    self.crossed = True
                if isvalid == "Hit Wall":
                    if self.restart:
                        self.track.restartRace()
                        return self.getStart()
                    else:
                        newLocation[1] -= 1
                        self.velocity = [0, 0]
                        return newLocation
        return newLocation

    def reward(self, x, y):
        if self.crossed:
            return 0
        else:
            return -1

    def selectAction(self, x, y):
        epsilon = 0.2
        if random.uniform(0, 1) < epsilon:
            return self.actions[random.choice(range(len(self.actions)))]
        else:
            return self.actions[self.qTable[x][y].argmax()]

    def qLearning(self):
        pass

qLearn = raceTrack.RaceTrack()
qLearn.createTrack("L-track.txt")
qLearn.printTrack()
temp = QLearning(qLearn)
for i in range(10):
    print(temp.selectA(0,0))
