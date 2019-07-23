import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#allcells = pd.read_hdf('/home/languo/data/ephys/switching_summary_stats/all_cells_all_measures_extra_mod_waveform_switching.h5',key='switching')
allcells =  pd.read_hdf('/home/languo/data/ephys/psychometric_summary_stats/all_cells_all_measures_waveform_psychometric.h5',key='psychometric')

goodQuality = (allcells['cellQuality'].isin([1,6]))&(allcells['ISI']<=0.02)
cellInStr = allcells['cellInStr']
#duplicateKept = allcells['keep_after_dup_test']
goodcells = allcells.loc[goodQuality&cellInStr]
#soundResponsive = np.array((abs(goodcells['maxZSoundMid'])>=3),dtype=bool)  #Switching mice
soundResponsive = np.array((abs(goodcells['maxZSoundMid1'])>=3)|(abs(goodcells['maxZSoundMid2'])>=3),dtype=bool)   #Psychometric mice
#goodcells = goodcells[abs(goodcells['maxZSoundMid'])>=3]
#color2 = ['modulated' if color[i]==1 else 'not modulated' for i in range(len(color))] 


CASE = 2

if CASE == 1:
    # -- Plot waveform parameters against each other for good cells -- #
    Na2K = abs(goodcells['peakNaAmp'] / goodcells['peakKAmp'])      
    Cap2Na = abs(goodcells['peakCapAmp'] / goodcells['peakNaAmp'])
    spkWidth = (goodcells['peakKTime'] - goodcells['peakNaTime']) #unit in sec
    sigModSound = np.array(((goodcells['modSig']<=0.05)&(goodcells['modDir']>=1)),dtype=bool) 
    sigModCenterout = np.array(((goodcells['modSig_-0.1-0s_center-out']<=0.05)&(goodcells['modDir_-0.1-0s_center-out']>=1)),dtype=bool)
    dataToPlot = pd.DataFrame({'Na2K':Na2K,'spkWidth':1000*spkWidth,'Cap2Na':Cap2Na,'soundResponsive':soundResponsive,'sigModSound':sigModSound,'sigModCenterout':sigModCenterout})  

    sns.set(font_scale=2) #This is to make fonts bigger

    '''
    # -- Plot Na/K peak ratio by cap/Na peak ratio -- # 
    g = sns.FacetGrid(dataToPlot, hue='soundResponsive', size=12, hue_kws={"marker": ["^", "v"], "color":['blue','red']})
    g.map(plt.scatter, 'Na2K', 'Cap2Na', edgecolor='white',s=20,alpha=0.7)
    g.set(xscale='log',yscale='log')
    g.set_ylabels('Cap peak to Na peak ratio (log scale)')
    g.set_xlabels('Na peak to K peak ratio (log scale)')
    plt.suptitle('All good cells from switching mice,\ncolored by whether significantly modulated during sound')
    g.add_legend()
    plt.show()
    '''
    numSoundResponsive = sum(soundResponsive)
    numModSoundRes = sum(soundResponsive&sigModCenterout)
    numNonSoundRes = sum(~soundResponsive)
    numModNonSR = sum((~soundResponsive)&sigModCenterout)

    # -- Plot Na/K peak ratio and cap/Na peak ratio by spike width -- # 
    for param in ['Na2K', 'Cap2Na']:
        #param = 'Cap2Na'
        #plt.clf()
        g = sns.FacetGrid(dataToPlot, col='soundResponsive', hue='sigModCenterout', hue_kws={"marker": ["^", "v"], "color":['blue','red'], "s":[20,26]})
        g.map(plt.scatter, param, 'spkWidth', edgecolor='white',alpha=0.7)
        g.set(xscale='log',yscale='log')
        g.set_xlabels('{} peak to {} peak ratio (log scale)'.format(param.split('2')[0],param.split('2')[1]))
        g.set_ylabels('spike width (time between Na&K peaks) ms (log scale)')
        g.add_legend()

        axisLims = g.axes[0][0].axis('tight')
        plt.suptitle('sound responsive: {} cells, modulated before center-out: {} cells,\nnot sound responsive: {} cells, modulated before center-out: {} cells'.format(numSoundResponsive,numModSoundRes,numNonSoundRes,numModNonSR))
        #plt.suptitle('All good cells from switching mice,\ncolored by whether significantly modulated during sound')

        #plt.axis('tight')
        #plt.autoscale(enable=True, axis='x', tight=True)
        plt.show()

elif CASE == 2:
    # -- Plot modulation index vs spike width or Cap2Na-peak-ratio for sound responsive good cells -- #
    soundResponsiveGoodCells = goodcells[soundResponsive]
    modIndex = abs(soundResponsiveGoodCells['modIndex'])
    Cap2Na = abs(soundResponsiveGoodCells['peakCapAmp'] / soundResponsiveGoodCells['peakNaAmp'])
    spkWidth = 1000*(soundResponsiveGoodCells['peakKTime'] - soundResponsiveGoodCells['peakNaTime']) #unit in msec

    sigModSound = np.array(((soundResponsiveGoodCells['modSig']<=0.05)&(soundResponsiveGoodCells['modDir']>=1)),dtype=bool) 
    
    for label,param in zip(['Capacitance peak to Na peak ratio (log)','spike width (K peak - Na peak) (log msec)'],[Cap2Na, spkWidth]):
        plt.figure()
        # -- Plot significantly modulated cells -- #
        plt.scatter(modIndex[sigModSound], param[sigModSound], color='r', marker='o')
        # -- Plot non-significantly modulated cells -- #
        plt.scatter(modIndex[~sigModSound], param[~sigModSound], color='k', marker='x')
        plt.yscale('log')
        #plt.xscale('log')
        plt.xlabel('modulation index (absolute value)')
        plt.ylabel(label)
        plt.show()
