import sys
sys.path.append('..')
import numpy as np
from statsmodels.stats.proportion import proportion_confint

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches

from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import extraplots

import studyparams


def logistic(x, L, x0, k, b):
    return L / (1 + np.exp(-k * (x - x0))) + b


def logistic_tuning_fit(stimArray, responseArray, minVal):
    """Fits a logistic curve to given data, setting the bottom asymptote.

    Inputs:
        stimArray: array of length N trials giving stimulus used for each trial. For frequency tuning, take logarithm of frequencies (if presented freqs were on log scale)
        responseArray: array of length N trials giving spike rate during each trial.
        minVal: float, minimum value of logistic curve

    Outputs:
        curveFit: parameters for fit gaussian curve.
        Rsquared: R^2 value for fit curve compared to raw data.
    """
    from scipy.optimize import curve_fit
    try:
        maxInd = np.argmax(responseArray)
        p0 = [max(responseArray), np.median(stimArray), 1] # initial guess
        upperBounds = [100+minVal, np.inf, np.inf]
        lowerBounds = [minVal, -np.inf, 0]
        curve_form = lambda x, L, x0, k: logistic(x, L, x0, k, minVal)
        curveFit = curve_fit(curve_form, stimArray, responseArray, p0=p0, bounds=(lowerBounds, upperBounds), maxfev=10000)[0]
    except RuntimeError:
        print
        "Could not fit logistic curve to tuning data."
        return None, None
    except ValueError:
        print("Data could not be fit given the bounds")
        return None, None

    # calculate R^2 value for fit
    fitResponseArray = curve_form(stimArray, curveFit[0], curveFit[1], curveFit[2])
    residuals = responseArray - fitResponseArray
    SSresidual = np.sum(residuals ** 2)
    SStotal = np.sum((responseArray - np.mean(responseArray)) ** 2)
    Rsquared = 1 - (SSresidual / SStotal)

    return curveFit, Rsquared


SOM_ARCHT_MICE = studyparams.SOM_ARCHT_MICE
PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
PV_CHR2_MICE = studyparams.PV_CHR2_MICE
mouseType = [PV_ARCHT_MICE, SOM_ARCHT_MICE, PV_CHR2_MICE]
mouseLabel = ['PV-ArchT', 'SOM-ArchT', 'PV-ChR2']
legendLabel = ['no PV', 'no SOM', 'PV activated']

