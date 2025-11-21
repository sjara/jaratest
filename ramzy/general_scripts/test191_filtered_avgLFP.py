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
pDepth = 4000
# PROCESSED_DATA_DIR = 'C:\\tmpdata'
PROCESSED_DATA_DIR = os.path.join(settings.EPHYS_NEUROPIX_PATH, f'{subject}_lfp')
# PROCESSED_DATA_DIR = os.path.join('/Volumes/CrucialX10','Jaralab','data',f'{subject}_lfp')
OUTPUT_DIR = os.path.join(settings.FIGURES_DATA_PATH,studyName,f'{subject}_lfp')
# OUTPUT_DIR = os.path.join(PROCESSED_DATA_DIR,f'{subject}_lfp')

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

# -- Load data --

#ephysSession = '2025-03-10_15-30-45'; behavSession = '20250310a' # Shank 1a, tones
#ephysSession = '2025-03-10_16-17-01'; behavSession = '20250310e' # Shank 1a, AM
# ephysSession = '2025-03-10_15-43-57'; behavSession = '20250310b' # Shank 2a, tones
#ephysSession = '2025-03-10_15-55-03'; behavSession = '20250310c' # Shank 3a, tones
#ephysSession = '2025-03-10_16-06-35'; behavSession = '20250310d' # Shank 4a, tones
# ephysSession = '2025-04-09_12-27-15'; behavSession = '20250409a' # bank 385-480, tones
# ephysSession = '2025-04-09_12-35-59'; behavSession = '20250409b' # bank 385-480, AM
# ephysSession = '2025-04-09_12-43-46'; behavSession = '20250409a' # bank 385-480, naturalSound

# ephysSession = '2025-04-28_15-25-36'; behavSession = '20250428a' # shank1b extref, tones
# ephysSession = '2025-04-28_15-33-55'; behavSession = '20250428b' # shank1b extref, AM
# ephysSession = '2025-04-28_15-42-06'; behavSession = '20250428c' # shank1b, tones
# ephysSession = '2025-04-28_15-50-41'; behavSession = '20250428d' # shank1b, AM
# ephysSession = '2025-04-28_15-58-13'; behavSession = '20250428a' # shank1b, naturalSound

# ephysSession = '2025-06-02_11-09-19'; behavSession = '20250602a' # bank 385-480, soundLocalization
# ephysSession = '2025-06-02_11-41-31'; behavSession = '20250602a' # bank 385-480, tones
# ephysSession = '2025-06-06_15-06-39'; behavSession = '20250606a' # bank 385-480, tones left
# ephysSession = '2025-06-06_15-15-30'; behavSession = '20250606b' # bank 385-480, tones binaural
# ephysSession = '2025-06-06_15-32-30'; behavSession = '20250606c' # bank 385-480, AM left
# ephysSession = '2025-06-06_15-41-24'; behavSession = '20250606d' # bank 385-480, AM binaural
# ephysSession = '2025-06-06_15-49-33'; behavSession = '20250606a' # bank 385-480, nats left
# ephysSession = '2025-06-06_16-16-12'; behavSession = '20250606b' # bank 385-480, nats binaural

# ephysSession = '2025-06-07_14-07-32'; behavSession = '20250607a' # tones, shank1a
# ephysSession = '2025-06-07_14-16-23'; behavSession = '20250607b' # tones, shank2a
# ephysSession = '2025-06-07_14-25-37'; behavSession = '20250607c' # tones, shank3a
# ephysSession = '2025-06-07_14-36-14'; behavSession = '20250607d' # tones, shank4a
# ephysSession = '2025-06-07_14-45-38'; behavSession = '20250607e' # AM, shank1a
# ephysSession = '2025-06-07_14-55-28'; behavSession = '20250607f' # AM, shank2a
# ephysSession = '2025-06-07_15-03-36'; behavSession = '20250607g' # AM, shank3a
# ephysSession = '2025-06-07_15-11-28'; behavSession = '20250607h' # AM, shank4a
# ephysSession = '2025-06-07_15-22-13'; behavSession = '20250607i' # tones, bank 385-480
# ephysSession = '2025-06-07_15-30-29'; behavSession = '20250607j' # AM, bank 385-480
# ephysSession = '2025-06-10_16-07-57'; behavSession = '20250610b' # soundloc, 3-4_1-192
# ephysSession = '2025-06-10_17-20-19'; behavSession = '20250610a' # optoFreq, 3-4_1-192
# ephysSession = '2025-06-10_17-39-32'; behavSession = '20250610b' # optoAM,3-4_1-192
# ephysSession = '2025-06-30_14-59-47'; behavSession = '20250630c' # poniSpont
# ephysSession = '2025-07-18_15-42-52'; behavSession = '20250718a' # poniSpont

