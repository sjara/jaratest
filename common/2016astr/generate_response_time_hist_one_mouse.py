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

dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_photostim_tuning_vs_bias' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [6,6]

mouse = 'test059'

# -- Read in databases storing all measurements from psycurve mice -- #
psychometricFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
psychometricFileName = 'all_cells_all_measures_waveform_psychometric.h5'
psychometricFullPath = os.path.join(psychometricFilePath,psychometricFileName)
allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')

# -- Access mounted behavior drive for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE

if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

allBehavSessions = np.unique(allcells_psychometric.loc[allcells_psychometric['animalName']==mouse, 'behavSession'])
