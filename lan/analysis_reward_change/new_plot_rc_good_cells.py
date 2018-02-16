import os
import pandas as pd
import numpy as np
from scipy import stats
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import loadbehavior
import new_reward_change_plotter_functions as rcfuncs
reload(rcfuncs)
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

animal = 'gosi010'
tuningSessType = 'tc'
rcSessType = 'behavior'

#databaseFullPath = os.path.join(settings.DATABASE_PATH, animal, '{}_database.h5'.format(animal))
databaseFullPath = os.path.join(settings.DATABASE_PATH, 'new_celldb', '{}_database.h5'.format(animal))
key = 'reward_change'
qualityThreshold = 2
maxZThreshold = 3
ISIcutoff = 0.02

celldb = pd.read_hdf(databaseFullPath, key=key)

goodQualCells = celldb.query('keepAfterDupTest==True')
#celldb.query('isiViolations<{} and shapeQuality>{}'.format(ISIcutoff, qualityThreshold))

cOutWindow = '0.05-0.15s'
soundWindow = '0-0.1s'

print('Plotting all good quality non-duplicated cells')
plt.figure(figsize=(18,18))
gs = gridspec.GridSpec(5,3)
gs.update(left=0.1, right=0.9, wspace=0.3, hspace=0.8)
gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0:2,1], hspace=0.1)
gs01 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0:2,2], hspace=0.1)
gs02 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[2:4,1], hspace=0.1)
gs03 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[2:4,2], hspace=0.1)
gs04 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[2:4,0], hspace=0.1)

outputDir = '/home/languo/data/reports/reward_change/all_good_cells/'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

for ind, cell in goodQualCells.iterrows():
    plt.clf()
    tetrode = cell.tetrode
    cluster = cell.cluster
    date = cell.date
    
    figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
    figFullPath = os.path.join(outputDir, figname)
    
    if os.path.exists(figFullPath):
        continue # Do not repeatedly plot cells

    cellObj = ephyscore.Cell(cell)
    # Tuning raster
    ax1 = plt.subplot(gs[0:2, 0])
    rcfuncs.plot_tuning_raster(cellObj, sessionType='tc', intensity=50, timeRange = [-0.5,1])   
    
    # Sound-aligned low freq
    ax2 = plt.subplot(gs00[0:2, :])
    rcfuncs.plot_reward_change_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='low', byBlock=True, alignment='sound', timeRange=[-0.3,0.4])
    plt.title('Modulation index {:.3f}\n p value {:.3f}\n Mod dir {}'.format(cell['modIndLow_{}_sound'.format(soundWindow)],cell['modSigLow_{}_sound'.format(soundWindow)],cell['modDirLow_{}_sound'.format(soundWindow)]))
    ax3 = plt.subplot(gs00[2, :])
    rcfuncs.plot_reward_change_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData,freqToPlot='low', byBlock=True, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010)

    # Sound-aligned high freq
    ax4 = plt.subplot(gs01[0:2, :])
    rcfuncs.plot_reward_change_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='high', byBlock=True, alignment='sound', timeRange=[-0.3,0.4])
    plt.title('Modulation index {:.3f}\n p value {:.3f}\n Mod dir {}'.format(cell['modIndHigh_{}_sound'.format(soundWindow)],cell['modSigHigh_{}_sound'.format(soundWindow)],cell['modDirHigh_{}_sound'.format(soundWindow)]))
    ax5 = plt.subplot(gs01[2, :])
    rcfuncs.plot_reward_change_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData,freqToPlot='high', byBlock=True, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010)

    # Cout-aligned high freq
    ax6 = plt.subplot(gs02[0:2, :])
    rcfuncs.plot_reward_change_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='high', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Modulation index {:.3f}\n p value {:.3f}\n Mod dir {}'.format(cell['modIndHigh_{}_center-out'.format(cOutWindow)],cell['modSigHigh_{}_center-out'.format(cOutWindow)],cell['modDirHigh_{}_center-out'.format(cOutWindow)]))
    ax7 = plt.subplot(gs02[2, :])
    rcfuncs.plot_reward_change_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='high', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)
    
    # Cout-aligned low freq
    ax8 = plt.subplot(gs03[0:2, :])
    rcfuncs.plot_reward_change_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='low', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Modulation index {:.3f}\n p value {:.3f}\n Mod dir {}'.format(cell['modIndLow_{}_center-out'.format(cOutWindow)],cell['modSigLow_{}_center-out'.format(cOutWindow)],cell['modDirLow_{}_center-out'.format(cOutWindow)]))
    ax9 = plt.subplot(gs03[2, :])
    rcfuncs.plot_reward_change_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='low', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)
    
    # Movement-selectivity plot
    ax10 = plt.subplot(gs04[0:2, :])
    rcfuncs.plot_movement_response_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Movement selectivity index {:.3f}'.format(cell['movementModI_[0.05, 0.15]']))
    ax11 = plt.subplot(gs04[2, :])
    rcfuncs.plot_movement_response_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5])

    # Plot spike quality summary graphs
    ax12 = plt.subplot(gs[4, 0])
    rcfuncs.plot_waveform_each_cluster(cellObj, sessionType='tc')
 
    # Plot isi summary
    ax13 = plt.subplot(gs[4, 1])
    rcfuncs.plot_isi_loghist_each_cluster(cellObj, sessionType='tc')

    # Plot events in time summary
    ax14 = plt.subplot(gs[4, 2])
    rcfuncs.plot_events_in_time_each_cluster(cellObj, sessionType='tc')

    plt.suptitle('{}_{}_T{}_c{}'.format(animal,date,tetrode,cluster))
    # Save figure
 
    plt.savefig(figFullPath)



