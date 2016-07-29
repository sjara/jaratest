'''
This is a function that will sort ephys sessions according to their recorded time and generate a sessionList (sesionListSorted) for each site in the RecordingSite object in ephys_experiemtn.py. It will also generate another list (sessionNamesSorted) of the labels of the sessions in the sorted order.
'''


from jaratoolbox.test.nick.ephysExperiments import ephys_experiment
reload(ephys_experiment)
from jaratoolbox.test.nick.ephysExperiments.ephys_experiment import RecordingSite
from jaratoolbox.test.nick.ephysExperiments.ephys_experiment import EphysExperiment


def sortSessionList(sessionList):

    sessionNames = ['noiseburstEphysSession', 'laserPulseEphysSession', 'laserTrainEphysSession', 'tuningCurveEphysSession', 'bfEphysSession', 'laserPulseEphysSession3mW', 'laserPulseEphysSession1mW']
    sessionOrder = [i[0] for i in sorted(enumerate(sessionList), key=lambda x:x[1])]
    sessionListSorted = sorted(sessionList)  #the sorted list has all 'None' sessions in the beginning and then non-empty sessions in the order of the time recorded.
    sessionNamesSorted = [sessionNames[i] for i in sessionOrder] 
   
    return(sessionListSorted, sessionNamesSorted)

if __name__ == "__main__":

    from jaratoolbox.test.nick.ephysExperiments import ephys_experiment
    from jaratoolbox.test.nick.ephysExperiments.ephys_experiment import RecordingSite
    reload(ephys_experiment)

    site1 = RecordingSite(depth = 2612,
                      noiseburstEphysSession  = '2015-07-01_18-12-05',
                      laserPulseEphysSession  = '2015-07-01_18-06-54',
                      laserTrainEphysSession = None,
                      tuningCurveEphysSession  = '2015-07-01_18-18-47',
                      tuningCurveBehavIdentifier  = 'a',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = '2015-07-01_18-36-00',
                      laserPulseEphysSession1mW = None,
                      goodTetrodes = [6])
    
    print site1.sessionList

    (sessionListSorted, sessionNamesSorted) =sortSessionList(site1.sessionList)
    print sessionListSorted, sessionNamesSorted
