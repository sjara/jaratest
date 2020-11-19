import os
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots
from jaratoolbox import settings

import studyparams
import figparams

def load_data_for_this_stuff(mouse, sessionType):
    sessions = studyparams.miceDict[mouse][sessionType]
    behavData = behavioranalysis.load_many_sessions(mouse, sessions)

    numLasers = np.unique(behavData['laserSide'])
    numBands = np.unique(behavData['currentBand'])

    trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['laserSide'], numLasers,
                                                                   behavData['currentBand'], numBands)
    trialsEachLaser = behavioranalysis.find_trials_each_type(behavData['laserSide'], numLasers)

    valid = behavData['valid'].astype(bool)
    correct = behavData['outcome'] == behavData.labels['outcome']['correct']

    leftChoice = behavData['choice'] == behavData.labels['choice']['left']
    rightChoice = behavData['choice'] == behavData.labels['choice']['right']

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

    return trialsEachCond, trialsEachLaser, valid, correct, toneChoice, noiseChoice, numBands


PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
SOM_ARCHT_MICE = studyparams.SOM_ARCHT_MICE

mouseTypes = [PV_ARCHT_MICE, SOM_ARCHT_MICE]

baseColour = figparams.colp['baseline']
controlColour = figparams.colp['control']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
connectColour = figparams.colp['connectLine']
colours = [PVColour, SOMColour]

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 2)
gs.update(top=0.98, bottom=0.10, left=0.14, right=0.99, wspace=0.4, hspace=0.3)

