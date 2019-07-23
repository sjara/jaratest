from matplotlib import pyplot as plt
import numpy as np
from jaratest.nick.database import dataloader_v2 as dataloader
from scipy import stats
from jaratoolbox import spikesanalysis

defaultTCtype = 'tc'

def tuning_curve_response(cell):
    '''
    Calculate max Z-score during the response period for each freq-inten combo in a TC
    '''

    try:
        sessiontypeIndex = cell['sessiontype'].index(defaultTCtype)
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

    baseRange = [-0.1, 0]
    responseRange = [0, 0.1]
    alignmentRange = [baseRange[0], responseRange[1]]

    zvalArray = np.zeros((len(possibleIntensity), len(possibleFreq)))

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

            zStat, pValue = stats.ranksums(nspkResp[:,0], nspkBase[:,0])

            zvalArray[indinten, indfreq] = zStat

    return zvalArray

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

        self.threshold = None
        self.highFreq = None
        self.lowFreq = None
        self.BW10 = None
        self.bestFreq = None

    def draw_tc(self):
        # self.ax.cla()
        if self.thresh:
            arr = self.tcArray>self.thresh
        else:
            arr = self.tcArray
        cax = self.ax.imshow(arr, interpolation='none', cmap='gray', zorder=0, vmin=0, vmax=3)
        plt.colorbar(cax)
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

        freq = np.logspace(np.log10(self.freqLabs[x_idx-1]),
                           np.log10(self.freqLabs[x_idx]),
                           3)[1]

        self.lowFreq = freq

    def get_high(self, x_idx, y_idx):

        freq = np.logspace(np.log10(self.freqLabs[x_idx]),
                           np.log10(self.freqLabs[x_idx+1]),
                           3)[1]

        self.highFreq = freq

    def die(self, x_idx, y_idx):
        plt.close(self.fig)
        if not self.setNone:
            # self.Q10 = self.bestFreq / (self.highFreq - self.lowFreq)
            self.BW10 = (self.highFreq - self.lowFreq) / self.bestFreq
        else:
            self.BW10 = np.nan

    def dead(self):
        pass






































