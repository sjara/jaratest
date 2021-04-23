# -*- coding: utf-8 -*-
"""
This script creates a summary plot for amplitude modulated session data comparison using a database 
that has had statistics added with `database_add_am_stats.py`. 

This script plots:
1. Highest Sustained Rate: Rate that gave the highest sustained (50-100ms after stimulus 
presentation) response
2. highest synchronization: Highest rate that cell synchronizes to by Rayleigh test
3. Percent Synchronization: Percentage of cells that synchronize in each cell type group
4. Rate discrimination Accuracy: Ability of a cell to discriminate ampitude modulation rates (value 
between 0 and 1, where 1 represents perfect discrimination)
6. Phase Discrimination Accuracy: Ability of a cell to determine the phase of different amplitude 
modulation rates (value between 0 and 1, where 1 represents perfect determination)

When run without arguments, this script will use the default database generated for all animals. 
This script can also be run using arguments to specify a specfic basic database that has been 
generated. The two arguments are "SUBJECT" and "TAG".

Run as (if not using tag)
`database_add_am_stats.py` or `database_add_am_stats.py SUBJECT`

Run as (if using tag)
`database_add_am_stats.py SUBJECT TAG`

The file `figparams.py` contains common parameters for figures and data related to these figures. 
"""
import os
import figparams
import studyparams
import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import extraplots
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import sys 

np.random.seed(7) # Seed for jitter function

# Creates variation in point spacing
def jitter(arr, dotSpread):
    jitter = (np.random.random(len(arr))-0.5)*dotSpread
    jitteredArr = arr + jitter
    return jitteredArr

dotSpread = 0.2 # Value for spread of points on figures (higher value equals greater spread) 

# ========================== Run Mode ==========================

TAG = 0 # Automatically set to 1 if tag given

# Determining animals used and file name by arguments given
if __name__ == '__main__':
    if sys.argv[1:] != []: # Checks if there are any arguments after the script name 
        arguments = sys.argv[1:] # Script parameters 
        if len(arguments) == 2:
                tag = arguments[1]
                TAG = 1
        if arguments[0].upper() in 'ALL':
            subjects = 'all'
        elif arguments[0].upper() == 'TEST':
            subjects = studyparams.SINGLE_MOUSE[0]
        elif isinstance(arguments[0], str):
            subjects = arguments[0]
            if subjects not in studyparams.ASTR_D1_CHR2_MICE:
                sys.exit('\n SUBJECT ERROR, DATAFRAME COULD NOT BE LOADED')
    else:
        subjects = 'all'
        print('No arguments given, default database with all animals will be used')
else:
    subjects = 'all'
    print("figure_am.py being ran as module, default database with all animals will be used")

if TAG == 1:
    inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                                   'astrpi_{}_cells_{}.h5'.format(subjects, tag))
    figFilename = 'astrpi_{}_cells_figure_am_{}'.format(subjects, tag)
else:
    inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                                   'astrpi_{}_cells.h5'.format(subjects)) 
    figFilename = 'astrpi_{}_cells_figure_am'.format(subjects)

dir = os.path.dirname(inputDirectory)

# Checks if file path exists
if os.path.isdir(dir):
    print('Directory Exists')
else:
    sys.exit('\n DIRECTORY ERROR, DATAFRAME COULD NOT LOADED') 

outputDirectory = figparams.FIGURE_OUTPUT_DIR 

# A value of 1 plots the given comparison, 0 does not 
HIGHESTSUSTAINED = 1 #
HIGHESTSYNC = 1 #
PERCENTSYNC = 0 #
RATEDISCRIM = 1 #
PHASEDISCRIM = 0 #

# Loads database for plotting 
db = celldatabase.load_hdf(inputDirectory)

# ========================== Figure Parameters ========================== 

# Figure size
figSize = [12, 8] 

# Colors 
colorD1 = figparams.colors['D1']
colornD1 = figparams.colors['nD1']

# Font size
fontSizeLabels = figparams.fontSizeLabels*2
fontSizeTicks = fontSizeLabels*0.5
fontSizePanel = figparams.fontSizePanel*2
fontSizeTitles = figparams.fontSizeTitles*2

# Clears the figure
fig = plt.gcf()
fig.clf()

# creates gridspec object and sets spacing 
gs = gridspec.GridSpec(1, 10)
gs.update(left=0.04, right=0.98, top=0.95, bottom=0.175, wspace=1.1, hspace=0.5)

# Creates axes objects for each plot
axHighestSustained = plt.subplot(gs[0, 0:2])
axHighestSync = plt.subplot(gs[0, 2:4])
axPercentSync = plt.subplot(gs[0, 4:6])
axRateDiscrim = plt.subplot(gs[0, 6:8])
axPhaseDiscrim = plt.subplot(gs[0, 8:10])

freqs = [4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128]

# ========================== Highest Rate Sustained ==========================

if HIGHESTSUSTAINED:    
    # Selects only cells with highest rate sustained values 
    highestSustaineddb = db.query('AMHighestRateSustained * 0 == 0')

    # Seperates database into D1 and nD1 cells
    highestSustainedD1db = highestSustaineddb.query(studyparams.D1_CELLS)
    highestSustainednD1db = highestSustaineddb.query(studyparams.nD1_CELLS)
    
    # Creates array of highest rate sustained 
    highestSustainedD1 = highestSustainedD1db['AMHighestRateSustained'] 
    highestSustainednD1 = highestSustainednD1db['AMHighestRateSustained']
    
    # Calculates the median of the D1 and nD1 latencies 
    highestSustainedMedD1 = highestSustainedD1.median() # Median of D1 cell latency
    highestSustainedMednD1 = highestSustainednD1.median() # Median of nD1 cell latency
    
    # Calculates the median of the D1 and nD1 latencies 
    highestSustainedMeanD1 = highestSustainedD1.mean() # Median of D1 cell latency
    highestSustainedMeannD1 = highestSustainednD1.mean() # Median of nD1 cell latency
    
    # Calculates statistics for latency between cell type
    zStat, pVal = stats.mannwhitneyu(highestSustainednD1, highestSustainedD1, alternative='two-sided')

    # Places Pval on plot 
    plt.text(-5.1, 1, 'pVal = {:.4f}'.format(pVal))
    
    # Plot label
    axHighestSustained.set_ylabel('Highest Sustained Period Rate (Hz)', fontsize=fontSizeLabels)
        
    # Axis spacing and labels 
    axHighestSustained.set_xticks(range(2))
    axHighestSustained.set_xticklabels(['D1\n Median={:.2f} \n n={}'.format(highestSustainedMedD1, len(highestSustainedD1)), 
                               'nD1\n Median={:.2f} \n n={}'.format(highestSustainedMednD1,
                                                                    len(highestSustainednD1))])
    axHighestSustained.set_xlim([-0.5, 1.5])
    axHighestSustained.set_yticks(freqs)
    axHighestSustained.set_ylim([0, 130])
    extraplots.set_ticks_fontsize(axHighestSustained, fontSizeTicks) # Axis tick fontsize
    
    # plots latency of nD1 cells with a median line
    pos = jitter(np.ones(len(highestSustainednD1))*1, dotSpread)
    axHighestSustained.plot(pos, highestSustainednD1, '.', color=colornD1)
    axHighestSustained.plot([.85,1.15], [highestSustainedMednD1, highestSustainedMednD1], color='black', lw=4, alpha=0.6) 
    axHighestSustained.plot([.85,1.15], [highestSustainedMeannD1, highestSustainedMeannD1], color='grey', lw=4, alpha=0.6)
    
    # Plots latency of D1 cells with a median line
    pos = jitter(np.ones(len(highestSustainedD1))*0, dotSpread)
    axHighestSustained.plot(pos, highestSustainedD1, '.', color=colorD1)
    axHighestSustained.plot([-.15,.15], [highestSustainedMedD1, highestSustainedMedD1], color='black', lw=4, alpha=0.6)
    axHighestSustained.plot([-.15,.15], [highestSustainedMeanD1, highestSustainedMeanD1], color='grey', lw=4, alpha=0.6)
    
    # Removes box around entire plot 
    extraplots.boxoff(axHighestSustained)  

# ========================== Highest Synchronization ==========================

if HIGHESTSYNC: 
    # Selects cells that have a highestSync value
    highestSyncdb = db.query("highestSyncCorrected * 0 == 0")
    
    # Seperates database into D1 and nD1 cells
    highestSyncD1db = highestSyncdb.query(studyparams.D1_CELLS)
    highestSyncnD1db = highestSyncdb.query(studyparams.nD1_CELLS)
    
    # Creates array of highest rate Sync 
    highestSyncD1 = highestSyncD1db['highestSyncCorrected'] 
    highestSyncnD1 = highestSyncnD1db['highestSyncCorrected']
    
    # Calculates the median of the D1 and nD1 latencies 
    highestSyncMedD1 = highestSyncD1.median() # Median of D1 cell latency
    highestSyncMednD1 = highestSyncnD1.median() # Median of nD1 cell latency
    
    # Calculates the median of the D1 and nD1 latencies 
    highestSyncMeanD1 = highestSyncD1.mean() # Median of D1 cell latency
    highestSyncMeannD1 = highestSyncnD1.mean() # Median of nD1 cell latency
    
    # Calculates statistics for latency between cell type
    zStat, pVal = stats.mannwhitneyu(highestSyncnD1, highestSyncD1, alternative='two-sided')

    # Places Pval on plot 
    plt.text(-3.8, 1, 'pVal = {:.4f}'.format(pVal))
    
    # Plot label
    axHighestSync.set_ylabel('Highest Synchronization (Hz)', fontsize=fontSizeLabels)
        
    # Axis spacing and labels 
    axHighestSync.set_xticks(range(2))
    axHighestSync.set_xticklabels(['D1\n Median={:.2f} \n n={}'.format(highestSyncMedD1, len(highestSyncD1)), 
                               'nD1\n Median={:.2f} \n n={}'.format(highestSyncMednD1,
                                                                    len(highestSyncnD1))])
    axHighestSync.set_xlim([-0.5, 1.5])
    axHighestSync.set_yticks(freqs)
    axHighestSync.set_ylim([0, 130])
    extraplots.set_ticks_fontsize(axHighestSync, fontSizeTicks) # Axis tick fontsize
    
    # plots latency of nD1 cells with a median line
    pos = jitter(np.ones(len(highestSyncnD1))*1, dotSpread)
    axHighestSync.plot(pos, highestSyncnD1, '.', color=colornD1)
    axHighestSync.plot([.85,1.15], [highestSyncMednD1, highestSyncMednD1], color='black', lw=4, alpha=0.6) 
    axHighestSync.plot([.85,1.15], [highestSyncMeannD1, highestSyncMeannD1], color='grey', lw=4, alpha=0.6)
    
    # Plots latency of D1 cells with a median line
    pos = jitter(np.ones(len(highestSyncD1))*0, dotSpread)
    axHighestSync.plot(pos, highestSyncD1, '.', color=colorD1)
    axHighestSync.plot([-.15,.15], [highestSyncMedD1, highestSyncMedD1], color='black', lw=4, alpha=0.6)
    axHighestSync.plot([-.15,.15], [highestSyncMeanD1, highestSyncMeanD1], color='grey', lw=4, alpha=0.6)
    
    # Removes box around entire plot 
    extraplots.boxoff(axHighestSync) 
   
