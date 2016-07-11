'''
Load continuous (LFP) data and plot average locked to stimulus presentation.
'''

import os
from jaratoolbox import loadopenephys
reload(loadopenephys)
from pylab import *

'''
dataDir = '/data/ephys/test084/2015-01-03_17-40-58'
dataDir = '/data/ephys/test084/2015-01-03_17-55-46'
dataDir = '/data/ephys/test084/2015-01-03_18-27-09'
dataDir = '/data/ephys/test084/2015-01-03_18-52-02'
dataDir = '/data/ephys/test084/2015-01-03_19-06-45'

dataDir = '/home/jarauser/data/ephys/test090/2015-01-05_20-07-48'
'''
#ephysRoot= '/home/jarauser/data/ephys/test090/'
#ephysRoot= '/home/jarauser/data/ephys/test091/'
#ephysRoot= '/home/jarauser/data/ephys/test092/'
#ephysRoot= '/home/jarauser/data/ephys/test093/'
#ephysRoot= '/home/jarauser/data/ephys/rata001/'
#ephysRoot= '/home/jarauser/data/ephys/rata002/'
ephysRoot= '/home/jarauser/data/ephys/rata003/'

ephysSession=sort(os.listdir(ephysRoot))[-1]
dataDir = os.path.join(ephysRoot,ephysSession)

#dataDir = '/home/jarauser/data/ephys/test084/2015-01-03_17-40-58'

timeRange = [-0.6,0.8]

eventsFilename = os.path.join(dataDir,'all_channels.events')
events = loadopenephys.Events(eventsFilename)
###eventTimes=ev.timestamps  #/SAMPLING_RATE
eventOnsetTimes=events.timestamps[events.eventID==1] # Stim onset
###eventOnsetTimes=eventOnsetTimes[:-1] # The last behavior trial is always started but never finishe

#channelsToPlot = [15,18]
channelsToPlot = [16,17]
channelsToPlot = [3,6,11,15,19,23]
nChannels = len(channelsToPlot)
clf()
for indc,channel in enumerate(channelsToPlot):
    #filenameOnly = '109_CH15.continuous'
    #filenameOnly = '109_CH18.continuous'
    filenameOnly = '109_CH{0}.continuous'.format(channel)
    #filenameOnly = '110_CH{0:02d}.continuous'.format(channel)
    filename = os.path.join(dataDir,filenameOnly)
    datacont = loadopenephys.DataCont(filename)
    (lockedLFP,timeVec) = datacont.lock_to_event(eventOnsetTimes,timeRange)

    subplot(nChannels,1,indc+1)
    maxAbsVal = np.max(abs(lockedLFP),axis=1)
    tooLarge = maxAbsVal>6000
    plot(timeVec,mean(lockedLFP[~tooLarge,:],axis=0))
    #plot(timeVec,mean(lockedLFP,axis=0))
    #plot(timeVec,mean(lockedLFP[100:200,:],axis=0))
    ###plot(tile(timeVec,(1,locked)),lockedLFP) # NOT FINISHED
    ylim([-200,80])
    show()

    if 0:
        clf()
        plot(datacont.samples[:10000],'-')
        draw(); show()

show()


'''
if 1:
    if 1:
        samplesVec = np.arange(int(timeRange[0]*datacont.samplingRate),
                               int(timeRange[-1]*datacont.samplingRate))
        timeVec = samplesVec/datacont.samplingRate
        nSamples = len(timeVec)
        nTrials = len(eventOnsetTimes)
        lockedLFP = np.empty((nTrials,nSamples))
        for inde,eventTime in enumerate(eventOnsetTimes):
            if not np.isnan(eventTime):
                zeroSampleThisEvent = eventTime-datacont.timestamps[0]
                samplesIndexes = samplesVec + zeroSampleThisEvent
                lockedLFP[inde,:] = datacont.samples[samplesIndexes]
            else:
                lockedLFP[inde,:] = np.NaN
        #return (lockedLFP,timeVec)
'''
