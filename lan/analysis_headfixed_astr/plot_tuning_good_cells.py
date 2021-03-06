import os
import pandas as pd
import numpy as np
from scipy import stats
from jaratoolbox import settings
from jaratest.nick.database import dataloader_v2 as dataloader
from jaratest.lan.Ephys import dataplotter_vlan as dataplotter
reload(dataplotter)
from jaratest.lan.analysis_reward_change import reward_change_loader_plotter_functions as rcfuncs
reload(rcfuncs)
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

animal = 'adap041'
noiseburstSessType = 'noiseburst'
tuningSessType = 'tc'

databaseFullPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(animal))
key = 'head_fixed'
qualityThreshold = 3 #2
maxZThreshold = 2
ISIcutoff = 0.02
tuningIntensity = [60,50,40,30] #range(30,70,10)
celldb = pd.read_hdf(databaseFullPath, key=key)

goodQualCells = celldb.query("isiViolations<{} and shapeQuality>{} and astrRegion!='undetermined'".format(ISIcutoff, qualityThreshold))
maxZscore = goodQualCells.ZscoreEachIntensity.apply(lambda x : np.max(np.abs(x)))
goodRespCells=goodQualCells[maxZscore >= maxZThreshold]

#goodRespCells = goodQualCells.loc[abs(goodQualCells.tuningZscore) >= maxZThreshold]
outputDir = '/home/languo/data/ephys/head_fixed_astr/all_mice/responsive_cells'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

# -- Plot reports ONLY for sound responsive cells-- #
for ind, cell in goodRespCells.iterrows():
    tetrode = int(cell.tetrode)
    cluster = int(cell.cluster)
    date = cell.date
    depth = cell.depth
    brainArea = cell.brainarea
    astrRegion = cell.astrRegion
    #bestFreq = cell.tuningWeightedBFEachIntensity
    figname = '{}_{}_{}_{}_{}_T{}c{}'.format(animal,brainArea,astrRegion, depth,date,tetrode,cluster)     
    
    if os.path.exists(os.path.join(outputDir, figname)):
        continue
    else:
        print 'ploting {}'.format(figname)
        tuningSessInd = cell.sessiontype.index(tuningSessType)
        tuningEphys = cell.ephys[tuningSessInd]
        tuningBehav = cell.behavior[tuningSessInd]
        noiseSessInd = cell.sessiontype.index(noiseburstSessType)
        noiseEphys = cell.ephys[noiseSessInd]
        plt.figure(figsize=(18,18))
        gs = gridspec.GridSpec(2,2)
        gs.update(left=0.1, right=0.9, wspace=0.3, hspace=0.3)
        gs00 = gridspec.GridSpecFromSubplotSpec(4, 4, subplot_spec=gs[:,1], hspace=0.1)

        # Plot spike quality summary graphs
        ax = plt.subplot(gs[0, 0])
        rcfuncs.plot_waveform_each_cluster(animal, tuningEphys, tetrode, cluster)
        plt.title('quality score:{}'.format(cell.shapeQuality))

        # Plot noise bursts
        ax = plt.subplot(gs[1,0])
        rcfuncs.plot_noisebursts_response_raster(animal, noiseEphys, tetrode, cluster)

        # Plot sorted tuning raster
        for ind,intensity in enumerate(tuningIntensity):
            ax = plt.subplot(gs00[ind, :])
            rcfuncs.plot_tuning_raster(animal, tuningEphys, tuningBehav, tetrode, cluster, intensity=intensity, timeRange = [-0.35,0.75])
            #if ind == 0:
                #plt.title('weighted best freq:{}'.format(bestFreq))
        plt.suptitle(figname)
        # Save figure

        #figname = '{}_{}_T{}_c{}_headfixed_astr.png'.format(animal,date,tetrode,cluster)
        figFullPath = os.path.join(outputDir, figname)
        plt.savefig(figFullPath, format='png')
        print 'Saving figure {}'.format(figname)
