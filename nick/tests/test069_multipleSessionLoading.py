from jaratoolbox import spikesorting
from jaratoolbox import loadopenephys
reload(loadopenephys)
reload(spikesorting)

subject = 'pinp016'

# #Sessions that have spikes
# sessions = ['2017-03-15_16-37-53', '2017-03-15_16-39-52']

#Sessions with no spikes, cause failure
# sessions = ['2017-03-07_13-56-23', '2017-03-07_13-59-17']
sessions = ['2017-03-07_13-56-23', '2017-03-07_13-59-17', '2017-03-07_14-01-57', '2017-03-07_14-06-13']

tetrode = 1 

oneTT = spikesorting.MultipleSessionsToCluster(subject,
                                               sessions,
                                               tetrode,
                                               'test_session')
oneTT.load_waveforms()

oneTT.create_fet_files()


