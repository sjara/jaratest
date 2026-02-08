import numpy as np
from sklearn.svm import SVC,LinearSVC
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.model_selection import train_test_split
import os
from jaratoolbox import settings
from jaratoolbox import celldatabase,extraplots,ephyscore,behavioranalysis,spikesanalysis
import numpy as np
import studyparams
import studyutils
from importlib import reload
import warnings
reload(studyparams)
reload(spikesanalysis)
reload(ephyscore)


def extract_temporal_features(timeseries):
    """Extracts sophisticated features from a single PSTH trial."""
    return np.array([
        np.mean(timeseries),          # Overall rate
        np.std(timeseries),           # Variability/Burstiness
        np.max(timeseries),           # Peak response
        np.argmax(timeseries),        # Latency to peak
        np.sum(np.diff(timeseries)**2) # 'Energy' or volatility
    ])

def decode_tone_from_spikes(features, targets, tones, reg = 1.0, seeds = np.arange(100), n_splits=5):
    """
    Collapses time bins to focus on mean firing rate per neuron.
    This reduces features from ~125,000 to 2,491.
    """
    n_neurons, _, n_bins = features.shape
    unique_tones = np.sort(np.unique(targets))
    
    # 1. Align and Truncate (as before)
    min_repeats_per_tone = {tone: min([np.sum(targets[n] == tone) for n in range(n_neurons)]) 
                            for tone in unique_tones}
    total_aligned_trials = sum(min_repeats_per_tone.values())
    
    n_features = 5
    # 2. Build aligned matrix (Averaging over the bin axis immediately)
    X_aligned = np.zeros((total_aligned_trials, n_neurons,n_features))
    y_aligned = []

    current_row = 0
    for tone in unique_tones:
        n_reps = min_repeats_per_tone[tone]
        for r in range(n_reps):
            y_aligned.append(tone)
            for n in range(n_neurons):
                neuron_tone_indices = np.where(targets[n] == tone)[0]
                source_idx = neuron_tone_indices[r]
                # MEAN over time bins to get a single firing rate value
                X_aligned[current_row, n,:] = extract_temporal_features(features[n, source_idx, :])
            current_row += 1

    X = X_aligned
    y = np.array(y_aligned)
    
    # 3. Pipeline with Ridge Regularization (L2)
    pipeline = Pipeline([
        # ('scaler', StandardScaler()),
        # ('svm', LinearSVC(penalty='l1',C=reg, dual=False, max_iter=10000))
        ('pca', PCA(n_components=50)),
        # ('svm', SVC(kernel='rbf', C=reg, gamma='scale'))
        ('logit', LogisticRegression(penalty = 'l2',
                                     multi_class='multinomial', 
                                    solver='saga', C = reg,
                                    max_iter=2000))
        # ('rf',  RandomForestClassifier(n_estimators=500, 
        #                                 max_depth=20, 
        #                                 max_features='log2', 
        #                                 n_jobs=-1, 
        #                                 random_state=42,
        #                                 bootstrap=True
        #                                 ))
            ])
    
    predTonesAll,trueTonesAll,errorsAll,confusionAll = [],[],[],[]

    y_preds,y_tests,y_trains,X_trains = [],[],[],[]

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    # for fold, (train_idx, test_idx) in enumerate(skf.split(X, y)):
    for seed in seeds:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, stratify=y,shuffle=True, random_state=seed
        )

        # X_train, X_test = X[train_idx], X[test_idx]
        # y_train, y_test = y[train_idx], y[test_idx]

        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)

        y_preds.append(y_pred)
        y_tests.append(y_tests)
        y_trains.append(y_train)
        X_trains.append(X_train)

        predTones = np.array([possibleTone[int(y)] for y in y_pred])
        trueTones = np.array([possibleTone[int(y)] for y in y_test])
        errors = np.abs(np.log2(predTones/trueTones))

        predTonesAll.append(predTones)
        trueTonesAll.append(trueTones)
        errorsAll.extend(errors)
        confusionAll.append(confusion_matrix(y_test,y_pred,normalize='all'))

    print(f"Mean Error: {np.mean(errorsAll):0.2f} octaves")

    outputs = {'pipeline':pipeline,
               'y_test':y_tests,
               'y_train':y_trains,
               'X_train':X_trains,
               'y_pred':y_preds,
               'predTones':predTonesAll,
               'trueTones':trueTonesAll,
               'octaveError':errorsAll,
               'confusion':confusionAll}

    return outputs



studyName = '2025hemisym'

implants = ['LR','RL']
outputsEachImplant = {}
eventKey = 'Evoked'

