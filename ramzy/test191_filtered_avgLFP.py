"""
Load avgLFP saved by test190... and postprocess (subtract baseline and filter).
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from jaratoolbox import settings
from jaratoolbox import loadneuropix
from jaratoolbox import extraplots
from importlib import reload
reload(loadneuropix)


# PROCESSED_DATA_DIR = 'C:\\tmpdata'
PROCESSED_DATA_DIR = '/mnt/c/tmpdata'

# -- Load data --
subject = 'inpi003'
#behavSession = '20250310a'
# behavSession = '20250310b'
#behavSession = '20250310c'
#behavSession = '20250310d'
# behavSession = '20250409a'
behavSession = '20250409b'

dataFile = os.path.join(PROCESSED_DATA_DIR, f'{subject}_{behavSession}_avgLFP.npz')

dataLFP = np.load(dataFile)
avgLFP = dataLFP['avgLFP']
timeVec = dataLFP['timeVec']
sampleRate = dataLFP['sampleRate']
nChannels = dataLFP['nChannels']
possibleStim = dataLFP['possibleStim']
labelsAvgLFP = dataLFP['labelsAvgLFP']
subject = str(dataLFP['subject'])
ephysSession = str(dataLFP['ephysSession'])

# -- Load probe map --
rawDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject, ephysSession)
processedDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, 
                                 subject, 
                                 ephysSession+"_processed_multi")
if os.path.exists(rawDataPath):
    xmlfile = os.path.join(rawDataPath, 'Record Node 101', 'settings.xml')

elif os.path.exists(processedDataPath):
    xmlfile = os.path.join(processedDataPath, 'info', 'settings.xml')

else:
    Exception('Please make sure there is a settings.xml file in your neuropixels ephys data directory.')    
probeMap = loadneuropix.ProbeMap(xmlfile)

# -- Sort channels according to depth --
chanOrder = np.argsort(probeMap.channelID)
yPosNewOrder = probeMap.ypos[chanOrder]
sortedChannels = np.argsort(yPosNewOrder)

# -- Subtract baseline --
baselineRange = [-0.2, 0]
baselineSamples = np.logical_and(timeVec >= baselineRange[0], timeVec < baselineRange[1])
baseline = np.mean(avgLFP[:, baselineSamples, :], axis=1)
avgLFPnobase = avgLFP - baseline[:, np.newaxis, :]

sortedAvgLFP = avgLFPnobase[:, :, sortedChannels]

colorLimit = max(abs(avgLFPnobase.max()), abs(avgLFPnobase.min()))
clim = [-colorLimit, colorLimit]

FILTER = 0
if FILTER:
    # -- Filter avgLFP --
    print('Filtering avgLFP...')
    highcut = 300
    bCoeff, aCoeff = signal.iirfilter(4, Wn=highcut, fs=sampleRate, btype="low", ftype="butter")
    sortedAvgLFP = signal.filtfilt(bCoeff, aCoeff, sortedAvgLFP, axis=1)
    #sys.exit()

if 1:
    print('Plotting responses for all stimuli...')
    plt.clf()
    for indStim in range(len(possibleStim)):
        ax = plt.subplot(4, 4, indStim+1)
        plt.imshow(sortedAvgLFP[indStim, :, :].T, aspect='auto', origin='lower',
                   extent=[timeVec[0], timeVec[-1], 0, nChannels], clim=clim)
        #plt.imshow([[0]])
        plt.axvline(0, color='1', alpha=0.5)
        plt.xlabel('Time (s)')
        plt.ylabel('Channel')
        plt.title(f'{possibleStim[indStim]/1000:0.1f} kHz')
        ax.set_yticks(np.arange(0, nChannels+96, 96))
        ax.label_outer()
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('μV', rotation=0, va='center', labelpad=-5)
    plt.suptitle(f'Average LFP: {subject} {ephysSession} ({behavSession})', fontweight='bold')
    plt.tight_layout()
    plt.show()

if 1:
    # -- Save figure --
    figFormat = 'png'
    figFilename = f'{subject}_{ephysSession}_{behavSession}_avgLFP'
    extraplots.save_figure(figFilename, figFormat, [24, 12], outputDir=PROCESSED_DATA_DIR,
                           facecolor='w')
    
if 0:
    print('Plotting...')
    stimToPlot = 8#11
    plt.clf()
    plt.subplot(211)
    if not FILTER:
        plt.imshow(avgLFPnobase[stimToPlot,:,:].T, aspect='auto', origin='lower',
                   extent=[timeVec[0], timeVec[-1], 0, nChannels])
    else:
        plt.imshow(filteredAvgLFP[stimToPlot,:,:].T, aspect='auto', origin='lower',
                   extent=[timeVec[0], timeVec[-1], 0, nChannels])
    plt.colorbar()
    plt.subplot(212)
    plt.imshow(sortedAvgLFP[stimToPlot,:,:].T, aspect='auto', origin='lower',
               extent=[timeVec[0], timeVec[-1], 0, nChannels])
    plt.colorbar()
    plt.title('Average LFP for {} Hz'.format(possibleStim[stimToPlot]))
    plt.xlabel('Time (s)')
    plt.ylabel('Channel')
    plt.show()

