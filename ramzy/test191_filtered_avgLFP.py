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


subject = 'poni004'
studyName = 'patternedOpto'
pDepth = 3000
PROCESSED_DATA_DIR = 'C:\\tmpdata'
OUTPUT_DIR = os.path.join(PROCESSED_DATA_DIR,f'{subject}_lfp')
# PROCESSED_DATA_DIR = os.path.join(settings.EPHYS_NEUROPIX_PATH, 'poni004_lfp')
# PROCESSED_DATA_DIR = os.path.join('/Volumes/CrucialX10','Jaralab','data',f'{subject}_lfp')
# OUTPUT_DIR = os.path.join(settings.FIGURES_DATA_PATH,studyName,f'{subject}_lfp')

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

# -- Load data --

# behavSession = '20250310a' # freq
# behavSession = '20250310b' # am
#behavSession = '20250310c' # freq
# behavSession = '20250310d' # am
# behavSession = '20250409a' # freq
# behavSession = '20250409b' # am
# behavSession = '20250428a' # freq
# behavSession = '20250428b' # am
# behavSession = '20250428c' # freq
# behavSession = '20250428d' # am

# behavSession = '20250602a' # freq
# behavSession = '20250602a_sloc' # soundloc

# behavSession = '20250606a' # freq left
# behavSession = '20250606b' # freq binaural
# behavSession = '20250606c' # am left
# behavSession = '20250606d' # am binaural
# behavSession = '20250606a_naturalSound' # left
# behavSession = '20250606b_naturalSound' # binaural

# behavSession = '20250607a' #1a tones
# behavSession = '20250607b' #2a tones
# behavSession = '20250607c' # 3a tones
# behavSession = '20250607d' # 4a tones
# behavSession = '20250607e' # 1a am
# behavSession = '20250607f' # 2a am
# behavSession = '20250607g' # 3a am
# behavSession = '20250607h' # 4a am
# behavSession = '20250607i' # bank 385-480 tones
# behavSession = '20250607j' # bank 385-480 AM
# behavSession = '20250610a-laser' # optoFreq, 3-4_1-192
# behavSession = '20250610b-laser' # optoAM bank 1-192 shanks 3/4
# behavSession = '20250613a-laser' # optoNaturalSound, 3-4_1-192
# behavSession = '20250630c'
# behavSession = '20250718a'
behavSession = '20250807a'

paradigm = 'tuningFreq'
# paradigm = 'tuningAM'
# paradigm = 'soundLocation'
# paradigm = 'naturalSound'
# paradigm = 'poniSpont'

dataFile = os.path.join(PROCESSED_DATA_DIR, f'{subject}_{behavSession}_avgLFP.npz')

dataLFP = np.load(dataFile)
avgLFP = dataLFP['avgLFP']
timeVec = dataLFP['timeVec']
sampleRate = dataLFP['sampleRate']
nChannels = dataLFP['nChannels']
possibleStim = dataLFP['possibleStim']
labelsAvgLFP = dataLFP['labelsAvgLFP']
if len(labelsAvgLFP)==4:
    possibleLaser = dataLFP['possibleLaser']

else:
    possibleLaser = ''

subject = str(dataLFP['subject'])
ephysSession = str(dataLFP['ephysSession'])
print(ephysSession)

# -- Load probe map --
rawDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject, ephysSession)
# ksDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, 
#                                  subject, 
#                                  ephysSession+"_processed_multi")

ksDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, 
                                 'poni001', 
                                 "2025-06-09_11-10-08_processed_multi")

if os.path.exists(rawDataPath):
    xmlfile = os.path.join(rawDataPath, 'Record Node 101', 'settings.xml')

elif os.path.exists(ksDataPath):
    xmlfile = os.path.join(ksDataPath, 'info', 'settings.xml')

else:
    print('Please make sure there is a settings.xml file in your neuropixels ephys data directory.')    
    exit(1)

probeMap = loadneuropix.ProbeMap(xmlfile)


# -- Sort channels according to depth & shank--
''' 
Ordering of the rows in avgLFP do not match that of probeMap, so we need some kind of conversion 
between them. For some row, i, in avgLFP, chanOrder[i] gives its corresponding index in the 
various lists contained in probeMap (e.g., probeMap.ypos[chanOrder[10]] gives the y position of
the channel at avgLFP[10]).
'''

chanOrder = np.argsort(probeMap.channelID)          # conversion between LFP and probeMap

sortedChannels = sorted(list(np.arange(0,nChannels)),
                        key = lambda x: probeMap.ypos[chanOrder[x]]*(100**probeMap.channelShank[chanOrder[x]]))

### Alternative method ///
# yPosNewOrder = probeMap.ypos[chanOrder]
# yPosOrder = np.argsort(yPosNewOrder)

# -- Split channels according to shank -- 
# shankDict = {}
# for i in yPosOrder: 
#     shank = probeMap.channelShank[chanOrder[i]]     # get current shank
#     if shank not in shankDict: 
#         shankDict[shank] = []                       # make new list if needed
#     shankDict[shank].append(i)                      # append to correspond shank's list of channel indices

# # -- Concatenate into sortedChannels list --
# sortedChannels = np.concatenate([shankDict[i] for i in range(4) if i in shankDict])

