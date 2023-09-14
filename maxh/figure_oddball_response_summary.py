"""
Plot  oddball enhancement index for all cells (for saline and DOI).

Based on generate_oddball_comparison_plots.py by Max Horrocks.
"""

import os
import sys
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import extraplots
from jaratoolbox import colorpalette as cp
import studyparams

SAVE_FIGURE = 1

subject = 'allMice'

"""
Choose which database type you're using.
1 = database with all trials.
2 = database with only nonrunning trials.
3 = database with only running trials.
"""
databaseType = 1


"""
Choose what criteria you want for cell selection.
1 = baseline firing rate of standard stimuli is less than firing rate during standard stimuli (saline)
2 = baseline firing rate of oddball stimuli is less than firing rate during oddball stimuli (saline)
3 = baseline firing rate of standard stimuli is less than firing rate during standard stimuli (pre)

"""
cell_selection_type = 1

"""
Cells are also selected by if the standard stimuli firing rate is above the firingThreshold under pre, saline, and DOI.
"""
firingThreshold = 5


if databaseType == 1:
    nameType = 'allTrials'
if databaseType == 2:
    nameType = 'nonRunningTrials'
if databaseType == 3:
    nameType = 'runningTrials'


dbPath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
#filename = os.path.join(dbPath, f'{subject}_puretone_and_oddball_calcs_{nameType}')


filename = '/home/jarauser/Max/allAcidCombined_20230825.h5'
celldb = celldatabase.load_hdf(filename)

#celldb = celldb.query('subject == @subject')

fontsize = 16
figsToPlot = [1, 1, 1, 1]

#fig, axes = plt.subplots(figsize = (10,10))
fig = plt.gcf()
gsMain = gs.GridSpec(1, np.sum(figsToPlot), figure = fig)
gsMain.update(top=0.90, bottom=0.2, left=0.1, right=0.95, wspace=0.3, hspace=0.075)
barLoc = np.array([-0.6, 0, 0.6])

colors = {'saline':cp.TangoPalette['SkyBlue2'], 'doi': cp.TangoPalette['ScarletRed1']}

plt.suptitle(f'{subject} mice oddball comparison', fontsize=16, fontweight='bold', y = 0.99)
fig.text(0.04, 0.5, 'Oddball Enhancement Index', va='center', rotation='vertical', fontsize = fontsize)


# FM 

upOddballIndexSalineColumn= celldb['upOddballIndexSaline']
upOddballIndexDOIColumn= celldb['upOddballIndexDOI']
upOddballIndexPreColumn= celldb['upOddballIndexPre']

upOddSpikesAvgSalineColumn = celldb['upOddSpikesAvgFiringRateSaline']
upOddSpikesAvgDOIColumn = celldb['upOddSpikesAvgFiringRateDOI']
upOddSpikesAvgPreColumn = celldb['upOddSpikesAvgFiringRatePre']

upStandSpikesAvgSalineColumn = celldb['upStandardSpikesAvgFiringRateSaline']
upStandSpikesAvgDOIColumn = celldb['upStandardSpikesAvgFiringRateDOI']
upStandSpikesAvgPreColumn = celldb['upStandardSpikesAvgFiringRatePre']

downOddballIndexSalineColumn= celldb['downOddballIndexSaline']
downOddballIndexDOIColumn= celldb['downOddballIndexDOI']
downOddballIndexPreColumn= celldb['downOddballIndexPre']

downOddSpikesAvgSalineColumn = celldb['downOddSpikesAvgFiringRateSaline']
downOddSpikesAvgDOIColumn = celldb['downOddSpikesAvgFiringRateDOI']
downOddSpikesAvgPreColumn = celldb['downOddSpikesAvgFiringRatePre']

downStandSpikesAvgSalineColumn = celldb['downStandardSpikesAvgFiringRateSaline']
downStandSpikesAvgDOIColumn = celldb['downStandardSpikesAvgFiringRateDOI']
downStandSpikesAvgPreColumn = celldb['downStandardSpikesAvgFiringRatePre']


baselineUpStandardFiringRateSaline = celldb['baselineUpStandardFiringRateSaline']
baselineDownStandardFiringRateSaline = celldb['baselineDownStandardFiringRateSaline']