# ========================== Percent Synchronization ==========================
    
if PERCENTSYNC:
    # Plot label
    axPercentSync.set_ylabel('BW10 Zoomed-in', fontsize=fontSizeLabels)
    
    # Axis spacing and labels  
    axPercentSync.set_xticks(range(2)) # x-axis tick positioning 
    axPercentSync.set_xticklabels(['D1\n Median={:.2f}'.format(BW10MedD1), 
                                  'nD1\n Median={:.2f}'.format(BW10MednD1)])
    axPercentSync.set_xlim([-0.5, 1.5]) # x-axis tick limits 
    axPercentSync.set_ylim([0, 1.5]) # y-axis tick limits 
    extraplots.set_ticks_fontsize(axPercentSync, fontSizeTicks) # Sets tick fontsize
    
    # Plots BW10 zoomed for nD1 cells with a median line
    pos = jitter(np.ones(len(BW10nD1))*1, dotSpread*2)
    axPercentSync.plot(pos, BW10nD1, '.', color=colornD1)
    axPercentSync.plot([.80,1.20], [BW10MednD1, BW10MednD1], color='black', lw=4, alpha=0.6)
    
    # Plots BW10 zoomed for D1 cells with a median line
    pos = jitter(np.ones(len(BW10D1))*0, dotSpread*2)
    axPercentSync.plot(pos, BW10D1, '.', color=colorD1)
    axPercentSync.plot([-.20,.20], [BW10MedD1, BW10MedD1], color='black', lw=4, alpha=0.6)
    
    extraplots.boxoff(axPercentSync) # Removes box around plot
   
# ========================== Rate Discrimination Accuracy  ==========================

if RATEDISCRIM:  
    # Selects only cells with highest rate sustained values 
    rateDiscrimdb = db.query('rateDiscrimAccuracy * 0 == 0')

    # Seperates database into D1 and nD1 cells
    rateDiscrimD1db = rateDiscrimdb.query(studyparams.D1_CELLS)
    rateDiscrimnD1db = rateDiscrimdb.query(studyparams.nD1_CELLS)
    
    # Creates array of highest rate sustained 
    rateDiscrimD1 = rateDiscrimD1db['rateDiscrimAccuracy'] 
    rateDiscrimnD1 = rateDiscrimnD1db['rateDiscrimAccuracy']
    max1 = rateDiscrimD1.max()
    max2 = rateDiscrimnD1.max()
    # Calculates the median of the D1 and nD1 latencies 
    rateDiscrimMedD1 = rateDiscrimD1.median() # Median of D1 cell latency
    rateDiscrimMednD1 = rateDiscrimnD1.median() # Median of nD1 cell latency
    
    # Calculates the median of the D1 and nD1 latencies 
    rateDiscrimMeanD1 = rateDiscrimD1.mean() # Median of D1 cell latency
    rateDiscrimMeannD1 = rateDiscrimnD1.mean() # Median of nD1 cell latency
    
    # Calculates statistics for latency between cell type
    zStat, pVal = stats.mannwhitneyu(rateDiscrimnD1, rateDiscrimD1, alternative='two-sided')

    # Places Pval on plot 
    plt.text(-1.1, 1, 'pVal = {:.4f}'.format(pVal))
    
    # Plot label
    axRateDiscrim.set_ylabel('Rate Discrimination accuracy', fontsize=fontSizeLabels)
        
    # Axis spacing and labels 
    axRateDiscrim.set_xticks(range(2))
    axRateDiscrim.set_xticklabels(['D1\n Median={:.2f} \n n={}'.format(rateDiscrimMedD1, len(rateDiscrimD1)), 
                               'nD1\n Median={:.2f} \n n={}'.format(rateDiscrimMednD1,
                                                                    len(rateDiscrimnD1))])
    axRateDiscrim.set_xlim([-0.5, 1.5])
    axRateDiscrim.set_yticks([0.5, 0.6, 0.7, 0.8, 0.9, 1])
    axRateDiscrim.set_ylim([0.5, 1])
    extraplots.set_ticks_fontsize(axRateDiscrim, fontSizeTicks) # Axis tick fontsize
    
    # plots latency of nD1 cells with a median line
    pos = jitter(np.ones(len(rateDiscrimnD1))*1, dotSpread)
    axRateDiscrim.plot(pos, rateDiscrimnD1, '.', color=colornD1)
    axRateDiscrim.plot([.85,1.15], [rateDiscrimMednD1, rateDiscrimMednD1], color='black', lw=4, alpha=0.6) 
    axRateDiscrim.plot([.85,1.15], [rateDiscrimMeannD1, rateDiscrimMeannD1], color='grey', lw=4, alpha=0.6)
    
    # Plots latency of D1 cells with a median line
    pos = jitter(np.ones(len(rateDiscrimD1))*0, dotSpread)
    axRateDiscrim.plot(pos, rateDiscrimD1, '.', color=colorD1)
    axRateDiscrim.plot([-.15,.15], [rateDiscrimMedD1, rateDiscrimMedD1], color='black', lw=4, alpha=0.6)
    axRateDiscrim.plot([-.15,.15], [rateDiscrimMeanD1, rateDiscrimMeanD1], color='grey', lw=4, alpha=0.6)
    
    # Removes box around entire plot 
    extraplots.boxoff(axRateDiscrim)

# ========================== Phase Discrimination Accuracy ==========================

if PHASEDISCRIM: 
    onsetdb = db.query('tuningResponseFRIndex > {}'.format(latencyRatio))
    onsetdb = onsetdb.query('tuningResponseFR > {}'.format(latencyRate))   
    onsetdb = onsetdb.query('bw10 > 0')
    # onsetdb = db
    
    # Seperates database into D1 and nD1 cells
    onsetD1db = onsetdb.query(studyparams.D1_CELLS) # D1 cells
    onsetnD1db = onsetdb.query(studyparams.nD1_CELLS) # nD1 cells
    
    # Creates array of onset to sustained ratio values for each cell group
    onsetD1 = onsetD1db['cfOnsetivityIndex']
    onsetnD1 = onsetnD1db['cfOnsetivityIndex']
    
    zstat, pVal = stats.mannwhitneyu(onsetnD1, onsetD1, alternative='two-sided')
    
    plt.text(2.8, 8, 'pVal = {:.2f}'.format(pVal))
    
    # Filters out any non-number values
    onsetD1 = onsetD1[onsetD1*0 == 0]
    onsetnD1 = onsetnD1[onsetnD1*0 == 0]
    
    # Takes median of D1 and nD1 onset to sustained ratios
    onsetMedD1 = np.median(onsetD1)
    onsetMednD1 = np.median(onsetnD1)
    
    # Plot label
    axPhaseDiscrim.set_ylabel('Onset to sustained ratio', fontsize=fontSizeLabels)
    
    # X-axis scaling and labels 
    axPhaseDiscrim.set_xticks(range(2))
    axPhaseDiscrim.set_xlim([-0.5, 1.5])
    axPhaseDiscrim.set_ylim([-0.51, 1.1])
    extraplots.set_ticks_fontsize(axPhaseDiscrim, fontSizeTicks)
    axPhaseDiscrim.set_xticklabels(['D1\n Median={:.2f}'.format(onsetMedD1), 
                             'nD1\n Median={:.2f}'.format(onsetMednD1)])
    
    # Plots onset to sustained ratio for nD1 cells with a median line
    pos = jitter(np.ones(len(onsetnD1))*1, dotSpread)
    axPhaseDiscrim.plot(pos, onsetnD1, '.', color=colornD1)
    axPhaseDiscrim.plot([.8,1.2], [onsetMednD1, onsetMednD1], color='black', lw=4, alpha=0.6)
    
    # Plots onset to sustained ratio for D1 cells with a median line
    pos = jitter(np.ones(len(onsetD1))*0, dotSpread)
    axPhaseDiscrim.plot(pos, onsetD1, '.', color=colorD1)
    axPhaseDiscrim.plot([-.2,.2], [onsetMedD1, onsetMedD1], color='black', lw=4, alpha=0.6)
    
    extraplots.boxoff(axPhaseDiscrim) # Removes box around plot 

# ========================== Saving ==========================

extraplots.save_figure(figFilename, 'pdf', figSize, outputDirectory)
plt.show()



# ########################
# import os
# import sys
# import figparams
# import studyparams
# import numpy as np
# from jaratoolbox import celldatabase
# from jaratoolbox import settings
# from jaratoolbox import extraplots
# from matplotlib import pyplot as plt
# import matplotlib.gridspec as gridspec
# from scipy import stats

# # ========================== Utility Functions ==========================

# np.random.seed(7) # Seed for jitter function

# # Creates variation in point spacing
# def jitter(arr, dotSpread):
#     jitter = (np.random.random(len(arr))-0.5)*dotSpread
#     jitteredArr = arr + jitter
#     return jitteredArr

