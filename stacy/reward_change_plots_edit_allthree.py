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


def plot_ave_psycurve_reward_change(animal, sessions):
    FREQCOLORS =  [colorpalette.TangoPalette['Chameleon3'],
                   colorpalette.TangoPalette['ScarletRed1'],
                   colorpalette.TangoPalette['SkyBlue2']]

    allBehavDataThisAnimal = behavioranalysis.load_many_sessions(animal,sessions)
    targetFrequency = allBehavDataThisAnimal['targetFrequency']
    choice=allBehavDataThisAnimal['choice']
    valid=allBehavDataThisAnimal['valid']& (choice!=allBehavDataThisAnimal.labels['choice']['none'])
    choiceRight = choice==allBehavDataThisAnimal.labels['choice']['right']
    currentBlock = allBehavDataThisAnimal['currentBlock']
    blockTypes = [allBehavDataThisAnimal.labels['currentBlock']['same_reward'],allBehavDataThisAnimal.labels['currentBlock']['more_left'],allBehavDataThisAnimal.labels['currentBlock']['more_right']]
    #blockTypes = [allBehavDataThisAnimal.labels['currentBlock']['more_left'],allBehavDataThisAnimal.labels['currentBlock']['more_right']]
    blockLabels = ['same_reward','more_left','more_right']
    #blockLabels = ['more_left','more_right']
    trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
    
    nFreqs = len(np.unique(targetFrequency))
    #print trialsEachType
    nBlocks = len(blockTypes)
    #thisAnimalPos = inda
    #ax1=plt.subplot(gs[thisAnimalPos])
    #plt.clf()
    fontsize = 12
    allPline = []
    blockLegends = []
    fractionHitsEachValueAllBlocks = np.empty((nBlocks,nFreqs))

    for blockType in range(nBlocks):
        if np.any(trialsEachType[:,blockType]):
            targetFrequencyThisBlock = targetFrequency[trialsEachType[:,blockType]]    
            validThisBlock = valid[trialsEachType[:,blockType]]
            choiceRightThisBlock = choiceRight[trialsEachType[:,blockType]]
            #currentBlockValue = currentBlock[trialsEachBlock[0,block]]
            (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
            behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)
            fractionHitsEachValueAllBlocks[blockType,:] = fractionHitsEachValue
            
	    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,  ciHitsEachValue,xTickPeriod=1)
            plt.setp((pline, pcaps, pbars), color=FREQCOLORS[blockType])
            plt.setp(pdots, mfc=FREQCOLORS[blockType], mec=FREQCOLORS[blockType])
            allPline.append(pline)
            blockLegends.append(blockLabels[blockType])
            
            if blockType == nBlocks-1: 
                plt.xlabel('Frequency (kHz)',fontsize=fontsize)
                plt.ylabel('Rightward trials (%)',fontsize=fontsize)
                extraplots.set_ticks_fontsize(plt.gca(),fontsize)
                legend = plt.legend(allPline,blockLegends,loc=2) #Add the legend manually to the current Axes.
                ax = plt.gca().add_artist(legend)
                #plt.hold(True)
        #plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
        #plt.show()
    plt.title('%s %s-%s'%(animal,sessions[0],sessions[-1]))   
    return fractionHitsEachValueAllBlocks

'''
def save_svg_psycurve_reward_change(animal, sessions):
    import os
    outputDir='/home/src/jaratest/stacy' 
    animalStr = animal
    sessionStr = '-'.join(sessions)
    plt.gcf().set_size_inches((8.5,11))
    figformat = 'svg' 
    filename = 'behavior_summary_%s_%s.%s'%(animalStr,sessionStr,figformat)
    fullFileName = os.path.join(outputDir,filename)
    if not os.path.isfile(fullFileName):
        print 'saving figure to %s'%fullFileName
        plt.gcf().savefig(fullFileName,format=figformat)

'''

