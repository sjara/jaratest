import sys
import importlib

def calculate_cell_depth(cell, tetrodeLengthList):
    '''
    cell: a row from the celldb pandas DataFrame.
    '''
    tetrode = int(cell.tetrode)
    depthThisCell = cell.depth - tetrodeLengthList[tetrode-1]
    return depthThisCell

def testInTargetRange(depthThisCell, targetRangeLongestTt):
    inTargetRange = (depthThisCell >= targetRangeLongestTt[0]) & (depthThisCell <= targetRangeLongestTt[1])
    return inTargetRange

def celldb_in_target_range_check(celldb, inforecPath):
    # -- Added striatumRange and tetrodeLengthList to inforec files after histology verification of striatum/cortex range -- #
    animal = celldb.subject.loc[0]
    sys.path.append(inforecPath)   #settings.INFOREC_PATH
    inforec = importlib.import_module('{}_inforec'.format(animal))
    tetrodeLengthList = inforec.tetrodeLengthList
    targetRangeLongestTt = inforec.targetRangeLongestTt

    actualDepthEachCell = celldb.apply(lambda row: calculate_cell_depth(row, tetrodeLengthList), axis=1)
    inTargetArea = testInTargetRange(actualDepthEachCell, targetRangeLongestTt)
        
    return actualDepthEachCell, inTargetArea
