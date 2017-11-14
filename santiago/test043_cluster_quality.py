'''
Automatic cluster quality

THINGS TO FIGURE OUT
- Copy all files corresponding to an ephys session to my computer
- Copy all files related to a multisession/date.
- Keep inforec in a place accessible to everyone
- Find session from inforec (by giving subject and date)
- Load spikes/samples given session from inforec.
- Importing inforec gives:
  RuntimeWarning: Parent module 'module' not found while handling absolute import
- Get ephys file given inforec.
'''

from jaratoolbox import loadopenephys
from jaratoolbox import spikesorting
reload(spikesorting)
from matplotlib import pyplot as plt
import imp
import sys

print sys.argv[0]

if len(sys.argv)>1:
    tetrode = int(sys.argv[1])
else:
    tetrode = 3
    
#subject = 'gosi004'
#ephysSession = '2017-02-11_15-46-30'
#ephysSession = '2017-02-11_15-54-13'

subject = 'd1pi015'
ephysSession = '2016-08-07_16-48-07'

srate = 30000.0

'''
inforecFilename = '/data/inforec/gosi004_inforec.py'
inforec = imp.load_source('module.name', inforecFilename)
inforec.experiments[5].sites[0].sessions[0].ephys_dir
'''

ttdata = spikesorting.TetrodeToCluster(subject,ephysSession,tetrode)
ttdata.load_waveforms()
ttdata.set_clusters_from_file()

'''
report = spikesorting.ClusterReportFromData(ttdata.timestamps,
                                            ttdata.samples,
                                            ttdata.clusters,
                                            outputDir=None,
                                            figtitle='title',
                                            showfig=False)
'''

plt.clf()
for cluster in range(1,7):
    #cluster = 2
    indsThisCluster = (ttdata.clusters==cluster)
    onettwaveforms = ttdata.samples[indsThisCluster,:,:]
    (peakTimes, peakAmplitudes, spikeShape, spikeShapeSD) = spikesorting.estimate_spike_peaks(onettwaveforms,srate)

    #print peakTimes
    #print peakAmplitudes

    shapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
    print 'c{0}  shapeQuality = {1:0.2f}'.format(cluster,shapeQuality)

    nSamples = len(spikeShape)
    #tvec = 

    plt.subplot(6,1,cluster)
    plt.hold(1)
    plt.fill_between(range(nSamples),spikeShape+spikeShapeSD,spikeShape-spikeShapeSD,color='0.75')
    plt.plot(spikeShape,'.-')
    
    plt.hold(0)
    plt.show()

