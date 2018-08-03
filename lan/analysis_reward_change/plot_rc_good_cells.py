import os
import shutil
import pandas as pd
import numpy as np
from scipy import stats
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import celldatabase
from jaratoolbox import loadbehavior
import new_reward_change_plotter_functions as rcfuncs
reload(rcfuncs)
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

#animal = 'gosi010'
tuningSessType = 'tc'
rcSessType = 'behavior'
evlockDir = '/home/languo/data/ephys/evlock_spktimes'

#databaseFullPath = os.path.join(settings.DATABASE_PATH, animal, '{}_database.h5'.format(animal))
databaseFullPath = os.path.join(settings.DATABASE_PATH, 'new_celldb', 'rc_database.h5')
#key = 'reward_change'
qualityThreshold = 2
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05
#celldb = pd.read_hdf(databaseFullPath, key=key)
celldb = celldatabase.load_hdf(databaseFullPath)

goodQualCells = celldb.loc[celldb['keepAfterDupTest']==1]  # Non-duplicate cells
#celldb.query('isiViolations<{} and shapeQuality>{}'.format(ISIcutoff, qualityThreshold))

cOutWindow = '0-0.3s'
soundWindow = '0-0.1s'
movementSelWindow = [0.0,0.3]

#movementSelective = goodQualCells.loc[goodQualCells['movementModS_{}_removedsidein'.format(movementSelWindow)] < 0.05]
sigModSound = goodQualCells.loc[(goodQualCells['modSigHigh_{}_sound'.format(soundWindow)]<=0.05) | (goodQualCells['modSigLow_{}_sound'.format(soundWindow)]<=0.05)]
#sigModCenterOut = goodQualCells.loc[(goodQualCells['modSigLow_{}_center-out_removedsidein'.format(cOutWindow)]<=0.05) | (goodQualCells['modSigHigh_{}_center-out'.format(cOutWindow)]<=0.05)]

movementSelective = goodQualCells['movementModS_{}_removedsidein'.format(movementSelWindow)] < alphaLevel
moreRespMoveLeft = movementSelective & (goodQualCells['movementModI_{}_removedsidein'.format(movementSelWindow)] < 0)
moreRespMoveRight = movementSelective & (goodQualCells['movementModI_{}_removedsidein'.format(movementSelWindow)] > 0)
leftModIndName = 'modIndLow_'+cOutWindow+'_'+'center-out'+'_removedsidein'
leftModSigName = 'modSigLow_'+cOutWindow+'_'+'center-out'+'_removedsidein'
leftModDirName = 'modDirLow_'+cOutWindow+'_'+'center-out'+'_removedsidein'
rightModIndName = 'modIndHigh_'+cOutWindow+'_'+'center-out'+'_removedsidein'
rightModSigName = 'modSigHigh_'+cOutWindow+'_'+'center-out'+'_removedsidein'
rightModDirName = 'modDirHigh_'+cOutWindow+'_'+'center-out'+'_removedsidein'
goodLeftMovementSelCells = goodQualCells[moreRespMoveLeft]
goodRightMovementSelCells = goodQualCells[moreRespMoveRight] 
goodMovementSelCells = goodQualCells[movementSelective]
goodLeftMovementSelModSig = goodLeftMovementSelCells[leftModSigName]
goodLeftMovementSelModDir = goodLeftMovementSelCells[leftModDirName]
goodRightMovementSelModSig = goodRightMovementSelCells[rightModSigName]
goodRightMovementSelModDir = goodRightMovementSelCells[rightModDirName]
sigModulatedLeft = (goodLeftMovementSelModSig < alphaLevel) & (goodLeftMovementSelModDir > 0)
sigModulatedRight = (goodRightMovementSelModSig < alphaLevel) & (goodRightMovementSelModDir > 0)
sigModLeftCells = goodLeftMovementSelCells[sigModulatedLeft]
sigModRightCells = goodRightMovementSelCells[sigModulatedRight]

outputDir = '/home/languo/data/reports/reward_change/all_good_cells/'

movementSelOutputDir = '/home/languo/data/reports/reward_change/movement_sel_{}_removedsidein/'.format(movementSelWindow)
soundOutputDir = '/home/languo/data/reports/reward_change/sig_mod_sound_{}/'.format(soundWindow)
cOutOutputDir = '/home/languo/data/reports/reward_change/sig_mod_cOut_{}_removedsidein/'.format(cOutWindow)


