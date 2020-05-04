import raceTrack
import ValueIteration

def main():
    rTrack=raceTrack.RaceTrack()
    lTrack = raceTrack.RaceTrack()
    rTrack.createTrack('C:/Users/nardi/Documents/2019-2020 School Year/Spring Semester/446/CSCI446Project4/R-track.txt')
    lTrack.createTrack('C:/Users/nardi/Documents/2019-2020 School Year/Spring Semester/446/CSCI446Project4/L-track.txt')
    print(rTrack.printTrack())
    rValue = ValueIteration.ValueIteration(rTrack)
    policy = rValue.valueIter('Resume', 1000,10000)
    print(rValue.timeTrial(policy, 10000, 'Resume', False))

    print(lTrack.printTrack())
    lValue= ValueIteration.ValueIteration(lTrack)
    lPolicy = lValue.valueIter('Resume', 1000,10000)
    print(lValue.timeTrial(lPolicy, 10000, 'Resume', False))

    oTrack = raceTrack.RaceTrack()
    oTrack.createTrack('C:/Users/nardi/Documents/2019-2020 School Year/Spring Semester/446/CSCI446Project4/O-track.txt')
    oValue = ValueIteration.ValueIteration(oTrack)
    oPolicy = oValue.valueIter('Resume', 1000, 10000)
    print(oValue.timeTrial(oPolicy, 10000, 'Resume', False))

    rrPolicy = rValue.valueIter('Restart', 1000, 10000)
    print(rValue.timeTrial(rrPolicy, 10000, 'Restart', False))

    lrPolicy = lValue.valueIter('Restart', 1000, 10000)
    print(lValue.timeTrial(lrPolicy, 10000, 'Restart', False))

    orPolicy = lValue.valueIter('Restart', 1000, 10000)
    print(oValue.timeTrial(orPolicy, 10000, 'Restart', False))


main()
    