import numpy as np
import raceTrack
import time
from random import random
from random import randint
from copy import deepcopy

class ValueIteration:
    def __init__(self, rTrack):
        self.track = rTrack
        self.raceTrack = self.track.getTrack()
        self.actions=[(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]
        self.minVelocity = -5
        self.maxVelocity = 5
        self.velocities = range(self.minVelocity, self.maxVelocity+1)
        self.qTable = [[[[[random() for _ in self.actions] for _ in self.velocities] for _ in (self.velocities)] for _ in line] for line in self.raceTrack]
        self.cost = 0
        self.startLocations = self.getStart()
        self.crossed = False
        self.totalCost = 0
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

        return newXVel, newYVel

    def driveTrack(self, oldYPos, oldXPos, oldYVel, oldXVel, accelX, accelY, deterministic, crashType):
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
            if random() > self.probAccelSuccess: #determins if the acceleration fails or not
                accelX = 0
                accelY = 0

        newVelX, newVelY, = self.getNewVelocity(oldXVel,oldYVel, accelX, accelY) #gets the new velocity

        tempX, tempY = self.getNewPosition(oldXPos, oldYPos, newVelX, newVelY, crashType) #gets the new positions
        
        newX, newY= self.getNearestOpen(tempY, tempX, newVelY, newVelX)

        if newX != tempX or newY != tempY:
            if crashType =='Restart' and self.raceTrack[newX][newY]=='F':
                newPos = randint(0,len(self.startLocations))
                newX = self.startLocations[newPos][0]
                newY = self.startLocations[newPos][1]
            newVelX =0
            newVelY=0
        
        return newX, newY, newVelX, newVelY


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
        
        return newXPos, newYPos
    
    def getNearestOpen(self,yCrash, xCrash, vy, vx, open=['.','S','G']):
        """
        Locate the nearest open cell in order to hangel crashing. Distance is calculated by Manhatten distance. 
        Args: 
            yCrash: The y-coordinate of the crash
            xCrash: The x-coordinate of the crash
            vy: The Velocity in the y direction
            vx: The Velocity in the x direction
            open: Contains environment types
        Returns: 
            x,y coordinates of nearest open space
        """
        rows = self.track.getXSize()
        cols = self.track.getYsize()

        max_radius = max(rows, cols)

        for radius in range(max_radius): 
            if vx==0: 
                xRange = range(-radius, radius+1)
            elif vx <0:
                xRange = range(0, radius+1)
            else: 
                xRange= range(-radius, 1)

            for xOff in xRange: 
                x= xCrash+xOff
                yRad = radius - abs(xOff)

                if vy ==0:
                    yRange = range(yCrash- yRad, yCrash+yRad+1)
                elif vy <0:
                    yRange = range(yCrash, yCrash+yRad+1)
                else:
                    yRange = range(yCrash-yRad, yCrash+1)

                for y in yRange: 
                    if x<0 or x>= rows: continue
                    if y<0 or y>= cols: continue

                    if self.raceTrack[x][y] in open:
                        return x,y
        return xCrash-1, yCrash-1
        
    def getPolicyfromQ(self,cols, rows):
        """
        This method returns the policy pi(s) based on the action taken in each state
        that maximizes the value of Q in the table Q[s,a]. This is pi*(s)...the
        best action that the race car should take in each state is the one that 
        maximizes the value of Q. (* means optimal)
        Args: 
            cols: Number of columns in the racetrack
            rows: Number of rows in the racetrack 
        Return: 
            pi: the policy
        """
        pi={}

        for x in range(rows):
            for y in range(cols):
                for velocityY in self.velocities: 
                    for velocityX in self.velocities:
                        pi[(x,y,velocityX,velocityY)]=self.actions[np.argmax(self.qTable[x][y][velocityY][velocityX])]
    
    def valueIter(self, crashType, reward, numTrainIter):
        """
        This method is the actual value iteration algorithm
        Args: 
            crashType: Defines what type of what happens when you crash 
            reward: reward of the terminal states
            numTrainIter: Number of training iterations. 
        Return: 
            policy pi(s) which maps a given state to an optimal action
        """
        #Calculate the number of rows and columns of the racetrack
        rows = self.track.getXSize()
        cols = self.track.getYsize()



        #Generates the List comprehension for the entire file
        #stored as Xposition, Yposition, VelocityY, VelocityX
        values =[[[[random() for _ in self.velocities] for _ in self.velocities]for rYPOs in line] for line in self.raceTrack]

        # Set the finish line states to 
        for x in range(rows):
            for y in range(cols): 
                if self.raceTrack[x][y]=='F':
                    for vy in self.velocities:
                        for vx in self.velocities:
                                values[x][y][vy][vx] = reward
        
        #Set finish line state-action pairs to 0
        for x in range(rows):
            for y in range(cols):
                if self.raceTrack[x][y]=='F':
                    for vy in self.velocities:
                        for vx in self.velocities:
                            for ai, a in enumerate(self.actions):
                                self.qTable[x][y][vy][vx][ai]=reward
        
        # This is where we train the agent (i.e. race car). Training entails 
        # optimizing the values in the tables of V(s) and Q(s,a)
        for t in range(numTrainIter):
 
            # Keep track of the old V(s) values so we know if we reach stopping 
            # criterion
            values_prev = deepcopy(values)
 
            # When this value gets below the error threshold, we stop training.
            # This is the maximum change of V(s)
            delta = 0.0
 
            # For all the possible states s in S
            for x in range(rows):
                for y in range(cols):
                    for vy in self.velocities:
                        for vx in self.velocities:
                         
                            # If the car crashes into a wall
                            if self.raceTrack[x][y]=='#':
 
                                # Wall states have a negative value
                                # I set some arbitrary negative value since
                                # we want to train the car not to hit walls
                                values[x][y][vy][vx] = -9.9
 
                                # Go back to the beginning
                                # of this inner for loop so that we set
                                # all the other wall states to a negative value
                                continue
 
                            # For each action a in the set of possible actions A
                            for ai, a in enumerate(self.actions):
 
                                # The reward is -1 for every state except
                                # for the finish line states
                                if self.raceTrack[x][y]=='F':
                                    r = reward
                                else:
                                    r = -1
 
                                # Get the new state s'. s' is based on the current 
                                # state s and the current action a
                                new_x, new_y, new_vx, new_vy = self.driveTrack(y, x, vy, vx, a[0], a[1], True, crashType)
 
                                # V(s'): value of the new state when taking action
                                # a from state s. This is the one step look ahead.
                                value_of_new_state = values_prev[new_x][new_y][new_vy][new_vx]
 
                                # Get the new state s'. s' is based on the current 
                                # state s and the action (0,0)
                                new_x, new_y, new_vx, new_vy = self.driveTrack(y,x,vy,vx,a[0],a[1],True,crashType)
 
                                # V(s'): value of the new state when taking action
                                # (0,0) from state s. This is the value if for some
                                # reason the race car attemps to accelerate but 
                                # fails
                                value_of_new_state_if_action_fails = values_prev[new_x][new_y][new_vy][new_vx]
 
                                # Expected value of the new state s'
                                # Note that each state-action pair has a unique 
                                # value for s'
                                expected_value = (self.probAccelSuccess * value_of_new_state) + (self.probAccelFail * (value_of_new_state_if_action_fails))
 
                                # Update the Q-value in Q[s,a]
                                # immediate reward + discounted future value
                                self.qTable[x][y][vy][vx][ai] = r + (self.discRate * expected_value)
 
                            # Get the action with the highest Q value
                            argMaxQ = np.argmax(self.qTable[x][y][vy][vx])
 
                            # Update V(s)
                            values[x][y][vy][vx] = self.qTable[x][y][vy][vx][argMaxQ]
 
            # Make sure all the rewards to 0 in the terminal state
            for x in range(rows):
                for y in range(cols):
                    # Terminal state has a value of 0
                    if self.raceTrack[x][y]=='F':
                        for vy in self.velocities:
                            for vx in self.velocities:                 
                                values[x][y][vy][vx] = reward
 
            # See if the V(s) values are stabilizing
            # Finds the maximum change of any of the states. Delta is a float.
            delta = max([max([max([max([abs(values[x][y][vy][vx] - values_prev[x][y][vy][vx]) for vx in self.velocities]) for vy in (self.velocities)]) for y in range(cols)]) for x in range(rows)])
 
            # If the values of each state are stabilizing, return the policy
            # and exit this method.
            if delta < self.errorThres:
                return(self.getPolicyfromQ(cols,rows))
        return(self.getPolicyfromQ(cols,rows))

    def timeTrial(self,steps, maxSteps, crashPlan, animate):
        """
        Preforms the time trail for racer using the Value Iteration method
        Args:
            Steps: The Policy generated by the Value Iteration for our function
            maxSteps: The maximum number of steps we are allowing our racer to make. 
            crashPlan: Which of our two choices are we using for our crashplan. If "restart" then it restarts after crashing. 
            animate: whether or not we want to print out the steps of our algorithm. 
        Returns:
            numSteps: The number of steps actually taken by our algorithm. 
        """
        randStart = randint(0, len(self.startLocations))
        x = self.startLocations[randStart][0]
        y= self.startLocations[randStart][1]

        vy,vx=0,0

        stopClock =0

        for i in range(maxSteps):
            if animate:
                self.track.printTrack()
            
            ax=steps[(x,y,vx,vy)][0]
            ay=steps[(x,y,vx,vy)][1]

            if self.raceTrack[x][y]=='F':
                return i
            
            x,y,vy,vx = self.driveTrack(y,x,vy,vx, ax, ay, False, crashPlan)

            if vy==0 and vx==0:
                stopClock+=1
            else:
                stopClock=0

            if stopClock==5:
                return maxSteps
        return maxSteps





 