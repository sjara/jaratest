import numpy as np
from jaratest.nick.probes import probelayout
from jaratoolbox import settings
from jaratoolbox import loadopenephys
from matplotlib import pyplot as plt
from jaratest.nick.inforecordings import lasertest_inforec as inforec
import os

channelMap = probelayout.channelMap[:6, :] #Only tetrodes 1-6 are still intact
channels = channelMap.ravel() #Take the channels one at a time

animalName = 'lasertest'

# session = '2016-08-22_16-03-24'

#The channels arranged by tetrode, 7 and 8 are broken off

secondsEachTrace=0.5
EPHYS_SAMPLING_RATE=30000.0

timebase = np.arange(0, secondsEachTrace*EPHYS_SAMPLING_RATE)/EPHYS_SAMPLING_RATE

sessions = inforec.experiments[0].sites[0].session_ephys_dirs()

#maprow = tetrode
#mapcol = channel
#meanTraceEachChannel(sessions, tetrode, channel, samples)
meanTraceEachChannel = np.empty((len(sessions), np.shape(channelMap)[0], np.shape(channelMap)[1], secondsEachTrace*EPHYS_SAMPLING_RATE))

#for indChan, channel in enumerate(channels):


colors = plt.cm.viridis(np.linspace(0, 1, len(sessions)))

for indSession, session in enumerate(sessions):
    for (indr, indc), channel in np.ndenumerate(channelMap):
        contFn = '100_CH{}.continuous'.format(channel)
        fullContFile = os.path.join(settings.EPHYS_PATH, animalName, session, contFn)
        fullEventFile = os.path.join(settings.EPHYS_PATH, animalName, session, 'all_channels.events')
        contData = loadopenephys.DataCont(fullContFile)

        #Multiply by 1000 and div by gain (*1000/5000)
        contData.samples = contData.samples/5.0

        #Load the events
        eventData = loadopenephys.Events(fullEventFile)
        eventData.timestamps = eventData.timestamps[((eventData.eventID==1) & (eventData.eventChannel==0))]
        startTimestamp = contData.timestamps[0]
        eventSampleNumbers = eventData.timestamps - startTimestamp
        traces = np.empty((len(eventSampleNumbers), secondsEachTrace*EPHYS_SAMPLING_RATE))
        for indSamp, sampNumber in enumerate(eventSampleNumbers):
            trace = contData.samples[sampNumber:sampNumber + secondsEachTrace*EPHYS_SAMPLING_RATE]
            trace = trace - trace[0]
            traces[indSamp, :] = trace
        meanTrace = np.mean(traces, axis = 0)
        meanTraceEachChannel[indSession, indr, indc, :]=meanTrace

maxVoltageAll = np.max(meanTraceEachChannel.ravel())
minVoltageAll = np.min(meanTraceEachChannel.ravel())
scalebarSize = abs(minVoltageAll)

fontsize=10
plt.clf()


axes = np.empty(np.shape(channelMap), dtype='object')
for (indr, indc), chan in np.ndenumerate(channelMap):
    axes[indr, indc] = plt.subplot2grid(np.shape(channelMap),(indr, indc))

for indSession, session in enumerate(sessions):
    for (indr, indc), chan in np.ndenumerate(channelMap):

        ax = axes[indr, indc]

        trace = meanTraceEachChannel[indSession, indr, indc, :]
        # import pdb; pdb.set_trace()
        ax.plot(timebase, trace, color=colors[indSession])
        ax.hold(1)
        ax.set_ylim([minVoltageAll, maxVoltageAll])
        ax.set_xticks([0, 0.1])
        ax.set_title('Ch{}'.format(chan))
        ax.axis('off')

        if indSession==0:
            ax.plot(2*[0],[0,-scalebarSize],color='0.5',lw=3)

        if ((indSession==0)&(indr==0)&(indc==0)):
            ax.text(-0.01,-scalebarSize/2,'{0:0.0f}uV'.format(np.round(scalebarSize)),
                        ha='right',va='center',ma='center',fontsize=fontsize, rotation='vertical')

def getYlabelpoints(n):
    rawArray = np.array(range(1, n+1))/float(n+1) #The positions in a perfect (0,1) world
    diffFromCenter = rawArray - 0.6
    partialDiffFromCenter = diffFromCenter * 0.1 #Percent change has to be determined empirically
    finalArray = rawArray - partialDiffFromCenter
    return finalArray

sessionLabelPositions = getYlabelpoints(len(channelMap))
for indp, position in enumerate(sessionLabelPositions[::-1]):
    sessionLab = 'TT{}'.format(indp+1)
    plt.figtext(0.075, position, sessionLab, rotation='vertical')



color_patches = []
color_patches.append(mpatches.Patch(color='red', label='0.25mg/ml'))
