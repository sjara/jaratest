import os
import pandas as pd
import numpy as np
from scipy import stats
from jaratoolbox import settings
import reward_change_loader_plotter_functions as rcfuncs
reload(rcfuncs)
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

animal = 'gosi008'
tuningSessType = 'tc'
rcSessType = 'behavior'

databaseFullPath = os.path.join(settings.DATABASE_PATH, animal, '{}_database.h5'.format(animal))
key = 'reward_change'
qualityThreshold = 2
maxZThreshold = 3
ISIcutoff = 0.02

gosidb = pd.read_hdf(databaseFullPath, key=key)

goodQualCells = gosidb.query('isiViolations<{} and shapeQuality>{}'.format(ISIcutoff, qualityThreshold))

sigModSoundHigh = goodQualCells.loc[goodQualCells['modSigHigh_0-0.1s_sound']<=0.05]
sigModSoundLow = goodQualCells.loc[goodQualCells['modSigLow_0-0.1s_sound']<=0.05]

sigModCenterOutLeft = goodQualCells.loc[goodQualCells['modSigLow_0-0.1s_center-out']<=0.05]
sigModCenterOutRight = goodQualCells.loc[goodQualCells['modSigHigh_0-0.1s_center-out']<=0.05]


# -- Plot reports -- #
for ind, cell in sigModSoundLow.iterrows():
    outputDir = '/home/languo/data/ephys/reward_change_stats/sig_mod_sound_low/'
    animal = cell.subject
    tuningSessInd = cell.sessiontype.index(tuningSessType)
    tuningEphys = cell.ephys[tuningSessInd]
    tuningBehav = cell.behavior[tuningSessInd]
    rcSessInd = cell.sessiontype.index(rcSessType)
    rcEphys = cell.ephys[rcSessInd]
    rcBehav = cell.behavior[rcSessInd]
    tetrode = int(cell.tetrode)
    cluster = int(cell.cluster)
    date = cell.date
    plt.figure(figsize=(18,12))
    gs = gridspec.GridSpec(2,2)
    gs.update(left=0.1, right=0.9, wspace=0.3, hspace=0.3)
    gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0,1], hspace=0.1)
    gs01 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[1,1], hspace=0.1)

    ax1 = plt.subplot(gs[0, 0])
    rcfuncs.plot_tuning_raster(animal, tuningEphys, tuningBehav, tetrode, cluster, intensity=50, timeRange = [-0.5,1])
    
    # Sound-aligned low freq
    ax2 = plt.subplot(gs00[0:2, :])
    rcfuncs.plot_reward_change_raster(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='low', byBlock=True, alignment='sound', timeRange=[-0.3,0.4])
    plt.title('Modulation index {}\n p value {}'.format(cell['modIndLow_0-0.1s_sound'],cell['modSigLow_0-0.1s_sound']))
    ax3 = plt.subplot(gs00[2, :])
    rcfuncs.plot_reward_change_psth(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='low', byBlock=True, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010)
    # Cout-aligned low freq
    ax4 = plt.subplot(gs01[0:2, :])
    rcfuncs.plot_reward_change_raster(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='low', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Modulation index {}\n p value {}'.format(cell['modIndLow_0-0.1s_center-out'],cell['modSigLow_0-0.1s_center-out']))
    ax5 = plt.subplot(gs01[2, :])
    rcfuncs.plot_reward_change_psth(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='low', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)
    
    # Plot spike quality summary graphs
    ax6 = plt.subplot(gs[1, 0])
    rcfuncs.plot_waveform_each_cluster(animal, rcEphys, tetrode, cluster)
 
    plt.suptitle('Significantly modulated 0-0.1s window after sound onset')
    # Save figure
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath)
   
for ind, cell in sigModSoundHigh.iterrows():
    animal = cell.subject
    tuningSessInd = cell.sessiontype.index(tuningSessType)
    tuningEphys = cell.ephys[tuningSessInd]
    tuningBehav = cell.behavior[tuningSessInd]
    rcSessInd = cell.sessiontype.index(rcSessType)
    rcEphys = cell.ephys[rcSessInd]
    rcBehav = cell.behavior[rcSessInd]
    tetrode = int(cell.tetrode)
    cluster = int(cell.cluster)
    date = cell.date

    plt.figure(figsize=(18,12))
    gs = gridspec.GridSpec(2,2)
    gs.update(left=0.1, right=0.9, wspace=0.3, hspace=0.3)
    gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0,1], hspace=0.1)
    gs01 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[1,1], hspace=0.1)

    ax1 = plt.subplot(gs[0, 0])
    rcfuncs.plot_tuning_raster(animal, tuningEphys, tuningBehav, tetrode, cluster, intensity=50, timeRange = [-0.5,1])
    
    # Sound-aligned high freq
    ax2 = plt.subplot(gs00[0:2, :])
    rcfuncs.plot_reward_change_raster(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='high', byBlock=True, alignment='sound', timeRange=[-0.3,0.4])
    plt.title('Modulation index {}\n p value {}'.format(cell['modIndHigh_0-0.1s_sound'],cell['modSigHigh_0-0.1s_sound']))
    ax3 = plt.subplot(gs00[2, :])
    rcfuncs.plot_reward_change_psth(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='high', byBlock=True, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010)
    # Cout-aligned high freq
    ax4 = plt.subplot(gs01[0:2, :])
    rcfuncs.plot_reward_change_raster(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='high', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Modulation index {}\n p value {}'.format(cell['modIndHigh_0-0.1s_center-out'],cell['modSigHigh_0-0.1s_center-out']))
    ax5 = plt.subplot(gs01[2, :])
    rcfuncs.plot_reward_change_psth(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='high', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)
    
    # Plot spike quality summary graphs
    ax6 = plt.subplot(gs[1, 0])
    rcfuncs.plot_waveform_each_cluster(animal, rcEphys, tetrode, cluster)
    plt.suptitle('Significantly modulated 0-0.1s window after sound onset')
    outputDir = '/home/languo/data/ephys/reward_change_stats/sig_mod_sound_high/'
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    
    # Save figure
    figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath)


