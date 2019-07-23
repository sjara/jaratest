from scipy import optimize
import os
import numpy as np
from numpy import inf
from matplotlib import pyplot as plt
import pandas
from jaratoolbox import settings
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import spikesanalysis
from jaratest.nick.database import dataplotter
from jaratest.nick.database import dataplotter
from scipy import stats
import collections
import statsmodels

#Gaussian function
def gaussian(x, a, x0, sigma, y0):
    return a*np.exp(-(x-x0)**2/(2*sigma**2)) + y0

def inverse_gaussian(y, a, x0, sigma, y0):
    #Inverse function
    #x = sqrt(-ln((y-y0)/a)*2*sigma**2) + x0
    sqrtInner = -1*np.log((y-y0)/a)*2*sigma**2
    if sqrtInner<0: #No solutions
        return None
    else:
        lower = x0 - np.sqrt(sqrtInner)
        upper = x0 + np.sqrt(sqrtInner)
        return [lower, upper]

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def get_colors(ncolors):
    ''' returns n distinct colours for plotting purpouses when you don't want to manually specify colours'''
    from matplotlib.pyplot import cm
    colors = cm.viridis(np.linspace(0,1,ncolors))
    return colors

def convert_openephys(dataObj):
    '''
    Converts to seconds and milivolts
    '''
    if hasattr(dataObj, 'samples'):
        dataObj.samples = dataObj.samples.astype(float)-2**15
        dataObj.samples = (1000.0/dataObj.gain[0,0]) * dataObj.samples
    if hasattr(dataObj, 'timestamps'):
        dataObj.timestamps = dataObj.timestamps/dataObj.samplingRate
    return dataObj

def get_session_inds(cell, sessiontype):
    return [i for i, st in enumerate(cell['sessiontype']) if st==sessiontype]

def get_session_ephys(cell, sessiontype):
    sessionInds = get_session_inds(cell, sessiontype)
    sessionInd = sessionInds[0] #FIXME: Just takes the first one for now
    ephysSession = cell['ephys'][sessionInd]
    ephysBaseDir = os.path.join(settings.EPHYS_PATH, cell['subject'])
    tetrode=int(cell['tetrode'])
    eventFilename=os.path.join(ephysBaseDir,
                               ephysSession,
                               'all_channels.events')
    spikesFilename=os.path.join(ephysBaseDir,
                                ephysSession,
                                'Tetrode{}.spikes'.format(tetrode))
    eventData=loadopenephys.Events(eventFilename)
    spikeData = loadopenephys.DataSpikes(spikesFilename)
    if spikeData.timestamps is not None:
        clustersDir = os.path.join(ephysBaseDir, '{}_kk'.format(ephysSession))
        clustersFile = os.path.join(clustersDir,'Tetrode{}.clu.1'.format(tetrode))
        spikeData.set_clusters(clustersFile)
        spikeData.samples=spikeData.samples[spikeData.clusters==cell['cluster']]
        spikeData.timestamps=spikeData.timestamps[spikeData.clusters==cell['cluster']]
        spikeData = convert_openephys(spikeData)
    eventData = convert_openephys(eventData)
    return spikeData, eventData

def get_session_bdata(cell, sessiontype):
    sessionInds = get_session_inds(cell, sessiontype)
    sessionInd = sessionInds[0] #FIXME: Just takes the first one for now
    behavFile = cell['behavior'][sessionInd]
    behavDataFilePath=os.path.join(settings.BEHAVIOR_PATH, cell['subject'], behavFile)
    bdata = loadbehavior.BehaviorData(behavDataFilePath,readmode='full')
    return bdata

#Load ephys and behavior data
db = pandas.read_hdf('/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5', 'dataframe')
soundResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')



# cell = soundResponsive.iloc[34] #Cell with really low thresh
# cell = soundResponsive.iloc[36] #Inhibited
cell = soundResponsive.iloc[39] #beautiful cell
# cell = soundResponsive.iloc[5] #beautiful cell




spikeData, eventData = get_session_ephys(cell, 'tc')
eventOnsetTimes = eventData.get_event_onset_times()
bdata = get_session_bdata(cell, 'tc')

