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

STUDY_NAME = '2017rc'

FIGNAME = 'behavior_change'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

if not os.path.exists(dataDir):
    os.mkdir(dataDir)


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

    possibleFreqs = np.unique(targetFrequency)
    nFreqs = len(possibleFreqs)
    print '{}, freqs: {}'.format(animal, str(possibleFreqs))
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
        #plt.show()
    plt.title('%s_%sto%s'%(animal,sessions[0],sessions[-1]))   
    return fractionHitsEachValueAllBlocks, possibleFreqs


def save_svg_psycurve_reward_change(animal, sessions):
    import os
    #outputDir='/home/languo/data/behavior_reports' 
    outputDir='/tmp/'
    animalStr = animal
    sessionStr = '-'.join(sessions)
    plt.gcf().set_size_inches((8.5,11))
    figformat = 'svg' 
    filename = 'behavior_summary_%s_%s.%s'%(animalStr,sessionStr,figformat)
    fullFileName = os.path.join(outputDir,filename)
    #if not os.path.isfile(fullFileName):
    print 'saving figure to %s'%fullFileName
    plt.gcf().savefig(fullFileName,format=figformat)


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    plt.style.use(['seaborn-white','seaborn-talk'])

    CASE = 2
    # -- For checking a particular animal's performance on a particular date -- #
    if CASE == 1:
        subjects = ['adap067']
    
        if len(sys.argv)>1:
            sessions = sys.argv[1:]

        for thisAnimal in subjects:
            plot_ave_psycurve_reward_change(thisAnimal, sessions)
            save_svg_psycurve_reward_change(thisAnimal, sessions)

    # -- All reward change mice, all good sessions average plot -- #
    elif CASE == 2:
        sujectSessionsDict = {'adap012':['20160219a','20160223a','20160224a','20160226a','20160227a','20160228a','20160229a'],
                              #'adap008':['20151118a','20151119a','20151120a','20151121a','20151122a','20151123a','20151124a'], #same_left_right block transition
                              'adap005':['20151118a','20151119a','20151120a','20151121a','20151122a','20151123a','20151124a'], #same_left_right block transition
                              #'adap011':['20160122a','20160123a','20160124a','20160125a','20160126a'],
                              #'adap013':['20160216a','20160217a','20160309a','20160310a','20160311a','20160312a','20160313a','20160314a'], #some of them are of same_right_left block transition
                              #'adap015':['20160302a','20160309a','20160310a','20160311a','20160312a','20160313a','20160314a','20160315a'], #some of them are of same_right_left block transition
                              'adap017':['20160219a','20160222a','20160223a','20160224a','20160226a','20160301a','20160302a','20160309a','20160310a','20160311a','20160312a','20160313a','20160314a'], #some of them are of same_right_left block transition
                              'adap071':['20171002a','20171003a','20171004a','20171005a','20171006a','20171007a'],
                              'adap067':['20171023a','20171024a','20171025a','20171026a','20171027a','20171028a'],
                              'gosi004':['20170127a','20170128a','20170129a','20170130a','20170131a','20170201a'],
                              'gosi008':['20170210a','20170212a','20170213a','20170214a','20170215a','20170216a'],
                              'gosi001':['20170406a','20170407a','20170408a','20170409a','20170410a','20170411a'],
                              'gosi010':['20170406a','20170407a','20170408a','20170409a','20170410a','20170411a']
        }
        #sujectSessionsDict = {'adap071':['20171002a','20171003a','20171004a','20171005a','20171006a','20171007a']}
        numOfAnimals = len(sujectSessionsDict.keys())
        avePsycurveMoreLeft = np.empty((numOfAnimals,8)) #We used 8 frequencies in the psy curve
        avePsycurveMoreRight = np.empty((numOfAnimals,8))

        for ind, (subject, sessions) in enumerate(sujectSessionsDict.items()):
            fractionHitsEachValueAllBlocks, possibleFreqs = plot_ave_psycurve_reward_change(subject, sessions)
            #save_svg_psycurve_reward_change(subject, sessions)
            avePsycurveMoreLeft[ind,:] = fractionHitsEachValueAllBlocks[1,:] #The second row is more_left block
            avePsycurveMoreRight[ind,:] = fractionHitsEachValueAllBlocks[2,:]#The third row is more_right block
            # FIXME: Note that I'm only using the last "possibleFreqs", but each subject may have a different one
       
        # -- This plots an average psycurve for all the mice -- #    
        import scipy.stats as stats
        fontsize = 12
        plt.clf()
        plt.errorbar(x=range(1,9),y=np.mean(avePsycurveMoreLeft,axis=0),yerr=stats.sem(avePsycurveMoreLeft,axis=0),linewidth=3,linestyle='-',capthick=2,elinewidth=2,marker='o',ms=8,color=colorpalette.TangoPalette['ScarletRed1'])
        plt.hold('on')
        plt.errorbar(x=range(1,9),y=np.mean(avePsycurveMoreRight,axis=0),yerr=stats.sem(avePsycurveMoreRight,axis=0),linewidth=3,linestyle='-',capthick=2,elinewidth=2,marker='o',ms=8,color=colorpalette.TangoPalette['SkyBlue2'])
        plt.xlabel('Frequency (kHz)',fontsize=fontsize)
        plt.ylabel('Proportion of rightward choice',fontsize=fontsize)
        plt.ylim((-0.1,1.1))
        extraplots.set_ticks_fontsize(plt.gca(),fontsize)
        plt.show()
      
        outputFile = 'psychometric_summary_{}_mice.npz'.format(len(sujectSessionsDict.keys()))
        outputFullPath = os.path.join(dataDir,outputFile)
        print('Saving data to {}'.format(outputFullPath))
        np.savez(outputFullPath, avePsycurveMoreLeft=avePsycurveMoreLeft, avePsycurveMoreRight=avePsycurveMoreRight,
                 subjects=sujectSessionsDict.keys(), possibleFreqs=possibleFreqs)