for ind, cell in sigModCenterOutRight.iterrows():
    animal = cell.subject
    tuningSessInd = cell.sessiontype.index(tuningSessType)
    tuningEphys = cell.ephys[tuningSessInd]
    tuningBehav = cell.behavior[tuningSessInd]
    rcSessInd = cell.sessiontype.index(rcSessType)
    rcEphys = cell.ephys[rcSessInd]
    rcBehav = cell.behavior[rcSessInd]
    tetrode = int(cell.tetrode)
    cluster = int(cell.cluster)
    date = cell.date
    plt.figure(figsize=(18,12))
    gs = gridspec.GridSpec(2,2)
    gs.update(left=0.1, right=0.9, wspace=0.3, hspace=0.3)
    gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0,1], hspace=0.1)
    gs01 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[1,1], hspace=0.1)

    ax1 = plt.subplot(gs[0, 0])
    rcfuncs.plot_tuning_raster(animal, tuningEphys, tuningBehav, tetrode, cluster, intensity=50, timeRange = [-0.5,1])
    
    # Sound-aligned high freq
    ax2 = plt.subplot(gs00[0:2, :])
    rcfuncs.plot_reward_change_raster(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='high', byBlock=True, alignment='sound', timeRange=[-0.3,0.4])
    plt.title('Modulation index {}\n p value {}'.format(cell['modIndHigh_0-0.1s_sound'], cell['modSigHigh_0-0.1s_sound']))
    ax3 = plt.subplot(gs00[2, :])
    rcfuncs.plot_reward_change_psth(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='high', byBlock=True, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010)
    # Cout-aligned high freq
    ax4 = plt.subplot(gs01[0:2, :])
    rcfuncs.plot_reward_change_raster(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='high', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Modulation index {}\n p value {}'.format(cell['modIndHigh_0-0.1s_center-out'], cell['modSigHigh_0-0.1s_center-out']))
    ax5 = plt.subplot(gs01[2, :])
    rcfuncs.plot_reward_change_psth(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='high', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)
    
    # Plot spike quality summary graphs
    ax6 = plt.subplot(gs[1, 0])
    rcfuncs.plot_waveform_each_cluster(animal, rcEphys, tetrode, cluster)
    plt.suptitle('Significantly modulated 0-0.1s window after center out')
    outputDir = '/home/languo/data/ephys/reward_change_stats/sig_mod_centerout_right/'
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)

    # Save figure
    figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath)


for ind, cell in sigModCenterOutLeft.iterrows():
    animal = cell.subject
    tuningSessInd = cell.sessiontype.index(tuningSessType)
    tuningEphys = cell.ephys[tuningSessInd]
    tuningBehav = cell.behavior[tuningSessInd]
    rcSessInd = cell.sessiontype.index(rcSessType)
    rcEphys = cell.ephys[rcSessInd]
    rcBehav = cell.behavior[rcSessInd]
    tetrode = int(cell.tetrode)
    cluster = int(cell.cluster)
    date = cell.date
    plt.figure(figsize=(18,12))
    gs = gridspec.GridSpec(2,2)
    gs.update(left=0.1, right=0.9, wspace=0.3, hspace=0.3)
    gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0,1], hspace=0.1)
    gs01 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[1,1], hspace=0.1)

    ax1 = plt.subplot(gs[0, 0])
    rcfuncs.plot_tuning_raster(animal, tuningEphys, tuningBehav, tetrode, cluster, intensity=50, timeRange = [-0.5,1])
    
    # Sound-aligned low freq
    ax2 = plt.subplot(gs00[0:2, :])
    rcfuncs.plot_reward_change_raster(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='low', byBlock=True, alignment='sound', timeRange=[-0.3,0.4])
    plt.title('Modulation index {}\n p value {}'.format(cell['modIndLow_0-0.1s_sound'], cell['modSigLow_0-0.1s_sound']))
    ax3 = plt.subplot(gs00[2, :])
    rcfuncs.plot_reward_change_psth(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='low', byBlock=True, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010)
    # Cout-aligned low freq
    ax4 = plt.subplot(gs01[0:2, :])
    rcfuncs.plot_reward_change_raster(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='low', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Modulation index {}\n p value {}'.format(cell['modIndLow_0-0.1s_center-out'], cell['modSigLow_0-0.1s_center-out']))
    ax5 = plt.subplot(gs01[2, :])
    rcfuncs.plot_reward_change_psth(animal, rcBehav, rcEphys, tetrode, cluster, freqToPlot='low', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)
    
    # Plot spike quality summary graphs
    ax6 = plt.subplot(gs[1, 0])
    rcfuncs.plot_waveform_each_cluster(animal, rcEphys, tetrode, cluster)
    plt.suptitle('Significantly modulated 0-0.1s window after center out')
    outputDir = '/home/languo/data/ephys/reward_change_stats/sig_mod_centerout_left/'
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)

    # Save figure
    figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath)
