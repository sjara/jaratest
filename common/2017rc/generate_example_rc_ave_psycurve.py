'''
Generate average psycurve for reward change task for select animals.
'''
import os
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
import figparams
import numpy as np
from reward_change_sessions import animals

FIGNAME = 'reward_change_behavior'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

scriptFullPath = os.path.realpath(__file__)

numSessionsToInclude = 6
blockLabels = ['same_reward','more_left','more_right']
animalsUsed = ['adap012', 'adap071']
resultsDict = {}
for indA,animalName in enumerate(animalsUsed):
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
    fractionHitsEachBlockEachFreq = np.empty((nBlocks,nFreqs))
    
    for blockType in range(nBlocks):
        if np.any(trialsEachType[:,blockType]):
            targetFrequencyThisBlock = targetFrequency[trialsEachType[:,blockType]]    
            validThisBlock = valid[trialsEachType[:,blockType]]
            choiceRightThisBlock = choiceRight[trialsEachType[:,blockType]]
            (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)

            fractionHitsEachBlockEachFreq[blockType,:] = fractionHitsEachValue
        else:
            fractionHitsEachBlockEachFreq[blockType,:] = np.NaN
    resultsDict.update({animalName: fractionHitsEachBlockEachFreq})

outputFilename = 'example_rc_ave_pycurve.npz'
outputFullPath = os.path.join(outputDir, outputFilename)
np.savez(outputFullPath, animalsUsed=animalsUsed, numSessionsToInclude=numSessionsToInclude, blockLabels=blockLabels, script=scriptFullPath, **resultsDict)