# dotSpread = 0.2 # Value for spread of points on figures (higher value equals greater spread) 

# # ========================== Run Mode ==========================

# TAG = 0 # Automatically set to 1 if tag given

# # Determining animals used and file name by arguments given
# if __name__ == '__main__':
#     if sys.argv[1:] != []: # Checks if there are any arguments after the script name 
#         arguments = sys.argv[1:] # Script parameters 
#         if len(arguments) == 2:
#                 tag = arguments[1]
#                 TAG = 1
#         if arguments[0].upper() in 'ALL':
#             subjects = 'all'
#         elif arguments[0].upper() == 'TEST':
#             subjects = studyparams.SINGLE_MOUSE[0]
#         elif isinstance(arguments[0], str):
#             subjects = arguments[0]
#             if subjects not in studyparams.ASTR_D1_CHR2_MICE:
#                 sys.exit('\n SUBJECT ERROR, DATAFRAME COULD NOT BE LOADED')
#     else:
#         subjects = 'all'
#         print('No arguments given, default database with all animals will be used')
# else:
#     subjects = 'all'
#     print("figure_am.py being ran as module, default database with all animals will be used")

# if TAG == 1:
#     inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
#                                    'astrpi_{}_cells_{}.h5'.format(subjects, tag))
#     figFilename = 'astrpi_{}_cells_figure_am_{}'.format(subjects, tag)
# else:
#     inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
#                                    'astrpi_{}_cells.h5'.format(subjects)) 
#     figFilename = 'astrpi_{}_cells_figure_am'.format(subjects)

# dir = os.path.dirname(inputDirectory)

# # Checks if file path exists
# if os.path.isdir(dir):
#     print('Directory Exists')
# else:
#     sys.exit('\n DIRECTORY ERROR, DATAFRAME COULD NOT LOADED') 

# outputDirectory = figparams.FIGURE_OUTPUT_DIR   

# # A value of 1 plots the given comparison, 0 does not 
# HIGHESTSUSTAINED = 0 # 
# PERCENTSYNC = 0 # 
# RATEDiscrim= 0 # 
# PHASEDECRIM = 0 # 

# # Loads database for plotting 
# db = celldatabase.load_hdf(inputDirectory)

# # Filters for cells that have an AM response
# db = db.query('AMPval * 0 == 0')

# # ========================== Figure Parameters ========================== 

# # Figure size
# figSize = [12, 8] 

# # Colors 
# colorD1 = figparams.colors['D1']
# colornD1 = figparams.colors['nD1']

# # Font size
# fontSizeLabels = figparams.fontSizeLabels*2
# fontSizeTicks = fontSizeLabels*0.5
# fontSizePanel = figparams.fontSizePanel*2
# fontSizeTitles = figparams.fontSizeTitles*2

# # Clears the figure
# fig = plt.gcf()
# fig.clf()

# # creates gridspec object and sets spacing 
# gs = gridspec.GridSpec(1, 12)
# gs.update(left=0.04, right=0.98, top=0.95, bottom=0.175, wspace=1.1, hspace=0.5)

# # Creates axes objects for each plot

# axHighestSustained = plt.subplot(gs[0, 0:2])
# axPercentSyncn = plt.subplot(gs[0, 1:2])
# axRateDiscrim = plt.subplot(gs[0, 2:3])
# axPhaseDecrim = plt.subplot(gs[0, 3:4])

# # ========================== Highest Sustained Rate ==========================

# if HIGHESTSUSTAINED:  
#     highestSustaineddb = db

#     # Seperates database into D1 and nD1 cells
#     highestSustainedD1db = highestSustaineddb.query(studyparams.D1_CELLS) # D1 cells
#     highestSustainednD1db = highestSustaineddb.query(studyparams.nD1_CELLS)
    
#     # Creates array of latencies in milliseconds for each cell group 
#     highestSustainedD1 = highestSustainedD1db['AMHighestRateSustained'] # latency of each D1 cell in milliseconds
#     highestSustainednD1 = highestSustainednD1db['AMHighestRateSustained'] # latency of each nD1 cell in milliseconds
    
#     # Calculates the median of the D1 and nD1 highestSustained
#     highestSustainedMedD1 = highestSustainedD1.median() # Median of D1 cell highestSustained
#     highestSustainedMednD1 = highestSustainednD1.median() # Median of nD1 cell highestSustained
    
#     # Calculates statistics for highestSustained between cell types 
#     zStat, pVal = stats.mannwhitneyu(highestSustainednD1, highestSustainedD1, alternative='two-sided')
    
#     # Places Pval on plot 
#     plt.text(-8, 1, 'pVal = {:.2f}'.format(pVal))
    
#     # Plot label 
#     axHighestSustained.set_ylabel('highestSustained', fontsize=fontSizeLabels)
    
#     # Axis spacing and labels  
#     axHighestSustained.set_xticks(range(2))
#     axHighestSustained.set_xticklabels(['D1\n Median={:.2f} \n n={}'.format(highestSustainedMedD1, len(highestSustainedD1)),
#                             'nD1\n Median={:.2f} \n n={}'.format(highestSustainedMednD1, len(highestSustainednD1))]) 
#     axHighestSustained.set_xlim([-0.5, 1.5]) 
#     extraplots.set_ticks_fontsize(axHighestSustained, fontSizeTicks) # Sets tick fontsize
    
#     # Plots highestSustained for nD1 cells with a median line
#     pos = jitter(np.ones(len(highestSustainednD1))*1, dotSpread)
#     axHighestSustained.plot(pos, highestSustainednD1, '.', color=colornD1)
#     axHighestSustained.plot([.85,1.15], [highestSustainedMednD1, highestSustainedMednD1], color='black', lw=4, alpha=0.6)
    
#     # Plots highestSustained for D1 cells with a median line
#     pos = jitter(np.ones(len(highestSustainedD1))*0, dotSpread)
#     axHighestSustained.plot(pos, highestSustainedD1, '.', color=colorD1)
#     axHighestSustained.plot([-.15,.15], [highestSustainedMedD1, highestSustainedMedD1], color='black', lw=4, alpha=0.6) 
    
#     extraplots.boxoff(axHighestSustained) # Removes box around plot
   
# # ========================== Percent Synchronization ==========================

# if PERCENTSYNC:

#     annotateX = 0.2
#     annotateY = np.array([-0.3, -0.45]) + 0.1
#     rectX = annotateX-0.2
#     # rectY = [0.5825, 0.55]
#     rectY = annotateY
#     rectWidth = 0.15
#     rectHeight = 0.1

#     # TODO: Move these to the axis transform
#     axPercentSyncD1.annotate('Unsynchronized', xy=(annotateX, annotateY[0]), xycoords='axes fraction', fontsize=fontSizeTicks-2)
#     axPercentSyncnD1.annotate('Synchronized', xy=(annotateX, annotateY[1]), xycoords='axes fraction', fontsize=fontSizeTicks-2)

#     fig = plt.gcf()
#     rect1 = mpatches.Rectangle(xy=(rectX, rectY[0]), width=rectWidth, height=rectHeight, fc='w', ec='k', clip_on=False,
#                                transform=axACPie.transAxes)
#     rect2 = mpatches.Rectangle(xy=(rectX, rectY[1]), width=rectWidth, height=rectHeight, fc='k', ec='k', clip_on=False,
#                                transform=axACPie.transAxes)

#     axACPie.add_patch(rect1)
#     axACPie.add_patch(rect2)


#     popStatCol = 'highestSyncCorrected'
#     acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
#     acPopStat = acPopStat[pd.notnull(acPopStat)]
#     thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]
#     thalPopStat = thalPopStat[pd.notnull(thalPopStat)]

#     acSyncN = len(acPopStat[acPopStat > 0])
#     acNonSyncN = len(acPopStat[acPopStat == 0])
#     acSyncFrac = acSyncN/float(acSyncN + acNonSyncN)
#     acNonSyncFrac = acNonSyncN/float(acSyncN + acNonSyncN)

#     pieWedges = axACPie.pie([acNonSyncFrac, acSyncFrac], colors=['w', colornD1], shadow=False, startangle=0)
#     for wedge in pieWedges[0]:
#         wedge.set_edgecolor(colornD1)

#     # axACPie.annotate('Non-Sync\n{}%'.format(int(100*acNonSyncFrac)), xy=[0.8, 0.8], rotation=0, fontweight='bold', textcoords='axes fraction')
#     # axACPie.annotate('Sync\n{}%'.format(int(100*acSyncFrac)), xy=[-0.05, -0.05], rotation=0, fontweight='bold', textcoords='axes fraction')
#     fontSizePercent = 12
#     axACPie.annotate('{:0.0f}%'.format(np.round(100*acNonSyncFrac)), xy=[0.48, 0.6], rotation=0,
#                      fontweight='regular', textcoords='axes fraction', fontsize=fontSizePercent)
#     axACPie.annotate('{:0.0f}%'.format(np.round(100*acSyncFrac)), xy=[0.25, 0.25], rotation=0,
#                      fontweight='bold', textcoords='axes fraction', fontsize=fontSizePercent, color='w')
#     axACPie.set_aspect('equal')

#     thalSyncN = len(thalPopStat[thalPopStat > 0])
#     thalNonSyncN = len(thalPopStat[thalPopStat == 0])
#     thalSyncFrac = thalSyncN/float(thalSyncN + thalNonSyncN)
#     thalNonSyncFrac = thalNonSyncN/float(thalSyncN + thalNonSyncN)

#     pieWedges = axThalPie.pie([thalNonSyncFrac, thalSyncFrac], colors=['w', colorD1], shadow=False, startangle=0)
#     for wedge in pieWedges[0]:
#         wedge.set_edgecolor(colorD1)

