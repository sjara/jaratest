'''
Script to go through and read all the cell quality as well as the computed measures we defined in analysis, such as sound responsiveness, and whether modulated when mice going left versus going right etc.
Methods to read each type of txt files generated from analysis of psychometric curve animals (maxZ sound score, ISI violation, modulation index, movement modulation index, minimal performance, minimal trials) are in individual functions. Also check allcells files for cluster quality, depth info. The results will be concatenated into a pandas DataFrame. 

Lan Guo 20161118
'''

from jaratoolbox import settings
import os
import sys
import importlib
import re
import numpy as np
import pandas as pd
import codecs
cellNumPerSession = 96


def read_allcells_quality_depth(allcellsFilename):
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)
    cellsThisAnimal=allcells.cellDB
    cellQualityDf = pd.DataFrame(columns=['animalName','cellQuality','tetrode','cluster','behavSession','cellDepth'])
    #dtype=['str','int','int','int','str','float']
    for oneCell in cellsThisAnimal:
        cellQualityDf = cellQualityDf.append({'animalName':oneCell.animalName,'cellDepth':oneCell.depth,'cellQuality':oneCell.quality[oneCell.cluster-1],'tetrode':oneCell.tetrode,'cluster':oneCell.cluster,'behavSession':oneCell.behavSession}, ignore_index=True)
        
    return cellQualityDf


def read_nlines_from_txt_file(openedFile, n):
    '''
    Function to read n lines from a file given a file object.
    '''
    lines = [line for line in [openedFile.readline() for _ in range(n)] if len(line)]
    return lines


class nestedDict(dict): 
    #This is for making a dict that it returns a new instance (of dict) whenever a key is accessed but missing
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def read_sound_maxZ_file_psychometric_return_Df(maxZFilename):
    '''
    Reads txt files containing maximal Z scores of sound responses calculated by each chord frequencies presented in the 2afc psychometric curve task. 
    Text File foramt: file starts with behavSession line ('Behavior Session:behavSession\n'), followed by one line for each frequency (there are 6 frequencies in each session) in the task, each frequency line starts with the frequency, followed by a space ' ', then the maxZ scores separated by comma ',' .
    '''
    maxZFile = open(maxZFilename, 'r')
    
    behavSessionCount=0 #for keeping track of how many behav session was processed
    
    maxZDict = nestedDict()
    behavName = ''
    for line in maxZFile:
        behavLine = line.split(':')
        freqLine = line.split()
        if (behavLine[0] == 'Behavior Session'):
            behavName = behavLine[1][:-1]
        else:
            maxZDict[behavName][freqLine[0]] = freqLine[1].split(',')[0:-1]
    maxZFile.close()

    maxZDf = pd.DataFrame()
    numCellsPerSession = 96

    for behavSession in maxZDict.keys():
        allFreqsSorted = sorted(int(freq) for freq in maxZDict[behavSession].keys()) #has to turn string (dic keys) to int for sorting by frequency!
        maxZAllFreqs = np.zeros((numCellsPerSession,len(allFreqsSorted))) #initialize ndarray for all cells and all 6 frequencies in the psychometric task, some sessions may not have all 6 so those values will be zero
        for indf,freq in enumerate(allFreqsSorted):
            maxZThisFreq = maxZDict[behavSession][str(freq)] #has to turn the freq back to str
            maxZAllFreqs[:,indf] = maxZThisFreq
        thisSessionDf = pd.DataFrame({'behavSession':np.tile(behavSession,numCellsPerSession),'tetrode':np.repeat(range(1,9),12),'cluster':np.tile(range(1,13),8),'maxZSoundMid1':maxZAllFreqs[:,(len(allFreqsSorted)/2-1)],'maxZSoundMid2':maxZAllFreqs[:,len(allFreqsSorted)/2]})
        maxZDf = maxZDf.append(thisSessionDf, ignore_index=True)
    return maxZDf



