import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
from jaratoolbox import extraplots
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pdb


animalLists = [['adap005','adap012', 'adap013', 'adap015', 'adap017'], ['gosi001','gosi004', 'gosi008','gosi010']]
animalLabels = ['astr', 'ac']

modulationWindows = {'sound':['0-0.1s'],
                     'center-out': ['0.05-0.15s',
                                    '0.05-0.25s',
                                    '0.05-0.35s']
                     }
freqLabels = ['Low','High']
movementDirections = ['Left', 'Right']
#plotAll = True
#normalized = False
#logscaled = False

qualityThreshold = 3 #2.5 
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05

plt.figure()

outputDir = '/home/languo/data/ephys/reward_change_stats/reports/'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

for indRegion, (label,animalList) in enumerate(zip(animalLabels, animalLists)):
    celldbPath = os.path.join(settings.DATABASE_PATH,'reward_change_{}.h5'.format(label))
    celldb = pd.read_hdf(celldbPath, key='reward_change')

    # -- Plot histogram of modulation index for sound responsive cells, take the most responsive frequency -- #
    goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{} and consistentInFiring==True and keep_after_dup_test==True and inTargetArea==True and met_behav_criteria==True'.format(ISIcutoff, qualityThreshold))

    soundResp = goodQualCells.behavZscore.apply(lambda x: np.max(np.abs(x)) >=  maxZThreshold) #The bigger of the sound Z score is over threshold
    moreRespLowFreq = soundResp & goodQualCells.behavZscore.apply(lambda x: abs(x[0]) > abs(x[1]))
    moreRespHighFreq = soundResp & goodQualCells.behavZscore.apply(lambda x: abs(x[1]) > abs(x[0]))
    goodLowFreqRespCells = goodQualCells[moreRespLowFreq]
    goodHighFreqRespCells = goodQualCells[moreRespHighFreq]

    movementSelective = goodQualCells.movementModS < alphaLevel
    moreRespMoveLeft = movementSelective & (goodQualCells.movementModI < 0)
    moreRespMoveRight = movementSelective & (goodQualCells.movementModI > 0)
    goodLeftMovementSelCells = goodQualCells[moreRespMoveLeft]
    goodRightMovementSelCells = goodQualCells[moreRespMoveRight]

    for indw, modWindow in enumerate(modulationWindows['sound']):
        lowFreqModIndName = 'modIndLow_'+modWindow+'_'+'sound'
        lowFreqModSigName = 'modSigLow_'+modWindow+'_'+'sound'
        highFreqModIndName = 'modIndHigh_'+modWindow+'_'+'sound'
        highFreqModSigName = 'modSigHigh_'+modWindow+'_'+'sound'

        goodLowFreqRespModInd = goodLowFreqRespCells[lowFreqModIndName]
        goodLowFreqRespModSig = goodLowFreqRespCells[lowFreqModSigName]
        goodHighFreqRespModInd = goodHighFreqRespCells[highFreqModIndName]
        goodHighFreqRespModSig = goodHighFreqRespCells[highFreqModSigName]
        sigModulatedLow = goodLowFreqRespModSig < alphaLevel
        sigModulatedHigh = goodHighFreqRespModSig < alphaLevel
        sigModI = np.concatenate((goodLowFreqRespModInd[sigModulatedLow].values,
                                  goodHighFreqRespModInd[sigModulatedHigh].values))
        nonsigModI = np.concatenate((goodLowFreqRespModInd[~sigModulatedLow].values,
                                  goodHighFreqRespModInd[~sigModulatedHigh].values))
        
        plt.clf()
        binsEdges = np.linspace(-1,1,20)
        plt.hist([sigModI,nonsigModI], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
        figTitle = '{}_{}_sound_responsive_cells'.format(label,modWindow)
        plt.title(figTitle)
        plt.text(-0.85, 0.5*plt.ylim()[1], '{} modulated out of {} sound-responsive cells: {:.3f}%'.format(len(sigModI), sum(soundResp), 100*float(len(sigModI))/sum(soundResp)))  
        
        plt.xlabel('Modulation index')
        plt.ylabel('Num of cells')
        #plt.show()
        figFullPath = os.path.join(outputDir, figTitle)
        plt.savefig(figFullPath,format='png')


        # -- Plot reward modulation during movement only for movement-selective cells -- #
    for indw, modWindow in enumerate(modulationWindows['center-out']):
        leftModIndName = 'modIndLow_'+modWindow+'_'+'center-out'
        leftModSigName = 'modSigLow_'+modWindow+'_'+'center-out'
        rightModIndName = 'modIndHigh_'+modWindow+'_'+'center-out'
        rightModSigName = 'modSigHigh_'+modWindow+'_'+'center-out'
        
        goodMovementSelCells = goodQualCells[movementSelective]
        sigModEitherDirection = (goodMovementSelCells[leftModSigName] < alphaLevel) | (goodMovementSelCells[rightModSigName] < alphaLevel)  
        print 'Out of {} movement-selective cells, {} were modulated by reward either going left or going right'.format(len(goodMovementSelCells), sum(sigModEitherDirection))
        goodLeftMovementSelModInd = goodLeftMovementSelCells[leftModIndName]
        goodLeftMovementSelModSig = goodLeftMovementSelCells[leftModSigName]
        goodRightMovementSelModInd = goodRightMovementSelCells[rightModIndName]
        goodRightMovementSelModSig = goodRightMovementSelCells[rightModSigName]
        sigModulatedLeft = goodLeftMovementSelModSig < alphaLevel
        sigModulatedRight = goodRightMovementSelModSig < alphaLevel
        sigModI = np.concatenate((goodLeftMovementSelModInd[sigModulatedLeft].values,
                                  goodRightMovementSelModInd[sigModulatedRight].values))
        nonsigModI = np.concatenate((goodLeftMovementSelModInd[~sigModulatedLeft].values,
                                     goodRightMovementSelModInd[~sigModulatedRight].values))
        
        plt.clf()
        binsEdges = np.linspace(-1,1,20)
        plt.hist([sigModI,nonsigModI], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
        figTitle = '{}_{}_movement_selective_cells'.format(label,modWindow)
        plt.title(figTitle)
        plt.text(-0.85, 0.5*plt.ylim()[1], '{} modulated out of {} movement-selective cells: {:.3f}%'.format(len(sigModI), sum(movementSelective), 100*float(len(sigModI))/sum(movementSelective))) 
        plt.text(-0.9, 0.8*plt.ylim()[1], 'Out of {} movement-selective cells, {} were modulated \nby reward either going left or going right'.format(len(goodMovementSelCells), sum(sigModEitherDirection)))

        plt.xlabel('Modulation index')
        plt.ylabel('Num of cells')
        #plt.show()
        figFullPath = os.path.join(outputDir, figTitle)
        plt.savefig(figFullPath,format='png')


        # -- Plot reward modulation during movement for all good cells -- #
    for indw, modWindow in enumerate(modulationWindows['center-out']):
        leftModIndName = 'modIndLow_'+modWindow+'_'+'center-out'
        leftModSigName = 'modSigLow_'+modWindow+'_'+'center-out'
        rightModIndName = 'modIndHigh_'+modWindow+'_'+'center-out'
        rightModSigName = 'modSigHigh_'+modWindow+'_'+'center-out'
        
        goodCellsLeftModInd = goodQualCells[leftModIndName]
        goodCellsLeftModSig = goodQualCells[leftModSigName]
        goodCellsRightModInd = goodQualCells[rightModIndName]
        goodCellsRightModSig = goodQualCells[rightModSigName]
        sigModulatedLeft = goodCellsLeftModSig < alphaLevel
        sigModulatedRight = goodCellsRightModSig < alphaLevel
        sigModILeft = goodCellsLeftModInd[sigModulatedLeft].values
        nonsigModILeft = goodCellsLeftModInd[~sigModulatedLeft].values
        sigModIRight = goodCellsRightModInd[sigModulatedRight].values
        nonsigModIRight = goodCellsRightModInd[~sigModulatedRight]
        
        binsEdges = np.linspace(-1,1,20)
        plt.clf()
        plt.subplot(1,2,1)
        plt.hist([sigModILeft,nonsigModILeft], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
        figTitle = '{}_{}_center-out_left'.format(label,modWindow)
        plt.title(figTitle)
        plt.text(-0.85, 0.5*plt.ylim()[1], '{} modulated out of \n{} good cells: {:.3f}%'.format(len(sigModILeft), len(goodQualCells), 100*float(len(sigModILeft))/len(goodQualCells)))        
        plt.xlabel('Modulation index')
        plt.ylabel('Num of cells')
        #plt.show()
        plt.subplot(1,2,2)
        plt.hist([sigModIRight,nonsigModIRight], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
        figTitle = '{}_{}_center-out_right'.format(label,modWindow)
        plt.title(figTitle)
        plt.text(-0.85, 0.5*plt.ylim()[1], '{} modulated out of \n{} good cells: {:.3f}%'.format(len(sigModIRight), len(goodQualCells), 100*float(len(sigModIRight))/len(goodQualCells)))
        plt.tight_layout()
        figSupTitle = '{}_{}_center-out_all_good_cells'.format(label,modWindow)
        figFullPath = os.path.join(outputDir, figSupTitle)
        plt.savefig(figFullPath,format='png')

'''
# ---------------- Movement --------------------#
plt.figure(figsize=(15,15))
gs = gridspec.GridSpec(len(modulationWindows['center-out']),len(animalLabels)*len(freqLabels))
gs.update(left=0.05, right=0.98, top=0.93, bottom=0.05, wspace=0.3, hspace=0.2)

for indRegion, (label,animalList) in enumerate(zip(animalLabels, animalLists)):
    celldbPath = os.path.join(settings.DATABASE_PATH,'reward_change_{}.h5'.format(label))
    celldb = pd.read_hdf(celldbPath, key='reward_change')

    # -- Plot histogram of modulation index -- #
    goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{}'.format(ISIcutoff, qualityThreshold))

    #lowFreqResponsive = goodQualCells.behavZscore.apply(lambda x: abs(x[0]) >= maxZThreshold)
    #highFreqResponsive = goodQualCells.behavZscore.apply(lambda x: abs(x[1]) >= maxZThreshold)
    #goodLowFreqRespCells=goodQualCells[lowFreqResponsive]
    #goodHighFreqRespCells=goodQualCells[highFreqResponsive]

    # For each window we calculated modulation index, check all good cells and all cells that response to this frequency (for sound mod) to see which cells were modulated by reward
    for indf, freq in enumerate(freqLabels):
        #plt.clf()
        numWins = len(modulationWindows['center-out'])
        for indw, modWindow in enumerate(modulationWindows['center-out']):
            modIndName = 'modInd'+freq+'_'+modWindow+'_'+'center-out'
            modSigName = 'modSig'+freq+'_'+modWindow+'_'+'center-out'
            print 'For {}, there are {} good cells'.format(label, len(goodQualCells))
            allGoodCellsModInd = goodQualCells[modIndName]
            allGoodCellsModSig = goodQualCells[modSigName]
            sigModGoodCells = allGoodCellsModSig < alphaLevel
            sigModIGoodCells = allGoodCellsModInd[sigModGoodCells]
            nonsigModIGoodCells = allGoodCellsModInd[~sigModGoodCells]

            #responsiveThisFreq = goodQualCells.behavZscore.apply(lambda x: abs(x[indf]) >= maxZThreshold)
            #allGoodRespCellsThisFreq = goodQualCells[responsiveThisFreq]
            #respCellsModInd = allGoodRespCellsThisFreq[modIndName]
            #respCellsModSig = allGoodRespCellsThisFreq[modSigName]
            #sigModRespCells = respCellsModSig < alphaLevel
            #sigModIRespCells = respCellsModInd[sigModRespCells]
            #nonsigModIRespCells = respCellsModInd[~sigModRespCells]
            # -- Plot reports only for good cells-- #
            ax = plt.subplot(gs[indw, indRegion+indf*len(animalLabels)])
            binsEdges = np.linspace(-1,1,60)
            ax.hist([sigModIGoodCells,nonsigModIGoodCells], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
            ax.set_title('Moving {}\n{}_good cells_{}'.format(movementDirections[indf],label,modWindow),fontsize=16)
            ax.text(-0.85, 0.5*plt.ylim()[1], '{} modulated out of {} cells: {:.3f}%'.format(sum(sigModGoodCells), len(sigModGoodCells), 100*float(sum(sigModGoodCells))/len(sigModGoodCells)))
            
    figTitle = 'reward_modulation_during_movement'
    plt.suptitle(figTitle, fontsize=25)    
    fig = plt.gcf()
    fig.text(0.5, 0.02, 'Modulation index', ha='center', va='center')
    fig.text(0.02, 0.5, 'Num of cells', ha='center', va='center', rotation='vertical')
    #plt.show()
    figFullPath = os.path.join(outputDir, figTitle)
    plt.savefig(figFullPath)


#--------------Sound -------------------#
plt.figure(figsize=(12,16))
gs = gridspec.GridSpec(2*len(modulationWindows['sound'])*len(freqLabels),len(animalLabels))
gs.update(left=0.08, right=0.98, top=0.9, bottom=0.05, wspace=0.2, hspace=0.3)
    for indf, freq in enumerate(freqLabels):
        #plt.clf()
        numWins = len(modulationWindows['sound'])
        for indw, modWindow in enumerate(modulationWindows['sound']):
            modIndName = 'modInd'+freq+'_'+modWindow+'_'+'sound'
            modSigName = 'modSig'+freq+'_'+modWindow+'_'+'sound'
            print 'For {}, there are {} good cells'.format(label, len(goodQualCells))
            allGoodCellsModInd = goodQualCells[modIndName]
            allGoodCellsModSig = goodQualCells[modSigName]
            sigModGoodCells = allGoodCellsModSig < alphaLevel
            sigModIGoodCells = allGoodCellsModInd[sigModGoodCells]
            nonsigModIGoodCells = allGoodCellsModInd[~sigModGoodCells]

            responsiveThisFreq = goodQualCells.behavZscore.apply(lambda x: abs(x[indf]) >= maxZThreshold)

            allGoodRespCellsThisFreq = goodQualCells[responsiveThisFreq]
            respCellsModInd = allGoodRespCellsThisFreq[modIndName]
            respCellsModSig = allGoodRespCellsThisFreq[modSigName]
            sigModRespCells = respCellsModSig < alphaLevel
            sigModIRespCells = respCellsModInd[sigModRespCells]
            nonsigModIRespCells = respCellsModInd[~sigModRespCells]
            # -- Plot reports -- #
            ax1 = plt.subplot(gs[2*indw+indf*numWins*2, indRegion])
            binsEdges = np.linspace(-1,1,60)
            ax1.hist([sigModIGoodCells,nonsigModIGoodCells], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
            ax1.set_title('{} freq\n{}_good cells_{}'.format(freq,label,modWindow),fontsize=16)
            ax1.text(-0.85, 0.5*plt.ylim()[1], '{} modulated out of {} cells: {:.3f}%'.format(sum(sigModGoodCells), len(sigModGoodCells), 100*float(sum(sigModGoodCells))/len(sigModGoodCells)))
            ax2 = plt.subplot(gs[2*indw+indf*numWins*2+1, indRegion])
            ax2.hist([sigModIRespCells,nonsigModIRespCells], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
            ax2.set_title('{} freq\n{}_sound responsive cells_{}'.format(freq,label,modWindow),fontsize=16)
            ax2.text(-0.85, 0.5*plt.ylim()[1], '{} modulated out of {} cells: {:.3f}%'.format(sum(sigModRespCells), len(sigModRespCells), 100*float(sum(sigModRespCells))/len(sigModRespCells)))     
        
    figTitle = 'reward_modulation_during_sound'
    plt.suptitle(figTitle, fontsize=25)    
    fig = plt.gcf()
    fig.text(0.5, 0.02, 'Modulation index', ha='center', va='center')
    fig.text(0.02, 0.5, 'Num of cells', ha='center', va='center', rotation='vertical')
    #plt.show()
    figFullPath = os.path.join(outputDir, figTitle)
    plt.savefig(figFullPath)
'''
