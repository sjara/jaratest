from jaratoolbox import spikesanalysis
import sys
import pandas
from jaratest.nick.database import dataloader_v2 as dataloader
import numpy as np
from matplotlib import pyplot as plt
from jaratest.nick.database import dataplotter
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratest.nick.stats import circstats
from scipy import stats
import matplotlib
matplotlib.rcParams['svg.fonttype'] = 'none'

def session_type_indices(cell):
    sessiontypes = ['NoiseBurst', 'LaserPulse', 'LaserTrain', 'AM', 'TuningCurve']

    for sessiontype in sessiontypes:
        try:
            sessiontypeIndex = cell['sessiontype'].index(sessiontype)
        except ValueError: #The cell does not have this session type
            sessiontypeIndex = None

        cell['{}_index'.format(sessiontype)] = sessiontypeIndex


def event_response_score(cell, sessiontype, maxZonly=False,
                         responseTimeRange = [-0.5, 1], skip=False):
    '''
    Used to calculate simple response to noise bursts and laser pulses
    '''

    #Find the index of the ephys for this session if it exists
    try:
        sessiontypeIndex = cell['sessiontype'].index(sessiontype)
    except ValueError: #The cell does not have this session type
        return None

    #Initialize a data loader for this animal
    loader = dataloader.DataLoader(cell['subject'])

    #Return the cluster spike data for this ephys session
    ephysDir = cell['ephys'][sessiontypeIndex]
    clusterSpikeData = loader.get_session_spikes(ephysDir, int(cell['tetrode']), cluster=int(cell['cluster']))
    clusterSpikeTimes = clusterSpikeData.timestamps

    #Get the events for this session and calculate onset times
    eventData = loader.get_session_events(ephysDir)
    eventOnsetTimes = loader.get_event_onset_times(eventData, minEventOnsetDiff=None)

    if skip:
        onsetTimesToUse = np.arange(skip, len(eventOnsetTimes), skip)
        eventOnsetTimes = eventOnsetTimes[onsetTimesToUse]

    #Zscore settings from billy
    baseRange = [-0.050,-0.025]              # Baseline range (in seconds)
    binTime = baseRange[1]-baseRange[0]         # Time-bin size
    responseTimeRange = responseTimeRange       #Time range to calculate z value for (should be divisible by binTime
    responseTime = responseTimeRange[1]-responseTimeRange[0]
    numBins = responseTime/binTime
    binEdges = np.arange(responseTimeRange[0], responseTimeRange[1], binTime)
    timeRange = [-0.5, 1]

    #TODO: Get the spikes and events

    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(clusterSpikeTimes,eventOnsetTimes,timeRange)

    [zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange,binEdges) #computes z score for each bin. zStat is array of z scores. maxZ is maximum value of z in timeRange

    if maxZonly:
        return maxZ
    else:
      return zStat, pValue, maxZ


