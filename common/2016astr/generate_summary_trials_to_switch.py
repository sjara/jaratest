'''
Calculate how long it takes a mouse to switch.

Inspired by /zadorlab/data_analysis/201308XX_mice_vs_rats_paper/estimate_ntrials_to_switch.py
Used in Jaramillo and Zador (2014)
'''

import numpy as np
import scipy.optimize
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
import matplotlib
from matplotlib import pyplot as plt
import figparams

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

sessionsDict = {'adap020':['20160414a',
                           '20160419a',
                           '20160420a',
                           '20160423a',
                           '20160424a',
                           '20160425a',
                           '20160426a',
                           '20160427a',
                           '20160428a',
                           '20160430a',
                           '20160503a',
                           '20160504a',
                           '20160505a',
                           '20160506a',
                           '20160512a',
                           '20160519a',
                           '20160520a',
                           '20160521a',
                           '20160522a',
                           '20160524a',
                           '20160525a',
                           '20160526a',
                           '20160531a',
                           '20160601a',
                           '20160602a',
                           '20160603a',
                           '20160609a',
                           '20160610a',
                           '20160615a',
                       ],
                'test017':['20150226a',
                           '20150227a',
                           '20150309a',
                           '20150311a',
                           '20150313a',
                           '20150316a',
                       ],
                'test059':['20150617a',
                           '20150618a',
                           '20150619a',
                           '20150623a',
                           '20150625a',
                           '20150626a',
                           '20150628a',
                           '20150629a',
                           '20150630a',
                           '20150701a',
                       ],
                'test089':['20150729a',
                           #'20150731a', # This session has a manual block change at the end.
                           '20150801a',
                           '20150803a',
                           '20150804a',
                           '20150806a',
                           '20150807a',
                           '20150810a',
                           '20150811a',
                           '20150812a',
                           '20150814a',
                           '20150827a',
                           '20150828a',
                           '20150901a',
                           '20150902a',
                           '20150909a',
                           '20150910a',
                           '20150911a',
                           '20150913a',
                           '20150915a',
                           '20150918a',
                           '20150921a',
                           '20150923a',
                           '20150924a',
                           '20150925a',
                           '20151009a',
                           '20151207a',
                           '20151208a',
                           '20151210a',
                           '20151211a',
                           '20151213a',
                           '20151214a',
                           '20151222a',
                           '20160111a',
                           '20160112a',
                           '20160113a',
                           '20160114a',
                           '20160115a',
                           '20160116a',
                           '20160118a',
                           '20160120a',
                           '20160122a',
                           '20160123a',
                           '20160124a',
                           '20160125a',
                           '20160127a',
                           '20160128a',
                           '20160130a',
                           '20160202a',
                       ]
}

SAVE_FIGURE = 1
outputDir = '/tmp/'

# -- Functions for exponential fit --
def fixedintercept_exponential(xval,intercept,tau,amp=1):
    return amp*(1-np.exp(-(xval)/tau)) + intercept

def error_fixed_exponential(theta,xval,yval,intercept):
    yhat = fixedintercept_exponential(xval,intercept,*theta)
    return np.sum((yval-yhat)**2)

figFilename = 'supp_trials_to_switch'
figFormat = 'svg'
figSize = [7,7]

paradigm = '2afc'
#fontsize = 14
plt.clf()
plt.gcf().set_facecolor('w')

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.5]   # Horiz position for panel labels
labelPosY = [0.95, 0.5]