for indType, mice in enumerate(mouseType):
    for mouse in mice:
        if indType == 2:
            laserSessions = studyparams.miceDict[mouse]['3mW laser']
        else:
            laserSessions = studyparams.miceDict[mouse]['10mW laser']
        laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

        numLasers = np.unique(laserBehavData['laserSide'])
        numBands = np.unique(laserBehavData['currentBand'])
        numSNRs = np.unique(laserBehavData['currentSNR'])

        trialsEachCond = behavioranalysis.find_trials_each_combination(laserBehavData['laserSide'], numLasers,
                                                                       laserBehavData['currentBand'], numBands)
        trialsEachSNR = behavioranalysis.find_trials_each_type(laserBehavData['currentSNR'], numSNRs)

        trialsEachCond3Params = np.zeros(
            (len(laserBehavData['laserSide']), len(numLasers), len(numBands), len(numSNRs)), dtype=bool)
        for ind in range(len(numSNRs)):
            trialsEachCond3Params[:, :, :, ind] = trialsEachCond & trialsEachSNR[:, ind][:, np.newaxis, np.newaxis]

        valid = laserBehavData['valid'].astype(bool)
        correct = laserBehavData['outcome'] == laserBehavData.labels['outcome']['correct']
        rightChoice = laserBehavData['choice'] == laserBehavData.labels['choice']['right']
        leftChoice = laserBehavData['choice'] == laserBehavData.labels['choice']['left']

        if 'toneSide' in laserBehavData.keys():
            if laserBehavData['toneSide'][-1] == laserBehavData.labels['toneSide']['right']:
                toneChoice = rightChoice
                noiseChoice = leftChoice
            elif laserBehavData['toneSide'][-1] == laserBehavData.labels['toneSide']['left']:
                toneChoice = leftChoice
                noiseChoice = rightChoice
        else:
            # all tones meant go to right before introduction of 'toneSide' key
            toneChoice = rightChoice
            noiseChoice = leftChoice

        fig = plt.gcf()
        fig.clf()
        fig.set_facecolor('w')

        gs = gridspec.GridSpec(1, len(numBands)+1)
        gs.update(top=0.90, bottom=0.15, left=0.07, right=0.98, wspace=0.5, hspace=0.3)

        # -- plot logistic curve fits for each bandwidth and laser presentation --
        bandColours = ['r', 'k', 'b']
        laserLines = ['-', '--']
        theseLabels = ['control', legendLabel[indType]]

        fitCurves = []
        fitxVals = np.linspace(-10,20,500)

        for band in range(len(numBands)):
            axPsyCurve = plt.subplot(gs[0, band])
            laserFill = [bandColours[band], 'white']
            lines = []
            for laser in range(len(numLasers)):
                thisPsyCurve = np.zeros(len(numSNRs))
                upperErrorBar = np.zeros(len(numSNRs))
                lowerErrorBar = np.zeros(len(numSNRs))
                for snr in range(len(numSNRs)):
                    validThisCond = valid[trialsEachCond3Params[:, laser, band, snr]]
                    toneChoiceThisCond = toneChoice[trialsEachCond3Params[:, laser, band, snr]]
                    thisPsyCurve[snr] = 100.0 * np.sum(toneChoiceThisCond) / np.sum(validThisCond)

                    CIthisSNR = np.array(
                        proportion_confint(np.sum(toneChoiceThisCond), np.sum(validThisCond), method='wilson'))
                    upperErrorBar[snr] = 100.0 * CIthisSNR[1] - thisPsyCurve[snr]
                    lowerErrorBar[snr] = thisPsyCurve[snr] - 100.0 * CIthisSNR[0]

                line, = plt.plot(numSNRs[1:], thisPsyCurve[1:], color=bandColours[band], mec=bandColours[band], marker='o',
                         mfc=laserFill[laser], ls='none', ms=10, zorder=-laser)
                lines.append(line)
                plt.errorbar(numSNRs[1:], thisPsyCurve[1:], yerr=[lowerErrorBar[1:], upperErrorBar[1:]], fmt='none',
                             color=bandColours[band], lw=2, capsize=5, capthick=1)

                fitParams, R2 = logistic_tuning_fit(numSNRs[1:], thisPsyCurve[1:], thisPsyCurve[0])

                if fitParams is not None:
                    fitPsyCurve = logistic(fitxVals, fitParams[0], fitParams[1], fitParams[2], thisPsyCurve[0])
                    plt.plot(fitxVals, fitPsyCurve, color=bandColours[band], ls=laserLines[laser], lw=2)
                    fitCurves.append(fitPsyCurve)
                else:
                    fitCurves.append(None)

            plt.legend(lines, theseLabels, borderaxespad=0.3, prop={'size': 12}, loc='best')

            axPsyCurve.set_title('{} octaves'.format(numBands[band]))
            # axPsyCurve.set_xticks(range(len(numSNRs)))
            # axPsyCurve.set_xticklabels(numSNRs)
            axPsyCurve.set_xlabel('SNR (dB)')

            axPsyCurve.set_ylim(0, 100)
            axPsyCurve.set_ylabel('% trials tone reported')

            extraplots.boxoff(axPsyCurve)

        # -- plot 50% detection point for each bandwidth and laser presentation --
        axThresh = plt.subplot(gs[0, -1])

        barLoc = np.array([-0.24, 0.24])
        xLocs = np.arange(len(numBands))
        xTickLabels = numBands

        for band in range(len(numBands)):
            threshold = np.zeros(len(numLasers))
            for laser in range(len(numLasers)):
                thisCurve = fitCurves[2*band+laser]
                if thisCurve is not None:
                    threshArg = np.argmin((np.abs(thisCurve - 50))) # argument nearest to 50% detection rate
                    threshold[laser] = fitxVals[threshArg]
                else:
                    threshold[laser] = None

            if all(threshold):
                xVals = barLoc + xLocs[band]
                plt.plot(xVals, threshold, 'k-', lw=2)
                l1, = plt.plot(xVals[0], threshold[0], 'o', mec='k', mfc='k', ms=10)
                l2, = plt.plot(xVals[1], threshold[1], 'o', mec='k', mfc='white', ms=10)

        if all(threshold):
            axThresh.legend([l1, l2], ['control', legendLabel[indType]])

            axThresh.set_xlim(xLocs[0] - 0.5, xLocs[-1] + 0.5)
            axThresh.set_xticks(xLocs)
            axThresh.set_xticklabels(numBands)
            axThresh.set_xlabel('Masker bandwidth (oct)')

            yLims = axThresh.get_ylim()
            axThresh.set_ylim(yLims[0] - 10, yLims[1] + 10)
            axThresh.set_ylabel('Detection threshold (dB)')

            extraplots.boxoff(axThresh)

        plt.suptitle(mouse + ' ({})'.format(mouseLabel[indType]))

        figFilename = '{}_logistic_fit_report'.format(mouse)
        extraplots.save_figure(figFilename, 'png', [3*len(numBands)+2, 4], '/tmp/')
