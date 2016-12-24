'''
Script to generate the example psycurves under control and photostim conditions. Calculate and store the fraction hits at each frequency, use pysignifit for psycurve fitting and store the fitted curve.
Lan Guo 20161220 
'''

import numpy as np
import pypsignifit as psi
import os
from jaratoolbox import behavioranalysis


scriptFullPath = os.path.realpath(__file__)

# -- Example psycurve under photostim of left hemisphere -- #
animal = 'd1pi015'
session = '20160829a'

bdata = behavioranalysis.load_many_sessions(animal,[session])
targetFrequency=bdata['targetFrequency']
choice=bdata['choice']
valid=bdata['valid'] & (choice!=bdata.labels['choice']['none'])
choiceRight = choice==bdata.labels['choice']['right']

trialType = bdata['trialType']
stimTypes = [bdata.labels['trialType']['no_laser'],bdata.labels['trialType']['laser_left'],bdata.labels['trialType']['laser_right']]
stimLabels = ['no_laser','laser_left','laser_right']
trialsEachType = behavioranalysis.find_trials_each_type(trialType,stimTypes)
nStimTypes = len(stimTypes)

# -- Loop through control and photostim conditions -- #
psycurveDict = {}
for stimType in range(nStimTypes):
    if np.any(trialsEachType[:,stimType]):
        # -- Calculate and store psychometric curve points -- #
        targetFrequencyThisBlock = targetFrequency[trialsEachType[:,stimType]]    
        validThisBlock = valid[trialsEachType[:,stimType]]
        choiceRightThisBlock = choiceRight[trialsEachType[:,stimType]]
        (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
    behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)
        psycurveDict['possibleValues'] = possibleValues
        psycurveDict['fractionHitsEachValue_{}'.format(stimLabels[stimType])] = fractionHitsEachValue
        psycurveDict['ciHitsEachValue_{}'.format(stimLabels[stimType])] = ciHitsEachValue
        psycurveDict['nTrialsEachValue_{}'.format(stimLabels[stimType])] = nTrialsEachValue
        psycurveDict['nHitsEachValue_{}'.format(stimLabels[stimType])] = nHitsEachValue
        # -- Fit psycurve and store fitted values -- #
        constraints = None
        logPossibleValues = np.log2(possibleValues)
        data = np.c_[logPossibleValues,nHitsEachValue,nTrialsEachValue]
        # linear core 'ab': (x-a)/b; logistic sigmoid: 1/(1+np.exp(-(xval-alpha)/beta))
        psyCurveInference = psi.BootstrapInference(data,sample=False, sigmoid='logistic', core='ab',priors=constraints, nafc=1)
        xValues = logPossibleValues
        xRange = xValues[-1]-xValues[1]
        # Extrapolate fitted curve past the limit of logPossiblValues
        fitxval = np.linspace(xValues[0]-0.2*xRange,xValues[-1]+0.2*xRange,40)
        fityval = psyCurveInference.evaluate(x=fitxval)
        psycurveDict['logPossibleValues'] = logPossibleValues
        psycurveDict['fitxval_{}'.format(stimLabels[stimType])] = fitxval
        psycurveDict['fityval_{}'.format(stimLabels[stimType])] = fityval
        
        
outputDir = '/home/languo/data/mnt/figuresdata'
outputFile = 'example_photostim_psycurve_{0}_{1}.npz'.format(animal, session)
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, animal='d1pi015', session='20160829a', script=scriptFullPath,**psycurveDict)


# -- Example psycurve under photostim of right hemisphere -- #
animal = 'd1pi016'
session = '20160803a'

bdata = behavioranalysis.load_many_sessions(animal,[session])
targetFrequency=bdata['targetFrequency']
choice=bdata['choice']
valid=bdata['valid'] & (choice!=bdata.labels['choice']['none'])
choiceRight = choice==bdata.labels['choice']['right']

trialType = bdata['trialType']
stimTypes = [bdata.labels['trialType']['no_laser'],bdata.labels['trialType']['laser_left'],bdata.labels['trialType']['laser_right']]
stimLabels = ['no_laser','laser_left','laser_right']
trialsEachType = behavioranalysis.find_trials_each_type(trialType,stimTypes)
nStimTypes = len(stimTypes)

# -- Loop through control and photostim conditions -- #
psycurveDict = {}
for stimType in range(nStimTypes):
    if np.any(trialsEachType[:,stimType]):
        # -- Calculate and store psychometric curve points -- #
        targetFrequencyThisBlock = targetFrequency[trialsEachType[:,stimType]]    
        validThisBlock = valid[trialsEachType[:,stimType]]
        choiceRightThisBlock = choiceRight[trialsEachType[:,stimType]]
        (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
    behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)
        psycurveDict['possibleValues'] = possibleValues
        psycurveDict['fractionHitsEachValue_{}'.format(stimLabels[stimType])] = fractionHitsEachValue
        psycurveDict['ciHitsEachValue_{}'.format(stimLabels[stimType])] = ciHitsEachValue
        psycurveDict['nTrialsEachValue_{}'.format(stimLabels[stimType])] = nTrialsEachValue
        psycurveDict['nHitsEachValue_{}'.format(stimLabels[stimType])] = nHitsEachValue
        # -- Fit psycurve and store fitted values -- #
        constraints = None
        logPossibleValues = np.log2(possibleValues)
        data = np.c_[logPossibleValues,nHitsEachValue,nTrialsEachValue]
        # linear core 'ab': (x-a)/b; logistic sigmoid: 1/(1+np.exp(-(xval-alpha)/beta))
        psyCurveInference = psi.BootstrapInference(data,sample=False, sigmoid='logistic', core='ab',priors=constraints, nafc=1)
        xValues = logPossibleValues
        xRange = xValues[-1]-xValues[1]
        # Extrapolate fitted curve past the limit of logPossiblValues
        fitxval = np.linspace(xValues[0]-0.2*xRange,xValues[-1]+0.2*xRange,40)
        fityval = psyCurveInference.evaluate(x=fitxval)
        psycurveDict['logPossibleValues'] = logPossibleValues
        psycurveDict['fitxval_{}'.format(stimLabels[stimType])] = fitxval
        psycurveDict['fityval_{}'.format(stimLabels[stimType])] = fityval
        
        
outputDir = '/home/languo/data/mnt/figuresdata'
outputFile = 'example_photostim_psycurve_{0}_{1}.npz'.format(animal, session)
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, animal='d1pi016', session='20160803a',script=scriptFullPath, **psycurveDict)

