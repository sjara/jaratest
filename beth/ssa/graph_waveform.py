import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
import studyparams

dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,'celldb_{}.h5'.format(studyparams.STUDY_NAME))

figFormat = 'png'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME,'reports')

# -- Load the database of cells --
celldb = celldatabase.load_hdf(dbFilename)

for indRow,dbRow in celldb[266:267].iterrows():
    oneCell = ephyscore.Cell(dbRow)

    #ephysData, bdata = oneCell.load('noiseburst')
    #ephysData, bdata = oneCell.load('tc')
    #ephysData, bdata = oneCell.load('standard')
    ephysData, bdata = oneCell.load('oddball')

    spikesorting.plot_waveforms(ephysData['samples'])

    '''
    Saving the figure --------------------------------------------------------------
    '''
    figFilename ='{}_{}_{}um_T{}_c{}_oddwave.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    figFullpath = os.path.join(outputDir,figFilename)
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([6,4])

    plt.tight_layout()
    plt.show()