#     # axThalPie.annotate('Non-Sync\n{}%'.format(int(100*thalNonSyncFrac)), xy=[0.8, 0.8], rotation=0, fontweight='bold', textcoords='axes fraction')
#     # axThalPie.annotate('Sync\n{}%'.format(int(100*thalSyncFrac)), xy=[-0.05, -0.05], rotation=0, fontweight='bold', textcoords='axes fraction')
#     axThalPie.annotate('{:0.0f}%'.format(np.round(100*thalNonSyncFrac)), xy=[0.57, 0.525], rotation=0,
#                      fontweight='regular', textcoords='axes fraction', fontsize=fontSizePercent)
#     axThalPie.annotate('{:0.0f}%'.format(np.round(100*thalSyncFrac)), xy=[0.2, 0.3], rotation=0,
#                        fontweight='bold', textcoords='axes fraction', fontsize=fontSizePercent, color='w')
#     axThalPie.set_aspect('equal')

#     oddsratio, pValue = stats.fisher_exact([[acSyncN, thalSyncN],
#                                             [acNonSyncN, thalNonSyncN]])
#     print("AC: {} Nonsync / {} total".format(acNonSyncN, acSyncN+acNonSyncN))
#     print("Thal: {} Nonsync / {} total".format(thalNonSyncN, thalSyncN+thalNonSyncN))
#     print("p-Val for fisher exact test: {}".format(pValue))
#     if pValue < 0.05:
#         starMarker = '*'
#     else:
#         starMarker = 'n.s.'


#     axThalPie.annotate('C', xy=(labelPosX[2], labelPosY[1]), xycoords='figure fraction',
#                        fontsize=fontSizePanel, fontweight='bold')
#     axThalPie.annotate('D', xy=(labelPosX[3], labelPosY[1]), xycoords='figure fraction',
#                        fontsize=fontSizePanel, fontweight='bold')
#     axThalPie.annotate('G', xy=(labelPosX[2], labelPosY[0]), xycoords='figure fraction',
#                        fontsize=fontSizePanel, fontweight='bold')
#     axThalPie.annotate('H', xy=(labelPosX[3], labelPosY[0]), xycoords='figure fraction',
#                        fontsize=fontSizePanel, fontweight='bold')

#     xBar = -2
#     # FarUntagged, CloseUntagged, tagged
#     yCircleCenters = [0, 3]
#     xTickWidth = 0.2
#     yGapWidth = 0.5

    # -- Plotting stars for the pie charts -- ######
    # def plot_y_lines_with_ticks(ax, x, y1, y2, gapwidth, tickwidth, color='k', starMarker="*", fontSize=9):
    #     ax.plot([x, x], [y1, np.mean([y1, y2])-(gapwidth/2)], '-', clip_on=False, color=color)
    #     ax.hold(1)
    #     ax.plot([x, x], [np.mean([y1, y2])+(gapwidth/2), y2], '-', clip_on=False, color=color)
    #     ax.plot([x, x+xTickWidth], [y1, y1], '-', clip_on=False, color=color)
    #     ax.plot([x, x+xTickWidth], [y2, y2], '-', clip_on=False, color=color)

    #     if starMarker == '*':
    #         ax.plot(x, np.mean([y1, y2]), starMarker, clip_on=False, ms=fontSizeStars, mfc='k', mec='None')
    #     else:
    #         ax.text(x, np.mean([y1, y2]), starMarker, fontsize=fontSize, rotation='vertical', va='center', ha='center', clip_on=False)


    # plot_y_lines_with_ticks(axACPie, xBar, yCircleCenters[0], yCircleCenters[1],
    #                         yGapWidth, xTickWidth, starMarker=starMarker)

    #####################################################

    # width = 0.5
    # plt.hold(1)
    # loc = [1, 2]
    # # axSummary.bar(loc[0]-width/2, thalNonSyncPercent, width, color=colorATh)
    # # axSummary.bar(loc[0]-width/2, thalSyncPercent, width, bottom=thalNonSyncPercent, color=colorATh, alpha=0.5)
    # # axSummary.bar(loc[1]-width/2, acNonSyncPercent, width, color=colorAC)
    # # axSummary.bar(loc[1]-width/2, acSyncPercent, width, bottom=acNonSyncPercent, color=colorAC, alpha=0.5)
    # axSummary.bar(loc[0], thalNonSyncPercent, width, color=colorATh)
    # axSummary.bar(loc[0], thalSyncPercent, width, bottom=thalNonSyncPercent, color=colorATh, alpha=0.5)
    # axSummary.bar(loc[1], acNonSyncPercent, width, color=colorAC)
    # axSummary.bar(loc[1], acSyncPercent, width, bottom=acNonSyncPercent, color=colorAC, alpha=0.5)
    # extraplots.boxoff(axSummary)

    # extraplots.new_significance_stars([1, 2], 105, 2.5, starMarker='*',
    #                                     fontSize=fontSizeStars, gapFactor=starGapFactor)

    # axSummary.text(2.65, 30, 'Non-Sync.', rotation=90, fontweight='bold')
    # axSummary.text(2.65, 75, 'Sync.', rotation=90, fontweight='bold', color='0.5')

    # axSummary.set_xlim([0.5, 2.6])
    # # extraplots.boxoff(axSummary)
    # axSummary.set_ylim([0, 100.5])
    # axSummary.set_xticks([1, 2])
    # tickLabels = ['ATh:Str', 'AC:Str']
    # axSummary.set_xticklabels(tickLabels)
    # axSummary.set_ylabel('% neurons', labelpad=-5)

    ##########################################################
########
    
        
#     # Seperates database into D1 and nD1 cells
#     thresholdD1db = db.query(studyparams.D1_CELLS) # D1 cells
#     thresholdnD1db = db.query(studyparams.nD1_CELLS) # nD1 cells
    
#     # Creates array of threshold values for each cell group
#     thresholdD1 = thresholdD1db['thresholdFRA']
#     thresholdnD1 = thresholdnD1db['thresholdFRA']
    
#     zStat, pVal = stats.mannwhitneyu(thresholdnD1, thresholdD1, alternative='two-sided')
    
#     plt.text(-2.6, -0.62, 'pVal = {:.2f}'.format(pVal))
    
#     # Takes median of D1 and nD1 thresholds
#     thresholdMedD1 = thresholdD1.median()
#     thresholdMednD1 = thresholdnD1.median()
    
#     # Plot label
#     axThreshold.set_ylabel('Threshold (dB SPL)', fontsize=fontSizeLabels)
    
#     # Axis spacing and labels
#     axThreshold.set_xticks(range(2))
#     axThreshold.set_xlim([-0.5, 1.5])
#     extraplots.set_ticks_fontsize(axThreshold, fontSizeTicks)
#     axThreshold.set_xticklabels(['D1\n Median={:.2f}'.format(thresholdMedD1), 
#                                  'nD1\n Median={:.2f}'.format(thresholdMednD1)])
    
#     plt.sca(axThreshold)
#     spacing = 0.01 # Value for point spacing 
    
#     # Plots threshold for nD1 cells with a median line
#     markers = extraplots.spread_plot(1, thresholdnD1, spacing)
#     plt.setp(markers, color=colornD1)
#     axThreshold.plot([-.1,.1], [thresholdMedD1, thresholdMedD1], color='black', lw=10)
    
#     # Plots threshold for D1 cells with a median line
#     markers = extraplots.spread_plot(0, thresholdD1, spacing)
#     plt.setp(markers, color=colorD1)
#     axThreshold.plot([.9,1.1], [thresholdMednD1, thresholdMednD1], color='black', lw=10)
    
#     extraplots.boxoff(axThreshold) # Removes box around plot
# # ========================== Rate Discrimination Accuracy ==========================

# if RATEDiscrim:
#     # dbPathRate = os.path.join(dataDir, 'celldatabase_with_am_discrimination_accuracy.h5')
#     dbPathRate = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 'celldatabase_calculated_columns.h5')
#     # dataframeRate = pd.read_hdf(dbPathRate, key='dataframe')
#     dataframeRate = celldatabase.load_hdf(dbPathRate)
#     # Show population distributions
#     colorATh = figparams.cp.TangoPalette['SkyBlue2']
#     colorAC = figparams.cp.TangoPalette['ScarletRed1']
#     # dataMS=5

#     goodISIRate = dataframeRate.query('isiViolations<0.02 or modifiedISI<0.02')
#     goodShapeRate = goodISIRate.query('spikeShapeQuality > 2')
#     goodLaserRate = goodShapeRate.query("autoTagged==1 and subject != 'pinp018'")
#     goodNSpikesRate = goodLaserRate.query('nSpikes>2000')

#     goodPulseLatency = goodNSpikesRate.query('summaryPulseLatency<0.01')

#     dbToUse = goodPulseLatency

#     acRate = dbToUse.groupby('brainArea').get_group('rightAC')
#     thalRate = dbToUse.groupby('brainArea').get_group('rightThal')

#     popStatCol = 'rateDiscrimAccuracy'
#     # popStatCol = 'accuracySustained'
#     acPopStat = acRate[popStatCol][pd.notnull(acRate[popStatCol])]
#     thalPopStat = thalRate[popStatCol][pd.notnull(thalRate[popStatCol])]

#     # plt.clf()
#     # axSummary = plt.subplot(111)
#     axSummary = plt.subplot(gs[1, 4])

#     jitterFrac = 0.2
#     pos = jitter(np.ones(len(thalPopStat))*0, jitterFrac)
#     axSummary.plot(pos, thalPopStat, 'o', mec=colorATh, mfc='None', alpha=1, ms=dataMS)
#     medline(np.median(thalPopStat), 0, 0.5)
#     pos = jitter(np.ones(len(acPopStat))*1, jitterFrac)
#     axSummary.plot(pos, acPopStat, 'o', mec=colorAC, mfc='None', alpha=1, ms=dataMS)
#     medline(np.median(acPopStat), 1, 0.5)
#     tickLabels = ['ATh:Str'.format(len(thalPopStat)), 'AC:Str'.format(len(acPopStat))]
#     axSummary.set_xticks(range(2))
#     axSummary.set_xticklabels(tickLabels, rotation=45)
#     extraplots.set_ticks_fontsize(axSummary, fontSizeLabels)
#     axSummary.set_ylim([0.5, 1])
#     yticks = [0.5, 0.6, 0.7, 0.8, 0.9, 1]
#     axSummary.set_yticks(yticks)
#     ytickLabels = ['50', '', '', '', '', '100']
#     axSummary.set_yticklabels(ytickLabels)
#     axSummary.set_ylabel('Discrimination accuracy\nof AM rate (%)', fontsize=fontSizeLabels, labelpad=-12)
#     # extraplots.set_ticks_fontsize(axSummary, fontSizeLabels)

