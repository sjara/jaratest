import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
from numpy import array
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
import studyparams

reload(studyparams)
startTime = time.time()

dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,'responsivedb_{}.h5'.format(studyparams.STUDY_NAME))
#dbFilename = os.path.join(dbPath,'signRespCellsdb_{}.h5'.format(studyparams.STUDY_NAME))
# -- Load the database of cells --
celldb = celldatabase.load_hdf(dbFilename)

binWidth = 0.01
responseRange = [0, 0.1] # seconds
timeRange = [-0.1, 0.4]  # In seconds

predictionNeuronHigh = []
predictionNeuronMid = []
posPredErrorNeuronHigh = []
posPredErrorNeuronMid = []

predictionNeuronMidD = []
predictionNeuronLowD = []
posPredErrorNeuronMidD = []
posPredErrorNeuronLowD = []
count = 0
for indRow,dbRow in celldb.iterrows():
    # -- ASCENDING --
    # -- Middle frequency prediction neuron --
    if (celldb['meanEvokedFirstOddA'][indRow] > celldb['meanEvokedFirstStdA'][indRow]) and (celldb['pValHighFRA'][indRow] < 0.05):
        predictionNeuronMid.append(celldb.iloc[indRow])
        print('{} {} {:.0f}um T{} c{} is a mid freq pred neuron.'.format(dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster']))
    # -- Middle frequency positive prediction error neuron --
    if (celldb['meanEvokedSecondOddA'][indRow] > celldb['meanEvokedSecondStdA'][indRow]) and (celldb['pValMidFRA'][indRow] < 0.05):
        posPredErrorNeuronMid.append(celldb.iloc[indRow])
        #print('{} {} {:.0f}um T{} c{} is a mid freq pos pred error neuron.'.format(dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster']))
    # -- High frequency positive prediction error neuron --
    if (celldb['meanEvokedFirstOddA'][indRow] > celldb['meanEvokedFirstStdA'][indRow]) and (celldb['pValHighFRA'][indRow] < 0.05):
        posPredErrorNeuronHigh.append(celldb.iloc[indRow])
    # -- High frequency prediction neuron --
    if (celldb['meanEvokedSecondOddA'][indRow] > celldb['meanEvokedSecondStdA'][indRow]) and (celldb['pValMidFRA'][indRow] < 0.05):
        predictionNeuronHigh.append(celldb.iloc[indRow])

    # -- DESCENDING --
    # -- Middle frequency prediction neuron --
    if (celldb['meanEvokedFirstOddD'][indRow] > celldb['meanEvokedFirstStdD'][indRow]) and (celldb['pValLowFRD'][indRow] < 0.05):
        predictionNeuronMidD.append(celldb.iloc[indRow])
        print('{} {} {:.0f}um T{} c{} is a descend mid freq pred neuron.'.format(dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster']))
    # -- Middle frequency positive prediction error neuron --
    if (celldb['meanEvokedSecondOddD'][indRow] > celldb['meanEvokedSecondStdD'][indRow]) and (celldb['pValMidFRD'][indRow] < 0.05):
        posPredErrorNeuronMidD.append(celldb.iloc[indRow])
    # -- Low frequency positive prediction error neuron --
    if (celldb['meanEvokedFirstOddD'][indRow] > celldb['meanEvokedFirstStdD'][indRow]) and (celldb['pValLowFRD'][indRow] < 0.05):
        posPredErrorNeuronLowD.append(celldb.iloc[indRow])
    # -- Low frequency prediction neuron --
    if (celldb['meanEvokedSecondOddD'][indRow] > celldb['meanEvokedSecondStdD'][indRow]) and (celldb['pValMidFRD'][indRow] < 0.05):
        predictionNeuronLowD.append(celldb.iloc[indRow])



print('There are {} total cells.'.format(len(celldb)))
print('ASCENDING:')
print('There are {} mid frequency prediction neurons.'.format(len(predictionNeuronMid)))
print('There are {} mid frequency positive prediction error neurons.'.format(len(posPredErrorNeuronMid)))
#print('There are {} high frequency prediction neurons.'.format(len(predictionNeuronHigh)))
#print('There are {} high frequency positive prediction error neurons.'.format(len(posPredErrorNeuronHigh)))

print('DESCENDING:')
print('There are {} mid frequency prediction neurons.'.format(len(predictionNeuronMidD)))
print('There are {} mid frequency positive prediction error neurons.'.format(len(posPredErrorNeuronMidD)))
#print('There are {} low frequency prediction neurons.'.format(len(predictionNeuronLowD)))
#print('There are {} low frequency positive prediction error neurons.'.format(len(posPredErrorNeuronLowD)))

totalTime = time.time() - startTime
print ('The script took {:.2f} seconds'.format(totalTime))
