from jaratoolbox import settings
from jaratoolbox import loadopenephys
from jaratest.nick.inforecordings import lasertest_inforec as inforec
reload(inforec)
import os

animalName = 'lasertest'

tetrodes=range(1, 7)
sessions = inforec.experiments[0].sites[0].session_ephys_dirs()
labels = inforec.experiments[0].sites[0].session_types()

for indSession, session in enumerate(sessions):
    print '\n\n'
    print '{} Session {}'.format(labels[indSession], session)
    for indTet, tetrode in enumerate(tetrodes):
        spikesFn = 'Tetrode{}.spikes'.format(tetrode)
        spikesFile = os.path.join(settings.EPHYS_PATH, animalName, session, spikesFn)
        print 'Tetrode {}'.format(tetrode)
        spikeData = loadopenephys.DataSpikes(spikesFile)
        if hasattr(spikeData, 'timestamps'):
            print len(spikeData.timestamps)
