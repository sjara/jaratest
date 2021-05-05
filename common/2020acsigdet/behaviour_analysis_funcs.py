import os
import numpy as np
import matplotlib.colors
import matplotlib.pyplot as plt
from scipy import stats

from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams

#REALLY DUMB WORKAROUND FOR THE FACT THAT COLOR LISTS ONLY TAKES RGBA INPUTS
def list_colours_to_rgba(colours):
    dumbcolours = np.zeros((len(colours),4))
    for indColour, colour in enumerate(colours):
        thisColour = matplotlib.colors.colorConverter.to_rgba(colour, alpha=1)
        dumbcolours[indColour,:] = thisColour
    return dumbcolours

def bootstrap_median_CI(data, reps=1000, interval=95):
    medians = np.zeros(reps)
    for ind in range(reps):
        samples = np.random.choice(data, len(data), replace=True)
        medians[ind] = np.median(samples)
    low = np.percentile(medians,(100-interval)/2.0)
    high = np.percentile(medians,interval+(100-interval)/2.0)
    return [low, high]

# function to calculate effect size (Cohen's d)
def cohend(data1, data2, independent=True):
    n1, n2 = len(data1), len(data2)

    # use pooled std for independent samples or pre-treatment std for paired samples
    if independent:
        stdev1, stdev2 = np.var(data1, ddof=1), np.var(data2, ddof=1)
        stdev = np.sqrt(((n1-1)*stdev1 + (n2-1)*stdev2) / (n1 + n2 - 2))
    else:
        stdev = np.var(data1, ddof=1)
    return (np.mean(data1) - np.mean(data2)) / stdev

def get_reaction_times(mouse, sessions):
    behavData = behavioranalysis.load_many_sessions(mouse, sessions)
    if all(~np.isnan(behavData['timeCenterOut'])):
        reactionTimes = behavData['timeCenterOut'] - behavData['timeTarget']
        decisionTimes = behavData['timeSideIn'] - behavData['timeCenterOut']
    else:
        reactionTimes = []
        decisionTimes = []
        for session in sessions:
            thisBehavFile = os.path.join(settings.BEHAVIOR_PATH, mouse, mouse + '_2afc_' + session + '.h5')
            if os.path.exists(thisBehavFile):
                thisBehavData = loadbehavior.BehaviorData(thisBehavFile, readmode='full')
            timeSound = thisBehavData['timeTarget']
            timeCenterOut = np.zeros(len(timeSound))
            timeSideIn = thisBehavData['timeSideIn']

            eventCode = np.array(thisBehavData.events['eventCode'])
            eventTime = thisBehavData.events['eventTime']
            CoutInds = np.where(eventCode == behavData.stateMatrix['eventsNames']['Cout'])[0]

            for trial in range(len(timeSound)):
                soundEventInd = np.where(eventTime == timeSound[trial])[0][0]
                CoutInd = CoutInds[np.argmax(CoutInds > soundEventInd)]
                timeCenterOut[trial] = eventTime[CoutInd]

            thisReactionTimes = timeCenterOut - timeSound
            thisDecisionTimes = timeSideIn - timeCenterOut

            reactionTimes.extend(thisReactionTimes)
            decisionTimes.extend(thisDecisionTimes)

        reactionTimes = np.array(reactionTimes)
        decisionTimes = np.array(decisionTimes)

    return reactionTimes, decisionTimes

def get_trials(behavData):
    numLasers = np.unique(behavData['laserSide'])
    numBands = np.unique(behavData['currentBand'])
    numSNRs = np.unique(behavData['currentSNR'])

    trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['laserSide'], numLasers,
                                                                   behavData['currentBand'], numBands)
    trialsEachSNR = behavioranalysis.find_trials_each_type(behavData['currentSNR'], numSNRs)

    trialsEachCond3Params = np.zeros((len(behavData['laserSide']), len(numLasers), len(numBands), len(numSNRs)), dtype=bool)
    for ind in range(len(numSNRs)):
        trialsEachCond3Params[:, :, :, ind] = trialsEachCond & trialsEachSNR[:, ind][:, np.newaxis, np.newaxis]

    incorrect = behavData['outcome'] == behavData.labels['outcome']['error']
    correct = behavData['outcome'] == behavData.labels['outcome']['correct']
    rightChoice = behavData['choice'] == behavData.labels['choice']['right']
    leftChoice = behavData['choice'] == behavData.labels['choice']['left']

    if 'toneSide' in behavData.keys():
        if behavData['toneSide'][-1] == behavData.labels['toneSide']['right']:
            toneChoice = rightChoice
            noiseChoice = leftChoice
        elif behavData['toneSide'][-1] == behavData.labels['toneSide']['left']:
            toneChoice = leftChoice
            noiseChoice = rightChoice
    else:
        # all tones meant go to right before introduction of 'toneSide' key
        toneChoice = rightChoice
        noiseChoice = leftChoice

    return correct, incorrect, toneChoice, noiseChoice, trialsEachCond3Params, [numLasers, numBands, numSNRs]

