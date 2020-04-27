import raceTrack

def main():
    rTrack=raceTrack.RaceTrack()
    rTrack.createTrack('R-track.txt')
    print(rTrack.getXSize())
    print(rTrack.getYsize())

main()
    