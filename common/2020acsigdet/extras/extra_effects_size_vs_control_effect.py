import sys
sys.path.append('..')
import os
import numpy as np
import pandas as pd
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import extraplots

import studyparams
import figparams
import behaviour_analysis_funcs as funcs

dbName = 'good_sessions.csv'
# dataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
dbPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
sessionDB = pd.read_csv(dbPath)

dbName = 'good_mice.csv'
# dataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
dbPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
mouseDB = pd.read_csv(dbPath)

mouseRow = mouseDB.query('strain=="PVChR2"')
PV_CHR2_MICE = mouseRow['mice'].apply(eval).iloc[-1]
mouseRow = mouseDB.query('strain=="PVArchT"')
PV_ARCHT_MICE = mouseRow['mice'].apply(eval).iloc[-1]
mouseRow = mouseDB.query('strain=="SOMArchT"')
SOM_ARCHT_MICE = mouseRow['mice'].apply(eval).iloc[-1]
mouseType = [PV_CHR2_MICE, PV_ARCHT_MICE, SOM_ARCHT_MICE]
trialType = ['laser', 'control']
laserPower = ['3mW', '10mW', '10mW']
legendLabels = ['PV activated', 'no PV', 'no SOM']

SAVE_FIGURE = 1
CIS = 0
outputDir = '/tmp/'
figFilename1 = 'FigX_effect_vs_control_effect'
figFilename2 = 'FigX_effect_size_vs_performance'
figFilename3 = 'FigX_effect_size_vs_accuracy'
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [12,3]  # In inches
figSize2 = [9,3]

ExcColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
colours = [PVColour, PVColour, SOMColour]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

# -- generate data for plots --

accuracies = []
dprimes = []
hitRates = []
FArates = []

for indMouseType, mice in enumerate(mouseType):

    thisAccuracies = None
    thisdprimes = None
    thisHitRates = None
    thisFArates = None

    for indMouse, mouse in enumerate(mice):
        for indSesType, sesType in enumerate(trialType):
            sessionTypeName = f'{laserPower[indMouseType]} {sesType}'

            dbRow = sessionDB.query('mouse==@mouse and sessionType==@sessionTypeName')
            laserSessions = dbRow['goodSessions'].apply(eval).iloc[-1]

            laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

            correct, incorrect, toneChoice, noiseChoice, trialsEachCond3Params, labels = funcs.get_trials(laserBehavData)

            numLasers = np.unique(laserBehavData['laserSide'])

            trialsEachLaser = behavioranalysis.find_trials_each_type(laserBehavData['laserSide'], numLasers)

            if thisAccuracies is None:
                thisAccuracies = np.zeros((len(trialType), len(mice), len(numLasers)))
                thisdprimes = np.zeros_like(thisAccuracies)
                thisHitRates = np.zeros_like(thisAccuracies)
                thisFArates = np.zeros_like(thisAccuracies)

            for indLaser in range(len(numLasers)):
                trialsThisLaser = trialsEachLaser[:,indLaser]
                # -- compute accuracy as percent correct trials out of all valid trials --
                thisCorrect = correct[trialsThisLaser]
                thisIncorrect = incorrect[trialsThisLaser]

                thisAccuracies[indSesType, indMouse, indLaser] = 100.0 * np.sum(thisCorrect) / (np.sum(thisCorrect) + np.sum(thisIncorrect))

                # -- compute hit rate, FA rate, and d prime --
                thisToneChoice = toneChoice[trialsThisLaser]
                thisNoiseChoice = noiseChoice[trialsThisLaser]

                toneTrials = np.sum(thisCorrect & thisToneChoice) + np.sum(thisIncorrect & thisNoiseChoice)
                noiseTrials = np.sum(thisCorrect & thisNoiseChoice) + np.sum(thisIncorrect & thisToneChoice)

                hitRate = np.sum(thisCorrect & thisToneChoice) / toneTrials
                FArate = np.sum(thisIncorrect & thisToneChoice) / noiseTrials

                thisHitRates[indSesType, indMouse, indLaser] = hitRate
                thisFArates[indSesType, indMouse, indLaser] = FArate
                thisdprimes[indSesType, indMouse, indLaser] = (stats.norm.ppf(hitRate) - stats.norm.ppf(FArate)) / np.sqrt(2)

    accuracies.append(thisAccuracies)
    hitRates.append(thisHitRates)
    FArates.append(thisFArates)
    dprimes.append(thisdprimes)

# -- make plots --
edgeColours = [PVColour, PVColour, SOMColour]
fillColours = [PVColour, 'white', 'white']
lineStyles = ['-', '--', '--']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 4)
gs.update(top=0.90, bottom=0.15, left=0.07, right=0.98, wspace=0.5, hspace=0.3)

