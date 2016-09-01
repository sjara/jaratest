'''
Test spikesorting module
'''

from jaratoolbox import settings
from jaratoolbox import spikesorting
reload(spikesorting)
import os

CASE = 3

if CASE==1:
    animalName = 'test030'
    ephysSession = '2014-06-25_18-33-30_TT6goodGND'
    tetrode = 6
elif CASE==2:
    animalName = 'hm4d002'
    ephysSession = '2014-08-04_18-04-45'
    tetrode = 2
elif CASE==3:
    animalName = 'test080'
    ephysSession = '2014-11-23_18-27-39'
    tetrode = 2
elif CASE==4:
    animalName = 'pinp003'
    ephysSession = '2015-06-22_18-39-21'
    tetrode = 6

#spike_filename='..../2014-06-25_18-33-30_TT6goodGND/Tetrode6.spikes'
#dataspikes = loadopenephys.DataSpikes(spike_filename)

oneTT = spikesorting.TetrodeToCluster(animalName,ephysSession,tetrode)
#oneTT.load_waveforms()




# --- Test ---
from jaratoolbox import loadopenephys
reload(loadopenephys)
from pylab import *
N_CHANNELS = 4
SAMPLES_PER_SPIKE = 40

dataDir = os.path.join(settings.EPHYS_PATH,'%s/%s/'%(animalName,ephysSession))
tetrodeFile = os.path.join(dataDir,'Tetrode%d.spikes'%tetrode)

dataTT = loadopenephys.DataSpikes(tetrodeFile)
dataTT.timestamps = dataTT.timestamps/0.03  # in microsec
dataTT.samples = dataTT.samples.astype(float)-2**15
dataTT.set_clusters('/tmp/TT2.clu.1')

crep = spikesorting.ClusterReportFromData(dataTT)


'''
dataTT.samples = dataTT.samples.reshape((-1,N_CHANNELS,SAMPLES_PER_SPIKE),order='C')

fetArray = spikesorting.calculate_features(dataTT.samples,['peak','valley'])

spikesorting.write_fet_file('/tmp/TT2.fet.1',fetArray)
'''

'''
plot(dataTT.samples[:10,:].T,'.-')
draw()
show()
'''

'''
~/tmp/klustakwik/KK2/KlustaKwik TT6 1 -Subset 1e5 -MinClusters 6 -MaxClusters 12 -MaxPossibleClusters 12 -UseFeatures 11111111

~/tmp/klustakwik/KK2/KlustaKwik TT6 1 -Subset 1e5 -MinClusters 10 -MaxClusters 24 -MaxPossibleClusters 12 -UseFeatures 11111111
### Gave an error: seg fault out of range index 12 (probably because of the 24)
'''