baselineUpOddFiringRateSaline = celldb['baselineUpOddFiringRateSaline']
baselineDownOddFiringRateSaline = celldb['baselineDownOddFiringRateSaline']

baselineUpStandardFiringRatePre = celldb['baselineUpStandardFiringRatePre']
baselineDownStandardFiringRatePre = celldb['baselineDownStandardFiringRatePre']

baselineUpOddFiringRatePre = celldb['baselineUpOddFiringRatePre']
baselineDownOddFiringRatePre = celldb['baselineDownOddFiringRatePre']

# Chord

highOddballIndexSalineColumn= celldb['highOddballIndexSaline']
highOddballIndexDOIColumn= celldb['highOddballIndexDOI']
highOddballIndexPreColumn= celldb['highOddballIndexPre']

highOddSpikesAvgSalineColumn = celldb['highOddSpikesAvgFiringRateSaline']
highOddSpikesAvgDOIColumn = celldb['highOddSpikesAvgFiringRateDOI']
highOddSpikesAvgPreColumn = celldb['highOddSpikesAvgFiringRatePre']

highStandSpikesAvgSalineColumn = celldb['highStandardSpikesAvgFiringRateSaline']
highStandSpikesAvgDOIColumn = celldb['highStandardSpikesAvgFiringRateDOI']
highStandSpikesAvgPreColumn = celldb['highStandardSpikesAvgFiringRatePre']

lowOddballIndexSalineColumn= celldb['downOddballIndexSaline']
lowOddballIndexDOIColumn= celldb['downOddballIndexDOI']
lowOddballIndexPreColumn= celldb['downOddballIndexPre']

lowOddSpikesAvgSalineColumn = celldb['lowOddSpikesAvgFiringRateSaline']
lowOddSpikesAvgDOIColumn = celldb['lowOddSpikesAvgFiringRateDOI']
lowOddSpikesAvgPreColumn = celldb['lowOddSpikesAvgFiringRatePre']

lowStandSpikesAvgSalineColumn = celldb['lowStandardSpikesAvgFiringRateSaline']
lowStandSpikesAvgDOIColumn = celldb['lowStandardSpikesAvgFiringRateDOI']
lowStandSpikesAvgPreColumn = celldb['lowStandardSpikesAvgFiringRatePre']


baselineHighStandardFiringRateSaline = celldb['baselineHighStandardFiringRateSaline']
baselineLowStandardFiringRateSaline = celldb['baselineLowStandardFiringRateSaline']

baselineHighOddFiringRateSaline = celldb['baselineHighOddFiringRateSaline']
baselineLowOddFiringRateSaline = celldb['baselineLowOddFiringRateSaline']

baselineHighStandardFiringRatePre = celldb['baselineHighStandardFiringRatePre']
baselineLowStandardFiringRatePre = celldb['baselineLowStandardFiringRatePre']

baselineHighOddFiringRatePre = celldb['baselineHighOddFiringRatePre']
baselineLowOddFiringRatePre = celldb['baselineLowOddFiringRatePre']


if cell_selection_type == 1:
    selectionUp = (baselineUpStandardFiringRateSaline < upStandSpikesAvgSalineColumn)
    selectionDown = (baselineDownStandardFiringRateSaline < downStandSpikesAvgSalineColumn)
    selectionHigh = (baselineHighStandardFiringRateSaline < highStandSpikesAvgSalineColumn)
    selectionLow = (baselineLowStandardFiringRateSaline < lowStandSpikesAvgSalineColumn)
    selectionName = 'selection01'

if cell_selection_type == 2:
    selectionUp = (baselineUpOddFiringRateSaline < upOddSpikesAvgSalineColumn)
    selectionDown = (baselineDownOddFiringRateSaline < downOddSpikesAvgSalineColumn)
    selectionHigh = (baselineHighOddFiringRateSaline < highOddSpikesAvgSalineColumn)
    selectionLow = (baselineLowOddFiringRateSaline < lowOddSpikesAvgSalineColumn)
    selectionName = 'selection02'