def read_ISI_violation_file_return_Df(ISIFilename):
    '''
    File format: file starts with behavSession line ('Behavior Session:behavSession\n'), followed by one line for the ISI violation percentage for all possible clusters in this session, separated by comman ','.
    '''
    ISIFile = open(ISIFilename, 'r')
    behavSessionCount=0
    ISIDict = {'behavSession':[],'ISI':[],'tetrode':[],'cluster':[]}
    for line in ISIFile:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1] 
            behavSessionCount+=1
            ISIDict['behavSession'].extend([behavName]*cellNumPerSession)
            ISIDict['tetrode'].extend(np.repeat(range(1,9),12))
            ISIDict['cluster'].extend(np.tile(range(1,13),8))
        else:
            ISIDict['ISI'].extend([float(x) for x in line.split(',')[0:-1]])
    ISIFile.close()      
    ISIDf = pd.DataFrame(ISIDict)
    #print ISI[100:150]
    ISIDf.sort('behavSession',ascending=True,inplace=True)
    ISIDf = ISIDf.reset_index(drop=True)
    #ISI = ISI['ISI'].values()
    
    return ISIDf #This is a Df two cols: 'behavSession' and 'ISI'


def read_mod_index_psychometric_two_mid_freqs_return_Df(modIndexFilename):
    '''
    File format: each session's record starts with one line for the behavior session name (e.g. "Behavior Session:20160414a"). This is followed by a new line containing the modI values for every cluster for each frequency used in the task (start with 'modI:' modIndex separated by ','). Next is a new line containing the p value significance for the modulation of each frequency used in the task for every cluster (start with 'modSig:' mod significance separated by ',').   
    '''
    modIFile = open(modIndexFilename, 'r')
    modIDict = nestedDict()
    modSigDict = nestedDict()
    modulationDict = {'modIndexMid1':[],'modIndexMid2':[],'modSigMid1':[],'modSigMid2':[],'behavSession':[],'tetrode':[],'cluster':[]} 
    #store all the modulation indices for the two middle frequencies
    
    behavName = ''
    for line in modIFile:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        splitLine = line.split(':')
        if (splitLine[0] == 'Behavior Session'):
            behavName = splitLine[1][:-1]
        elif (splitLine[0] == 'modI'):
            modIDict[behavName][splitLine[1]] = [float(x) for x in splitLine[2].split(',')[0:-1]]
            
        elif (splitLine[0] == 'modSig'):
            modSigDict[behavName][splitLine[1]] = [float(x) for x in splitLine[2].split(',')[0:-1]]
    modIFile.close()
   
    for behavSession in modIDict.keys():
        modulationDict['behavSession'].extend([behavSession]*cellNumPerSession)
        modulationDict['tetrode'].extend(np.repeat(range(1,9),12))
        modulationDict['cluster'].extend(np.tile(range(1,13),8))
        freqs = sorted([int(key) for key in modIDict[behavSession].keys()])
        midFreq1 = freqs[len(freqs)/2-1]
        midFreq2 = freqs[len(freqs)/2]
        modulationDict['modIndexMid1'].extend(modIDict[behavSession][str(midFreq1)])
        modulationDict['modIndexMid2'].extend(modIDict[behavSession][str(midFreq2)])
        modulationDict['modSigMid1'].extend(modSigDict[behavSession][str(midFreq1)])
        modulationDict['modSigMid2'].extend(modSigDict[behavSession][str(midFreq2)])

    modulationDf = pd.DataFrame(modulationDict)
    modulationDf.sort('behavSession',ascending=True,inplace=True) #sort dataframe so that behavSessions are in ascending order
    modulationDf = modulationDf.reset_index(drop=True)
    return modulationDf


def read_movement_modI_return_Df(movementModIFilename):
    movementModIFile = open(movementModIFilename, 'r')
    movementModIDict = {'movementModI':[], 'behavSession':[], 'tetrode':[],'cluster':[]}
    
    for line in movementModIFile:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1]  
            #behavSessionList.append(behavName)
            #behavSessionCount+=1
            movementModIDict['behavSession'].extend([behavName]*cellNumPerSession)
            movementModIDict['tetrode'].extend(np.repeat(range(1,9),12))
            movementModIDict['cluster'].extend(np.tile(range(1,13),8))
        else:
            movementModIDict['movementModI'].extend([float(x) for x in line.split(',')[0:-1]])
    movementModIDf=pd.DataFrame(movementModIDict)
    movementModIDf.sort('behavSession',ascending=True,inplace=True)
    movementModIDf=movementModIDf.reset_index(drop=True)
    return movementModIDf


