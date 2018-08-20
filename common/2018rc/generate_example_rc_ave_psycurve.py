'''
Generate average psycurve for reward change task for select animals.
'''
import os
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
import figparams
import pypsignifit as psi
import numpy as np
from reward_change_sessions import animals

FIGNAME = 'reward_change_behavior'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

scriptFullPath = os.path.realpath(__file__)

numSessionsToInclude = 6
blockLabels = ['more_left','more_right'] #['same_reward','more_left','more_right']
animalsUsed = ['adap012', 'adap071', 'gosi008']
#resultsDict = {}
for indA,animalName in enumerate(animalsUsed):
    psycurveDict = {}
    sessions = animals[animalName][:numSessionsToInclude]
    allBehavDataThisAnimal = behavioranalysis.load_many_sessions(animalName,sessions)
    targetFrequency = allBehavDataThisAnimal['targetFrequency']
    currentBlock = allBehavDataThisAnimal['currentBlock']
    blockTypes = [allBehavDataThisAnimal.labels['currentBlock'][blockLabel] for blockLabel in blockLabels]
    trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
    choice = allBehavDataThisAnimal['choice']
    valid = allBehavDataThisAnimal['valid']& (choice!=allBehavDataThisAnimal.labels['choice']['none'])
    choiceRight = choice==allBehavDataThisAnimal.labels['choice']['right'] 
    nBlocks = len(blockTypes)
    nFreqs = len(np.unique(targetFrequency))
    possibleValues = np.unique(targetFrequency)
    psycurveDict['possibleFreqs'] = possibleValues
    logPossibleValues = np.log2(possibleValues)
    psycurveDict['logPossibleFreqs'] = logPossibleValues
    psycurveDict['fractionHitsEachBlockEachFreq'] = np.empty((nBlocks,nFreqs))
    psycurveDict['ciHitsEachBlockEachFreq'] = np.empty((nBlocks,2,nFreqs))
    psycurveDict['nTrialsEachBlockEachFreq'] = np.empty((nBlocks,nFreqs))
    psycurveDict['nHitsEachBlockEachFreq'] = np.empty((nBlocks,nFreqs))
    psycurveDict['fitxval'] = np.empty((nBlocks,40))
    psycurveDict['fityval'] = np.empty((nBlocks,40))

    for blockType in range(nBlocks):
        if np.any(trialsEachType[:,blockType]):
            targetFrequencyThisBlock = targetFrequency[trialsEachType[:,blockType]]    
            validThisBlock = valid[trialsEachType[:,blockType]]
            choiceRightThisBlock = choiceRight[trialsEachType[:,blockType]]
            (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)

            psycurveDict['fractionHitsEachBlockEachFreq'][blockType,:] = fractionHitsEachValue
            psycurveDict['ciHitsEachBlockEachFreq'][blockType,:,:] = ciHitsEachValue
            psycurveDict['nTrialsEachBlockEachFreq'][blockType,:] = nTrialsEachValue
            psycurveDict['nHitsEachBlockEachFreq'][blockType,:] = nHitsEachValue
            # -- Fit psycurve and store fitted values -- #
            lowerFreqConstraint = logPossibleValues[0]
            upperFreqConstraint = logPossibleValues[-1]
            constraints = ( 'Uniform({}, {})'.format(lowerFreqConstraint, upperFreqConstraint),
                            'Uniform(0,5)' ,
                            'Uniform(0,1)',
                            'Uniform(0,1)')
            data = np.c_[logPossibleValues,nHitsEachValue,nTrialsEachValue]
            # linear core 'ab': (x-a)/b; logistic sigmoid: 1/(1+np.exp(-(xval-alpha)/beta))
            psyCurveInference = psi.BootstrapInference(data,sample=False, sigmoid='logistic', core='ab',priors=constraints, nafc=1)
            xValues = logPossibleValues
            xRange = xValues[-1]-xValues[1]
            # Extrapolate fitted curve past the limit of logPossiblValues
            fitxval = np.linspace(xValues[0]-0.2*xRange,xValues[-1]+0.2*xRange,40)
            fityval = psyCurveInference.evaluate(x=fitxval)
            psycurveDict['fitxval'][blockType,:] = fitxval
            psycurveDict['fityval'][blockType,:] = fityval

        else:
            fractionHitsEachBlockEachFreq[blockType,:] = np.NaN
            ciHitsEachBlockEachFreq[blockType,:] = np.NaN
            nTrialsEachBlockEachFreq[blockType,:] = np.NaN
            nHitsEachBlockEachFreq[blockType,:] = np.Nan

    outputFilename = 'example_rc_ave_pycurve_{}.npz'.format(animalName)
    outputFullPath = os.path.join(outputDir, outputFilename)
    np.savez(outputFullPath, animalsUsed=animalsUsed, numSessionsToInclude=numSessionsToInclude, blockLabels=blockLabels, script=scriptFullPath, **psycurveDict)
