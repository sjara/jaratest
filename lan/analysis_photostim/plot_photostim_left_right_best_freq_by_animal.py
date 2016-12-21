

import numpy as np
import pandas as pd
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt

#d1pi014:7.3-16.3kHz, d1pi015:6.2-19.2kHz, d1pi016:mostly 7-22kHz
freqBoundaryEachAnimal = {'d1pi014':10.908,
                          'd1pi015':10.911,
                          'd1pi016':12.410}

tuningFilename = '/home/languo/data/behavior_reports/photostim_response_freq_summary.csv'
tuning_df = pd.read_csv(tuningFilename)

for animal in freqBoundaryEachAnimal.keys():
    tuning_df.loc[tuning_df['animalName']==animal,'most_responsive_freq'] = np.log2(tuning_df.loc[tuning_df['animalName']==animal,'most_responsive_freq'])-np.log2(freqBoundaryEachAnimal[animal])

'''                                                                                
grid = sns.FacetGrid(data=tuning_df, col='animalName')
grid.map(sns.swarmplot,'stim_hemi','most_responsive_freq')
grid.axes[0,0].set_ylabel('log2 distance between\nbest freq and boundary')                #grid.set(xticklabels=['left','right'])                                     
#plt.ylabel('log2 distance \n(best freq - psycurve boundary)')#this only changes the last subplot
'''

grid = sns.FacetGrid(data=tuning_df, hue='animalName')
grid.map(sns.swarmplot,'stim_hemi','most_responsive_freq')
grid.axes[0,0].set_ylabel('log2 distance between\nbest freq and boundary')
plt.xlabel('Recorded hemisphere')
plt.xticks([0,1],['left hemi','right hemi'])
mrf_left = tuning_df['most_responsive_freq'][tuning_df['stim_hemi']==1].dropna()
mrf_right = tuning_df['most_responsive_freq'][tuning_df['stim_hemi']==2].dropna()

(x,pvalue) = stats.ranksums(mrf_left,mrf_right)
plt.suptitle('all three mice left vs right hemi best freq\n p = {}'.format(str(pvalue)))
plt.show()