for inds,subject in enumerate(sessionsDict.iterkeys()):
    eachBehavData = []

    nTrialsToAnalyze = 140  # Number of trials after switch
    allCorrectMidFreqAfterSwitch = np.ma.masked_array(np.zeros((0,nTrialsToAnalyze)),dtype=int)

    for session in sessionsDict[subject]:
        behavFileName = loadbehavior.path_to_behavior_data(subject,paradigm,session)
        bdata = loadbehavior.FlexCategBehaviorData(behavFileName)
        bdata.find_trials_each_block()
        eachBehavData.append(bdata)

        # -- Estimate valid trial index within each block (index starts at 1) --    
        valid = bdata['valid']
        indexValidEachBlock = []
        for blockInd in range(bdata.blocks['nBlocks']):
            trialsThisBlock = bdata.blocks['trialsEachBlock'][:,blockInd]
            indexValidEachBlock.extend(np.cumsum(valid[trialsThisBlock]))
        bdata['indexValidEachBlock'] = np.array(indexValidEachBlock)

        # -- Get subset of trials (only valid) --
        valid = bdata['valid'].astype(bool)
        correct = bdata['outcome']==bdata.labels['outcome']['correct']
        correctSubset = correct[valid]
        indexEachBlockSubset = bdata['indexValidEachBlock'][valid]
        trialsMidFreq = bdata['targetFrequency']==bdata['midFreq']
        trialsMidFreqSubset = trialsMidFreq[valid]

        # -- Estimate performance of first N trials after switch --
        trialsPerBlock = bdata['trialsPerBlock']
        nSwitches = bdata.blocks['nBlocks']-1
        correctMidFreqAfterSwitch = np.ma.masked_array(np.zeros((nSwitches,nTrialsToAnalyze)),dtype=int)
        correctMidFreqAfterSwitch.mask = np.ones(correctMidFreqAfterSwitch.shape, dtype=bool)
        for indt in range(nTrialsToAnalyze):
            trialsToAnalyze = np.flatnonzero(indexEachBlockSubset==indt+1)[1:]
            midFreqAfterSwitch = trialsMidFreqSubset[trialsToAnalyze]
            if len(correctSubset[trialsToAnalyze]) == nSwitches:
                correctMidFreqAfterSwitch[:,indt] = correctSubset[trialsToAnalyze]
                correctMidFreqAfterSwitch.mask[:,indt] = ~midFreqAfterSwitch  # Unmask mid-freq trials
            else:
                correctMidFreqAfterSwitch[:-1,indt] = correctSubset[trialsToAnalyze]
                correctMidFreqAfterSwitch.mask[:-1,indt] = ~midFreqAfterSwitch  # Unmask mid-freq trials

        allCorrectMidFreqAfterSwitch = np.ma.vstack((allCorrectMidFreqAfterSwitch,
                                                     correctMidFreqAfterSwitch))

    avgCorrectAfterSwitch = allCorrectMidFreqAfterSwitch.mean(axis=0)

    if np.any(avgCorrectAfterSwitch.mask):
        raise Warning('At least one trial after switch has no data. Further calculation will not be accurate!')

    # -- Fit exponential --
    xval = np.arange(len(avgCorrectAfterSwitch),dtype=float)
    ### FIXME: filling may cause inaccuracies. See warning above.
    yMeasured = avgCorrectAfterSwitch.filled(0.5)
    intercept = 1-avgCorrectAfterSwitch[-10:].mean()

    theta0 = np.array([25.,1]) # NEW with fixed intercept
    thetahat = scipy.optimize.fmin(error_fixed_exponential,theta0,args=(xval,yMeasured,intercept),disp=False)
    yFit = fixedintercept_exponential(xval,intercept, *thetahat)

    firstTrialAboveChance = np.flatnonzero(yFit>0.5)[0] # Starting from trial zero

    print '{0}:  Tau={1:0.1f}   FirstTrialAboveChance={2}'.format(subject,thetahat[0],firstTrialAboveChance)

    mfactor = 100
    plt.subplot(2,2,inds+1)
    plt.hold(True)
    plt.plot(xval+1, mfactor*avgCorrectAfterSwitch, 'o-',
             color='0.75', mfc='w', mew=2, mec='0.75', clip_on=False)
    plt.plot(xval+1, mfactor*yFit, '-', lw=4, color='k')
    plt.axhline(mfactor*0.5, ls='--', color='0.5')
    plt.axvline(firstTrialAboveChance, ls='--',color='0.75')
    plt.xlabel('Trials after switch',fontsize=fontSizeLabels)
    plt.ylabel('Correct trials for\nreversing sound (%)',ma='center',fontsize=fontSizeLabels,labelpad=0.01)
    plt.ylim([0,mfactor*1])
    plt.yticks([0,50,100], fontsize=fontSizeTicks)
    extraplots.boxoff(plt.gca())
    plt.hold(False)
    plt.title(subject, fontsize=fontSizeLabels)

plt.tight_layout(pad=0.2, w_pad=1.5, h_pad=1.0, rect=(0.05,0.1,0.98,0.95))
plt.show()

plt.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.annotate('D', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
