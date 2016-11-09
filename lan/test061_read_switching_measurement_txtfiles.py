'''
To select cells to plot, we need to check cell quality as well as many computed measures we defined in analysis, such as sound responsiveness, and whether modulated when mice going left versus going right etc.
Script with methods to read txt files generated from analysis of switching animals (maxZ sound score, ISI violation, modulation index, movement modulation index, minimal performance, minimal trials) and store them in dictionaries. Also looks at all cells and gets cluster quality, depth info.

Lan Guo 20160818
'''
# -- TO DO -- #
# file-reading functions should output not a dict with behavSessions as keys but preferrably a dataframe with behavSession as a col (so can sort by behavSession)
 
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


def read_sound_maxZ_file_switching_return_Df(maxZFilename):
    '''
    File foramt: file starts with behavSession line ('Behavior Session:behavSession\n'), followed by one line for each frequency (there are 3 frequencies in each session) in the task, each frequency line starts with the frequency, followed by a space ' ', then the maxZ scores separated by comma ',' .
    '''
    maxZFile = open(maxZFilename, 'r')
    #maxZsoundDict = {'maxZSoundLow':[],'maxZSoundMid':[],'maxZSoundHigh':[],'behavSession':[]}
    
    behavSessionCount=0 #for keeping track of how many behav session was processed
    '''
    while True:
        linesOneSession = read_nlines_from_txt_file(maxZFile, 4)
        if not linesOneSession:
            break
        behavLine = linesOneSession[0]
        if behavLine.startswith(codecs.BOM_UTF8):
            behavLine = line[3:]
        if (behavLine.split(':')[0] == 'Behavior Session'):
            behavName = behavLine.split(':')[1][:-1]  
            #behavSessionList.append(behavName)
            behavSessionCount+=1
            maxZsoundDict['behavSession'].extend([behavName]*cellNumPerSession)
        freqLowLine = linesOneSession[1]
        maxZsoundDict['maxZSoundLow'].extend([float(x) for x in freqLowLine.split()[1].split(',')[0:-1]])
        freqMidLine = linesOneSession[2]
        maxZsoundDict['maxZSoundMid'].extend([float(x) for x in freqMidLine.split()[1].split(',')[0:-1]])
        freqHighLine = linesOneSession[3]
        maxZsoundDict['maxZSoundHigh'].extend([float(x) for x in freqHighLine.split()[1].split(',')[0:-1]])
    '''
    class nestedDict(dict):#This is for maxZDict
        def __getitem__(self, item):
            try:
                return super(nestedDict, self).__getitem__(item)
            except KeyError:
                value = self[item] = type(self)()
                return value
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
        allFreqsSorted = sorted(int(maxZ) for maxZ in maxZDict[behavSession].keys()) #has to turn string (dic keys) to int for sorting by frequency!
        maxZAllFreqs = np.zeros((numCellsPerSession,3)) #initialize ndarray for all cells and all 3 frequencies in the switching task, some sessions may not have all 3 so those values will be zero
        for indf,freq in enumerate(allFreqsSorted):
            maxZThisFreq = maxZDict[behavSession][str(freq)] #has to turn the freq back to str
            maxZAllFreqs[:,indf] = maxZThisFreq
        thisSessionDf = pd.DataFrame({'behavSession':np.tile(behavSession,numCellsPerSession),'tetrode':np.repeat(range(1,9),12),'cluster':np.tile(range(1,13),8),'maxZSoundLow':maxZAllFreqs[:,0],'maxZSoundMid':maxZAllFreqs[:,1],'maxZSoundHigh':maxZAllFreqs[:,2]})
        maxZDf = maxZDf.append(thisSessionDf, ignore_index=True)
    
    #maxZsoundDf = pd.DataFrame(maxZsoundDict)     
    #print maxZsound[100:150]
    #maxZsoundDf.sort('behavSession',ascending=True,inplace=True)
    #maxZsoundDf = maxZsoundDf.reset_index(drop=True)
    #maxZsound = maxZsound.values() #This gets a numpy matrix of the values
    #return maxZsoundDf #This is a DataFrame with columns 'maxZSoundLow', 'maxZSoundMid', 'maxZSoundHigh', and 'behaveSession'
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