'''
sigModSoundHigh = goodQualCells.loc[goodQualCells['modSigHigh_{}_sound'.format(soundWindow)]<=0.05]
sigModSoundLow = goodQualCells.loc[goodQualCells['modSigLow_{}_sound'.format(soundWindow)]<=0.05]

sigModCenterOutLeft = goodQualCells.loc[goodQualCells['modSigLow_{}_center-out'.format(cOutWindow)]<=0.05]
sigModCenterOutRight = goodQualCells.loc[goodQualCells['modSigHigh_{}_center-out'.format(cOutWindow)]<=0.05]

plt.figure(figsize=(8,12))
gs = gridspec.GridSpec(3,3)
gs.update(left=0.1, right=0.9, wspace=0.3, hspace=0.3)
gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0,1], hspace=0.1)
gs01 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0,2], hspace=0.1)

outputDir = '/home/languo/data/reports/reward_change/sig_mod_sound_low/'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
# -- Plot reports -- #
for ind, cell in sigModSoundLow.iterrows():
    plt.clf()
    tetrode = cell.tetrode
    cluster = cell.cluster
    date = cell.date
    cellObj = ephyscore.Cell(cell)
    # Tuning raster
    ax1 = plt.subplot(gs[0, 0])
    rcfuncs.plot_tuning_raster(cellObj, sessionType='tc', intensity=50, timeRange = [-0.5,1])   
       
    # Sound-aligned low freq
    ax2 = plt.subplot(gs00[0:2, :])
    rcfuncs.plot_reward_change_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='low', byBlock=True, alignment='sound', timeRange=[-0.3,0.4])
    plt.title('Modulation index {}\n p value {}\n Mod dir {}'.format(cell['modIndLow_{}_sound'.format(soundWindow)],cell['modSigLow_{}_sound'.format(soundWindow)],cell['modDirLow_{}_sound'.format(soundWindow)]))
    ax3 = plt.subplot(gs00[2, :])
    rcfuncs.plot_reward_change_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData,freqToPlot='low', byBlock=True, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010)

    # Movement-selectivity plot
    ax4 = plt.subplot(gs01[0:2, :])
    rcfuncs.plot_movement_response_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Movement selectivity index {}'.format(cell['movementModI_[0.05, 0.15]']))
    ax5 = plt.subplot(gs01[2, :])
    rcfuncs.plot_movement_response_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5])

    # Plot spike quality summary graphs
    ax6 = plt.subplot(gs[1, 0])
    rcfuncs.plot_waveform_each_cluster(cellObj, sessionType='tc')
 
    # Plot isi summary
    ax7 = plt.subplot(gs[1, 1])
    rcfuncs.plot_isi_loghist_each_cluster(cellObj, sessionType='tc')

    # Plot events in time summary
    ax8 = plt.subplot(gs[1, 2])
    rcfuncs.plot_events_in_time_each_cluster(cellObj, sessionType='tc')

    plt.suptitle('{}_{}_T{}_c{}\nSignificantly modulated {} window after sound onset'.format(animal,date,tetrode,cluster, soundWindow))
    # Save figure
    figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath)


outputDir = '/home/languo/data/reports/reward_change/sig_mod_sound_high/'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)   
for ind, cell in sigModSoundHigh.iterrows():
    plt.clf()
    tetrode = cell.tetrode
    cluster = cell.cluster
    date = cell.date
    cellObj = ephyscore.Cell(cell)
    # Tuning raster
    ax1 = plt.subplot(gs[0, 0])
    rcfuncs.plot_tuning_raster(cellObj, sessionType='tc', intensity=50, timeRange = [-0.5,1])   
       
    # Sound-aligned low freq
    ax2 = plt.subplot(gs00[0:2, :])
    rcfuncs.plot_reward_change_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='high', byBlock=True, alignment='sound', timeRange=[-0.3,0.4])
    plt.title('Modulation index {}\n p value {}\n Mod dir {}'.format(cell['modIndHigh_{}_sound'.format(soundWindow)],cell['modSigHigh_{}_sound'.format(soundWindow)],cell['modDirHigh_{}_sound'.format(soundWindow)]))
    ax3 = plt.subplot(gs00[2, :])
    rcfuncs.plot_reward_change_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData,freqToPlot='high', byBlock=True, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010)

    # Movement-selectivity plot
    ax4 = plt.subplot(gs01[0:2, :])
    rcfuncs.plot_movement_response_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Movement selectivity index {}'.format(cell['movementModI_[0.05, 0.15]']))
    ax5 = plt.subplot(gs01[2, :])
    rcfuncs.plot_movement_response_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5])

    # Plot spike quality summary graphs
    ax6 = plt.subplot(gs[1, 0])
    rcfuncs.plot_waveform_each_cluster(cellObj, sessionType='tc')
 
    # Plot isi summary
    ax7 = plt.subplot(gs[1, 1])
    rcfuncs.plot_isi_loghist_each_cluster(cellObj, sessionType='tc')

    # Plot events in time summary
    ax8 = plt.subplot(gs[1, 2])
    rcfuncs.plot_events_in_time_each_cluster(cellObj, sessionType='tc')

    plt.suptitle('{}_{}_T{}_c{}\nSignificantly modulated {} window after sound onset'.format(animal,date,tetrode,cluster, soundWindow))
    # Save figure
    figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath)


outputDir = '/home/languo/data/reports/reward_change/sig_mod_centerout_right/'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
for ind, cell in sigModCenterOutRight.iterrows():
    plt.clf()
    tetrode = cell.tetrode
    cluster = cell.cluster
    date = cell.date
    cellObj = ephyscore.Cell(cell)
    # Tuning raster
    ax1 = plt.subplot(gs[0, 0])
    rcfuncs.plot_tuning_raster(cellObj, sessionType='tc', intensity=50, timeRange = [-0.5,1])   
       
    # Cout-aligned high freq
    ax2 = plt.subplot(gs00[0:2, :])
    rcfuncs.plot_reward_change_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='high', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Modulation index {}\n p value {}\n Mod dir {}'.format(cell['modIndHigh_{}_center-out'.format(cOutWindow)],cell['modSigHigh_{}_center-out'.format(cOutWindow)],cell['modDirHigh_{}_center-out'.format(cOutWindow)]))
    ax3 = plt.subplot(gs00[2, :])
    rcfuncs.plot_reward_change_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='high', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)

    # Movement-selectivity plot
    ax4 = plt.subplot(gs01[0:2, :])
    rcfuncs.plot_movement_response_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Movement selectivity index {}'.format(cell['movementModI_[0.05, 0.15]']))
    ax5 = plt.subplot(gs01[2, :])
    rcfuncs.plot_movement_response_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5])

    # Plot spike quality summary graphs
    ax6 = plt.subplot(gs[1, 0])
    rcfuncs.plot_waveform_each_cluster(cellObj, sessionType='tc')
 
    # Plot isi summary
    ax7 = plt.subplot(gs[1, 1])
    rcfuncs.plot_isi_loghist_each_cluster(cellObj, sessionType='tc')

    # Plot events in time summary
    ax8 = plt.subplot(gs[1, 2])
    rcfuncs.plot_events_in_time_each_cluster(cellObj, sessionType='tc')

    plt.suptitle('{}_{}_T{}_c{}\nSignificantly modulated {} window after center out'.format(animal,date,tetrode,cluster, cOutWindow))
    # Save figure
    figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath)


outputDir = '/home/languo/data/reports/reward_change/sig_mod_centerout_left/'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
for ind, cell in sigModCenterOutLeft.iterrows():
    plt.clf()
    tetrode = cell.tetrode
    cluster = cell.cluster
    date = cell.date
    cellObj = ephyscore.Cell(cell)
    # Tuning raster
    ax1 = plt.subplot(gs[0, 0])
    rcfuncs.plot_tuning_raster(cellObj, sessionType='tc', intensity=50, timeRange = [-0.5,1])   
       
    # Cout-aligned low freq
    ax2 = plt.subplot(gs00[0:2, :])
    rcfuncs.plot_reward_change_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='low', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Modulation index {}\n p value {}\n Mod dir {}'.format(cell['modIndLow_{}_center-out'.format(cOutWindow)],cell['modSigLow_{}_center-out'.format(cOutWindow)],cell['modDirLow_{}_center-out'.format(cOutWindow)]))
    ax3 = plt.subplot(gs00[2, :])
    rcfuncs.plot_reward_change_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='low', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)

    # Movement-selectivity plot
    ax4 = plt.subplot(gs01[0:2, :])
    rcfuncs.plot_movement_response_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Movement selectivity index {}'.format(cell['movementModI_[0.05, 0.15]']))
    ax5 = plt.subplot(gs01[2, :])
    rcfuncs.plot_movement_response_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5])

    # Plot spike quality summary graphs
    ax6 = plt.subplot(gs[1, 0])
    rcfuncs.plot_waveform_each_cluster(cellObj, sessionType='tc')
 
    # Plot isi summary
    ax7 = plt.subplot(gs[1, 1])
    rcfuncs.plot_isi_loghist_each_cluster(cellObj, sessionType='tc')

    # Plot events in time summary
    ax8 = plt.subplot(gs[1, 2])
    rcfuncs.plot_events_in_time_each_cluster(cellObj, sessionType='tc')

    plt.suptitle('{}_{}_T{}_c{}\nSignificantly modulated {} window after center out'.format(animal,date,tetrode,cluster, cOutWindow))
    # Save figure
    figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath)

'''
