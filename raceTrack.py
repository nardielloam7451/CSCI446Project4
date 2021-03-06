class RaceTrack: 
    def __init__(self):
        self.trackSize=[]
        self.raceTrack =[]

    def createTrack(self, fileName):
        """
        Function which reads in the track and stores them within a list
        Args:
            The Name of the File which contains the data for our Tracks, read in as a string
        Returns:
            None
        """
        trackFile = open(fileName)
        self.trackSize = trackFile.readline().split(",")
        self.raceTrack = ['' for i in range(int(self.trackSize[0]))]
        for i, line in zip(range(int(self.trackSize[0])), trackFile):
            self.raceTrack[i]=list(line.strip())
        
        trackFile.close()

    def getXSize(self):
        """
        Function which returns the X-Dimension of the track
        Args: 
            None
        Returns:
            An integer of the x size for the track. 
        """
        return int(self.trackSize[0])

    def getYsize(self):
        """
        Function which returns the Y-Dimension of the track
        Args: 
            None
        Returns:
            An integer of the x size for the track. 
        """
        return int(self.trackSize[1])

    def printTrack(self):
        """
        Prints out the track for the user, in a nice row by row format. 
        Args: 
            None
        Returns:
            None
        """
        row = int(self.trackSize[0])
        for i in range(row):
            print(' '.join(map(str, self.raceTrack[i])))
        print("\n")

    def racerPosition(self, Xcor, Ycor):
        """
        Adds the Racers Current Position to the Track, and lets the racer know if the move was valid or not
        Args:
            Xcor: The new X-coordinate of our racer
            Ycor: The new Y-coordinate of our racer
        Returns:
            A String of if the move was valid or not
        """
        oldValue= self.raceTrack[Xcor][Ycor]
        if oldValue == '#':
            return "Hit Wall"
        elif oldValue =='.' or oldValue =='R' or oldValue == 'S':
            self.raceTrack[Xcor][Ycor]='R'
            return "On Track"
        elif oldValue=='F':
            return "Finished Track"

    def restartRace(self):
        """
        Resets the Track to its default state when called. 
        Args:
            None
        Returns:
            None
        """
        row = int(self.trackSize[0])
        for i in range(row):
            for j in range(len(self.raceTrack[i])):
                if self.raceTrack[i][j]=='R':
                    self.raceTrack[i][j]='.'

    def getTrack(self):
        return self.raceTrack




