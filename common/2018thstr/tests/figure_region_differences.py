import os
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)
from jaratoolbox import colorpalette
from scipy import stats
import copy
import pandas as pd
import figparams
reload(figparams)

from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache
mcc = MouseConnectivityCache(resolution=25)
rsp = mcc.get_reference_space()
rspAnnotationVolumeRotated = np.rot90(rsp.annotation, 1, axes=(2, 0))

np.random.seed(0)

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(ax, yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    ax.plot([start, end], [yval, yval], color=color, lw=linewidth)

FIGNAME = 'figure_tagged_untagged'
SAVE_FIGURE = 0
# outputDir = '/mnt/jarahubdata/reports/nick/20171218_all_2018thstr_figures'
outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'plots_tagged_vs_untagged_am' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12,8] # In inches


colorTagged = colorpalette.TangoPalette['SkyBlue2']
colorUntagged = colorpalette.TangoPalette['Aluminium3']

labelPosX = [0.04, 0.48]   # Horiz position for panel labels
labelPosY = [0.48, 0.95]    # Vert position for panel labels

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
dbase = pd.read_hdf(dbPath, key='dataframe')

fig = plt.gcf()
plt.clf()
fig.set_facecolor('w')

for region in ['rightThal', 'rightAC']:
    dataframe = dbase.query("brainArea == @region and nSpikes>2000")

    ### GET ONLY CELLS THAT COME FROM SITES WHERE AT LEAST ONE SOUND/LASER CELL WAS RECORDED
    dataframe = dataframe[~pd.isnull(dataframe['cellX'])]

    # CALCULATE BRAIN LOCATION FOR EACH CELL
    dataframe['location'] = ''
    for indRow, dbRow in dataframe.iterrows():
        try:
            thisCoordID = rspAnnotationVolumeRotated[int(dbRow['cellX']), int(dbRow['cellY']), int(dbRow['cellZ'])]
        except ValueError:
            dataframe.at[indRow, 'location'] = 'NaN'
        else:
            structDict = rsp.structure_tree.get_structures_by_id([thisCoordID])[0]
            dataframe.at[indRow, 'location'] = structDict['name']

    goodISI = dataframe.query('isiViolations<0.02 or modifiedISI<0.02')
    # goodISI = dataframe.query('isiViolations<0.02')
    goodShape = goodISI.query('spikeShapeQuality > 2')
    goodFit = goodShape.query('rsquaredFit > 0.04')

    #Calculate the midpoint of the gaussian fit
    goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
    goodFitToUse = goodFit.query('fitMidPoint<32000')

    # taggedCellsFreq = goodFitToUse[goodFitToUse['autoTagged']==1]
    # untaggedCellsFreq = goodFitToUse[goodFitToUse['autoTagged']==0]
    dbFreq = goodFitToUse
    dbAM = goodShape

    # taggedCellsAM = goodShape[goodShape['autoTagged']==1]
    # untaggedCellsAM = goodShape[goodShape['autoTagged']==0]


    freqFeatures = ['BW10', 'latency', 'threshold']
    amFeatures = ['highestSyncCorrected', 'mutualInfoBCBits']

    for feature in freqFeatures:
        dbFreq.boxplot(column=feature, by='location', rot=90)
        plt.gcf().set_size_inches((8.5,11))
        plt.subplots_adjust(bottom=0.4)
        plt.ylabel(feature)
        plt.savefig('{}_{}.png'.format(region, feature))

    for feature in amFeatures:
        dbAM.boxplot(column=feature, by='location', rot=90)
        plt.gcf().set_size_inches((8.5,11))
        plt.subplots_adjust(bottom=0.4)
        plt.ylabel(feature)
        plt.savefig('{}_{}.png'.format(region, feature))