def read_movement_modS_return_Df(movementModSFilename):
    movementModSFile = open(movementModSFilename, 'r')
    movementModSDict = {'movementModS':[], 'behavSession':[], 'tetrode':[],'cluster':[]}
    
    for line in movementModSFile:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1]  
            #behavSessionList.append(behavName)
            #behavSessionCount+=1
            movementModSDict['behavSession'].extend([behavName]*cellNumPerSession)
            movementModSDict['tetrode'].extend(np.repeat(range(1,9),12))
            movementModSDict['cluster'].extend(np.tile(range(1,13),8))
        else:
            movementModSDict['movementModS'].extend([float(x) for x in line.split(',')[0:-1]])
    movementModSDf=pd.DataFrame(movementModSDict)
    movementModSDf.sort('behavSession',ascending=True,inplace=True)
    movementModSDf=movementModSDf.reset_index(drop=True)
    return movementModSDf


def read_min_performance_file_return_list(minPerfFilename):
    '''
    File format: file starts with one line describing the minimal performance criterion/cut-off, followed by all the session names for sessions that passed the cut-off, each session name is one line.
    '''
    minPerfFile = open(minPerfFilename, 'r')
    minPerfFile.readline()
    minPerfList=minPerfFile.read().split()
    minPerfFile.close()
    return minPerfList #This is a list of all sessions that passed the check (may not contain all behavSessions recorded in the all_cells file)


def read_min_trial_file_return_dict(minTrialFilename):
    '''
    File format: file starts with one line describing the minimal trial number criterion/cut-off. This line is followed by an empty line, then behavior sessions names (e.g. 20160229a) of all the sessions are listed, one on each line, along with the middle frequency presented in that session if it passed the min trial test (e.g. "20160412a: 11000") 
    '''
    minTrialFile = open(minTrialFilename, 'r')
    minTrialFile.readline()
    minTrialFile.readline()
    minTrialDict= {}
    for lineCount,line in enumerate(minTrialFile):
        minTrialStr = line.split(':')
        trialFreq = minTrialStr[1].split()
        minTrialDict.update({minTrialStr[0][1:]:trialFreq})
        # if the session's middle frequency does not pass the minimum trial criteria, the value of that session's key will be empty.
    minTrialFile.close()
    return minTrialDict #this is a dict with behav sessions as keys and mid freq as value if that session passed this check 