# -- Plot all reports -- #
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
    animal = cell.subject
    figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
    figFullPath = os.path.join(outputDir, figname)
    
    if os.path.exists(figFullPath):
        continue # Do not repeatedly plot cells

    cellObj = ephyscore.Cell(cell)
    # Tuning raster
    ax1 = plt.subplot(gs[0:2, 0])
    rcfuncs.plot_tuning_raster(cellObj, sessionType='tc', intensity=50, timeRange = [-0.5,1])  
    maxAbsSoundZ = max(min(cell.behavZscore),max(cell.behavZscore),key=abs)
    plt.title('Max soundresp Zscore in 2afc:{:.3f}'.format(maxAbsSoundZ))
    
    # Sound-aligned low freq
    ax2 = plt.subplot(gs00[0:2, :])
    rcfuncs.plot_reward_change_raster(cellObj, evlockDir, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='low', byBlock=True, alignment='sound', timeRange=[-0.3,0.4])
    plt.title('Modulation index {:.3f}\n p value {:.3f}\n Mod dir {}'.format(cell['modIndLow_{}_sound'.format(soundWindow)],cell['modSigLow_{}_sound'.format(soundWindow)],cell['modDirLow_{}_sound'.format(soundWindow)]))
    ax3 = plt.subplot(gs00[2, :])
    rcfuncs.plot_reward_change_psth(cellObj, evlockDir, behavClass=loadbehavior.FlexCategBehaviorData,freqToPlot='low', byBlock=True, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010)

    # Sound-aligned high freq
    ax4 = plt.subplot(gs01[0:2, :])
    rcfuncs.plot_reward_change_raster(cellObj, evlockDir, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='high', byBlock=True, alignment='sound', timeRange=[-0.3,0.4])
    plt.title('Modulation index {:.3f}\n p value {:.3f}\n Mod dir {}'.format(cell['modIndHigh_{}_sound'.format(soundWindow)],cell['modSigHigh_{}_sound'.format(soundWindow)],cell['modDirHigh_{}_sound'.format(soundWindow)]))
    ax5 = plt.subplot(gs01[2, :])
    rcfuncs.plot_reward_change_psth(cellObj, evlockDir, behavClass=loadbehavior.FlexCategBehaviorData,freqToPlot='high', byBlock=True, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010)

    # Cout-aligned high freq
    ax6 = plt.subplot(gs03[0:2, :])
    rcfuncs.plot_reward_change_raster(cellObj, evlockDir, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='high', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Modulation index {:.3f}\n p value {:.3f}\n Mod dir {}'.format(cell['modIndHigh_{}_center-out'.format(cOutWindow)],cell['modSigHigh_{}_center-out'.format(cOutWindow)],cell['modDirHigh_{}_center-out'.format(cOutWindow)]))
    ax7 = plt.subplot(gs03[2, :])
    rcfuncs.plot_reward_change_psth(cellObj, evlockDir, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='high', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)
    
    # Cout-aligned low freq
    ax8 = plt.subplot(gs02[0:2, :])
    rcfuncs.plot_reward_change_raster(cellObj, evlockDir, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='low', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Modulation index {:.3f}\n p value {:.3f}\n Mod dir {}'.format(cell['modIndLow_{}_center-out'.format(cOutWindow)],cell['modSigLow_{}_center-out'.format(cOutWindow)],cell['modDirLow_{}_center-out'.format(cOutWindow)]))
    ax9 = plt.subplot(gs02[2, :])
    rcfuncs.plot_reward_change_psth(cellObj, evlockDir, behavClass=loadbehavior.FlexCategBehaviorData, freqToPlot='low', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)
    
    # Movement-selectivity plot
    ax10 = plt.subplot(gs04[0:2, :])
    rcfuncs.plot_movement_response_raster(cellObj, evlockDir, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5])
    plt.title('Movement selectivity index {:.3f}, pVal {:.3f}'.format(cell['movementModI_[0.05, 0.15]'], cell['movementModS_[0.05, 0.15]']))
    ax11 = plt.subplot(gs04[2, :])
    rcfuncs.plot_movement_response_psth(cellObj, evlockDir, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5])

    # Plot spike quality summary graphs
    ax12 = plt.subplot(gs[4, 0])
    rcfuncs.plot_waveform_each_cluster(cellObj, sessionType='behavior')
 
    # Plot isi summary
    ax13 = plt.subplot(gs[4, 1])
    rcfuncs.plot_isi_loghist_each_cluster(cellObj, sessionType='behavior')

    # Plot events in time summary
    ax14 = plt.subplot(gs[4, 2])
    rcfuncs.plot_events_in_time_each_cluster(cellObj, sessionType='behavior')

    plt.suptitle('{}_{}_T{}_c{}'.format(animal,date,tetrode,cluster))
    # Save figure
 
    plt.savefig(figFullPath)



# -- Copy significantly modulated reports into different folders -- #
for ind, cell in sigModSound.iterrows():
    tetrode = cell.tetrode
    cluster = cell.cluster
    date = cell.date
    animal = cell.subject
    figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
    figFullPath = os.path.join(outputDir, figname)
    if not os.path.exists(soundOutputDir):
        os.mkdir(soundOutputDir)
    newOutputFullPath = os.path.join(soundOutputDir, figname)
    shutil.copyfile(figFullPath, newOutputFullPath)
        
# for ind, cell in sigModCenterOut.iterrows():
#     tetrode = cell.tetrode
#     cluster = cell.cluster
#     date = cell.date
#     animal = cell.subject
#     figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
#     figFullPath = os.path.join(outputDir, figname)
#     if not os.path.exists(cOutOutputDir):
#         os.mkdir(cOutOutputDir)
#     newOutputFullPath = os.path.join(cOutOutputDir, figname)
#     shutil.copyfile(figFullPath, newOutputFullPath)

            
# for ind, cell in movementSelective.iterrows():
#     tetrode = cell.tetrode
#     cluster = cell.cluster
#     date = cell.date
#     animal = cell.subject
#     figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
#     figFullPath = os.path.join(outputDir, figname)
#     if not os.path.exists(movementSelOutputDir):
#         os.mkdir(movementSelOutputDir)
#     newOutputFullPath = os.path.join(movementSelOutputDir, figname)
#     shutil.copyfile(figFullPath, newOutputFullPath)

for ind, cell in sigModLeftCells.iterrows():
    tetrode = cell.tetrode
    cluster = cell.cluster
    date = cell.date
    animal = cell.subject
    figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
    figFullPath = os.path.join(outputDir, figname)
    newOutputFullPath = os.path.join(cOutOutputDir, 'sigModLeft', figname)
    shutil.copyfile(figFullPath, newOutputFullPath)

for ind, cell in sigModRightCells.iterrows():
    tetrode = cell.tetrode
    cluster = cell.cluster
    date = cell.date
    animal = cell.subject
    figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
    figFullPath = os.path.join(outputDir, figname)
    newOutputFullPath = os.path.join(cOutOutputDir, 'sigModRight', figname)
    shutil.copyfile(figFullPath, newOutputFullPath)
