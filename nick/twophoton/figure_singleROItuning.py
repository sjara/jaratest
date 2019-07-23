import os
import numpy as np
from scipy import io
from jaratoolbox import extraplots
from matplotlib import pyplot as plt

#Maybe we really want a function that takes an arr of (nEvents, nSamples) and another of the condition on each event and plots that? With mean and std area?
def plot_calcium_tuning(tuningArr):
    '''
    Plot the eventlocked traces for multiple frequencies (or whatever)
    Args:
        tuningArr (array): Shape of (nFreqs, nSamples). Already the average response.
    '''
    nAxes, nSamples = np.shape(tuningArr)
    maxResponse = np.max(np.ravel(tuningArr))
    minResponse = np.min(np.ravel(tuningArr))

    #FIXME: Some experimental parameters are hardcoded here.
    #We should alter the function to either accept parameters or load them.
    possibleFreqs = np.logspace(np.log2(2), np.log2(40), num=8, base=2)
    stimDur = 0.1
    samplingRate = 17.0
    samplesBefore = 10
    samplesAfter = 30

    timePerFrame = 1/samplingRate
    samplesPerStimulus = np.ceil(stimDur/timePerFrame)


    plt.clf()
    plt.subplots_adjust(bottom=0.35)
    for indAxis in range(nAxes):
        ax = plt.subplot(1, nAxes, indAxis+1)
        ax.plot(range(nSamples), tuningArr[indAxis, :], 'k-')
        ax.axis('off')
        ax.set_ylim([minResponse, maxResponse])
        ax.text(nSamples/2, minResponse-abs(minResponse*1.8), '{:.1f}'.format((possibleFreqs[indAxis])), ha='center', va='top')
        # lineY = minResponse-abs(minResponse*0.05)

        #Plot X axis lines
        lineY = minResponse
        plt.plot([0, nSamples], [lineY, lineY], '-', lw=3, color='0.5')
        plt.plot([samplesBefore+1, samplesBefore+samplesPerStimulus], [lineY, lineY], lw=15, color='r', solid_capstyle='butt')

        #Plot Y axis scale bar
        if indAxis==0:
            #Indicate time base
            plt.text(0, lineY-abs(lineY*0.1), '-{:.02f}\nsec'.format(samplesBefore/samplingRate), ha='center', va='top')
            plt.text(samplesBefore+samplesAfter, lineY-abs(lineY*0.1), '{:.02f}\nsec'.format(samplesAfter/samplingRate), ha='center', va='top')

            # plt.plot([-1, -1], [lineY, lineY + (maxResponse-minResponse)*0.5], '-', color=0.5)
            plt.plot([-1, -1], [minResponse, maxResponse], '-', color='0.5')
            plt.plot([-5, -1], [0, 0], '-', color='0.5')
            plt.plot([-5, -1], [minResponse, minResponse], '-', color='0.5')
            plt.plot([-5, -1], [maxResponse, maxResponse], '-', color='0.5')
            plt.text(-8, 0, '0', ha='right', va='center')
            plt.text(-8, maxResponse, '{:.2f}'.format(maxResponse), ha='right', va='center')
            plt.text(-8, minResponse, '{:.2f}'.format(minResponse), ha='right', va='center')
            plt.text(-20, np.mean([minResponse, maxResponse]), 'df/f', ha='right', va='center', rotation=90)

    plt.show()

intermediateDataDir = '/home/nick/data/2pdata/tmp'
saveDir = '/home/nick/data/2pdata/tmpFigs'

# for indROI in range(len(os.listdir(intermediateDataDir))):
for indROI in [10, 15, 45]:
    fName = os.path.join(intermediateDataDir, 'imag003_ROI_{}.npy'.format(indROI))
    thisROI = np.load(fName)
    plot_calcium_tuning(thisROI)
    plt.title('{}'.format(indROI))
    figFn = os.path.join(saveDir, 'imag003_ROI_{}.png'.format(indROI))
    plt.savefig(figFn)
