'''
This script plots modulation index histogram in different windows:
0-0.1 sec after sound-onset or 0.05-0.25 sec after center-out.
To use in IPython console: 'run plot_reward_mod_ind_histogram_diff_window.py sound' or 'run plot_reward_mod_ind_histogram_diff_window.py center-out'
'''
import sys
import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import celldatabase
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.stats as stats

STUDY_NAME = '2018rc'
brainRegions = ['rightAStr', 'rightAC']
#animalList = ['adap005', 'adap012', 'adap013', 'adap015', 'adap017'] #['gosi001','gosi004','gosi008','gosi010','adap067','adap071']

modulationWindows = {'sound':'-0.2-0s',
                     'center-out': '0-0.3s',
                     'side-in': '-0.2-0s'}
freqLabels = ['Low','High']
movementDirections = ['Left', 'Right']

#qualityThreshold = 3 
maxZThreshold = 3
#ISIcutoff = 0.02
alphaLevel = 0.05
checkModDir = True #False

plt.figure(figsize=(6,6))
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
dbFolder = os.path.join(settings.DATABASE_PATH, 'new_celldb')
outputDir = '/home/languo/data/reports/reward_change/summaries'
figFormat = 'png'

celldbPath = os.path.join(dbFolder,'rc_database.h5')
#celldb = pd.read_hdf(celldbPath, key='reward_change')
celldb = celldatabase.load_hdf(celldbPath)

