"""
Show psychometric for freely-moving mice (FM discrimination task).
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
from jaratoolbox import settings 


subjects = ['frem002','frem003','frem005']  # 003, 005
sessions = ['20211012a','20211013a','20211014a','20211015a',
            '20211016a','20211017a','20211018a','20211019a']
paradigm = '2afc'

fontSizeLabels = 12

for subject in subjects:
    fig0 = plt.gcf()
    fig0.clf()
    gs0 = gridspec.GridSpec(1,1, left=0.15, right=0.98, bottom=0.15, wspace=0.25)

    try:
        bdata = behavioranalysis.load_many_sessions(subject,paradigm=paradigm,sessions=sessions)
    except UnboundLocalError:
        continue

    nSessions = bdata['sessionID'][-1]

    validTrials = bdata['valid'].astype(bool)
    correctTrials = bdata['outcome']==bdata.labels['outcome']['correct']
    rightwardChoice = bdata['choice']==bdata.labels['choice']['right']

    targetParamValue = bdata['targetFMslope']
    possibleParamValue = np.unique(targetParamValue)
    nParamValues = len(possibleParamValue)

    (possibleValues, fractionHitsEachValue, ciHitsEachValue, nTrialsEachValue, nHitsEachValue)=\
        behavioranalysis.calculate_psychometric(rightwardChoice, targetParamValue, validTrials)


    #plt.subplot(1,3,indsub+1)
    plotColor = '#1f77b4'  #[0.2,0.2,1]
    ax0 = fig0.add_subplot(gs0[0,0])
    xTicks = np.arange(-1, 1.2, 0.2)
    (pline, pcaps, pbars, pdots) = \
        extraplots.plot_psychometric(possibleValues,fractionHitsEachValue,
                                     ciHitsEachValue, xTicks=xTicks, xscale='linear')
    plt.setp([pline, pcaps, pbars, pdots], color=plotColor)
    plt.setp(pdots,mfc=plotColor)
    plt.axhline(y=50, color='0.85', ls='--')
    #plt.minorticks_off()
    plt.ylim([-5,105])
    plt.ylabel('Rightward choice (%)', fontsize=fontSizeLabels)
    plt.xlabel('FM slope (A.U.)', fontsize=fontSizeLabels)
    sessionStr = '{} - {}'.format(sessions[0],sessions[-1])
    titleStr = f'{subject}: {sessionStr}'
    plt.title(titleStr, fontsize=fontSizeLabels, fontweight='bold')
    extraplots.boxoff(ax0)
    plt.pause(0.01)
    plt.show()
    input('Press ENTER to see next plot')
    #print('Click on figure to see next plot.'); plt.waitforbuttonpress();
    #sys.exit()

    if 0:
        format = 'png'
        filename = '{}_{}_psycurve'.format(subject,sessions[0])
        extraplots.save_figure(filename, format, [6,5], '/tmp/', facecolor='w')

