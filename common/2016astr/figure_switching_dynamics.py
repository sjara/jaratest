'''

'''
import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
import matplotlib.gridspec as gridspec
import matplotlib
import pandas as pd
import figparams

qualityList = [1,6]
maxZThreshold = 3
ISIcutoff = 0.02
removedDuplicates = True

FIGNAME = 'behavior_dynamics_switching'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To

#colorLeft = figparams.colp['MidFreqL']
#colorRight = figparams.colp['MidFreqR']
#soundColor = figparams.colp['sound']

SAVE_FIGURE = 1
outputDir = '/tmp/'

figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,7]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1

labelPosX = [0.02]   # Horiz position for panel labels
labelPosY = [0.95]    # Vert position for panel labels

# -- Read in databases storing all measurements from switching mice -- #
switchingFilePath = os.path.join(settings.FIGURES_DATA_PATH,figparams.STUDY_NAME)
switchingFileName = 'all_cells_all_measures_extra_mod_waveform_switching.h5'
switchingFullPath = os.path.join(switchingFilePath,switchingFileName)
allcells_switching = pd.read_hdf(switchingFullPath,key='switching')

# -- Get intermediate data relevant to this subfigure of sound modulation -- #
## Plot all good cells from switcing task ##
goodcells = (allcells_switching.cellQuality.isin(qualityList)) & (allcells_switching.ISI <= ISIcutoff)
cellsInStr = allcells_switching.cellInStr==1
keepAfterDupTest = allcells_switching.keep_after_dup_test
cellsToUse = allcells_switching[goodcells & cellsInStr & keepAfterDupTest] #just look at the good cells THAT ARE IN STR 

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')
#ax.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

animals = np.unique(cellsToUse.animalName)
paradigm = '2afc'

f = open(os.path.join(outputDir,'sessionsDict.txt'), 'a')

for animal in animals:
    f.write("'"+animal+"':[\n")

    cellsThisAnimal = cellsToUse.query("animalName=='{}'".format(animal))
    behavSessThisAnimal = np.unique(cellsThisAnimal.behavSession)
    for session in behavSessThisAnimal:
        print 'Plotting dynamics of {} {}'.format(animal, session)
        '''
        behavFileName = loadbehavior.path_to_behavior_data(animal,paradigm,session)
        behavData = loadbehavior.FlexCategBehaviorData(behavFileName)
        
        hPlots = behavioranalysis.plot_dynamics(behavData, winsize=40,fontsize=12, soundfreq=None)
        if SAVE_FIGURE:
            figFilename = 'plots_dynamics_{}_{}'.format(session, animal)
            extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
        '''
        
        f.write("'"+session+"',\n")
    f.write("],\n")

f.close()
