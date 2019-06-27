'''
Generate[1] and save[2] database with calculated stats and parameters that will be used in /
analysis
'''
import os
import pandas as pd
import numpy as np
import time
import studyparams
from scipy import stats
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
import database_generation_funcs as funcs
reload(funcs)
reload(studyparams)

SAVE = 0

def calculate_base_stats(db, filename = ''):
    '''
    Calculate parameters to be used to filter cells in calculate_indices
    '''

    sessionMulti = ['tuningCurve','tuningCurve(tc)'] #sessions with multivariate stimulus 'shortTuningCurve','am'
    sessionSingle = ['noiseburst','laserpulse']#sessions with single variable stimulus
    #FILTERING DATAFRAME
    firstCells = db.query(studyparams.FIRST_FLTRD_CELLS) #isiViolations<0.02 and spikeShapeQuality>2

    for indIter, (indRow, dbRow) in enumerate(firstCells.iterrows()):

        dbRow = firstCells.loc[indRow]
        sessions = dbRow['sessionType']
        oneCell = ephyscore.Cell(dbRow, useModifiedClusters=False)

        print "Now processing ", dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster'],indRow
        print "Sessions tested in this cell are(is) ",sessions

        for session in sessions:
            ephysData, bdata = oneCell.load(session)

            #SOUND RESPONSES AND LASER RESPONSES
            if session in sessionSingle: # single stimulus
                baseRange = [-0.1,0]# if session != 'laserpulse' else [-0.05,-0.04]
                nspkBase, nspkResp = funcs.calculate_firing_rate(ephysData, baseRange,session)
                respSpikeMean = nspkResp.ravel().mean()
                try:
                    zStats, pVals = stats.mannwhitneyu(nspkResp, nspkBase)
                except ValueError: #All numbers identical will cause mann-whitney to fail
                    zStats, pVals = [0, 1]

                firstCells.loc[indRow,'{}_pVal'.format(session)] = pVals # changed from at to loc via recommendation from pandas
                firstCells.loc[indRow,'{}_FR'.format(session)] = respSpikeMean#mean firing rate

            #Frequency tuning responses and AM
            elif session in sessionMulti: # multivariate stimulus
                baseRange = [-0.1,0] if session != 'am' else [-0.5, -0.1]

                currentFreq = bdata['currentFreq']
                currentIntensity = bdata['currentIntensity']
                trialsEachType = behavioranalysis.find_trials_each_type(currentFreq,np.unique(currentFreq))
                uniqFreq = np.unique(currentFreq)
                uniqueIntensity = np.unique(currentIntensity)

                allIntenBase = np.array([])
                respSpikeMean = np.empty((len(uniqueIntensity),len(uniqFreq)))#same as allIntenResp
                allIntenRespMedian = np.empty((len(uniqueIntensity),len(uniqFreq)))
                Rsquareds = np.empty((len(uniqueIntensity),len(uniqFreq)))

                for indInten, intensity in enumerate(uniqueIntensity):
                    spks = np.array([])
                    freqs = np.array([])
                    popts = []
                    pcovs = []
                    ind10AboveButNone = []
                    for indFreq, freq in enumerate(uniqFreq):
                        selectinds = np.flatnonzero((currentFreq==freq)&(currentIntensity==intensity)).tolist()

                        nspkBase, nspkResp = funcs.calculate_firing_rate(ephysData, baseRange, session, selectinds = selectinds)

                        spks = np.concatenate([spks,nspkResp.ravel()])
                        freqs = np.concatenate([freqs,np.ones(len(nspkResp.ravel()))*freq])
                        respSpikeMean[indInten,indFreq] = np.mean(nspkResp)
                        allIntenBase = np.concatenate([allIntenBase,nspkBase.ravel()])

                        Rsquared, popt = funcs.calculate_fit(uniqFreq,allIntenBase,freqs,spks)

                        Rsquareds[indInten,indFreq] = Rsquared
                        popts.append(popt)
                     #---------------------------End of freq loop------------------------------------------
                     # The reason why we are calculating bw10 here, it is to save the calculation time
                    responseThreshold = funcs.calculate_response_threshold(0.2, allIntenBase,respSpikeMean)
                # [6] Find Frequency Response Area (FRA) unit: fra boolean set, yes or no, but it's originally a pair
                    fra = respSpikeMean > responseThreshold
                # [6.5] get the intensity threshold
                    intensityInd, freqInd = funcs.calculate_intensity_threshold_and_CF_indices(fra,respSpikeMean)
                    if intensityInd is None: #None of the intensities had anything
                        bw10 = None
                        lowerFreq = None
                        upperFreq = None
                        cf = None
                        intensityThreshold = None
                        fit_midpoint = None
                    else:
                        intensityThreshold = uniqueIntensity[intensityInd]
                        cf = uniqFreq[freqInd]
                    # [8] getting BW10 value, Bandwidth at 10dB above the neuron's sound intensity Threshold(SIT)
                        ind10Above = intensityInd + int(10/np.diff(uniqueIntensity)[0]) #How many inds to go above the threshold intensity ind
                        lowerFreq, upperFreq, Rsquared10AboveSIT = funcs.calculate_BW10_params(ind10Above, popts,Rsquareds,responseThreshold,intensityThreshold)
                        # print('lf:{},uf:{},R2:{}'.format(lowerFreq,upperFreq,Rsquared10AboveSIT))

                        if (lowerFreq is not None) and (upperFreq is not None):
                            fit_midpoint = np.sqrt(lowerFreq*upperFreq)
                            bw10 = (upperFreq - lowerFreq)/cf

                        else:
                                fit_midpoint = None
                                bw10 = None
                    #ADD PARAMS TO DATAFRAME [9] store data in DB: intensity threshold, rsquaredFit, bw10, cf, fra
                        firstCells.at[indRow, 'thresholdFRA']= intensityThreshold
                        firstCells.at[indRow,'cf'] = cf
                        firstCells.at[indRow,'lowerFreq'] = lowerFreq
                        firstCells.at[indRow,'upperFreq'] = upperFreq
                        firstCells.at[indRow,'rsquaredFit'] = Rsquared10AboveSIT
                        firstCells.at[indRow,'bw10'] = bw10
                        firstCells.at[indRow,'fit_midpoint'] = fit_midpoint

            else:
                print("session {} is ignored".format(session))#Lasertrain, shortTuningCurve and AM are ignored
    return firstCells

