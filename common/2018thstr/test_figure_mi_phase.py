import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
from collections import Counter
from scipy import stats
import pandas as pd
# import figparams
# reload(figparams)
from sklearn import metrics

def medline(yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    plt.plot([start, end], [yval, yval], color=color, lw=linewidth)

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase_phaseMI.h5'
dataframe = pd.read_hdf(dbPath, key='dataframe')

dataframe = dataframe.query("pulsePval<0.05 and trainRatio>0.8")

ac = dataframe.groupby('brainArea').get_group('rightAC')
thal = dataframe.groupby('brainArea').get_group('rightThal')

possibleFreqKeys = [4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128]

keys = ['mutualInfoPhase_{}Hz'.format(rate) for rate in possibleFreqKeys]

acData = np.full((len(ac), len(possibleFreqKeys)), np.nan)
thalData = np.full((len(thal), len(possibleFreqKeys)), np.nan)

for externalInd, (indRow, row) in enumerate(ac.iterrows()):
    for indKey, key in enumerate(keys):
        acData[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(thal.iterrows()):
    for indKey, key in enumerate(keys):
        thalData[externalInd, indKey] = row[key]

acData[acData<0]=0
thalData[thalData<0]=0

for indCol, freqKey in enumerate(possibleFreqKeys):
    acDataThisFreq = acData[:,indCol][np.logical_not(np.isnan(acData[:,indCol]))]
    thalDataThisFreq = thalData[:,indCol][np.logical_not(np.isnan(thalData[:,indCol]))]
    zStat, pVal = stats.ranksums(acDataThisFreq, thalDataThisFreq)
    print "{}Hz, p={}".format(freqKey, pVal)


acMean = np.nanmean(acData, axis=0)
# acMean = np.nanmedian(acData, axis=0)
acStd = np.nanstd(acData, axis=0)

thalMean = np.nanmean(thalData, axis=0)
# thalMean = np.nanmedian(thalData, axis=0)
thalStd = np.nanstd(thalData, axis = 0)

numAC = sum(np.logical_not(np.isnan(acData[:,0])))
numThal = sum(np.logical_not(np.isnan(thalData[:,0])))

# plt.clf()
# plt.plot(acMean, 'r-', label='AC')
# # plt.fill_between(range(len(possibleFreqKeys)), acMean+acStd/numAC, acMean-acStd/numAC, color='r', alpha=0.5)
# plt.hold(1)
# plt.plot(thalMean, 'b-', label="ATh")
# # plt.fill_between(range(len(possibleFreqKeys)), thalMean+thalStd/numThal, thalMean-thalStd/numThal, color='b', alpha=0.5)
# ax = plt.gca()
# ax.set_xticks(range(len(possibleFreqKeys)))
# ax.set_xticklabels(possibleFreqKeys)
# # ax.set_ylim([0, 0.06])
# ax.set_ylabel('MI between neuronal firing rate and stimulus phase')
# plt.legend()
# plt.show()

plt.clf()
for indRate in range(len(possibleFreqKeys)):
    indThal = indRate-0.1
    indAC = indRate+0.1
    plt.plot(np.ones(len(thalData[:,indRate]))*indThal, thalData[:,indRate], 'o', mec='b', mfc='None')
    # medline(np.nanmedian(thalData[:,indRate]), indThal, 0.1)
    medline(np.nanmean(thalData[:,indRate]), indThal, 0.1)
    plt.hold(1)
    plt.plot(np.ones(len(acData[:,indRate]))*indAC, acData[:,indRate], 'o', mec='r', mfc='None')
    # medline(np.nanmedian(acData[:,indRate]), indAC, 0.1)
    medline(np.nanmean(acData[:,indRate]), indAC, 0.1)
plt.show()
