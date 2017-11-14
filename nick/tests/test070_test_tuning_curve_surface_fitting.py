import pandas
from jaratest.nick.database import dataloader_v2 as dataloader
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
from jaratoolbox import spikesanalysis
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import scipy

db = pandas.read_hdf('/home/nick/data/database/pinp017/pinp017_database.h5', 'database')

soundResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')

cell = soundResponsive.iloc[0]


sessiontypeIndex = cell['sessiontype'].index('tc')

#Initialize a data loader for this animal
loader = dataloader.DataLoader(cell['subject'])

#Get the behavior data
behavData = loader.get_session_behavior(cell['behavior'][sessiontypeIndex])
intensityEachTrial = behavData['currentIntensity']
freqEachTrial = behavData['currentFreq']

possibleFreq = np.unique(freqEachTrial)
possibleIntensity = np.unique(intensityEachTrial)

#Return the cluster spike data for this ephys session
ephysDir = cell['ephys'][sessiontypeIndex]
clusterSpikeData = loader.get_session_spikes(ephysDir, int(cell['tetrode']), cluster=int(cell['cluster']))
clusterSpikeTimes = clusterSpikeData.timestamps

#Get the events for this session and calculate onset times
eventData = loader.get_session_events(ephysDir)
eventOnsetTimes = loader.get_event_onset_times(eventData, minEventOnsetDiff=None)

baseRange = [-0.1, 0]
responseRange = [0, 0.1]
alignmentRange = [baseRange[0], responseRange[1]]


response = np.empty((len(possibleIntensity), len(possibleFreq)))
base = np.empty((len(possibleIntensity), len(possibleFreq)))

for indfreq, freq in enumerate(possibleFreq):
    for indinten, inten in enumerate(possibleIntensity):
        selectinds = np.flatnonzero((freqEachTrial==freq)&(intensityEachTrial==inten))
        selectedOnsetTimes = eventOnsetTimes[selectinds]

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(clusterSpikeTimes,selectedOnsetTimes,alignmentRange)

        nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            baseRange)
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            responseRange)

        response[indinten, indfreq] = nspkResp.mean()
        base[indinten, indfreq] = nspkBase.mean()

fig = plt.figure()
ax = fig.gca(projection='3d')

X, Y = np.meshgrid(np.arange(len(possibleFreq)), np.arange(len(possibleIntensity)))
Z = response

# ax.plot_surface(X, Y, response, rstride=1, cstride=1, facecolors=rgb)

# cset = ax.contour(X, Y, Z, extend3d=True, cmap=cm.coolwarm)
# cset = ax.scatter(X, Y, Z)
# ax.clabel(cset, fontsize=9, inline=1)
# plt.show()

xi = np.linspace(0,len(possibleFreq),100)
yi = np.linspace(0,len(possibleIntensity),100)

zi = scipy.interpolate.griddata((X.ravel(), Y.ravel()), Z.ravel(), (xi[None,:], yi[:,None]), method='cubic')
# CS = plt.contour(xi,yi,zi,15,linewidths=0.5,color='k')
# CS = plt.contour(xi,yi,zi,15,linewidths=0.5,color='k')

xig, yig = np.meshgrid(xi, yi)

# surf = ax.plot_surface(xig, yig, zi,
#                        linewidth=1, cmap=cm.jet)

ax.plot_surface(xig, yig, zi, rstride=8, cstride=8, alpha=0.3)
cset = ax.contourf(xig, yig, zi, zdir='z', offset=0, cmap=cm.coolwarm)
cset = ax.contourf(xig, yig, zi, zdir='x', offset=0, cmap=cm.coolwarm)
cset = ax.contourf(xig, yig, zi, zdir='y', offset=0, cmap=cm.coolwarm)
