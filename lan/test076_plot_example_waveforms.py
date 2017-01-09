import sys
import importlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratest.lan import test055_load_n_plot_billy_data_one_cell as loader
reload(loader)
import matplotlib.gridspec as gridspec

allcells = pd.read_hdf('/home/languo/data/ephys/switching_summary_stats/all_cells_all_measures_extra_mod_waveform_switching.h5',key='switching')

goodcells = allcells.loc[(allcells['cellQuality'].isin([1,6]))&(allcells['ISI']<=0.02)]

Na2K = abs(goodcells['peakNaAmp'] / goodcells['peakKAmp'])      
Cap2Na = abs(goodcells['peakCapAmp'] / goodcells['peakNaAmp'])
spkWidth = (goodcells['peakKTime'] - goodcells['peakNaTime']) #unit in sec

sigModSound = np.array(((goodcells['modSig']<=0.05)&(goodcells['modDir']>=1)),dtype=bool) 
sigModCenterout = np.array(((goodcells['modSig_-0.1-0s_center-out']<=0.05)&(goodcells['modDir_-0.1-0s_center-out']>=1)),dtype=bool)
soundResponsive = np.array((abs(goodcells['maxZSoundMid'])>=3),dtype=bool) 

dataToPlot = pd.DataFrame({'Na2K':Na2K,'spkWidth':1000*spkWidth,'Cap2Na':Cap2Na,'soundResponsive':soundResponsive,'sigModSound':sigModSound,'sigModCenterout':sigModCenterout})

CASE = 3
# -- Pick out some cells and plot their ave waveform to check -- #
if CASE == 1:
    wideSpikes = goodcells.loc[dataToPlot['spkWidth']>1.0]

    gs = gridspec.GridSpec(10,len(wideSpikes)/10+1)
    for cellInd in range(len(wideSpikes)):
        cell = wideSpikes.iloc[cellInd]
        cellParams = {'behavSession':cell['behavSession'],
                      'tetrode':cell['tetrode'],
                      'cluster':cell['cluster']}
        mouseName = cell['animalName']
        allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
        sys.path.append(settings.ALLCELLS_PATH)

        allcells = importlib.import_module(allcellsFileName)

        ### Using cellDB methode to find the index of this cell in the cellDB ###
        cellIndex = allcells.cellDB.findcell(mouseName,**cellParams)

        thisCell = allcells.cellDB[cellIndex]

        ax = plt.subplot(gs[cellInd])
        loader.plot_ave_wave_form_w_peak_times(thisCell)
        print 'plotting cell {}'.format(cellInd+1)

    plt.show()

if CASE == 2:
    import random
    narrowSpikes = goodcells.loc[dataToPlot['spkWidth']<0.2]
    narrowSpikesSmallCap = narrowSpikes.loc[dataToPlot.Cap2Na<0.5]
    
    samples = random.sample(range(len(narrowSpikesSmallCap)),30) #sampling without replacement
    
    gs = gridspec.GridSpec(10,len(samples)/10+1)
    for cellInd in range(len(samples)):
        cell = narrowSpikesSmallCap.iloc[cellInd]
        cellParams = {'behavSession':cell['behavSession'],
                      'tetrode':cell['tetrode'],
                      'cluster':cell['cluster']}
        mouseName = cell['animalName']
        allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
        sys.path.append(settings.ALLCELLS_PATH)

        allcells = importlib.import_module(allcellsFileName)

        ### Using cellDB methode to find the index of this cell in the cellDB ###
        cellIndex = allcells.cellDB.findcell(mouseName,**cellParams)

        thisCell = allcells.cellDB[cellIndex]

        ax = plt.subplot(gs[cellInd])
        loader.plot_ave_wave_form_w_peak_times(thisCell)
        print 'plotting cell {}'.format(cellInd+1)

    plt.show()

if CASE == 3: 
    import random
    goodcells = pd.read_hdf('/home/languo/data/ephys/switching_summary_stats/good_cells_all_measures_extra_mod_waveform_switching.h5',key='switching')
    
    for label in np.unique(goodcells.labels): #These are 'sCap2Na','mCap2Na','lCap2Na'
    #for label in [1]:    
        modulatedCells = goodcells.loc[(goodcells.labels==label) & (goodcells.modSig<=0.05)]
        plt.figure()
        if len(modulatedCells) <= 30:
            #Plot all ave waveforms
            gs = gridspec.GridSpec(10,len(modulatedCells)/10+1)
            for cellInd in range(len(modulatedCells)):
                cell = modulatedCells.iloc[cellInd]
                cellParams = {'behavSession':cell['behavSession'],
                              'tetrode':cell['tetrode'],
                              'cluster':cell['cluster']}
                mouseName = cell['animalName']
                allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
                sys.path.append(settings.ALLCELLS_PATH)

                allcells = importlib.import_module(allcellsFileName)

                ### Using cellDB methode to find the index of this cell in the cellDB ###
                cellIndex = allcells.cellDB.findcell(mouseName,**cellParams)

                thisCell = allcells.cellDB[cellIndex]

                ax = plt.subplot(gs[cellInd])
                loader.plot_ave_wave_form_w_peak_times(thisCell)
                print 'plotting cell {}'.format(cellInd+1)
            plt.suptitle('Average waveform for Cluster {} modulated cells'.format(label))
            plt.show()
        else:
            plt.figure()
            samples = random.sample(range(len(modulatedCells)),30)
            gs = gridspec.GridSpec(10,len(samples)/10+1)
            for cellInd in range(len(samples)):
                cell = modulatedCells.iloc[cellInd]
                cellParams = {'behavSession':cell['behavSession'],
                              'tetrode':cell['tetrode'],
                              'cluster':cell['cluster']}
                mouseName = cell['animalName']
                allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
                sys.path.append(settings.ALLCELLS_PATH)

                allcells = importlib.import_module(allcellsFileName)

                ### Using cellDB methode to find the index of this cell in the cellDB ###
                cellIndex = allcells.cellDB.findcell(mouseName,**cellParams)

                thisCell = allcells.cellDB[cellIndex]

                ax = plt.subplot(gs[cellInd])
                loader.plot_ave_wave_form_w_peak_times(thisCell)
                print 'plotting cell {}'.format(cellInd+1)
            plt.suptitle('Average waveform for Cluster {} modulated cells'.format(label))
            plt.show()