#     zstat, pVal = stats.mannwhitneyu(thalPopStat, acPopStat)

#     messages.append("{} p={}".format("Rate discrimination accuracy", pVal))
#     messages.append("{} ATh n={}, AC n={}".format(popStatCol, len(thalPopStat), len(acPopStat)))

#     # plt.title('p = {}'.format(np.round(pVal, decimals=5)))

#     # axSummary.annotate('C', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
#     #             fontsize=fontSizePanel, fontweight='bold')

#     # starHeightFactor = 0.2
#     # starGapFactor = 0.3
#     # starYfactor = 0.1
#     yDataMax = max([max(acPopStat), max(thalPopStat)]) - 0.025
#     yStars = yDataMax + yDataMax*starYfactor
#     yStarHeight = (yDataMax*starYfactor)*starHeightFactor

#     starString = None if pVal < 0.05 else 'n.s.'
#     # fontSizeStars = 9
#     extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
#                                   starSize=fontSizeStars, starString=starString,
#                                   gapFactor=starGapFactor)
#     extraplots.boxoff(axSummary)
#     plt.hold(1)

# # ========================== Phase Discrimination Accuracy ==========================
    
# if PHASEDECRIM:
#     phasedb = db
    
#     # Seperates database into D1 and nD1 cells
#     phaseD1db = phasedb.query(studyparams.D1_CELLS) # D1 cells
#     phasenD1db = phasedb.query(studyparams.nD1_CELLS) # nD1 cells
    
#     # Creates array of onset to sustained ratio values for each cell group
#     phaseD1 = phaseD1db['cfOnsetivityIndex']
#     phasenD1 = phasenD1db['cfOnsetivityIndex']

#     possibleRateKeys = np.array([4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128])
#     ratesToUse = possibleRateKeys
#     keys = ['phaseDiscrimAccuracy_{}Hz'.format(rate) for rate in ratesToUse]

#     D1Data = np.full((len(phaseD1), len(ratesToUse)), np.nan)
#     nD1Data = np.full((len(phasenD1), len(ratesToUse)), np.nan)

#     for externalInd, (indRow, row) in enumerate(acPhase.iterrows()):
#         for indKey, key in enumerate(keys):
#             D1data[externalInd, indKey] = row[key]

#     for externalInd, (indRow, row) in enumerate(thalPhase.iterrows()):
#         for indKey, key in enumerate(keys):
#             thalData[externalInd, indKey] = row[key]

#     acMeanPerCell = np.nanmean(D1data, axis=1)
#     acMeanPerCell = acMeanPerCell[~np.isnan(acMeanPerCell)]
#     thalMeanPerCell = np.nanmean(thalData, axis=1)
#     thalMeanPerCell = thalMeanPerCell[~np.isnan(thalMeanPerCell)]

#     # plt.clf()

#     axSummary = plt.subplot(gs[1, 5])

#     jitterFrac = 0.2
#     pos = jitter(np.ones(len(thalMeanPerCell))*0, jitterFrac)
#     axSummary.plot(pos, thalMeanPerCell, 'o', mec=colorATh, mfc='None', alpha=1, ms=dataMS)
#     medline(np.median(thalMeanPerCell), 0, 0.5)
#     pos = jitter(np.ones(len(acMeanPerCell))*1, jitterFrac)
#     axSummary.plot(pos, acMeanPerCell, 'o', mec=colorAC, mfc='None', alpha=1, ms=dataMS)
#     medline(np.median(acMeanPerCell), 1, 0.5)
#     tickLabels = ['ATh:Str'.format(len(thalMeanPerCell)), 'AC:Str'.format(len(acMeanPerCell))]
#     axSummary.set_xticks(range(2))
#     axSummary.set_xticklabels(tickLabels, rotation=45)
#     extraplots.set_ticks_fontsize(axSummary, fontSizeLabels)
#     axSummary.set_ylim([0.5, 1])
#     yticks = [0.5, 0.6, 0.7, 0.8, 0.9, 1]
#     axSummary.set_yticks(yticks)
#     ytickLabels = ['50', '', '', '', '', '100']
#     axSummary.set_yticklabels(ytickLabels)
#     # axSummary.set_yticklabels(map(str, [50, 60, 70, 80, 90, 100]))
#     axSummary.set_ylabel('Discrimination accuracy\nof AM phase (%)', fontsize=fontSizeLabels, labelpad=-12)


#     zstat, pVal = stats.mannwhitneyu(thalMeanPerCell, acMeanPerCell)

#     messages.append("{} p={}".format("Phase discrimination accuracy", pVal))
#     messages.append("{} ATh n={}, AC n={}".format("Phase discrimination accuracy", len(thalPopStat), len(acPopStat)))

#     # plt.title('p = {}'.format(np.round(pVal, decimals=5)))

#     # axSummary.annotate('C', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
#     #             fontsize=fontSizePanel, fontweight='bold')

#     # starHeightFactor = 0.2
#     # starGapFactor = 0.3
#     # starYfactor = 0.1
#     yDataMax = max([max(acMeanPerCell), max(thalMeanPerCell)])
#     yStars = yDataMax + yDataMax*starYfactor
#     yStarHeight = (yDataMax*starYfactor)*starHeightFactor

#     starString = None if pVal < 0.05 else 'n.s.'
#     # fontSizeStars = 9
#     extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
#                                   starSize=fontSizeStars, starString=starString,
#                                   gapFactor=starGapFactor)

#     extraplots.boxoff(axSummary)
    
# # ========================== Saving ==========================

# extraplots.save_figure(figFilename, 'pdf', figSize, outputDirectory)
# plt.show()























# ################

# import os
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
# import matplotlib.patches as mpatches
# from jaratoolbox import settings
# from jaratoolbox import extraplots
# from jaratoolbox import behavioranalysis
# from jaratoolbox import spikesanalysis
# from jaratoolbox import celldatabase
# from scipy import stats
# import pandas as pd
# import figparams
# import studyparams

# FIGNAME = 'figure_am'
# d1mice = studyparams.ASTR_D1_CHR2_MICE
# nameDB = '_'.join(d1mice) + '.h5'
# # pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
# pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, '{}.h5'.format('temp'))
# # os.path.join(studyparams.PATH_TO_TEST,nameDB)
# db = celldatabase.load_hdf(pathtoDB)

# outputDir = '/var/tmp/figuresdata/2019astrpi/output'

# # # db = pd.read_hdf(dbPath, key='dataframe')
# # db = celldatabase.load_hdf(dbPath)
# # # db = db.query("subject=='pinp015'")
# # # goodLaser = db.query('pulsePval<0.05 and pulseZscore>0 and trainRatio>0.8')
# # # goodLaser = db[db['taggedCond']==0]
# # goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
# # goodShape = goodISI.query('spikeShapeQuality > 2')
# # goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")
# # # goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018' and summaryPulseLatency < 0.01")
# # goodNSpikes = goodLaser.query('nSpikes>2000')
# # goodPulseLatency = goodNSpikes.query('summaryPulseLatency<0.006')

# # goodSoundResponsiveBool = (~pd.isnull(goodNSpikes['BW10'])) | (~pd.isnull(goodNSpikes['highestSyncCorrected'])) | (goodNSpikes['noiseZscore']<0.05)
# # goodSoundResponsive = goodNSpikes[goodSoundResponsiveBool]

# d1mice = studyparams.ASTR_D1_CHR2_MICE
# nameDB = '_'.join(d1mice) + '.h5'
# # pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
# pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, '{}.h5'.format('temp'))
# # os.path.join(studyparams.PATH_TO_TEST,nameDB)
# db = celldatabase.load_hdf(pathtoDB)
# # TODO: Need to decide what we will filter AM by
# # db = db.query('rsquaredFit>{}'.format(studyparams.R2_CUTOFF))
# # exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME, 'data_AM_tuning_examples.npz')
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)

# # ac = dbToUse.groupby('brainArea').get_group('rightAC')
# # thal = dbToUse.groupby('brainArea').get_group('rightThal')

# np.random.seed(1)

# messages = []


# def jitter(arr, frac):
#     jitter = (np.random.random(len(arr))-0.5)*2*frac
#     jitteredArr = arr + jitter
#     return jitteredArr


# def medline(yval, midline, width, color='k', linewidth=3):
#     start = midline-(width/2)
#     end = midline+(width/2)
#     plt.plot([start, end], [yval, yval], color=color, lw=linewidth)


# PANELS = [1, 1, 1, 1, 0, 0, 0]

# SAVE_FIGURE = 1
# # outputDir = '/tmp/'
# # outputDir = '/mnt/jarahubdata/reports/nick/20171218_all_2018thstr_figures'
# # outputDir = figparams.FIGURE_OUTPUT_DIR
# figFilename = 'plots_am_tuning' # Do not include extension
# figFormat = 'pdf'  # 'pdf' or 'svg'
# # figFormat = 'pdf' # 'pdf' or 'svg'
# # figSize = [13, 8]  # In inches

# fullPanelWidthInches = 6.9
# figSizeFactor = 2
# figWidth = fullPanelWidthInches * figSizeFactor
# figHeight = figWidth / 1.625
# figSize = [figWidth, figHeight]  # In inches


# thalHistColor = '0.4'
# acHistColor = '0.4'

# fontSizeLabels = figparams.fontSizeLabels * figSizeFactor
# fontSizeTicks = figparams.fontSizeTicks * figSizeFactor
# fontSizePanel = figparams.fontSizePanel * figSizeFactor
# fontSizeTitles = 12

# # Params for extraplots significance stars
# fontSizeNS = figparams.fontSizeNS
# fontSizeStars = figparams.fontSizeStars
# starHeightFactor = figparams.starHeightFactor
# starGapFactor = figparams.starGapFactor
# starYfactor = figparams.starYfactor
# dotEdgeColor = figparams.dotEdgeColor
# dataMS = 6

