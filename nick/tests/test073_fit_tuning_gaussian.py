from scipy import optimize
import pandas
from jaratoolbox import settings
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import spikesanalysis
from jaratest.nick.database import dataplotter
from jaratest.nick.database import dataplotter
from scipy import stats

#Gaussian function
def gaussian(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

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
db = pandas.read_hdf('/home/nick/data/database/corticostriatal_master_20170452.h5', 'database')
soundResponsive = masterdb.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')



# cell = soundResponsive.iloc[34] #Cell with really low thresh
# cell = soundResponsive.iloc[36] #Inhibited
# cell = soundResponsive.iloc[39] #beautiful cell
cell = soundResponsive.iloc[5] #beautiful cell




spikeData, eventData = get_session_ephys(cell, 'tc')
eventOnsetTimes = eventData.get_event_onset_times()
bdata = get_session_bdata(cell, 'tc')

#Get number of spikes evoked in each condition
baseRange = [-0.2, 0]
responseRange = [0, 0.2]
alignmentRange = [baseRange[0], responseRange[1]]

intensityEachTrial = bdata['currentIntensity']
freqEachTrial = bdata['currentFreq']
possibleFreq = np.unique(freqEachTrial)
possibleIntensity = np.unique(intensityEachTrial)

clusterSpikeTimes = spikeData.timestamps

plt.close('all')
plt.figure()
dataplotter.two_axis_heatmap(spikeData.timestamps,
                             eventOnsetTimes,
                             firstSortArray = bdata['currentIntensity'],
                             secondSortArray = bdata['currentFreq'],
                             flipFirstAxis=False,
                             firstSortLabels= np.unique(bdata['currentIntensity']),
                             secondSortLabels = ['{:.3}'.format(freq/1000.) for freq in np.unique(bdata['currentFreq'])],
                             timeRange=[0, 0.2])
plt.show()

plt.figure()
dataplotter.plot_raster(spikeData.timestamps, eventOnsetTimes, sortArray=bdata['currentFreq'])
plt.show()

plt.figure()

colors = get_colors(len(possibleIntensity))

aboveBaseline = []
popts = []

for indinten, inten in enumerate(possibleIntensity):
    spks = np.array([])
    inds = np.array([])
    base = np.array([])
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

        base = np.concatenate([base, nspkBase.ravel()])
        spks = np.concatenate([spks, nspkResp.ravel()])
        inds = np.concatenate([inds, np.ones(len(nspkResp.ravel()))*indfreq])

    #Anova to see if freq changes responses
    # scipy.stats.f_oneway()

    #Fit gaussian to the spike data
    popt, pcov = optimize.curve_fit(gaussian, inds, spks, p0=[1, 8, 4], bounds=(0, [inf, 15, 15]))
    popts.append(popt)
    # plt.plot(inds, spks, 'k.')
    aboveBaseline.append(max(gaussian(inds, *popt)) > base.mean()+base.std())

    plt.hold(1)
    plt.plot(inds,gaussian(inds, *popt), '-', color=colors[indinten])

plt.axhline(base.mean(), ls='-', color='k')
plt.axhline(base.mean()+base.std(), ls='--', color='k')

aboveBaseline = np.array(above_baseline)
indintenFirstAbove = np.where(aboveBaseline==True)[0][0]
indinten10aboveThresh = indintenFirstAbove+2
poptFirstAbove = popts[indintenFirstAbove]
popt10Above = popts[indinten10aboveThresh]
estsFirstAbove = gaussian(np.unique(inds), *poptFirstAbove)
ests10Above = gaussian(np.unique(inds), *popt10Above)

estsAboveBaseline10 = ests10Above>base.mean()+base.std()
freqsAboveBaseline10 = possibleFreq[estsAboveBaseline10]

lower = freqsAboveBaseline10[0]
upper = freqsAboveBaseline10[-1]

cf = possibleFreq[np.argmax(estsFirstAbove)]
threshold = possibleIntensity[indintenFirstAbove]








plt.show()

