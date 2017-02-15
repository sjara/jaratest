'''
Script to plot daily reports for all clusters and tetrodes recorded during the reward change freq discrimination task.
The unit of plotting is a 'site' as defined in inforec files and nick's celldatabase class.
Lan Guo 20170215
'''
import imp
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratest.lan.Ephys import reward_change_loader_plotter_functions as rcfuncs

inforecFilepath = settings.INFOREC_PATH # This is the folder where you store all the inforec files in your computer
animal = 'gosi004'
inforecFilename = 'gosi004_inforec.py'
inforecFullpath = os.path.join(inforecFilepath, animal, inforecFilename)
inforec = imp.load_source('module.name', inforecFullpath)

outputDir = os.path.join(settings.EPHYS_PATH, animal, 'reward_change_reports')
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

expIndToPlot = 0 # This is the index(in the whole inforec's experiment list) of the experiment you want to plot
siteIndToPlot = 0 # This is the index(in the experiment's site list) of the site you want to plot
site = inforec.experiments[expIndToPlot].sites[siteIndToPlot]
date = site.date
tuningEphysThisSite = site.session_ephys_dirs()[site.session_types().index('tc')]
tuningBehavThisSite = site.session_behav_filenames()[site.session_types().index('tc')]
2afcEphysThisSite = site.session_ephys_dirs()[site.session_types().index('behavior')]
2afcBehavThisSite = site.session_behav_filenames()[site.session_types().index('behavior')]

for tetrode in siteObj.tetrodes:
    clusterList = rcfuncs.set_clusters_from_file(animal, 2afcEphysThisSite, tetrode)
    numClusters = np.unique(clusterList)
    for cluster in numClusters:
        plt.subplot2grid((3,9),(0,0),rowspan=3,colspan=3)
        rcfuncs.load_n_plot_tuning_raster(tuningEphysThisSite, tuningBehavThisSite, tetrode, cluster, intensity=50, timeRange = [-0.5,1])
        plt.subplot2grid((3,9),(0,3),rowspan=3,colspan=3)
        rcfuncs.plot_rew_change_per_cell_raster_psth(behavSession, ephysSession, tetrode, cluster, freqToPlot='both', byBlock=True, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010)
        plt.subplot2grid((3,9),(0,6),rowspan=3,colspan=3)
        rcfuncs.plot_rew_change_per_cell_raster_psth(behavSession, ephysSession, tetrode, cluster, freqToPlot='both', byBlock=True, alignment='center-out', timeRange=[-0.3,0.4], binWidth=0.010)
        figname = '{}_{}_T{}_c{}_reward_change.png'.format(animal,date,tetrode,cluster)
        figFullPath = os.path.join(outputDir, figname)
        plt.savefig(figFullPath)