if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    #plt.style.use(['seaborn-white','seaborn-talk'])

    CASE = 1

    if CASE == 1:
        subjects = [#'gosi001', 
		    #'gosi002', 
		    #'gosi004', 
		    #'gosi006', 
		    #'gosi007', 
		    'gosi008', 
		    #'gosi010', 
		    #'gosi011',
		    #'gosi013'
		   ]
    
        if len(sys.argv)>1:
            sessions = sys.argv[1:]
	else:
	    sessions = [#'20170127a', 
			#'20170128a', 
			#'20170129a', 
			#'20170130a', 
			#'20170131a',
			#'20170201a',
			#'20170202a',
			#'20170203a',
			#'20170204a',
			#'20170205a',
			#'20170206a',
			#'20170207a',
			#'20170208a',
			#'20170209a',
			'20170210a',
			'20170212a',
			'20170213a',
		   	'20170214a',
			'20170215a',
			'20170216a',
			#'20170227a',			
			#'20170303a',
                        #'20170306a',
			#'20170307a',
                        #'20170308a',
                        #'20170309a',
                        #'20170310a',
                        #'20170311a',
                        #'20170312a'
			]

	plt.clf()
        for indanimal, thisAnimal in enumerate(subjects):
	    plt.subplot(1,1,indanimal+1)
            plot_ave_psycurve_reward_change(thisAnimal, sessions)
 	plt.show()


    elif CASE == 2:
        sujectSessionsDict = {'gosi001':['20170127a','20170128a','20170129a','20170130a','20170131a','20170201a','20170202a', '20170203a'],
                              'gosi002':['20170127a','20170128a','20170129a','20170130a','20170131a','20170201a','20170202a', '20170203a'], 
                              'gosi004':['20170127a','20170128a','20170129a','20170130a','20170131a','20170201a','20170202a', '20170203a'],
                              'gosi006':['20170127a','20170128a','20170129a','20170130a','20170131a','20170201a','20170202a', '20170203a'],
                              'gosi007':['20170127a','20170128a','20170129a','20170130a','20170131a','20170201a','20170202a', '20170203a'],
                              'gosi008':['20170127a','20170128a','20170129a','20170130a','20170131a','20170201a','20170202a', '20170203a'], 
                              'gosi010':['20170127a','20170128a','20170129a','20170130a','20170131a','20170201a','20170202a', '20170203a'],
			      'gosi011':['20170127a','20170128a','20170129a','20170130a','20170131a','20170201a','20170202a', '20170203a'],
			      'gosi013':['20170127a','20170128a','20170129a','20170130a','20170131a','20170201a','20170202a', '20170203a'], 
                              }
        numOfAnimals = len(sujectSessionsDict.keys())
        avePsycurveMoreLeft = np.empty((numOfAnimals,8)) # 8 frequencies in the psy curve
        avePsycurveMoreRight = np.empty((numOfAnimals,8))

        for ind, (subject, sessions) in enumerate(sujectSessionsDict.items()):
            fractionHitsEachValueAllBlocks = plot_ave_psycurve_reward_change(subject, sessions)
            save_svg_psycurve_reward_change(subject, sessions)
            avePsycurveMoreLeft[ind,:] = fractionHitsEachValueAllBlocks[0,:] #The first row is more_left block
            avePsycurveMoreRight[ind,:] = fractionHitsEachValueAllBlocks[1,:]#The second row is more_right block

        fontsize = 12
        plt.clf()
        #plt.errorbar(x=range(1,9),y=np.mean(avePsycurveMoreLeft,axis=0),yerr=np.std(avePsycurveMoreLeft,axis=0),linewidth=3,linestyle='-',capthick=2,elinewidth=2,marker='o',ms=8,color=colorpalette.TangoPalette['ScarletRed1'])
        plt.hold('on')
        #plt.errorbar(x=range(1,9),y=np.mean(avePsycurveMoreRight,axis=0),yerr=np.std(avePsycurveMoreRight,axis=0),linewidth=3,linestyle='-',capthick=2,elinewidth=2,marker='o',ms=8,color=colorpalette.TangoPalette['SkyBlue2'])
        plt.xlabel('Frequency (kHz)',fontsize=fontsize)
        plt.ylabel('Rightward trials (%)',fontsize=fontsize)
        plt.ylim((-0.1,1.1))
        extraplots.set_ticks_fontsize(plt.gca(),fontsize)	
        plt.show()
