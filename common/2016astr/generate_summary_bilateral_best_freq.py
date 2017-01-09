'''
Generate and store intermediate data for plot showing frequency-selectivity of astr neurons recorded in the left versus the right hemisphere (using photostim mice). Each mouse and hemisphere is an individual item in the final npz file.
Lan Guo20161221
'''

import os
import numpy as np
import pandas as pd
from jaratoolbox import settings
reload(settings)
import figparams

scriptFullPath = os.path.realpath(__file__)

# Psycurve frequencies used in 2afc task: d1pi014:7.3-16.3kHz, d1pi015:6.2-19.2kHz, d1pi016:mostly 7-22kHz; 6 frequencies were used in the task
numFreqs = 6
freqs014 = np.logspace(np.log2(7.3), np.log2(16.3), base=2, num=numFreqs)
freqs015 = np.logspace(np.log2(6.2), np.log2(19.2), base=2, num=numFreqs)
freqs016 = np.logspace(np.log2(7), np.log2(22), base=2, num=numFreqs)

# -- Psycurve boundary calculated as equal log distance to either of the middle frequencies used in 2afc task -- #
boundary014 = np.logspace(np.log2(freqs014[numFreqs/2-1]), np.log2(freqs014[numFreqs/2]), base=2, num=3)[1]
boundary015 = np.logspace(np.log2(freqs015[numFreqs/2-1]), np.log2(freqs015[numFreqs/2]), base=2, num=3)[1]
boundary016 = np.logspace(np.log2(freqs016[numFreqs/2-1]), np.log2(freqs016[numFreqs/2]), base=2, num=3)[1]
freqBoundaryEachAnimal = {'d1pi014':boundary014,
                          'd1pi015':boundary015,
                          'd1pi016':boundary016}

# -- Load database containing quantifications of tuning -- #
tuingFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
tuningFileName = 'photostim_response_freq_summary.csv'
tuningFullPath = os.path.join(tuingFilePath,tuningFileName)
tuning_df = pd.read_csv(tuningFullPath)

resultsDict = dict(freqs014=freqs014, freqs015=freqs015, freqs016=freqs015, boundary014=boundary014, boundary015=boundary015, boundary016=boundary016, tuningDatabase=tuningFileName, script=scriptFullPath)

### Recalculate 'most_responsive_freq' as log2 distance to psycurve boundary ###
for animal in freqBoundaryEachAnimal.keys():
    tuning_df.loc[tuning_df['animalName']==animal,'most_responsive_freq'] = np.log2(tuning_df.loc[tuning_df['animalName']==animal,'most_responsive_freq'])-np.log2(freqBoundaryEachAnimal[animal]) 
    resultsDict['{}_left'.format(animal)] = tuning_df.loc[(tuning_df['animalName']==animal) & (tuning_df['stim_hemi']==1),'most_responsive_freq'].dropna().values
    resultsDict['{}_right'.format(animal)] = tuning_df.loc[(tuning_df['animalName']==animal) & (tuning_df['stim_hemi']==2),'most_responsive_freq'].dropna().values


### Save data ###
outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'summary_bilateral_best_freq.npz'
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, **resultsDict)
