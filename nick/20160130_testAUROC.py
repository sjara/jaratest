from jaratoolbox.test.nick.database import dataloader
from jaratoolbox.test.nick.database import dataplotter
from jaratoolbox.test.nick.database import cellDB
from jaratoolbox.test.nick.database import clusterfuncs
from jaratoolbox import spikesorting
from matplotlib import pyplot as plt
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis


reload(cellDB)
reload(clusterfuncs)

figdb = cellDB.CellDB()
figdbFn = '/home/nick/data/database/pinp003_thalamus_cells.json'
figdb.load_from_json(figdbFn)

loader = dataloader.DataLoader('offline', experimenter='nick')

figdb[0].get_session_types()

clusterfuncs.plot_cluster_tuning(figdb[1], 3)

spikeData, eventData, behavData = loader.get_cluster_data(figdb[1], 3)


currentFreq = behavData['currentFreq']
possibleFreq = np.unique(currentFreq)
currentIntensity=behavData['currentIntensity']
possibleIntensity = np.unique(currentIntensity)



spikeTimestamps=spikeData.timestamps
eventOnsetTimes=loader.get_event_onset_times(eventData)
timeRange = [-0.5, 1]

spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
    spikeTimestamps, eventOnsetTimes, timeRange)





def num_spikes_in_timerange_select_trials(spikeTimestamps, eventOnsetTimes, timeRange, selectInds):
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimestamps, eventOnsetTimes, timeRange)
    numSpikesEachTrial=squeeze(diff(indexLimitsEachTrial, axis=0))
    numSpikesSelectTrials=numSpikesEachTrial[selectInds]

    return numSpikesSelectTrials





#####################################################
### Code to plot the auroc versus baseline for all times, all freqs
from sklearn.metrics import roc_curve, auc

starts = arange(-0.5, 1, 0.1)
stops = arange(-0.4, 1.1, 0.1)
ranges = vstack((starts, stops))

auroc_mat = zeros([len(possibleFreq), len(starts)])

for indFreq, freq in enumerate(possibleFreq):
    select = np.flatnonzero((currentFreq==freq)&(currentIntensity==70))

    baselineRange = [-0.3, -0.2]

    spikesBaseline = num_spikes_in_timerange_select_trials(spikeTimestamps, eventOnsetTimes, baselineRange, select)

    labelsBaseline = np.zeros(len(spikesBaseline))


    for indRange in range(len(starts)):

        spikesThisRange = num_spikes_in_timerange_select_trials(spikeTimestamps, eventOnsetTimes, ranges[:,indRange], select)
        labelsThisRange = np.ones(len(spikesThisRange))

        spikes = np.concatenate((spikesBaseline, spikesThisRange))
        labels = np.concatenate((labelsBaseline, labelsThisRange))

        fpr, tpr, thresholds = roc_curve(labels, spikes)
        auroc = auc(fpr, tpr)

        auroc_mat[indFreq, indRange] = auroc


ax=subplot(111)
cm = ax.imshow(auroc_mat, interpolation='none', cmap='bwr')
cm.set_clim([0, 1])
ax.set_yticklabels(possibleFreq/1000)

#########################################################################

#Now I want to plot the auroc versus the response to all other freqencies,
#all at a single intensity

auroc_mat = zeros((len(possibleFreq), len(possibleFreq)))

responseRange = [0, 0.1]
intensity = 70

for indFreq1, freq1 in enumerate(possibleFreq):
    selectFreq1 = np.flatnonzero((currentFreq==freq1)&(currentIntensity==intensity))

    spikesFreq1 = num_spikes_in_timerange_select_trials(spikeTimestamps, eventOnsetTimes, responseRange, selectFreq1)
    labelsFreq1 = ones(len(spikesFreq1)) #The first freq is the ones

    for indFreq2, freq2 in enumerate(possibleFreq):
        selectFreq2 = np.flatnonzero((currentFreq==freq2)&(currentIntensity==intensity))

        spikesFreq2 = num_spikes_in_timerange_select_trials(spikeTimestamps, eventOnsetTimes, responseRange, selectFreq2)
        labelsFreq2 = zeros(len(spikesFreq2)) #THe second freq is the zeros

        spikes = concatenate((spikesFreq1, spikesFreq2))
        labels = concatenate((labelsFreq1, labelsFreq2))

        fpr, tpr, thresholds = roc_curve(labels, spikes)
        auroc = auc(fpr, tpr)

        auroc_mat[indFreq2, indFreq1] = auroc

