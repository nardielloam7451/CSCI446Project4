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

        for line in trackFile:
            partTrack=line.split()
            self.raceTrack.append(partTrack)
        
        trackFile.close()
        

    def getXSize(self):
        """
        Function which returns the X-Dimension of the track
        Args: 
            None
        Returns:
            An integer of the x size for the track. 
        """
        return self.trackSize[0]

    def getYsize(self):
        """
        Function which returns the Y-Dimension of the track
        Args: 
            None
        Returns:
            An integer of the x size for the track. 
        """
        return self.trackSize[1]





