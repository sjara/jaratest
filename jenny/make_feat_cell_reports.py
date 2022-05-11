import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import colorpalette
import scipy.optimize
import matplotlib

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To render as font rather than outlines

subject = 'feat004'
inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
dbPath = os.path.join(settings.DATABASE_PATH, f'celldb_{subject}.h5')



celldb = celldatabase.load_hdf(dbPath)
#celldb = celldatabase.generate_cell_database(inforecFile)

for indRow, dbRow in celldb.iterrows():
    plt.clf()

    oneCell = ephyscore.Cell(dbRow)
    gsMain = gs.GridSpec(3, 4)
    gsMain.update(left=0.075, right=0.98, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4) #Change spacing of things
    plt.suptitle(oneCell, fontsize=16, fontweight='bold', y = 0.99)

    # Plot Waveform
    ax0 = plt.subplot(gsMain[0, 0])
    plt.plot(dbRow.spikeShape, linewidth = 3)
    #plt.title('bestChannel = {}'.format(dbRow.bestChannel))
    plt.text(30, -0.1, f"bestChannel = {dbRow.bestChannel}")
    #plt.title('x {}, '.format(dbRow.x_coord) + 'y {}, '.format(dbRow.y_coord) + 'z {}'.format(dbRow.z_coord))
    #plt.title(f'x:{dbRow.x_coord:0.1f}, ' + f'y:{dbRow.y_coord:0.1f}, ' + f'z:{dbRow.z_coord}')
    plt.title(f'Recording Site:{dbRow.recordingSiteName}\n'+f'x:{dbRow.x_coord:0.0f}  ' +
              f'y:{dbRow.y_coord:0.0f}  ' + f'z:{dbRow.z_coord:0.0f}')

    #FTVOTBorders
    ephysData, bdata = oneCell.load('FTVOTBorders')

    # Align spikes to an event
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.3, 0.45]  # In seconds
    (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    # Type-sorted rasters -- FTVOTBorders
    timeRange = [-0.3, 0.45]
    VOTParamsEachTrial = bdata['targetVOTpercent']
    possibleVOTParams = np.unique(VOTParamsEachTrial)
    FTParamsEachTrial = bdata['targetFTpercent']
    possibleFTParams = np.unique(FTParamsEachTrial)
    trialsEachVOT_FT = behavioranalysis.find_trials_each_combination(VOTParamsEachTrial, possibleVOTParams, FTParamsEachTrial, possibleFTParams)
    trialsEachVOT_FTmin = trialsEachVOT_FT[:, :, 0]
    trialsEachVOT_FTmax = trialsEachVOT_FT[:, :, -1]
    trialsEachFT_VOTmin = trialsEachVOT_FT[:, 0, :]
    trialsEachFT_VOTmax = trialsEachVOT_FT[:, -1, :]
    #trialsEachVOTCond = behavioranalysis.find_trials_each_type(VOTParamsEachTrial, possibleVOTParams)
    #trialsEachFTCond = behavioranalysis.find_trials_each_type(FTParamsEachTrial, possibleFTParams)
    VOTlabels = list(possibleVOTParams)
    FTlabels = list(possibleFTParams)
    colorsEachVOT = ['#3e5cfc', '#3ebbfc', '#fdce89', '#ea8d04']
    colorsEachFT = ['#3e5cfc', '#3ebbfc', '#fdce89', '#ea8d04']

    # Raster -- VOT (FTmin)
    ax1 = plt.subplot(gsMain[1, 0])
    pRaster, hcond, zline =extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange, trialsEachVOT_FTmin, colorsEachVOT, labels = VOTlabels)
    plt.setp(pRaster, ms=2)
    plt.xlabel('Time (s)')
    #plt.ylabel('Trials')
    plt.title(f'VOT, FTmin (n = {np.sum(trialsEachVOT_FTmin)})')

    # PSTH -- VOT (FTmax)
    binWidth = 0.010
    timeRange = [-0.3, 0.45]
    timeVec = np.arange(timeRange[0], timeRange[-1], binWidth)
    smoothWinSizePsth = 6
    lwPsth = 2
    downsampleFactorPsth = 3
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeVec)
    ax2 = plt.subplot(gsMain[2, 0], sharex=ax1)
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec, trialsEachVOT_FTmin, colorsEachVOT, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
    plt.xlabel('Time (s)')
    plt.ylabel('Firing Rate (Sp/s)')

    # Raster -- VOT (FTmax)
    ax3 = plt.subplot(gsMain[1, 1])
    pRaster, hcond, zline =extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange, trialsEachVOT_FTmax, colorsEachVOT, labels = VOTlabels)
    plt.setp(pRaster, ms=2)
    plt.xlabel('Time (s)')
    #plt.ylabel('trials')
    plt.title(f'VOT, FTmax (n = {np.sum(trialsEachVOT_FTmax)})')

    # PSTH -- VOT (FTmax)
    binWidth = 0.010
    timeRange = [-0.3, 0.45]
    timeVec = np.arange(timeRange[0], timeRange[-1], binWidth)
    smoothWinSizePsth = 6
    lwPsth = 2
    downsampleFactorPsth = 3
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeVec)
    ax4 = plt.subplot(gsMain[2, 1], sharex=ax3)
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec, trialsEachVOT_FTmax, colorsEachVOT, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
    plt.xlabel('Time (s)')
    plt.ylabel('Firing Rate (Sp/s)')

    # Raster -- FT (VOT = min)
    ax5 = plt.subplot(gsMain[1, 2])
    pRaster, hcond, zline =extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange, trialsEachFT_VOTmin, colorsEachFT, labels = VOTlabels)
    plt.setp(pRaster, ms=2)
    plt.xlabel('Time (s)')
    #plt.ylabel('Trials')
    plt.title(f'FT, VOTmin (n = {np.sum(trialsEachFT_VOTmin)})')

    # PSTH -- FT (VOT = min)
    binWidth = 0.010
    timeRange = [-0.3, 0.45]
    timeVec = np.arange(timeRange[0], timeRange[-1], binWidth)
    smoothWinSizePsth = 6
    lwPsth = 2
    downsampleFactorPsth = 3
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeVec)
    ax6 = plt.subplot(gsMain[2, 2], sharex=ax5)
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec, trialsEachFT_VOTmin, colorsEachFT, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
    plt.xlabel('Time (s)')
    plt.ylabel('Firing Rate (Sp/s)')


    # Raster -- FT (VOT = max)
    ax7 = plt.subplot(gsMain[1, 3])
    pRaster, hcond, zline =extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange, trialsEachFT_VOTmax, colorsEachFT, labels = VOTlabels)
    plt.setp(pRaster, ms=2)
    plt.xlabel('Time (s)')
    #plt.ylabel('trials')
    plt.title(f'FT, VOTmax (n = {np.sum(trialsEachFT_VOTmax)})')

    # PSTH -- FT (VOT = min)
    binWidth = 0.010
    timeRange = [-0.3, 0.45]
    timeVec = np.arange(timeRange[0], timeRange[-1], binWidth)
    smoothWinSizePsth = 6
    lwPsth = 2
    downsampleFactorPsth = 3
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeVec)
    ax8 = plt.subplot(gsMain[2, 3], sharex=ax7)
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec, trialsEachFT_VOTmax, colorsEachFT, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
    plt.xlabel('Time (s)')
    plt.ylabel('Firing Rate (Sp/s)')

    #AM
    ephysData, bdata = oneCell.load('AM')

    # Align spikes to an event
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.3, 0.75]  # In seconds
    (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    # Type-sorted rasters -- AM
    timeRange = [-0.3, 0.75]
    soundParamsEachTrial = bdata['currentFreq']
    possibleParams = np.unique(soundParamsEachTrial)
    trialsEachCond = behavioranalysis.find_trials_each_type(soundParamsEachTrial, possibleParams)
    ax9 = plt.subplot(gsMain[0, 1])
    pRaster, hcond, zline =extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange, trialsEachCond)
    plt.setp(pRaster, ms=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Trials')
    plt.title('AM')

    #pureTones
    ephysData, bdata = oneCell.load('pureTones')

    # Align spikes to an event
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    if len(eventOnsetTimes) > len(bdata['currentIntensity']):
        print('Ephys data is {} trial longer than bdata, ignoring last trial of ephysData'.format(len(eventOnsetTimes) - len(bdata['currentIntensity'])))
        newLastTrial = len(bdata['currentIntensity'])
        eventOnsetTimes = eventOnsetTimes[0:newLastTrial]
    timeRange = [-0.2, 0.3]  # In seconds
    (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    # Type-sorted rasters -- pureTones
    timeRange = [-0.2, 0.3]
    soundFreqEachTrial = bdata['currentFreq']
    possibleFreq = np.unique(soundFreqEachTrial)
    soundIntensityEachTrial = bdata['currentIntensity']
    possibleIntensities = np.unique(bdata['currentIntensity'])
    trialsEachFreq = behavioranalysis.find_trials_each_type(soundFreqEachTrial, possibleFreq)
    ax10 = plt.subplot(gsMain[0, 2])
    pRaster, hcond, zline =extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange, trialsEachFreq)
    plt.setp(pRaster, ms=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Trials')
    plt.title('Pure Tones')

    # Fit Gaussian tuning
    def gaussian(x, a, x0, sigma, y0):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))+y0

    #Get average firing rates for each freq, intensity
    binWidth = 0.010
    timeRange = [0, bdata['stimDur'][-1]]
    trialsEachCond = behavioranalysis.find_trials_each_combination(soundFreqEachTrial, possibleFreq, soundIntensityEachTrial, possibleIntensities)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    avgRateEachCond = np.empty((len(possibleFreq), len(possibleIntensities)))
    for indFreq, thisFreq in enumerate(possibleFreq):
        for indIntensity, thisIntensity in enumerate(possibleIntensities):
            spikeCountThisCond = sum(spikeCountMat[trialsEachCond[:, indFreq, indIntensity]])
            numTrialsThisCond = sum(trialsEachCond[:, indFreq, indIntensity])
            avgCountThisCond = spikeCountThisCond/numTrialsThisCond
            timeWindow = timeRange[1] - timeRange[0]
            avgRateEachCond[indFreq, indIntensity] = avgCountThisCond/timeWindow

    possibleLogFreq = np.log2(possibleFreq)
    nFreq = len(possibleLogFreq)

    #Fit for intensity = 60dB
    # PARAMS: a, x0, sigma, y0
    p0 = [1, possibleLogFreq[nFreq//2], 1, 0]
    bounds = ([0, possibleLogFreq[0], 0, 0],
              [np.inf, possibleLogFreq[-1], np.inf, np.inf])

    popt, pcov = scipy.optimize.curve_fit(gaussian, possibleLogFreq,
                                          avgRateEachCond[:, 0], p0=p0, bounds=bounds)

    # -- Calculate R^2 --
    gaussianResp = gaussian(possibleLogFreq, *popt)
    residuals = avgRateEachCond[:, 0] - gaussianResp
    ssquared = np.sum(residuals**2)
    ssTotal = np.sum((avgRateEachCond[:, 0]-np.mean(avgRateEachCond[:, 0]))**2)
    Rsquared_60dB = 1 - (ssquared/ssTotal)

    # -- Calculate bandwidth --
    fullWidthHalfMax_60dB = 2.355*popt[2] # Sigma is popt[2]

    ax11 = plt.subplot(gsMain[0, 3])
    yvals = np.linspace(possibleLogFreq[0], possibleLogFreq[-1], 60)
    xvals = gaussian(yvals, *popt)
    plt.plot(avgRateEachCond[:, 0], possibleLogFreq, 'ko')
    line1, = plt.plot(xvals, yvals, 'k-', lw=3)
    #plt.title(f'R^2 = {Rsquared_60dB:0.4f} , Bandwidth = {fullWidthHalfMax:0.2f} oct')
    plt.xlabel('Firing rate (Hz)')
    plt.ylabel('Frequency (kHz)')
    yTickLabels = [f'{freq/1000:0.0f}' for freq in possibleFreq]
    plt.yticks(possibleLogFreq, yTickLabels)

    #Fit for intensity = 70dB
    # PARAMS: a, x0, sigma, y0
    p0 = [1, possibleLogFreq[nFreq//2], 1, 0]
    bounds = ([0, possibleLogFreq[0], 0, 0],
              [np.inf, possibleLogFreq[-1], np.inf, np.inf])

    popt, pcov = scipy.optimize.curve_fit(gaussian, possibleLogFreq,
                                          avgRateEachCond[:, 1], p0=p0, bounds=bounds)

    # -- Calculate R^2 --
    gaussianResp = gaussian(possibleLogFreq, *popt)
    residuals = avgRateEachCond[:, 1] - gaussianResp
    ssquared = np.sum(residuals**2)
    ssTotal = np.sum((avgRateEachCond[:, 1]-np.mean(avgRateEachCond[:, 1]))**2)
    Rsquared_70dB = 1 - (ssquared/ssTotal)

    # -- Calculate bandwidth --
    fullWidthHalfMax_70dB = 2.355*popt[2] # Sigma is popt[2]

    #ax11 = plt.subplot(gsMain[0, 3])
    yvals = np.linspace(possibleLogFreq[0], possibleLogFreq[-1], 60)
    xvals = gaussian(yvals, *popt)
    plt.plot(avgRateEachCond[:, 1], possibleLogFreq, 'ro')
    line2, = plt.plot(xvals, yvals, 'r-', lw=3)
    plt.title(f'60dB: R^2 = {Rsquared_60dB:0.4f}, BW = {fullWidthHalfMax_60dB:0.2f} oct \n' + f'70dB: R^2 = {Rsquared_70dB:0.4f}, BW = {fullWidthHalfMax_70dB:0.2f} oct \n', fontsize = 12)
    plt.xlabel('Firing rate (Hz)')
    plt.ylabel('Frequency (kHz)')
    yTickLabels = [f'{freq/1000:0.0f}' for freq in possibleFreq]
    plt.yticks(possibleLogFreq, yTickLabels)
    ax11.legend([line1, line2], ['60dB', '70dB'], loc = 'lower left')



    plt.gcf().set_size_inches([14, 12])
    print(oneCell)
    plt.show()
    input("press enter for next cell")
    #figPath = os.path.join(settings.FIGURES_DATA_PATH, 'cell_reports', f'{subject}_{dbRow.date}_{dbRow.maxDepth}um_c{dbRow.cluster}_report.png')
    #plt.savefig(figPath, format='png')

    plt.close()
plt.close()