for implant in implants:
    subjects = studyparams.SUBJECTS_EACH_IMPLANT[implant]
    sites = studyparams.SITES_EACH_IMPLANT[implant]
    sessionDatesEachSite = studyparams.SESSION_DATES_EACH_SITE
    subjectsEachSite = studyparams.SUBJECT_EACH_SITE
    sessionType = 'optoTuningAMtone'

    sessionDatesAll = [sessionDatesEachSite[site] for site in sites]

    dbPath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
    dbFilename = os.path.join(dbPath,f'celldb_{implant}_{sessionType}_freqtuning.h5')
    # celldb = celldatabase.generate_cell_database_from_subjects(subjects)
    celldbBase = celldatabase.load_hdf(dbFilename)

    responsive = studyutils.find_tone_responsive_cells(celldbBase, eventKey, frThreshold=studyparams.FR_THRESHOLD,allreagents=True,sessionType=sessionType)

    steadyParams = ['BaselineFiringRate'] 
    steady = studyutils.find_steady_cells(celldbBase, steadyParams, 1.3,sessionType=sessionType)
    selective = studyutils.find_freq_selective(celldbBase, minR2=studyparams.MIN_PVAL,sessionType=sessionType)
    selectedCells = responsive# & steady & selective

    celldb = celldbBase[selectedCells]



    timeRange = studyparams.TIME_RANGES_AM[eventKey]
    binSize = 0.05
    binEdges = np.arange(timeRange[0], timeRange[1], binSize)
    nBins = len(binEdges)-1
    nTones = 16
    nTrialsToUse = 290
    mods = ['fast','slow','fastOn','slowOn']

    PSTHsEachMod = {mod: np.empty((0,nTones,nBins)) for mod in mods}

    spikeCountsEachMod = {mod: np.empty((0,nTrialsToUse,nBins)) for mod in mods}

    labelsEachMod = {mod: np.empty((0,nTrialsToUse)) for mod in mods}

    for inds,site in enumerate(sites):
        sessionDatesThisSite = sessionDatesEachSite[site]
        subjectThisSite = subjectsEachSite[site]

        for sessionDate in sessionDatesThisSite:
            celldbSubset = celldb[( celldb.subject == subjectThisSite) \
                                    & (celldb.date == sessionDate )]

            nCells = len(celldbSubset)
            print(nCells,sessionDate,subjectThisSite)

            if not nCells: 
                continue
            ensemble = ephyscore.CellEnsemble(celldbSubset)
            
            ephysData, bdata = ensemble.load(sessionType)


            toneEachTrial = bdata['currentFreq']
            possibleTone = np.unique(toneEachTrial)
            modEachTrial = bdata['currentMod']
            possibleMod = np.unique(modEachTrial)
            laserEachTrial = bdata['laserTrial']
            possibleLaser = np.unique(laserEachTrial)
            currentStims = [toneEachTrial, modEachTrial, laserEachTrial]
            possibleStims = [possibleTone,possibleMod,possibleLaser]

            nTrials = toneEachTrial.shape[0]
            nTones = len(possibleTone)

            eventOnsetTimes = ephysData['events']['stimOn'][:nTrials]# Ignore trials not in bdata 
            spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = \
                                ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)

            
            
            spikeCount = ensemble.spiketimes_to_spikecounts(binEdges) # The shape is (nCells, nTrials, nBins)
            
            trialsAllCombs = behavioranalysis.find_trials_each_combination_n(currentStims,possibleStims)
            
            trialsEachMod = {'fast' : trialsAllCombs[:,:,1,0],
                            'slow' : trialsAllCombs[:,:,0,0],
                            'fastOn' : trialsAllCombs[:,:,1,1],
                            'slowOn' : trialsAllCombs[:,:,0,1]}
            
            for indm,mod in enumerate(trialsEachMod):
                trialsEachCond = trialsEachMod[mod]


                # currentPSTH = np.empty((nCells,nTones,nBins))
                # for indcond,trialsThisCond in enumerate(trialsEachCond.T):
                #     for cell in range(nCells):
                #         currentPSTH[cell,indcond,:] = spikeCount[cell,trialsThisCond,:].mean(axis=0)

                # PSTHsEachMod[mod] = np.vstack([PSTHsEachMod[mod],currentPSTH])

                
                spikeCountsEachMod[mod] = np.vstack([spikeCountsEachMod[mod],spikeCount[:,:nTrialsToUse,:]])
                labelsEachMod[mod] = np.vstack([labelsEachMod[mod],[np.nonzero(trialsEachCond)[1][:nTrialsToUse]]*nCells])


    outputs={}
    for mod in sorted(mods):
        print(mod)
        outputs[mod] = decode_tone_from_spikes(spikeCountsEachMod[mod],labelsEachMod[mod],possibleTone,reg=0.01)

    outputsEachImplant[implant] = outputs
