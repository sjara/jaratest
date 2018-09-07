import os
from jaratoolbox import settings
from matplotlib import pyplot as plt
from jaratoolbox import spikesanalysis
import numpy as np

STUDY_NAME = '2018thstr'
FIGNAME = 'figure_am'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

exampleDataPath = os.path.join(dataDir, 'data_am_examples.npz')
exampleData = np.load(exampleDataPath)

exampleFreqEachTrial = exampleData['exampleFreqEachTrial'].item()
exampleSpikeTimes = exampleData['exampleSpikeTimes'].item()
exampleTrialIndexForEachSpike = exampleData['exampleTrialIndexForEachSpike'].item()
exampleIndexLimitsEachTrial = exampleData['exampleIndexLimitsEachTrial'].item()

exampleName = 'AC1'

spikeTimes = exampleSpikeTimes[exampleName]
indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
freqEachTrial = exampleFreqEachTrial[exampleName]
# trialsEachCondition = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)

countRange = [0.1, 0.5]
spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimes,indexLimitsEachTrial,countRange)
numSpikesInTimeRangeEachTrial = np.squeeze(spikeCountMat)

if len(numSpikesInTimeRangeEachTrial) == len(freqEachTrial)+1:
    numSpikesInTimeRangeEachTrial = numSpikesInTimeRangeEachTrial[:-1]


from statsmodels.nonparametric import smoothers_lowess
out = smoothers_lowess.lowess(numSpikesInTimeRangeEachTrial, np.log2(freqEachTrial))

sortedX = np.unique(out[:,0])
predictedY = np.unique(out[:,1])


plt.clf()
plt.plot(np.log2(freqEachTrial), numSpikesInTimeRangeEachTrial, 'k.')
plt.plot(sortedX, predictedY, 'r-o')
plt.show()
