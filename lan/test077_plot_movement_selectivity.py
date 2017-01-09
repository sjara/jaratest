import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

allcells_switching = pd.read_hdf('/home/languo/data/ephys/switching_summary_stats/all_cells_all_measures_extra_mod_waveform_switching.h5',key='switching')

allcells_psychometric = pd.read_hdf('/home/languo/data/ephys/psychometric_summary_stats/all_cells_all_measures_psychometric.h5',key='psychometric')

# Custom function for plotting median of data series as vertical line
def plot_median_axvline(data, **kwargs):
    median = np.median(data)
    ymin, ymax = plt.ylim()
    plt.axvline(median, ymin, ymax, **kwargs)
    

for ind,allcells in enumerate([allcells_switching,allcells_psychometric]):
    #plt.figure()
    allcells = allcells[allcells.cellQuality.isin([1,6])] #just look at the good cells
    sigMod = np.array((allcells.movementModS<=0.05), dtype=bool)

    
    dataToPlot = pd.DataFrame({'selective':sigMod, 'animalName':allcells.animalName, 'movementModI':allcells.movementModI})
    
    #g = sns.FacetGrid(dataToPlot, col='animalName', hue='selective', hue_kws={"color":['blue','red']}, sharey=False)
    g = sns.FacetGrid(dataToPlot, col='animalName', row='selective', sharey=False, sharex=False)
    g.map(plt.hist, 'movementModI', edgecolor='k',alpha=0.5,bins=50,stacked=True)
    g.map(plot_median_axvline, 'movementModI', color='grey',ls='dashed',lw=1)
    g.set_ylabels('Number of cells')
    g.set_xlabels('Movement selectivity index')
    plt.suptitle('{} - all good cells'.format(['switching','psychometric'][ind]))
    g.add_legend()
    plt.show()
    '''
    median = np.median(dataToPlot.movementModI[sigMod])
    T,p = stats.wilcoxon(dataToPlot.movementModI[sigMod])
    print 'For {} cells, median movement index is: {}, p value is: {}'.format(['switching','psychometric'][ind],median,p)
    '''
