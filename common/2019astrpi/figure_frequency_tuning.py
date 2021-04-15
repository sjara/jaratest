# -*- coding: utf-8 -*-
"""
This script creates a summary plot for tuning curve data comparison using a database that has had
statistics added with `database_add_tuning_stats.py`. 

This script plots:
1. Latency (Delay in cell response)
2. BW10 (Bandwidth of cell response 10 dB above intensity threshold)
3. BW10 zoomed- (A zoomed-in version of BW10 to show more detail)
4. Threshold (The intensity with the maximum firing rate)
5. onset to sustianed ratio (Ratio of firing rate between onset (0-50ms after stimulus presentation)
and sustained (50-100ms after stimulus presentation) periods)

Run as:
figure_frequency_tuning.py SUBJECT TAG 

A database must exist with these parameters or script will fail. If the tuning statistics have not 
previously calculated and 'tuning' not in filename,'tuning' will be added to the filename. 
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

NO_TAG = 0 # Set to 1 if no tag 

# Determing run mode by arguments
if __name__ == "__main__":
    if sys.argv[1:] != []: # Checks if there are any arguments after the script name 
        arguments = sys.argv[1:] # Script parameters 
        if arguments[0] == "all":
            d1mice = studyparams.ASTR_D1_CHR2_MICE
            subjects = 'all'
        elif arguments[0].upper() == 'TEST':
            d1mice = studyparams.SINGLE_MOUSE
            subjects = studyparams.SINGLE_MOUSE[0]
        elif isinstance(arguments[0], str):
            d1mice = []
            subjects = arguments[0]
            d1mice.append(subjects)
            if d1mice[0] not in studyparams.ASTR_D1_CHR2_MICE:
                answer = input('Subject could not be found, Would you like to run for all animals?')
                if answer.upper() in ['YES', 'Y', '1']:
                    d1mice = studyparams.ASTR_D1_CHR2_MICE
                else:
                    sys.exit()
            else:
                print('Subject found in database')
        else:
            # If no mice are specified, default to using all mice in the studyparams
            d1mice = studyparams.ASTR_D1_CHR2_MICE
            subjects = 'all'
        if len(arguments) == 2:
            tag = arguments[1]
        else:
            NO_TAG = 1 
    else:
        d1mice = studyparams.ASTR_D1_CHR2_MICE
        subjects = 'all'
        NO_TAG = 1 
        
if NO_TAG == 1:
    inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                               'astrpi_{}_cells.h5'.format(subjects)) 
    outputDirectory = figparams.FIGURE_OUTPUT_DIR 
else:
    inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                               'astrpi_{}_cells_{}.h5'.format(subjects, tag))
    outputDirectory = figparams.FIGURE_OUTPUT_DIR 

figFilename = 'figure_{}'.format(studyparams.DATABASE_NAME)

# A value of 1 plots the given comparison, 0 does not 
LATENCY = 1 # Time of response relative to stimulus
BW10 = 1 # bandwidth of response 10 decibels above threshold response
THRESHOLD = 1 # Lowest amplitude of response at the characteristic frequency
ONSET = 1 # Ratio of response after stimulus between onset (0-50ms) and sustained (50-100ms) periods

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
axLatency = plt.subplot(gs[0, 0:2])
axBW10 = plt.subplot(gs[0, 2:4])
axBW10Zoomed = plt.subplot(gs[0, 4:6])
axThreshold = plt.subplot(gs[0, 6:8])
axOnset = plt.subplot(gs[0, 8:10])

# ========================== Latency ==========================

if LATENCY:
    # Parameters for cell selection for latency comparison
    latencyRatio = 0.35 # Ratio of response between onset within the FRA and baseline periods 
    latencyRate = 0.15 # Rate of response during the response period within the FRA
    
    # Selects only cells with latency values 
    latencydb = db.query('latency * 0 == 0')
    
    # Filters for cells with a sufficient response 
    latencydb = latencydb.query('tuningResponseFRIndex > {}'.format(latencyRatio))
    latencydb = latencydb.query('tuningResponseFR > {}'.format(latencyRate))
    latencydb = latencydb.query('bw10 > 0')

    # Seperates database into D1 and nD1 cells
    latencyD1db = latencydb.query(studyparams.D1_CELLS) # D1 cells
    latencynD1db = latencydb.query(studyparams.nD1_CELLS)
    
    # Creates array of latencies in milliseconds for each cell group 
    latencyD1 = latencyD1db['latency'] * 1000 # latency of each D1 cell in milliseconds
    latencynD1 = latencynD1db['latency'] * 1000 # latency of each nD1 cell in milliseconds
    
    # Calculates the median of the D1 and nD1 latencies 
    latencyMedD1 = latencyD1.median() # Median of D1 cell latency
    latencyMednD1 = latencynD1.median() # Median of nD1 cell latency
    
    # Calculates statistics for latency between cell type
    latencyzstat, latencypVal = stats.mannwhitneyu(latencynD1, latencyD1, alternative='two-sided')

    # Places Pval on plot 
    plt.text(-10.75, 1, 'pVal = {:.2f}'.format(latencypVal))
    
    # Plot label
    axLatency.set_ylabel('Latency (ms)', fontsize=fontSizeLabels)
        
    # Axis spacing and labels 
    axLatency.set_xticks(range(2))
    axLatency.set_xticklabels(['D1\n Median={:.2f} \n n={}'.format(latencyMedD1, len(latencyD1)), 
                               'nD1\n Median={:.2f} \n n={}'.format(latencyMednD1,
                                                                    len(latencynD1))])
    axLatency.set_xlim([-0.5, 1.5])
    # y-axis tick limits # To make graph look cleaner if verified no points below zero 
    # axLatency.set_ylim([0, 80])
    extraplots.set_ticks_fontsize(axLatency, fontSizeTicks) # Axis tick fontsize
    
    # plots latency of nD1 cells with a median line
    pos = jitter(np.ones(len(latencynD1))*1, dotSpread)
    axLatency.plot(pos, latencynD1, '.', color=colornD1)
    axLatency.plot([.85,1.15], [latencyMednD1, latencyMednD1], color='black', lw=4, alpha=0.6) 
    
    # Plots latency of D1 cells with a median line
    pos = jitter(np.ones(len(latencyD1))*0, dotSpread)
    axLatency.plot(pos, latencyD1, '.', color=colorD1)
    axLatency.plot([-.15,.15], [latencyMedD1, latencyMedD1], color='black', lw=4, alpha=0.6)
    
    # Removes box around entire plot 
    extraplots.boxoff(axLatency)  

# ========================== BW10 ==========================

if BW10: 
    # Selects cells that have a BW10 value
    BW10db = db.query("bw10 * 0 == 0")
    
    # Seperates database into D1 and nD1 cells
    BW10D1db = BW10db.query(studyparams.D1_CELLS) # D1 cells
    BW10nD1db = BW10db.query(studyparams.nD1_CELLS) # nD1 cells
    
    # Creates array of BW10 values for each cell group
    BW10D1 = BW10D1db["bw10"]
    BW10nD1 = BW10nD1db["bw10"]
    
    # Calculates the median of the D1 and nD1 BW10
    BW10MedD1 = BW10D1.median() # Median of D1 cell BW10
    BW10MednD1 = BW10nD1.median() # Median of nD1 cell BW10
    
    # Calculates statistics for BW10 between cell types 
    BW10zstat, BW10pVal = stats.mannwhitneyu(BW10nD1, BW10D1, alternative='two-sided')
    
    # Places Pval on plot 
    plt.text(-8, 1, 'pVal = {:.2f}'.format(BW10pVal))
    
    # Plot label 
    axBW10.set_ylabel('BW10', fontsize=fontSizeLabels)
    
    # Axis spacing and labels  
    axBW10.set_xticks(range(2))
    axBW10.set_xticklabels(['D1\n Median={:.2f} \n n={}'.format(BW10MedD1, len(BW10D1)),
                            'nD1\n Median={:.2f} \n n={}'.format(BW10MednD1, len(BW10nD1))]) 
    axBW10.set_xlim([-0.5, 1.5]) 
    extraplots.set_ticks_fontsize(axBW10, fontSizeTicks) # Sets tick fontsize
    
    # Plots BW10 for nD1 cells with a median line
    pos = jitter(np.ones(len(BW10nD1))*1, dotSpread)
    axBW10.plot(pos, BW10nD1, '.', color=colornD1)
    axBW10.plot([.85,1.15], [BW10MednD1, BW10MednD1], color='black', lw=4, alpha=0.6)
    
    # Plots BW10 for D1 cells with a median line
    pos = jitter(np.ones(len(BW10D1))*0, dotSpread)
    axBW10.plot(pos, BW10D1, '.', color=colorD1)
    axBW10.plot([-.15,.15], [BW10MedD1, BW10MedD1], color='black', lw=4, alpha=0.6) 
    
    extraplots.boxoff(axBW10) # Removes box around plot
   
# ========================== BW10 Zoomed ==========================
    
    # Plot label
    axBW10Zoomed.set_ylabel('BW10 Zoomed-in', fontsize=fontSizeLabels)
    
    # Axis spacing and labels  
    axBW10Zoomed.set_xticks(range(2)) # x-axis tick positioning 
    axBW10Zoomed.set_xticklabels(['D1\n Median={:.2f}'.format(BW10MedD1), 
                                  'nD1\n Median={:.2f}'.format(BW10MednD1)])
    axBW10Zoomed.set_xlim([-0.5, 1.5]) # x-axis tick limits 
    axBW10Zoomed.set_ylim([0, 1.5]) # y-axis tick limits 
    extraplots.set_ticks_fontsize(axBW10Zoomed, fontSizeTicks) # Sets tick fontsize
    
    # Plots BW10 zoomed for nD1 cells with a median line
    pos = jitter(np.ones(len(BW10nD1))*1, dotSpread*2)
    axBW10Zoomed.plot(pos, BW10nD1, '.', color=colornD1)
    axBW10Zoomed.plot([.80,1.20], [BW10MednD1, BW10MednD1], color='black', lw=4, alpha=0.6)
    
    # Plots BW10 zoomed for D1 cells with a median line
    pos = jitter(np.ones(len(BW10D1))*0, dotSpread*2)
    axBW10Zoomed.plot(pos, BW10D1, '.', color=colorD1)
    axBW10Zoomed.plot([-.20,.20], [BW10MedD1, BW10MedD1], color='black', lw=4, alpha=0.6)
    
    extraplots.boxoff(axBW10Zoomed) # Removes box around plot
   
# ========================== Threshold ==========================

if THRESHOLD:
    # Seperates database into D1 and nD1 cells
    thresholdD1db = db.query(studyparams.D1_CELLS) # D1 cells
    thresholdnD1db = db.query(studyparams.nD1_CELLS) # nD1 cells
    
    # Creates array of threshold values for each cell group
    thresholdD1 = thresholdD1db['thresholdFRA']
    thresholdnD1 = thresholdnD1db['thresholdFRA']
    
    zstat, pVal = stats.mannwhitneyu(thresholdnD1, thresholdD1, alternative='two-sided')
    
    plt.text(-2.6, -0.62, 'pVal = {:.2f}'.format(pVal))
    
    # Takes median of D1 and nD1 thresholds
    thresholdMedD1 = thresholdD1.median()
    thresholdMednD1 = thresholdnD1.median()
    
    # Plot label
    axThreshold.set_ylabel('Threshold (dB SPL)', fontsize=fontSizeLabels)
    
    # Axis spacing and labels
    axThreshold.set_xticks(range(2))
    axThreshold.set_xlim([-0.5, 1.5])
    extraplots.set_ticks_fontsize(axThreshold, fontSizeTicks)
    axThreshold.set_xticklabels(['D1\n Median={:.2f}'.format(thresholdMedD1), 
                                 'nD1\n Median={:.2f}'.format(thresholdMednD1)])
    
    plt.sca(axThreshold)
    spacing = 0.01 # Value for point spacing 
    
    # Plots threshold for nD1 cells with a median line
    markers = extraplots.spread_plot(1, thresholdnD1, spacing)
    plt.setp(markers, color=colornD1)
    axThreshold.plot([-.1,.1], [thresholdMedD1, thresholdMedD1], color='black', lw=10)
    
    # Plots threshold for D1 cells with a median line
    markers = extraplots.spread_plot(0, thresholdD1, spacing)
    plt.setp(markers, color=colorD1)
    axThreshold.plot([.9,1.1], [thresholdMednD1, thresholdMednD1], color='black', lw=10)
    
    extraplots.boxoff(axThreshold) # Removes box around plot

# ========================== Onset to Sustained Ratio ==========================

if ONSET:
    
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
    axOnset.set_ylabel('Onset to sustained ratio', fontsize=fontSizeLabels)
    
    # X-axis scaling and labels 
    axOnset.set_xticks(range(2))
    axOnset.set_xlim([-0.5, 1.5])
    axOnset.set_ylim([-0.51, 1.1])
    extraplots.set_ticks_fontsize(axOnset, fontSizeTicks)
    axOnset.set_xticklabels(['D1\n Median={:.2f}'.format(onsetMedD1), 
                             'nD1\n Median={:.2f}'.format(onsetMednD1)])
    
    # Plots onset to sustained ratio for nD1 cells with a median line
    pos = jitter(np.ones(len(onsetnD1))*1, dotSpread)
    axOnset.plot(pos, onsetnD1, '.', color=colornD1)
    axOnset.plot([.8,1.2], [onsetMednD1, onsetMednD1], color='black', lw=4, alpha=0.6)
    
    # Plots onset to sustained ratio for D1 cells with a median line
    pos = jitter(np.ones(len(onsetD1))*0, dotSpread)
    axOnset.plot(pos, onsetD1, '.', color=colorD1)
    axOnset.plot([-.2,.2], [onsetMedD1, onsetMedD1], color='black', lw=4, alpha=0.6)
    
    extraplots.boxoff(axOnset) # Removes box around plot 

# ========================== Saving ==========================

extraplots.save_figure(figFilename, 'pdf', figSize, outputDirectory)
plt.show()