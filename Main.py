import raceTrack
import ValueIteration

def main():
    rTrack=raceTrack.RaceTrack()
    rTrack.createTrack('C:/Users/nardi/Documents/2019-2020 School Year/Spring Semester/446/CSCI446Project4/R-track.txt')
    print(rTrack.printTrack())
    temp = ValueIteration.ValueIteration(rTrack)
    policy = temp.valueIter('Resume', 1000,10000)

main()
    