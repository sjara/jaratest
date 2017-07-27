import os
import numpy as np
from jaratoolbox import settings
from matplotlib import pyplot as plt
import scipy.stats as stats
#import figparams

STUDY_NAME = '2016astr'
FIGNAME = 'photostim_2afc'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

summaryFilename = 'summary_photostim_percent_right_choice_change.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

# These numbers are percent rightward choice (stim - control) for each condition:
left014 = summary['d1pi014leftHemiStim']
left015 = summary['d1pi015leftHemiStim']
left016 = summary['d1pi016leftHemiStim']
right014 = summary['d1pi014rightHemiStim']
right015 = summary['d1pi015rightHemiStim']
right016 = summary['d1pi016rightHemiStim']

left014sessions = summary['d1pi014leftHemiStimSessions']
left015sessions = summary['d1pi015leftHemiStimSessions']
left016sessions = summary['d1pi016leftHemiStimSessions']
right014sessions = summary['d1pi014rightHemiStimSessions']
right015sessions = summary['d1pi015rightHemiStimSessions']
right016sessions = summary['d1pi016rightHemiStimSessions']

SHAPES = {'d1pi014':'s',
          'd1pi015':'o',
          'd1pi016':'^'}

# -- Plot contralateral bias vs location (on the left or right side in relation to center) -- #
# location based on histology:
locationDict = {'left014': 'center',
                'right014': 'right of center',
                'left015': 'left of center', 
                'right015': 'right of center',
                'left016': 'left of center',
                'right016': 'center'}

contraLeft014 = left014
contraLeft015 = left015
contraLeft016 = left016
#This is a rough estimate of % leftward bias assuming %right+%left choices sum up to 100%:
contraRight014 = -right014 
contraRight015 = -right015
contraRight016 = -right016

np.random.seed(7)
plt.clf()
for animal,leftToCenterData in zip(['d1pi015','d1pi016'],[contraLeft015,contraLeft016]):
    randOffset = 0.3*(np.random.rand(len(leftToCenterData))-0.5)
    plt.plot(1+randOffset, 100*leftToCenterData, SHAPES[animal], mec='k', mfc='None')

for animal,rightToCenterData in zip(['d1pi014','d1pi015'],[contraRight014,contraRight015]):
    randOffset = 0.3*(np.random.rand(len(rightToCenterData))-0.5)
    plt.plot(3+randOffset, 100*rightToCenterData, SHAPES[animal], mec='k', mfc='None')

for animal,centerData in zip(['d1pi014','d1pi016'],[contraLeft014,contraRight016]):
    randOffset = 0.3*(np.random.rand(len(centerData))-0.5)
    plt.plot(2+randOffset, 100*centerData, SHAPES[animal], mec='k', mfc='None')

plt.xticks([1,2,3], ['left of center', 'center', 'right of center'])
plt.ylabel('Contra lateral bias: stim - control (%)')
plt.show()

# -- Plot contralateral bias vs distance off from center (positive is to lateral, negative is to medial side) -- #
'''
distanceOffCenter = {'d1pi014left':0,
                     'd1pi014right':0.5,
                     'd1pi015left':0.2,
                     'd1pi015right':0.25,
                     'd1pi016left':0.5,
                     'd1pi016right':0}
'''

distanceOffCenter = {'0': {'d1pi014':contraLeft014,
                           'd1pi016':contraRight016},
                     '0.2': {'d1pi015':contraLeft015},
                     '0.25': {'d1pi015':contraRight015},
                     '0.5': {'d1pi014':contraRight014,
                             'd1pi016':contraLeft016}
                     }

plt.figure()
for key, valueDict in distanceOffCenter.items():
    for animal, value in valueDict.items():
        randOffset = 0.1*(np.random.rand(len(value))-0.5)
        plt.plot(float(key)+randOffset, 100*value, SHAPES[animal], mec='k', mfc='None')

plt.xticks([-0.5,0,0.5], ['medial', 'center', 'lateral'])
plt.ylabel('Contra lateral bias: stim - control (%)')
plt.show()


# -- Plot rightward bias vs distance off from center (positive is to lateral, negative is to medial side) -- #
distanceOffCenter = {'0': {'d1pi014':left014,
                           'd1pi016':right016},
                     '0.2': {'d1pi015':left015},
                     '0.25': {'d1pi015':right015},
                     '0.5': {'d1pi014':right014,
                             'd1pi016':left016}
                     }

plt.figure()
for key, valueDict in distanceOffCenter.items():
    for animal, value in valueDict.items():
        randOffset = 0.1*(np.random.rand(len(value))-0.5)
        plt.plot(float(key)+randOffset, 100*value, SHAPES[animal], mec='k', mfc='None')

plt.xticks([-0.5,0,0.5], ['medial', 'center', 'lateral'])
plt.ylabel('Bias to high freq: stim - control (%)')
plt.show()

# Add median and stats

# -- Plot contralateral bias vs distance off from center (positive is to lateral, negative is to medial side) for each hemisphere -- #
plt.figure()
# Left hemi
distanceOffCenter = {'0': {'d1pi014':contraLeft014},
                     '0.25': {'d1pi015':contraLeft015},
                     '0.5': {'d1pi016':contraLeft016}
                     }