def plot_cell_phys(cell, rastertypes, tctype):

    loader = dataloader.DataLoader(cell['subject'])

    fig = plt.clf()


    #Plot raster sessions
    for indRaster, rastertype in enumerate(rastertypes):
        plt.subplot2grid((6, 6), (indRaster, 0), rowspan = 1, colspan = 3)

        try:
            sessiontypeIndex = cell['sessiontype'].index(rastertype)
        except ValueError: #The cell does not have this session type
            continue

        sessionEphys = cell['ephys'][sessiontypeIndex]

        rasterSpikes = loader.get_session_spikes(sessionEphys, int(cell['tetrode']), cluster=int(cell['cluster']))
        spikeTimestamps = rasterSpikes.timestamps

        rasterEvents = loader.get_session_events(sessionEphys)
        eventOnsetTimes = loader.get_event_onset_times(rasterEvents)

        dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, ms=1)

        plt.ylabel('{}\n{}'.format(rastertype, sessionEphys.split('_')[1]), fontsize = 10)
        ax=plt.gca()
        extraplots.set_ticks_fontsize(ax,6)


    #Plot tuning curve
    try:
        sessiontypeIndex = cell['sessiontype'].index(tctype)

        plt.subplot2grid((6, 6), (0, 3), rowspan = 3, colspan = 3)

        bdata = loader.get_session_behavior(cell['behavior'][sessiontypeIndex])
        eventData = loader.get_session_events(cell['ephys'][sessiontypeIndex])
        spikeData = loader.get_session_spikes(cell['ephys'][sessiontypeIndex],
                                            int(cell['tetrode']),
                                            cluster = int(cell['cluster']))

        spikeTimestamps = spikeData.timestamps

        eventOnsetTimes = loader.get_event_onset_times(eventData)

        freqEachTrial = bdata['currentFreq']
        intensityEachTrial = bdata['currentIntensity']

        possibleFreq = np.unique(freqEachTrial)
        possibleIntensity = np.unique(intensityEachTrial)

        xlabel='Frequency (kHz)'
        ylabel='Intensity (dB SPL)'

        freqLabels = ["%.1f" % freq for freq in possibleFreq/1000.0]
        intenLabels = ["%.1f" % inten for inten in possibleIntensity]

        dataplotter.two_axis_heatmap(spikeTimestamps=spikeTimestamps,
                                     eventOnsetTimes=eventOnsetTimes,
                                     firstSortArray=intensityEachTrial,
                                     secondSortArray=freqEachTrial,
                                     firstSortLabels=intenLabels,
                                     secondSortLabels=freqLabels,
                                     xlabel=xlabel,
                                     ylabel=ylabel,
                                     plotTitle='',
                                     flipFirstAxis=True,
                                     flipSecondAxis=False,
                                     timeRange=[0, 0.1],
                                     cmap='magma')

        # plt.title("{0}\n{1}".format(mainTCsession, mainTCbehavFilename), fontsize = 10)

    except ValueError: #The cell does not have this session type
        print 'no tc'

    plt.show()

def plot_cell_tc(cell, tctype):
    loader = dataloader.DataLoader(cell['subject'])
    # try:
    sessiontypeIndex = cell['sessiontype'].index(tctype)

    plt.cla()

    bdata = loader.get_session_behavior(cell['behavior'][sessiontypeIndex])
    eventData = loader.get_session_events(cell['ephys'][sessiontypeIndex])
    spikeData = loader.get_session_spikes(cell['ephys'][sessiontypeIndex],
                                        int(cell['tetrode']),
                                        cluster = int(cell['cluster']))

    spikeTimestamps = spikeData.timestamps

    eventOnsetTimes = loader.get_event_onset_times(eventData)

    freqEachTrial = bdata['currentFreq']
    intensityEachTrial = bdata['currentIntensity']

    possibleFreq = np.unique(freqEachTrial)
    possibleIntensity = np.unique(intensityEachTrial)

    xlabel='Frequency (kHz)'
    ylabel='Intensity (dB SPL)'

    freqLabels = ["%.1f" % freq for freq in possibleFreq/1000.0]
    intenLabels = ["%d" % inten for inten in possibleIntensity]

    ax, cax, cbar, spikeArray = dataplotter.two_axis_heatmap(spikeTimestamps=spikeTimestamps,
                                                                eventOnsetTimes=eventOnsetTimes,
                                                                firstSortArray=intensityEachTrial,
                                                                secondSortArray=freqEachTrial,
                                                                firstSortLabels=intenLabels,
                                                                secondSortLabels=freqLabels,
                                                                xlabel=xlabel,
                                                                ylabel=ylabel,
                                                                plotTitle='',
                                                                flipFirstAxis=False,
                                                                flipSecondAxis=False,
                                                                timeRange=[0, 0.1],
                                                                cmap='YlOrRd')

    fontsize=20

    ax.set_xticks(np.linspace(0, 15, 3))
    ax.set_xticklabels(np.round(np.logspace(np.log10(2), np.log10(40), 3), decimals=1))
    ax.set_xlabel('Frequency (kHz)', fontsize=fontsize)
    ax.set_ylabel('Intensity (dB SPL)', fontsize=fontsize)
    cbar.ax.yaxis.labelpad=-10

    maxFr = np.max(spikeArray.ravel())
    print maxFr
    cbar.set_clim(0, maxFr)
    cbar.set_ticks([0, maxFr])
    cbar.set_ticklabels([0, np.int(maxFr*10)])
    cbar.set_label('Firing rate (Hz)', fontsize=fontsize)
    plt.show()

    extraplots.set_ticks_fontsize(ax, fontsize)
    extraplots.set_ticks_fontsize(cbar.ax, fontsize)

    # plt.title("{0}\n{1}".format(mainTCsession, mainTCbehavFilename), fontsize = 10)

    # except ValueError: #The cell does not have this session type
    #     print 'no tc'