# -- accuracy plot --
axAccuracy = plt.subplot(gs[0, 0])

lines = []
for indMouseType in range(len(mouseType)):
    expChange = accuracies[indMouseType][0,:,1] - accuracies[indMouseType][0,:,0]
    controlChange = accuracies[indMouseType][1,:,1] - accuracies[indMouseType][1,:,0]
    l1, = plt.plot(controlChange, expChange, 'o', mec=edgeColours[indMouseType], mfc=fillColours[indMouseType])
    lines.append(l1)

    yLim = [-17, 3]
    xLim = [-10, 10]

    # -- linear regression for each cell type --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange, expChange)
    xvals = np.linspace(xLim[0], xLim[1], 500)
    yvals = slope * xvals + intercept
    plt.plot(xvals, yvals, lineStyles[indMouseType], color=edgeColours[indMouseType], zorder=-1)

    plt.plot([-100, 100], [0, 0], ':', c='0.5', zorder=-10)
    plt.plot([0, 0], [-100, 100], ':', c='0.5', zorder=-10)
    plt.plot([-100, 100], [-100, 100], ':', c='0.5', zorder=-10)

    print(f'{legendLabels[indMouseType]} accuracy: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

axAccuracy.set_xlim(xLim)
axAccuracy.set_ylim(yLim)

plt.legend(lines, legendLabels, loc='best', fontsize=8)
axAccuracy.set_xlabel('laser-out change in accuracy')
axAccuracy.set_ylabel('laser-in change in accuracy')

extraplots.boxoff(axAccuracy)

# -- d' plot --
axdprime = plt.subplot(gs[0, 1])

lines = []
for indMouseType in range(len(mouseType)):
    expChange = dprimes[indMouseType][0,:,1] - dprimes[indMouseType][0,:,0]
    controlChange = dprimes[indMouseType][1,:,1] - dprimes[indMouseType][1,:,0]
    l1, = plt.plot(controlChange, expChange, 'o', mec=edgeColours[indMouseType], mfc=fillColours[indMouseType])
    lines.append(l1)

    lines.append(l1)

    yLim = [-0.7, 0.1]
    xLim = [-0.4, 0.3]

    # -- linear regression for each cell type --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange, expChange)
    xvals = np.linspace(xLim[0], xLim[1], 500)
    yvals = slope * xvals + intercept
    plt.plot(xvals, yvals, lineStyles[indMouseType], color=edgeColours[indMouseType], zorder=-1)

    plt.plot([-100, 100], [0, 0], ':', c='0.5', zorder=-10)
    plt.plot([0, 0], [-100, 100], ':', c='0.5', zorder=-10)
    plt.plot([-100, 100], [-100, 100], ':', c='0.5', zorder=-10)

    print(f'{legendLabels[indMouseType]} d\': \ncorrelation coefficient: {rVal} \np Val: {pVal}')

axdprime.set_xlim(xLim)
axdprime.set_ylim(yLim)

plt.legend(lines, legendLabels, loc='best', fontsize=8)
axdprime.set_xlabel('laser-out change in d\'')
axdprime.set_ylabel('laser-in change in d\'')

extraplots.boxoff(axdprime)

# -- hits plot --
axHits = plt.subplot(gs[0, 2])

lines = []
for indMouseType in range(len(mouseType)):
    expChange = hitRates[indMouseType][0,:,1] - hitRates[indMouseType][0,:,0]
    controlChange = hitRates[indMouseType][1,:,1] - hitRates[indMouseType][1,:,0]
    l1, = plt.plot(controlChange, expChange, 'o', mec=edgeColours[indMouseType], mfc=fillColours[indMouseType])
    lines.append(l1)

    yLim = [-0.7, 0.1]
    xLim = [-0.2, 0.2]

    # -- linear regression for each cell type --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange, expChange)
    xvals = np.linspace(xLim[0], xLim[1], 500)
    yvals = slope * xvals + intercept
    plt.plot(xvals, yvals, lineStyles[indMouseType], color=edgeColours[indMouseType], zorder=-1)

    plt.plot([-100, 100], [0, 0], ':', c='0.5', zorder=-10)
    plt.plot([0, 0], [-100, 100], ':', c='0.5', zorder=-10)
    plt.plot([-100, 100], [-100, 100], ':', c='0.5', zorder=-10)

    print(f'{legendLabels[indMouseType]} hit rate: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

axHits.set_xlim(xLim)
axHits.set_ylim(yLim)

plt.legend(lines, legendLabels, loc='best', fontsize=8)
axHits.set_xlabel('laser-out change in hit rate')
axHits.set_ylabel('laser-in change in hit rate')

extraplots.boxoff(axHits)

# -- FAs plot --
axFAs = plt.subplot(gs[0, 3])

lines = []
for indMouseType in range(len(mouseType)):
    expChange = FArates[indMouseType][0,:,1] - FArates[indMouseType][0,:,0]
    controlChange = FArates[indMouseType][1,:,1] - FArates[indMouseType][1,:,0]
    l1, = plt.plot(controlChange, expChange, 'o', mec=edgeColours[indMouseType], mfc=fillColours[indMouseType])
    lines.append(l1)

    yLim = [-0.4, 0.1]
    xLim = [-0.2, 0.2]

    # -- linear regression for each cell type --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange, expChange)
    xvals = np.linspace(xLim[0], xLim[1], 500)
    yvals = slope * xvals + intercept
    plt.plot(xvals, yvals, lineStyles[indMouseType], color=edgeColours[indMouseType], zorder=-1)

    plt.plot([-100, 100], [0, 0], ':', c='0.5', zorder=-10)
    plt.plot([0, 0], [-100, 100], ':', c='0.5', zorder=-10)
    plt.plot([-100, 100], [-100, 100], ':', c='0.5', zorder=-10)

    print(f'{legendLabels[indMouseType]} false alarm rate: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

axFAs.set_xlim(xLim)
axFAs.set_ylim(yLim)

plt.legend(lines, legendLabels, loc='best', fontsize=8)
axFAs.set_xlabel('laser-out change in FA rate')
axFAs.set_ylabel('laser-in change in FA rate')

extraplots.boxoff(axFAs)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename1, figFormat, figSize, outputDir)

# -- new figure: effect size vs performance (at same measure)
fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 4)
gs.update(top=0.90, bottom=0.15, left=0.07, right=0.98, wspace=0.5, hspace=0.3)

# -- accuracy plot --
axAccuracy = plt.subplot(gs[0, 0])

lines = []
for indMouseType in range(len(mouseType)):
    expChange = accuracies[indMouseType][0,:,1] - accuracies[indMouseType][0,:,0]
    expPerformance = accuracies[indMouseType][0,:,0]
    l1, = plt.plot(expPerformance, expChange, 'o', mec=edgeColours[indMouseType], mfc=fillColours[indMouseType])
    lines.append(l1)

    # -- linear regression for each cell type --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(expPerformance, expChange)
    xvals = np.linspace(50, 90, 500)
    yvals = slope * xvals + intercept
    plt.plot(xvals, yvals, lineStyles[indMouseType], color=edgeColours[indMouseType], zorder=-1)

    print(f'{legendLabels[indMouseType]} accuracy: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

plt.legend(lines, legendLabels, loc='best', fontsize=8)
axAccuracy.set_xlabel('Baseline accuracy')
axAccuracy.set_ylabel('Change in accuracy')

extraplots.boxoff(axAccuracy)

# -- d' plot --
axdprime = plt.subplot(gs[0, 1])

lines = []
for indMouseType in range(len(mouseType)):
    expChange = dprimes[indMouseType][0,:,1] - dprimes[indMouseType][0,:,0]
    expPerformance = dprimes[indMouseType][0,:,0]
    l1, = plt.plot(expPerformance, expChange, 'o', mec=edgeColours[indMouseType], mfc=fillColours[indMouseType])
    lines.append(l1)

    # -- linear regression for each cell type --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(expPerformance, expChange)
    xvals = np.linspace(0.3, 2, 200)
    yvals = slope * xvals + intercept
    plt.plot(xvals, yvals, lineStyles[indMouseType], color=edgeColours[indMouseType], zorder=-1)

    print(f'{legendLabels[indMouseType]} d\': \ncorrelation coefficient: {rVal} \np Val: {pVal}')

plt.legend(lines, legendLabels, loc='best', fontsize=8)
axdprime.set_xlabel('Baseline d\'')
axdprime.set_ylabel('Change in d\'')

extraplots.boxoff(axdprime)

# -- hits plot --
axHits = plt.subplot(gs[0, 2])

lines = []
for indMouseType in range(len(mouseType)):
    expChange = hitRates[indMouseType][0,:,1] - hitRates[indMouseType][0,:,0]
    expPerformance = hitRates[indMouseType][0,:,0]
    l1, = plt.plot(expPerformance, expChange, 'o', mec=edgeColours[indMouseType], mfc=fillColours[indMouseType])
    lines.append(l1)

    # -- linear regression for each cell type --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(expPerformance, expChange)
    xvals = np.linspace(0.4, 1.0, 200)
    yvals = slope * xvals + intercept
    plt.plot(xvals, yvals, lineStyles[indMouseType], color=edgeColours[indMouseType], zorder=-1)

    print(f'{legendLabels[indMouseType]} hit rate: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

plt.legend(lines, legendLabels, loc='best', fontsize=8)
axHits.set_xlabel('Baseline hit rate')
axHits.set_ylabel('Change in hit rate')

extraplots.boxoff(axHits)

# -- FAs plot --
axFAs = plt.subplot(gs[0, 3])

lines = []
for indMouseType in range(len(mouseType)):
    expChange = FArates[indMouseType][0,:,1] - FArates[indMouseType][0,:,0]
    expPerformance = FArates[indMouseType][0,:,0]
    l1, = plt.plot(expPerformance, expChange, 'o', mec=edgeColours[indMouseType], mfc=fillColours[indMouseType])
    lines.append(l1)

    # -- linear regression for each cell type --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(expPerformance, expChange)
    xvals = np.linspace(0.0, 0.8, 200)
    yvals = slope * xvals + intercept
    plt.plot(xvals, yvals, lineStyles[indMouseType], color=edgeColours[indMouseType], zorder=-1)

    print(f'{legendLabels[indMouseType]} FA rate: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

plt.legend(lines, legendLabels, loc='best', fontsize=8)
axFAs.set_xlabel('Baseline FA rate')
axFAs.set_ylabel('Change in FA rate')

extraplots.boxoff(axFAs)


# -- new figure: effect size at various measures vs accuracy
fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 3)
gs.update(top=0.90, bottom=0.15, left=0.07, right=0.98, wspace=0.5, hspace=0.3)

# -- d' plot --
axdprime = plt.subplot(gs[0, 0])

lines = []
for indMouseType in range(len(mouseType)):
    expChange = dprimes[indMouseType][0,:,1] - dprimes[indMouseType][0,:,0]
    expPerformance = accuracies[indMouseType][0,:,0]
    l1, = plt.plot(expPerformance, expChange, 'o', mec=edgeColours[indMouseType], mfc=fillColours[indMouseType])
    lines.append(l1)

    # -- linear regression for each cell type --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(expPerformance, expChange)
    xvals = np.linspace(50, 100, 200)
    yvals = slope * xvals + intercept
    plt.plot(xvals, yvals, lineStyles[indMouseType], color=edgeColours[indMouseType], zorder=-1)

    print(f'{legendLabels[indMouseType]} d\': \ncorrelation coefficient: {rVal} \np Val: {pVal}')

plt.legend(lines, legendLabels, loc='best', fontsize=8)
axdprime.set_xlabel('Baseline Accuracy (%)')
axdprime.set_ylabel('Change in d\'')

extraplots.boxoff(axdprime)

# -- hits plot --
axHits = plt.subplot(gs[0, 1])

lines = []
for indMouseType in range(len(mouseType)):
    expChange = hitRates[indMouseType][0,:,1] - hitRates[indMouseType][0,:,0]
    expPerformance = accuracies[indMouseType][0,:,0]
    l1, = plt.plot(expPerformance, expChange, 'o', mec=edgeColours[indMouseType], mfc=fillColours[indMouseType])
    lines.append(l1)

    # -- linear regression for each cell type --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(expPerformance, expChange)
    xvals = np.linspace(50, 100, 200)
    yvals = slope * xvals + intercept
    plt.plot(xvals, yvals, lineStyles[indMouseType], color=edgeColours[indMouseType], zorder=-1)

    print(f'{legendLabels[indMouseType]} hit rate: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

plt.legend(lines, legendLabels, loc='best', fontsize=8)
axHits.set_xlabel('Baseline Accuracy (%)')
axHits.set_ylabel('Change in hit rate')

extraplots.boxoff(axHits)

# -- FAs plot --
axFAs = plt.subplot(gs[0, 2])

lines = []
for indMouseType in range(len(mouseType)):
    expChange = FArates[indMouseType][0,:,1] - FArates[indMouseType][0,:,0]
    expPerformance = accuracies[indMouseType][0,:,0]
    l1, = plt.plot(expPerformance, expChange, 'o', mec=edgeColours[indMouseType], mfc=fillColours[indMouseType])
    lines.append(l1)

    # -- linear regression for each cell type --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(expPerformance, expChange)
    xvals = np.linspace(50, 100, 200)
    yvals = slope * xvals + intercept
    plt.plot(xvals, yvals, lineStyles[indMouseType], color=edgeColours[indMouseType], zorder=-1)

    print(f'{legendLabels[indMouseType]} FA rate: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

plt.legend(lines, legendLabels, loc='best', fontsize=8)
axFAs.set_xlabel('Baseline Accuracy (%)')
axFAs.set_ylabel('Change in FA rate')

extraplots.boxoff(axFAs)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename3, figFormat, figSize2, outputDir)