ax1 = plt.subplot(121)
for key, valueDict in distanceOffCenter.items():
    for animal, value in valueDict.items():
        randOffset = 0.1*(np.random.rand(len(value))-0.5)
        plt.plot(float(key)+randOffset, 100*value, SHAPES[animal], mec='k', mfc='None')
        plt.plot(0.2*np.array([-1,1])+float(key), 100*np.tile(np.mean(value),2), lw=2,color='grey')

(Z, pVal) = stats.ranksums(contraLeft015, contraLeft014)
plt.text(-0.25, 40, 'p value between medial \nand lateral: {}'.format(pVal))
plt.xticks([-0.5,0,0.5], ['medial', 'center', 'lateral'])
plt.ylabel('Contra lateral bias: stim - control (%)')
plt.title('Left hemisphere')

# Right hemi
distanceOffCenter = {'0': {'d1pi016':contraRight016},
                     '0.25': {'d1pi015':contraRight015},
                     '0.5': {'d1pi014':contraRight014}
                     }

ax2 = plt.subplot(122)
for key, valueDict in distanceOffCenter.items():
    for animal, value in valueDict.items():
        randOffset = 0.1*(np.random.rand(len(value))-0.5)
        plt.plot(float(key)+randOffset, 100*value, SHAPES[animal], mec='k', mfc='None')
        plt.plot(0.2*np.array([-1,1])+float(key), 100*np.tile(np.mean(value),2), lw=2, color='grey')

(Z, pVal) = stats.ranksums(contraRight016, contraRight015)
plt.text(-0.25, 40, 'p value between medial \nand lateral: {}'.format(pVal))
plt.xticks([-0.5,0,0.5], ['medial edge', 'center', 'lateral edge'])
plt.ylabel('Contra lateral bias: stim - control (%)')
plt.title('Right hemisphere')
plt.show()

# -- Plot relationship between tuning freq and rightward bias -- #
STUDY_NAME = '2016astr'
FIGNAME = 'sound_freq_selectivity'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

summaryFilename = 'summary_bilateral_best_freq.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

left014Freqs = summary['d1pi014_left']
left015Freqs = summary['d1pi015_left']
left016Freqs = summary['d1pi016_left']
right014Freqs = summary['d1pi014_right']
right015Freqs = summary['d1pi015_right']
right016Freqs = summary['d1pi016_right']
left014FreqsSessions = summary['d1pi014_left_sessions']
left015FreqsSessions = summary['d1pi015_left_sessions']
left016FreqsSessions = summary['d1pi016_left_sessions']
right014FreqsSessions = summary['d1pi014_right_sessions']
right015FreqsSessions = summary['d1pi015_right_sessions']
right016FreqsSessions = summary['d1pi016_right_sessions']

## checked and make sure the sessions for behavior and frequency data matched up
allFreqs = np.concatenate([left014Freqs, left015Freqs, left016Freqs, right014Freqs, right015Freqs, right016Freqs])
allRightBias = 100*np.concatenate([left014, left015, left016, right014, right015, right016])

plt.figure()
plt.scatter(allFreqs[~np.isnan(allFreqs)], allRightBias[~np.isnan(allFreqs)])
plt.xlabel('Preferred frequency to boundary (octaves)')
plt.ylabel('Bias to high freq: stim - control (%)')
plt.xlim([-1.7, 1.7])
r, pVal = stats.spearmanr(allFreqs[~np.isnan(allFreqs)], allRightBias[~np.isnan(allFreqs)])
plt.text(-1.0,50, 'p value for spearman correlation test is {}'.format(pVal))
plt.show()

# -- Left hemi -- #
allFreqsLeft = np.concatenate([left014Freqs, left015Freqs, left016Freqs])
allRightBiasLeft = 100*np.concatenate([left014, left015, left016])

plt.figure()
plt.scatter(allFreqsLeft[~np.isnan(allFreqsLeft)], allRightBiasLeft[~np.isnan(allFreqsLeft)])
plt.xlabel('Preferred frequency to boundary (octaves)')
plt.ylabel('Bias to high freq: stim - control (%)')
plt.xlim([-1.7, 1.7])
r, pVal = stats.spearmanr(allFreqsLeft[~np.isnan(allFreqsLeft)], allRightBiasLeft[~np.isnan(allFreqsLeft)])
plt.text(-1.2,45, 'Left hemi: p value for spearman correlation test is {}'.format(pVal))
plt.show()

# -- Right hemi -- #
allFreqsRight = np.concatenate([right014Freqs, right015Freqs, right016Freqs])
allRightBiasRight = 100*np.concatenate([right014, right015, right016])

plt.figure()
plt.scatter(allFreqsRight[~np.isnan(allFreqsRight)], allRightBiasRight[~np.isnan(allFreqsRight)])
plt.xlabel('Preferred frequency to boundary (octaves)')
plt.ylabel('Bias to high freq: stim - control (%)')
plt.xlim([-1.7, 1.7])
r, pVal = stats.spearmanr(allFreqsRight[~np.isnan(allFreqsRight)], allRightBiasRight[~np.isnan(allFreqsRight)])
plt.text(-1.2,15, 'Right hemi: p value for spearman correlation test is {}'.format(pVal))
plt.show()
