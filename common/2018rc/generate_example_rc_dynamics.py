'''
Generate behavior dynamic plot for reward change task for select animals.
'''
import os
import figparams
import numpy as np
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import extrafuncs
from reward_change_sessions import animals


FIGNAME = 'reward_change_behavior'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

scriptFullPath = os.path.realpath(__file__)

numSessionsToInclude = 6
blockLabels = ['same_reward','more_left','more_right']
sessionsDict = {'adap071':'20171007a'}
#animalsUsed = ['adap012', 'adap071']
resultsDict = {}
paradigm = '2afc'

def calculate_dynamics(behavData, winsize=40, soundfreq=None, byBlock=True):
    if soundfreq:
        possibleFreq = soundfreq
    else:
        possibleFreq = np.unique(behavData['targetFrequency'])
    if byBlock:
        behavData.find_trials_each_block()

        nBlocks = behavData.blocks['nBlocks']
        trialsEachBlock = behavData.blocks['trialsEachBlock']
        validEachBlock = trialsEachBlock & (behavData['valid'][:,np.newaxis].astype(bool))
        nValidEachBlock = np.sum(validEachBlock,axis=0)
        lastValidEachBlock = np.cumsum(nValidEachBlock) # Actually, these values correspond to lastIndex+1
        firstValidEachBlock = np.concatenate(([0],lastValidEachBlock[:-1]))
        rightChoice = behavData['choice']==behavData.labels['choice']['right']
        
        movAvChoiceMatrix = np.ndarray([len(possibleFreq), sum(valid)])
        for indb in range(nBlocks):
            trialsThisBlock = trialsEachBlock[:,indb]
            validThisBlock = validEachBlock[:,indb]
            for indf,thisFreq in enumerate(possibleFreq):
                trialsThisFreq = (behavData['targetFrequency']==thisFreq)
                choiceVecThisFreq = np.ma.masked_array(rightChoice[validThisBlock])
                choiceVecThisFreq.mask = ~trialsThisFreq[validThisBlock]
                movAvChoice = extrafuncs.moving_average_masked(choiceVecThisFreq,winsize)
                print thisFreq
                movAvChoiceMatrix[indf, firstValidEachBlock[indb]:lastValidEachBlock[indb]] = movAvChoice
    else:
        valid = behavData['valid']
        movAvChoiceMatrix = np.ndarray([len(possibleFreq), sum(valid)])
        rightChoice = behavData['choice']==behavData.labels['choice']['right']
        for indf,thisFreq in enumerate(possibleFreq):
            trialsThisFreq = (behavData['targetFrequency']==thisFreq)
            choiceVecThisFreq = np.ma.masked_array(rightChoice[valid])
            choiceVecThisFreq.mask = ~trialsThisFreq[valid]
            movAvChoice = extrafuncs.moving_average_masked(choiceVecThisFreq,winsize)
            movAvChoiceMatrix[indf, :] = movAvChoice
    return movAvChoiceMatrix


for animalName,session in sessionsDict.items():
    behavFileName = loadbehavior.path_to_behavior_data(animalName,paradigm,session)
    behavData = loadbehavior.FlexCategBehaviorData(behavFileName)
    #allBehavDataThisAnimal = behavioranalysis.load_many_sessions(animalName,sessions)
    #targetFrequency = allBehavDataThisAnimal['targetFrequency']
    #currentBlock = allBehavDataThisAnimal['currentBlock']
    #blockTypes = [allBehavDataThisAnimal.labels['currentBlock'][blockLabel] for blockLabel in blockLabels]
    #trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
    #choice = allBehavDataThisAnimal['choice']
    #valid = allBehavDataThisAnimal['valid']& (choice!=allBehavDataThisAnimal.labels['choice']['none'])
    #choiceRight = choice==allBehavDataThisAnimal.labels['choice']['right'] 
    #nBlocks = len(blockTypes)
    #nFreqs = len(np.unique(targetFrequency))
    movAvChoiceMatrix = calculate_dynamics(behavData, winsize=40, soundfreq=None, byBlock=True)
    
    
    #outputFilename = 'example_rc_dynamics.npz'
    #outputFullPath = os.path.join(outputDir, outputFilename)
    #np.savez(outputFullPath, animalName=animalName, session=session, blockLabels=blockLabels, script=scriptFullPath, **resultsDict)
