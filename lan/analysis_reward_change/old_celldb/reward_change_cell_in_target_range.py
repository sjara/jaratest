import os
import sys
import importlib
import pandas as pd
import numpy as np
from jaratoolbox import settings
from jaratoolbox import loadbehavior

animalList = ['adap067']

for animal in animalList:
    #celldbPath = os.path.join(settings.DATABASE_PATH,'reward_change_{}.h5'.format(label))
    celldbPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(animal))
    celldb = pd.read_hdf(celldbPath, key='reward_change')
        
    if not ('inTargetArea' in celldb.columns): 
        print 'Calculating actual depth and test whether in range of target'

        # -- Added striatumRange and tetrodeLengthList to inforec files after histology verification of striatum/cortex range -- #
        sys.path.append(settings.INFOREC_PATH)  
        inforec = importlib.import_module('{}_inforec'.format(animal))
        tetrodeLengthList = inforec.tetrodeLengthList
        targetRangeLongestTt = inforec.targetRangeLongestTt

        def calculate_cell_depth(cell):
            tetrode = int(cell.tetrode)
            depthThisCell = cell.depth - tetrodeLengthList[tetrode-1]
            return depthThisCell

        def testInTargetRange(cell):
            depthThisCell = cell.actualDepth
            inTargetRange = (depthThisCell >= targetRangeLongestTt[0]) & (depthThisCell <= targetRangeLongestTt[1])
            return inTargetRange
        
        actualDepth = celldb.apply(lambda row: calculate_cell_depth(row), axis=1)
        celldb['actualDepth'] = actualDepth
        inTargetArea = celldb.apply(lambda row: testInTargetRange(row), axis=1)
        celldb['inTargetArea'] = inTargetArea

    celldb.to_hdf(celldbPath, key='reward_change')        