if cell_selection_type == 3:
    selectionUp = (baselineUpStandardFiringRatePre < upStandSpikesAvgPreColumn)
    selectionDown = (baselineDownStandardFiringRatePre < downStandSpikesAvgPreColumn)
    selectionHigh = (baselineHighStandardFiringRatePre < highStandSpikesAvgPreColumn)
    selectionLow = (baselineLowStandardFiringRatePre < lowStandSpikesAvgPreColumn)
    selectionName = 'selection03'

# Cell Selection

selectedCellsUp = ((upStandSpikesAvgSalineColumn > firingThreshold) &
                   (upStandSpikesAvgDOIColumn > firingThreshold) &
                   (upStandSpikesAvgPreColumn > firingThreshold) &
                   selectionUp)

selectedCellsDown = ((downStandSpikesAvgSalineColumn > firingThreshold) &
                     (downStandSpikesAvgDOIColumn > firingThreshold) &
                     (downStandSpikesAvgPreColumn > firingThreshold) &
                     selectionDown)


selectedCellsHigh = ((highStandSpikesAvgSalineColumn > firingThreshold) &
                   (highStandSpikesAvgDOIColumn > firingThreshold) &
                   (highStandSpikesAvgPreColumn > firingThreshold) &
                   selectionHigh)


selectedCellsLow = ((lowStandSpikesAvgSalineColumn > firingThreshold) &
                     (lowStandSpikesAvgDOIColumn > firingThreshold) &
                     (lowStandSpikesAvgPreColumn > firingThreshold) &
                     selectionLow)


                                  

upOddballIndexSaline = upOddballIndexSalineColumn[selectedCellsUp].to_numpy()
upOddballIndexDOI = upOddballIndexDOIColumn[selectedCellsUp].to_numpy()
upOddballIndexPre = upOddballIndexPreColumn[selectedCellsUp].to_numpy()

downOddballIndexSaline = downOddballIndexSalineColumn[selectedCellsDown].to_numpy()
downOddballIndexDOI = downOddballIndexDOIColumn[selectedCellsDown].to_numpy()
downOddballIndexPre = downOddballIndexPreColumn[selectedCellsDown].to_numpy()

highOddballIndexSaline = highOddballIndexSalineColumn[selectedCellsHigh].to_numpy()
highOddballIndexDOI = highOddballIndexDOIColumn[selectedCellsHigh].to_numpy()
highOddballIndexPre = highOddballIndexPreColumn[selectedCellsHigh].to_numpy()

lowOddballIndexSaline = lowOddballIndexSalineColumn[selectedCellsLow].to_numpy()
lowOddballIndexDOI = lowOddballIndexDOIColumn[selectedCellsLow].to_numpy()
lowOddballIndexPre = lowOddballIndexPreColumn[selectedCellsLow].to_numpy()

cellCountUp = selectedCellsUp.sum()
cellCountDown = selectedCellsDown.sum()
cellCountHigh = selectedCellsHigh.sum()
cellCountLow = selectedCellsLow.sum()


plotCount = 0

