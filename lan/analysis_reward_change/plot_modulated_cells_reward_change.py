'''
Script to plot daily reports for all clusters and tetrodes recorded during the reward change freq discrimination task.
The unit of plotting is a 'site' as defined in inforec files and nick's celldatabase class.
Lan Guo 20170215
'''
import os
import imp
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
reload(settings)
from jaratest.stacy import reward_change_loader_plotter_functions_stacy as rcfuncs
reload(rcfuncs)
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches

colorDictRC = {'leftMoreLowFreq':'g', #green
               'rightMoreLowFreq':'m', #magenta
               'sameRewardLowFreq':'y', #yellow
               'leftMoreHighFreq':'r', #red
               'rightMoreHighFreq':'b', #blue
               'sameRewardHighFreq':'darkgrey'}


animalLists = [['adap005','adap012', 'adap013', 'adap015', 'adap017'], ['gosi001','gosi004', 'gosi008','gosi010']]
animalLabels = ['astr', 'ac']
modulationWindows = ['0-0.1s_sound','0-0.1s_center-out']
freqLabels = ['Low','High']
qualityThreshold = 2.5 #3 
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05

outputDir = '/home/languo/data/ephys/reward_change_stats/modulated_cells_reports/'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

for indRegion, (label,animalList) in enumerate(zip(animalLabels, animalLists)):
    celldbPath = os.path.join(settings.DATABASE_PATH,'reward_change_{}.h5'.format(label))
    celldb = pd.read_hdf(celldbPath, key='reward_change')
    goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{}'.format(ISIcutoff, qualityThreshold))
    
    for indf, freq in enumerate(freqLabels):
        for indw, modWindow in enumerate(modulationWindows):
            modIndName = 'modInd'+freq+'_'+modWindow
            modSigName = 'modSig'+freq+'_'+modWindow
            allGoodCellsModInd = goodQualCells[modIndName]
            allGoodCellsModSig = goodQualCells[modSigName]
            sigModGoodCells = goodQualCells.loc[allGoodCellsModSig < alphaLevel]
            #responsiveThisFreq = goodQualCells.behavZscore.apply(lambda x: abs(x[indf]) >= maxZThreshold)
            for indc, cell in sigModGoodCells.iterrows():
                animal = cell['animalName']
                tetrode = cell['tetrode']
                cluster = cell['cluster']
                modIThisFreqThisWindow = cell['modIndName']
                movementModInd = cell['movementModI']
                tuningSessionInd = cell['sessiontype'].index('tc')
                tuningEphysThisCell = cell['ephys'][tuningSessionInd]
                tuningBehavThisCell = cell['behavior'][tuningSessionInd]
                thisFreqZscore = cell['behavZscore'][indf]
                rcInd = cell['sessiontype'].index('behavior')
                rcEphysThisCell = cell['ephys'][rcInd]
                rcBehavThisCell = cell['behavior'][rcInd]

                plt.figure(figsize=(9,12))
                gs = gridspec.GridSpec(2,3)
                gs.update(left=0.1, right=0.9, wspace=0.3, hspace=0.3)
                gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0,1], hspace=0.1)
                gs01 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0,2], hspace=0.1)

                # Tuning raster
                ax1 = plt.subplot(gs[0, 0])
                rcfuncs.plot_tuning_raster(animal, tuningEphysThisCell, tuningBehavThisCell, tetrode, cluster, intensity=50, timeRange = [-0.5,1])
                ax1.set_title('Z score for {}Hz: {:.3f}'.format(freq, thisFreqZscore))
                # mod window-aligned this freq 
                alignment = modWindow.split('_')[1]
                ax2 = plt.subplot(gs00[0:2, :])
                rcfuncs.plot_reward_change_raster(animal, rcBehavThisCell, rcEphysThisCell, tetrode, cluster, freqToPlot=freq.lower(), byBlock=True, alignment=alignment, timeRange=[-0.3,0.4])
                ax2.set_title('Reward modulation index: {:.3f}'.format(modIThisFreqThisWindow))
                ax3 = plt.subplot(gs00[2, :])
                rcfuncs.plot_reward_change_psth(animal, rcBehavThisCell, rcEphysThisCell, tetrode, cluster, freqToPlot=freq.lower(), byBlock=True, alignment=alignment, timeRange=[-0.3,0.4], binWidth=0.010)

                # Plot movement-related response, includes all valid trials (correct&incorrect)
                ax4 = plt.subplot(gs01[0:2, :])
                rcfuncs.plot_movement_response_raster(animal, rcBehavThisCell, rcEphysThisCell, tetrode, cluster, alignment='center-out', timeRange=[-0.3,0.5])
                ax4.set_title('Movement modulation index: {:.3f}'.format(movementModInd))
                ax5 = plt.subplot(gs01[2, :])
                rcfuncs.plot_movement_response_psth(animal, rcBehavThisCell, rcEphysThisCell, tetrode, cluster, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)

                # Plot spike quality summary graphs
                ax6 = plt.subplot(gs[1, 0])
                rcfuncs.plot_waveform_each_cluster(animal, rcEphysThisCell, tetrode, cluster)

                ax7 = plt.subplot(gs[1,1])
                rcfuncs.plot_isi_loghist_each_cluster(animal, rcEphysThisCell, tetrode, cluster)

                ax8 = plt.subplot(gs[1, 2])
                rcfuncs.plot_events_in_time_each_cluster(animal, rcEphysThisCell, tetrode, cluster)

                # Save figure
                figname = '{}_{}_T{}_c{}_{}_{}.png'.format(animal,date,tetrode,cluster, freq, modWindow)
                plt.suptitle(figname)
                figFullPath = os.path.join(outputDir, figname)
                plt.savefig(figFullPath)