# -- functions for plotting common panels across figures --
# make the plots showing paired comparison of laser vs no laser averages
def plot_laser_comparison(axes, data, laserColour, laserFaceColour, yLim, xticklabels):
    barLoc = np.array([-0.24, 0.24])

    for indMouse in range(data[0].shape[0]):
        plt.plot(barLoc, [data[0][indMouse], data[1][indMouse]], '-', color=figparams.colp['connectLine'])

    plt.plot(np.tile(barLoc[0], data[0].shape[0]), data[0], 'o', color=figparams.colp['baseline'], ms=figparams.markerSize)
    plt.plot(np.tile(barLoc[1], data[1].shape[0]), data[1], 'o', mec=laserColour, mfc=laserFaceColour, ms=figparams.markerSize)

    # median = np.median(accuracyData, axis=0)
    # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')

    axes.set_xlim(barLoc[0] - 0.2, barLoc[1] + 0.2)
    axes.set_xticks(barLoc)
    axes.set_xticklabels(xticklabels)
    axes.set_ylim(yLim)

    extraplots.boxoff(axes)
    extraplots.set_ticks_fontsize(axes, figparams.fontSizeTicks)

    pVal = stats.wilcoxon(data[1], data[0])[1]
    print(f"Change in pVal: {pVal}")

    if pVal < 0.05:
        extraplots.significance_stars(barLoc, 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)

def plot_cell_type_comparison(axes, data, colours, yLim, facecolours=None):
    width = 0.3
    barLoc = np.array([-0.18, 0.18])

    for indType in range(len(data)):
        if facecolours is None:
            facecolours = np.tile('white', len(data))
        jitter = 0.8 * width * (np.random.random(len(data[indType])) - 0.5)
        plt.scatter(np.tile(barLoc[indType], len(data[indType])) + jitter, data[indType], edgecolors=colours[indType], facecolors=facecolours[indType])

        plt.plot([barLoc[indType] - width / 2, barLoc[indType] + width / 2], [np.median(data[indType]), np.median(data[indType])],
                 color='k', linewidth=4, zorder=10)  # medians

        CI = bootstrap_median_CI(data[indType])
        # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
        plt.plot([barLoc[indType], barLoc[indType]], CI, color='k', linewidth=2)  # error bars
        plt.plot([barLoc[indType] - width / 8, barLoc[indType] + width / 8], [CI[0], CI[0]], color='k', linewidth=2)  # bottom caps
        plt.plot([barLoc[indType] - width / 8, barLoc[indType] + width / 8], [CI[1], CI[1]], color='k', linewidth=2)  # top caps

    pVal = stats.ranksums(data[0], data[1])[1]
    print(f'PV change vs SOM change p val: {pVal}')

    if pVal < 0.05:
        extraplots.significance_stars(xLocs[indBand], 0.98 * np.diff(yLim), 0.02 * np.diff(yLim), gapFactor=0.3)

    plt.plot([-10, 10], [0, 0], '--', color='0.5', zorder=0)  # line at 0 indicating direction of change

    axes.set_xlim(barLoc[0] - 0.3, barLoc[1] + 0.3)
    axes.set_xticks(barLoc)
    axes.set_ylim(yLim)

    extraplots.boxoff(axes)

# scatter plot comparing laser in and laser out data
def plot_exp_vs_control_scatter(axes, xData, yData, colours, xLim, yLim, facecolours='none'):
    plt.scatter(xData, yData, edgecolors=colours, facecolors=facecolours, s=(figparams.markerSize)**2)

    plt.plot([-100, 100], [0, 0], ':', c='0.5', zorder=-10)
    plt.plot([0, 0], [-100, 100], ':', c='0.5', zorder=-10)
    plt.plot([-100, 100], [-100, 100], ':', c='0.5', zorder=-10)

    axes.set_xlim(xLim)
    axes.set_ylim(yLim)
    axes.set(adjustable='box', aspect='equal')
    extraplots.boxoff(axes)
    extraplots.set_ticks_fontsize(axes, figparams.fontSizeTicks)


if __name__ == "__main__":
    mouse = 'band091'
    sessions = ['20200317a', '20200318a', '20200320a', '20200321a', '20200323a']

    reactionTimes, decisionTimes = get_reaction_times(mouse, sessions)