def plot_cell_am(cell, amtype):

    fontsize=20

    loader = dataloader.DataLoader(cell['subject'])
    try:
        sessiontypeIndex = cell['sessiontype'].index(amtype)

        plt.cla()

        bdata = loader.get_session_behavior(cell['behavior'][sessiontypeIndex])
        eventData = loader.get_session_events(cell['ephys'][sessiontypeIndex])
        spikeData = loader.get_session_spikes(cell['ephys'][sessiontypeIndex],
                                            int(cell['tetrode']),
                                            cluster = int(cell['cluster']))

        spikeTimestamps = spikeData.timestamps
        eventOnsetTimes = loader.get_event_onset_times(eventData)

        currentFreq = bdata['currentFreq']
        dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray=currentFreq, fillWidth=0,timeRange=[-0.2, 0.8], ms=2.5)

        ax = plt.gca()
        # extraplots.set_ticks_fontsize(ax, fontsize)
        # ax.set_yticks(np.linspace(0, 10, 3))
        # ax.set_yticklabels(np.round(np.logspace(np.log10(4), np.log10(128), 3), decimals=1))

        fig = plt.gcf()
        # fig.set_size_inches(4.3, 3.9)
        plt.ylabel('AM Rate (Hz)', fontsize=fontsize)
        plt.xlabel('Time from sound onset (s)', fontsize=fontsize)

        # ax.set_xticks([0, 0.5])


    except ValueError: #The cell does not have this session type
        print 'no am'


def tuning_curve_response(cell):
    '''
    Calculate max Z-score during the response period for each freq-inten combo in a TC
    '''

    try:
        sessiontypeIndex = cell['sessiontype'].index('TuningCurve')
    except ValueError: #The cell does not have this session type
        return None

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

    timeRange = [0, 0.1]

    baseRange = [-0.050,-0.025]              # Baseline range (in seconds)
    binTime = baseRange[1]-baseRange[0]         # Time-bin size
    responseTimeRange = timeRange       #Time range to calculate z value for (should be divisible by binTime
    responseTime = responseTimeRange[1]-responseTimeRange[0]
    numBins = responseTime/binTime
    binEdges = np.arange(responseTimeRange[0], responseTimeRange[1], binTime)


    zvalArray = np.zeros((len(possibleIntensity), len(possibleFreq)))

    for indfreq, freq in enumerate(possibleFreq):
        for indinten, inten in enumerate(possibleIntensity):
            selectinds = np.flatnonzero((freqEachTrial==freq)&(intensityEachTrial==inten))
            selectedOnsetTimes = eventOnsetTimes[selectinds]


            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(clusterSpikeTimes,selectedOnsetTimes,timeRange)

            [zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange,binEdges) #computes z score for each bin. zStat is array of z scores. maxZ is maximum value of z in timeRange

            zvalArray[indinten, indfreq] = maxZ
            # zvalArray = np.flipud(zvalArray)

    return zvalArray


