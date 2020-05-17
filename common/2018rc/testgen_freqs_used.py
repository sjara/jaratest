'''
Generate intermediate data for plotting reward change behavior summary: 
percent rightward choice for each animal in left_more reward vs right_more reward condition
for the extreme freqs and middle freqs.
'''
import os
#import pypsignifit as psi
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
import figparams
import numpy as np
from reward_change_sessions import animals

scriptFullPath = os.path.realpath(__file__)

numSessionsToInclude = 6
numFreqs = 9
blockLabels = ['same_reward','more_left','more_right'] #['same_reward','more_left','more_right']
animalsUsed = [animalName for animalName in sorted(animals.keys())]
resultAllAnimals = np.empty((len(blockLabels), numFreqs, len(animalsUsed)))
freqsAllAnimals = np.empty((numFreqs, len(animalsUsed)))

for indA,animalName in enumerate(animalsUsed):
    sessions = animals[animalName][:numSessionsToInclude]
    resultThisAnimal = np.empty((len(blockLabels), numFreqs))
    #for indS,session in enumerate(sessions):
    bdata = behavioranalysis.load_many_sessions(animalName, sessions)
    choice = bdata['choice']
    valid = bdata['valid'] & (choice!=bdata.labels['choice']['none'])
    freqEachTrial = bdata['targetFrequency']
    choiceRight = choice==bdata.labels['choice']['right']
    currentBlock = bdata['currentBlock']
    blockTypes = [bdata.labels['currentBlock'][blockLabel] for blockLabel in blockLabels] 
    trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)

    possibleFreqs = np.unique(freqEachTrial)
    print(animalName)
    print(possibleFreqs)
    '''
    for indB,blockLabel in enumerate(blockLabels):
        if np.any(trialsEachType[:, indB]):
            targetFrequencyThisBlock = freqEachTrial[trialsEachType[:, indB]]    
            validThisBlock = valid[trialsEachType[:,indB]]
            choiceRightThisBlock = choiceRight[trialsEachType[:,indB]]
            (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
            behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)
            # -- Fit psycurve and store fitted values -- #
            #constraints = None
            logPossibleValues = np.log2(possibleValues)
            lowerFreqConstraint = logPossibleValues[0]
            upperFreqConstraint = logPossibleValues[-1]
            constraints = ( 'Uniform({}, {})'.format(lowerFreqConstraint, upperFreqConstraint),
                            'Uniform(0,5)' ,
                            'Uniform(0,1)',
                            'Uniform(0,1)')
            data = np.c_[logPossibleValues,nHitsEachValue,nTrialsEachValue]
            # linear core 'ab': (x-a)/b; logistic sigmoid: 1/(1+np.exp(-(xval-alpha)/beta))
            psyCurveInference = psi.BootstrapInference(data,sample=False, sigmoid='logistic', core='ab',priors=constraints, nafc=1)
            midFreq = np.logspace(np.log2(possibleValues[0]), np.log2(possibleValues[-1]), 
                base=2, num=len(possibleValues)+1)[(len(possibleValues)+1)/2]
            midFreqLog = np.log2(midFreq)
            freqsToFit = np.logspace(logPossibleValues[0], logPossibleValues[-1], num=9, base=2) #[logPossibleValues[0], midFreqLog, logPossibleValues[-1]]
            fittedRightwardChoiceThisBlock = 100 * psyCurveInference.evaluate(x=np.log2(freqsToFit))
            resultThisAnimal[indB, :] = fittedRightwardChoiceThisBlock
        elif not np.any(trialsEachType[:, indB]):
            resultThisAnimal[indB, :] = np.repeat(np.NaN, numFreqs)
    freqsAllAnimals[:, indA] = freqsToFit
    resultAllAnimals[:,:,indA] = resultThisAnimal
    '''

'''
summaryFilename = 'rc_fitted_rightward_choice_each_condition_by_freq_summary.npz'
summaryFullPath = os.path.join(outputDir,summaryFilename)
np.savez(summaryFullPath, animalsUsed=animalsUsed, numSessionsToInclude=numSessionsToInclude, 
    blockLabels=blockLabels, freqs=['lowest','middle','highest'], script=scriptFullPath, 
    resultAllAnimals=resultAllAnimals, fittedFreqsAllAnimals=freqsAllAnimals)
'''
