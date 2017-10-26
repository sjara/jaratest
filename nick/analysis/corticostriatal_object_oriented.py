import pandas
from matplotlib import pyplot as plt
from collections import Counter
from jaratest.nick.stats import am_funcs
reload(am_funcs)
import numpy as np
from numpy import inf
from jaratoolbox import colorpalette
from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from scipy import optimize
from scipy import stats
from scipy import signal
import datetime

#Its just functions that load data when given a 'cell' from the celldatabase
from jaratest.nick.database import dataloader_v3 as dataloader
reload(dataloader)

from jaratest.nick.stats import tuningfuncs
from jaratest.nick.reports import pinp_report
reload(pinp_report)


class Analysis(object):

    def __init__(self):
        self.db = None
        self.inforecFolderFormat = '/home/nick/src/jaratest/nick/inforecordings/{}/{}_inforec.py' #(mouse, mouse)

    def load_db(self, dbFn):
        '''
        Sets self.db to the dataframe stored in an hdf file
        '''
        self.db = pandas.read_hdf(dbFn, 'database')

        # self.dbFolderFormat = '/home/nick/data/database/{}/{}_database.h5' #(mouse, mouse)
    def new_db(self, mice):
        '''
        Sets self.db to a new database built from a list of mice (uses their inforec files)
        '''
        dbs = []
        for mouse in mice:
            db = celldatabase.generate_cell_database(self.inforecFolderFormat.format(mouse, mouse))
            dbs.append(db)
        self.db = pandas.concat(dbs, ignore_index=True)

    def append_db(self, dbFn):
        '''
        Load an existing HDF5 database file and append it to self.db
        This is used when we need to calculate all features for a new mouse and append the other mice
        '''
        existingDB = pandas.read_hdf(dbFn, 'database')
        self.db = pandas.concat([self.db, existingDB], ignore_index=True)

    def calculate_shape_quality(self, dataframe=None):
        '''
        Calculate the shape quality for each cluster in the whole database or a subset

        '''
        #Use the whole database by default
        if dataframe is None:
            dataframe = self.db

        allShapeQuality = np.empty(len(dataframe))
        for indCell, cell in dataframe.iterrows():
            peakAmplitudes = cell['clusterPeakAmplitudes']
            spikeShapeSD = cell['clusterSpikeSD']
            shapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
            allShapeQuality[indCell] = shapeQuality
        allShapeQuality[allShapeQuality==inf]=0

        #NOTE: If we use self.db this should set the values directly, right??
        #TODO: Test this
        dataframe['shapeQuality'] = allShapeQuality
        return dataframe


    def calculate_response_score(self, spikeTimestamps, eventOnsetTimes, baseRange, responseRange):
        '''
        Calculate z-score and p-val for ranksums comparison of num spikes in response v. base range
        '''
        alignmentRange = [baseRange[0], responseRange[1]]
        (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimestamps,
                                                                    eventOnsetTimes,
                                                                    alignmentRange)
        nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            baseRange)
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            responseRange)
        [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)
        return zScore, pVal

    def calculate_noiseburst_response(self, dataframe=None):

        #Use the whole database by default
        if dataframe is None:
            dataframe = self.db

        #Calculate noiseburst response
        #TODO: Response to things other than noise as well??
        noiseZscore = np.empty(len(dataframe))
        noisePval = np.empty(len(dataframe))
        baseRange = [-0.2,0]
        responseRange = [0, 0.2]
        for indCell, cell in dataframe.iterrows():
            spikeData, eventData = dataloader.get_session_ephys(cell, 'noiseburst')
            eventOnsetTimes = eventData.get_event_onset_times()
            if spikeData.timestamps is not None:
                zScore, pVal = self.calculate_response_score(spikeData.timestamps,
                                                            eventOnsetTimes,
                                                            baseRange,
                                                            responseRange)
                noiseZscore[indCell] = zScore
                noisePval[indCell] = pVal
            else:
                noiseZscore[indCell] = None
                noisePval[indCell] = None
        dataframe['noiseZscore'] = noiseZscore
        dataframe['noisePval'] = noisePval

    def calculate_laser_pulse_response(self, dataframe=None):

        #Use the whole database by default
        if dataframe is None:
            dataframe = self.db

        #Laser pulse response
        pulseZscore = np.empty(len(dataframe))
        pulsePval = np.empty(len(dataframe))
        baseRange = [-0.1,0]
        responseRange = [0, 0.1]
        for indCell, cell in dataframe.iterrows():
            spikeData, eventData = dataloader.get_session_ephys(cell, 'laserpulse')
            eventOnsetTimes = eventData.get_event_onset_times()
            if spikeData.timestamps is not None:
                zScore, pVal = self.calculate_response_score(spikeData.timestamps,
                                                            eventOnsetTimes,
                                                            baseRange,
                                                            responseRange)
                pulseZscore[indCell] = zScore
                pulsePval[indCell] = pVal
            else:
                pulseZscore[indCell] = None
                pulsePval[indCell] = None

        dataframe['pulseZscore'] = pulseZscore
        dataframe['pulsePval'] = pulsePval

    def calculate_laser_train_ratio(self, dataframe=None):

        #Use the whole database by default
        if dataframe is None:
            dataframe = self.db

        #Laser train response, ratio of pulse avg spikes
        trainRatio = np.empty(len(dataframe))
        timeRange = [-0.1, 1] #For initial alignment
        baseRange = [0, 0.05] #Base range is response to first pulse
        responseRange = [0.2, 0.25] #Response to 3rd pulse
        for indCell, cell in dataframe.iterrows():
            spikeData, eventData = dataloader.get_session_ephys(cell, 'lasertrain')
            eventOnsetTimes = eventData.get_event_onset_times()
            eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)
            if spikeData.timestamps is not None:
                (spikeTimesFromEventOnset,
                trialIndexForEachSpike,
                indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                            eventOnsetTimes,
                                                                            timeRange)
                avgSpikesBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                        indexLimitsEachTrial,
                                                                        baseRange).mean()
                avgSpikesResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                        indexLimitsEachTrial,
                                                                        responseRange).mean()
                ratio = avgSpikesResp/avgSpikesBase
                trainRatio[indCell] = ratio
            else:
                trainRatio[indCell] = None
        dataframe['trainRatio'] = trainRatio

    def calculate_am_statistics(self, dataframe=None):
        #AM stats - calculates KW anova on number of spikes during stimulus for each AM rate
        amKWstat = np.empty(len(dataframe))
        amKWp = np.empty(len(dataframe))

        for indCell, cell in dataframe.iterrows():
            spikeData, eventData = dataloader.get_session_ephys(cell, 'am')
            eventOnsetTimes = eventData.get_event_onset_times()
            bdata = dataloader.get_session_bdata(cell, 'am')

            if spikeData.timestamps is not None:
                rateEachTrial = bdata['currentFreq'] #NOTE: bdata uses 'Freq' but this is AM so I'm calling it rate
                possibleRate = np.unique(rateEachTrial)
                timeRange = [0, 0.5]
                respSpikeArrays = [] #List to hold the arrays of response bin spike counts (not all same number of trials)
                respSpikeInds = [] #This will hold arrays with the inds for which rate the response spikes came from
                for indRate, thisRate in enumerate(possibleRate):
                    trialsThisRate = np.flatnonzero(rateEachTrial==thisRate)
                    (spikeTimesFromEventOnset,
                    trialIndexForEachSpike,
                    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                                eventOnsetTimes[trialsThisRate],
                                                                                timeRange)
                    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                        indexLimitsEachTrial,
                                                                        timeRange)
                    respSpikeArrays.append(nspkResp.ravel())

                try:
                    statistic, pval = stats.kruskal(*respSpikeArrays)
                except ValueError:
                    pval=None
                    statistic=None

                amKWp[indCell] = pval
                amKWstat[indCell] = statistic
            else:
                amKWp[indCell] = None
                amKWstat[indCell] = None

        dataframe['amKWp'] = amKWp
        dataframe['amKWstat'] = amKWstat

    @staticmethod
    def rayleigh_test(r, n):
        #r (mean vector length) comes from the vectorstrength calculation (as strength)
        #Rayleigh's R statistic = n (number of samples) * r (mean vector length)
        #The probability of R is approximated by:
        # R = n*r
        # P = exp[ sqrt( 1+4*n+4(n**2 - R**2) ) - (1+2*n) ]
        # From Biostatistical Analysis, Zar, 3rd edition eq 26.4, cites Greenwood and Durand, 1955
        R = n*r
        p = np.exp( np.sqrt( 1+4*n+4*(n**2 - R**2) ) - (1+2*n) )
        return p

    def calculate_highest_significant_sync_rate(self, dataframe=None):

        #Use the whole database by default
        if dataframe is None:
            dataframe = self.db

        #Highest significant sync rate
        #TODO: I need to unit test this part
        highestSync = np.empty(len(dataframe))
        for indCell, cell in dataframe.iterrows():
            spikeData, eventData = dataloader.get_session_ephys(cell, 'am')
            bdata = dataloader.get_session_bdata(cell, 'am')
            eventOnsetTimes = eventData.get_event_onset_times(eventChannel=5)
            eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)

            if spikeData.samples is not None:

                #NOTE: This is where I am ignoring the onset response. is 50msec sufficient??
                timeRange = [0.05, 0.5]

                freqEachTrial = bdata['currentFreq']
                possibleFreq = np.unique(freqEachTrial)

                (spikeTimesFromEventOnset,
                trialIndexForEachSpike,
                indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                            eventOnsetTimes,
                                                                            timeRange)
                allRayleighPvals = np.zeros(len(possibleFreq))
                for indFreq, oneFreq in enumerate(possibleFreq):
                    trialsThisFreq = np.flatnonzero(freqEachTrial==oneFreq)
                    spikeTimesThisFreq = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, trialsThisFreq)]

                    #Number of radians in one second for this stimulus frequency
                    radsPerSec=oneFreq*2*np.pi
                    period = 1.0/oneFreq
                    spikeRads = (spikeTimesThisFreq*radsPerSec)%(2*np.pi)

                    #Compute average vector length and angle
                    strength, phase = signal.vectorstrength(spikeTimesThisFreq, period)

                    #Compute prob for the rayleigh statistic
                    p = self.rayleigh_test(strength, len(spikeTimesThisFreq))
                    allRayleighPvals[indFreq] = p

                if np.any(allRayleighPvals<0.05):
                    hs = np.max(possibleFreq[allRayleighPvals<0.05])
                else:
                    hs = 0
                highestSync[indCell] = hs

            else:
                highestSync[indCell] = 0

        dataframe['highestSync'] = highestSync

    @staticmethod
    def gaussian(x, a, x0, sigma):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))

    @staticmethod
    def index_all_true_after(arr):
        '''
        Find the index for a boolean array where all the inds after are True
        Args:
            arr (1-d array of bool): an array of boolean vals
        Returns:
            ind (int): The index of the first True val where all subsequent vals are also True
        '''
        for ind, _ in enumerate(arr):
            miniarr = arr[ind:]
            if np.all(miniarr):
                return ind

    def calculate_tuning_curve_params(self, dataframe):

        #Use the whole database by default
        if dataframe is None:
            dataframe = self.db

        #Tuning curve estimation
        #DONE: Need to make this method use the continuous curves we fit

        cfs = np.full(len(dataframe), np.nan)
        thresholds = np.full(len(dataframe), np.nan)
        lowerFreqs = np.full(len(dataframe), np.nan)
        upperFreqs = np.full(len(dataframe), np.nan)

        for indCell, cell in dataframe.iterrows():
            try:
                spikeData, eventData = dataloader.get_session_ephys(cell, 'tc')
                bdata = dataloader.get_session_bdata(cell, 'tc')
            except IndexError: #The cell does not have a tc
                print "No tc for cell {}".format(indCell)
                thresholds[indCell] = None
                cfs[indCell] = None
                lowerFreqs[indCell] = None
                upperFreqs[indCell] = None
                continue

            eventOnsetTimes = eventData.get_event_onset_times()

            if spikeData.timestamps is not None:

                baseRange = [-0.2, 0]
                responseRange = [0, 0.2]
                alignmentRange = [baseRange[0], responseRange[1]]
                freqEachTrial = bdata['currentFreq']
                possibleFreq = np.unique(freqEachTrial)
                intensityEachTrial = bdata['currentIntensity']
                possibleIntensity = np.unique(intensityEachTrial)
                allBaselineCountArrays = []
                aboveBaseline = []
                popts = []

                for indinten, inten in enumerate(possibleIntensity):
                    spks = np.array([])
                    # inds = np.array([])
                    freqs = np.array([])
                    base = np.array([])
                    for indfreq, freq in enumerate(possibleFreq):
                        selectinds = np.flatnonzero((freqEachTrial==freq)&(intensityEachTrial==inten))
                        selectedOnsetTimes = eventOnsetTimes[selectinds]
                        (spikeTimesFromEventOnset,
                        trialIndexForEachSpike,
                        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
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
                        # inds = np.concatenate([inds, np.ones(len(nspkResp.ravel()))*indfreq])
                        freqs = np.concatenate([freqs, np.ones(len(nspkResp.ravel()))*freq])

                    allBaselineCountArrays.append(base)

                    #DONE: Finish setting the initial param guesses and bounds for fitting in log2(freq) space
                    try:
                        popt, pcov = optimize.curve_fit(self.gaussian, #Fit the curve for this intensity
                                                        np.log2(freqs),
                                                        spks,
                                                        p0=[1, np.log2(possibleFreq[7]), 1],
                                                        bounds=([0, np.log2(possibleFreq[0]), 0],
                                                                [inf, np.log2(possibleFreq[-1]), inf]))
                        popts.append(popt) #Save the curve paramaters
                    except RuntimeError:
                        print "RUNTIME ERROR, Cell {}".format(indCell)
                        thresholds[indCell] = None
                        cfs[indCell] = None
                        lowerFreqs[indCell] = None
                        upperFreqs[indCell] = None
                        break

                    #Save whether the max fitted val of the curve is greater than base+1s.d.
                    #This is discrete, we want to maximize on the continuous function
                    # aboveBaseline.append(max(self.gaussian(inds, *popt)) > base.mean()+base.std())
                    #DONE: This needs to be finished after I change to fitting in log(freq) space
                    fm = lambda x: -self.gaussian(x, *popt)
                    r = optimize.minimize_scalar(fm, bounds=(np.log2(possibleFreq[0]), np.log2(possibleFreq[-1])))
                    # maxX = 2**r["x"] #The max x val is a log2(freq) value, so convert back to freq
                    aboveBaseline.append(self.gaussian(r["x"], *popt)>(base.mean()+base.std()))

                aboveBaseline = np.array(aboveBaseline)
                indintenFirstAbove = self.index_all_true_after(aboveBaseline)
                #TODO: I need to find the max for THIS curve and save that as cf
                #TODO: Need to save the intensity
                if indintenFirstAbove is None:
                    #No frequencies pass the threshold
                    threshold = None
                    cf = None
                    continue
                else:
                    threshold = possibleIntensity[indintenFirstAbove]
                    #Find the max for the threshold intensity
                    poptFirstAbove = popts[indintenFirstAbove]
                    fm = lambda x: -self.gaussian(x, *poptFirstAbove)
                    r = optimize.minimize_scalar(fm, bounds=(np.log2(possibleFreq[0]), np.log2(possibleFreq[-1])))
                    cf = 2**r["x"] #The max x val is a log2(freq) value, so convert back to freq

                indinten10aboveThresh = indintenFirstAbove+2
                baselineAllIntensities = np.concatenate(allBaselineCountArrays)

                try:
                    popt10Above = popts[indinten10aboveThresh]
                    #TODO: using this set of popts, find the point where the curve crosses y=base.mean+base.std
                    #We need to find the max using these popts as well so we know the midpoint
                    fm = lambda x: -self.gaussian(x, *popt10Above)
                    r = optimize.minimize_scalar(fm, bounds=(np.log2(possibleFreq[0]), np.log2(possibleFreq[-1])))

                    xMax = r["x"]

                    #The function to find roots for. curve minus the baseline+std
                    fr = lambda x: self.gaussian(x, *popt10Above) - (baselineAllIntensities.mean()+baselineAllIntensities.std())

                    #Check the inputs first. fr(a) and fr(b) need to be opposite sign for root finding to work
                    #Lower root finding
                    alower = np.log2(possibleFreq[0]) #The minimum x val
                    blower = xMax #The x value of the function max
                    if np.sign(fr(alower)) != np.sign(fr(blower)):
                        rootLower = optimize.brentq(fr, alower, blower)
                        lowerFreq = 2**rootLower
                    else:
                        lowerFreq = None

                    #Upper root
                    aupper = xMax #The minimum x val
                    bupper = np.log2(possibleFreq[-1]) #The x value of the function max
                    if np.sign(fr(aupper)) != np.sign(fr(bupper)):
                        rootUpper = optimize.brentq(fr, aupper, bupper)
                        upperFreq = 2**rootUpper
                    else:
                        upperFreq = None
                except IndexError:
                    #We were not able to catch 10db above threshold. In this case, we can still get cf and thresh, but not uF/lF
                    upperFreq = None
                    lowerFreq = None
                    continue

                #Things to save
                thresholds[indCell] = threshold
                cfs[indCell] = cf
                lowerFreqs[indCell] = lowerFreq
                upperFreqs[indCell] = upperFreq

            else:
                thresholds[indCell] = None
                cfs[indCell] = None
                lowerFreqs[indCell] = None
                upperFreqs[indCell] = None

        dataframe['threshold'] = thresholds
        dataframe['cf'] = cfs
        dataframe['lowerFreq'] = lowerFreqs
        dataframe['upperFreq'] = upperFreqs

if __name__=="__main__":
    # mice = ['pinp015', 'pinp016', 'pinp017', 'pinp018']

    mice = ['pinp019']
    aobj = Analysis(mice)
    aobj.calculate_shape_quality(dataframe=aobj.db)
    aobj.calculate_noiseburst_response(dataframe=aobj.db)
    aobj.calculate_laser_pulse_response(dataframe=aobj.db)
    aobj.calculate_laser_train_ratio(dataframe=aobj.db)
    aobj.calculate_am_statistics(dataframe=aobj.db)
    aobj.calculate_highest_significant_sync_rate(dataframe=aobj.db)
    aobj.calculate_tuning_curve_params(dataframe=aobj.db)

    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    aobj.db.to_hdf('/home/nick/data/database/corticostriatal_pinp019_{}.h5'.format(now), 'database')
    aobj.append_existing_db('/home/nick/data/database/corticostriatal_master_2017-05-29_15-47-34.h5')
    aobj.db.to_hdf('/home/nick/data/database/corticostriatal_master_{}.h5'.format(now), 'database')

    # aobj.db.to_hdf('/home/nick/data/database/corticostriatal_master_{}.h5'.format(now), 'database')

# masterdb['BW10'] = 1/masterdb['Q10']

# soundResponsive = masterdb.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
# soundLaserResponsive = soundResponsive.query('pulsePval<0.05 and trainRatio>0.8')

# soundResponsive['Identified'] = (soundResponsive.pulsePval<0.05) & (soundResponsive.trainRatio>0.8)

# soundResponsive = masterdb.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
# soundLaserResponsive = soundResponsive.query('pulsePval<0.05 and trainRatio>0.8')


# # plt.clf()
# # stdev = 0.05
# # markersize = 8
# # linewidth = 2
# # thalColor = colorpalette.TangoPalette['Orange2']
# # cortColor = colorpalette.TangoPalette['Plum2']


# # colors = {'rightThal':thalColor, 'rightAC':cortColor}

# # #Hist of highestSync
# plt.hold(1)
# plt.clf()
# plt.hist(soundResponsive.groupby('brainarea').get_group('rightThal')['highestSync'], histtype='step', lw = 2)
# plt.hist(soundResponsive.groupby('brainarea').get_group('rightAC')['highestSync'], histtype='step', lw = 2)
# plt.show()

# # #Hist of amRval
# plt.clf()
# plt.hold(1)
# plt.hist(soundResponsive.groupby('brainarea').get_group('rightThal')['amRval'], histtype='step', lw = 2)
# plt.hist(soundResponsive.groupby('brainarea').get_group('rightAC')['amRval'], histtype='step', lw = 2)
# plt.xlabel('Correlation R val between AM rate and overall FR during stim', fontsize=14)
# plt.show()

# #Hist of BW10
# # plt.clf()
# # plt.hold(1)
# # plt.hist(soundResponsive.groupby('brainarea').get_group('rightThal')['BW10'].dropna(), histtype='step', lw = 2)
# # plt.hist(soundResponsive.groupby('brainarea').get_group('rightAC')['BW10'].dropna(), histtype='step', lw = 2)
# # plt.show()

# #Thresholds
# #Nurons that had a BW10 have a valid threshold. otherwise, I was clicking to move the program forward
# hadBW10 = soundResponsive[pandas.notnull(soundResponsive.BW10)]
# plt.clf()
# plt.hold(1)
# plt.hist(hadBW10.groupby('brainarea').get_group('rightThal')['threshold'].dropna(), histtype='step', lw = 2)
# plt.hist(hadBW10.groupby('brainarea').get_group('rightAC')['threshold'].dropna(), histtype='step', lw = 2)
# plt.show()

# #Plot reports
# thalSR = soundResponsive.groupby('brainarea').get_group('rightThal')
# fig_path = '/home/nick/data/database/corticostriatal_master_20170425/reports_SR_thal/'
# for indCell, cell in thalSR.iterrows():
#     pinp_report.plot_pinp_report(cell, fig_path)

# cortSR = soundResponsive.groupby('brainarea').get_group('rightAC')
# fig_path = '/home/nick/data/database/corticostriatal_master_20170425/reports_SR_ctx/'
# for indCell, cell in cortSR.iterrows():
#     pinp_report.plot_pinp_report(cell, fig_path)
