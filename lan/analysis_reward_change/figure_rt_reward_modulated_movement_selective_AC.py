'''
Create histogram of response times for select reward modulated cells.
'''
import os, sys
import matplotlib
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import scipy.stats as stats
from jaratoolbox import extraplots
from jaratoolbox import settings
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp

STUDY_NAME = '2017rc'
FIGNAME = 'reward_modulation_movement_selective_cells'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

colorDict = {'leftMoreLowFreq':cp.TangoPalette['SkyBlue2'],
             'rightMoreLowFreq':cp.TangoPalette['Orange2'],
             'sameRewardLowFreq':'y',
             'leftMoreHighFreq':'r',
             'rightMoreHighFreq':'b',
             'sameRewardHighFreq':'darkgrey'}

soundColor = cp.TangoPalette['Butter2']
timeRange = [-0.3,0.5]

# -- Select example cells here -- #
infoEachCell = []
infoEachCell.append({ 'cellName':'gosi001_2017-05-06_T3_c5',
                      'alignment':'center-out', 'brainRegion':'ac' })
infoEachCell.append({ 'cellName':'gosi004_2017-02-13_T7_c8',
                      'alignment':'center-out', 'brainRegion':'ac' })
infoEachCell.append({ 'cellName':'gosi008_2017-03-14_T7_c8',
                      'alignment':'center-out', 'brainRegion':'ac' })


if len(sys.argv)>1:
    cellInd = int(sys.argv[1])
    cellsToPlot = [infoEachCell[cellInd]]
else:
    cellsToPlot = infoEachCell


SAVE_FIGURE = 1
outputDir = '/tmp/'

figFormat = 'svg' # 'pdf' or 'svg'
figSize = [5,5]

fontSizeLabels = 12 #figparams.fontSizeLabels
fontSizeTicks = 12 #figparams.fontSizeTicks
fontSizePanel = 16 #figparams.fontSizePanel
#labelDis = 0.1

#labelPosX = [0.015, 0.355, 0.68]   # Horiz position for panel labels
#labelPosY = [0.92]    # Vert position for panel labels

msRaster = 4
smoothWinSizePsth = 3
lwPsth = 3
downsampleFactorPsth = 1
soundFreqsToPlot = ['lowfreq','highfreq']

for indc, cellInfo in enumerate(cellsToPlot):
    alignment = cellInfo['alignment']
    brainRegion = cellInfo['brainRegion']
    cellName = cellInfo['cellName']
    for soundFreq in soundFreqsToPlot:
        fig = plt.gcf()
        fig.clf()
        fig.set_facecolor('w')
        figFilename = 'rc_response_time_{}_{}_{}'.format(brainRegion, soundFreq, cellName)
        
        behavSumFilename = 'behavior_times_{}_{}_{}.npz'.format(soundFreq, animal, date)
        behavSumFullPath = os.path.join(dataDir,behavSumFilename)
        behavSum = np.load(behavSumFullPath)
        leftMoreTrialsOneFreq = behavSum['leftMoreTrials']
        rightMoreTrialsOneFreq = behavSum['rightMoreTrials']
        responseTimes = behavSum['responseTimes']
        

        
        plt.show()
        if SAVE_FIGURE:
            extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

