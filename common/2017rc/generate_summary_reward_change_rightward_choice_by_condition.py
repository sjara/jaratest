'''
Generate intermediate data for plotting reward change behavior summary: percent rightward choice for each animal in left_more reward vs right_more reward condition.
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
animalsUsed = [animalName for animalName in sorted(animals.keys())]
resultAllAnimals = np.empty((len(blockLabels), numSessionsToInclude, len(animalsUsed)))

for indA,animalName in enumerate(animalsUsed):
    sessions = animals[animalName][:numSessionsToInclude]
    resultThisAnimal = np.empty((len(blockLabels), numSessionsToInclude))
    for indS,session in enumerate(sessions):
        bdata = behavioranalysis.load_many_sessions(animalName, [session])
        choice = bdata['choice']
        valid = bdata['valid'] & (choice!=bdata.labels['choice']['none'])
        choiceRight = choice==bdata.labels['choice']['right']
        currentBlock = bdata['currentBlock']
        blockTypes = [bdata.labels['currentBlock']['same_reward'],bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
        trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)

        for indB,blockLabel in enumerate(blockLabels):
            if np.any(trialsEachType[:, indB]):
                validThisBlock = valid[trialsEachType[:, indB]]
                choiceRightThisBlock = choiceRight[trialsEachType[:,indB]]
                percentRightwardChoiceThisBlock = 100*sum(choiceRightThisBlock) / float(sum(validThisBlock))
                resultThisAnimal[indB, indS] = percentRightwardChoiceThisBlock
            elif not np.any(trialsEachType[:, indB]):
                resultThisAnimal[indB, indS] = np.NaN
    resultAllAnimals[:,:,indA] = resultThisAnimal

summaryFilename = 'rc_rightward_choice_each_condition_summary.npz'
summaryFullPath = os.path.join(outputDir,summaryFilename)
np.savez(summaryFullPath, animalsUsed=animalsUsed, numSessionsToInclude=numSessionsToInclude, blockLabels=blockLabels, script=scriptFullPath, resultAllAnimals=resultAllAnimals)