if figsToPlot[0]:
    ax1 = plt.subplot(gsMain[plotCount])
    plt.axhline(0, ls=':', color='0.75')
    for i in range(len(upOddballIndexSaline)):
        plt.plot(barLoc, [upOddballIndexPre[i], upOddballIndexSaline[i], upOddballIndexDOI[i]], '-', color = '0.5')

    plt.plot(np.tile(barLoc[0], len(upOddballIndexPre)), upOddballIndexPre, 'o', color= 'black')
    plt.plot(np.tile(barLoc[1], len(upOddballIndexSaline)), upOddballIndexSaline, 'o', color=colors['saline'])
    plt.plot(np.tile(barLoc[2], len(upOddballIndexDOI)), upOddballIndexDOI, 'o', color=colors['doi'])

    ax1.set_xlim([-1,1])
    ax1.set_xticks(barLoc)
    ax1.set_xticklabels(['Pre','Saline', 'DOI'])
    #ax1.set_ylabel('Oddball enhancement index', fontsize = fontsize)
    #axes.set_ylim(0,5)
    #extraplots.boxoff(axes)
    extraplots.set_ticks_fontsize(ax1, fontsize)
    extraplots.boxoff(ax1)
    #extraplots.significance_stars(barLoc, 0.55, 0.02, color='0.75', starSize=10, gapFactor=0.1)
    plotCount = plotCount+1 

    upStat1, upP1 = scipy.stats.wilcoxon(upOddballIndexPre, upOddballIndexSaline)
    upStat2, upP2 = scipy.stats.wilcoxon(upOddballIndexSaline, upOddballIndexDOI)
    preUpMed = np.median(upOddballIndexPre)
    salineUpMed = np.median(upOddballIndexSaline)
    doiUpMed = np.median(upOddballIndexDOI)


    ax1.set_title("FM Up", fontsize = fontsize)
    ax1.text(0.5, -0.1, f"Pre median: {preUpMed:.3f}", ha="center", transform=ax1.transAxes)
    ax1.text(0.5, -0.125, f"Saline median: {salineUpMed:.3f}", ha="center", transform=ax1.transAxes)
    ax1.text(0.5, -0.15, f"DOI median: {doiUpMed:.3f}", ha="center", transform=ax1.transAxes)

    ax1.text(0.5, -0.2, f"Pre to Saline p: {upP1:.4f}", ha="center", transform=ax1.transAxes)
    ax1.text(0.5, -0.225, f"Saline to DOI p: {upP2:.10f}", ha="center", transform=ax1.transAxes)

    ax1.text(0.5, -0.25, f" Number of cells: {cellCountUp}", ha="center", transform=ax1.transAxes)



if figsToPlot[1]:
    ax2 = plt.subplot(gsMain[plotCount])
    plt.axhline(0, ls=':', color='0.75')
    for i in range(len(downOddballIndexSaline)):
        plt.plot(barLoc, [downOddballIndexPre[i], downOddballIndexSaline[i], downOddballIndexDOI[i]], '-', color = '0.5')

    plt.plot(np.tile(barLoc[0], len(downOddballIndexPre)), downOddballIndexPre, 'o', color= 'black')
    plt.plot(np.tile(barLoc[1], len(downOddballIndexSaline)), downOddballIndexSaline, 'o', color=colors['saline'])
    plt.plot(np.tile(barLoc[2], len(downOddballIndexSaline)), downOddballIndexDOI, 'o', color=colors['doi'])

    ax2.set_xlim([-1,1])
    ax2.set_xticks(barLoc)
    ax2.set_xticklabels(['Pre', 'Saline', 'DOI'])
    #ax2.set_ylabel('Oddball enhancement index', fontsize = fontsize)
    #axes.set_ylim(0,5)
    extraplots.boxoff(ax2)
    extraplots.set_ticks_fontsize(ax2, fontsize)
    plotCount = plotCount+1 

    downStat1, downP1 = scipy.stats.wilcoxon(downOddballIndexPre, downOddballIndexSaline)
    downStat2, downP2 = scipy.stats.wilcoxon(downOddballIndexSaline, downOddballIndexDOI)
    preDownMed = np.median(downOddballIndexPre)
    salineDownMed = np.median(downOddballIndexSaline)
    doiDownMed = np.median(downOddballIndexDOI)

    ax2.set_title("FM Down", fontsize = fontsize)
    ax2.text(0.5, -0.1, f"Pre median: {preDownMed:.3f}", ha="center", transform=ax2.transAxes)
    ax2.text(0.5, -0.125, f"Saline median: {salineDownMed:.3f}", ha="center", transform=ax2.transAxes)
    ax2.text(0.5, -0.15, f"DOI median: {doiDownMed:.3f}", ha="center", transform=ax2.transAxes)

    ax2.text(0.5, -0.2, f"Pre to Saline p: {downP1:.4f}", ha="center", transform=ax2.transAxes)
    ax2.text(0.5, -0.225, f"Saline to DOI p: {downP2:.4f}", ha="center", transform=ax2.transAxes)

    ax2.text(0.5, -0.25, f" Number of cells: {cellCountDown}", ha="center", transform=ax2.transAxes)