#Get number of spikes evoked in each condition
baseRange = [-0.1, 0]
responseRange = [0, 0.1]
alignmentRange = [baseRange[0], responseRange[1]]

intensityEachTrial = bdata['currentIntensity']
freqEachTrial = bdata['currentFreq']
possibleFreq = np.unique(freqEachTrial)
possibleIntensity = np.unique(intensityEachTrial)

clusterSpikeTimes = spikeData.timestamps

# plt.close('all')
# plt.figure()
# dataplotter.two_axis_heatmap(spikeData.timestamps,
#                              eventOnsetTimes,
#                              firstSortArray = bdata['currentIntensity'],
#                              secondSortArray = bdata['currentFreq'],
#                              flipFirstAxis=False,
#                              firstSortLabels= np.unique(bdata['currentIntensity']),
#                              secondSortLabels = ['{:.3}'.format(freq/1000.) for freq in np.unique(bdata['currentFreq'])],
#                              timeRange=[0, 0.2])
# plt.show()

plt.close('all')
plt.figure()
dataplotter.plot_raster(spikeData.timestamps, eventOnsetTimes, sortArray=bdata['currentFreq'])
# plt.show()

# plt.clf()
plt.figure()


colors = get_colors(len(possibleIntensity))

aboveBaseline = []
popts = []
allAx = []
allIntenBase = np.array([])
allIntenResp = np.empty((len(possibleIntensity), len(possibleFreq)))
allIntenRespMedian = np.empty((len(possibleIntensity), len(possibleFreq)))
for indinten, inten in enumerate(possibleIntensity):
    ax = plt.subplot(len(possibleIntensity), 1, len(possibleIntensity)-indinten)
    allAx.append(ax)
    spks = np.array([])
    inds = np.array([])
    base = np.array([])
    lam = np.empty(len(possibleFreq))
    lamci = np.empty((len(possibleFreq), 2))
    zVals = np.empty(len(possibleFreq))
    for indfreq, freq in enumerate(possibleFreq):
        selectinds = np.flatnonzero((freqEachTrial==freq)&(intensityEachTrial==inten))
        selectedOnsetTimes = eventOnsetTimes[selectinds]
        (spikeTimesFromEventOnset,
         trialIndexForEachSpike,
         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(clusterSpikeTimes,
                                                                       selectedOnsetTimes,
                                                                       alignmentRange)
        nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            baseRange)
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            responseRange)

        zStat, pVal = stats.ranksums(nspkResp, nspkBase)
        zVals[indfreq] = zStat


        #try to fit Poisson rate parameter for the response
        # res = statsmodels.discrete.discrete_model.Poisson(nspkResp, np.ones_like(nspkResp)).fit()

        base = np.concatenate([base, nspkBase.ravel()])
        spks = np.concatenate([spks, nspkResp.ravel()])
        inds = np.concatenate([inds, np.ones(len(nspkResp.ravel()))*indfreq])
        print spks.mean()
        # lam[indfreq] = res.predict()[0]
        allIntenBase = np.concatenate([allIntenBase, nspkBase.ravel()])
        allIntenResp[indinten, indfreq] = np.mean(nspkResp)
        allIntenRespMedian[indinten, indfreq] = np.median(nspkResp)
        # lamci[ind]

    #Anova to see if freq changes responses
    # scipy.stats.f_oneway()

    #Fit gaussian to the spike data
    popt, pcov = optimize.curve_fit(gaussian, inds, spks, p0=[1, 8, 4, np.mean(allIntenBase)], bounds=(0, [inf, 15, 15, 10]))
    popts.append(popt)
    # plt.plot(inds, spks, 'k.')
    aboveBaseline.append(max(gaussian(inds, *popt)) > base.mean()+base.std())

    plt.plot(jitter(inds, 0.2), spks, 'k.')
    # plt.plot(jitter(inds, 0.2), base, 'k.')
    # seaborn.violinplot(inds, spks)
    plt.hold(1)
    plt.plot(range(len(possibleFreq)), zVals, 'r-')
    # plt.plot(range(len(possibleFreq)), gaussian(range(len(possibleFreq)), *popt), '-', color='k')

