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

    #This is bad I know
    possibleFreqs = np.logspace(np.log2(2), np.log2(40), num=8, base=2)

    plt.clf()
    for indAxis in range(nAxes):
        ax = plt.subplot(1, nAxes, indAxis+1)
        ax.plot(range(nSamples), tuningArr[indAxis, :], 'k-')
        ax.axis('off')
        ax.set_ylim([minResponse, maxResponse])
        ax.text(nSamples/2, minResponse-abs(minResponse*0.15), '{:.1f}'.format((possibleFreqs[indAxis])), ha='center', va='top')
        # lineY = minResponse-abs(minResponse*0.05)

        #Plot X axis lines
        lineY = minResponse
        plt.plot([0, nSamples], [lineY, lineY], '-', lw=3, color='0.5')

        #Plot Y axis scale bar
        if indAxis==0:
            # plt.plot([-1, -1], [lineY, lineY + (maxResponse-minResponse)*0.5], '-', color=0.5)
            plt.plot([-1, -1], [minResponse, maxResponse], '-', color='0.5')
            plt.plot([-5, -1], [0, 0], '-', color='0.5')
            plt.plot([-5, -1], [minResponse, minResponse], '-', color='0.5')
            plt.plot([-5, -1], [maxResponse, maxResponse], '-', color='0.5')

    plt.show()

intermediateDataDir = '/home/nick/data/2pdata/tmp'
saveDir = '/home/nick/data/2pdata/tmpFigs'

# for indROI in range(len(os.listdir(intermediateDataDir))):
for indROI in [0]:
    fName = os.path.join(intermediateDataDir, 'imag003_ROI_{}.npy'.format(indROI))
    thisROI = np.load(fName)
    plot_calcium_tuning(thisROI)
    figFn = os.path.join(saveDir, 'imag003_ROI_{}.png'.format(indROI))
    # plt.savefig(figFn)
