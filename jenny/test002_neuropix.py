import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
import scipy.optimize

inforecFile = os.path.join(settings.INFOREC_PATH,'feat004_inforec.py')
celldb = celldatabase.generate_cell_database(inforecFile)

for indRow, dbRow in celldb.iterrows():
    #plt.clf()
    indplot = 1

    oneCell = ephyscore.Cell(dbRow)
    plt.subplot(3,4,1)
    plt.plot(dbRow.spikeShape, linewidth = 3)
    plt.text(30, -0.1, f"bestChannel = {dbRow.bestChannel}")
    plt.title(oneCell)

    #FTVOTBorders
    ephysData, bdata = oneCell.load('FTVOTBorders')

    # Align spikes to an event
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.3,  0.45]  # In seconds
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    # Type-sorted rasters -- FTVOTBorders
    timeRange = [-0.3, 0.45]
    VOTParamsEachTrial = bdata['targetVOTpercent']
    possibleVOTParams = np.unique(VOTParamsEachTrial)
    FTParamsEachTrial = bdata['targetFTpercent']
    possibleFTParams = np.unique(FTParamsEachTrial)
    trialsEachVOT_FT = behavioranalysis.find_trials_each_combination(VOTParamsEachTrial, possibleVOTParams, FTParamsEachTrial, possibleFTParams)
    trialsEachVOT_FTmin = trialsEachVOT_FT[:,:,0]
    trialsEachVOT_FTmax = trialsEachVOT_FT[:,:,-1]
    trialsEachFT_VOTmin = trialsEachVOT_FT[:,0,:]
    trialsEachFT_VOTmax = trialsEachVOT_FT[:,-1,:]
    #trialsEachVOTCond = behavioranalysis.find_trials_each_type(VOTParamsEachTrial, possibleVOTParams)
    #trialsEachFTCond = behavioranalysis.find_trials_each_type(FTParamsEachTrial, possibleFTParams)
    colorEachCond = ['0.3','0.5','c','b']

    # Raster -- VOT (FTmin)
    plt.subplot(3,4,5)
    fRaster = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange, trialsEachVOT_FTmin, colorEachCond)
    plt.setp(fRaster, ms=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Trials')
    plt.title('VOT, FT = min')

    # PSTH -- VOT (FTmax)
    binWidth = 0.010
    timeRange = [-0.3,  0.45]
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    smoothWinSizePsth = 6
    lwPsth = 2
    downsampleFactorPsth = 3
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
    plt.subplot(3,4,9)
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec, trialsEachVOT_FTmin, colorEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
    plt.xlabel('Time (s)')
    plt.ylabel('Firing Rate (Sp/s)')

    # Raster -- VOT (FTmax)
    plt.subplot(3,4,6)
    fRaster = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange, trialsEachVOT_FTmax, colorEachCond)
    #plt.setp(fRaster, ms=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Trials')
    plt.title('VOT, FT = max')

    # PSTH -- VOT (FTmax)
    binWidth = 0.010
    timeRange = [-0.3,  0.45]
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    smoothWinSizePsth = 6
    lwPsth = 2
    downsampleFactorPsth = 3
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
    plt.subplot(3,4,10)
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec, trialsEachVOT_FTmax, colorEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
    plt.xlabel('Time (s)')
    plt.ylabel('Firing Rate (Sp/s)')

    # Raster -- FT (VOT = min)
    plt.subplot(3,4,7)
    fRaster = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange, trialsEachFT_VOTmin, colorEachCond)
    plt.setp(fRaster, ms=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Trials')
    plt.title('FT, VOT = min')

    # PSTH -- FT (VOT = min)
    binWidth = 0.010
    timeRange = [-0.3,  0.45]
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    smoothWinSizePsth = 6
    lwPsth = 2
    downsampleFactorPsth = 3
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
    plt.subplot(3,4,11)
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec, trialsEachFT_VOTmin, colorEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
    plt.xlabel('Time (s)')
    plt.ylabel('Firing Rate (Sp/s)')


    # Raster -- FT (VOT = max)
    plt.subplot(3,4,8)
    fRaster = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange, trialsEachFT_VOTmax, colorEachCond)
    plt.setp(fRaster, ms=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Trials')
    plt.title('FT, VOT = max')

    # PSTH -- FT (VOT = min)
    binWidth = 0.010
    timeRange = [-0.3,  0.45]
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    smoothWinSizePsth = 6
    lwPsth = 2
    downsampleFactorPsth = 3
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
    plt.subplot(3,4,12)
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec, trialsEachFT_VOTmax, colorEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
    plt.xlabel('Time (s)')
    plt.ylabel('Firing Rate (Sp/s)')

    #AM
    ephysData, bdata = oneCell.load('AM')

    # Align spikes to an event
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.3,  0.75]  # In seconds
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    # Type-sorted rasters -- AM
    timeRange = [-0.3, 0.75]
    soundParamsEachTrial = bdata['currentFreq']
    possibleParams = np.unique(soundParamsEachTrial)
    trialsEachCond = behavioranalysis.find_trials_each_type(soundParamsEachTrial, possibleParams)
    plt.subplot(3,4,2)
    fRaster = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange, trialsEachCond)
    #plt.setp(fRaster, ms=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Trials')
    plt.title('AM')

    #pureTones
    ephysData, bdata = oneCell.load('pureTones')

    # Align spikes to an event
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.2,  0.3]  # In seconds
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    # Type-sorted rasters -- pureTones
    timeRange = [-0.2, 0.3]
    soundFreqEachTrial = bdata['currentFreq']
    possibleFreq = np.unique(soundFreqEachTrial)
    soundIntensityEachTrial = bdata['currentIntensity']
    possibleIntensities = np.unique(bdata['currentIntensity'])
    trialsEachFreq = behavioranalysis.find_trials_each_type(soundFreqEachTrial, possibleFreq)
    plt.subplot(3,4,3)
    fRaster = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange, trialsEachFreq)
    plt.setp(fRaster, ms=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Trials')
    plt.title('Pure Tones')
    '''
    # Fit Gaussian tuning
    def gaussian(x, a, x0, sigma, y0):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))+y0

    #Possible Freq
    #averageFiringRate = [2.3, 5.6, 10.1, 14.2, 8.9]
    binWidth = 0.010
    timeRange = [0,  bdata['stimDur'][-1]]
    trialsEachCond = behavioranalysis.find_trials_each_combination(soundFreqEachTrial, possibleFreq, soundIntensityEachTrial, possibleIntensities)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange)
    spikesEachFreq_60db = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond[:,:,0], indexLimitsEachTrial)
    spikesEachFreq_70db = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond[:,:,1], indexLimitsEachTrial)
    # ?? trialsEachFreq == 694, indexLimitsEachTrial == 695.
    avgRateEachFreq_60db = spikesEachFreq_60db/bdata['stimDur'][-1]
    avgRateEachFreq_70db = spikesEachFreq_70db/bdata['stimDur'][-1]
    possibleLogFreq = np.log2(possibleFreq)
    nFreq = len(possibleLogFreq)

    # PARAMS: a, x0, sigma, y0
    p0 = [1, possibleLogFreq[nFreq//2], 1, 0]
    bounds = ([0, possibleLogFreq[0], 0, 0],
              [np.inf, possibleLogFreq[-1], np.inf, np.inf])

    popt_60, pcov_60 = scipy.optimize.curve_fit(gaussian, possibleLogFreq,
                                          averageFiringRate_60db, p0=p0, bounds=bounds)

    popt_70, pcov_70 = scipy.optimize.curve_fit(gaussian, possibleLogFreq,
                                          averageFiringRate_70db, p0=p0, bounds=bounds)

    # -- Calculate R^2 --
    gaussianResp = gaussian(possibleLogFreq, *popt)
    residuals = averageFiringRate - gaussianResp
    ssquared = np.sum(residuals**2)
    ssTotal = np.sum((averageFiringRate-np.mean(averageFiringRate))**2)
    Rsquared = 1 - (ssquared/ssTotal)

    # -- Calculate bandwidth --
    fullWidthHalfMax = 2.355*popt[2] # Sigma is popt[2]

    plt.clf()
    xvals = np.linspace(possibleLogFreq[0], possibleLogFreq[-1], 60)
    yvals = gaussian(xvals, *popt)
    plt.plot(possibleLogFreq, averageFiringRate, 'o')
    plt.plot(xvals, yvals, '-', lw=3)
    plt.title(f'R^2 = {Rsquared:0.4f} ,  Bandwidth = {fullWidthHalfMax:0.2f} oct')
    plt.ylabel('Firing rate (Hz)')
    plt.xlabel('Frequency (kHz)')
    xTickLabels = [f'{freq/1000:0.0f}' for freq in possibleFreq]
    plt.xticks(possibleLogFreq, xTickLabels)
    plt.show()
    '''


    plt.gcf().set_size_inches([14, 12])
    print(oneCell)
    plt.show()
    input("press enter for next cell")
    indplot += 1
    plt.close()
plt.close()
