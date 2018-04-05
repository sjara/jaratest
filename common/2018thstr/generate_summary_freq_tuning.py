import os
import numpy as np
from numpy import inf
from scipy import optimize
from scipy import stats
from scipy import signal
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
import figparams
import pandas as pd

FIGNAME = 'figure_frequency_tuning'

def gaussian(x, a, x0, sigma, y0):
    return a*np.exp(-(x-x0)**2/(2*sigma**2)) + y0

def inverse_gaussian(y, a, x0, sigma, y0):
    #Inverse function
    #sqrt(-ln((y-y0)/a)*2*sigma**2) + x0
    sqrtInner = -1*np.log((y-y0)/a)*2*sigma**2
    if sqrtInner<0: #No solutions
        return None
    else:
        lower = x0 - np.sqrt(sqrtInner)
        upper = x0 + np.sqrt(sqrtInner)
        return [lower, upper]

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

def find_cf_inds(fra, resp, threshold=0.85):
    '''
    fra (np.array): boolean array of shape (nInten, nFreq). Higher index = higher intensity
    resp (np.array): response spike number array of shape (nInten, nFreq). Higher index = higher intensity
    threshold (float): At least this proportion of the intensities above must have a response for the freq to be cf
    '''
    results = []
    for indRow, row in enumerate(fra):
        for indCol, column in enumerate(row):
            if column: #Or we do a comparison here
                colAbove = fra[indRow:, indCol]
                if np.mean(colAbove)>0.85:
                # if np.all(colAbove):
                    results.append((indRow, indCol))
    resultIntenInds = [a for a, b in results]
    try:
        minResultIntenInd = min(resultIntenInds)
    except ValueError:
        return (None, None)
    else:
        resultsAtMinInten = [(a, b) for a, b in results if a==minResultIntenInd]
        resultSpikeCounts = [resp[a, b] for a, b in resultsAtMinInten]
        resultWithMaxFiring = resultsAtMinInten[resultSpikeCounts.index(max(resultSpikeCounts))]
        return resultWithMaxFiring


#Example cells we want to show tuning curves for
#AC
examples = {}
examples.update({'AC1' : 'pinp016_2017-03-09_1904_6_6'})
examples.update({'AC2' : 'pinp017_2017-03-22_1143_6_5'})

#Thalamus
examples.update({'Thal1' : 'pinp015_2017-02-15_3110_7_3'})
examples.update({'Thal2' : 'pinp016_2017-03-16_3800_3_6'})

#Striatum
examples.update({'Str1' : 'pinp020_2017-05-10_2682_7_3'})
examples.update({'Str2' : 'pinp025_2017-09-01_2111_4_3'})

exampleList = [val for key, val in examples.iteritems()]
exampleKeys = [key for key, val in examples.iteritems()]
exampleSpikeData = {}

#THE METHOD
# Calculate response range spikes for each combo
# Calculate baseline rate
# Calculate intensity threshold for cell by using response threshold
# Fit gaussian to spike data 10db above intensity threshold
# Determine upper and lower bounds of tc

# dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
db = pd.read_hdf(dbPath, key='dataframe')

soundResponsive = db.query('isiViolations<0.02 and spikeShapeQuality>2 and noisePval<0.05')
dataframe = db
#Only process the examples
# dataframe = db.query('cellLabel in @exampleList')

#Make labels for all the cells
dataframe['cellLabel'] = dataframe.apply(lambda row:'{}_{}_{}_{}_{}'.format(row['subject'], row['date'], int(row['depth']), int(row['tetrode']), int(row['cluster'])), axis=1)

# exampleDBinds = []
# for exName, exInfo in examples.iteritems():
#     exCell = find_cell(dataframe, exInfo)
#     print exCell

#Init arrays to hold the vals we will calculate here
cfs = np.full(len(dataframe), np.nan)
thresholds = np.full(len(dataframe), np.nan)
lowerFreqs = np.full(len(dataframe), np.nan)
upperFreqs = np.full(len(dataframe), np.nan)
rsquaredFit = np.full(len(dataframe), np.nan)