maxSpikes = max(spks)
for ax in allAx:
    ax.set_ylim([-0.1, maxSpikes])

    #Print out the fitted curve values to compare to a threshold by eye
    # print gaussian(range(len(possibleFreq)), *popt)

# thresh = allIntenBase.mean() + allIntenResp.max()*0.2
thresh = allIntenBase.mean() + 0.2*(allIntenResp.max()-allIntenBase.mean())
threshMedian = allIntenBase.mean() + 0.2*(allIntenRespMedian.max()-allIntenBase.mean())
fra = allIntenResp > thresh
fraMedian = allIntenRespMedian > threshMedian

plt.clf()
plt.subplot(211)
plt.imshow(np.flipud(allIntenResp), interpolation='none')
plt.subplot(212)
plt.imshow(np.flipud(fra), interpolation='none')

plt.figure()
indThresh = 0
numSpikes = allIntenResp[indThresh, :]
poptThreshold = popts[indThresh]
plt.plot(range(len(possibleFreq)), gaussian(range(len(possibleFreq)), *poptThreshold), '-', color='k')
plt.hold(True)
plt.plot(range(len(possibleFreq)), numSpikes, 'b-o')
plt.axhline(y=thresh, color='r')

lower, upper = inverse_gaussian(thresh, *poptThreshold)
plt.axvline(x=lower, color='r')
plt.axvline(x=upper, color='r')

plt.show()


# loc, scale = stats.expon.fit(allIntenBase, floc=0)
# # loc, scale = stats.expon.fit(allIntenBase)
# # rv = stats.expon()
# plt.figure()
# plt.clf()
# x = np.linspace(0, 10, 100)
# y = stats.expon.pdf(x, loc=loc, scale=scale)
# # # h = hist(allIntenBase, bins=np.arange(10)-0.5, align='mid')

# cnt = collections.Counter(allIntenBase)
# cntVals = [val for key, val in cnt.iteritems()]
# cntKeys = [key for key, val in cnt.iteritems()]
# plt.plot(cntKeys, np.array(cntVals)/float(len(allIntenBase)), 'b-o', label='Data')

# # h = plt.hist(allIntenBase, bins=np.arange(0,10), normed=True)
# # plt.hold(1)
# # # plot(x, y*len(allIntenBase), 'r-')
# plt.plot(x, y, 'r-', label='Fitted exponential curve')
# thresh = stats.expon.ppf(0.95, loc=loc, scale=scale)
# plt.axvline(x=thresh, color='r', ls='--', label='95th percentile for fit')
# plt.xlabel('Number of spikes in baseline range')
# plt.ylabel('Proportion of trials')
# plt.legend()
# plt.savefig('/tmp/expfit.png')



# res = statsmodels.Poisson(allIntenBase, np.ones_like(allIntenBase)).fit()

# fit_alpha, fit_loc, fit_beta = scipy.stats.gamma.fit(allIntenBase)

# allIntenBase = scipy.stats.expon.rvs(loc=0, scale=1.5, size=10000)






# plt.axhline(base.mean(), ls='-', color='k')
# plt.axhline(base.mean()+base.std(), ls='--', color='k')

# aboveBaseline = np.array(above_baseline)
# indintenFirstAbove = np.where(aboveBaseline==True)[0][0]
# indinten10aboveThresh = indintenFirstAbove+2
# poptFirstAbove = popts[indintenFirstAbove]
# popt10Above = popts[indinten10aboveThresh]
# estsFirstAbove = gaussian(np.unique(inds), *poptFirstAbove)
# ests10Above = gaussian(np.unique(inds), *popt10Above)

# estsAboveBaseline10 = ests10Above>base.mean()+base.std()
# freqsAboveBaseline10 = possibleFreq[estsAboveBaseline10]

# lower = freqsAboveBaseline10[0]
# upper = freqsAboveBaseline10[-1]

# cf = possibleFreq[np.argmax(estsFirstAbove)]
# threshold = possibleIntensity[indintenFirstAbove]


plt.show()

