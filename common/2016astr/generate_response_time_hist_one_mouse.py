'''
Generate intermediate data and plot a histogram of response times (time between center-out and side-in) for all good sessions of one mouse (recorded in psychometric task).
'''
import os
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
from scipy import stats
import pandas as pd
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)
import figparams
reload(figparams)

FIGNAME = '2afc_response_time'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_response_time' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [6,6]

mouse = 'test055'

# -- Read in databases storing all measurements from psycurve mice -- #
psychometricFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
psychometricFileName = 'all_cells_all_measures_waveform_psychometric.h5'
psychometricFullPath = os.path.join(psychometricFilePath,psychometricFileName)
allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')

# -- Access mounted behavior drive for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE

if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))
scriptFullPath = os.path.realpath(__file__)

allBehavSessions = np.unique(allcells_psychometric.loc[allcells_psychometric['animalName']==mouse, 'behavSession'].values)
resultsDict = {'animal':mouse, 'script':scriptFullPath}

allRespTimes = np.array([])
for behavSession in allBehavSessions:
    behavFileName = '{0}_{1}_{2}.h5'.format(mouse,'2afc',behavSession)
    behavFile = os.path.join(BEHAVIOR_PATH,mouse,behavFileName)
    bdata = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')
    validTrials = bdata['valid'].astype('bool') & (bdata['choice']!=bdata.labels['choice']['none'])
    timeCenterOut = bdata['timeCenterOut'][validTrials]
    timeSideIn = bdata['timeSideIn'][validTrials]
    responseTimes = timeSideIn-timeCenterOut
    resultsDict[behavSession] = responseTimes
    allRespTimes = np.concatenate((allRespTimes, responseTimes))
    if np.any(np.isnan(responseTimes)):
        print 'Session {}: Found Nan values in response time even though selecting for valid trials with a choice'.format(behavSession)

# -- Save response times for each session for one mouse -- #
outputFile = 'response_times_by_session_{}.npz'.format(mouse)
outputDataDir = os.path.join(dataDir,FIGNAME) 
if not os.path.exists(outputDataDir):
    os.mkdir(outputDataDir)
outputFullPath = os.path.join(outputDataDir,outputFile)
np.savez(outputFullPath, **resultsDict)   

# -- Plot hist -- #
plt.figure()
responseTimesToPlot = 1000*allRespTimes[~np.isnan(allRespTimes)] 
plt.hist(responseTimesToPlot, bins=1000)
plt.xlabel('response time (ms)')
plt.show()
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# -- Summary -- #
print 'Median response time is (in sec):', np.median(responseTimesToPlot), '\nSD of response time is:', np.std(responseTimesToPlot)