for indRegion, brainRegion in enumerate(brainRegions):    
    # -- For histogram of modulation index for sound-responsive cells, take the most responsive frequency -- #
    goodQualCells = celldb.query("keepAfterDupTest==1 and brainArea=='{}'".format(brainRegion))
    print brainRegion, ', number of good qual non-duplicated cell is ', len(goodQualCells)
    soundResp = goodQualCells.behavZscore.apply(lambda x: np.max(np.abs(x[~np.isnan(x)])) >=  maxZThreshold) #The bigger of the sound Z score is over threshold
    moreRespLowFreq = soundResp & goodQualCells.behavZscore.apply(lambda x: abs(x[~np.isnan(x)][0]) > abs(x[~np.isnan(x)][-1]))
    moreRespHighFreq = soundResp & goodQualCells.behavZscore.apply(lambda x: abs(x[~np.isnan(x)][-1]) > abs(x[~np.isnan(x)][0]))
    goodLowFreqRespCells = goodQualCells[moreRespLowFreq]
    goodHighFreqRespCells = goodQualCells[moreRespHighFreq]

    # -- For histogram of modulation index for movement-selective cells, take the preferred movement direction -- #
    movementSelective = goodQualCells['movementModS_[0.05, 0.15]'] < alphaLevel
    moreRespMoveLeft = movementSelective & (goodQualCells['movementModI_[0.05, 0.15]'] < 0)
    moreRespMoveRight = movementSelective & (goodQualCells['movementModI_[0.05, 0.15]'] > 0)
    goodLeftMovementSelCells = goodQualCells[moreRespMoveLeft]
    goodRightMovementSelCells = goodQualCells[moreRespMoveRight]


    if len(sys.argv) == 1:
        print 'Please provide which alignment you want to plot modulation index window with: sound, center-out, or side-in'
    elif len( sys.argv) == 2:
        alignment = sys.argv[1]
        # -- Plot reward modulation during sound only for sound-responsive cells -- #
        if alignment == 'sound':
            modWindow = modulationWindows['sound']
            lowFreqModIndName = 'modIndLow_'+modWindow+'_'+'sound'
            lowFreqModSigName = 'modSigLow_'+modWindow+'_'+'sound'
            lowFreqModDirName = 'modDirLow_'+modWindow+'_'+'sound'
            highFreqModIndName = 'modIndHigh_'+modWindow+'_'+'sound'
            highFreqModSigName = 'modSigHigh_'+modWindow+'_'+'sound'
            highFreqModDirName = 'modDirHigh_'+modWindow+'_'+'sound'
            
            goodLowFreqRespModInd = (-1) * goodLowFreqRespCells[lowFreqModIndName]
            goodLowFreqRespModSig = goodLowFreqRespCells[lowFreqModSigName]
            goodLowFreqRespModDir = goodLowFreqRespCells[lowFreqModDirName]
            goodHighFreqRespModInd = goodHighFreqRespCells[highFreqModIndName]
            goodHighFreqRespModSig = goodHighFreqRespCells[highFreqModSigName]
            goodHighFreqRespModDir = goodHighFreqRespCells[highFreqModDirName]
            
            if checkModDir:
                sigModulatedLow = (goodLowFreqRespModSig < alphaLevel) & (goodLowFreqRespModDir > 0)
                sigModulatedHigh = (goodHighFreqRespModSig < alphaLevel) & (goodHighFreqRespModDir > 0)
            else:
                sigModulatedLow = goodLowFreqRespModSig < alphaLevel
                sigModulatedHigh = goodHighFreqRespModSig < alphaLevel
            sigModI = np.concatenate((goodLowFreqRespModInd[sigModulatedLow].values,
                                      goodHighFreqRespModInd[sigModulatedHigh].values))
            nonsigModI = np.concatenate((goodLowFreqRespModInd[~sigModulatedLow].values,
                                      goodHighFreqRespModInd[~sigModulatedHigh].values))

            allModI = np.concatenate((goodLowFreqRespModInd.values, goodHighFreqRespModInd.values))
            Z, pVal = stats.wilcoxon(allModI)
            print 'Population mod ind mean: {:.2f}, compared to zero p value: {:.3f}'.format(np.mean(allModI), pVal)
            plt.clf()
            binsEdges = np.linspace(-1,1,20)
            plt.hist([sigModI,nonsigModI], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
            figTitle = '{}_{}_sound_sound_responsive_cells'.format(brainRegion,modWindow)
            #figTitle = '{}_{}_sound_responsive_cells'.format(animal,modWindow)
            plt.title(figTitle)
            plt.text(-0.85, 0.5*plt.ylim()[1], '{} modulated out of {} sound-responsive cells: {:.3f}%'.format(len(sigModI), sum(soundResp), 100*float(len(sigModI))/sum(soundResp)))  

            plt.xlabel('Modulation index')
            plt.ylabel('Num of cells')
            #plt.show()
            figFullPath = os.path.join(outputDir, figTitle)
            print 'Saving {} to {}'.format(figTitle, outputDir)
            plt.savefig(figFullPath,format=figFormat)


        # -- Plot reward modulation during movement only for movement-selective cells -- #
        elif alignment == 'center-out':
            modWindow = modulationWindows['center-out']
            leftModIndName = 'modIndLow_'+modWindow+'_'+'center-out'+'_removedsidein'
            leftModSigName = 'modSigLow_'+modWindow+'_'+'center-out'+'_removedsidein'
            leftModDirName = 'modDirLow_'+modWindow+'_'+'center-out'+'_removedsidein'
            rightModIndName = 'modIndHigh_'+modWindow+'_'+'center-out'+'_removedsidein'
            rightModSigName = 'modSigHigh_'+modWindow+'_'+'center-out'+'_removedsidein'
            rightModDirName = 'modDirHigh_'+modWindow+'_'+'center-out'+'_removedsidein'

            goodMovementSelCells = goodQualCells[movementSelective]
            sigModEitherDirection = (goodMovementSelCells[leftModSigName] < alphaLevel) | (goodMovementSelCells[rightModSigName] < alphaLevel)  
            print 'Out of {} movement-selective cells, {} were modulated by reward either going left or going right'.format(len(goodMovementSelCells), sum(sigModEitherDirection))
            goodLeftMovementSelModInd = (-1) * goodLeftMovementSelCells[leftModIndName]
            goodLeftMovementSelModSig = goodLeftMovementSelCells[leftModSigName]
            goodLeftMovementSelModDir = goodLeftMovementSelCells[leftModDirName]
            
            goodRightMovementSelModInd = goodRightMovementSelCells[rightModIndName]
            goodRightMovementSelModSig = goodRightMovementSelCells[rightModSigName]
            goodRightMovementSelModDir = goodRightMovementSelCells[rightModDirName]
            
            if checkModDir:
                sigModulatedLeft = (goodLeftMovementSelModSig < alphaLevel) & (goodLeftMovementSelModDir > 0)
                sigModulatedRight = (goodRightMovementSelModSig < alphaLevel) & (goodRightMovementSelModDir > 0)
            else:
                sigModulatedLeft = goodLeftMovementSelModSig < alphaLevel
                sigModulatedRight = goodRightMovementSelModSig < alphaLevel

            sigModI = np.concatenate((goodLeftMovementSelModInd[sigModulatedLeft].values,
                                      goodRightMovementSelModInd[sigModulatedRight].values))
            nonsigModI = np.concatenate((goodLeftMovementSelModInd[~sigModulatedLeft].values,
                                         goodRightMovementSelModInd[~sigModulatedRight].values))
            allModI = np.concatenate((goodLeftMovementSelModInd.values, goodRightMovementSelModInd.values))
            Z, pVal = stats.wilcoxon(allModI)
            print 'Population mod ind mean: {:.2f}, compared to zero p value: {:.3f}'.format(np.mean(allModI), pVal)
            plt.clf()
            binsEdges = np.linspace(-1,1,20)
            plt.hist([sigModI,nonsigModI], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
            figTitle = '{}_{}_Cout_movement_selective_cells'.format(brainRegion,modWindow)
            #figTitle = '{}_{}_movement_selective_cells'.format(animal,modWindow)
            plt.title(figTitle)
            plt.text(-0.85, 0.5*plt.ylim()[1], '{} modulated out of {} movement-selective cells: {:.3f}%'.format(len(sigModI), sum(movementSelective), 100*float(len(sigModI))/sum(movementSelective))) 
            plt.text(-0.9, 0.8*plt.ylim()[1], 'Out of {} movement-selective cells, {} were modulated \nby reward either going left or going right'.format(len(goodMovementSelCells), sum(sigModEitherDirection)))

            plt.xlabel('Modulation index')
            plt.ylabel('Num of cells')
            #plt.show()
            figFullPath = os.path.join(outputDir, figTitle)
            print 'Saving {} to {}'.format(figTitle, outputDir)
            plt.savefig(figFullPath,format=figFormat)

        # -- Plot reward modulation before side-in separately for low and high freq for all good cells -- #
        elif alignment == 'side-in':
            modWindow = modulationWindows['side-in']
            leftModIndName = 'modIndLow_'+modWindow+'_'+'side-in'
            leftModSigName = 'modSigLow_'+modWindow+'_'+'side-in'
            leftModDirName = 'modDirLow_'+modWindow+'_'+'side-in'
            rightModIndName = 'modIndHigh_'+modWindow+'_'+'side-in'
            rightModSigName = 'modSigHigh_'+modWindow+'_'+'side-in'
            rightModDirName = 'modDirHigh_'+modWindow+'_'+'side-in'

            goodLeftModInd = goodQualCells[leftModIndName]
            goodLeftModSig = goodQualCells[leftModSigName]
            goodLeftModDir = goodQualCells[leftModDirName]
            goodRightModInd = goodQualCells[rightModIndName]
            goodRightModSig = goodQualCells[rightModSigName]
            goodRightModDir = goodQualCells[rightModDirName]
                        
            if checkModDir:
                sigModulatedLeft = (goodLeftModSig < alphaLevel) & (goodLeftModDir > 0)
                sigModulatedRight = (goodRightModSig < alphaLevel) & (goodRightModDir > 0)
            else:
                sigModulatedLeft = goodLeftModSig < alphaLevel
                sigModulatedRight = goodRightModSig < alphaLevel

            sigModILeft = goodLeftModInd[sigModulatedLeft].values
            nonsigModILeft = goodLeftModInd[~sigModulatedLeft].values
            sigModIRight = goodRightModInd[sigModulatedRight].values
            nonsigModIRight = goodRightModInd[~sigModulatedRight]
            
            plt.clf()
            binsEdges = np.linspace(-1,1,20)
            plt.hist([sigModILeft,nonsigModILeft], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
            figTitle = '{}_{}_sideIn_lowfreq_good_cells'.format(brainRegion,modWindow)
            #figTitle = '{}_{}_movement_selective_cells'.format(animal,modWindow)
            plt.title(figTitle)
            plt.text(-0.85, 0.5*plt.ylim()[1], '{} modulated out of {} good cells: {:.3f}%'.format(len(sigModILeft), len(goodQualCells), 100*float(len(sigModILeft))/len(goodQualCells))) 
            
            plt.xlabel('Modulation index')
            plt.ylabel('Num of cells')
            #plt.show()
            figFullPath = os.path.join(outputDir, figTitle)
            print 'Saving {} to {}'.format(figTitle, outputDir)
            plt.savefig(figFullPath,format=figFormat)

            plt.clf()
            binsEdges = np.linspace(-1,1,20)
            plt.hist([sigModIRight,nonsigModIRight], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
            figTitle = '{}_{}_sideIn_highfreq_good_cells'.format(brainRegion,modWindow)
            plt.title(figTitle)
            plt.text(-0.85, 0.5*plt.ylim()[1], '{} modulated out of {} good cells: {:.3f}%'.format(len(sigModIRight), len(goodQualCells), 100*float(len(sigModIRight))/len(goodQualCells))) 
            
            plt.xlabel('Modulation index')
            plt.ylabel('Num of cells')
            #plt.show()
            figFullPath = os.path.join(outputDir, figTitle)
            print 'Saving {} to {}'.format(figTitle, outputDir)
            plt.savefig(figFullPath,format=figFormat)

