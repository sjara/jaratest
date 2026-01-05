"""
This script plots changes in freq tuning from off to on.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import PercentFormatter
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

subjEachImplant = studyparams.SUBJECTS_EACH_SHAM
sessionDatesEachSubj = studyparams.SHAM_DATES_EACH_SUBJECT
probeDepthEachSubj = studyparams.PDEPTH_EACH_SUBJECT

sessionType = sys.argv[1]
eventKey = sys.argv[2]
loadDB = sys.argv[3] if len(sys.argv)==4 else ''


# subject='poni001'
# sessionDate='2025-08-19'
# probeDepth=2360
# eventKey='Evoked'
    


SAVE_FIGURE = 1
SAVE=1 
studyName = 'hemisym'
BTRmetric = studyparams.TIME_KEY_METRIC
if studyparams.BLNORM:
    outputDir = os.path.join(settings.FIGURES_DATA_PATH,studyName,'norm_comparisons')
else:
    outputDir = os.path.join(settings.FIGURES_DATA_PATH,studyName,'comparisons')
dbPath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
figFilename = f'plots_{eventKey}_compare_{sessionType}' # Do not include extension
figFormat = 'pdf' #'svg'
figSize = figparams.FIGSIZE[sessionType] # In inches
modRates = studyparams.SESSION_MODRATES[sessionType]
nRates = len(modRates)

# plotAllCells=True
plotAllCells=False

# metricAnnotation = 'FanoFactor'
metricAnnotation = 'DiscrimRatio'
# metricAnnotation = 'SelectivityKstat'


TIME_RANGES = studyparams.TIME_RANGES_AM if 'AM' in sessionType else studyparams.TIME_RANGES_FREQ

trialSubset = ''


fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.002, 0.215, 0.43, 0.65, 0.825]   # Horiz position for panel labels
labelPosY = [0.96, 0.47]    # Vert position for panel labels

# -- Assigned colors (defined in figparams) --
colorsRasterDark = figparams.colors
colorsRasterLight = figparams.colorsLight
pColor = '0.5'

rasterMarkerSize = 0.8

def plot_stim(yLims, stimDuration, stimLineWidth=6, stimColor=figparams.colorStim,yposOffset=0,xposOffset=0):
    yPos = (1.02+stimDuration*0.04*yposOffset)*yLims[-1] + 0.075*(yLims[-1]-yLims[0])*2*stimDuration
    pstim = plt.plot([xposOffset, stimDuration], 2*[yPos], lw=stimLineWidth, color=stimColor,
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
                    fontsize=fontSize, fontweight='bold')

# -- Main gridspec --
if 'Freq' in sessionType:
    gsMain = gridspec.GridSpec(2, 4, width_ratios=[0.2, 0.2, 0.2, 0.2])
    gsMain.update(left=0.06, right=0.98, top=0.95, bottom=0.1, wspace=0.25, hspace=0.6)
else:
    gsMain = gridspec.GridSpec(2, 3, width_ratios=[0.2, 0.2, 0.4])
    gsMain.update(left=0.06, right=0.98, top=0.95, bottom=0.1, wspace=0.25, hspace=0.3)

celldbEachImplant = {}
selectedCellsEachImplant = {}
metricDiffEachImplant = {}

if 'opto' in sessionType:
    cellsToPlotAll = []
else:
    cellsToPlotAll = [237,241,207,5]

for indimp,implant in enumerate(subjEachImplant):
    if loadDB:
        dbFilename = os.path.join(dbPath,f'celldb_{implant}_{sessionType}_freqtuning.h5')
        if studyparams.BLNORM:
            dbFilename = dbFilename.replace('.h5','_norm.h5')
        celldbThisImplant = celldatabase.load_hdf(dbFilename)

    else:
        # -- Load data --
        celldbEachSubj = []
        
        for indsub,subject in enumerate(subjEachImplant[implant]):
            # dbFilenameThisSubject = os.path.join(dbPath,f'celldb_{subject}_{sessionType}.h5')
            dbFilenameThisSubject = os.path.join(dbPath,f'celldb_{subject}_sham_freqtuning.h5')
            if studyparams.BLNORM:
                dbFilenameThisSubject = dbFilenameThisSubject.replace('.h5','_norm.h5')
            # sessionDate = sessionDatesEachSubj[subject]
            probeDepth = probeDepthEachSubj[subject]
            celldbThisSubj = celldatabase.load_hdf(dbFilenameThisSubject)
            celldbThisSubj = celldbThisSubj[(celldbThisSubj['date'].apply(lambda x: x in sessionDatesEachSubj[subject])) \
                                & (celldbThisSubj['pdepth'].apply(lambda x: x in probeDepthEachSubj[subject]))\
                                    & (celldbThisSubj['sessionType'].apply(lambda x: sessionType in x))]

            celldbEachSubj.append(celldbThisSubj)

        celldbThisImplant = pd.concat(celldbEachSubj)
        nCells = len(celldbThisImplant)

        celldbThisImplant['cellDepth'] = studyutils.get_cell_depths(celldbThisImplant)
        

        for indr,reagent in enumerate(studyparams.REAGENTS[sessionType]):
            for tKey in studyparams.EVENT_KEYS:
                celldbThisImplant[reagent+'ToneDiscrimRatio'+tKey] = celldbThisImplant[reagent+'ToneDiscrimBestFreq'+tKey]/celldbThisImplant[reagent+'ToneMeanDiscrim'+tKey]
                # smoothedFiringRates = []
                # smoothedFanoFactors = np.empty(len(celldbThisImplant))

                octaveFRs = []
                fits = []
                    
                for indcell,(indrow,dbRow) in enumerate(celldbThisImplant.iterrows()):
                    # firingRates = dbRow[reagent+'ToneFiringRateEachFreq'+tKey]
                    # smoothedFiringRates.append(studyutils.moving_average(firingRates))
                    # smoothedFanoFactors[indcell] = (np.std(smoothedFiringRates[indcell])**2)/np.mean(smoothedFiringRates[indcell])

                    bestFreqInd = np.argmax(dbRow[reagent+'ToneFiringRateEachFreq'+tKey])
                    if bestFreqInd < studyparams.N_FREQ//2:
                        octaveFRs.append(dbRow[reagent+'ToneFiringRateEachFreq'+tKey][bestFreqInd:studyparams.N_FREQ//2+bestFreqInd])

                    else:
                        octaveFRs.append(dbRow[reagent+'ToneFiringRateEachFreq'+tKey][bestFreqInd - studyparams.N_FREQ//2+1: bestFreqInd+1][::-1])
                


                # celldbThisImplant[reagent+'ToneFiringRateEachFreqSmoothed'+tKey] = smoothedFiringRates
                # celldbThisImplant[reagent+'ToneFanoFactorSmoothed'+tKey] = smoothedFanoFactors

                celldbThisImplant[reagent+'ToneFiringRateEachOctave'+tKey] = octaveFRs
                

    

    # -- Find best time range for each cell --
    if eventKey == 'BTR':
        # print(f'Finding best time ranges based on {BTRmetric}')
        # bestKeys = studyutils.find_best_time_keys(celldbThisImplant,BTRmetric,['Evoked','Delayed'])
        bestKeys = studyutils.find_best_time_keys(celldbThisImplant,
                                                BTRmetric,['Onset','Sustained','Interim','Evoked'],
                                                sessionType='optoShamAMtone')
        
        measurements = studyparams.METRICS[6:] 
        for indr,reagent in enumerate(studyparams.REAGENTS['optoShamAMtone']):
            celldbThisImplant[reagent+'BestTimeRange']=bestKeys[indr]
            for metric in studyparams.METRICS[6:]:
                BTRs = []
                for indc,dbRow in celldbThisImplant.iterrows():
                    tKey = dbRow[reagent+'BestTimeRange']
                    BTRs.append(dbRow[reagent+'Tone'+metric+tKey])
                
                celldbThisImplant[reagent+'Tone'+metric+'BTR'] = BTRs

        # bestKeys = studyutils.find_best_time_keys(celldbThisImplant,
        #                                         BTRmetric,['Onset','Sustained','Interim','Evoked'],
        #                                         sessionType='optoTuningFreq')
        
        # measurements = studyparams.METRICS[6:] 
        # for indr,reagent in enumerate(studyparams.REAGENTS['optoTuningFreq']):
        #     celldbThisImplant[reagent+'BestTimeRange']=bestKeys[indr]
        #     for metric in studyparams.METRICS[6:]:
        #         BTRs = []
        #         for indc,dbRow in celldbThisImplant.iterrows():
        #             tKey = dbRow[reagent+'BestTimeRange']
        #             BTRs.append(dbRow[reagent+'Tone'+metric+tKey])
                
        #         celldbThisImplant[reagent+'Tone'+metric+'BTR'] = BTRs

    
    

            

    # -- Process data --
    maxChangeFactor = studyparams.MAX_CHANGE_FACTOR

    modRates = studyparams.SESSION_MODRATES[sessionType]


    selective = studyutils.find_freq_selective(celldbThisImplant, minR2=studyparams.MIN_PVAL,sessionType=sessionType)
    goodD = studyutils.find_good_dprime(celldbThisImplant, eventKey,minDisc=studyparams.MIN_DPRIME,sessionType=sessionType)
    goodFit = studyutils.find_good_gaussian_fit(celldbThisImplant, eventKey,minR2=studyparams.MIN_R_SQUARED,sessionType=sessionType)
    anyFitall = ~np.isnan(celldbThisImplant[f'{modRates[0]}Hz_offToneGaussianA'+eventKey])
    for mod in modRates[1:]:
        anyFitall &= ~np.isnan(celldbThisImplant[f'{mod}Hz_offToneGaussianA'+eventKey])
    highFiring = np.ones(len(celldbThisImplant),dtype=bool)

    RScell = studyutils.find_RS_cells(celldbThisImplant)


    reagents = studyparams.REAGENTS[sessionType] #if 'AMtone' in sessionType else studyparams.REAGENTS[sessionType]
    
    for indr, reagent in enumerate(reagents):
        #celldbThisImplant[reagent+'ToneGaussianMax'+eventKey] = ( celldbThisImplant[reagent+'ToneGaussianA'+eventKey] +
        #                                      celldbThisImplant[reagent+'ToneGaussianY0'+eventKey] )
        negResponseThisReagent = celldbThisImplant[reagent+'ToneGaussianA'+eventKey]<0
        thisToneGaussianMax = ( celldbThisImplant[reagent+'ToneGaussianA'+eventKey] +
                                celldbThisImplant[reagent+'ToneGaussianY0'+eventKey] )
        thisToneGaussianMax[negResponseThisReagent] = celldbThisImplant[reagent+'ToneGaussianY0'+eventKey]
        celldbThisImplant[reagent+'ToneGaussianMax'+eventKey] = thisToneGaussianMax
        celldbThisImplant[reagent+'ToneGaussianBandwidth'+eventKey] = \
            extraplots.gaussian_full_width_half_max(celldbThisImplant[reagent+'ToneGaussianSigma'+eventKey])
        baselineFiringRate = celldbThisImplant[reagent+'ToneBaselineFiringRate']
        celldbThisImplant[reagent+'ToneGaussianMaxChange'+eventKey] = np.abs(thisToneGaussianMax-baselineFiringRate)
        highFiring &= (celldbThisImplant[reagent+'ToneFiringRateBestFreq'+eventKey] >= studyparams.FR_THRESHOLD) | (baselineFiringRate >= studyparams.FR_THRESHOLD)

        celldbThisImplant[reagent+'ToneFanoSelectivityComposite'+eventKey] = celldbThisImplant[reagent+'ToneSelectivityKstat'+eventKey]*celldbThisImplant[reagent+'ToneFanoFactor'+eventKey]
        celldbThisImplant[reagent+'ToneDiscrimRatio'+eventKey] = celldbThisImplant[reagent+'ToneDiscrimBestFreq'+eventKey]/celldbThisImplant[reagent+'ToneMeanDiscrim'+eventKey]

        celldbThisImplant[reagent+'ToneFiringRateRatio'+eventKey] = celldbThisImplant[reagent+'ToneFiringRateBestFreq'+eventKey]/celldbThisImplant[reagent+'ToneAvgEvokedFiringRate'+eventKey]

        

    posResponse = np.zeros(len(celldbThisImplant))
    posMod = np.zeros(len(celldbThisImplant),dtype=bool)
    # posMod = np.ones(len(celldbThisImplant),dtype=bool)

    lasMod = np.ones(len(celldbThisImplant),dtype=bool)

    for mod in studyparams.SESSION_MODRATES[sessionType]:
        thisMetricoff = celldbThisImplant[f'{mod}Hz_offTone'+metricAnnotation+eventKey]
        thisMetricon = celldbThisImplant[f'{mod}Hz_onTone'+metricAnnotation+eventKey]
        celldbThisImplant[f'{mod}Hz_ToneLaserModulation'+eventKey] = studyutils.modulation_index(thisMetricoff,thisMetricon)

        # posResponse &= (celldbThisImplant[f'{mod}Hz_offToneGaussianA'+eventKey]>0)
        # posMod |= (np.abs(celldbThisImplant[f'{mod}Hz_ToneLaserModulation'+eventKey]) >= studyparams.MIN_MODULATION)
        posMod |= (abs(celldbThisImplant[f'{mod}Hz_ToneLaserModulation'+eventKey]) >= studyparams.MIN_MODULATION)
        
        
        # lasMod &= (celldbThisImplant[f'{mod}Hz_onToneLaserPval'] <= studyparams.MIN_PVAL) 

        lasMod &= ( (celldbThisImplant[f'{mod}Hz_onToneLaserPval'] <= studyparams.MIN_PVAL) & \
            (((celldbThisImplant[f'{mod}Hz_onToneLaserFiringRate']/celldbThisImplant[f'{mod}Hz_onToneBaselineFiringRate'] > studyparams.MAX_CHANGE_FACTOR/3) | \
                 (celldbThisImplant[f'{mod}Hz_onToneBaselineFiringRate']/celldbThisImplant[f'{mod}Hz_onToneLaserFiringRate']) > studyparams.MAX_CHANGE_FACTOR/3)) )

        if 1:
            fitLins = []
            for indcell,dbRow in celldbThisImplant.iterrows():
                # firingRatesOff = dbRow[f'{mod}Hz_offToneFiringRateEachFreq{eventKey}']/dbRow[f'{mod}Hz_offToneBaselineFiringRate'] 
                # firingRatesOn = dbRow[f'{mod}Hz_onToneFiringRateEachFreq{eventKey}']/dbRow[f'{mod}Hz_onToneBaselineFiringRate'] 

                firingRatesOff = dbRow[f'{mod}Hz_offToneFiringRateEachFreq{eventKey}']
                firingRatesOn = dbRow[f'{mod}Hz_onToneFiringRateEachFreq{eventKey}']
                if sum(firingRatesOff)==0:
                    firingRatesOff[0] += 0.0001

                linfit = stats.linregress(firingRatesOff,firingRatesOn)
                fitLins.append(linfit)
                
            celldbThisImplant[f'{mod}Hz_ToneNormFitSlope{eventKey}'] = np.array([i.slope for i in fitLins])
            celldbThisImplant[f'{mod}Hz_ToneNormFitIntercept{eventKey}'] = np.array([i.intercept for i in fitLins])
            celldbThisImplant[f'{mod}Hz_ToneNormFitRval{eventKey}'] = np.array([i.rvalue for i in fitLins])
            celldbThisImplant[f'{mod}Hz_ToneNormFitPval{eventKey}'] = np.array([i.pvalue for i in fitLins])

    goodDepth = (celldbThisImplant['cellDepth'] <= 1600)

    responsive = studyutils.find_tone_responsive_cells(celldbThisImplant, eventKey, frThreshold=studyparams.FR_THRESHOLD,allreagents=True,sessionType=sessionType)


    steadyParams = ['BaselineFiringRate','LaserFiringRate'] 
    steady = studyutils.find_steady_cells(celldbThisImplant, steadyParams, maxChangeFactor,sessionType=sessionType)

    print(f'goodD\t\t{sum(goodD)} cells')
    print(f'lasMod\t\t{sum(lasMod)} cells')
    print(f'goodDepth\t{sum(goodDepth)} cells')
    print(f'posMod\t\t{sum(posMod)} cells')
    print(f'selective\t{sum(selective)} cells')
    print(f'responsive\t{sum(responsive)} cells')
    print(f'goodFit\t\t{sum(goodFit)} cells')
    print(f'steady\t\t{sum(steady)} cells')
    print(f'highFiring\t{sum(highFiring)} cells')
    # print(f'RScell\t\t{sum(RScell)} cells')


    selectedCells =  responsive & highFiring & steady  & selective 

    if 0:
        selectedCells &= posMod

    if len(cellsToPlotAll)<4:
        if 'AMtone' in sessionType:
            cellsToPlot = sorted(np.nonzero(selectedCells)[0],
                                key=lambda x: -1*abs(np.diff([celldbThisImplant.iloc[x][f'{mod}Hz_ToneLaserModulation'+eventKey] for mod in modRates])))[-3:-1]
        else:
            cellsToPlot = sorted(np.nonzero(selectedCells)[0],
                                key=lambda x: celldbThisImplant.iloc[x][f'0Hz_ToneLaserModulation'+eventKey])[-3:-1]
        cellsToPlotAll += cellsToPlot
    else:
        cellsToPlot = cellsToPlotAll[2*indimp:2*indimp+2]

    selectedCellsEachImplant[implant] = selectedCells
    celldbEachImplant[implant] = celldbThisImplant
    
    # -- Save the updated celldbThisImplant --
    if SAVE:
        dbFilename = os.path.join(dbPath,f'celldb_{implant}_{sessionType}_freqtuning.h5')
        if studyparams.BLNORM:
            dbFilename = dbFilename.replace('.h5','_norm.h5')
        celldatabase.save_hdf(celldbThisImplant, dbFilename)
    '''
    metrics = ['ToneGaussianX0', 'ToneGaussianBandwidth', 'ToneGaussianMax']
    metricsLabel = ['BF', 'Bandwidth', 'Max resp']
    metricsUnits = ['kHz', 'oct', 'spk/s']
    metricLims = [[np.log2(2000), np.log2(40000)], [0, 10], [0, 120]]
    metricTicks = [[2000, 8000, 32000], [0, 5, 10], [0, 60, 120]]
    '''

    # -- Plot examples --
    metrics = ['ToneFanoFactor'+eventKey, 'ToneDiscrimRatio'+eventKey,  'ToneSelectivityKstat'+eventKey]
    # metricsLabel = ['BF', 'Width', 'Max Δ']
    metricsLabel = ['FF', "d'",  'H-stat' ]
    #metricsLabel = ['BF', 'Bandwidth', 'Resp at BF']
    # metricsUnits = ['kHz', 'norm.', 'spk/s']
    # metricLims = [[np.log2(2000), np.log2(40000)], [0, 6], [0, 10]]
    # metricTicks = [[2000, 8000, 32000], [0, 5, 10], [0, 25, 50]]
    metricsUnits = ['AU', 'AU', 'oct']
    metricLims = [[0, 10],   [0, 300]]
    metricTicks = [[0,5,10],   [0, 150, 300]]


    # metrics = ['ToneSelectivityKstat'+eventKey, 'ToneFanoFactor'+eventKey,'ToneGaussianBandwidth'+eventKey]
    # metricsLabel = ['H-stat',"FF",'Bandwidth' ]
    # metricsUnits = ['AU', 'AU', 'oct']
    # metricLims = [[0, 300], [0, 10], [0, 10]]
    # metricTicks = [[0, 150, 300],[0, 5, 10], [0,5,10]]


    # -- Plot results --
    fig = plt.gcf()
    # fig.clf()
    fig.set_facecolor('w')

    
    # subfigure_labels = ['A','B','C','D','E','F','G']
    subfigure_labels = [f'A$_{indimp+1}$',f'B$_{indimp+1}$',f'C$_{indimp+1}$',f'D$_{indimp+1}$',f'E$_{indimp+1}$']
    offset=0
    if 'Freq' in sessionType:
        gs_panel_label(gsMain[indimp,0],subfigure_labels[0])
        offset=1

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
        gsExample = gsMain[indimp, indcell+offset].subgridspec(1, 1, hspace=0.4)
        gs_panel_label(gsExample[0],subfigure_labels[indcell+offset])

        gsRasters = gsExample[0].subgridspec(nRates, 1, hspace=0.1)
        # gsTuning = gsExample[1].subgridspec(nRates,1, hspace=0.4)
        # axTuning = plt.subplot(gsExample[1])
        #cellInd, dbRow = celldatabase.find_cell(celldbThisImplant, **cellsToPlot[indcell])
        dbRow = celldbThisImplant.iloc[cellsToPlot[indcell]]
        oneCell = ephyscore.Cell(dbRow)
        
        reagentLabels = ['Laser OFF', 'Laser ON']

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
            
            rasterLabels[-1] = int(possibleStimInKHz[-1])

            rasterLabels *= trialsEachCond.shape[2]

            rasterLabels[0] = int(possibleStimInKHz[0])
            reagent=f'{mod}Hz_off'
            
            colorEachCond = [colorsRasterDark[sessionType][reagent], colorsRasterLight[sessionType][reagent]]*(nStim)
            (pRasterS,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial, timeRange,
                                                            np.reshape(trialsEachCond,(trialsEachCond.shape[0],np.prod(trialsEachCond.shape[1:])),'F'), 
                                                            labels=rasterLabels,
                                                            colorEachCond=colorEachCond,
                                                            rasterized=False)
            
            nTrialson = sum(bdata['laserTrial'][trialInds])
            nTrialsoff = sum(1-bdata['laserTrial'][trialInds])


            plt.setp(pRasterS, ms=rasterMarkerSize)
            if indr==len(possibleMod)-1:
                plt.xlabel('Time (s)', fontsize=fontSizeLabels)
            plt.ylabel('Freq (kHz)', fontsize=fontSizeLabels)
            plt.axhline(nTrialsoff,color='r',linestyle='dashed',zorder=-10)

            plt.yticks([nTrialsoff//2,nTrialsoff+nTrialson//2],
                        ['off','on'],minor=True)
            ax = plt.gca()
            ax.tick_params(axis='y',which='minor',left=False, right=True, labelleft=False, labelright=True)
        
            if eventKey == 'BTR':
                plt.fill_between(TIME_RANGES[dbRow[reagent+'BestTimeRange']],
                                 *plt.ylim(),color=figparams.colorLaser,alpha=0.6)
                # plt.axvline(TIME_RANGES[dbRow[reagent+'BestTimeRange']][1],color='r',zorder=-10)
            else:
                plt.fill_between(TIME_RANGES[eventKey], *plt.ylim(), 
                                 color=figparams.colorLaser, alpha=0.4)
            #axRaster.set_yticklabels(['2']+['']*(nFreq-2)+['40'])
            if indr==0:
                plot_stim(plt.ylim(), stimDuration)
                plot_stim(plt.ylim(),stimDuration,yposOffset=2,xposOffset=-0.25,stimColor=colorsRasterDark[sessionType]['off'])
                # plt.title(f'Cell #{cellInd}',loc='left')
            
                if nRates>1:
                    axRaster.set_xticklabels([])

    # -- Plot metrics summary --        
    nCells = sum(selectedCells)
    if 'Freq' in sessionType:
        gsMetrics = gsMain[indimp, 2+offset].subgridspec(1, 2, hspace=0.4)
    
    else:
        gsMetrics = gsMain[indimp, 2+offset].subgridspec(1, 2, hspace=0.4)
    
    indmOffset=0
    if 1 and 'Freq' in sessionType:
        gs_panel_label(gsMetrics[0,0],subfigure_labels[2],hpad=0.1)
        indmOffset = 1
        octaves = np.round(np.array(list(1-possibleStim[::-1]/2000)+list(abs(1-possibleStim[1:]/2000))),2)
        octRange = (abs(octaves) < 2.3)
        nOcts = len(octaves)

        gsFirstMetric = gsMetrics[0,0].subgridspec(nRates,1,hspace=0.4)

        for indr,mod in enumerate(modRates):
            thisAx = plt.subplot(gsFirstMetric[indr])
            thisMetricoff = np.array([*celldbThisImplant[f'{mod}Hz_offToneNormResponseEachOctave'+eventKey][selectedCells]])
            thisMetricon = np.array([*celldbThisImplant[f'{mod}Hz_onToneNormResponseEachOctave'+eventKey][selectedCells]])

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
                    plt.ylabel('Normalized Response',fontsize=fontSizeLabels, fontweight='normal')
                    plt.xlabel('Octaves From Peak Response',fontsize=fontSizeLabels, fontweight='normal')
                    plt.ylim([0,1.1])
                    plt.yticks([0,0.25,0.5,0.75,1])
                    plt.xticks(np.arange(-2,3))
                    # plt.title(f'Mean Normalized Tone\nResponses {mod}Hz')
                    plt.legend(['off','on'],loc='upper right')
                    # plt.fill_between(octaves[octRange],
                    #                  meanon[octRange] + stdon[octRange],
                    #                  meanon[octRange] - stdon[octRange],
                    #                  color=colorsRasterDark[sessionType][f'{mod}Hz_on'],
                    #                  alpha=0.5)

                    plt.gca().set_aspect(aspect=4/1.1, adjustable='box')
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
    for indm, metric in enumerate(metrics[:1]):
        print(f'----- {metric} -----')

        if indm==0:
            gsThisMetric = gsMetrics[0+indmOffset].subgridspec(nRates,1,hspace=0.1)
            gs_panel_label(gsMetrics[0+indmOffset],subfigure_labels[2+offset+indmOffset],hpad=0.1)
        else:
            gsThisMetric = gsMetrics[1,indm-1].subgridspec(nRates,1,hspace=0.1)
            gs_panel_label(gsMetrics[1,indm-1],subfigure_labels[4+indm],hpad=0.1)

        print(np.nonzero(selectedCells))
        nCells = np.sum(selectedCells)
        for indmod,mod in enumerate(modRates):
            thisMetricoff = celldbThisImplant[f'{mod}Hz_off'+metric][selectedCells]
            thisMetricon = celldbThisImplant[f'{mod}Hz_on'+metric][selectedCells]

            notnans = (~np.isnan(thisMetricon) & ~np.isnan(thisMetricoff))


            thisMetricoff = thisMetricoff[notnans]
            thisMetricon = thisMetricon[notnans]
            
            wstat, pVal = stats.wilcoxon(thisMetricoff, thisMetricon,alternative='greater')
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
                plt.plot(thisMetricoff, thisMetricon, 'o', mec=colorsRasterDark[sessionType][f'{mod}Hz_off'], mfc='none',alpha=0.75)
                # plt.plot(thisMetricoff, thisMetricon, '.', color=colorsRasterDark[sessionType][f'{mod}Hz_off'])
        
            plt.plot(meanoff, meanon, '+', color='k', ms=10, mew=2)
            plt.plot(metricLims[indm], metricLims[indm], 'k--', lw=1)
            
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

            if indmod==len(modRates)-1:
                plt.xlabel(f'{metricsLabel[indm]} off ({metricsUnits[indm]})', fontsize=fontSizeLabels)
            else:
                plt.xticks([])
            plt.ylabel(f'{metricsLabel[indm]} on ({metricsUnits[indm]})', fontsize=fontSizeLabels)
            #plt.gca().tick_params(labelleft=False)

            plt.gca().set_aspect('equal', 'box')

            if indm==99:
                thisAx.set_xscale('log')
                thisAx.set_yscale('log')
            if pVal >= 0.001:
                plt.text(0.5, 0.9, f'p = {pVal:0.3f}',
                            transform=thisAx.transAxes, ha='center', fontsize=fontSizeTicks)
            else:
                plt.text(0.5, 0.9, f'p < 0.001',
                            transform=thisAx.transAxes, ha='center', fontsize=fontSizeTicks)
            if indm+indmod==0:
                plt.title(f'N = {nCells} cells', fontsize=fontSizeLabels, fontweight='normal')
        # plt.tight_layout()
        #extraplots.boxoff(thisAx)

    if 'AMtone' in sessionType:
        gsModulation = gsMetrics[1].subgridspec(2, 1, hspace=0.3, height_ratios=[0.4,0.2])
        gs_panel_label(gsMetrics[1],subfigure_labels[3+offset])
        thisAx = plt.subplot(gsModulation[0])
        plt.sca(thisAx)

        metric = 'ToneLaserModulation'+eventKey

        print(f'----- {metric} -----')

        thisMetricoff = celldbThisImplant[selectedCells]['4Hz_ToneLaserModulation'+eventKey]
        thisMetricon = celldbThisImplant[selectedCells]['64Hz_ToneLaserModulation'+eventKey]

        notnans = (~np.isnan(thisMetricon) & ~np.isnan(thisMetricoff))

        thisMetricoff = thisMetricoff[notnans]
        thisMetricon = thisMetricon[notnans]
        medianoff = np.nanmedian(thisMetricoff)
        medianon = np.nanmedian(thisMetricon)
        meanoff = np.nanmean(thisMetricoff)
        meanon = np.nanmean(thisMetricon)

        wstat,pVal = stats.wilcoxon(thisMetricoff,thisMetricon)

        print(f'wstat={wstat}, p={pVal:f}')

        for indcell,dbRow in celldbThisImplant[selectedCells].iterrows():
            plt.plot([1,2],[dbRow['4Hz_ToneLaserModulation'+eventKey],
                            dbRow['64Hz_ToneLaserModulation'+eventKey]],lw=0.4, alpha=0.2)
        plt.plot([1,2],[meanoff,meanon],color='r',lw=1)
        # plt.boxplot([thisMetricoff,thisMetricon],showmeans=True)
        violas = plt.violinplot([thisMetricoff,thisMetricon],
                    showmedians=True,showextrema=True)

        for key in ['cmedians', 'cmaxes', 'cmins', 'cbars']:
            violas[key].set_color(figparams.colors[sessionType]['pre'])

        for indv,body in enumerate(violas['bodies']):
            body.set_facecolor(colorsRasterDark[sessionType][f'{modRates[indv]}Hz_off'])
            body.set_edgecolor(colorsRasterDark[sessionType][f'{modRates[indv]}Hz_off'])

        plt.gca().set_aspect('equal', 'box')

        plt.xticks([1,2],['4 Hz','64 Hz'],fontsize=fontSizeLabels, fontweight='normal')
        plt.ylim([-1,1])
        # plt.title(f'{implant[0]} -> {implant[1]} Laser Modulation',
        #                 fontsize=fontSizeLabels, fontweight='normal')
        if pVal >= 0.001:
            plt.text(0.5, 0.9, f'p = {pVal:0.3f}',
                        transform=thisAx.transAxes, ha='center', fontsize=fontSizeTicks)
        else:
            plt.text(0.5, 0.9, f'p < 0.001',
                        transform=thisAx.transAxes, ha='center', fontsize=fontSizeTicks)
        plt.ylabel('Modulation Index (AU)',fontsize=fontSizeLabels, fontweight='normal')
        # plt.xlabel('AM Rate',fontsize=fontSizeLabels, fontweight='normal')

        metricDiff = thisMetricon-thisMetricoff
        metricDiffEachImplant[implant] = metricDiff

        thisAx = plt.subplot(gsModulation[1])
        plt.hist(metricDiff[metricDiff<=0], bins=np.arange(-1,1,0.05),
                 color = colorsRasterDark[sessionType]['4Hz_off'],
                 weights=np.ones(len(metricDiff[metricDiff<=0]))/len(metricDiff),
                 label = f'64Hz < 4Hz')
        
        plt.hist(metricDiff[metricDiff>0], bins=np.arange(-1,1,0.05),
                 color = colorsRasterDark[sessionType]['64Hz_off'],
                 weights=np.ones(len(metricDiff[metricDiff>0]))/len(metricDiff),
                 label= f'64hz ≥ 4Hz')
        
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        plt.legend(handlelength=1)

        

        

        print(f'[N={nCells}]  Median {metric}: 4Hz={medianoff:0.4f}, ' +
                f'64Hz={medianon:0.4f}')
            
        print(f'\tMean {metric}: 4Hz={meanoff:0.4f}, ' +
            f'64Hz={meanon:0.4f}  p={pVal:0.4f}')
        print(f'\t 64Hz>4Hz: {np.mean(thisMetricon>thisMetricoff):0.1%}'+
            f'\t 64Hz<4Hz: {np.mean(thisMetricon<thisMetricoff):0.1%}')
        

        print(f'Median Δ{metric}: {np.nanmedian(thisMetricon - thisMetricoff):0.4f}')
        print(f'Mean Δ{metric}: {np.nanmean(thisMetricon - thisMetricoff):0.4f}')
        plt.xlim([-1,1])
        # plt.ylim([0,15])
        plt.xlabel('Change in Modulation Index (AU)',fontsize=fontSizeLabels, fontweight='normal')
        plt.ylabel('# Cells',fontsize=fontSizeLabels, fontweight='normal')


        plt.gca().set_aspect('auto', 'box')

if SAVE_FIGURE:
    cellstring = str(cellsToPlotAll[0])
    for cell in cellsToPlotAll[1:]:
        cellstring += f'-{cell:03d}'

    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
        
    extraplots.save_figure(figFilename+cellstring, figFormat, 
                            figSize, outputDir,transparent=False)

plt.show()

if plotAllCells:
    for implant in celldbEachImplant:
        celldb = celldbEachImplant[implant]
        selectedCells = selectedCellsEachImplant[implant]

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
        # cellInds = [list(range(i,i+5)) for i in range(0,nCells,5)]

        sortedInds = sorted(list(range(nCells)),
                            key = lambda x: -1*(np.sum([celldb.iloc[x][f'{mod}Hz_ToneLaserModulation{eventKey}'] for mod in modRates])))
        
        cellInds = [list(sortedInds[i:i+5]) for i in range(0,nCells,5)]
        
        for pageNum, cellsToPlot in enumerate(cellInds):

            # -- Plot results --
            fig = plt.gcf()
            fig.clf()
            fig.set_facecolor('w')

            # -- Main gridspec --
            gsMain = gridspec.GridSpec(3, 5, height_ratios=[0.4,0.2,0.2],
                                       width_ratios=[0.2, 0.2, 0.2, 0.2, 0.2])
            gsMain.update(left=0.04, right=0.99, top=0.95, bottom=0.1, wspace=0.35, hspace=0.3)

            # -- Show panel labels --
            # for indp, plabel in enumerate(['A','B','C','D','E']):
            #     plt.figtext(labelPosX[indp], labelPosY[0], plabel, fontsize=fontSizePanel, fontweight='bold')



            for indcell, cellInd in enumerate(cellsToPlot):
                if cellInd < nCells:
                    # gsExample = gsMain[0, indcell].subgridspec(3, 1,hspace=0.35)
                    # gsRasters = gsExample[0].subgridspec(nRates, 1, hspace=0.1)
                    # gsTuning = gsExample[1].subgridspec(nRates,1, hspace=0.8)
                    # gsExtras = gsExample[2].subgridspec(2,2, hspace=0.4,wspace=0.4)

                    gsRasters = gsMain[0,indcell].subgridspec(nRates,1,hspace=0.1)
                    gsTuning = gsMain[1,indcell].subgridspec(nRates,1,hspace=0.8)
                    gsExtras = gsMain[2,indcell].subgridspec(2,2,hspace=0.8,wspace=0.4)

                    # axTuning = plt.subplot(gsExample[1])
                    #cellInd, dbRow = celldatabase.find_cell(celldb, **cellsToPlot[indcell])
                    dbRow = celldb.iloc[cellInd]
                    oneCell = ephyscore.Cell(dbRow)
                    
                    reagentLabels = ['Laser OFF', 'Laser ON']
                    

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

                    
                    for indmod,mod in enumerate(possibleMod):
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
                        axRaster = plt.subplot(gsRasters[indmod])
                        possibleStimInKHz = possibleStim/1000
                        rasterLabels = ['']*nStim;
                        rasterLabels[0] = int(possibleStimInKHz[0])
                        rasterLabels[-1] = int(possibleStimInKHz[-1])

                        rasterLabels *= trialsEachCond.shape[2]

                        reagent=f'{mod}Hz_off'
                        
                        colorEachCond = [colorsRasterDark[sessionType][reagent], colorsRasterLight[sessionType][reagent]]*(nStim)
                        (pRasterS,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                                        indexLimitsEachTrial, timeRange,
                                                                        np.reshape(trialsEachCond,(trialsEachCond.shape[0],np.prod(trialsEachCond.shape[1:])),'F'), 
                                                                        labels=rasterLabels,
                                                                        colorEachCond=colorEachCond,
                                                                        rasterized=True)
                        
                        nTrialson = sum(bdata['laserTrial'][trialInds])
                        nTrialsoff = sum(1-bdata['laserTrial'][trialInds])


                        plt.setp(pRasterS, ms=rasterMarkerSize)

                        if indmod==1:
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

                        else:
                            plt.axvline(TIME_RANGES[eventKey][0],color='r',zorder=-10)
                            plt.axvline(TIME_RANGES[eventKey][1],color='r',zorder=-10)
                        #axRaster.set_yticklabels(['2']+['']*(nFreq-2)+['40'])
                        if indmod==0:
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
                        axTuning = plt.subplot(gsTuning[indmod])
                        
                        allFits = []
                        for reagent in reagentsThisMod:
                            # -- Plot tuning curve --
                            plt.sca(axTuning)
                            window = 3
                            firingRates = dbRow[reagent+'ToneFiringRateEachFreq'+eventKey]
                            smoothedFRs = dbRow[reagent+'ToneFiringRateEachFreqSmoothed'+eventKey]
        
                            
                            fitParams = [dbRow[reagent+'ToneGaussianA'+eventKey], dbRow[reagent+'ToneGaussianX0'+eventKey],
                                        dbRow[reagent+'ToneGaussianSigma'+eventKey], dbRow[reagent+'ToneGaussianY0'+eventKey]]
                            # pdots, pfit = extraplots.plot_tuning_curve(possibleStim, firingRates, fitParams)
                            pfit = plt.plot(np.log2(possibleStim), smoothedFRs)
                            plt.plot(np.log2(possibleStim),firingRates,'--',
                                     color=colorsRasterDark[sessionType][reagent],alpha=0.6)
                            pfit[0].set_color(colorsRasterDark[sessionType][reagent])
                            allFits.append(pfit[0])
                            # if eventKey == 'BTR':
                            #     plt.title(dbRow['4Hz_off'+'BestTimeRange'] + ' ' + dbRow['64Hz_off'+'BestTimeRange'])
                            # pdots[0].set_color(colorsRasterDark[sessionType][reagent])
                            extraplots.boxoff(axTuning)
                            xTicks = np.array([2000, 4000, 8000,16000, 32000])
                            axTuning.set_xticks(np.log2(xTicks))
                            axTuning.set_xticklabels((xTicks/1000).astype(int))
                            if indmod==1:
                                axTuning.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
                            axTuning.set_ylabel('spk/s', fontsize=fontSizeLabels)
                            # axTuning.set_title(f'Cell #{cellInd}',loc='left')
                            axTuning.legend(allFits, ['off','on'],  handlelength=1,
                                                loc='upper right',bbox_to_anchor=(1, 1.5))
                            
                        if metricAnnotation:
                            if 'Smoothed' in metricAnnotation:
                                annoMetricoff = dbRow[f'{mod}Hz_offTone'+metricAnnotation.replace('Smoothed','')+eventKey]
                                annoMetricon = dbRow[f'{mod}Hz_onTone'+metricAnnotation.replace('Smoothed','')+eventKey]

                                annoMetricoffSmoothed = dbRow[f'{mod}Hz_offTone'+metricAnnotation+eventKey]
                                annoMetriconSmoothed = dbRow[f'{mod}Hz_onTone'+metricAnnotation+eventKey]

                                prestring = 'Smoothed: '

                            elif 'FanoFactor' in metricAnnotation and 0:
                                annoMetricoff = dbRow[f'{mod}Hz_offTone'+metricAnnotation+eventKey]
                                annoMetricon = dbRow[f'{mod}Hz_onTone'+metricAnnotation+eventKey]

                                annoMetricoffSmoothed = dbRow[f'{mod}Hz_offTone'+metricAnnotation+'Smoothed'+eventKey]
                                annoMetriconSmoothed = dbRow[f'{mod}Hz_onTone'+metricAnnotation+'Smoothed'+eventKey]

                                prestring = 'Smoothed: '

                            else:
                                annoMetricoff = dbRow[f'{mod}Hz_offTone'+metricAnnotation+eventKey]
                                annoMetricon = dbRow[f'{mod}Hz_onTone'+metricAnnotation+eventKey]
                                annoMetricoffSmoothed = dbRow[f'{mod}Hz_offTone'+'SelectivityKstat'+eventKey]
                                annoMetriconSmoothed = dbRow[f'{mod}Hz_onTone'+'SelectivityKstat'+eventKey]
                                prestring = 'Kstat: '

                            if indmod==0:
                                plt.title(f'{metricAnnotation}\n{mod}Hz: off={annoMetricoff:0.4f}, on={annoMetricon:0.4f}\n'+
                                          f'{prestring}off={annoMetricoffSmoothed:0.4f}, on={annoMetriconSmoothed:0.4f}',y=1.1)
                            else:
                                plt.title(f'{mod}Hz: off={annoMetricoff:0.4f}, on={annoMetricon:0.4f}\n'+
                                          f'{prestring}off={annoMetricoffSmoothed:0.4f}, on={annoMetriconSmoothed:0.4f}')

                        
                        
                        
                        
                        axSpikeShape = plt.subplot(gsExtras[0,0])
                        spikeShape = dbRow['spikeShape']
                        timeVec = 1000*np.arange(len(spikeShape))/30000
                        plt.title('Spike Shape')
                        plt.xlabel('ms')
 
                        plt.sca(axSpikeShape)
                        plt.plot(timeVec,spikeShape,'-k')


                        axFRs = plt.subplot(gsExtras[0,1])
                        FRsoff = dbRow[f'{mod}Hz_offToneFiringRateEachFreq{eventKey}']
                        FRson = dbRow[f'{mod}Hz_onToneFiringRateEachFreq{eventKey}']

                        FRs = [FRsoff,FRson]

                        linfit = stats.linregress(*FRs)
                        maxval = max(np.concat(FRs))
                        
                        plt.sca(axFRs)
                        plt.ylim([0,maxval])
                        plt.xlim([0,maxval])
                        plt.plot(*FRs,'.',color=colorsRasterDark[sessionType][f'{mod}Hz_off'])
                        plt.plot(np.linspace(0,maxval,50),np.linspace(0,maxval,50),'--k')
                        plt.plot(np.linspace(0,maxval,50),
                                 linfit.intercept + linfit.slope*np.linspace(0,maxval,50),
                                 '--',color=colorsRasterDark[sessionType][f'{mod}Hz_off'])
                        plt.title('FR each freq')
                        plt.xlabel('spk/s off')
                        plt.ylabel('spk/s on')
                        



                        axDprimes = plt.subplot(gsExtras[1,indmod])
                        discrimsEachFreq = [abs(dbRow[f'{mod}Hz_offToneDiscrimEachFreq{eventKey}']),
                                            abs(dbRow[f'{mod}Hz_onToneDiscrimEachFreq{eventKey}'])]
                        
                        medianoff=np.nanmedian(discrimsEachFreq[0])
                        medianon=np.nanmedian(discrimsEachFreq[1])
                        plt.sca(axDprimes)

                        maxval = max(np.concat(discrimsEachFreq))
                        
                        plt.plot(*discrimsEachFreq,'.',color=colorsRasterDark[sessionType][f'{mod}Hz_off'])
                        plt.plot(np.linspace(0,maxval,50),np.linspace(0,maxval,50),'--k')
                        plt.plot(medianoff, medianon, '+', color='k', ms=10, mew=2)
                        plt.title("d' each freq")
                        plt.xlabel("d' off")
                        plt.ylabel("d' on")



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

                outputDirNew = os.path.join(outputDir,f'{implant}_selectedCells')
                if not os.path.exists(outputDirNew):
                    os.mkdir(outputDirNew)
                extraplots.save_figure(f'{pageNum}_'+figFilename+'_Just_Curves'+cellstring, 
                                    figFormat, [i*1.5 for i in figSize], outputDirNew,transparent=False)




                



if 0 and ('AMtone' in sessionType):
    plt.figure()
    for indimp,implant in enumerate(studyparams.SUBJECTS_EACH_IMPLANT):
        celldbThisImplant = celldbEachImplant[implant]
        selectedCells = selectedCellsEachImplant[implant]
        plt.subplot(1,2,indimp+1)

        thisMetricoff = celldbThisImplant[selectedCells]['4Hz_ToneLaserModulation'+eventKey]
        thisMetricon = celldbThisImplant[selectedCells]['64Hz_ToneLaserModulation'+eventKey]

        notnans = (~np.isnan(thisMetricon) & ~np.isnan(thisMetricoff))

        thisMetricoff = thisMetricoff[notnans]
        thisMetricon = thisMetricon[notnans]
        wstat,pVal = stats.wilcoxon(thisMetricoff,thisMetricon)

        print(f'wstat={wstat}, p={pVal:f}')
        

        for indcell,dbRow in celldbThisImplant[selectedCells].iterrows():
            plt.plot([1,2],[dbRow['4Hz_ToneLaserModulation'+eventKey],dbRow['64Hz_ToneLaserModulation'+eventKey]],lw=0.4)

        violas = plt.violinplot([thisMetricoff,thisMetricon],
                    showmedians=True,showextrema=True)

        for key in ['cmedians', 'cmaxes', 'cmins', 'cbars']:
            violas[key].set_color(figparams.colors[sessionType]['pre'])

        for indv,body in enumerate(violas['bodies']):
            body.set_facecolor(colorsRasterDark[sessionType][f'{modRates[indv]}Hz_off'])
            body.set_edgecolor(colorsRasterDark[sessionType][f'{modRates[indv]}Hz_off'])

        

        plt.xticks([1,2],['4 Hz','64 Hz'])
        plt.ylim([-0.5,0.5])
        plt.title(f'{implant[0]}->{implant[1]} Laser Modulation using {metricAnnotation}\n'+
                f'wstat={wstat}, p={pVal:f}\n64hz > 4Hz: {np.mean(thisMetricon>thisMetricoff):0.1%}'+
                    f'\t 64Hz < 4Hz: {np.mean(thisMetricon<thisMetricoff):0.1%}')
        
    extraplots.save_figure(figFilename+f'_LaserModulation_{metricAnnotation}', 
                                figFormat, [8,5], outputDir,transparent=False)

    plt.show()