def read_mod_index_switching_return_Df(modIndexFilename):
    '''
    File format: each session's record starts with one line for the behavior session name (e.g. "Behavior Session:20160414a"). This is followed by a new line containing the modI values for every cluster for the middle frequency (start with 'modI:' modIndex separated by ','). Next is a new line containing the p value significance for the modulation of the middle frequency for every cluster (start with 'modSig:' mod significance separated by ','). Last new line is the modulation direction score ((start with 'modDir:' mod dir score separated by ',').  
    '''
    modIFile = open(modIndexFilename, 'r')
    modulationDict = {'modIndex':[],'modSig':[],'modDir':[],'behavSession':[],'tetrode':[],'cluster':[]} #stores all the modulation indices for the middle frequency
    #modSigDict = {} #stores the significance of the modulation of each cell
    #modDirectionScoreDict = {} #stores the score of how often the direction of modulation changes
    behavName = ''
    behavName = ''
    for line in modIFile:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        splitLine = line.split(':')
        if (splitLine[0] == 'Behavior Session'):
            behavName = splitLine[1][:-1]
            modulationDict['behavSession'].extend([behavName]*cellNumPerSession)
            modulationDict['tetrode'].extend(np.repeat(range(1,9),12))
            modulationDict['cluster'].extend(np.tile(range(1,13),8))
        elif (splitLine[0] == 'modI'):
            modulationDict['modIndex'].extend([float(x) for x in splitLine[1].split(',')[0:-1]])
        elif (splitLine[0] == 'modSig'):
            modulationDict['modSig'].extend([float(x) for x in splitLine[1].split(',')[0:-1]])
        elif (splitLine[0] == 'modDir'):
            modulationDict['modDir'].extend([float(x) for x in splitLine[1].split(',')[0:-1]])

    modIFile.close()
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
    CASE = 3
    if CASE == 0:
        switchingMice = ['test059','test017','test089','adap020']
        #switchingMice = ['adap020']
        #mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
        allMiceDfs = []

        for mouseName in switchingMice:
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
            maxZsoundDf = read_sound_maxZ_file_switching_return_Df(maxZFilename)
            #--Filter behavSessions by minPerformance --#
            maxZsoundDf = maxZsoundDf[maxZsoundDf['behavSession'].isin(minPerfList)]
            dfs.append(maxZsoundDf)

            #elif 'ISI' in filename:
            ISIFilename = os.path.join(processedDir,'ISI_Violations.txt')
            ISIDf = read_ISI_violation_file_return_Df(ISIFilename)
            dfs.append(ISIDf)

            #elif ('modIndex' in filename) & ('movement' not in filename):
            modulationFilename = os.path.join(processedDir,'modIndex.txt')
            modulationDf = read_mod_index_switching_return_Df(modulationFilename)
            dfs.append(modulationDf)

            #elif 'minTrial' in filename:
            minTrialFilename = os.path.join(processedDir,'minTrial.txt')
            minTrialDict = read_min_trial_file_return_dict(minTrialFilename) 

            #elif 'movement' in filename:
            movementIFilename = os.path.join(processedDir,'modIndex_LvsR_movement_0.05to0.15sec_window_'+mouseName)
            #if 'modIndex' in filename:
            if os.path.isfile(movementIFilename):
                movementIDf = read_movement_modI_return_Df(movementIFilename)
                dfs.append([movementIDf])
            movementSFilename = os.path.join(processedDir,'modSig_LvsR_movement_0.05to0.15sec_window_'+mouseName)
            #elif 'modSig' in filename:
            if os.path.isfile(movementSFilename):
                movementSDf = read_movement_modS_return_Df(movementSFilename)
                dfs.append([movementSDf])

            #--Joining all the resulting dataFrames on 'behavSession' column --#
            dfThisMouse = reduce(lambda left,right: pd.merge(left,right,on=['behavSession','tetrode','cluster'],how='inner'), dfs)
            #df_final.sort('behavSession',ascending=True,inplace=True)
            allMiceDfs.append(dfThisMouse)

        dfAllSwitchingMouse = pd.concat(allMiceDfs, ignore_index=True) 

        dfAllSwitchingMouse.to_hdf('/home/languo/data/ephys/switching_summary_stats/all_cells_all_measures.h5',key='switching')

    if CASE == 1:
        # -- Plot mod index histogram with ISI,quality,maxZMidFreq filters, color significantly modulated cells differently -- #
        dfAllSwitchingMouse = pd.read_hdf('/home/languo/data/ephys/switching_summary_stats/all_cells_all_measures.h5',key='switching')

        # -- Plot histogram of significantly modulated cells -- #
        import matplotlib.pyplot as plt

        #colors = ['b','g'] #blue for nonsignificantly modulated, green is significantly modulated
        qualityFilter = ((dfAllSwitchingMouse['cellQuality']==1) | (dfAllSwitchingMouse['cellQuality']==6))
        ISIFilter = dfAllSwitchingMouse['ISI']<=0.02
        sigModFilter = (dfAllSwitchingMouse['modSig']<=0.05)
        soundResponsiveFilter =  ((dfAllSwitchingMouse['maxZSoundMid']>=3) | (dfAllSwitchingMouse['maxZSoundMid']<=-3))
        #color = np.array([colors[i] for i in sigModFilter])

        # Plot modulation index for good quality cells only, color blue for nonsignificantly modulated, green is significantly modulated
        nonsigModulatedCells = dfAllSwitchingMouse['modIndex'][qualityFilter][soundResponsiveFilter][ISIFilter][~sigModFilter]
        sigModulatedCells = dfAllSwitchingMouse['modIndex'][qualityFilter][soundResponsiveFilter][ISIFilter][sigModFilter]
        plt.hist(nonsigModulatedCells, bins=60, color='grey')
        plt.hist(sigModulatedCells, bins=60, color='k')
        #plt.hist([nonsigModulatedCells,sigModulatedCells], bins=100, stacked=True)
        plt.title('{} cells recorded (good quality responsive to mid freq low ISI violation), {} cells significantly modulated'.format((len(nonsigModulatedCells)+len(sigModulatedCells)),len(sigModulatedCells)))
        plt.show()
  
    if CASE == 2:
        # -- Plot mod index histogram with ISI,quality,maxZMidFreq,and *modulation direction* filters, color significantly modulated cells differently -- #
        dfAllSwitchingMouse = pd.read_hdf('/home/languo/data/ephys/switching_summary_stats/all_cells_all_measures.h5',key='switching')

        # -- Plot histogram of significantly modulated cells -- #
        import matplotlib.pyplot as plt

        #colors = ['b','g'] #blue for nonsignificantly modulated, green is significantly modulated
        qualityFilter = ((dfAllSwitchingMouse['cellQuality']==1) | (dfAllSwitchingMouse['cellQuality']==6))
        ISIFilter = dfAllSwitchingMouse['ISI']<=0.02
        sigModFilter = (dfAllSwitchingMouse['modSig']<=0.05)
        soundResponsiveFilter =  ((dfAllSwitchingMouse['maxZSoundMid']>=3) | (dfAllSwitchingMouse['maxZSoundMid']<=-3))
        modDirFilter = dfAllSwitchingMouse['modDir']>=1
        #color = np.array([colors[i] for i in sigModFilter])

        # Plot modulation index for good quality cells only, color blue for nonsignificantly modulated, green is significantly modulated
        nonsigModulatedCells = dfAllSwitchingMouse['modIndex'][qualityFilter][soundResponsiveFilter][ISIFilter][modDirFilter][~sigModFilter] #check for quality,sound response(for midFreq),ISI,mod direction, no significant modulation index
        sigModulatedCells = dfAllSwitchingMouse['modIndex'][qualityFilter][soundResponsiveFilter][ISIFilter][modDirFilter][sigModFilter] #check for quality,sound response(for midFreq),ISI,mod direction, and significant modulation index
        plt.hist(nonsigModulatedCells, bins=60, color='grey')
        plt.hist(sigModulatedCells, bins=60, color='k')
        #plt.hist([nonsigModulatedCells,sigModulatedCells], bins=100, stacked=True)
        plt.title('{} cells total (good quality, responsive to mid freq, low ISI violation, modulation direction checked),\n {} cells significantly modulated'.format((len(nonsigModulatedCells)+len(sigModulatedCells)),len(sigModulatedCells)))

        plt.show()

    if CASE == 3:
        # -- Plot 2afc raster and PSTH for cells significantly modulated (with ISI,quality,maxZMidFreq criteria met, optional *check modulation directio* --#
        import numpy as np
        import matplotlib.pyplot as plt
        import os
        from jaratest.lan import test055_load_n_plot_billy_data_one_cell as plotter
        reload(plotter)
        
        dfAllSwitchingMouse = pd.read_hdf('/home/languo/data/ephys/switching_summary_stats/all_cells_all_measures.h5',key='switching')
        
        # -- This parameter sets whether to check for modulation direction score -- #
        checkModDir = True

        # -- Apply selection filters -- #
        qualityFilter = ((dfAllSwitchingMouse['cellQuality']==1) | (dfAllSwitchingMouse['cellQuality']==6))
        ISIFilter = dfAllSwitchingMouse['ISI']<=0.02
        sigModFilter = (dfAllSwitchingMouse['modSig']<=0.05)
        soundResponsiveFilter =  ((dfAllSwitchingMouse['maxZSoundMid']>=3) | (dfAllSwitchingMouse['maxZSoundMid']<=-3))
        nonsigModulatedCells = dfAllSwitchingMouse[qualityFilter][soundResponsiveFilter][ISIFilter][~sigModFilter]
        if checkModDir:
            modDirFilter = dfAllSwitchingMouse['modDir']>=1
            sigModulatedCells = dfAllSwitchingMouse[qualityFilter][soundResponsiveFilter][ISIFilter][modDirFilter][sigModFilter]
            outputDir = '/home/languo/data/ephys/switching_summary_stats/sigMod_withDirCheck/'
        else:
            sigModulatedCells = dfAllSwitchingMouse[qualityFilter][soundResponsiveFilter][ISIFilter][sigModFilter]
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