def am_dependence(cell):
    '''
    Calculate the average firing rate of a cell during the 0.5sec AM sound.
    Perform a linear regression on average firing rate and AM rate, and
    return the correlation coefficient for the regression.
    '''

    try:
        sessiontypeIndex = cell['sessiontype'].index('AM')
    except ValueError: #The cell does not have this session type
        return None

    #Initialize a data loader for this animal
    loader = dataloader.DataLoader(cell['subject'])

    #Get the behavior data
    behavData = loader.get_session_behavior(cell['behavior'][sessiontypeIndex])
    freqEachTrial = behavData['currentFreq']

    possibleFreq = np.unique(freqEachTrial)

    ephysDir = cell['ephys'][sessiontypeIndex]
    clusterSpikeData = loader.get_session_spikes(ephysDir, int(cell['tetrode']), cluster=int(cell['cluster']))
    clusterSpikeTimes = clusterSpikeData.timestamps

    #Get the events for this session and calculate onset times
    eventData = loader.get_session_events(ephysDir)
    eventOnsetTimes = loader.get_event_onset_times(eventData, minEventOnsetDiff=None)

    timeRange = [0, 0.5]

    trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possibleFreq)

    spikeArray = dataplotter.avg_spikes_in_event_locked_timerange_each_cond(clusterSpikeTimes,
                                                                            trialsEachCond,
                                                                            eventOnsetTimes,
                                                                            timeRange)

    slope, intercept, r_value, p_value, std_err = stats.linregress(spikeArray, possibleFreq)

    return r_value


class TuningAnalysis(object):
    '''
    Plot a tuning curve array. The user can then click on the CF, the lower flank, and the
    upper flank. Calculate Q10 from these selections
    '''

    def __init__(self, arr, freqLabs=None, intenLabs=None, dbAbove=10, thresh=None):

        self.tcArray = arr
        self.freqLabs = freqLabs
        self.intenLabs = intenLabs
        self.dbAbove = dbAbove
        self.setNone = False

        self.bestFreq=None
        self.bw=None

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.hold(True)
        self.thresh = thresh
        self.step=0.5
        self.draw_tc()

        self.mpid=self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.kpid = self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        self.state = 0
        self.statefuncs = [self.get_cf, self.get_low, self.get_high, self.die, self.dead]
        self.transitions = [1, 2, 3, 4]

    def draw_tc(self):
        # self.ax.cla()
        if self.thresh:
            arr = self.tcArray>self.thresh
        else:
            arr = self.tcArray
        cax = self.ax.imshow(arr, interpolation='none', cmap='gray', zorder=0, vmin=0, vmax=3)
        plt.colorbar()
        self.ax.set_title('Threshold: {}'.format(self.thresh))
        self.fig.show()

    def on_click(self, event):
        '''
        Method to record mouse clicks in the mouseClickData attribute
        and plot the points on the current axes
        '''
        # x = np.int(event.xdata-0.5)
        # y = np.int(event.ydata-0.5)

        img = self.ax.get_images()[0]
        imgarray = img.get_array()
        extent = img.get_extent()

        # Get the x and y index spacing
        x_space = np.linspace(extent[0], extent[1], imgarray.shape[1])
        y_space = np.linspace(extent[3], extent[2], imgarray.shape[0])

        # Find the closest index
        x_idx= (np.abs(x_space - event.xdata)).argmin()
        y_idx= (np.abs(y_space - event.ydata)).argmin()

        print 'X: {}, Y: {}'.format(x_idx, y_idx)
        print self.freqLabs[x_idx]
        print self.intenLabs[y_idx]

        self.ax.plot(event.xdata, event.ydata, 'r+', zorder=1)
        self.fig.canvas.draw()

        #Do something with the click data depending on the state
        statefunc = self.statefuncs[self.state]
        statefunc(x_idx, y_idx)

        self.state = self.transitions[self.state]

    def on_key_press(self, event):
        '''
        Method to listen for keypresses and take action
        '''

        #Functions to cycle through the dimensions
        if event.key=="<":
            self.thresh = self.thresh - self.step
            self.draw_tc()

        elif event.key=='>':
            self.thresh = self.thresh + self.step
            self.draw_tc()

        elif event.key=='n':
            self.setNone=True
            print "SET TO NONE, keep clicking"

    def get_cf(self, x_idx, y_idx):

        self.bestFreq = self.freqLabs[x_idx]
        self.threshold = self.intenLabs[y_idx]

        bwInten = self.threshold + self.dbAbove
        bwIntenIdx = np.where(self.intenLabs==bwInten)[0]

        self.ax.axhline(y = bwIntenIdx - 0.5, color='r', zorder=1)
        self.ax.axhline(y = bwIntenIdx + 0.5, color='r', zorder=1)

    def get_low(self, x_idx, y_idx):
        self.lowFreq = self.freqLabs[x_idx]

    def get_high(self, x_idx, y_idx):
        self.highFreq = self.freqLabs[x_idx]

    def die(self, x_idx, y_idx):
        plt.close(self.fig)
        if not self.setNone:
            self.Q10 = self.bestFreq / (self.highFreq - self.lowFreq)
        else:
            self.Q10 = np.nan

    def dead(self):
        pass


