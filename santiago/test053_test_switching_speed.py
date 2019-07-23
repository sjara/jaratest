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
from matplotlib import pyplot as plt


sessionsDict = {
                'test017':['20150226a',
                           '20150227a',
                           '20150309a',
                           '20150311a',
                           '20150313a',
                           '20150316a',
                       ],
}


'''
subject = 'test017'
loadingClass = loadbehavior.FlexCategBehaviorData
allBehavData = behavioranalysis.load_many_sessions(subject, sessionsDict[subject],
                                                   loadingClass=loadingClass)
'''

subject = 'test017'
paradigm = '2afc'
eachBehavData = []

nTrialsToAnalyze = 150  # Number of trials after switch
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

plt.clf()
plt.plot(avgCorrectAfterSwitch,'.-')
plt.show()


# -- Functions for exponential fit --
def fixedintercept_exponential(xval,intercept,tau,amp=1):
    return amp*(1-np.exp(-(xval)/tau)) + intercept

def error_fixed_exponential(theta,xval,yval,intercept):
    yhat = fixedintercept_exponential(xval,intercept,*theta)
    return np.sum((yval-yhat)**2)

# -- Fit exponential --
xval = np.arange(len(avgCorrectAfterSwitch),dtype=float)
### FIXME: filling may cause inaccuracies. See warning above.
yMeasured = avgCorrectAfterSwitch.filled(0.5)
#intercept = avgCorrectAfterSwitch[:3].mean()
intercept = 1-avgCorrectAfterSwitch[-10:].mean()

theta0 = np.array([25.,1]) # NEW with fixed intercept
thetahat = scipy.optimize.fmin(error_fixed_exponential,theta0,args=(xval,yMeasured,intercept),disp=False)
yFit = fixedintercept_exponential(xval,intercept, *thetahat)

firstTrialAboveChance = np.flatnonzero(yFit>0.5)[0] # Starting from trial zero

print 'Tau={0:0.1f}   FirstTrialAboveChance={1}'.format(thetahat[0],firstTrialAboveChance)

mfactor = 100
fontsize = 14
plt.clf()
plt.gcf().set_facecolor('w')
plt.plot(xval+1, mfactor*avgCorrectAfterSwitch, 'o-',
         color='0.75', mfc='w', mew=2, mec='0.75', clip_on=False)
plt.plot(xval+1, mfactor*yFit, '-', lw=4, color='k')
plt.axhline(mfactor*0.5, ls='--', color='0.5')
plt.axvline(firstTrialAboveChance, ls='--',color='0.75')
plt.xlabel('Trials after switch',fontsize=fontsize)
plt.ylabel('Correct trials for\nreversing sound (%)',ma='center',fontsize=fontsize)
plt.ylim([0,mfactor*1])
extraplots.boxoff(plt.gca())
plt.title(subject)
plt.show()

