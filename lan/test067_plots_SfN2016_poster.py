'''
Script to generate figure plots for SfN 2016 poster

Lan Guo 2016-11-03
'''

import sys
import os
import importlib
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratest.billy.scripts import celldatabase_quality_tuning as cellDB
from jaratest.lan import test055_load_n_plot_billy_data_one_cell as switchingPlotter
reload(switchingPlotter)
from jaratest.lan import test022_plot2afc_given_cell_rew_change as rcPlotter
reload(rcPlotter)
'''
from jaratest.nick.database import dataplotter 
from jaratoolbox import settings
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import spikesorting
from jaratoolbox import ephyscore
'''
import matplotlib
matplotlib.rcParams['font.family'] = 'Helvetica'
#matplotlib.rcParams['font.family'] = 'Whitney-Medium'
matplotlib.rcParams['svg.fonttype'] = 'none'  

CASE = 3
if CASE == 1:
    from jaratoolbox import extraplots
    # -- Plot 2afc switching raster and PSTH examples -- #
    ### Params associated with the cell of interest ###
    cellParamsList = [('adap020',{'behavSession':'20160418a',
                                  'tetrode':6,
                                  'cluster':8}),
                      ('adap020',{'behavSession':'20160524a',
                                  'tetrode':2,
                                  'cluster':9}),
                      ('test059',{'behavSession':'20150624a',
                                  'tetrode':1,
                                  'cluster':2}),
                       ('test089',{'behavSession':'20160124a',
                                  'tetrode':4,
                                  'cluster':6})]

    for (mouseName, cellParams) in cellParamsList:
        ### Loading allcells file for a specified mouse ###
        #allcellsFileName = 'allcells_'+mouseName
        allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
        sys.path.append(settings.ALLCELLS_PATH)

        allcells = importlib.import_module(allcellsFileName)

        ### Using cellDB methode to find the index of this cell in the cellDB ###
        cellIndex = allcells.cellDB.findcell(mouseName,**cellParams)
        #pdb.set_trace()
        # TEST, plotting cells with sig modulation in 20150624a behav session

        thisCell = allcells.cellDB[cellIndex]
        ephysSession = thisCell.ephysSession
        tuningSession = thisCell.tuningSession
        tuningBehavior = thisCell.tuningBehavior

        #(eventOnsetTimes, spikeTimestamps, bData) = load_remote_tuning_data(thisCell,BEHAVDIR_MOUNTED,EPHYSDIR_MOUNTED)
        #plt.style.use(['seaborn-white', 'seaborn-talk']) 
        #plt.figure()
        #plot_tuning_raster_one_intensity(thisCell)
        #plt.figure()
        #plot_tuning_PSTH_one_intensity(thisCell,timeRange=[-0.3,0.4],halfFreqs=True)
        #movement-selectivity plot
        filePath = '/tmp'
        plt.figure()
        switchingPlotter.plot_switching_raster(thisCell, freqToPlot='middle', alignment='sound',timeRange=[-0.3,0.5],byBlock=True)
        extraplots.boxoff(plt.gca())
        switchingPlotter.save_report_plot(thisCell.animalName,thisCell.behavSession,thisCell.tetrode,thisCell.cluster,filePath,chartType='raster',figFormat='svg')
        plt.figure()
        switchingPlotter.plot_switching_PSTH(thisCell, freqToPlot='middle', alignment='sound',timeRange=[-0.3,0.5],byBlock=False, binWidth=0.010)
        extraplots.boxoff(plt.gca())
        switchingPlotter.save_report_plot(thisCell.animalName,thisCell.behavSession,thisCell.tetrode,thisCell.cluster,filePath,chartType='PSTH',figFormat='svg')
    
        plt.show()
   
