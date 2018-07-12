'''
Generate intermediate data for plotting reward change behavior summary: 
percent rightward choice for each animal in left_more reward vs right_more reward condition
for the extreme freqs and middle freqs.
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
numFreqs = 3
blockLabels = ['more_left','more_right'] #['same_reward','more_left','more_right']
animalsUsed = [animalName for animalName in sorted(animals.keys())]
resultAllAnimals = np.empty((len(blockLabels), numFreqs, len(animalsUsed)))

for indA,animalName in enumerate(animalsUsed):
    sessions = animals[animalName][:numSessionsToInclude]
    resultThisAnimal = np.empty((len(blockLabels), numFreqs))
    #for indS,session in enumerate(sessions):
    bdata = behavioranalysis.load_many_sessions(animalName, sessions)
    choice = bdata['choice']
    valid = bdata['valid'] & (choice!=bdata.labels['choice']['none'])
    freqEachTrial = bdata['targetFrequency']
    frequencies = np.unique(freqEachTrial)
    highestFreq = frequencies[-1]
    lowestFreq = frequencies[0]
    middleFreqs = [frequencies[len(frequencies)/2-1], frequencies[len(frequencies)/2]]
    freqsToCalculate = [lowestFreq, middleFreqs, highestFreq]
    choiceRight = choice==bdata.labels['choice']['right']
    currentBlock = bdata['currentBlock']
    blockTypes = [bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']] #[bdata.labels['currentBlock']['same_reward'],bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
    trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)

    for indB,blockLabel in enumerate(blockLabels):
        if np.any(trialsEachType[:, indB]):
            for indF, freq in enumerate(freqsToCalculate):
                if indF == 1:
                    trialsThisFreq = np.logical_or(freqEachTrial==freq[0], freqEachTrial==freq[1])
                else:
                    trialsThisFreq = freqEachTrial==freq
                validThisFreq = valid & trialsThisFreq
                choiceRightThisFreq = choiceRight & trialsThisFreq
                validThisBlockThisFreq = validThisFreq[trialsEachType[:, indB]]
                choiceRightThisBlockThisFreq = choiceRightThisFreq[trialsEachType[:,indB]]
                percentRightwardChoiceThisBlock = 100*sum(choiceRightThisBlockThisFreq) / float(sum(validThisBlockThisFreq))
                resultThisAnimal[indB, indF] = percentRightwardChoiceThisBlock
        elif not np.any(trialsEachType[:, indB]):
            resultThisAnimal[indB, indF] = np.NaN
    resultAllAnimals[:,:,indA] = resultThisAnimal

summaryFilename = 'rc_ave_rightward_choice_each_condition_by_freq_summary.npz'
summaryFullPath = os.path.join(outputDir,summaryFilename)
np.savez(summaryFullPath, animalsUsed=animalsUsed, numSessionsToInclude=numSessionsToInclude, blockLabels=blockLabels, freqs=['low','middle-two','high'], script=scriptFullPath, resultAllAnimals=resultAllAnimals)
