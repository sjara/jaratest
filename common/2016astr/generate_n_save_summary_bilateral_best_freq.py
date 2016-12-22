'''
Generate and store intermediate data for plot showing frequency-selectivity of astr neurons recorded in the left versus the right hemisphere (using photostim mice). Each mouse and hemisphere is an individual item in the final npz file.
Lan Guo20161221
'''

import os
import numpy as np
import pandas as pd
from jaratoolbox import settings

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
tuningFilename = '/home/languo/data/behavior_reports/photostim_response_freq_summary.csv'
tuning_df = pd.read_csv(tuningFilename)

resultsDict = {}
### Recalculate 'most_responsive_freq' as log2 distance to psycurve boundary ###
for animal in freqBoundaryEachAnimal.keys():
    tuning_df.loc[tuning_df['animalName']==animal,'most_responsive_freq'] = np.log2(tuning_df.loc[tuning_df['animalName']==animal,'most_responsive_freq'])-np.log2(freqBoundaryEachAnimal[animal]) 
    resultsDict['{}_left'.format(animal)] = tuning_df.loc[(tuning_df['animalName']==animal) & (tuning_df['stim_hemi']==1),'most_responsive_freq'].dropna().values
    resultsDict['{}_right'.format(animal)] = tuning_df.loc[(tuning_df['animalName']==animal) & (tuning_df['stim_hemi']==2),'most_responsive_freq'].dropna().values


### Save data ###
outputDir = '/home/languo/data/mnt/figuresdata'
outputFile = 'summary_bilateral_best_freq.npz'
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, **resultsDict)