if figsToPlot[2]:
    ax3 = plt.subplot(gsMain[plotCount])
    plt.axhline(0, ls=':', color='0.75')
    for i in range(len(highOddballIndexSaline)):
        plt.plot(barLoc, [highOddballIndexPre[i], highOddballIndexSaline[i], highOddballIndexDOI[i]], '-', color = '0.5')

    plt.plot(np.tile(barLoc[0], len(highOddballIndexPre)), highOddballIndexPre, 'o', color= 'black')
    plt.plot(np.tile(barLoc[1], len(highOddballIndexSaline)), highOddballIndexSaline, 'o', color=colors['saline'])
    plt.plot(np.tile(barLoc[2], len(highOddballIndexDOI)), highOddballIndexDOI, 'o', color=colors['doi'])

    ax3.set_xlim([-1,1])
    ax3.set_xticks(barLoc)
    ax3.set_xticklabels(['Pre','Saline', 'DOI'])
    #ax3.set_ylabel('Oddball enhancement index', fontsize = fontsize)
    #axes.set_ylim(0,5)
    #extraplots.boxoff(axes)
    extraplots.set_ticks_fontsize(ax3, fontsize)
    extraplots.boxoff(ax3)
    #extraplots.significance_stars(barLoc, 0.55, 0.02, color='0.75', starSize=10, gapFactor=0.1)
    
    plotCount = plotCount+1 

    highStat1, highP1 = scipy.stats.wilcoxon(highOddballIndexPre, highOddballIndexSaline)
    highStat2, highP2 = scipy.stats.wilcoxon(highOddballIndexSaline, highOddballIndexDOI)
    preHighMed = np.median(highOddballIndexPre)
    salineHighMed = np.median(highOddballIndexSaline)
    doiHighMed = np.median(highOddballIndexDOI)

    ax3.set_title("High Chord", fontsize = fontsize)
    ax3.text(0.5, -0.1, f"Pre median: {preHighMed:.3f}", ha="center", transform=ax3.transAxes)
    ax3.text(0.5, -0.125, f"Saline median: {salineHighMed:.3f}", ha="center", transform=ax3.transAxes)
    ax3.text(0.5, -0.15, f"DOI median: {doiHighMed:.3f}", ha="center", transform=ax3.transAxes)

    ax3.text(0.5, -0.2, f"Pre to Saline p: {highP1:.4f}", ha="center", transform=ax3.transAxes)
    ax3.text(0.5, -0.225, f"Saline to DOI p: {highP2:.4f}", ha="center", transform=ax3.transAxes)

    ax3.text(0.5, -0.25, f" Number of cells: {cellCountHigh}", ha="center", transform=ax3.transAxes)


if figsToPlot[3]:
    ax4 = plt.subplot(gsMain[plotCount])
    plt.axhline(0, ls=':', color='0.75')
    for i in range(len(lowOddballIndexSaline)):
        plt.plot(barLoc, [lowOddballIndexPre[i], lowOddballIndexSaline[i], lowOddballIndexDOI[i]], '-', color = '0.5')

    plt.plot(np.tile(barLoc[0], len(lowOddballIndexPre)), lowOddballIndexPre, 'o', color= 'black')
    plt.plot(np.tile(barLoc[1], len(lowOddballIndexSaline)), lowOddballIndexSaline, 'o', color=colors['saline'])
    plt.plot(np.tile(barLoc[2], len(lowOddballIndexDOI)), lowOddballIndexDOI, 'o', color=colors['doi'])

    ax4.set_xlim([-1,1])
    ax4.set_xticks(barLoc)
    ax4.set_xticklabels(['Pre','Saline', 'DOI'])
    #ax4.set_ylabel('Oddball enhancement index', fontsize = fontsize)
    #axes.set_ylim(0,5)
    #extraplots.boxoff(axes)
    extraplots.set_ticks_fontsize(ax4, fontsize)
    extraplots.boxoff(ax4)
    #extraplots.significance_stars(barLoc, 0.55, 0.02, color='0.75', starSize=10, gapFactor=0.1)
    plotCount = plotCount+1

    lowStat1, lowP1 = scipy.stats.wilcoxon(lowOddballIndexPre, lowOddballIndexSaline)
    lowStat2, lowP2 = scipy.stats.wilcoxon(lowOddballIndexSaline, lowOddballIndexDOI)
    preLowMed = np.median(lowOddballIndexPre)
    salineLowMed = np.median(lowOddballIndexSaline)
    doiLowMed = np.median(lowOddballIndexDOI)

    ax4.set_title("Low Chord", fontsize = fontsize)
    ax4.text(0.5, -0.1, f"Pre median: {preLowMed:.3f}", ha="center", transform=ax4.transAxes)
    ax4.text(0.5, -0.125, f"Saline median: {salineLowMed:.3f}", ha="center", transform=ax4.transAxes)
    ax4.text(0.5, -0.15, f"DOI median: {doiLowMed:.3f}", ha="center", transform=ax4.transAxes)

    ax4.text(0.5, -0.2, f"Pre to Saline p: {lowP1:.4f}", ha="center", transform=ax4.transAxes)
    ax4.text(0.5, -0.225, f"Saline to DOI p: {lowP2:.4f}", ha="center", transform=ax4.transAxes)

    ax4.text(0.5, -0.25, f" Number of cells: {cellCountLow}", ha="center", transform=ax4.transAxes)

     

 # Goes through each psth plot and calculutes the lowest and highest ylimit values.
