

#%%
import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import extrastats
from statsmodels.stats import proportion
from jaratest.nick.behavior import soundtypes

import pandas as pd


dataDir = '/home/nick/data/dissertation_amod/'

# amod002 and 003 ran with chords and AM sounds
# subject = 'amod002'
subjects = ['amod002', 'amod003']
soundTypes = ['chords', 'amp_mod']

sessions = ['20160412a', '20160413a', '20160414a', '20160415a', '20160416a',
               '20160417a', '20160418a', '20160419a', '20160420a', '20160421a']
muscimol = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]


# amod004 ran with tones and AM sounds
# subject = 'amod004'
# soundTypes = ['tones', 'amp_mod']

fontSizeLegend = 8
fontSizeLabels = 14
fontSizeTicks = 10
fontSizeAxes = 10
ylabelPad = -0.1
errlw = 2

labelPosX =  [0.05, 0.35, 0.66]
labelPosY = [0.92, 0.47]

gs = gridspec.GridSpec(2, 3)
gs.update(wspace=0.4, hspace=0.4)


plt.clf()
for indSubject, subject in enumerate(subjects):

    axSummary = plt.subplot(gs[indSubject, 2])

    #Collect percent correct information
    allnCorr = []
    allnVal = []
    allfracCorr = []

    sessionInd = []
    animalInd = []
    soundType = []
    muscimolInjected = []
    for indSession, session in enumerate(sessions):
        (bdataObjs, bdataSoundTypes) = soundtypes.load_behavior_sessions_sound_type(subject, [session])
        for st in [0, 1]: #0 = mod, 1=chord
            bdata = bdataObjs[st]
            nCorr = sum(bdata['outcome']==bdata.labels['outcome']['correct'])
            nVal = sum(bdata['valid'])
            allfracCorr.append(float(nCorr)/nVal)
            allnCorr.append(nCorr)
            allnVal.append(nVal)
            sessionInd.append(indSession)
            animalInd.append(indSubject)
            soundType.append(st)
            muscimolInjected.append(muscimol[indSession])

        nCorr = allnCorr
        nIncorr = np.array(allnVal) - np.array(allnCorr)
        data = pd.DataFrame({'nCorr':np.array(nCorr),
                            'nIncorr':np.array(nIncorr),
                            'soundType':np.array(soundType),
                            'muscimolInjected':np.array(muscimolInjected),
                            'sessionInd':np.array(sessionInd)})

    nCorrMusAM = np.mean(data.query('muscimolInjected==1 and soundType==0')['nCorr'])
    nIncorrMusAM = np.mean(data.query('muscimolInjected==1 and soundType==0')['nIncorr'])
    percentCorrectMusAM = nCorrMusAM.astype(float) / (nCorrMusAM + nIncorrMusAM)
    ciMusAM = np.array(proportion.proportion_confint(nCorrMusAM,
        nCorrMusAM + nIncorrMusAM,
        method = 'wilson'))
    lowerMusAM = percentCorrectMusAM - ciMusAM[0]
    upperMusAM = ciMusAM[1] - percentCorrectMusAM

    # Saline AM group
    nCorrSalAM = np.mean(data.query('muscimolInjected==0 and soundType==0')['nCorr'])
    nIncorrSalAM = np.mean(data.query('muscimolInjected==0 and soundType==0')['nIncorr'])
    percentCorrectSalAM = nCorrSalAM.astype(float) / (nCorrSalAM + nIncorrSalAM)
    ciSalAM = np.array(proportion.proportion_confint(nCorrSalAM,
        nCorrSalAM + nIncorrSalAM,
        method = 'wilson'))
    lowerSalAM = percentCorrectSalAM - ciSalAM[0]
    upperSalAM = ciSalAM[1] - percentCorrectSalAM

    # Muscimol Chords group
    nCorrMusChords = np.mean(data.query('muscimolInjected==1 and soundType==1')['nCorr'])
    nIncorrMusChords = np.mean(data.query('muscimolInjected==1 and soundType==1')['nIncorr'])
    percentCorrectMusChords = nCorrMusChords.astype(float) / (nCorrMusChords + nIncorrMusChords)
    ciMusChords = np.array(proportion.proportion_confint(nCorrMusChords,
        nCorrMusChords + nIncorrMusChords,
        method = 'wilson'))
    lowerMusChords = percentCorrectMusChords - ciMusChords[0]
    upperMusChords = ciMusChords[1] - percentCorrectMusChords

    # Saline Chords group
    nCorrSalChords = np.mean(data.query('muscimolInjected==0 and soundType==1')['nCorr'])
    nIncorrSalChords = np.mean(data.query('muscimolInjected==0 and soundType==1')['nIncorr'])
    percentCorrectSalChords = nCorrSalChords.astype(float) / (nCorrSalChords + nIncorrSalChords)
    ciSalChords = np.array(proportion.proportion_confint(nCorrSalChords,
        nCorrSalChords + nIncorrSalChords,
        method = 'wilson'))
    lowerSalChords = percentCorrectSalChords - ciSalChords[0]
    upperSalChords = ciSalChords[1] - percentCorrectSalChords

    # Lower and upper confidence intervals for the errorbar command
    lowerAM = [lowerSalAM, lowerMusAM]
    upperAM = [upperSalAM, upperMusAM]
    lowerChords = [lowerSalChords, lowerMusChords]
    upperChords = [upperSalChords, upperMusChords]

    axSummary.errorbar(x=[0,1], y=[percentCorrectSalAM, percentCorrectMusAM],
                yerr=[lowerAM, upperAM], ls='-', label='AM', color='k',
                lw=errlw)
    
    axSummary.errorbar(x=[0,1], y=[percentCorrectSalChords, percentCorrectMusChords],
                yerr=[lowerChords, upperChords], ls='--', label='Frequency', color='k',
                lw=errlw)
    plt.legend(frameon=False, fontsize = fontSizeLegend)
    axSummary.set_yticks([0.5, 0.75, 1])
    axSummary.set_ylim([0.45, 1.05])
    axSummary.set_yticklabels(['50', '75', '100'])
    axSummary.set_ylabel('Correct choice (%)', fontsize=fontSizeAxes, labelpad=ylabelPad)
    axSummary.set_xlabel('Injection', fontsize=fontSizeAxes)
    axSummary.set_xticks([0, 1])
    axSummary.set_xticklabels(['Saline', 'Muscimol'])
    axSummary.set_xlim([-0.25, 1.25])
    extraplots.boxoff(axSummary)
    extraplots.set_ticks_fontsize(axSummary, fontSizeTicks)
    #plt.title(subject)


    # Plot psychometrics
    for indSt, stype in enumerate(soundTypes):

        ax1 = plt.subplot(gs[indSubject, indSt])

        musFilename = 'psychometric_{}_{}_muscimol.npz'.format(subject, stype)
        musFullPath = os.path.join(dataDir,musFilename)
        musData = np.load(musFullPath)

        salFilename = 'psychometric_{}_{}_saline.npz'.format(subject, stype)
        salFullPath = os.path.join(dataDir,salFilename)
        salData = np.load(salFullPath)

        dataToPlot = [musData, salData]
        curveColors = ['r', 'k']
        plotHandles = []


        for indCond, condData in enumerate(dataToPlot):

            color = curveColors[indCond]

            logPossibleValues = condData['logPossibleValues']
            estimate = condData['estimate']
            ciHitsEachValue = condData['ciHitsEachValue']
            fractionHitsEachValue = condData['fractionHitsEachValue']
            possibleValues = condData['possibleValues']

            xRange = logPossibleValues[-1]-logPossibleValues[1]

            fitxvals = np.linspace(logPossibleValues[0]-0.1*xRange,logPossibleValues[-1]+0.1*xRange,40)
            fityvals = extrastats.psychfun(fitxvals, *estimate)

            upperWhisker = ciHitsEachValue[1,:]-fractionHitsEachValue
            lowerWhisker = fractionHitsEachValue-ciHitsEachValue[0,:]

            # ax1.hold(True)
            (pline, pcaps, pbars) = ax1.errorbar(logPossibleValues,
                                                    100*fractionHitsEachValue,
                                                    yerr = [100*lowerWhisker, 100*upperWhisker],
                                                    ecolor=color, fmt=None, clip_on=False)

            pdots = ax1.plot(logPossibleValues, 100*fractionHitsEachValue, 'o', ms=6, mec='None', mfc=color,
                            clip_on=False)

            #ax1.set_xticks(logPossibleValues)
            #freqLabels = ['{:.03}'.format(x) for x in possibleValues/1000.0]
            #ax1.set_xticklabels(freqLabels)
            #ax1.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels, fontsize=fontSizeAxes)

            pfit, = ax1.plot(fitxvals, 100*fityvals, color=color, lw=2, clip_on=False)
            plotHandles.append(pfit)

        # ax1.annotate('B', xy=(labelPosX[0],labelPosY[0]), xycoords='axes fraction',
        #                 fontsize=fontSizePanel, fontweight='bold')

        extraplots.boxoff(ax1)

        xticks = ax1.get_xticks()
        newXtickLabels = np.logspace(logPossibleValues[0], logPossibleValues[-1], 3, base=2)
        # 1/0
        ax1.set_xticks(np.log2(np.array(newXtickLabels)))
        if not stype=='amp_mod':
            ax1.set_xticklabels(['{:.3}'.format(x/1000.0) for x in newXtickLabels])
            ax1.set_xlabel('Frequency (kHz)', fontsize=fontSizeAxes)
            #if indSubject = 0:
                #ax1.set_title(stype.capitalize())
                #ax1.set_title(stype.capitalize())
        else:
            ax1.set_xticklabels(['{:.3}'.format(x) for x in newXtickLabels])
            ax1.set_xlabel('AM Rate (Hz)', fontsize=fontSizeAxes)
            #if indSubject = 0:
                #ax1.set_title("AM")

        # ax1.set_xlim([fitxvals[0],fitxvals[-1]])

        ax1.set_ylim([0, 100])
        ax1.set_ylabel('Rightward trials (%)', fontsize=fontSizeAxes, labelpad=ylabelPad)
        extraplots.set_ticks_fontsize(ax1,fontSizeTicks)
        ax1.set_yticks([0, 50, 100])

        leg = ax1.legend([plotHandles[1],plotHandles[0]], ['Saline','Muscimol'], loc='upper left', frameon=False,
                            labelspacing=0.1, handlelength=1.5, handletextpad=0.2, borderaxespad=0.1, fontsize=fontSizeLegend)

fig = plt.gcf()

plt.text(x=labelPosX[0], y=labelPosY[0],
s='A', fontsize=fontSizeLabels, transform=fig.transFigure,
fontweight='bold')

plt.text(x=labelPosX[1], y=labelPosY[0],
s='B', fontsize=fontSizeLabels, transform=fig.transFigure,
fontweight='bold')

plt.text(x=labelPosX[2], y=labelPosY[0],
s='C', fontsize=fontSizeLabels, transform=fig.transFigure,
fontweight='bold')

plt.text(x=labelPosX[0], y=labelPosY[1],
s='D', fontsize=fontSizeLabels, transform=fig.transFigure,
fontweight='bold')

plt.text(x=labelPosX[1], y=labelPosY[1],
s='E', fontsize=fontSizeLabels, transform=fig.transFigure,
fontweight='bold')

plt.text(x=labelPosX[2], y=labelPosY[1],
s='F', fontsize=fontSizeLabels, transform=fig.transFigure,
fontweight='bold')

fig.set_size_inches(10, 5)
plt.show()
plt.savefig('/home/nick/dissertation/figures/chapter4/figure_main_amod_effect.pdf')
#%%
