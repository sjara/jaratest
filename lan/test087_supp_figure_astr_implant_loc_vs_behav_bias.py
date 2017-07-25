import os
import numpy as np
from jaratoolbox import settings
from matplotlib import pyplot as plt
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