# labelPosX = [0.02, 0.35, 0.68, 0.85]   # Horiz position for panel labels
# labelPosY = [0.46, 0.96]    # Vert position for panel labels

# # Define colors, use figparams
# laserColor = figparams.colp['blueLaser']
# colorD1 = figparams.cp.TangoPalette['SkyBlue2']
# colornD1 = figparams.cp.TangoPalette['ScarletRed1']

# fig = plt.gcf()
# plt.clf()
# fig.set_facecolor('w')

# gs = gridspec.GridSpec(2, 8)
# gs.update(left=0.05, right=0.98, top=0.94, bottom=0.10, wspace=0.8, hspace=0.5)

# # Load example data
# exampleDataPath = os.path.join(dataDir, 'data_am_examples.npz')
# exampleData = np.load(exampleDataPath, allow_pickle=True)

# exampleFreqEachTrial = exampleData['exampleFreqEachTrial'].item()
# exampleSpikeTimes = exampleData['exampleSpikeTimes'].item()
# exampleTrialIndexForEachSpike = exampleData['exampleTrialIndexForEachSpike'].item()
# exampleIndexLimitsEachTrial = exampleData['exampleIndexLimitsEachTrial'].item()

# axDirectCellEx1 = plt.subplot(gs[0, 0:2])
# axDirectFREx1 = plt.subplot(gs[0, 2])
# axDirectCellEx2 = plt.subplot(gs[0, 3:5])
# axDirectFREx2 = plt.subplot(gs[0, 5])
# axNonDirectEx1 = plt.subplot(gs[1, 0:2])
# axNonDirectFREx1 = plt.subplot(gs[1, 2])
# axNonDirectEx2 = plt.subplot(gs[1, 3:5])
# axNonDirectFREx2 = plt.subplot(gs[1, 5])
# axSyncPie = plt.subplot(gs[0, 6])
# axMaxSync = plt.subplot(gs[0, 7])
# axAccuracyAMRate = plt.subplot(gs[1, 6])
# axAccuracyAMPhase = plt.subplot(gs[1, 7])


# def plot_example_with_rate(axRaster, axFR, exampleName, color='k'):

#     spikeTimes = exampleSpikeTimes[exampleName]
#     indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
#     timeRange = [-0.2, 0.7]
#     freqEachTrial = exampleFreqEachTrial[exampleName]
#     possibleFreq = np.unique(freqEachTrial)
#     freqLabels = ['{0:.0f}'.format(freq) for freq in possibleFreq]
#     trialsEachCondition = behavioranalysis.find_trials_each_type(freqEachTrial, possibleFreq)
#     plt.sca(axRaster)
#     pRaster, hCond, zline = extraplots.raster_plot(spikeTimes, indexLimitsEachTrial,
#                                                     timeRange, trialsEachCondition, labels=freqLabels)
#     plt.setp(pRaster, ms=figparams.rasterMS)

#     blankLabels = ['']*11
#     for labelPos in [0, 5, 10]:
#         blankLabels[labelPos] = freqLabels[labelPos]

#     axRaster.set_yticklabels(blankLabels)

#     # ax = plt.gca()
#     axRaster.set_xticks([0, 0.5])
#     axRaster.set_xlabel('Time from\nsound onset (s)', fontsize=fontSizeLabels, labelpad=-1)
#     axRaster.set_ylabel('AM rate (Hz)', fontsize=fontSizeLabels, labelpad=-5)

#     # ax.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
#     #             fontsize=fontSizePanel, fontweight='bold')

#     countRange = [0.1, 0.5]
#     # spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimes, indexLimitsEachTrial, countRange)
#     # numSpikesInTimeRangeEachTrial = np.squeeze(spikeCountMat)
#     numSpikesInTimeRangeEachTrial = np.squeeze(np.diff(indexLimitsEachTrial,
#                                                         axis=0))

#     if len(numSpikesInTimeRangeEachTrial) == len(freqEachTrial)+1:
#         numSpikesInTimeRangeEachTrial = numSpikesInTimeRangeEachTrial[:-1]
#     conditionMatShape = np.shape(trialsEachCondition)
#     numRepeats = np.product(conditionMatShape[1:])
#     nSpikesMat = np.reshape(numSpikesInTimeRangeEachTrial.repeat(numRepeats),
#                             conditionMatShape)
#     spikesFilteredByTrialType = nSpikesMat * trialsEachCondition
#     avgSpikesArray = np.sum(spikesFilteredByTrialType, 0) / np.sum(
#         trialsEachCondition, 0).astype('float')/np.diff(np.array(countRange))
#     stdSpikesArray = np.std(spikesFilteredByTrialType, 0)/np.diff(np.array(countRange))

#     axRate = plt.subplot(axFR)
#     plt.sca(axRate)
#     nRates = len(possibleFreq)
#     plt.hold(True)
#     plt.plot(avgSpikesArray, range(nRates), 'ro-', mec='none', ms=6, lw=3, color=color)
#     plt.plot(avgSpikesArray-stdSpikesArray, range(len(possibleFreq)), 'k:')
#     plt.plot(avgSpikesArray+stdSpikesArray, range(len(possibleFreq)), 'k:')
#     axRate.set_ylim([-0.5, nRates-0.5])
#     axRate.set_yticks(range(nRates))
#     axRate.set_yticklabels([])

#     # ax = plt.gca()
#     axRate.set_xlabel('Firing rate\n(spk/s)', fontsize=fontSizeLabels, labelpad=-1)
#     extraplots.boxoff(axRate)
#     # extraplots.boxoff(ax, keep='right')

# if PANELS[0]:
#     plot_example_with_rate(axDirectCellEx1, axDirectFREx1, 'Direct1', color=colorD1)
#     axDirectCellEx1.set_title('Direct pathway example 1', fontsize=fontSizeTitles)
#     axDirectFREx1.set_xlim([0, 100])
#     axDirectFREx1.set_xticks([0, 100])
#     extraplots.set_ticks_fontsize(axDirectFREx1, fontSizeTicks)
#     extraplots.set_ticks_fontsize(axDirectCellEx1, fontSizeTicks)
# axDirectCellEx1.annotate('A', xy=(labelPosX[0], labelPosY[1]), xycoords='figure fraction',
#                           fontsize=fontSizePanel, fontweight='bold')

# if PANELS[1]:
#     plot_example_with_rate(axDirectCellEx2, axDirectFREx2, 'Direct2', color=colorD1)
#     axDirectCellEx2.set_title('Direct pathway example 2', fontsize=fontSizeTitles)
#     axDirectFREx2.set_xlim([0, 15])
#     axDirectFREx2.set_xticks([0, 15])
#     extraplots.set_ticks_fontsize(axDirectFREx2, fontSizeTicks)
#     extraplots.set_ticks_fontsize(axDirectCellEx2, fontSizeTicks)
# axDirectCellEx2.annotate('B', xy=(labelPosX[1], labelPosY[1]), xycoords='figure fraction',
#                           fontsize=fontSizePanel, fontweight='bold')

# if PANELS[2]:
#     plot_example_with_rate(axNonDirectEx1, axNonDirectFREx1, 'nDirect1', color=colornD1)
#     axNonDirectEx1.set_title('Non-direct pathway example 1', fontsize=fontSizeTitles)
#     axNonDirectFREx1.set_xlim([0, 35])
#     axNonDirectFREx1.set_xticks([0, 35])
#     extraplots.set_ticks_fontsize(axNonDirectFREx1, fontSizeTicks)
#     extraplots.set_ticks_fontsize(axNonDirectEx1, fontSizeTicks)
# axNonDirectEx1.annotate('E', xy=(labelPosX[0], labelPosY[0]), xycoords='figure fraction',
#                         fontsize=fontSizePanel, fontweight='bold')

# if PANELS[3]:
#     plot_example_with_rate(axNonDirectEx2, axNonDirectFREx2, 'nDirect2', color=colornD1)
#     axNonDirectEx2.set_title('Non-direct pathway example 2', fontsize=fontSizeTitles)
#     axNonDirectFREx2.set_xlim([0, 25])
#     axNonDirectFREx2.set_xticks([0, 25])
#     extraplots.set_ticks_fontsize(axNonDirectFREx2, fontSizeTicks)
#     extraplots.set_ticks_fontsize(axNonDirectEx2, fontSizeTicks)
# axNonDirectFREx2.annotate('F', xy=(labelPosX[1], labelPosY[0]), xycoords='figure fraction',
#                           fontsize=fontSizePanel, fontweight='bold')

# # ---------------- Highest Sync -------------------

# if PANELS[4]:
#     popStatCol = 'highestSyncCorrected'
#     acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
#     thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

#     acPopStat = acPopStat[acPopStat > 0]
#     thalPopStat = thalPopStat[thalPopStat > 0]

#     # possibleFreqLabels = ["{0:.1f}".format(freq) for freq in np.unique(thalPopStat)]
#     ytickLabels = [4, 8, 16, 32, 64, 128]
#     yticks = np.log(ytickLabels)

#     acPopStat = np.log(acPopStat)
#     thalPopStat = np.log(thalPopStat)

#     axSummary = plt.subplot(gs[0, 5])
#     spacing = 0.07
#     plt.sca(axSummary)

#     # pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
#     # axSummary.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=0.5)
#     plt.hold(1)
#     markers = extraplots.spread_plot(0, thalPopStat, spacing)
#     plt.setp(markers, mec=colorD1, mfc='None')
#     plt.setp(markers, ms=dataMS)

#     plt.hold(1)
#     medline(np.median(thalPopStat), 0, 0.5)
#     plt.hold(1)

#     # pos = jitter(np.ones(len(acPopStat))*1, 0.20)
#     # axSummary.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=0.5)
#     markers = extraplots.spread_plot(1, acPopStat, spacing)
#     plt.setp(markers, mec=colornD1, mfc='None')
#     plt.setp(markers, ms=dataMS)

#     plt.hold(1)
#     medline(np.median(acPopStat), 1, 0.5)
#     plt.hold(1)

#     axSummary.set_yticks(yticks)
#     axSummary.set_yticklabels(ytickLabels)