for indType, mice in enumerate(mouseTypes):
    changeAccuracy = None
    changeBias = None
    sessionTypes = ['10mW control', '10mW laser']

    for indMouse, mouse in enumerate(mice):
        for indSession, sessionType in enumerate(sessionTypes):
            trialsEachCond, trialsEachLaser, valid, correct, toneChoice, noiseChoice, numBands = load_data_for_this_stuff(mouse, sessionType)

            # -- compute accuracies and bias for each bandwidth in both control and experimental condition --
            for indBand in range(len(numBands)):
                trialsEachLaser = trialsEachCond[:, :, indBand]

                # -- sort trials by laser presentation, compute accuracy as percent correct trials out of all valid trials --
                laserValid = valid[trialsEachLaser[:, 1]]
                laserCorrect = correct[trialsEachLaser[:, 1]]
                thisLaserAccuracy = 100.0 * np.sum(laserCorrect) / np.sum(laserValid)

                controlValid = valid[trialsEachLaser[:, 0]]
                controlCorrect = correct[trialsEachLaser[:, 0]]
                thisControlAccuracy = 100.0 * np.sum(controlCorrect) / np.sum(controlValid)

                if changeAccuracy is None:
                    changeAccuracy = np.zeros((2, len(mice), len(numBands)))
                changeAccuracy[indSession, indMouse, indBand] = thisLaserAccuracy - thisControlAccuracy
                # -- compute bias to a side as difference/sum --
                laserToneChoice = toneChoice[trialsEachLaser[:, 1]]
                laserNoiseChoice = noiseChoice[trialsEachLaser[:, 1]]
                thisLaserBias = 1.0 * (np.sum(laserToneChoice) - np.sum(laserNoiseChoice)) / (np.sum(laserToneChoice) + np.sum(laserNoiseChoice))

                controlToneChoice = toneChoice[trialsEachLaser[:, 0]]
                controlNoiseChoice = noiseChoice[trialsEachLaser[:, 0]]
                thisControlBias = 1.0 * (np.sum(controlToneChoice) - np.sum(controlNoiseChoice)) / (np.sum(controlToneChoice) + np.sum(controlNoiseChoice))

                if changeBias is None:
                    changeBias = np.zeros((2, len(mice), len(numBands)))
                changeBias[indSession, indMouse, indBand] = thisLaserBias - thisControlBias

    axAccuracy = plt.subplot(gs[indType, 0])

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(numBands))
    accyLims = [(-10, 5), (-15, 5)]
    xTickLabels = numBands
    legendLabels = ['no laser', 'laser']

    for indBand, band in enumerate(numBands):
        thisxLocs = barLoc + xLocs[indBand]

        for indMouse in range(changeAccuracy.shape[1]):
            plt.plot(thisxLocs, [changeAccuracy[0,indMouse,indBand], changeAccuracy[1,indMouse,indBand]], '-', color=connectColour)
        plt.plot(np.tile(thisxLocs[0], changeAccuracy.shape[1]), changeAccuracy[0,:,indBand], 'o', color=controlColour)
        plt.plot(np.tile(thisxLocs[1], changeAccuracy.shape[1]), changeAccuracy[1,:,indBand], 'o', mec=colours[indType], mfc='white')

        plt.plot([thisxLocs[0]-0.1, thisxLocs[0]+0.1], np.tile(np.median(changeAccuracy[0,:,indBand]),2), '-', color='k', lw=3)
        plt.plot([thisxLocs[1] - 0.1, thisxLocs[1] + 0.1], np.tile(np.median(changeAccuracy[1,:,indBand]), 2), '-', color='k', lw=3)

        axAccuracy.set_xlim(-0.5, 1.5)
        axAccuracy.set_xticks(xLocs)
        axAccuracy.set_xticklabels(numBands)
        axAccuracy.set_xlabel('Bandwidth (octaves)')

        axAccuracy.set_ylim(accyLims[indType])
        axAccuracy.set_ylabel('Change in accuracy (%)')

        extraplots.boxoff(axAccuracy)

        pVal = stats.ranksums(changeAccuracy[0,:,indBand], changeAccuracy[1,:,indBand])[1]
        print(f"Control vs inactivation change in accuracy at {band} octaves p val = {pVal}")
        if pVal < 0.05:
            extraplots.significance_stars(thisxLocs, 0.98 * accyLims[indType][1], 0.03 * np.diff(accyLims[indType]), gapFactor=0.2)


    axBias = plt.subplot(gs[indType, 1])
    biasyLims = [(-0.3, 0.3), (-0.5, 0.1)]

    for indBand, band in enumerate(numBands):
        thisxLocs = barLoc + xLocs[indBand]

        for indMouse in range(changeBias.shape[1]):
            plt.plot(thisxLocs, [changeBias[0, indMouse, indBand], changeBias[1, indMouse, indBand]], '-',
                     color=connectColour)
        plt.plot(np.tile(thisxLocs[0], changeBias.shape[1]), changeBias[0, :, indBand], 'o',
                 color=controlColour)
        plt.plot(np.tile(thisxLocs[1], changeBias.shape[1]), changeBias[1, :, indBand], 'o',
                 mec=colours[indType], mfc='white')

        plt.plot([thisxLocs[0] - 0.1, thisxLocs[0] + 0.1], np.tile(np.median(changeBias[0, :, indBand]), 2),
                 '-', color='k', lw=3)
        plt.plot([thisxLocs[1] - 0.1, thisxLocs[1] + 0.1], np.tile(np.median(changeBias[1, :, indBand]), 2),
                 '-', color='k', lw=3)

        axBias.set_xlim(-0.5, 1.5)
        axBias.set_xticks(xLocs)
        axBias.set_xticklabels(numBands)
        axBias.set_xlabel('Bandwidth (octaves)')

        axBias.set_ylim(biasyLims[indType])
        axBias.set_ylabel('Change in bias')

        extraplots.boxoff(axBias)

        pVal = stats.ranksums(changeBias[0, :, indBand], changeBias[1, :, indBand])[1]
        print(f"Control vs inactivation change in bias at {band} octaves p val = {pVal}")
        if pVal < 0.05:
            extraplots.significance_stars(thisxLocs, 0.98 * biasyLims[indType][1], 0.03 * np.diff(biasyLims[indType]),
                                          gapFactor=0.2)

extraplots.save_figure('Inhib_inactivation_by_bandwidth', 'pdf', [5,5], '/tmp/')