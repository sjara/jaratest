import os
import sys; sys.path.append('/home/nick/data')
import jaratoolbox; reload(jaratoolbox)
from jaratoolbox import settings; reload(settings)
from inforecordings import test098_inforec as inforec
reload(inforec)
from jaratest.nick.ephysExperiments import clusterManySessions_v2 as cms
import matplotlib.pyplot as plt
print inforec.test098
import pandas as pd
import numpy as np

exp = inforec.test098.experiments[1]

animalName = exp.subject

# sessionInds = [1, 5]
sessionInds = range(len(exp.sites[0].sessions))
sessionList = []
for ind in sessionInds:
    session = exp.sites[0].sessions[ind]
    sessionStr = '{}_{}'.format(session.date, session.timestamp)
    sessionList.append(sessionStr)

#The channel number recorded for each tetrode
contChannels = {1:31,
                2:27,
                3:24,
                4:29,
                5:3,
                6:14,
                7:5,
                8:6}

secondsEachTrace=0.1
EPHYS_SAMPLING_RATE=30000.0

timebase = np.arange(0, secondsEachTrace*EPHYS_SAMPLING_RATE)/EPHYS_SAMPLING_RATE
tetrodes=range(1, 9)

# figure()

meanTraceEachTetSession = np.empty((len(tetrodes), len(sessionList), secondsEachTrace*EPHYS_SAMPLING_RATE))

for indTetrode, tetrode in enumerate(tetrodes):
    contFn = '109_CH{}.continuous'.format(contChannels[tetrode])
    for indSession, session in enumerate(sessionList):
        fullContFile = os.path.join(settings.EPHYS_PATH, animalName, session, contFn)
        fullEventFile = os.path.join(settings.EPHYS_PATH, animalName, session, 'all_channels.events')

        contData = loadopenephys.DataCont(fullContFile)
        contData.samples = contData.samples/5.0
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
        meanTraceEachTetSession[indTetrode, indSession, :]=meanTrace

maxVoltageAll = np.max(meanTraceEachTetSession.ravel())
minVoltageAll = np.min(meanTraceEachTetSession.ravel())
scalebarSize = abs(minVoltageAll)

fontsize=10
clf()
for indTetrode, tetrode in enumerate(tetrodes):
    for indSession, session in enumerate(sessionList):
        subplot2grid((len(sessionList), 8),(indSession, indTetrode))
        trace = meanTraceEachTetSession[indTetrode, indSession, :]
        plot(timebase, trace, 'k')
        plt.hold(1)
        ylim([minVoltageAll, maxVoltageAll])
        ax=gca()
        ax.set_xticks([0, 0.1])
        if indSession==0:
            title('TT{}'.format(tetrode))

        axis('off')
        plt.plot(2*[0],[0,-scalebarSize],color='0.5',lw=3)

        if ((indTetrode==0)&(indSession==0)):
            plt.text(-0.01,-scalebarSize/2,'{0:0.0f}uV'.format(np.round(scalebarSize)),
                     ha='right',va='center',ma='center',fontsize=fontsize, rotation='vertical')


def getYlabelpoints(n):
    rawArray = np.array(range(1, n+1))/float(n+1) #The positions in a perfect (0,1) world
    diffFromCenter = rawArray - 0.6
    partialDiffFromCenter = diffFromCenter * 0.1 #Percent change has to be determined empirically
    finalArray = rawArray - partialDiffFromCenter
    return finalArray

sessionLabelPositions = getYlabelpoints(len(sessionList))
for indp, position in enumerate(sessionLabelPositions):
    sessionLab = sessionList[::-1][indp].split('_')[1]
    plt.figtext(0.075, position, "{}".format(sessionLab), rotation='vertical')

suptitle('{} {}'.format(exp.subject, exp.date))

savefig('/home/nick/data/ephys/test098/reports_ephys/experiment_{}.png'.format(exp.date))