# ephysSession = '2025-08-07_17-24-38'; behavSession = '20250807a' # tuningFreq shank 2 bank A
ephysSession = '2025-08-07_18-11-51'; behavSession = '20250807e' # shank 2 bank A parallel
# ephysSession = '2025-08-07_19-48-18'; behavSession = '20250807i' # 1-96 perp
# ephysSession = '2025-08-07_19-57-16'; behavSession = '20250807j' # shank 4 bank A perp
# ephysSession = '2025-08-07_19-36-04'; behavSession = '20250807h' # shank 4 bank A perp Freq
# ephysSession = '2025-08-07_20-08-00'; behavSession = '20250807k' # 97-192 perp
# ephysSession = '2025-08-07_20-17-40'; behavSession = '20250807l' # 193-288 perp
# ephysSession = '2025-08-07_20-27-43'; behavSession = '20250807m' # 289-384 perp

# ephysSession = '2025-08-07_17-53-33'; behavSession = '20250807c' # shank 3 bank A parallel Freq
# ephysSession = '2025-08-07_18-21-12'; behavSession = '20250807f' # shank 3 bank A parallel optoAM

# paradigm = 'tuningFreq'
paradigm = 'tuningAM'
# paradigm = 'soundLocation'
# paradigm = 'naturalSound'
# paradigm = 'poniSpont'

dataFile = os.path.join(PROCESSED_DATA_DIR, f'{subject}_{behavSession}_avgLFP.npz')

dataLFP = np.load(dataFile)
avgLFP = dataLFP['avgLFP']
timeVec = dataLFP['timeVec']
sampleRate = int(dataLFP['sampleRate'])
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
# rawDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject, ephysSession)
rawDataPath = os.path.join('/Volumes/CrucialX10','Jaralab','data',subject,ephysSession)
ksDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, 
                                 subject, 
                                 ephysSession+"_processed_multi")

# ksDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, 
#                                  'poni001', 
#                                  "2025-06-09_11-10-08_processed_multi")

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
    climAll = []
    sortedAvgLFP = []

    

    for indLaser in range(nLaser):
        baselineRange = [-0.2, 0]
        baselineSamples = np.logical_and(timeVec >= baselineRange[0], timeVec < baselineRange[1])
        baseline = np.mean(avgLFP[:, baselineSamples, :,:], axis=1)
        avgLFPnobase = avgLFP[:,:,:,indLaser] - baseline[:, np.newaxis, :,indLaser]

        FILTER = 0

        if FILTER:
            # -- Filter avgLFP --
            print('Filtering avgLFP...')
            highcut = 300
            bCoeff, aCoeff = signal.iirfilter(4, Wn=highcut, fs=sampleRate, btype="low", ftype="butter")
            avgLFPnobase = signal.filtfilt(bCoeff, aCoeff, avgLFPnobase, axis=1)
            #sys.exit()

        sortedAvgLFP.append(avgLFPnobase[:, :, sortedChannels])

        

        if indLaser:
            # baselineSamples = np.logical_and(timeVec >= 0, timeVec < 1)
            # baseline = np.mean(avgLFPnobase[:, baselineSamples, :], axis=0)
            # for i in range(avgLFPnobase.shape[0]):
            #     avgLFPnobase[i,baselineSamples,:] = avgLFPnobase[i,baselineSamples,:] - baseline[:, np.newaxis, :]
            postArtifactSamples = np.logical_and(timeVec >= 0.1, timeVec <= 0.4)
            colorLimit = max(max(abs(avgLFPnobase[:,postArtifactSamples,:].max()), 
                            abs(avgLFPnobase[:,postArtifactSamples,:].min()))//2,50)
        
        else:
            colorLimit = max(abs(avgLFPnobase.max()), 
                            abs(avgLFPnobase.min()))//2
        
        # colorLimit = max(abs(np.percentile(avgLFPnobase[:,postArtifactSamples,:],99)),
        #                  abs(np.percentile(avgLFPnobase[:,postArtifactSamples,:],1)))


        # colorLimit = max(abs(np.percentile(avgLFPnobase,99)),
        #                   abs(np.percentile(avgLFPnobase,1)))

        climAll.append([-colorLimit, colorLimit])


    

    if 1:
        print('Plotting responses for all stimuli...')
        plt.clf()
        plt.figure(figsize=(24,12))
        for indLaser in range(nLaser):
            clim = climAll[indLaser]
            for indStim in range(nStim):
                ax = plt.subplot(int(np.ceil(nStim/2)), 2*nLaser, 2*indStim+indLaser+1)
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
        plt.suptitle(f'Average LFP: {subject} {ephysSession} ({behavSession},shank{str(np.unique(probeMap.channelShank)+1)[1:-1]})', fontweight='bold')
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
        plt.suptitle(f'Average LFP: {subject} {ephysSession} ({behavSession},shank{str(np.unique(probeMap.channelShank)+1)[1:-1]})', fontweight='bold')
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