ax=subplot(111)
cm = ax.imshow(auroc_mat, interpolation='none', cmap = 'bwr')
colorbar(cm)
cm.set_clim([0, 1])
ax.set_yticks(range(len( possibleFreq )))
ax.set_yticklabels(["{:2.1f}".format(x) for x in possibleFreq/1000])
ax.set_xticks(range(len( possibleFreq )))
ax.set_xticklabels(["{:2.1f}".format(x) for x in possibleFreq/1000], rotation='vertical')


##############################################
#Now I want to plot the auroc versus baseline for each frequency, each intensity



auroc_mat = zeros([len(possibleIntensity), len(possibleFreq)])
baselineRange = [-0.3, -0.2]
responseRange = [0, 0.1]

for indFreq, freq in enumerate(possibleFreq):
    for indInten, intensity in enumerate(possibleIntensity):

        select = np.flatnonzero((currentFreq==freq)&(currentIntensity==intensity))


        spikesBaseline = num_spikes_in_timerange_select_trials(spikeTimestamps, eventOnsetTimes, baselineRange, select)
        labelsBaseline = zeros(len(spikesBaseline))

        spikesResponse = num_spikes_in_timerange_select_trials(spikeTimestamps, eventOnsetTimes, responseRange, select)
        labelsResponse = ones(len(spikesResponse))


        spikes = concatenate((spikesBaseline, spikesResponse))
        labels = concatenate((labelsBaseline, labelsResponse))

        fpr, tpr, thresholds = roc_curve(labels, spikes)
        auroc = auc(fpr, tpr)

        auroc_mat[indInten, indFreq] = auroc


ax=subplot(111)
cm = ax.imshow(flipud(auroc_mat), interpolation='none', cmap = 'RdGy', aspect='auto')
colorbar(cm)
cm.set_clim([0, 1])
ax.set_yticks(range(len( possibleIntensity )))
ax.set_yticklabels(["{:2.1f}".format(x) for x in possibleIntensity][::-1])
ax.set_xticks(range(len( possibleFreq )))
ax.set_xticklabels(["{:2.1f}".format(x) for x in possibleFreq/1000], rotation='vertical')


###############
#I now have code to test the responses through time, the responses relative to other freqs,
#and the responses relative to different intensities (resp versus baseline)








#DEBUG
select = np.flatnonzero((currentFreq==2000)&(currentIntensity==70))

baselineRange = [-0.3, -0.2]

spikesBaseline = num_spikes_in_timerange_select_trials(spikeTimestamps, eventOnsetTimes, baselineRange, select)

labelsBaseline = zeros(len(spikesBaseline))

thisRange = ranges[:,0]

spikesThisRange = num_spikes_in_timerange_select_trials(spikeTimestamps, eventOnsetTimes, thisRange, select)
labelsThisRange = ones(len(spikesThisRange))

spikes = concatenate((spikesBaseline, spikesThisRange))
labels = concatenate((labelsBaseline, labelsThisRange))

#CALCULATE AUROC AND PLOT!!
fpr, tpr, thresholds = roc_curve(labels, spikes)
auroc = auc(fpr, tpr)
plot(fpr, tpr)






plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')


select= np.flatnonzero((currentIntensity==70) & (currentFreq==possibleFreq[6]))

selectspikes = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, select)]
selectinds = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, select)]

plot(selectspikes, selectinds, '.')

####This is a good hack to reduce the index vals once they are selected
squeezedinds=array([list(unique(selectinds)).index(x) for x in selectinds])