elif CASE == 2:
    from jaratoolbox import extraplots
    # -- Plot reward change raster and PSTH examples -- #
    ### Params associated with the cell of interest ###
    cellParamsListSound = [('adap012',{'behavSession':'20160212a',
                                  'tetrode':3,
                                  'cluster':5}),
                           ('adap012',{'behavSession':'20160203a',
                                  'tetrode':3,
                                       'cluster':7})]
    cellParamsListCenterOut = [('adap012',{'behavSession':'20160204a',
                                  'tetrode':3,
                                  'cluster':3}),
                               ('adap012',{'behavSession':'20160213a',
                                  'tetrode':2,
                                   'cluster':10})]

    for (mouseName, cellParams) in cellParamsListSound:
        ### Loading allcells file for a specified mouse ###
        allcellsFileName = 'allcells_'+mouseName
        #allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
        sys.path.append(settings.ALLCELLS_PATH)
        allcells = importlib.import_module(allcellsFileName)

        ### Using cellDB methode to find the index of this cell in the cellDB ###
        cellIndex = allcells.cellDB.findcell(mouseName,**cellParams)
        #pdb.set_trace()
        # TEST, plotting cells with sig modulation in 20150624a behav session

        thisCell = allcells.cellDB[cellIndex]
        
        filePath = '/tmp'
        #plt.figure()
        rcPlotter.plot_rew_change_per_cell_raster(thisCell,alignment='sound',freqToPlot='right',byBlock=True, timeRange=[-0.3,0.5],binWidth=0.010)
        #plt.show()
        extraplots.boxoff(plt.gca())
        switchingPlotter.save_report_plot(thisCell.animalName,thisCell.behavSession,thisCell.tetrode,thisCell.cluster,filePath,chartType='raster',figFormat='svg')
        rcPlotter.plot_rew_change_per_cell_PSTH(thisCell,alignment='sound',freqToPlot='right',byBlock=False, timeRange=[-0.3,0.5],binWidth=0.010)
        #plt.show()
        extraplots.boxoff(plt.gca())
        switchingPlotter.save_report_plot(thisCell.animalName,thisCell.behavSession,thisCell.tetrode,thisCell.cluster,filePath,chartType='PSTH',figFormat='svg')
        
    for (mouseName, cellParams) in cellParamsListCenterOut:
        ### Loading allcells file for a specified mouse ###
        allcellsFileName = 'allcells_'+mouseName
        #allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
        sys.path.append(settings.ALLCELLS_PATH)
        allcells = importlib.import_module(allcellsFileName)

        ### Using cellDB methode to find the index of this cell in the cellDB ###
        cellIndex = allcells.cellDB.findcell(mouseName,**cellParams)
        #pdb.set_trace()
        # TEST, plotting cells with sig modulation in 20150624a behav session

        thisCell = allcells.cellDB[cellIndex]
        
        filePath = '/tmp'
        plt.figure()
        rcPlotter.plot_rew_change_per_cell_raster(thisCell,alignment='center-out',freqToPlot='right',byBlock=True, timeRange=[-0.4,0.6],binWidth=0.010)
        #plt.show()
        extraplots.boxoff(plt.gca())
        switchingPlotter.save_report_plot(thisCell.animalName,thisCell.behavSession,thisCell.tetrode,thisCell.cluster,filePath,chartType='raster',figFormat='svg')
        rcPlotter.plot_rew_change_per_cell_PSTH(thisCell,alignment='center-out',freqToPlot='right',byBlock=False, timeRange=[-0.4,0.6],binWidth=0.010)
        #plt.show()
        extraplots.boxoff(plt.gca())
        switchingPlotter.save_report_plot(thisCell.animalName,thisCell.behavSession,thisCell.tetrode,thisCell.cluster,filePath,chartType='PSTH',figFormat='svg')
        
        #plt.show()
       
elif CASE == 3:
    import pandas as pd
    import scipy.stats as stats
    df = pd.read_csv('/home/languo/data/behavior_reports/avePercentR_byStimType_byFreq.csv')   
    df.set_index(['freq_label','stim_type'],inplace=True)
    df.sortlevel(inplace=True)
    #highFreqLeftStim = df.iloc[df.index.isin([('high', 'left')])]  #Alternative,w/t sortlevel 
    diffHighFreqLeftStim = df.loc['high','left']['ave_performance_stim'] - df.loc['high','left']['ave_performance_baseline']
    diffLowFreqLeftStim = df.loc['low','left']['ave_performance_stim'] - df.loc['low','left']['ave_performance_baseline']
    diffHighFreqRightStim = df.loc['high','right']['ave_performance_stim'] - df.loc['high','right']['ave_performance_baseline']
    diffLowFreqRightStim = df.loc['low','right']['ave_performance_stim'] - df.loc['low','right']['ave_performance_baseline']
    
    pHighFreqLeftStim = stats.wilcoxon(diffHighFreqLeftStim)
    pLowFreqLeftStim = stats.wilcoxon(diffLowFreqLeftStim)
    pHighFreqRightStim = stats.wilcoxon(diffHighFreqRightStim)
    pLowFreqRightStim = stats.wilcoxon(diffLowFreqRightStim)
    
    print pHighFreqLeftStim,pLowFreqLeftStim,pHighFreqRightStim,pLowFreqRightStim
