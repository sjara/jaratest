
from jaratoolbox.test.nick.database import dataloader
from jaratoolbox.test.nick.database import dataplotter
from jaratoolbox.test.nick.database import cellDB
from jaratoolbox import spikesorting
from matplotlib import pyplot as plt
from jaratoolbox import extraplots
figdb = cellDB.CellDB()
figdbFn = '/home/nick/data/database/figure_cells/figure_cells.json' #Change to path on your comp
figdb.load_from_json(figdbFn)
#This database has some cells that I gave santiago for the RO1 grant

#Below is a site with a good cortex cell that has a nice AM response


ac = cellDB.Experiment('pinp009', '2016-01-27', experimenter='nick', defaultParadigm='am_tuning_curve')
site2 = ac.add_site(depth=863, tetrodes=[4, 5, 6])
site2.add_session('17-14-57', None, 'noiseburst')
site2.add_session('17-17-35', None, 'laserpulse') #0.2-0.5mW
site2.add_session('17-19-44', None, 'lasertrain') #0.2-0.5mW
site2.add_session('17-23-19', 'acb', 'AM')
site2.add_session('17-42-52', None, 'laserpulse2') #0.2-0.5mW
site2.add_session('17-45-04', None, 'lasertrain2') #0.2-0.5mW
site2.add_session('17-49-18', 'acc', 'tuningCurve') #only 60dB
site2.add_session('17-53-22', 'acd', 'tuningCurve2') #30-60dB
site2.add_cluster(6, 2) #Unit with nice waveform and AM responses

figdb.add_clusters(site2.clusterList) #This cell is now cell 10 in the db


figure()
thalTCax = subplot(111)
spikeData, eventData, behavData = loader.get_cluster_data(figdb[4], 'TuningCurve')
spikeTimestamps = spikeData.timestamps
eventOnsetTimes = loader.get_event_onset_times(eventData)

intensityEachTrial = behavData['currentIntensity']
freqEachTrial = behavData['currentFreq']

possibleFreq = np.unique(freqEachTrial)
possibleIntensity = np.unique(intensityEachTrial)


timeRangeBaseline = [-0.2, -0.1]
timeRangeResponse = [0, 0.1]

spikeTimesFromEventOnsetBaseline, trialIndexForEachSpikeBaseline, indexLimitsEachTrialBaseline = spikesanalysis.eventlocked_spiketimes(spikeTimestamps, eventOnsetTimes, timeRangeBaseline)
spikeTimesFromEventOnsetResponse, trialIndexForEachSpikeResponse, indexLimitsEachTrialResponse = spikesanalysis.eventlocked_spiketimes(spikeTimestamps, eventOnsetTimes, timeRangeResponse)

pvalmat = np.ones([len(possibleIntensity), len(possibleFreq)])
zscoremat = np.ones([len(possibleIntensity), len(possibleFreq)])

for indfreq, freq in enumerate(possibleFreq):
# for indfreq, freq in enumerate([2000]):
   for indinten, inten in enumerate(possibleIntensity):
   # for indinten, inten in enumerate([70]):
      select = np.flatnonzero((freqEachTrial==freq)&(intensityEachTrial==inten))

      selectspikesBaseline = spikeTimesFromEventOnsetBaseline[np.in1d(trialIndexForEachSpikeBaseline, select)]
      selectspikesResponse = spikeTimesFromEventOnsetResponse[np.in1d(trialIndexForEachSpikeResponse, select)]

      selectindsBaseline = trialIndexForEachSpikeBaseline[np.in1d(trialIndexForEachSpikeBaseline, select)]
      selectindsResponse = trialIndexForEachSpikeResponse[np.in1d(trialIndexForEachSpikeResponse, select)]

      selectlimitsBaseline = indexLimitsEachTrialBaseline[:, select]
      selectlimitsResponse = indexLimitsEachTrialResponse[:, select]

      numSpikesEachTrialBaseline = np.squeeze(np.diff(selectlimitsBaseline, axis=0))
      numSpikesEachTrialResponse = np.squeeze(np.diff(selectlimitsResponse, axis=0))

      wilcoxen = ranksums(numSpikesEachTrialResponse, numSpikesEachTrialBaseline)

      zscore = wilcoxen[0]
      pval = wilcoxen[1]

      pvalmat[indinten, indfreq] = pval
      zscoremat[indinten, indfreq] = zscore

figure()
a = pvalmat<0.05
imshow(flipud(a), cmap='Blues', interpolation='none', aspect='auto')

figure()
imshow(flipud(zscoremat>3), interpolation='none', aspect='auto')


figure()
clusterfuncs.plot_cluster_tuning(figdb[4], 'TuningCurve')
annotate('*', xy=(100,1), xytext=(0,0), color='r')



freqLabels = ["%.1f" % freq for freq in possibleFreq/1000.0]



thalTCax.set_xticks([2, 4, 6, 8, 10, 12, 14])
thalTCax.set_xticklabels([])
thalTCax.set_ylabel('Intensity (db SPL)', fontsize=10)
extraplots.set_ticks_fontsize(thalTCax, 10)
cbar.set_ticks([4.0, 12.0])
cbar.ax.set_yticklabels([40, 120], fontsize=10)
cbar.ax.set_ylabel('Firing rate (Hz)', rotation=270, fontsize=10, labelpad=-5)
thalTCax.set_xticks(np.linspace(1, 15, 5))
thalTCax.set_xticklabels([2, 4, 8, 16, 32])
extraplots.set_ticks_fontsize(thalTCax, 10)
thalTCax.set_xlabel('Sound Frequency (kHz)', fontsize=10, labelpad=2)
