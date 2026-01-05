"""
This script plots changes in freq tuning from off to on.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import extraplots
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
import scipy.stats as stats 
import statsmodels.stats as mostats
import poni_params as studyparams
import poni_utils as studyutils
import ponifig_params as figparams
import importlib
importlib.reload(figparams)
importlib.reload(studyutils)
importlib.reload(studyparams)

pd.set_option('mode.chained_assignment', None)

subject = sys.argv[1]

if len(sys.argv) > 4:
    sessionDates = sys.argv[2].split(',')
    sessionDate = sessionDates[0]
    sessionType = sys.argv[3]
    probeDepths = [int(i) for i in sys.argv[4].split(',')]
    probeDepth = probeDepths[0]
    eventKey = sys.argv[5]

    if len(sys.argv) == 7:
        justCurves = True

    else:
        justCurves = False

else:
    sessionDates = studyparams.SESSION_DATES_EACH_SUBJECT[subject]
    probeDepths = studyparams.PDEPTH_EACH_SUBJECT[subject]
    sessionType = sys.argv[2]
    eventKey = sys.argv[3]

    sessionDate = 'all'
    probeDepth = 'all'

    if len(sys.argv) == 5:
        justCurves = True

    else:
        justCurves = False



# subject='poni001'
# sessionDate='2025-08-19'
# probeDepth=2360
# eventKey='Evoked'
    


SAVE_FIGURE = 1
SAVE=0
studyName = 'hemisym'
BTRmetric = studyparams.TIME_KEY_METRIC
# BTRmetric = 'ResponseMinPval'
# BTRmetric = 'GaussianMaxChange'
# BTRmetric = 'GaussianRsquare'
# BTRmetric = 'DiscrimBestFreq'
# BTRmetric = 'SelectivityKstat'
# BTRmetric = 'FanoFactor'
subjDir = os.path.join(settings.FIGURES_DATA_PATH,studyName,subject)
if not os.path.exists(subjDir):
    os.mkdir(subjDir)
outputDir = os.path.join(subjDir,sessionDate)
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
figFilename = f'plots_{eventKey}_{subject}_{sessionDate}_{sessionType}' # Do not include extension
figFormat = 'pdf' #or 'svg'
figSize = [20, 10] # In inches
modRates = studyparams.SESSION_MODRATES[sessionType]
nRates = len(modRates)

TIME_RANGES = studyparams.TIME_RANGES_AM if 'AM' in sessionType else studyparams.TIME_RANGES_FREQ
# metricAnnotation = 'VariabilityIndex'
metricAnnotation = 'FanoFactor'
# metricAnnotation = 'SelectivityKstat'
# metricAnnotation = 'FanoSelectivityComposite'

# cellsToPlot = [36,115,135]
# cellsToPlot=False



# if len(sys.argv)==6:
#     trialSubset = sys.argv[5]
#     figFilename = figFilename + '_' + trialSubset
#     figFormat = 'pdf'
# else:
#     trialSubset = ''
# if trialSubset not in ['', 'laser', 'nonLaser']:
#     raise ValueError("trialSubset must be '', 'laser', 'nonLaser'")

trialSubset = ''

# -- Example cells to plot --
#Cells with decrease: 149, 200, 430, 432, 669, 732, 806, 1145 
# cellsToPlot = [149, 125, 83]   # Best: 149, 200, 1145
#cellsToPlot = [1145, 125, 83]   # Best: 149, 200, 1145
#cellsToPlot = [407, 1320, 1474]  # Give negative estimated max firing rate on on


fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.002, 0.215, 0.43, 0.65, 0.825]   # Horiz position for panel labels
labelPosY = [0.96, 0.47]    # Vert position for panel labels

# -- Assigned colors (defined in figparams) --
colorsRasterDark = figparams.colors
colorsRasterLight = figparams.colorsLight
pColor = '0.5'
#colorsRasterDark = {'off': figparams.colors['off'], 'on': figparams.colors['on']} 
#colorsRasterLight = {'off': figparams.colorsLight['off'], 'on': figparams.colorsLight['on']} 
#Oddball = figparams.colors['oddball']
#colorStandard = figparams.colors['standard']

rasterMarkerSize = 0.4

def plot_stim(yLims, stimDuration, stimLineWidth=6, stimColor=figparams.colorStim):
    yPos = 1.02*yLims[-1] + 0.075*(yLims[-1]-yLims[0])
    pstim = plt.plot([0, stimDuration], 2*[yPos], lw=stimLineWidth, color=stimColor,
                     clip_on=False, solid_capstyle='butt')
    return pstim[0]

def get_shared_ax(gsSubFig,keep='none',yaxis=False):
    sharedAx = plt.subplot(gsSubFig)
    extraplots.boxoff(sharedAx,keep=keep,yaxis=yaxis)
    sharedAx.tick_params('both',labelcolor='#0000')

    return sharedAx

def gs_shared_xylabs(gsSubFig,xlab='',ylab='',xpad=5,ypad=10,fontsize=figparams.fontSizeLabels):
    sharedAx = get_shared_ax(gsSubFig)
    sharedAx.set_xlabel(xlab,labelpad=xpad,size=fontsize)
    sharedAx.set_ylabel(ylab,labelpad=ypad,size=fontsize)

def gs_panel_label(gsSubFig,label='A',fontSize=figparams.fontSizePanel,hpad=0,vpad=0):
    sharedAx = get_shared_ax(gsSubFig)
    sharedAx.text(-0.25+hpad, 1.05+vpad, label, transform=sharedAx.transAxes, 
                    size=fontSize, weight='bold')
# -- Load data --
dbPath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,f'celldb_{subject}_laser_freqtuning.h5')
celldbAll = celldatabase.load_hdf(dbFilename)



if trialSubset == 'laser':
    dbFilename = os.path.join(dbPath,f'celldb_{subject}_freqtuning_laser.h5')
    celldb = celldatabase.load_hdf(dbFilename)
elif trialSubset == 'nonLaser':
    dbFilename = os.path.join(dbPath,f'celldb_{subject}_freqtuning_nonLaser.h5')
    celldb = celldatabase.load_hdf(dbFilename)
else:
    celldb = celldbAll[(celldbAll['date'].apply(lambda x: x in sessionDates)) \
                       & (celldbAll['pdepth'].apply(lambda x: x in probeDepths))\
                        & (celldbAll['sessionType'].apply(lambda x: sessionType in x))]

nCells = len(celldb)
# -- Find best time range for each cell --
if eventKey == 'BTR':
    # print(f'Finding best time ranges based on {BTRmetric}')
    # bestKeys = studyutils.find_best_time_keys(celldb,BTRmetric,['Evoked','Delayed'])
    bestKeys = studyutils.find_best_time_keys(celldb,
                                              BTRmetric,['Onset','Sustained','Interim'],
                                              sessionType=sessionType)
    
    measurements = studyparams.METRICS[6:] 
    for indr,reagent in enumerate(studyparams.REAGENTS[sessionType]):
        celldb[reagent+'BestTimeRange']=bestKeys[indr]
        for metric in studyparams.METRICS[6:]:
            BTRs = []
            for indc,dbRow in celldb.iterrows():
                tKey = dbRow[reagent+'BestTimeRange']
                BTRs.append(dbRow[reagent+'Tone'+metric+tKey])
            
            celldb[reagent+'Tone'+metric+'BTR'] = BTRs


# -- Process data --
maxChangeFactor = studyparams.MAX_CHANGE_FACTOR

modRates = studyparams.SESSION_MODRATES[sessionType]


selective = studyutils.find_freq_selective(celldb, minR2=studyparams.MIN_R_SQUARED,sessionType=sessionType)
goodD = studyutils.find_good_dprime(celldb, eventKey,minDisc=studyparams.MIN_DPRIME,sessionType=sessionType)
goodFit = studyutils.find_good_gaussian_fit(celldb, eventKey,minR2=studyparams.MIN_R_SQUARED,sessionType=sessionType)

anyFitall = ~np.isnan(celldb[f'{modRates[0]}Hz_offToneGaussianA'+eventKey])
for mod in modRates[1:]:
    anyFitall &= ~np.isnan(celldb[f'{mod}Hz_offToneGaussianA'+eventKey])
highFiring = np.ones(len(celldb),dtype=bool)

RScell = studyutils.find_RS_cells(celldb)

for indr, reagent in enumerate(studyparams.REAGENTS[sessionType]):
    #celldb[reagent+'ToneGaussianMax'+eventKey] = ( celldb[reagent+'ToneGaussianA'+eventKey] +
    #                                      celldb[reagent+'ToneGaussianY0'+eventKey] )
    negResponseThisReagent = celldb[reagent+'ToneGaussianA'+eventKey]<0
    thisToneGaussianMax = ( celldb[reagent+'ToneGaussianA'+eventKey] +
                            celldb[reagent+'ToneGaussianY0'+eventKey] )
    thisToneGaussianMax[negResponseThisReagent] = celldb[reagent+'ToneGaussianY0'+eventKey]
    celldb[reagent+'ToneGaussianMax'+eventKey] = thisToneGaussianMax
    celldb[reagent+'ToneGaussianBandwidth'+eventKey] = \
        extraplots.gaussian_full_width_half_max(celldb[reagent+'ToneGaussianSigma'+eventKey])
    baselineFiringRate = celldb[reagent+'ToneBaselineFiringRate']
    celldb[reagent+'ToneGaussianMaxChange'+eventKey] = np.abs(thisToneGaussianMax-baselineFiringRate)
    if 'off' in reagent:
        highFiring &= (celldb[reagent+'ToneAvgEvokedFiringRate'+eventKey] > 1)# | (baselineFiringRate > 1)

    celldb[reagent+'ToneFanoSelectivityComposite'+eventKey] = celldb[reagent+'ToneSelectivityKstat'+eventKey]*celldb[reagent+'ToneFanoFactor'+eventKey]


posResponse = np.ones(len(celldb))
posMod = np.zeros(len(celldb),dtype=bool)
for mod in modRates:
    thisMetricoff = celldb[f'{mod}Hz_offTone'+metricAnnotation+eventKey]
    thisMetricon = celldb[f'{mod}Hz_onTone'+metricAnnotation+eventKey]
    celldb[f'{mod}Hz_ToneLaserModulation'+eventKey] = studyutils.modulation_index(thisMetricoff,thisMetricon)

    # posResponse &= (celldb[f'{mod}Hz_offToneGaussianA'+eventKey]>0)
    posMod |= (celldb[f'{mod}Hz_ToneLaserModulation'+eventKey] > 0)


responsive = studyutils.find_tone_responsive_cells(celldb, eventKey, frThreshold=studyparams.FR_THRESHOLD,allreagents=True,sessionType=sessionType)
#posResponse = (celldbAll['preToneGaussianA'+eventKey]>0) #& (celldbAll['offToneGaussianA'+eventKey]>0) #& (celldbAll['onToneGaussianA'+eventKey]>0)
# posResponse = (celldb['offToneGaussianA'+eventKey]>0) & (celldb['onToneGaussianA'+eventKey]>0)
#posResponse = (celldbAll['onToneGaussianA'+eventKey]>0)
#posResponse = (celldb['offToneGaussianMax'+eventKey]>0) & (celldb['onToneGaussianMax'+eventKey]>0)
# posResponse = (celldb['4Hz_offToneGaussianA'+eventKey]>0) & (celldb['64Hz_offToneGaussianA'+eventKey] > 0)
# posResponse = (celldb['4Hz_offToneGaussianMaxChange'+eventKey]>0) | (celldb['64Hz_offToneGaussianMaxChange'+eventKey] > 3)


steadyParams = ['BaselineFiringRate','BaselineSigma'] 
steady = studyutils.find_steady_cells(celldb, steadyParams, maxChangeFactor,sessionType=sessionType)

print(f'goodD\t\t{sum(goodD)} cells')
print(f'selective\t{sum(selective)} cells')
print(f'responsive\t{sum(responsive)} cells')
print(f'anyFitBoth\t{sum(anyFitall)} cells')
print(f'steady\t\t{sum(steady)} cells')
print(f'highFiring\t{sum(highFiring)} cells')


# selectedCells = goodFit  & posResponse & steady & anyFitall
selectedCells =  goodD & steady & highFiring #& posMod #& steady #& posMod #& RScell
# selectedCells = responsive  & goodFit 
# selectedCells = steady & selective #& goodFit & posResponse & anyFitall
# selectedCells = posResponse & goodFit & anyFitboth
# selectedCells = responsive  & goodFit 
# selectedCells = goodD  & steady  & RScell
# selectedCells = responsive   & selective #& RScell


cellsToPlot = sorted(np.nonzero(selectedCells)[0],
                     key=lambda x: np.mean([celldb.iloc[x][f'{mod}Hz_offToneSelectivityKstat'+eventKey] for mod in modRates]))[-4:-1]

# -- Save the updated celldb --
if SAVE:
    dbFilename = os.path.join(dbPath,f'celldb_{subject}_{sessionDate}_freqtuning.h5')
    celldatabase.save_hdf(celldb, dbFilename)
'''
metrics = ['ToneGaussianX0', 'ToneGaussianBandwidth', 'ToneGaussianMax']
metricsLabel = ['BF', 'Bandwidth', 'Max resp']
metricsUnits = ['kHz', 'oct', 'spk/s']
metricLims = [[np.log2(2000), np.log2(40000)], [0, 10], [0, 120]]
metricTicks = [[2000, 8000, 32000], [0, 5, 10], [0, 60, 120]]
'''

# -- Plot examples --
if not justCurves:
    # metrics = ['ToneGaussianX0'+eventKey, 'ToneGaussianBandwidth'+eventKey, 'ToneGaussianMaxChange'+eventKey]
    metrics = ['ToneFanoFactor'+eventKey, 'ToneMeanDiscrim'+eventKey, 'ToneSelectivityKstat'+eventKey]
    # metricsLabel = ['BF', 'Width', 'Max Δ']
    metricsLabel = ['FF', "d'", 'H-stat']
    #metricsLabel = ['BF', 'Bandwidth', 'Resp at BF']
    # metricsUnits = ['kHz', 'norm.', 'spk/s']
    # metricLims = [[np.log2(2000), np.log2(40000)], [0, 6], [0, 10]]
    # metricTicks = [[2000, 8000, 32000], [0, 5, 10], [0, 25, 50]]
    metricsUnits = ['AU', 'AU', 'oct']
    metricLims = [ [0, 10], [0, 10], [0, 300]]
    metricTicks = [ [0, 5, 10], [0,5,10], [0, 150, 300]]


    # -- Plot results --
    fig = plt.gcf()
    fig.clf()
    fig.set_facecolor('w')

    # -- Main gridspec --
    gsMain = gridspec.GridSpec(1, 4, width_ratios=[0.2, 0.2, 0.2, 0.4])
    gsMain.update(left=0.04, right=0.99, top=0.95, bottom=0.1, wspace=0.35, hspace=0.1)
    subfigure_labels = ['A','B','C','D','E','F','G']

    # # -- Show panel labels --
    # for indp, plabel in enumerate(['A','B','C','D','E']):
    #     plt.figtext(labelPosX[indp], labelPosY[0], plabel, fontsize=fontSizePanel, fontweight='bold')
    # for indp, plabel in enumerate(['F','G']):
    #     plt.figtext(labelPosX[indp+3], labelPosY[1], plabel, fontsize=fontSizePanel, fontweight='bold')

    # -- Raster and PSTH parameters --
    timeRange = [-0.5, 1.0]
    binWidth = 0.010
    timeVec = np.arange(timeRange[0], timeRange[-1], binWidth)
    smoothWinSizePsth = 2 
    lwPsth = 2.5
    downsampleFactorPsth = 1

    for indcell, cellInd in enumerate(cellsToPlot):
        gsExample = gsMain[0, indcell].subgridspec(2, 1, hspace=0.3)
        gs_panel_label(gsExample[0],subfigure_labels[indcell])

        gsRasters = gsExample[0].subgridspec(nRates, 1, hspace=0.1)
        gsTuning = gsExample[1].subgridspec(nRates,1, hspace=0.4)
        # axTuning = plt.subplot(gsExample[1])
        #cellInd, dbRow = celldatabase.find_cell(celldb, **cellsToPlot[indcell])
        dbRow = celldb.iloc[cellsToPlot[indcell]]
        oneCell = ephyscore.Cell(dbRow)
        
        reagentLabels = ['Laser OFF', 'Laser ON']
        allFits = []

        ephysData, bdata = oneCell.load(sessionType) 

        stimEachTrial = bdata['currentFreq']
        possibleStim = np.unique(stimEachTrial) 
        
        if 'AMtone' in sessionType:
            modEachTrial = bdata['currentMod']
            possibleMod = np.unique(modEachTrial)
        else:
            modEachTrial = np.zeros(stimEachTrial.shape)
            possibleMod = np.unique(modEachTrial)

        

        trialsEachLaser={}
        reagentsToPlot = []

        
        for indr,mod in enumerate(possibleMod):
            mod = int(mod)
        
            reagentsToPlot = [f'{mod}Hz_off',f'{mod}Hz_on']
            
            trialInds = np.nonzero(modEachTrial==mod)
            
            spikeTimes = ephysData['spikeTimes']
            eventOnsetTimes = ephysData['events']['stimOn'][trialInds]

            stimEachTrial = bdata['currentFreq'][trialInds]
            nTrials = len(stimEachTrial)

            laserEachTrial = bdata['laserTrial'][trialInds]
            possibleLaser = np.unique(laserEachTrial)
            
            # -- onng this before selecting trials by laser/nonLaser --
            possibleStim = np.unique(stimEachTrial)
            nStim = len(possibleStim)
            
            stimDuration = bdata['stimDur'][-1]

            # If the ephys data is 1 more than the bdata, delete the last ephys trial.
            if len(stimEachTrial) == len(eventOnsetTimes)-1:
                eventOnsetTimes = eventOnsetTimes[:len(stimEachTrial)]
            assert len(stimEachTrial) == len(eventOnsetTimes), \
                "Number of trials in behavior and ephys do not match for {oneCell}"

            (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

            # trialsEachCond = behavioranalysis.find_trials_each_type(stimEachTrial, possibleStim)

            trialsEachCond = behavioranalysis.find_trials_each_combination(stimEachTrial,possibleStim,
                                                                       laserEachTrial, possibleLaser)
            
            yticks_major = [possibleStim]*trialsEachCond.shape[2]

            # -- Estimate evoked firing rate for each stim --
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                    indexLimitsEachTrial,
                                                                    timeRange)

            # -- Plot Raster --
            axRaster = plt.subplot(gsRasters[indr])
            possibleStimInKHz = possibleStim/1000
            rasterLabels = ['']*nStim;
            rasterLabels[0] = int(possibleStimInKHz[0])
            rasterLabels[-1] = int(possibleStimInKHz[-1])

            rasterLabels *= trialsEachCond.shape[2]
            reagent=f'{mod}Hz_off'
            
            colorEachCond = [colorsRasterDark[sessionType][reagent], colorsRasterLight[sessionType][reagent]]*(nStim)
            (pRasterS,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial, timeRange,
                                                            trialsEachCond, labels=rasterLabels,
                                                            colorEachCond=colorEachCond,
                                                            rasterized=False)
            
            nTrialson = sum(bdata['laserTrial'][trialInds])
            nTrialsoff = sum(1-bdata['laserTrial'][trialInds])


            plt.setp(pRasterS, ms=rasterMarkerSize)
            if indr==1:
                plt.xlabel('Time (s)', fontsize=fontSizeLabels)
            plt.ylabel('Freq (kHz)', fontsize=fontSizeLabels)
            plt.axhline(nTrialsoff,color='r',linestyle='dashed',zorder=-10)

            plt.yticks([nTrialsoff//2,nTrialsoff+nTrialson//2],
                       ['off','on'],minor=True)
            ax = plt.gca()
            ax.tick_params(axis='y',which='minor',left=False, right=True, labelleft=False, labelright=True)
        
            if eventKey == 'BTR':
                plt.axvline(TIME_RANGES[dbRow[reagent+'BestTimeRange']][0],color='r',zorder=-10)
                plt.axvline(TIME_RANGES[dbRow[reagent+'BestTimeRange']][1],color='r',zorder=-10)
            #axRaster.set_yticklabels(['2']+['']*(nFreq-2)+['40'])
            if indr==0:
                plot_stim(plt.ylim(), stimDuration)
                plt.title(f'Cell #{cellInd}',loc='left')
                axRaster.set_xticklabels([])


            axTuning = plt.subplot(gsTuning[indr])
            
            # # ### plot firing rates

            # firingRatesOff = dbRow[f'{mod}Hz_off'+'ToneFiringRateEachFreq'+eventKey]
            # firingRatesOn = dbRow[f'{mod}Hz_on'+'ToneFiringRateEachFreq'+eventKey]

            # maxVal = max(firingRatesOff.max(), firingRatesOn.max())


            # plt.sca(axTuning)

            # linfit = stats.linregress(firingRatesOff,firingRatesOn)
            # xfit = np.linspace(0,25,50)
            # yfit = linfit.intercept + linfit.slope*xfit

            # plt.plot(firingRatesOff,firingRatesOn,'.', color=colorsRasterDark[sessionType][f"{mod}Hz_off"],label=f'{mod} Hz')
            # plt.plot(xfit,yfit,'-',color = colorsRasterDark[sessionType][f"{mod}Hz_off"])
            # plt.plot(xfit,xfit,'--',color='k')

            # plt.xlim([0,maxVal])
            # plt.ylim([0,maxVal])


            reagentsThisMod = [i for i in reagentsToPlot if str(mod) in i]
            
            for reagent in reagentsThisMod:
                # -- Plot tuning curve --
                plt.sca(axTuning)
                firingRates = dbRow[reagent+'ToneFiringRateEachFreq'+eventKey]
                fitParams = [dbRow[reagent+'ToneGaussianA'+eventKey], dbRow[reagent+'ToneGaussianX0'+eventKey],
                            dbRow[reagent+'ToneGaussianSigma'+eventKey], dbRow[reagent+'ToneGaussianY0'+eventKey]]
                # pdots, pfit = extraplots.plot_tuning_curve(possibleStim, firingRates, fitParams)
                pfit = plt.plot(np.log2(possibleStim), firingRates)
                pfit[0].set_color(colorsRasterDark[sessionType][reagent])
                allFits.append(pfit[0])
                if eventKey == 'BTR' and metricAnnotation=='':
                    plt.title(dbRow[f'{mod}Hz_off'+'BestTimeRange'] + ' ')
                # pdots[0].set_color(colorsRasterDark[sessionType][reagent])
                extraplots.boxoff(axTuning)
                xTicks = np.array([2000, 4000, 8000,16000, 32000])
                axTuning.set_xticks(np.log2(xTicks))
                axTuning.set_xticklabels((xTicks/1000).astype(int))
                axTuning.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
                axTuning.set_ylabel('Firing rate (spk/s)', fontsize=fontSizeLabels)
                # axTuning.set_title(f'Cell #{cellInd}',loc='left')

            if metricAnnotation:
                annoMetricoff = dbRow[f'{mod}Hz_offTone'+metricAnnotation+eventKey]
                annoMetricon = dbRow[f'{mod}Hz_onTone'+metricAnnotation+eventKey]

                if indr==0:
                    plt.title(f'{metricAnnotation}\n{mod}Hz: off={annoMetricoff:0.4f}, on={annoMetricon:0.4f}')
                else:
                    plt.title(f'{mod}Hz: off={annoMetricoff:0.4f}, on={annoMetricon:0.4f}')

                axTuning.legend(allFits, ['off','on'], 
                        loc='upper left', handlelength=1)
                    


        # axTuning.legend(allFits, ['4Hz off','4Hz on','64Hz off','64Hz on'], 
        #                 loc='upper left', handlelength=1)
        
        
        # plt.sca(axTuning)

        # change4hz = dbRow['4Hz_ToneLaserChangeEachFreq'+eventKey]
        # change64hz = dbRow['64Hz_ToneLaserChangeEachFreq'+eventKey]
        # cmap = plt.get_cmap('Purples',len(possibleStim))

        # for indstim, stim in enumerate(possibleStimInKHz):
        #     plt.plot([1,2],[change4hz[indstim],change64hz[indstim]],label=f'{stim} kHz',color=cmap(indstim))
        #     plt.scatter([1,2],[change4hz[indstim],change64hz[indstim]],label=f'{stim} kHz',color=cmap(indstim))
        
        # plt.xticks([1,2],['4 Hz', '64 Hz'])

        # axTuning.legend(loc='upper left', handlelength=1)


    # -- Plot metrics summary --        
    nCells = sum(selectedCells)
    gsMetrics = gsMain[0, 3].subgridspec(2, 2, hspace=0.4, wspace=0.4)
    gs_panel_label(gsMetrics[0,0],subfigure_labels[3])

    octaves = np.round(np.array(list(1-possibleStim[::-1]/2000)+list(abs(1-possibleStim[1:]/2000))),2)
    octRange = (abs(octaves) < 2.3)
    nOcts = len(octaves)

    gsFirstMetric = gsMetrics[0,0].subgridspec(nRates,1,hspace=0.6, wspace=0.4)

    for indr,mod in enumerate(modRates):
        thisAx = plt.subplot(gsFirstMetric[indr])
        thisMetricoff = np.array([*celldb[f'{mod}Hz_offToneNormResponseEachOctave'+eventKey][selectedCells]])
        thisMetricon = np.array([*celldb[f'{mod}Hz_onToneNormResponseEachOctave'+eventKey][selectedCells]])

        wstats,pvals = [],[]

        for indo,oct in enumerate(octaves):
            if octRange[indo]:
                notnans = (~np.isnan(thisMetricon[:,indo]) & ~np.isnan(thisMetricoff[:,indo]))

                wstat,pval=stats.wilcoxon(thisMetricoff[notnans][:,indo],thisMetricon[notnans][:,indo],
                                        correction=True, alternative='less')
                # wstat,pval = stats.ttest_rel(thisMetricoff[notnans][:,indo],thisMetricon[notnans][:,indo])


                wstats.append(wstat)
                pvals.append(pval)

                meanoff = np.nanmean(thisMetricoff,axis=0)
                stdoff = np.nanstd(thisMetricoff,axis=0)
                meanon = np.nanmean(thisMetricon,axis=0)
                stdon = np.nanstd(thisMetricon,axis=0)

                maxVal = max(meanoff[octRange].max(), meanon[octRange].max())

                plt.plot(octaves[octRange],meanoff[octRange],
                        color=colorsRasterDark[sessionType][f'{mod}Hz_off'],label=f'{mod}Hz_off')
                # plt.fill_between(octaves[octRange],
                #                  meanoff[octRange] + stdoff[octRange],
                #                  meanoff[octRange] - stdoff[octRange],
                #                  color=colorsRasterDark[sessionType][f'{mod}Hz_off'],
                #                  alpha=0.5)
                
                plt.plot(octaves[octRange],meanon[octRange],color=colorsRasterDark[sessionType][f'{mod}Hz_on'],label=f'{mod}Hz_on')
                
                # plt.xticks(np.arange(-2,3))
                plt.ylabel('Normalized Response')
                plt.xlabel('Octaves From Peak Response')
                plt.ylim([0,1.2])
                plt.yticks([0,0.25,0.5,0.75,1])
                plt.xticks(np.arange(-2,3))
                # plt.title(f'Mean Normalized Tone\nResponses {mod}Hz')
                plt.legend(['off','on'])
                # plt.fill_between(octaves[octRange],
                #                  meanon[octRange] + stdon[octRange],
                #                  meanon[octRange] - stdon[octRange],
                #                  color=colorsRasterDark[sessionType][f'{mod}Hz_on'],
                #                  alpha=0.5)
            
                if pval <= 0.001:
                    plt.annotate('***',                          
                        (oct, meanon[indo]),                 
                        textcoords='offset points',   
                        xytext=(0, 10),               
                        ha='center'                 
                    )
                elif pval <= 0.01:
                    plt.annotate('**',                          
                        (oct, meanon[indo]),                 
                        textcoords='offset points',   
                        xytext=(0, 10),               
                        ha='center'                    
                    )
                elif pval <= 0.05:
                    plt.annotate('*',                          
                        (oct, meanon[indo]),                 
                        textcoords='offset points',   
                        xytext=(0, 10),               
                        ha='center'                        
                    )
                

    #for indm, metric in enumerate(['ToneGaussianMax']): #enumerate(metrics):
    for indm, metric in enumerate(metrics):
        print(f'----- {metric} -----')

        if indm==0:
            gsThisMetric = gsMetrics[0,1].subgridspec(nRates,1,hspace=0.4, wspace=0.4)
            gs_panel_label(gsMetrics[0,1],subfigure_labels[4])
        else:
            gsThisMetric = gsMetrics[1,indm-1].subgridspec(nRates,1,hspace=0.4, wspace=0.4)
            gs_panel_label(gsMetrics[1,indm-1],subfigure_labels[4+indm])

        print(np.nonzero(selectedCells))
        nCells = np.sum(selectedCells)
        for indmod,mod in enumerate(modRates):
            thisMetricoff = celldb[f'{mod}Hz_off'+metric][selectedCells]
            thisMetricon = celldb[f'{mod}Hz_on'+metric][selectedCells]

            notnans = (~np.isnan(thisMetricon) & ~np.isnan(thisMetricoff))


            thisMetricoff = thisMetricoff[notnans]
            thisMetricon = thisMetricon[notnans]
            
            wstat, pVal = stats.wilcoxon(thisMetricoff, thisMetricon)
            medianoff = np.nanmedian(abs(thisMetricoff))
            meanoff = np.nanmean(abs(thisMetricoff))
            medianon = np.nanmedian(abs(thisMetricon))
            meanon = np.nanmean(abs(thisMetricon))
            print(f'[N={nCells}]  Median {metric}: {mod}Hz off={medianoff:0.4f}, ' +
                f'on={medianon:0.4f}')
            
            print(f'\tMean {metric}: {mod}Hz off={meanoff:0.4f}, ' +
                f'on={meanon:0.4f}  p={pVal:0.4f}')
            print(f'\t on>off: {np.mean(thisMetricon>thisMetricoff):0.1%}'+
                f'\t on<off: {np.mean(thisMetricon<thisMetricoff):0.1%}')
            
            thisAx = plt.subplot(gsThisMetric[indmod])
            maxVal = max(thisMetricoff.max(), thisMetricon.max())
            if indm==99:
                plt.loglog(thisMetricoff, thisMetricon, 'o', mec='0.75', mfc='none')
            else:
                # plt.plot(thisMetricoff, thisMetricon, '.', mec=colorsRasterDark[sessionType][f'{mod}Hz_off'], mfc='none')
                plt.plot(thisMetricoff, thisMetricon, '.', color=colorsRasterDark[sessionType][f'{mod}Hz_off'])
        
            plt.plot(medianoff, medianon, '+', color='k', ms=10, mew=1)
            plt.plot(metricLims[indm], metricLims[indm], 'k--', lw=0.5)
            plt.gca().set_aspect('equal', 'box')
            plt.xlim(metricLims[indm])
            plt.ylim(metricLims[indm])
            if indm==99:
                axTicksLog = np.log2(metricTicks[indm])
                axTickLabels = [f'{int(x/1000)}' for x in metricTicks[indm]]
                plt.xticks(axTicksLog, axTickLabels, fontsize=fontSizeTicks)
                plt.yticks(axTicksLog, axTickLabels, fontsize=fontSizeTicks)
            else:
                plt.xticks(metricTicks[indm], fontsize=fontSizeTicks)
                plt.yticks(metricTicks[indm], fontsize=fontSizeTicks)
            plt.xlabel(f'{metricsLabel[indm]} off ({metricsUnits[indm]})', fontsize=fontSizeLabels)
            plt.ylabel(f'{metricsLabel[indm]} on ({metricsUnits[indm]})', fontsize=fontSizeLabels)
            #plt.gca().tick_params(labelleft=False)
            if indm==99:
                thisAx.set_xscale('log')
                thisAx.set_yscale('log')
            plt.text(0.5, 0.9, f'p = {pVal:0.3f}',
                    transform=thisAx.transAxes, ha='center', fontsize=fontSizeTicks)
            if indm+indmod==0:
                plt.title(f'N = {nCells} cells', fontsize=fontSizeLabels, fontweight='normal')
        # plt.tight_layout()
        #extraplots.boxoff(thisAx)

    if SAVE_FIGURE:
        cellstring = str(cellsToPlot[0])
        for cell in cellsToPlot[1:]:
            cellstring += f'-{cell:03d}'

        extraplots.save_figure(figFilename+cellstring, figFormat, 
                               figSize, outputDir,transparent=False)

    plt.show()

else:
    labelPosX = [0.002, 0.215, 0.43, 0.65, 0.825]   # Horiz position for panel labels
    labelPosY = [0.96, 0.47] 
    

    # -- Raster and PSTH parameters --
    timeRange = [-0.5, 1.0]
    binWidth = 0.010
    timeVec = np.arange(timeRange[0], timeRange[-1], binWidth)
    smoothWinSizePsth = 2 
    lwPsth = 2.5
    downsampleFactorPsth = 1

    cellIDs = np.arange(len(celldb))[selectedCells]
    celldb = celldb[selectedCells]

    # plotCells = cellsToPlot
    # if cellsToPlot:
    nCells = len(celldb)
    cellInds = [list(range(i,i+5)) for i in range(0,nCells,5)]
    
    for pageNum, cellsToPlot in enumerate(cellInds):

        # -- Plot results --
        fig = plt.gcf()
        fig.clf()
        fig.set_facecolor('w')

        # -- Main gridspec --
        gsMain = gridspec.GridSpec(1, 5, width_ratios=[0.2, 0.2, 0.2, 0.2,0.2])
        gsMain.update(left=0.04, right=0.99, top=0.95, bottom=0.1, wspace=0.35, hspace=0.3)

        # -- Show panel labels --
        # for indp, plabel in enumerate(['A','B','C','D','E']):
        #     plt.figtext(labelPosX[indp], labelPosY[0], plabel, fontsize=fontSizePanel, fontweight='bold')



        for indcell, cellInd in enumerate(cellsToPlot):
            if cellInd < nCells:
                gsExample = gsMain[0, indcell].subgridspec(2, 1, hspace=0.35)
                gsRasters = gsExample[0].subgridspec(nRates, 1, hspace=0.1)
                gsTuning = gsExample[1].subgridspec(nRates+1,1, hspace=0.8)

                # axTuning = plt.subplot(gsExample[1])
                #cellInd, dbRow = celldatabase.find_cell(celldb, **cellsToPlot[indcell])
                dbRow = celldb.iloc[cellsToPlot[indcell]]
                oneCell = ephyscore.Cell(dbRow)
                
                reagentLabels = ['Laser OFF', 'Laser ON']
                allFits = []

                ephysData, bdata = oneCell.load(sessionType) 

                stimEachTrial = bdata['currentFreq']
                possibleStim = np.unique(stimEachTrial) 
                
                if 'AMtone' in sessionType:
                    modEachTrial = bdata['currentMod']
                    possibleMod = np.unique(modEachTrial)
                else:
                    modEachTrial = np.zeros(stimEachTrial.shape)
                    possibleMod = np.unique(modEachTrial)


                trialsEachLaser={}
                reagentsToPlot = []

                
                for indr,mod in enumerate(possibleMod):
                    mod = int(mod)
                
                    reagentsToPlot = [f'{mod}Hz_off',f'{mod}Hz_on']
                    
                    trialInds = np.nonzero(modEachTrial==mod)
                    
                    spikeTimes = ephysData['spikeTimes']
                    eventOnsetTimes = ephysData['events']['stimOn'][trialInds]

                    stimEachTrial = bdata['currentFreq'][trialInds]
                    nTrials = len(stimEachTrial)

                    laserEachTrial = bdata['laserTrial'][trialInds]
                    possibleLaser = np.unique(laserEachTrial)
                    
                    # -- onng this before selecting trials by laser/nonLaser --
                    possibleStim = np.unique(stimEachTrial)
                    nStim = len(possibleStim)
                    
                    stimDuration = bdata['stimDur'][-1]

                    # If the ephys data is 1 more than the bdata, delete the last ephys trial.
                    if len(stimEachTrial) == len(eventOnsetTimes)-1:
                        eventOnsetTimes = eventOnsetTimes[:len(stimEachTrial)]
                    assert len(stimEachTrial) == len(eventOnsetTimes), \
                        "Number of trials in behavior and ephys do not match for {oneCell}"

                    (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = \
                        spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

                    # trialsEachCond = behavioranalysis.find_trials_each_type(stimEachTrial, possibleStim)

                    trialsEachCond = behavioranalysis.find_trials_each_combination(stimEachTrial,possibleStim,
                                                                            laserEachTrial, possibleLaser)
                    
                    yticks_major = [possibleStim]*trialsEachCond.shape[2]

                    # -- Estimate evoked firing rate for each stim --
                    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                            indexLimitsEachTrial,
                                                                            timeRange)

                    # -- Plot Raster --
                    axRaster = plt.subplot(gsRasters[indr])
                    possibleStimInKHz = possibleStim/1000
                    rasterLabels = ['']*nStim;
                    rasterLabels[0] = int(possibleStimInKHz[0])
                    rasterLabels[-1] = int(possibleStimInKHz[-1])

                    rasterLabels *= trialsEachCond.shape[2]

                    reagent=f'{mod}Hz_off'
                    
                    colorEachCond = [colorsRasterDark[sessionType][reagent], colorsRasterLight[sessionType][reagent]]*(nStim)
                    (pRasterS,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                                    indexLimitsEachTrial, timeRange,
                                                                    trialsEachCond, labels=rasterLabels,
                                                                    colorEachCond=colorEachCond,
                                                                    rasterized=True)
                    
                    nTrialson = sum(bdata['laserTrial'][trialInds])
                    nTrialsoff = sum(1-bdata['laserTrial'][trialInds])


                    plt.setp(pRasterS, ms=rasterMarkerSize)
                    plt.xlabel('Time (s)', fontsize=fontSizeLabels)
                    plt.ylabel('Freq (kHz)', fontsize=fontSizeLabels)
                    plt.axhline(nTrialsoff,color='r',linestyle='dashed',zorder=-10)

                    plt.yticks([nTrialsoff//2,nTrialsoff+nTrialson//2],
                            ['off','on'],minor=True)
                    ax = plt.gca()
                    ax.tick_params(axis='y',which='minor',left=False, right=True, labelleft=False, labelright=True)
                
                    if eventKey == 'BTR':
                        plt.axvline(TIME_RANGES[dbRow[reagent+'BestTimeRange']][0],color='r',zorder=-10)
                        plt.axvline(TIME_RANGES[dbRow[reagent+'BestTimeRange']][1],color='r',zorder=-10)
                    #axRaster.set_yticklabels(['2']+['']*(nFreq-2)+['40'])
                    if indr==0:
                        plot_stim(plt.ylim(), stimDuration)
                        plt.title(f'Cell #{cellIDs[cellInd]}',loc='left')
                        axRaster.set_xticklabels([])

                    firingRatesOff = dbRow[f'{mod}Hz_off'+'ToneFiringRateEachFreq'+eventKey]
                    firingRatesOn = dbRow[f'{mod}Hz_on'+'ToneFiringRateEachFreq'+eventKey]

                    # plt.sca(axTuning)

                    # maxVal = max(firingRatesOff.max(),firingRatesOn.max())

                    # linfit = stats.linregress(firingRatesOff,firingRatesOn)
                    # xfit = np.linspace(0,maxVal,100)
                    # yfit = linfit.intercept + linfit.slope*xfit

                    # plt.plot(firingRatesOff,firingRatesOn,'.', color=colorsRasterDark[sessionType][f"{mod}Hz_off"],label=f'{mod} Hz')
                    # plt.plot(xfit,yfit,'-',color = colorsRasterDark[sessionType][f"{mod}Hz_off"])
                    # plt.plot(xfit,xfit,'--',color='k')

                    # plt.xlim([0,maxVal])
                    # plt.ylim([0,maxVal])

                    # if eventKey == 'BTR':
                    #     plt.title(dbRow['4Hz_off'+'BestTimeRange'] + ' ' + dbRow['64Hz_off'+'BestTimeRange'])

                    reagentsThisMod = [i for i in reagentsToPlot if str(mod) in i]
                    axTuning = plt.subplot(gsTuning[indr])
                    

                    for reagent in reagentsThisMod:
                        # -- Plot tuning curve --
                        plt.sca(axTuning)
                        firingRates = dbRow[reagent+'ToneFiringRateEachFreq'+eventKey]
                        fitParams = [dbRow[reagent+'ToneGaussianA'+eventKey], dbRow[reagent+'ToneGaussianX0'+eventKey],
                                    dbRow[reagent+'ToneGaussianSigma'+eventKey], dbRow[reagent+'ToneGaussianY0'+eventKey]]
                        # pdots, pfit = extraplots.plot_tuning_curve(possibleStim, firingRates, fitParams)
                        pfit = plt.plot(np.log2(possibleStim), firingRates)
                        pfit[0].set_color(colorsRasterDark[sessionType][reagent])
                        allFits.append(pfit[0])
                        # if eventKey == 'BTR':
                        #     plt.title(dbRow['4Hz_off'+'BestTimeRange'] + ' ' + dbRow['64Hz_off'+'BestTimeRange'])
                        # pdots[0].set_color(colorsRasterDark[sessionType][reagent])
                        extraplots.boxoff(axTuning)
                        xTicks = np.array([2000, 4000, 8000,16000, 32000])
                        axTuning.set_xticks(np.log2(xTicks))
                        axTuning.set_xticklabels((xTicks/1000).astype(int))
                        axTuning.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
                        axTuning.set_ylabel('Firing rate (spk/s)', fontsize=fontSizeLabels)
                        # axTuning.set_title(f'Cell #{cellInd}',loc='left')

                    if metricAnnotation:
                        annoMetricoff = dbRow[f'{mod}Hz_offTone'+metricAnnotation+eventKey]
                        annoMetricon = dbRow[f'{mod}Hz_onTone'+metricAnnotation+eventKey]

                        if indr==0:
                            plt.title(f'{metricAnnotation}\n{mod}Hz: off={annoMetricoff:0.4f}, on={annoMetricon:0.4f}')
                        else:
                            plt.title(f'{mod}Hz: off={annoMetricoff:0.4f}, on={annoMetricon:0.4f}')

                    
                    axTuning.legend(allFits, ['off','on'], 
                            loc='upper left', handlelength=1)
                    
                    spikeShape = dbRow['spikeShape']
                    timeVec = 1000*np.arange(len(spikeShape))/30000
                    axSpikeShape = plt.subplot(gsTuning[nRates])
                    plt.sca(axSpikeShape)
                    plt.plot(timeVec,spikeShape)

                # plt.sca(axTuning)

                # change4hz = dbRow['4Hz_ToneLaserChangeEachFreq'+eventKey]
                # change64hz = dbRow['64Hz_ToneLaserChangeEachFreq'+eventKey]
                # cmap = plt.get_cmap('Purples',len(possibleStim))

                # for indstim, stim in enumerate(possibleStimInKHz):
                #     plt.plot([1,2],[change4hz[indstim],change64hz[indstim]],label=f'{stim} kHz',color=cmap(indstim))

                # axTuning.legend(loc='upper left', handlelength=1)

        if SAVE_FIGURE:
            cellstring = str(cellIDs[cellsToPlot[0]])
            for cell in cellsToPlot[1:]:
                if cell < nCells:
                    cellstring += f'-{cellIDs[cell]:03d}'

            outputDirNew = os.path.join(outputDir,'Just_Curves')
            if not os.path.exists(outputDirNew):
                os.mkdir(outputDirNew)
            extraplots.save_figure(figFilename+'_Just_Curves'+cellstring, 
                                   figFormat, figSize, outputDirNew,transparent=False)
            



if 1 and ('AMtone' in sessionType):
    plt.figure()
    
    thisMetricoff = celldb[selectedCells]['4Hz_ToneLaserModulation'+eventKey]
    thisMetricon = celldb[selectedCells]['64Hz_ToneLaserModulation'+eventKey]

    notnans = (~np.isnan(thisMetricon) & ~np.isnan(thisMetricoff))

    thisMetricoff = thisMetricoff[notnans]
    thisMetricon = thisMetricon[notnans]
    wstat,pVal = stats.wilcoxon(thisMetricoff,thisMetricon)
    
    print(f'wstat={wstat}, p={pVal:f}')
    
    for indcell,dbRow in celldb[selectedCells].iterrows():
        plt.plot([1,2],[dbRow['4Hz_ToneLaserModulation'+eventKey],dbRow['64Hz_ToneLaserModulation'+eventKey]],lw=0.4)
    
    violas = plt.violinplot([thisMetricoff,thisMetricon],
                   showmeans=True,showextrema=True)
    
    for key in ['cmeans', 'cmaxes', 'cmins', 'cbars']:
        violas[key].set_color(figparams.colors[sessionType]['pre'])

    for indv,body in enumerate(violas['bodies']):
        body.set_facecolor(colorsRasterDark[sessionType][f'{modRates[indv]}Hz_off'])
        body.set_edgecolor(colorsRasterDark[sessionType][f'{modRates[indv]}Hz_off'])


    
    plt.xticks([1,2],['4 Hz','64 Hz'])
    plt.ylim([-1,1])
    plt.title(f'{subject} Laser Modulation using {metricAnnotation}\n'+
              f'wstat={wstat}, p={pVal:f}\n64hz > 4Hz: {np.mean(thisMetricon>thisMetricoff):0.1%}'+
                f'\t 64Hz < 4Hz: {np.mean(thisMetricon<thisMetricoff):0.1%}')
    # 
    extraplots.save_figure(figFilename+f'_LaserModulation_{metricAnnotation}', 
                                   figFormat, [4,5], outputDir,transparent=False)
    
    plt.show()