#Init lists to hold indices of the cells that fail this analysis in one way or another
noTCinds = [] #Cells that do not have a TC or the TC session does not have any spikes
runtimeErrorInds = [] # Cells where the gaussian fit causes a runtime error
noFreqAboveThreshInds = [] #Cells where no combination causes a response above the response threshold
threshButNo10Above = [] #Cells where we were not able to capture 10dB above threshold because the threshold was too high
no10dbAboveInds = []
sparklyCells = []

#We want to iterate through each row in the dataframe. indRow is the dataframe index column, not a climbing iteration index
for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):
    failed=False
    cell = ephyscore.Cell(dbRow)
    try:
        ephysData, bdata = cell.load('tc')
    except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
        failed=True
        print "No tc for cell {}".format(indRow)
        noTCinds.append(indRow)
        #NOTE: If the cell has no TC data we actually don't need to do anything
        #because the arrays are filled with NaN by default
        continue #Move on to the next cell

    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimes = ephysData['spikeTimes']

    # HARDCODED baseline and response ranges here
    baseRange = [-0.1, 0]
    responseRange = [0, 0.1]
    alignmentRange = [baseRange[0], responseRange[1]]

    freqEachTrial = bdata['currentFreq']
    possibleFreq = np.unique(freqEachTrial)
    intensityEachTrial = bdata['currentIntensity']
    possibleIntensity = np.unique(intensityEachTrial)

    #Init list to hold the optimized parameters for the gaussian for each intensity
    popts = []
    Rsquareds = []

    #Init arrays to hold the baseline and response spike counts per condition
    allIntenBase = np.array([])
    allIntenResp = np.empty((len(possibleIntensity), len(possibleFreq)))
    allIntenRespMedian = np.empty((len(possibleIntensity), len(possibleFreq)))

    for indinten, inten in enumerate(possibleIntensity):
        spks = np.array([])
        freqs = np.array([])
        base = np.array([])
        for indfreq, freq in enumerate(possibleFreq):
            selectinds = np.flatnonzero((freqEachTrial==freq)&(intensityEachTrial==inten))
            selectedOnsetTimes = eventOnsetTimes[selectinds]
            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
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
            allIntenBase = np.concatenate([allIntenBase, nspkBase.ravel()])
            allIntenResp[indinten, indfreq] = np.mean(nspkResp)
            allIntenRespMedian[indinten, indfreq] = np.median(nspkResp)

        try:
            popt, pcov = optimize.curve_fit(gaussian, #Fit the curve for this intensity
                                            np.log2(freqs),
                                            spks,
                                            p0=[1, np.log2(possibleFreq[7]), 1, allIntenBase.mean()],
                                            bounds=([0, np.log2(possibleFreq[0]), 0, 0],
                                                    [inf, np.log2(possibleFreq[-1]), inf, inf]))
            popts.append(popt) #Save the curve paramaters

            ## Calculate the R**2 value for the fit
            fittedSpks = gaussian(np.log2(freqs), *popt)
            residuals = spks - fittedSpks
            SSresidual = np.sum(residuals**2)
            SStotal = np.sum((spks-np.mean(spks))**2)
            Rsquared = 1-(SSresidual/SStotal)
            Rsquareds.append(Rsquared)

        except RuntimeError:
            failed=True
            print "RUNTIME ERROR, Cell {}".format(indIter)
            runtimeErrorInds.append(indIter)
            thresholds[indIter] = None
            cfs[indIter] = None
            lowerFreqs[indIter] = None
            upperFreqs[indIter] = None
            popts.append([np.nan, np.nan, np.nan, np.nan])
            Rsquareds.append(np.nan)
            continue

    ### ----- Save the example cells out to an NPZ ---- ###
    if dbRow['cellLabel'] in exampleList:
        exampleInd = exampleList.index(dbRow['cellLabel'])
        exampleSpikeData.update({exampleKeys[exampleInd]:allIntenResp})


    # TODO: Remove sparkly cells NOTE: Not doing this for now, losing too many cells this way...
    # if allIntenResp.max()<0.2:
    #     thresholds[indIter] = None
    #     cfs[indIter] = None
    #     lowerFreqs[indIter] = None
    #     upperFreqs[indIter] = None
    #     sparklyCells.append(indRow)
    #     continue
    respMeanLowestInten = allIntenResp[0:2, :].mean()
    # respMax = allIntenResp.max()
    respMax = np.percentile(allIntenResp, 90)
    respRatio = respMax/respMeanLowestInten

    #TODO: Choose which FRA to use
    thresholdFRA = 0.2
    thresholdResponse = allIntenBase.mean() + thresholdFRA*(allIntenResp.max()-allIntenBase.mean())
    # threshMedian = allIntenBase.mean() + 0.2*(allIntenRespMedian.max()-allIntenBase.mean())
    fra = allIntenResp > thresholdResponse
    # fraMedian = allIntenRespMedian > threshMedian

    #TODO: Determine threshold intensity of cell from the FRA
    # indThreshInt = None
    # for indInten, inten in enumerate(possibleIntensity):
    #     boolThisInten = fra[indInten, :]
    #     if any(boolThisInten):
    #         indThreshInt = indInten
    #         break

    indThreshInt, indFreqCF = find_cf_inds(fra, allIntenResp)

    if indThreshInt is None: #None of the intensities had anything
        #TODO: Do something better than just skip?
        thresholds[indIter] = None
        cfs[indIter] = None
        lowerFreqs[indIter] = None
        upperFreqs[indIter] = None
        noFreqAboveThreshInds.append(indRow)
        continue

    threshold = possibleIntensity[indThreshInt]
    poptThreshold = popts[indThreshInt]
    #The CF is the mean of the gaussian for the threshold intensity

    # cf = 2**poptThreshold[1] #Use the x0 param
    cf = possibleFreq[indFreqCF]

    ind10Above = indThreshInt + int(10/np.diff(possibleIntensity)[0]) #How many inds to go above the threshold intensity ind
    try:
        Rsquared10Above = Rsquareds[ind10Above]
        popt10AboveThreshold = popts[ind10Above]
        #TODO: Need to do something if we can't get 10dB above threshold
    except IndexError:
        print "Failure indexerror didn't get 10 above"
        print threshold
        failed=True
        #We were not able to catch 10db above threshold. In this case, we can still get cf and thresh, but not uF/lF
        no10dbAboveInds.append(indIter)
        upperFreq = None
        lowerFreq = None
        Rsquared10Above = np.nan
    else:
        result = inverse_gaussian(thresholdResponse, *popt10AboveThreshold)
        if result is not None:
            lower, upper = result
            lowerFreq = 2**lower
            upperFreq = 2**upper
        else:
            #If this returns none, then the threshold passed but 10dB above did not pass.
            threshButNo10Above.append(indIter)
            lowerFreq=None
            upperFreq=None
    #Things to save
    rsquaredFit[indIter] = Rsquared10Above
    thresholds[indIter] = threshold
    cfs[indIter] = cf
    lowerFreqs[indIter] = lowerFreq
    upperFreqs[indIter] = upperFreq

dataframe['threshold'] = thresholds
dataframe['cf'] = cfs
dataframe['lowerFreq'] = lowerFreqs
dataframe['upperFreq'] = upperFreqs
dataframe['rsquaredFit'] = rsquaredFit

dataframe['BW10'] = (dataframe['upperFreq']-dataframe['lowerFreq'])/dataframe['cf']

dataframe.to_hdf(dbPath, key='dataframe')

# exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')
# np.savez(exampleDataPath, **exampleSpikeData)

# thalDB = dataframe.groupby('brainArea').get_group('rightThal')
# acDB = dataframe.groupby('brainArea').get_group('rightAC')
# astrDB = dataframe.groupby('brainArea').get_group('rightAstr')

# plt.subplot(311)
# plt.hist(thalDB['BW10'][pd.notnull(thalDB['BW10'])])
# plt.subplot(312)
# plt.hist(acDB['BW10'][pd.notnull(acDB['BW10'])])
# plt.subplot(313)
# plt.hist(astrDB['BW10'][pd.notnull(astrDB['BW10'])])


