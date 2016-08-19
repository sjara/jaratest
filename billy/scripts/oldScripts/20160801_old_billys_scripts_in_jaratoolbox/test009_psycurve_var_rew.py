'''
Script to plot psychometric curves per block for reward_change_freq_discrimination paradigm
'''
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#from jaratoolbox import behavioranalysis
from jaratoolbox.test.lan import behavioranalysis_vlan as behavioranalysis
reload(behavioranalysis)
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import settings
reload(settings)
from jaratoolbox import colorpalette
import matplotlib.lines as mlines

#EXPERIMENTER = 'santiago'
EXPERIMENTER = 'billy'
#settings.BEHAVIOR_PATH = '/home/languo/data/mnt/jarahubdata'
#settings.BEHAVIOR_PATH = '/var/tmp/data/'

subjects = ['adap013']
#subjects = ['test']
#subjects = ['adap011']

FREQCOLORS = [colorpalette.TangoPalette['Chameleon3'],
              colorpalette.TangoPalette['ScarletRed1'],
              colorpalette.TangoPalette['SkyBlue2'] , 'g', 'm', 'k']

if len(sys.argv)>1:
    sessions = sys.argv[1:]

nSessions = len(sessions)
nAnimals = len(subjects)

loadingClass = loadbehavior.FlexCategBehaviorData  #using this bdata class so we get 'blocks'
paradigm = '2afc'

gs = gridspec.GridSpec(nSessions*nAnimals, 1)
gs.update(hspace=0.5,wspace=0.4)
plt.clf()

for inds,thisSession in enumerate(sessions):
    for inda,animalName in enumerate(subjects):
        try:
            behavFile = loadbehavior.path_to_behavior_data(animalName,EXPERIMENTER,paradigm,thisSession)
            behavData = loadingClass(behavFile,readmode='full')
        except IOError:
            print thisSession+' does not exist'
            continue
        print 'Loaded %s %s'%(animalName,thisSession)

        targetFrequency = behavData['targetFrequency']
        choice=behavData['choice']
        valid=behavData['valid']& (choice!=behavData.labels['choice']['none'])
        choiceRight = choice==behavData.labels['choice']['right']
        currentBlock = behavData['currentBlock']

        behavData.find_trials_each_block()
        trialsEachBlock = behavData.blocks['trialsEachBlock']
        #print trialsEachBlock
        nBlocks = behavData.blocks['nBlocks']

        thisAnimalPos = 1*inda*nSessions
        thisPlotPos = thisAnimalPos+1*inds
        ax1=plt.subplot(gs[thisPlotPos])
        fontsize = 12
        allPline = []
        legendLabels = []
        for block in range(nBlocks):
            targetFrequencyThisBlock = targetFrequency[trialsEachBlock[:,block]]    
            validThisBlock = valid[trialsEachBlock[:,block]]
            choiceRightThisBlock = choiceRight[trialsEachBlock[:,block]]
            #currentBlockValue = currentBlock[trialsEachBlock[0,block]]
            (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
                                                                                                    behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)
            (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                ciHitsEachValue,xTickPeriod=1)
            
            plt.setp((pline, pcaps, pbars), color=FREQCOLORS[block])
            plt.setp(pdots, mfc=FREQCOLORS[block], mec=FREQCOLORS[block])
            #blockLine=mlines.Line2D([],[],color=FREQCOLORS[block],linewidth=2, label='block %d'%(block+1))   
            legendLabels.append('block %d'%(block+1))
            allPline.append(pline)
            legend = plt.legend(allPline,legendLabels,loc=2)
            # Add the legend manually to the current Axes.
            ax = plt.gca().add_artist(legend)
            plt.hold(True)
            
            if block == nBlocks-1: 
                plt.xlabel('Frequency (kHz)',fontsize=fontsize)
                plt.ylabel('Rightward trials (%)',fontsize=fontsize)
                extraplots.set_ticks_fontsize(plt.gca(),fontsize)
            
            #plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
            plt.show()
        plt.title('%s_%s'%(animalName,thisSession))   
    
    outputDir='/home/languo/data/behavior_reports' 
    animalStr = '-'.join(subjects)
    sessionStr = '-'.join(sessions)
    plt.gcf().set_size_inches((8.5,11))
    figformat = 'png' 
    filename = 'behavior_%s_%s.%s'%(animalStr,sessionStr,figformat)
    fullFileName = os.path.join(outputDir,filename)
    print 'saving figure to %s'%fullFileName
    plt.gcf().savefig(fullFileName,format=figformat)