#     # tickLabels = ['ATh:Str\nn={}'.format(len(thalPopStat)), 'AC:Str\nn={}'.format(len(acPopStat))]
#     tickLabels = ['ATh:Str', 'AC:Str']
#     axSummary.set_xticks(range(2))
#     axSummary.set_xticklabels(tickLabels, rotation=45)
#     axSummary.set_xlim([-0.5, 1.5])
#     extraplots.set_ticks_fontsize(axSummary, fontSizeLabels)
#     extraplots.boxoff(axSummary)
#     # axSummary.set_yticks(np.unique(thalPopStat))
#     # axSummary.set_yticklabels(possibleFreqLabels)
#     # axSummary.set_ylim([-0.001, 0.161])


#     yDataMax = max([max(acPopStat), max(thalPopStat)])
#     yStars = yDataMax + yDataMax*starYfactor
#     yStarHeight = (yDataMax*starYfactor)*starHeightFactor

#     zVal, pVal = stats.mannwhitneyu(thalPopStat, acPopStat)
#     messages.append("{} p={}".format(popStatCol, pVal))
#     # if pVal < 0.05:
#     #     extraplots.new_significance_stars([0, 1], np.log(170), np.log(1.1), starMarker='*',
#     #                                         fontSize=fontSizeStars, gapFactor=starGapFactor)
#     # else:
#     #     extraplots.new_significance_stars([0, 1], np.log(170), np.log(1.1), starMarker='n.s.',
#     #                                         fontSize=fontSizeStars, gapFactor=starGapFactor)
#     starString = None if pVal < 0.05 else 'n.s.'
#     extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
#                                   starSize=fontSizeStars, starString=starString,
#                                   gapFactor=starGapFactor)

#     axSummary.set_ylim([np.log(3.6), np.log(150)])
#     axSummary.set_ylabel('Highest AM sync. rate (Hz)', labelpad=-1, fontsize=fontSizeLabels)
#     plt.hold(1)

#     # ---------------- Percent non-sync --------------------
#     # axSummary = plt.subplot(gs[0, 5])

#     pieChartGS = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[0, 4])

#     axThalPie = plt.subplot(pieChartGS[0, 0])
#     axACPie = plt.subplot(pieChartGS[1, 0])

#     annotateX = 0.2
#     annotateY = np.array([-0.3, -0.45]) + 0.1
#     rectX = annotateX-0.2
#     # rectY = [0.5825, 0.55]
#     rectY = annotateY
#     rectWidth = 0.15
#     rectHeight = 0.1

#     # TODO: Move these to the axis transform
#     axACPie.annotate('Unsynchronized', xy=(annotateX, annotateY[0]), xycoords='axes fraction', fontsize=fontSizeTicks-2)
#     axACPie.annotate('Synchronized', xy=(annotateX, annotateY[1]), xycoords='axes fraction', fontsize=fontSizeTicks-2)

#     fig = plt.gcf()
#     rect1 = mpatches.Rectangle(xy=(rectX, rectY[0]), width=rectWidth, height=rectHeight, fc='w', ec='k', clip_on=False,
#                                 transform=axACPie.transAxes)
#     rect2 = mpatches.Rectangle(xy=(rectX, rectY[1]), width=rectWidth, height=rectHeight, fc='k', ec='k', clip_on=False,
#                                 transform=axACPie.transAxes)

#     axACPie.add_patch(rect1)
#     axACPie.add_patch(rect2)


#     popStatCol = 'highestSyncCorrected'
#     acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
#     acPopStat = acPopStat[pd.notnull(acPopStat)]
#     thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]
#     thalPopStat = thalPopStat[pd.notnull(thalPopStat)]

#     acSyncN = len(acPopStat[acPopStat > 0])
#     acNonSyncN = len(acPopStat[acPopStat == 0])
#     acSyncFrac = acSyncN/float(acSyncN + acNonSyncN)
#     acNonSyncFrac = acNonSyncN/float(acSyncN + acNonSyncN)

#     pieWedges = axACPie.pie([acNonSyncFrac, acSyncFrac], colors=['w', colornD1], shadow=False, startangle=0)
#     for wedge in pieWedges[0]:
#         wedge.set_edgecolor(colornD1)

#     # axACPie.annotate('Non-Sync\n{}%'.format(int(100*acNonSyncFrac)), xy=[0.8, 0.8], rotation=0, fontweight='bold', textcoords='axes fraction')
#     # axACPie.annotate('Sync\n{}%'.format(int(100*acSyncFrac)), xy=[-0.05, -0.05], rotation=0, fontweight='bold', textcoords='axes fraction')
#     fontSizePercent = 12
#     axACPie.annotate('{:0.0f}%'.format(np.round(100*acNonSyncFrac)), xy=[0.48, 0.6], rotation=0,
#                       fontweight='regular', textcoords='axes fraction', fontsize=fontSizePercent)
#     axACPie.annotate('{:0.0f}%'.format(np.round(100*acSyncFrac)), xy=[0.25, 0.25], rotation=0,
#                       fontweight='bold', textcoords='axes fraction', fontsize=fontSizePercent, color='w')
#     axACPie.set_aspect('equal')

#     thalSyncN = len(thalPopStat[thalPopStat > 0])
#     thalNonSyncN = len(thalPopStat[thalPopStat == 0])
#     thalSyncFrac = thalSyncN/float(thalSyncN + thalNonSyncN)
#     thalNonSyncFrac = thalNonSyncN/float(thalSyncN + thalNonSyncN)

#     pieWedges = axThalPie.pie([thalNonSyncFrac, thalSyncFrac], colors=['w', colorD1], shadow=False, startangle=0)
#     for wedge in pieWedges[0]:
#         wedge.set_edgecolor(colorD1)

#     # axThalPie.annotate('Non-Sync\n{}%'.format(int(100*thalNonSyncFrac)), xy=[0.8, 0.8], rotation=0, fontweight='bold', textcoords='axes fraction')
#     # axThalPie.annotate('Sync\n{}%'.format(int(100*thalSyncFrac)), xy=[-0.05, -0.05], rotation=0, fontweight='bold', textcoords='axes fraction')
#     axThalPie.annotate('{:0.0f}%'.format(np.round(100*thalNonSyncFrac)), xy=[0.57, 0.525], rotation=0,
#                       fontweight='regular', textcoords='axes fraction', fontsize=fontSizePercent)
#     axThalPie.annotate('{:0.0f}%'.format(np.round(100*thalSyncFrac)), xy=[0.2, 0.3], rotation=0,
#                         fontweight='bold', textcoords='axes fraction', fontsize=fontSizePercent, color='w')
#     axThalPie.set_aspect('equal')

#     oddsratio, pValue = stats.fisher_exact([[acSyncN, thalSyncN],
#                                             [acNonSyncN, thalNonSyncN]])
#     print("AC: {} Nonsync / {} total".format(acNonSyncN, acSyncN+acNonSyncN))
#     print("Thal: {} Nonsync / {} total".format(thalNonSyncN, thalSyncN+thalNonSyncN))
#     print("p-Val for fisher exact test: {}".format(pValue))
#     if pValue < 0.05:
#         starMarker = '*'
#     else:
#         starMarker = 'n.s.'


#     axThalPie.annotate('C', xy=(labelPosX[2], labelPosY[1]), xycoords='figure fraction',
#                         fontsize=fontSizePanel, fontweight='bold')
#     axThalPie.annotate('D', xy=(labelPosX[3], labelPosY[1]), xycoords='figure fraction',
#                         fontsize=fontSizePanel, fontweight='bold')
#     axThalPie.annotate('G', xy=(labelPosX[2], labelPosY[0]), xycoords='figure fraction',
#                         fontsize=fontSizePanel, fontweight='bold')
#     axThalPie.annotate('H', xy=(labelPosX[3], labelPosY[0]), xycoords='figure fraction',
#                         fontsize=fontSizePanel, fontweight='bold')

#     xBar = -2
#     # FarUntagged, CloseUntagged, tagged
#     yCircleCenters = [0, 3]
#     xTickWidth = 0.2
#     yGapWidth = 0.5

#     # -- Plotting stars for the pie charts -- ######
#     # def plot_y_lines_with_ticks(ax, x, y1, y2, gapwidth, tickwidth, color='k', starMarker="*", fontSize=9):
#     #     ax.plot([x, x], [y1, np.mean([y1, y2])-(gapwidth/2)], '-', clip_on=False, color=color)
#     #     ax.hold(1)
#     #     ax.plot([x, x], [np.mean([y1, y2])+(gapwidth/2), y2], '-', clip_on=False, color=color)
#     #     ax.plot([x, x+xTickWidth], [y1, y1], '-', clip_on=False, color=color)
#     #     ax.plot([x, x+xTickWidth], [y2, y2], '-', clip_on=False, color=color)

#     #     if starMarker == '*':
#     #         ax.plot(x, np.mean([y1, y2]), starMarker, clip_on=False, ms=fontSizeStars, mfc='k', mec='None')
#     #     else:
#     #         ax.text(x, np.mean([y1, y2]), starMarker, fontsize=fontSize, rotation='vertical', va='center', ha='center', clip_on=False)


#     # plot_y_lines_with_ticks(axACPie, xBar, yCircleCenters[0], yCircleCenters[1],
#     #                         yGapWidth, xTickWidth, starMarker=starMarker)

#     #####################################################

#     # width = 0.5
#     # plt.hold(1)
#     # loc = [1, 2]
#     # # axSummary.bar(loc[0]-width/2, thalNonSyncPercent, width, color=colorATh)
#     # # axSummary.bar(loc[0]-width/2, thalSyncPercent, width, bottom=thalNonSyncPercent, color=colorATh, alpha=0.5)
#     # # axSummary.bar(loc[1]-width/2, acNonSyncPercent, width, color=colorAC)
#     # # axSummary.bar(loc[1]-width/2, acSyncPercent, width, bottom=acNonSyncPercent, color=colorAC, alpha=0.5)
#     # axSummary.bar(loc[0], thalNonSyncPercent, width, color=colorATh)
#     # axSummary.bar(loc[0], thalSyncPercent, width, bottom=thalNonSyncPercent, color=colorATh, alpha=0.5)
#     # axSummary.bar(loc[1], acNonSyncPercent, width, color=colorAC)
#     # axSummary.bar(loc[1], acSyncPercent, width, bottom=acNonSyncPercent, color=colorAC, alpha=0.5)
#     # extraplots.boxoff(axSummary)

