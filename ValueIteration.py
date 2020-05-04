import numpy as np
import random
import raceTrack

class ValueIteration:
    def __init__(self, rTrack):
        self.track = rTrack
        self.raceTrack = self.track.getTrack()
        self.actions= [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]
        self.qTable = np.zeros((rTrack.getXSize(),rTrack.getYsize(), len(self.actions)))
        self.cost = 0
        self.startLocations = self.getStart()
        self.crossed = False
        self.totalCost = 0
        self.minVelocity = -1
        self.maxVelocity = 1
        self.discRate = 0.9 #The Discount rate, also known as gamma. 
        self.errorThres = 0.001 #The Error Threshold
        self.probAccelFail = 0.20 #The probability that the acceleration will fail
        self.probAccelSuccess = 1 - self.probAccelFail #The probability that the acceleration will succeed

    def getStart(self):
        """
        Gets the starting locations for our racetrack. 
        Args: 
            None
        Return: 
            A list of all starting positions that we have available. 
        """
        startLocations = []
        for x in range(len(self.raceTrack)):
                for y in range(len(self.raceTrack[x])):
                    for val in self.raceTrack[x][y]:
                        if val == 'S':
                            startLocations.append((x,y))
        return startLocations

    def getNewVelocity(self,oldVelX, oldVelY, accelX, accelY):
        """
        Get the new Veloicty values
        Args: 
            oldVelX= The old X-Velocity as an integer
            oldVelY = The old Y-Velocity as an integer
            accelX= The acceleration in the X direction
            accelY= The acceleration in the Y direction
        Returns: 
            Two new velocities in the x and y positions. 
        """
        newYVel= oldVelY +accelY
        newXVel= oldVelX +accelX
        if newXVel < self.minVelocity: newXVel = self.minVelocity
        if newXVel > self.maxVelocity: newXVel = self.maxVelocity
        if newYVel < self.minVelocity: newYVel = self.minVelocity
        if newYVel > self.maxVelocity: newYVel = self.maxVelocity

        return newYVel, newXVel

    def getNewPosition(self,xPos, yPos, xVel, yVel, punishment):
        """
        Get a new position using the old position and the velocity
        Args:
            xPos: The Old X position for the racer
            yPos: The Old Y Position for the racer
            xVel: The xVelocity of the racer
            yVel: The y-Velocity of the racer
            punishment: the crash penalty
        Returns: 
            The new X and Y coordinate and, but returns either the old position of 0,0 if racer crashed
        """
        newXPos= xPos+xVel
        newYPos = yPos+yVel
        check =self.track.getNewPosition(newXPos, newYPos)
        if check =="Hit Wall":
            if punishment == "Restart":
                newXPos = self.startLocations[0][0]
                newYPos = self.startLocations[0][1]
                return newXPos, newYPos, "Restart"
            elif punishment == 'Resume':
                newXPos = xPos
                newYPos = yPos
                return newXPos, newYPos, "Hit Wall"
        elif check == "Finished Track":
            return newXPos, yPos, "Finished Track"
        
        return newXPos, newYPos, "Moved"
        
    def Act(self, oldYPos, oldXPos, oldYVel, oldXVel, accelX, accelY, crashType, deterministic=(False)):
        """
        This method generates the new state s' (position and velocity) from the old
        state s and the action a taken by the race car. It also takes as parameters
        the two different crash scenarios (i.e. go to nearest
        open position on the race track or go back to start)
        
        Args:
            oldYPos = The old Y position for the racer
            oldXPos = The old X position for the racer
            oldYVel = The Old Y Velocity for the racer
            oldXVel = The old X Velocity for the racer
            accelX = The acceleration in the x direction for the racer
            accelY = The acceleration in the Y Direction for the racer
            deterministic = Whether or not we are running this algorithm deterministically 
            crashType = What is our plan in terms of a crash. 
        Return: 
            The new State s' where s' = newYPos, newXPos, newXVel, newYVel
        """

        if not deterministic: 
            if random.Random() > self.probAccelSuccess: #determins if the acceleration fails or not
                accelX = 0
                accelY = 0

        newVelX, newVelY, = self.getNewVelocity(oldXVel,oldYVel, accelX, accelY) #gets the new velocity

        newY, newX, message = self.getNewPosition(oldXPos, oldYPos, newVelX, newVelY, crashType) #gets the new positions
        
        if message == "Hit Wall": #checks if we crashed or not
            if crashType == "Restart":
                self.track.restartRace()
            newVelX, newVelY = 0,0
        
        return newY, newX, newVelX, newVelY


        
        