if __name__ == '__main__':
    CASE = 5
    if CASE == 0:
        import os

        wavefrom = True #Have generated all waveform data
        
        psychometricMice = ['adap013','adap017','adap015','test053','test055']
        #psychometricMice = ['adap013']
        
        allMiceDfs = []

        for mouseName in psychometricMice:
            allcellsFileName = 'allcells_'+mouseName+'_quality'
            #sys.path.append(settings.ALLCELLS_PATH)
            #allcells = importlib.import_module(allcellsFileName)
            cellQualityDf = read_allcells_quality_depth(allcellsFileName)

            # - Directory storing all computed measurements in txt files -- #
            #processedDir = os.path.join(settings.EPHYS_PATH,mouseName,mouseName+'_stats')
            processedDir = os.path.join('/home/languo/data/jarastorephys',mouseName+'_processed')
            #measurementFiles = [os.path.join(processedDir, f) for f in os.listdir(processedDir) if os.path.isfile(os.path.join(processedDir, f))]
            dfs = []
            dfs.append(cellQualityDf)

            #for filename in measurementFiles:
            #if 'maxZVal' in filename:
            #elif 'minPerformance' in filename:
            minPerfFilename = os.path.join(processedDir,'minPerformance.txt')
            minPerfList = read_min_performance_file_return_list(minPerfFilename)

            maxZFilename = os.path.join(processedDir,'maxZVal.txt')
            maxZsoundDf = read_sound_maxZ_file_psychometric_return_Df(maxZFilename)
            #--Filter behavSessions by minPerformance --#
            maxZsoundDf = maxZsoundDf[maxZsoundDf['behavSession'].isin(minPerfList)]
            dfs.append(maxZsoundDf)

            #elif 'ISI' in filename:
            ISIFilename = os.path.join(processedDir,'ISI_Violations.txt')
            ISIDf = read_ISI_violation_file_return_Df(ISIFilename)
            dfs.append(ISIDf)

            #elif ('modIndex' in filename) & ('movement' not in filename):
            modulationFilename = os.path.join(processedDir,'modIndex.txt')
            modulationDf = read_mod_index_psychometric_two_mid_freqs_return_Df(modulationFilename)
            dfs.append(modulationDf)

            #elif 'minTrial' in filename:
            # Right now minTrialDict is not used
            minTrialFilename = os.path.join(processedDir,'minTrial.txt')
            minTrialDict = read_min_trial_file_return_dict(minTrialFilename) 

            #elif 'movement' in filename:
            movementIFilename = os.path.join(processedDir,'modIndex_LvsR_movement_0.05to0.15sec_window_'+mouseName+'.txt')
            #if 'modIndex' in filename:
            if os.path.isfile(movementIFilename):
                movementIDf = read_movement_modI_return_Df(movementIFilename)
                dfs.append(movementIDf)
            movementSFilename = os.path.join(processedDir,'modSig_LvsR_movement_0.05to0.15sec_window_'+mouseName+'.txt')
            #elif 'modSig' in filename:
            if os.path.isfile(movementSFilename):
                movementSDf = read_movement_modS_return_Df(movementSFilename)
                dfs.append(movementSDf)

            #--Joining all the resulting dataFrames on 'behavSession' column --#
            dfThisMouse = reduce(lambda left,right: pd.merge(left,right,on=['behavSession','tetrode','cluster'],how='inner'), dfs)
            #df_final.sort('behavSession',ascending=True,inplace=True)
            allMiceDfs.append(dfThisMouse)

        dfAllPsychometricMouse = pd.concat(allMiceDfs, ignore_index=True) 
        dfAllPsychometricMouse['script']= os.path.realpath(__file__)

        dfAllPsychometricMouse.to_hdf('/home/languo/data/ephys/psychometric_summary_stats/all_cells_all_measures_psychometric.h5',key='psychometric')

    if CASE == 1:
        # -- Plot mod index histogram with ISI,quality,maxZMidFreq filters, color significantly modulated cells differently -- #
        dfAllPsychometricMouse = pd.read_hdf('/home/languo/data/ephys/psychometric_summary_stats/all_cells_all_measures_psychometric.h5',key='psychometric')

        # -- Plot histogram of significantly modulated cells -- #
        import matplotlib.pyplot as plt

        #colors = ['b','g'] #blue for nonsignificantly modulated, green is significantly modulated
        for freq in ['Mid1','Mid2']:
            qualityFilter = ((dfAllPsychometricMouse['cellQuality']==1) | (dfAllPsychometricMouse['cellQuality']==6))
            ISIFilter = dfAllPsychometricMouse['ISI']<=0.02
            sigModFilter = (dfAllPsychometricMouse['modSig'+freq]<=0.05)
            soundResponsiveFilter =  ((dfAllPsychometricMouse['maxZSound'+freq]>=3) | (dfAllPsychometricMouse['maxZSound'+freq]<=-3))
            #color = np.array([colors[i] for i in sigModFilter])

            # Plot modulation index for good quality cells only, color grey for nonsignificantly modulated, black is significantly modulated
            nonsigModulatedCells = dfAllPsychometricMouse['modIndex'+freq][qualityFilter][soundResponsiveFilter][ISIFilter][~sigModFilter]
            sigModulatedCells = dfAllPsychometricMouse['modIndex'+freq][qualityFilter][soundResponsiveFilter][ISIFilter][sigModFilter]
            plt.figure()
            #plt.hist(nonsigModulatedCells, bins=60, color='grey')
            #plt.hist(sigModulatedCells, bins=60, color='k')
            plt.hist([nonsigModulatedCells,sigModulatedCells], color=['grey','black'], bins=50, stacked=False)
            plt.title('{} cells recorded (good quality responsive to {} freq low ISI violation), {} cells significantly modulated'.format((len(nonsigModulatedCells)+len(sigModulatedCells)),freq,len(sigModulatedCells)))
            plt.show()


    if CASE == 2:
        # -- Plot mod index histogram with ISI,quality,maxZMidFreq filters, color significantly modulated cells differently. Polling cells sound-responsive to either mid freq -- #
        dfAllPsychometricMouse = pd.read_hdf('/home/languo/data/ephys/psychometric_summary_stats/all_cells_all_measures_psychometric.h5',key='psychometric')

        # -- Plot histogram of significantly modulated cells -- #
        import matplotlib.pyplot as plt

        #colors = ['b','g'] #blue for nonsignificantly modulated, green is significantly modulated
        
        qualityFilter = ((dfAllPsychometricMouse['cellQuality']==1) | (dfAllPsychometricMouse['cellQuality']==6))
        ISIFilter = dfAllPsychometricMouse['ISI']<=0.02
        sigModFilter1 = (dfAllPsychometricMouse['modSigMid1']<=0.05) 
        sigModFilter2 = (dfAllPsychometricMouse['modSigMid2']<=0.05)
        soundResponsiveFilter1 = ((dfAllPsychometricMouse['maxZSoundMid1']>=3) | (dfAllPsychometricMouse['maxZSoundMid1']<=-3)) 
        soundResponsiveFilter2 = ((dfAllPsychometricMouse['maxZSoundMid2']>=3) | (dfAllPsychometricMouse['maxZSoundMid2']<=-3))
        dfSigMidFreq1 = dfAllPsychometricMouse[qualityFilter][ISIFilter][soundResponsiveFilter1][sigModFilter1]
        dfNonSigMidFreq1 = dfAllPsychometricMouse[qualityFilter][ISIFilter][soundResponsiveFilter1][~sigModFilter1]
        dfSigMidFreq2 = dfAllPsychometricMouse[qualityFilter][ISIFilter][soundResponsiveFilter2][sigModFilter2]
        dfNonSigMidFreq2 = dfAllPsychometricMouse[qualityFilter][ISIFilter][soundResponsiveFilter2][~sigModFilter2]

        # Plot modulation index for each middle freq separately. color grey for nonsignificantly modulated, black is significantly modulated, blue is cells significantly modulated in the other middle freq
        plt.figure()
        nonsigModulatedCells = dfNonSigMidFreq1['modIndexMid1']
        sigModulatedCells = dfSigMidFreq1['modIndexMid1']
        cellsSigModOtherFreq = dfSigMidFreq2['modIndexMid1']
        plt.hist([nonsigModulatedCells,sigModulatedCells,cellsSigModOtherFreq], color=['grey','black','blue'], bins=50, stacked=True)
        plt.title('{} cells recorded (good quality responsive to {} freq low ISI violation), {} cells significantly modulated'.format((len(nonsigModulatedCells)+len(sigModulatedCells)),'Mid1',len(sigModulatedCells)))

        plt.figure()
        nonsigModulatedCells = dfNonSigMidFreq2['modIndexMid2']
        sigModulatedCells = dfSigMidFreq2['modIndexMid2']
        cellsSigModOtherFreq = dfSigMidFreq1['modIndexMid2']
        plt.hist([nonsigModulatedCells,sigModulatedCells,cellsSigModOtherFreq], color=['grey','black','blue'], bins=50, stacked=True)
        plt.title('{} cells recorded (good quality responsive to {} freq low ISI violation), {} cells significantly modulated'.format((len(nonsigModulatedCells)+len(sigModulatedCells)),'Mid2',len(sigModulatedCells)))
        plt.show()

    if CASE == 3:
        # -- Find cells that are sound-responsive to either middle freq, plot their 2 modulation indexes against each other and color them according to significance -- #
        dfAllPsychometricMouse = pd.read_hdf('/home/languo/data/ephys/psychometric_summary_stats/all_cells_all_measures_psychometric.h5',key='psychometric')

        # -- Plot histogram of significantly modulated cells -- #
        import matplotlib.pyplot as plt

        qualityFilter = ((dfAllPsychometricMouse['cellQuality']==1) | (dfAllPsychometricMouse['cellQuality']==6))
        ISIFilter = dfAllPsychometricMouse['ISI']<=0.02
        sigModFilter1 = (dfAllPsychometricMouse['modSigMid1']<=0.05) 
        sigModFilter2 = (dfAllPsychometricMouse['modSigMid2']<=0.05)
        soundResponsiveFilter1 = ((dfAllPsychometricMouse['maxZSoundMid1']>=3) | (dfAllPsychometricMouse['maxZSoundMid1']<=-3)) 
        soundResponsiveFilter2 = ((dfAllPsychometricMouse['maxZSoundMid2']>=3) | (dfAllPsychometricMouse['maxZSoundMid2']<=-3))
        dfModulatedEitherFreq = dfAllPsychometricMouse[ISIFilter][qualityFilter](sigMod)

    if CASE == 4:
        # -- Plot 2afc raster and PSTH for cells significantly modulated (with ISI,quality,maxZMidFreq criteria met, optional *check modulation directio* --#
        import numpy as np
        import matplotlib.pyplot as plt
        import os
        from jaratest.lan import test055_load_n_plot_billy_data_one_cell as plotter
        reload(plotter)
        
        dfAllPsychometricMouse = pd.read_hdf('/home/languo/data/ephys/psychometric_summary_stats/all_cells_all_measures_psychometric.h5',key='psychometric')
        
        # -- This parameter sets whether to check for modulation direction score -- #
        checkModDir = True

        # -- Apply selection filters -- #
        qualityFilter = ((dfAllPsychometricMouse['cellQuality']==1) | (dfAllPsychometricMouse['cellQuality']==6))
        ISIFilter = dfAllPsychometricMouse['ISI']<=0.02
        sigModFilter = (dfAllPsychometricMouse['modSig']<=0.05)
        soundResponsiveFilter =  ((dfAllPsychometricMouse['maxZSoundMid']>=3) | (dfAllPsychometricMouse['maxZSoundMid']<=-3))
        nonsigModulatedCells = dfAllPsychometricMouse[qualityFilter][soundResponsiveFilter][ISIFilter][~sigModFilter]
        if checkModDir:
            modDirFilter = dfAllPsychometricMouse['modDir']>=1
            sigModulatedCells = dfAllPsychometricMouse[qualityFilter][soundResponsiveFilter][ISIFilter][modDirFilter][sigModFilter]
            outputDir = '/home/languo/data/ephys/switching_summary_stats/sigMod_withDirCheck/'
        else:
            sigModulatedCells = dfAllPsychometricMouse[qualityFilter][soundResponsiveFilter][ISIFilter][sigModFilter]
            outputDir = '/home/languo/data/ephys/switching_summary_stats/sigMod_noDirCheck/'
        
        for animal in np.unique(sigModulatedCells['animalName']):
            allcellsFileName = 'allcells_'+animal+'_quality'
            sys.path.append(settings.ALLCELLS_PATH)
            allcells = importlib.import_module(allcellsFileName)
            
            cellsThisAnimal = sigModulatedCells[sigModulatedCells['animalName']==animal]
            # Loop through all the cells in one mouse, plot 2afc raster and PSTH
            for ind, cell in cellsThisAnimal.iterrows():
                cellParams = {'behavSession':cell['behavSession'],
                              'tetrode':cell['tetrode'],
                              'cluster':cell['cluster']}

                ### Using cellDB methode to find the index of this cell in the cellDB ###
                cellIndex = allcells.cellDB.findcell(animal,**cellParams)
                thisCell = allcells.cellDB[cellIndex]
                
                ### Plot 2afc raster and PSTH by block ###
                plt.style.use(['seaborn-white', 'seaborn-talk']) 
                plt.figure()
                plotter.plot_switching_raster(thisCell, freqToPlot='middle', alignment='sound',timeRange=[-0.5,1],byBlock=True)
                filePath = outputDir
                if not os.path.exists(filePath):
                    os.makedirs(filePath)
                date = cell['behavSession'][:-1]
                tetrode=cell['tetrode']
                cluster=cell['cluster']
                plotter.save_report_plot(animal,date,tetrode,cluster,filePath,chartType='raster')

                plt.figure()
                plotter.plot_switching_PSTH(thisCell, freqToPlot='middle', alignment='sound',timeRange=[-0.5,1],byBlock=True, binWidth=0.010)
                plotter.save_report_plot(animal,date,tetrode,cluster,filePath,chartType='PSTH')

    if CASE == 5:
        # -- Add 'script' field to database to indicate which script generated it -- #

        import pandas as pd
        import os
        
        dfAllPsychometricMouse = pd.read_hdf('/home/languo/data/ephys/psychometric_summary_stats/all_cells_all_measures_psychometric.h5',key='psychometric')
        scriptFullPath = os.path.realpath(__file__)
        dfAllPsychometricMouse['script'] = scriptFullPath
        dfAllPsychometricMouse.to_hdf('/home/languo/data/ephys/psychometric_summary_stats/all_cells_all_measures_psychometric.h5',key='psychometric')