### ///


# -- Subtract baseline --

if len(avgLFP.shape)==4:
    nLaser = avgLFP.shape[3]
    nStim = len(possibleStim)
    # baselineRange = [-0.2, 0]
    # baselineSamples = np.logical_and(timeVec >= baselineRange[0], timeVec < baselineRange[1])
    # baseline = np.mean(avgLFP[:, baselineSamples, :,:], axis=1)
    # avgLFPnobase = avgLFP - baseline[:, np.newaxis, :,:]

    # sortedAvgLFP = avgLFPnobase[:, :, sortedChannels,:]

    # colorLimit = max(abs(avgLFPnobase.max()), abs(avgLFPnobase.min()))/2
    # clim = [-colorLimit, colorLimit]

    colorLimit = []
    clim = []
    sortedAvgLFP = []
    for indLaser in range(nLaser):
        baselineRange = [-0.2, 0]
        baselineSamples = np.logical_and(timeVec >= baselineRange[0], timeVec < baselineRange[1])
        baseline = np.mean(avgLFP[:, baselineSamples, :,:], axis=1)
        avgLFPnobase = avgLFP[:,:,:,indLaser] - baseline[:, np.newaxis, :,indLaser]

        sortedAvgLFP.append(avgLFPnobase[:, :, sortedChannels])

        colorLimit = max(abs(avgLFPnobase.max()), abs(avgLFPnobase.min()))/2
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
        plt.figure(figsize=(24,12))
        for indLaser in range(nLaser):
            for indStim in range(nStim):
                ax = plt.subplot(int(np.ceil(nStim/4)), 4*nLaser, 2*indStim+indLaser+1)
                plt.imshow(sortedAvgLFP[indLaser][indStim, :, :].T, aspect='auto', origin='lower',
                        extent=[timeVec[0], timeVec[-1], 0, nChannels], clim=clim)
                
                #plt.imshow([[0]])
                plt.axvline(0, color='1', alpha=0.5)
                plt.xlabel('Time (s)')
                plt.ylabel('Channel')
                if 'Freq' in paradigm:
                    plt.title(f'{possibleStim[indStim]/1000:0.1f} kHz, Laser {indLaser}')
                elif 'AM' in paradigm:
                    plt.title(f'{possibleStim[indStim]} Hz, Laser {indLaser}')
                else:
                    plt.title(f'{possibleStim[indStim]}, Laser {indLaser}')

                # ax.set_yticks(np.arange(96, nChannels+96,96), [1,2,3,4])
                ax.set_yticks(np.arange(0, nChannels,24),
                                pDepth-probeMap.ypos[chanOrder[sortedChannels]][0:nChannels:24])
                
                ax.label_outer()
                cbar = plt.colorbar()
                cbar.ax.set_ylabel('μV', rotation=0, va='center', labelpad=-5)
        plt.suptitle(f'Average LFP: {subject} {ephysSession} ({behavSession})', fontweight='bold')
        plt.tight_layout()
        plt.close(1)

    if 1:
        # -- Save figure --
        figFormat = 'png'
        figFilename = f'{subject}_{ephysSession}_{behavSession}_avgLFP'
        extraplots.save_figure(figFilename, figFormat, [24, 12], outputDir=OUTPUT_DIR,
                            facecolor='w')
        plt.show()

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

else:
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
        plt.figure(figsize=(24,12))
        if 'spont' in paradigm.lower():
            sortedStims = sorted(list(possibleStim),
                                    key = lambda x: int(x[3])*10 + int(x[1]) if x!='off' else 0)
            possibleStim = sortedStims
        for indStim in range(len(possibleStim)):
            ax = plt.subplot(4, 4, indStim+1)
            plt.imshow(sortedAvgLFP[indStim, :, :].T, aspect='auto', origin='lower',
                    extent=[timeVec[0], timeVec[-1], 0, nChannels], clim=clim)
            #plt.imshow([[0]])
            plt.axvline(0, color='1', alpha=0.5)
            plt.xlabel('Time (s)')
            plt.ylabel('Channel')
            if 'Freq' in paradigm:
                plt.title(f'{possibleStim[indStim]/1000:0.1f} kHz')
            elif 'AM' in paradigm:
                plt.title(f'{possibleStim[indStim]} Hz')
            else:
                plt.title(f'{possibleStim[indStim]}')

            # ax.set_yticks(np.arange(96, nChannels+96,96), [1,2,3,4])
            ax.set_yticks(np.arange(0, nChannels,24),
                            pDepth-probeMap.ypos[chanOrder[sortedChannels]][0:nChannels:24])
            
            ax.label_outer()
            cbar = plt.colorbar()
            cbar.ax.set_ylabel('μV', rotation=0, va='center', labelpad=-5)
        plt.suptitle(f'Average LFP: {subject} {ephysSession} ({behavSession})', fontweight='bold')
        plt.tight_layout()
        plt.close(1)

    if 1:
        # -- Save figure --
        figFormat = 'png'
        figFilename = f'{subject}_{ephysSession}_{behavSession}_avgLFP'
        extraplots.save_figure(figFilename, figFormat, [24, 12], outputDir=OUTPUT_DIR,
                            facecolor='w')
        plt.show()

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