def calculate_indices(db, filename = ''):
    '''
    Filter cells that has a good fitting then separate D1 cells(laser responsive)\
    and non-D1 cells(non laser-responsive)
    '''
    pass
    # bestCells = db.query('rsquaredFit>{}'.format(studyparams.R2_CUTOFF))
    #
    # return bestCells

def calculate_cell_locations(db, filename = ''): # to be filled after complete collecting histology data
    pass

if __name__ == "__main__":
    # Cluster your data
    CLUSTER_DATA = 0  # We don't generally run this code. We kept this for documentation
    d1mice = studyparams.ASTR_D1_CHR2_MICE
    if CLUSTER_DATA: #SPIKE SORTING
        inforecFile = os.path.join(settings.INFOREC_PATH,'{}_inforec.py'.format(d1mice))
        clusteringObj = spikesorting.ClusterInforec(inforecFile)
        clusteringObj.process_all_experiments()
        pass

    ## Generate_cell_database_filters cells with the followings: isi < 0.05, spike quality > 2
    basicDB = celldatabase.generate_cell_database_from_subjects(d1mice)

    d1DBFilename = os.path.join(settings.FIGURES_DATA_PATH, '{}_d1mice.h5'.format(studyparams.STUDY_NAME))
    # Create and save a database, computing first the base stats and then the indices
    firstDB = calculate_base_stats(basicDB, filename = d1DBFilename)
    # bestCells = calculate_indices(firstDB, filename = d1DBFilename)

    if SAVE:
        dbpath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME,'{}.h5'.format('_'.join(d1mice)))
        firstDB.to_hdf(dbpath,key='df',mode='w')
        print "SAVED DATAFRAME to {}".format(dbpath)