if __name__=='__main__':


    CASE=8

    if CASE==1:
        noiseburstMaxZ = []
        for index, cell in database.iterrows():
            maxZ = event_response_score(cell, 'NoiseBurst', maxZonly=True)
            noiseburstMaxZ.append(maxZ)

            sys.stdout.write('\r')
            progress = (index/np.double(len(database)))
            message = 'Calculating Noise Burst Max Z'
            sys.stdout.write("%s\n[%-20s] %d%%" % (message, '='*np.int(progress*20), np.int(progress*100)))
            sys.stdout.flush()


        laserpulseMaxZ = []
        for index, cell in database.iterrows():
            maxZ = event_response_score(cell, 'LaserPulse', maxZonly=True)
            laserpulseMaxZ.append(maxZ)

            sys.stdout.write('\r')
            progress = (index/np.double(len(database)))
            sys.stdout.write('Calculating Laser Pulse Max Z\n')
            sys.stdout.write("[%-20s] %d%%" % ('='*np.int(progress*20), np.int(progress*100)))
            sys.stdout.flush()

        lasertrainMaxZ = []
        for index, cell in database.iterrows():
            maxZ = event_response_score(cell, 'LaserTrain', maxZonly=True, skip=5,
                                        responseTimeRange = [0, 0.08])
            lasertrainMaxZ.append(maxZ)

            sys.stdout.write('\r')
            progress = (index/np.double(len(database)))
            sys.stdout.write('Calculating Laser Train Max Z (last pulse)\n')
            sys.stdout.write("[%-20s] %d%%" % ('='*np.int(progress*20), np.int(progress*100)))
            sys.stdout.flush()


        noiseburstMaxZ = np.array(noiseburstMaxZ)
        laserpulseMaxZ = np.array(laserpulseMaxZ)
        lasertrainMaxZ = np.array(lasertrainMaxZ)

        database['noiseburstMaxZ'] = noiseburstMaxZ
        database['laserpulseMaxZ'] = laserpulseMaxZ
        database['lasertrainMaxZ'] = lasertrainMaxZ

        database.to_pickle(dbfn)

    elif CASE==2:
        onecell = database.ix[34]
        loader = dataloader.DataLoader(onecell['subject'])
        ltsession = onecell['sessiontype'].index('LaserTrain')
        ltphys = onecell['ephys'][ltsession]
        ltspikes = loader.get_session_spikes(ltphys, int(onecell['tetrode']), cluster=int(onecell['cluster']))
        spikeTimestamps = ltspikes.timestamps

        ltevents = loader.get_session_events(ltphys)
        eventOnsetTimes = loader.get_event_onset_times(ltevents, minEventOnsetDiff=None)

        # timeRange = [-0.5, 1.0]
        # (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        #     spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimes,timeRange)
        # plt.clf()

        # plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.')
        # plt.show()

    elif CASE==3:
        lasertrainMaxZ = []
        for index, cell in database.iterrows():
            maxZ = event_response_score(cell, 'LaserTrain', maxZonly=True, skip=5,
                                        responseTimeRange = [0, 0.08])
            lasertrainMaxZ.append(maxZ)

            sys.stdout.write('\r')
            progress = (index/np.double(len(database)))
            sys.stdout.write('Calculating Laser Train Max Z (last pulse)\n')
            sys.stdout.write("[%-20s] %d%%" % ('='*np.int(progress*20), np.int(progress*100)))
            sys.stdout.flush()

        lasertrainMaxZ = np.array(lasertrainMaxZ)

    elif CASE==4:
        dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb.pickle'

        # dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb.pickle'
        database = pandas.read_pickle(dbfn)

        q10s = []
        ixs = []

        goodcells = database[(database['noiseburstMaxZ']>2) & (database['isiViolations']<4)]
        for index, cell in goodcells.iterrows():

            loader = dataloader.DataLoader(cell['subject'])

            try:
                tuningindex = cell['sessiontype'].index('TuningCurve')
            except ValueError:
                q10s.append(None)
                continue

            bdata = loader.get_session_behavior(cell['behavior'][tuningindex])

            possibleFreq = np.unique(bdata['currentFreq'])
            possibleInten = np.unique(bdata['currentIntensity'])

            #Break out of the loop if the tc does not have enough intensities
            if len(possibleInten)<3:
                q10s.append(np.nan)
                continue

            if len(possibleInten)>6:
                q10s.append(np.nan)
                continue

            zvalArray = tuning_curve_response(cell)
            tuner = TuningAnalysis(np.flipud(zvalArray), freqLabs = possibleFreq, intenLabs = possibleInten[::-1], thresh=None)

            button = True
            while button:
                button = plt.waitforbuttonpress()
            button = True
            while button:
                button = plt.waitforbuttonpress()
            button = True
            while button:
                button = plt.waitforbuttonpress()
            button = True
            while button:
                button = plt.waitforbuttonpress()
            q10 = tuner.Q10

            database.set_value(index, 'Q10', q10)

        # noiseburstSorted = np.array(
        #     [250,  75, 142, 132, 248, 249, 255, 186, 140, 127,  78, 208, 134,
        #      76, 137,  98, 141, 105,  94,  50,  53,  88, 109,  48, 214, 128,
        #      122,  82,  90,  79, 225,  42, 102, 236, 258,  17,  60, 213, 190,
        #      21, 202,  68,  13, 150,  31,  11, 139, 168, 170,  12,  16,  15,
        #      20,  18, 171, 114, 126,   0,   6,   2, 157, 165, 169,  49,  22,
        #      97,  66,  64,  62, 221, 212, 220, 164, 153, 151,  35,  19,  14,
        #      83,  61, 182,   5,  52,  65,  58, 123, 215, 237, 205, 161,  44,
        #      86,  23, 147, 149, 129, 264,   8, 203, 262, 260, 259, 167, 103,
        #      91,  72,  95, 184, 185, 187, 254,  67,  51, 224, 267, 217, 246,
        #      219,  46,  27,  32, 113,  85, 112, 183,  57,  54, 226, 211, 263,
        #      233,  10, 244, 133,  96,  26,  36,  81, 196,  63, 256, 253,  47,
        #      87,  24, 160, 104, 101,  41, 106, 156, 146, 188, 251, 118, 130,
        #      239,  89, 229,  25,  99,  73, 172,   1, 163,  37,  29,  92,  80,
        #      77, 136, 121, 125, 207,  28,  33,  84, 193, 120,  56, 210, 144,
        #      191, 194, 180, 195,  55, 138, 243,  30, 222, 175, 162, 119, 204,
        #      238,  74, 131, 245, 148, 135, 228, 115, 252, 117, 124, 223, 216,
        #      206, 166, 174, 159, 111,  40,   9,  93, 108, 107,  45, 178, 143,
        #      70, 231, 200, 268, 145, 100,   3, 235, 189, 158, 242, 152, 218,
        #      116, 173,  59,   4, 261,  71, 176, 192, 179, 110, 227, 198,  39,
        #      201, 266, 230, 241,   7,  43, 177,  34, 257, 197, 247, 155, 240,
        #      69, 232, 265, 199, 209, 181,  38, 154, 234])

        # for index in noiseburstSorted[::-1]:

        #     cell=database.ix[index]
        #     try:
        #         zvalArray = tuning_curve_response(cell)
        #         plt.clf()
        #         # plt.imshow(np.flipud(zvalArray>2), interpolation='none', cmap='gray')

        #         plt.show
        #     except ValueError:
        #         continue
        #     plt.waitforbuttonpress()


        #I Think the idea is going to go like this:
        ## Present a tc to the user
        ## User clicks on cf
        ## Draw a line at the right val above threshold
        ## User clicks on the shoulders of the tc

        # Save the values, in frequency (and threshold db) for each cell

        # From this, can calculate Q

    elif CASE==5:
        # dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb.pickle'
        dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb.pickle'
        database = pandas.read_pickle(dbfn)

        # cell = database.ix[10]

        goodcells = database[(database['noiseburstMaxZ']>2) & (database['laserpulseMaxZ']>2) & (database['lasertrainMaxZ']>2) & (database['isiViolations']<4)]

        for indcell, cell in goodcells.iterrows():
            plot_cell_phys(cell, ['NoiseBurst', 'LaserPulse', 'LaserTrain'], 'TuningCurve')
            # plot_cell_phys(cell, [None, None, None], 'TuningCurve')

            plt.suptitle('index: {}'.format(indcell))

            plt.tight_layout()
            plt.waitforbuttonpress()


    elif CASE==6:
        # dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb_q10.pickle'
        dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb_q10.pickle'
        database = pandas.read_pickle(dbfn)

        # for index in [881, 1236]: #Thalamus
        for index in [241, 197]: #Cortex

            print index
            plt.figure()
            plot_cell_tc(database.ix[index], 'TuningCurve')
            plt.tight_layout()
            ax = plt.gca()
            # plt.title(1/database.ix[index]['Q10'])
            fig = plt.gcf()
            fig.set_size_inches(4.3, 3.9)
            plt.tight_layout()
            # plt.show()

            plt.savefig('figs/cortex_tuning_{}.svg'.format(index))

    elif CASE==7:

        dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb.pickle'

        # dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb.pickle'
        database = pandas.read_pickle(dbfn)

        # goodcells = database[(database['noiseburstMaxZ']>2) & (database['laserpulseMaxZ']>2) & (database['lasertrainMaxZ']>2) & (database['isiViolations']<4)]
        goodcells = database[(database['noiseburstMaxZ']>2) & (database['laserpulseMaxZ']>2)]

        for indcell, cell in goodcells.iterrows():
            print cell['sessiontype']
            plot_cell_am(cell, 'AM')
            plt.suptitle('index: {}'.format(indcell))
            ax = plt.gca()
            ax.set_xticks(np.linspace(0, 15, 3))
            ax.set_xticklabels(np.round(np.logspace(np.log10(2), np.log10(40), 3), decimals=1))
            plt.tight_layout()
            plt.show()
            plt.waitforbuttonpress()

    elif CASE==8:
        # dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb_q10.pickle'
        dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb_q10.pickle'
        database = pandas.read_pickle(dbfn)

        # for index in [1054]:
        for index in [39]:

            plt.clf()
            plot_cell_am(database.ix[index], 'AM')
            fig = plt.gcf()
            fig.set_size_inches(5.2, 3.9)
            ax = plt.gca()
            ax.set_xticks([0, 0.5])
            extraplots.boxoff(ax)
            extraplots.set_ticks_fontsize(ax, 20)
            plt.tight_layout()
            plt.savefig('/tmp/cortex_am_{}.svg'.format(index))
            # plt.show()


    elif CASE==9:
        # dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb_q10.pickle'
        dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb_q10.pickle'
        database = pandas.read_pickle(dbfn)

        for indCell, cell in database.iterrows():
            r_val = am_dependence(cell)

            database.set_value(indCell, 'amRval', r_val)

        database.to_pickle(dbfn)


    