#     # extraplots.new_significance_stars([1, 2], 105, 2.5, starMarker='*',
#     #                                     fontSize=fontSizeStars, gapFactor=starGapFactor)

#     # axSummary.text(2.65, 30, 'Non-Sync.', rotation=90, fontweight='bold')
#     # axSummary.text(2.65, 75, 'Sync.', rotation=90, fontweight='bold', color='0.5')

#     # axSummary.set_xlim([0.5, 2.6])
#     # # extraplots.boxoff(axSummary)
#     # axSummary.set_ylim([0, 100.5])
#     # axSummary.set_xticks([1, 2])
#     # tickLabels = ['ATh:Str', 'AC:Str']
#     # axSummary.set_xticklabels(tickLabels)
#     # axSummary.set_ylabel('% neurons', labelpad=-5)

#     ##########################################################


# # ---------------- Discrimination of Rate ----------------
# if PANELS[5]:
#     # dbPathRate = os.path.join(dataDir, 'celldatabase_with_am_discrimination_accuracy.h5')
#     dbPathRate = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 'celldatabase_calculated_columns.h5')
#     # dataframeRate = pd.read_hdf(dbPathRate, key='dataframe')
#     dataframeRate = celldatabase.load_hdf(dbPathRate)
#     # Show population distributions
#     colorATh = figparams.cp.TangoPalette['SkyBlue2']
#     colorAC = figparams.cp.TangoPalette['ScarletRed1']
#     # dataMS=5

#     goodISIRate = dataframeRate.query('isiViolations<0.02 or modifiedISI<0.02')
#     goodShapeRate = goodISIRate.query('spikeShapeQuality > 2')
#     goodLaserRate = goodShapeRate.query("autoTagged==1 and subject != 'pinp018'")
#     goodNSpikesRate = goodLaserRate.query('nSpikes>2000')

#     goodPulseLatency = goodNSpikesRate.query('summaryPulseLatency<0.01')

#     dbToUse = goodPulseLatency

#     acRate = dbToUse.groupby('brainArea').get_group('rightAC')
#     thalRate = dbToUse.groupby('brainArea').get_group('rightThal')

#     popStatCol = 'rateDiscrimAccuracy'
#     # popStatCol = 'accuracySustained'
#     acPopStat = acRate[popStatCol][pd.notnull(acRate[popStatCol])]
#     thalPopStat = thalRate[popStatCol][pd.notnull(thalRate[popStatCol])]

#     # plt.clf()
#     # axSummary = plt.subplot(111)
#     axSummary = plt.subplot(gs[1, 4])

#     jitterFrac = 0.2
#     pos = jitter(np.ones(len(thalPopStat))*0, jitterFrac)
#     axSummary.plot(pos, thalPopStat, 'o', mec=colorATh, mfc='None', alpha=1, ms=dataMS)
#     medline(np.median(thalPopStat), 0, 0.5)
#     pos = jitter(np.ones(len(acPopStat))*1, jitterFrac)
#     axSummary.plot(pos, acPopStat, 'o', mec=colorAC, mfc='None', alpha=1, ms=dataMS)
#     medline(np.median(acPopStat), 1, 0.5)
#     tickLabels = ['ATh:Str'.format(len(thalPopStat)), 'AC:Str'.format(len(acPopStat))]
#     axSummary.set_xticks(range(2))
#     axSummary.set_xticklabels(tickLabels, rotation=45)
#     extraplots.set_ticks_fontsize(axSummary, fontSizeLabels)
#     axSummary.set_ylim([0.5, 1])
#     yticks = [0.5, 0.6, 0.7, 0.8, 0.9, 1]
#     axSummary.set_yticks(yticks)
#     ytickLabels = ['50', '', '', '', '', '100']
#     axSummary.set_yticklabels(ytickLabels)
#     axSummary.set_ylabel('Discrimination accuracy\nof AM rate (%)', fontsize=fontSizeLabels, labelpad=-12)
#     # extraplots.set_ticks_fontsize(axSummary, fontSizeLabels)

#     zstat, pVal = stats.mannwhitneyu(thalPopStat, acPopStat)

#     messages.append("{} p={}".format("Rate discrimination accuracy", pVal))
#     messages.append("{} ATh n={}, AC n={}".format(popStatCol, len(thalPopStat), len(acPopStat)))

#     # plt.title('p = {}'.format(np.round(pVal, decimals=5)))

#     # axSummary.annotate('C', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
#     #             fontsize=fontSizePanel, fontweight='bold')

#     # starHeightFactor = 0.2
#     # starGapFactor = 0.3
#     # starYfactor = 0.1
#     yDataMax = max([max(acPopStat), max(thalPopStat)]) - 0.025
#     yStars = yDataMax + yDataMax*starYfactor
#     yStarHeight = (yDataMax*starYfactor)*starHeightFactor

#     starString = None if pVal < 0.05 else 'n.s.'
#     # fontSizeStars = 9
#     extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
#                                   starSize=fontSizeStars, starString=starString,
#                                   gapFactor=starGapFactor)
#     extraplots.boxoff(axSummary)
#     plt.hold(1)


# # -------------Discrimination of Phase -------------------
# if PANELS[6]:
#     dbPathPhase = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 'celldatabase_calculated_columns.h5')
#     # dbPhase = pd.read_hdf(dbPathPhase, key='dataframe')
#     dbPhase = celldatabase.load_hdf(dbPathPhase)

#     goodISIPhase = dbPhase.query('isiViolations<0.02 or modifiedISI<0.02')
#     goodShapePhase = goodISIPhase.query('spikeShapeQuality > 2')
#     goodLaserPhase = goodShapePhase.query("autoTagged==1 and subject != 'pinp018'")
#     goodNSpikesPhase = goodLaserPhase.query('nSpikes>2000')

#     acPhase = goodNSpikesPhase.groupby('brainArea').get_group('rightAC')
#     thalPhase = goodNSpikesPhase.groupby('brainArea').get_group('rightThal')

#     possibleRateKeys = np.array([4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128])
#     ratesToUse = possibleRateKeys
#     keys = ['phaseDiscrimAccuracy_{}Hz'.format(rate) for rate in ratesToUse]

#     acData = np.full((len(acPhase), len(ratesToUse)), np.nan)
#     thalData = np.full((len(thalPhase), len(ratesToUse)), np.nan)

#     for externalInd, (indRow, row) in enumerate(acPhase.iterrows()):
#         for indKey, key in enumerate(keys):
#             acData[externalInd, indKey] = row[key]

#     for externalInd, (indRow, row) in enumerate(thalPhase.iterrows()):
#         for indKey, key in enumerate(keys):
#             thalData[externalInd, indKey] = row[key]

#     acMeanPerCell = np.nanmean(acData, axis=1)
#     acMeanPerCell = acMeanPerCell[~np.isnan(acMeanPerCell)]
#     thalMeanPerCell = np.nanmean(thalData, axis=1)
#     thalMeanPerCell = thalMeanPerCell[~np.isnan(thalMeanPerCell)]

#     # plt.clf()

#     axSummary = plt.subplot(gs[1, 5])

#     jitterFrac = 0.2
#     pos = jitter(np.ones(len(thalMeanPerCell))*0, jitterFrac)
#     axSummary.plot(pos, thalMeanPerCell, 'o', mec=colorATh, mfc='None', alpha=1, ms=dataMS)
#     medline(np.median(thalMeanPerCell), 0, 0.5)
#     pos = jitter(np.ones(len(acMeanPerCell))*1, jitterFrac)
#     axSummary.plot(pos, acMeanPerCell, 'o', mec=colorAC, mfc='None', alpha=1, ms=dataMS)
#     medline(np.median(acMeanPerCell), 1, 0.5)
#     tickLabels = ['ATh:Str'.format(len(thalMeanPerCell)), 'AC:Str'.format(len(acMeanPerCell))]
#     axSummary.set_xticks(range(2))
#     axSummary.set_xticklabels(tickLabels, rotation=45)
#     extraplots.set_ticks_fontsize(axSummary, fontSizeLabels)
#     axSummary.set_ylim([0.5, 1])
#     yticks = [0.5, 0.6, 0.7, 0.8, 0.9, 1]
#     axSummary.set_yticks(yticks)
#     ytickLabels = ['50', '', '', '', '', '100']
#     axSummary.set_yticklabels(ytickLabels)
#     # axSummary.set_yticklabels(map(str, [50, 60, 70, 80, 90, 100]))
#     axSummary.set_ylabel('Discrimination accuracy\nof AM phase (%)', fontsize=fontSizeLabels, labelpad=-12)


#     zstat, pVal = stats.mannwhitneyu(thalMeanPerCell, acMeanPerCell)

#     messages.append("{} p={}".format("Phase discrimination accuracy", pVal))
#     messages.append("{} ATh n={}, AC n={}".format("Phase discrimination accuracy", len(thalPopStat), len(acPopStat)))

#     # plt.title('p = {}'.format(np.round(pVal, decimals=5)))

#     # axSummary.annotate('C', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
#     #             fontsize=fontSizePanel, fontweight='bold')

#     # starHeightFactor = 0.2
#     # starGapFactor = 0.3
#     # starYfactor = 0.1
#     yDataMax = max([max(acMeanPerCell), max(thalMeanPerCell)])
#     yStars = yDataMax + yDataMax*starYfactor
#     yStarHeight = (yDataMax*starYfactor)*starHeightFactor

#     starString = None if pVal < 0.05 else 'n.s.'
#     # fontSizeStars = 9
#     extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
#                                   starSize=fontSizeStars, starString=starString,
#                                   gapFactor=starGapFactor)

#     extraplots.boxoff(axSummary)

# print("\nSTATISTICS:\n")
# for message in messages:
#     print(message)
# print("\n")

# if SAVE_FIGURE:
#     extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
# plt.show()
