'''
Script to load many behavior sessions and generate summary(average) psychometric curve for reward_change_freq_discri paradigm
'''
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import colorpalette

#EXPERIMENTER = 'santiago'
EXPERIMENTER = 'lan'
#settings.BEHAVIOR_PATH = '/home/languo/data/mnt/jarahubdata'
#settings.BEHAVIOR_PATH = '/var/tmp/data/'

subjects = ['adap012']
#subjects = ['test']

FREQCOLORS = [colorpalette.TangoPalette['Chameleon3'],
              colorpalette.TangoPalette['ScarletRed1'],
              colorpalette.TangoPalette['SkyBlue2'] , 'g', 'm', 'k']

if len(sys.argv)>1:
    sessions = sys.argv[1:]

nSessions = len(sessions)
nAnimals = len(subjects)
gs = gridspec.GridSpec(nAnimals, 1)
gs.update(hspace=0.5,wspace=0.4)
plt.clf()

for inda, thisAnimal in enumerate(subjects):
    allBehavDataThisAnimal = behavioranalysis.load_many_sessions(thisAnimal,sessions)
    
    targetFrequency = allBehavDataThisAnimal['targetFrequency']
    choice=allBehavDataThisAnimal['choice']
    valid=allBehavDataThisAnimal['valid']& (choice!=allBehavDataThisAnimal.labels['choice']['none'])
    choiceRight = choice==allBehavDataThisAnimal.labels['choice']['right']
    currentBlock = allBehavDataThisAnimal['currentBlock']
    blockTypes = [allBehavDataThisAnimal.labels['currentBlock']['same_reward'],allBehavDataThisAnimal.labels['currentBlock']['more_left'],allBehavDataThisAnimal.labels['currentBlock']['more_right']]
    blockLabels = ['same_reward','more_left','more_right']
    trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
    
    #print trialsEachType
    nBlocks = len(blockTypes)
    thisAnimalPos = inda
    ax1=plt.subplot(gs[thisAnimalPos])
    fontsize = 12
    allPline = []
    blockLegends = []
    for blockType in range(nBlocks):
        if np.any(trialsEachType[:,blockType]):
            targetFrequencyThisBlock = targetFrequency[trialsEachType[:,blockType]]    
            validThisBlock = valid[trialsEachType[:,blockType]]
            choiceRightThisBlock = choiceRight[trialsEachType[:,blockType]]
            #currentBlockValue = currentBlock[trialsEachBlock[0,block]]
            (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
                                                                                                    behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)
            (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                ciHitsEachValue,xTickPeriod=1)

            plt.setp((pline, pcaps, pbars), color=FREQCOLORS[blockType])
            plt.setp(pdots, mfc=FREQCOLORS[blockType], mec=FREQCOLORS[blockType])
            allPline.append(pline)
            blockLegends.append(blockLabels[blockType])
            
            if blockType == nBlocks-1: 
                plt.xlabel('Frequency (kHz)',fontsize=fontsize)
                plt.ylabel('Rightward trials (%)',fontsize=fontsize)
                extraplots.set_ticks_fontsize(plt.gca(),fontsize)
                legend = plt.legend(allPline,blockLegends,loc=2)
                # Add the legend manually to the current Axes.
                ax = plt.gca().add_artist(legend)
                #plt.hold(True)
        #plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
        plt.show()
    plt.title('%s_%sto%s'%(thisAnimal,sessions[0],sessions[-1]))   

outputDir='/home/languo/data/behavior_reports' 
animalStr = '-'.join(subjects)
sessionStr = '-'.join(sessions)
plt.gcf().set_size_inches((8.5,11))
figformat = 'png' 
filename = 'behavior_summary_%s_%s.%s'%(animalStr,sessionStr,figformat)
fullFileName = os.path.join(outputDir,filename)
print 'saving figure to %s'%fullFileName
plt.gcf().savefig(fullFileName,format=figformat)



