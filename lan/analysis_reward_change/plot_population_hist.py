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

modulationWindows = ['0-0.1s_sound','0-0.1s_center-out']
freqLabels = ['Low','High']
#plotAll = True
#normalized = False
#logscaled = False

qualityThreshold = 2.5 #3 
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05
outputDir = '/home/languo/data/ephys/reward_change_stats/reports/'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

gs = gridspec.GridSpec(2*len(modulationWindows),len(animalLabels))
gs.update(left=0.08, right=0.98, top=0.9, bottom=0.1, wspace=0.25, hspace=0.5)

for indf, freq in enumerate(freqLabels):
    plt.clf()
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
    
        for indw, modWindow in enumerate(modulationWindows):
            modIndName = 'modInd'+freq+'_'+modWindow
            modSigName = 'modSig'+freq+'_'+modWindow
            #print 'For {}, there are {} good cells'.format(label, len(goodQualCells))
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
            ax1 = plt.subplot(gs[2*indw, indRegion])
            binsEdges = np.linspace(-1,1,60)
            ax1.hist([sigModIGoodCells,nonsigModIGoodCells], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
            ax1.set_title('{}_good cells_{}'.format(label,modWindow))
            ax1.text(-0.85, 0.5*plt.ylim()[1], '{} modulated out of {} cells: {:.3f}%'.format(sum(sigModGoodCells), len(sigModGoodCells), 100*float(sum(sigModGoodCells))/len(sigModGoodCells)))
            ax2 = plt.subplot(gs[2*indw+1, indRegion])
            ax2.hist([sigModIRespCells,nonsigModIRespCells], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
            ax2.set_title('{}_sound responsive cells_{}'.format(label,modWindow))
            ax2.text(-0.85, 0.5*plt.ylim()[1], '{} modulated out of {} cells: {:.3f}%'.format(sum(sigModRespCells), len(sigModRespCells), 100*float(sum(sigModRespCells))/len(sigModRespCells)))     
        
    figTitle = '{}_freq_reward_modulation'.format(freq)
    plt.suptitle(figTitle)    
    fig = plt.gcf()
    fig.text(0.5, 0.02, 'Modulation index', ha='center', va='center')
    fig.text(0.02, 0.5, 'Num of cells', ha='center', va='center', rotation='vertical')
    #plt.show()
    figFullPath = os.path.join(outputDir, figTitle)
    plt.savefig(figFullPath)