plot(selectspikes, squeezedinds, '.')


baseline=[-0.5, -0.25]
response=[0, 0.25]



#Count the spikes for each trial that fall into the baseline window
baselineSpikes=[]
for ind in unique(squeezedinds):
    spikesOneTrial = selectspikes[squeezedinds==ind]
    numspikesBaseline = (spikesOneTrial>baseline[0]) & (spikesOneTrial<baseline[1])
    numspikesBaseline=numspikesBaseline.sum()
    baselineSpikes.append(numspikesBaseline)

# count the spike times for each trial that fall within the response time window
responseSpikes=[]
for ind in unique(squeezedinds):
    spikesOneTrial = selectspikes[squeezedinds==ind]
    numspikesResponse = (spikesOneTrial>response[0]) & (spikesOneTrial<response[1])
    numspikesResponse=numspikesResponse.sum()
    responseSpikes.append(numspikesResponse)

maxSpikes=max(responseSpikes)

#Make as an array 
baselineSpikes=array(baselineSpikes)
responseSpikes=array(responseSpikes)


baselineAboveCriterion=[]
responseAboveCriterion=[]
for i in range(0, maxSpikes):
    baselineAboveCriterion.append((baselineSpikes>=i).sum()/float(len(baselineSpikes)))
    responseAboveCriterion.append((responseSpikes>=i).sum()/float(len(baselineSpikes)))

#Compute the area under the ROC curve

#Have to re-order in ascending
auroc=trapz(responseAboveCriterion[::-1], x=baselineAboveCriterion[::-1])


#Re-calculate for different response range

response=[0.25, 0.5]
responseSpikes=[]
for ind in unique(squeezedinds):
    spikesOneTrial = selectspikes[squeezedinds==ind]
    numspikesResponse = (spikesOneTrial>response[0]) & (spikesOneTrial<response[1])
    numspikesResponse=numspikesResponse.sum()
    responseSpikes.append(numspikesResponse)

#Have to reset the response spikes as an array each time
responseSpikes=array(responseSpikes)

baselineAboveCriterion=[]
responseAboveCriterion=[]
for i in range(0, maxSpikes):
    baselineAboveCriterion.append((baselineSpikes>=i).sum()/float(len(baselineSpikes)))
    responseAboveCriterion.append((responseSpikes>=i).sum()/float(len(baselineSpikes)))




###winner winner chicken dinner - much better method


#####Baseline spikes
#The trials you want to look at
select= np.flatnonzero((currentIntensity==70) & (currentFreq==possibleFreq[6]))

#The onset times for those trials
selectedOnsetTimes = eventOnsetTimes[select]

#The timerange you want to look at
timeRange_baseline = [-0.5, -0.25]

spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
    spikeTimestamps, selectedOnsetTimes, timeRange_baseline)

spikesEachTrial_baseline=squeeze(diff(indexLimitsEachTrial, axis=0))/diff(timeRange_baseline)


###Respones spikes
#Generating a bunch of start and stop timeranges
starts = arange(-0.5, 1, 0.1)
stops = arange(-0.4, 1.1, 0.1)


auroc_list=[]
for i in range(len(starts)):
    timeRange = vstack((starts, stops))[:,i]

    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimestamps, selectedOnsetTimes, timeRange)

    spikesEachTrial=squeeze(diff(indexLimitsEachTrial, axis=0))/diff(timeRange)

    baselineAboveCriterion=[]
    responseAboveCriterion=[]
    maxSpikes = max(max(spikesEachTrial_baseline), max(spikesEachTrial))
    for i in linspace(0, maxSpikes, 20):
        baselineAboveCriterion.append((spikesEachTrial_baseline>=i).sum()/float(len(spikesEachTrial_baseline)))
        responseAboveCriterion.append((spikesEachTrial>=i).sum()/float(len(spikesEachTrial)))

    auroc=trapz(responseAboveCriterion[::-1], x=baselineAboveCriterion[::-1])
    auroc_list.append(auroc)


