import raceTrack
import ValueIteration

def main():
    rTrack=raceTrack.RaceTrack()
    lTrack = raceTrack.RaceTrack()
    rTrack.createTrack('R-track.txt')
    lTrack.createTrack('L-track.txt')
    print(rTrack.printTrack())
    rValue = ValueIteration.ValueIteration(rTrack)
    policy = rValue.valueIter('Resume', 1000,10000)
    print(rValue.timeTrial(policy, 10000, 'Resume', False, 'R-Track'))

    print(lTrack.printTrack())
    lValue= ValueIteration.ValueIteration(lTrack)
    lPolicy = lValue.valueIter('Resume', 1000,10000)
    print(lValue.timeTrial(lPolicy, 10000, 'Resume', False, 'L-Track'))

    oTrack = raceTrack.RaceTrack()
    oTrack.createTrack('O-track.txt')
    oValue = ValueIteration.ValueIteration(oTrack)
    oPolicy = oValue.valueIter('Resume', 1000, 10000)
    print(oValue.timeTrial(oPolicy, 10000, 'Resume', False, 'O-Track'))

    rrPolicy = rValue.valueIter('Restart', 1000, 10000)
    print(rValue.timeTrial(rrPolicy, 10000, 'Restart', False, 'R-Track'))

    lrPolicy = lValue.valueIter('Restart', 1000, 10000)
    print(lValue.timeTrial(lrPolicy, 10000, 'Restart', False, 'L-Track'))

    orPolicy = lValue.valueIter('Restart', 1000, 10000)
    print(oValue.timeTrial(orPolicy, 10000, 'Restart', False, 'O-Track'))


main()
    