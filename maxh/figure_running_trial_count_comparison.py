"""
Plot  change in running trials for each sessiontype.

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

SAVE_FIGURE = 0


# Change to cellDB 
filename = '/home/jarauser/Max/acid007_runningTrialCount.h5'
celldb = celldatabase.load_hdf(filename)

fontsize = 16

figsToPlot = [1,1,1,1]
experiments = ['01', '02', '03', '04']


#fig, axes = plt.subplots(figsize = (10,10))
fig = plt.gcf()
gsMain = gs.GridSpec(1, np.sum(figsToPlot), figure = fig)
gsMain.update(top=0.90, bottom=0.2, left=0.1, right=0.95, wspace=0.3, hspace=0.075)
#gsMain.update(top=0.95, bottom=0.1, left=0.35, right=0.95, wspace=0.3, hspace=0.075)
#plt.subplots_adjust(wspace=0.5)
barLoc = np.array([-0.6, 0, 0.6])

colors = {'saline':cp.TangoPalette['SkyBlue2'], 'doi': cp.TangoPalette['ScarletRed1']}

plt.suptitle(f'acid006 Oddball Running Trial Comparison', fontsize=16, fontweight='bold', y = 0.99)
fig.text(0.04, 0.5, 'Running Trial Count', va='center', rotation='vertical', fontsize = fontsize)


experiment_type = celldb.experiment.unique()

seperated_dbs = {}

for experiments in experiment_type:
   # newdb = celldb.loc[celldb['experiment'] == experiments]
    newdb = celldb[celldb['experiment'] == experiments][['date', 'pre_running_trial_count', 'saline_running_trial_count', 'doi_running_trial_count']]
    seperated_dbs[experiments] = newdb
    
    # for index, row in newdb.iterrows():


plotCount = 0

if figsToPlot[0]:
    date = seperated_dbs['01']['date']
    preCnt = seperated_dbs['01']['pre_running_trial_count']
    salineCnt = seperated_dbs['01']['saline_running_trial_count']
    doiCnt =seperated_dbs['01']['doi_running_trial_count']

    ax1 = plt.subplot(gsMain[plotCount])
    plt.axhline(0, ls=':', color='0.75')
    for i in date.index:
        plt.plot(barLoc, [preCnt[i], salineCnt[i], doiCnt[i]], '-', color = '0.5')

    plt.plot(np.tile(barLoc[0], len(preCnt)), preCnt, 'o', color= 'black')
    plt.plot(np.tile(barLoc[1], len(salineCnt)), salineCnt, 'o', color=colors['saline'])
    plt.plot(np.tile(barLoc[2], len(doiCnt)), doiCnt, 'o', color=colors['doi'])

    ax1.set_xlim([-1,1])
    ax1.set_xticks(barLoc)
    ax1.set_xticklabels(['Pre','Saline', 'DOI'])
    ax1.set_title("High Chord")
    #ax1.set_ylabel('Oddball enhancement index', fontsize = fontsize)
    #axes.set_ylim(0,5)
    #extraplots.boxoff(axes)
    extraplots.set_ticks_fontsize(ax1, fontsize)
    extraplots.boxoff(ax1)
    #extraplots.significance_stars(barLoc, 0.55, 0.02, color='0.75', starSize=10, gapFactor=0.1)
    plotCount = plotCount+1 

if figsToPlot[1]:
    date = seperated_dbs['02']['date']
    preCnt = seperated_dbs['02']['pre_running_trial_count']
    salineCnt = seperated_dbs['02']['saline_running_trial_count']
    doiCnt =seperated_dbs['02']['doi_running_trial_count']

    ax2 = plt.subplot(gsMain[plotCount])
    plt.axhline(0, ls=':', color='0.75')
    for i in date.index:
        plt.plot(barLoc, [preCnt[i], salineCnt[i], doiCnt[i]], '-', color = '0.5')

    plt.plot(np.tile(barLoc[0], len(preCnt)), preCnt, 'o', color= 'black')
    plt.plot(np.tile(barLoc[1], len(salineCnt)), salineCnt, 'o', color=colors['saline'])
    plt.plot(np.tile(barLoc[2], len(doiCnt)), doiCnt, 'o', color=colors['doi'])

    ax2.set_xlim([-1,1])
    ax2.set_xticks(barLoc)
    ax2.set_xticklabels(['Pre','Saline', 'DOI'])
    ax2.set_title("Low Chord")
    #ax1.set_ylabel('Oddball enhancement index', fontsize = fontsize)
    #axes.set_ylim(0,5)
    #extraplots.boxoff(axes)
    extraplots.set_ticks_fontsize(ax2, fontsize)
    extraplots.boxoff(ax2)
    #extraplots.significance_stars(barLoc, 0.55, 0.02, color='0.75', starSize=10, gapFactor=0.1)
    plotCount = plotCount+1 

if figsToPlot[2]:
    date = seperated_dbs['03']['date']
    preCnt = seperated_dbs['03']['pre_running_trial_count']
    salineCnt = seperated_dbs['03']['saline_running_trial_count']
    doiCnt =seperated_dbs['03']['doi_running_trial_count']

    ax3 = plt.subplot(gsMain[plotCount])
    plt.axhline(0, ls=':', color='0.75')
    for i in date.index:
        plt.plot(barLoc, [preCnt[i], salineCnt[i], doiCnt[i]], '-', color = '0.5')

    plt.plot(np.tile(barLoc[0], len(preCnt)), preCnt, 'o', color= 'black')
    plt.plot(np.tile(barLoc[1], len(salineCnt)), salineCnt, 'o', color=colors['saline'])
    plt.plot(np.tile(barLoc[2], len(doiCnt)), doiCnt, 'o', color=colors['doi'])

    ax3.set_xlim([-1,1])
    ax3.set_xticks(barLoc)
    ax3.set_xticklabels(['Pre','Saline', 'DOI'])
    ax3.set_title("FM Down")
    #ax1.set_ylabel('Oddball enhancement index', fontsize = fontsize)
    #axes.set_ylim(0,5)
    #extraplots.boxoff(axes)
    extraplots.set_ticks_fontsize(ax3, fontsize)
    extraplots.boxoff(ax3)
    #extraplots.significance_stars(barLoc, 0.55, 0.02, color='0.75', starSize=10, gapFactor=0.1)
    plotCount = plotCount+1 

if figsToPlot[3]:
    date = seperated_dbs['04']['date']
    preCnt = seperated_dbs['04']['pre_running_trial_count']
    salineCnt = seperated_dbs['04']['saline_running_trial_count']
    doiCnt =seperated_dbs['04']['doi_running_trial_count']

    ax4 = plt.subplot(gsMain[plotCount])
    plt.axhline(0, ls=':', color='0.75')
    for i in date.index:
        plt.plot(barLoc, [preCnt[i], salineCnt[i], doiCnt[i]], '-', color = '0.5')

    plt.plot(np.tile(barLoc[0], len(preCnt)), preCnt, 'o', color= 'black')
    plt.plot(np.tile(barLoc[1], len(salineCnt)), salineCnt, 'o', color=colors['saline'])
    plt.plot(np.tile(barLoc[2], len(doiCnt)), doiCnt, 'o', color=colors['doi'])

    ax4.set_xlim([-1,1])
    ax4.set_xticks(barLoc)
    ax4.set_xticklabels(['Pre','Saline', 'DOI'])
    ax4.set_title("FM Up")
    #ax1.set_ylabel('Oddball enhancement index', fontsize = fontsize)
    #axes.set_ylim(0,5)
    #extraplots.boxoff(axes)
    extraplots.set_ticks_fontsize(ax4, fontsize)
    extraplots.boxoff(ax4)
    #extraplots.significance_stars(barLoc, 0.55, 0.02, color='0.75', starSize=10, gapFactor=0.1)
    plotCount = plotCount+1 
plt.show()


'''
    upStat1, upP1 = scipy.stats.wilcoxon(upOddballIndexPre, upOddballIndexSaline)
    uptext(0.5, -0.1, f"Pre median: {preUpMed:.3f}", ha="center", transform=ax1.transAxes)
    ax1.text(0.5, -0.125, f"Saline median: {salineUpMed:.3f}", ha="center", transform=ax1.transAxes)
    ax1.text(0.5, -0.15, f"DOI median: {doiUpMed:.3f}", ha="center", transform=ax1.transAxes)

    ax1.text(0.5, -0.2, f"Pre to Saline p: {upP1:.4f}", ha="center", transform=ax1.transAxes)
    ax1.text(0.5, -0.225, f"Saline to DOI p: {upP2:.4f}", ha="center", transform=ax1.transAxes)

    ax1.set_title("FM Up", fontsize = fontsize)
    ax1.text(0.5, -0.1, f"Pre median: {preUpMed:.3f}", ha="center", transform=ax1.transAxes)
    ax1.text(0.5, -0.125, f"Saline median: {salineUpMed:.3f}", ha="center", transform=ax1.transAxes)
    ax1.text(0.5, -0.15, f"DOI median: {doiUpMed:.3f}", ha="center", transform=ax1.transAxes)

    ax1.text(0.5, -0.2, f"Pre to Saline p: {upP1:.4f}", ha="center", transform=ax1.transAxes)
    ax1.text(0.5, -0.225, f"Saline to DOI p: {upP2:.4f}", ha="center", transform=ax1.transAxes)


'''

print('done')