max_ylim = -np.inf
min_ylim = np.inf
for i, ax in enumerate(fig.get_axes()):
    ylim = ax.get_ylim()
    if ylim[0] < min_ylim:
        min_ylim = ylim[0]
    if ylim[1] > max_ylim:
        max_ylim = ylim[1]

# Iterates through each psth plot and changes the ylimits to the min and max ylimit.
new_ylimits = [min_ylim, max_ylim]
for i, ax in enumerate(fig.get_axes()):
    ax.set_ylim(new_ylimits)

upStat1, upP1 = scipy.stats.wilcoxon(upOddballIndexPre, upOddballIndexSaline)
upStat2, upP2 = scipy.stats.wilcoxon(upOddballIndexSaline, upOddballIndexDOI)
print(f'-- FM up --')
print(np.median(upOddballIndexPre))
print(np.median(upOddballIndexSaline))
print(np.median(upOddballIndexDOI))
print(f'Pre to Saline p = {upP1}\n')
print(f'Saline to DOI p = {upP2}\n')

downStat1, downP1 = scipy.stats.wilcoxon(downOddballIndexPre, downOddballIndexSaline)
downStat2, downP2 = scipy.stats.wilcoxon(downOddballIndexSaline, downOddballIndexDOI)
print(f'-- FM down --')
print(np.median(downOddballIndexPre))
print(np.median(downOddballIndexSaline))
print(np.median(downOddballIndexDOI))
print(f'Pre to Saline p = {downP1}\n')
print(f'Saline to DOI p = {downP2}\n')

highStat1, highP1 = scipy.stats.wilcoxon(highOddballIndexPre, highOddballIndexSaline)
highStat2, highP2 = scipy.stats.wilcoxon(highOddballIndexSaline, highOddballIndexDOI)
print(f'-- High Chord --')
print(np.median(highOddballIndexPre))
print(np.median(highOddballIndexSaline))
print(np.median(highOddballIndexDOI))
print(f'Pre to Saline p = {highP1}\n')
print(f'Saline to DOI p = {highP2}\n')

lowStat1, lowP1 = scipy.stats.wilcoxon(lowOddballIndexPre, lowOddballIndexSaline)
lowStat2, lowP2 = scipy.stats.wilcoxon(lowOddballIndexSaline, lowOddballIndexDOI)
print(f'-- Low Chord --')
print(np.median(lowOddballIndexPre))
print(np.median(lowOddballIndexSaline))
print(np.median(lowOddballIndexDOI))
print(f'Pre to Saline p = {lowP1}\n')
print(f'Saline to DOI p = {lowP2}\n')


if SAVE_FIGURE:
    figName = f'{subject}_comparison_oddball_index_{nameType}_{selectionName}'
    figurePath = os.path.join(settings.FIGURES_DATA_PATH, f'{subject}/')
    if not os.path.exists(figurePath):
        os.makedirs(figurePath)
    extraplots.save_figure(figName, 'png', [12, 10], outputDir= figurePath, facecolor='w')
elif SAVE_FIGURE == 0:
    plt.show()
