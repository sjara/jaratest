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


inforecFilepath = settings.INFOREC_PATH # This is the folder where you store all the inforec files in your computer
animal = 'gosi008'
inforecFilename = 'gosi008_inforec.py'
inforecFullpath = os.path.join(inforecFilepath, animal, inforecFilename)
inforec = imp.load_source('module.name', inforecFullpath)

outputDir = os.path.join(settings.EPHYS_PATH, animal, 'reward_change_reports')
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

#### CHANGE THIS to plot different experiments ####
expIndToPlot = -1 # This is the index(in the whole inforec's experiment list) of the experiment you want to plot
#####################################################3


siteIndToPlot = 0 # This is the index(in the experiment's site list) of the site you want to plot
site = inforec.experiments[expIndToPlot].sites[siteIndToPlot]
date = site.date
tuningSessionInd = site.session_types().index('tc')
tuningEphysThisSite = site.session_ephys_dirs()[tuningSessionInd]
tuningBehavThisSite = site.session_behav_filenames()[tuningSessionInd]
try:
    rcInd = site.session_types().index('behavior')
    rcEphysThisSite = site.session_ephys_dirs()[rcInd]
    rcBehavThisSite = site.session_behav_filenames()[rcInd]
except ValueError:
    print 'This site did not have behavior recorded.'

for tetrode in site.tetrodes:
    clusterList = rcfuncs.set_clusters_from_file(animal, rcEphysThisSite, tetrode)
    numClusters = np.unique(clusterList)
    for cluster in numClusters:
        plt.figure(figsize=(18,12))
        gs = gridspec.GridSpec(3,3)
        gs.update(left=0.1, right=0.9, wspace=0.3, hspace=0.3)
        gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0,1], hspace=0.1)
        gs01 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[1,1], hspace=0.1)
        gs02 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0,2], hspace=0.1)
        gs03 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[1,2], hspace=0.1)
        gs04 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[1,0], hspace=0.1)
        # Tuning raster
        ax1 = plt.subplot(gs[0, 0])
        rcfuncs.plot_tuning_raster(animal, tuningEphysThisSite, tuningBehavThisSite, tetrode, cluster, intensity=50, timeRange = [-0.5,1])
        
        # Sound-aligned low freq
        ax2 = plt.subplot(gs00[0:2, :])
        rcfuncs.plot_reward_change_raster(animal, rcBehavThisSite, rcEphysThisSite, tetrode, cluster, freqToPlot='low', byBlock=True, alignment='sound', timeRange=[-0.3,0.4])
        ax3 = plt.subplot(gs00[2, :])
        rcfuncs.plot_reward_change_psth(animal, rcBehavThisSite, rcEphysThisSite, tetrode, cluster, freqToPlot='low', byBlock=True, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010)
        # Cout-aligned low freq
        ax4 = plt.subplot(gs01[0:2, :])
        rcfuncs.plot_reward_change_raster(animal, rcBehavThisSite, rcEphysThisSite, tetrode, cluster, freqToPlot='low', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5])
        ax5 = plt.subplot(gs01[2, :])
        rcfuncs.plot_reward_change_psth(animal, rcBehavThisSite, rcEphysThisSite, tetrode, cluster, freqToPlot='low', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)
        
        # Sound-aligned high freq
        ax6 = plt.subplot(gs02[0:2, :])
        rcfuncs.plot_reward_change_raster(animal, rcBehavThisSite, rcEphysThisSite, tetrode, cluster, freqToPlot='high', byBlock=True, alignment='sound', timeRange=[-0.3,0.4])
        ax7 = plt.subplot(gs02[2, :])
        rcfuncs.plot_reward_change_psth(animal, rcBehavThisSite, rcEphysThisSite, tetrode, cluster, freqToPlot='high', byBlock=True, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010)
        # Cout-aligned high freq
        ax8 = plt.subplot(gs03[0:2, :])
        rcfuncs.plot_reward_change_raster(animal, rcBehavThisSite, rcEphysThisSite, tetrode, cluster, freqToPlot='high', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5])
        ax9 = plt.subplot(gs03[2, :])
        rcfuncs.plot_reward_change_psth(animal, rcBehavThisSite, rcEphysThisSite, tetrode, cluster, freqToPlot='high', byBlock=True, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)
        
        # Plot movement-related response, includes all valid trials (correct&incorrect)
        ax10 = plt.subplot(gs04[0:2, :])
        rcfuncs.plot_movement_response_raster(animal, rcBehavThisSite, rcEphysThisSite, tetrode, cluster, alignment='center-out', timeRange=[-0.3,0.5])
        ax11 = plt.subplot(gs04[2, :])
        rcfuncs.plot_movement_response_psth(animal, rcBehavThisSite, rcEphysThisSite, tetrode, cluster, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010)
        
        # Plot spike quality summary graphs
        ax12 = plt.subplot(gs[2, 0])
        rcfuncs.plot_waveform_each_cluster(animal, rcEphysThisSite, tetrode, cluster)
        
        #ax13 = plt.subplot(gs[2, 1])
        #rcfuncs.plot_projections_each_cluster(animal, rcEphysThisSite, tetrode, cluster)
        
	ax13 = plt.subplot(gs[2,1])
	rcfuncs.plot_isi_loghist_each_cluster(animal, rcEphysThisSite, tetrode, cluster)

        ax14 = plt.subplot(gs[2, 2])
        rcfuncs.plot_events_in_time_each_cluster(animal, rcEphysThisSite, tetrode, cluster)
        
        # Save figure
        figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
        figFullPath = os.path.join(outputDir, figname)
        plt.savefig(figFullPath)
