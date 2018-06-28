# This README documents the 'Work-flow' to go from raw data to a full database for the reward change study.

* All scripts in this section live in 'jaratest/common/2018rc/analysis_reward_change/'

## Cluster ephys recording (run script:reward_change_generate_cell_database.py, with CASE=1)
##* Calculate spike shape quality, add column 'spikeShapeQuality' in database 
##* Calculate percent isi violation , add column 'isiViolations' in database
## Check if cell is recorded from a session that met the behavior criteria (run script: reward_change_generate_cell_database.py, with CASE=2), column 'metBehavCriteria' in database
## Check if cell depth falls inside the range for the targeted brain region based on histology (run script: reward_change_generate_cell_database.py, with CASE=2), column 'inTargetArea' in database
## Check firing consistency for the 2afc session (run script: reward_change_generate_cell_database.py, with CASE=2), column 'consistentFiring' in database.
## '''Based on all the measurements above, save out a sub database with only the good quality cells''' for subsequent analysis. Naming convention is 'ANIMALNAME_database.h5'.
#* In code this looks like: 
#* ISIcutoff = 0.02
#* qualityThreshold = 3
#* goodQualCells = fullDb.query('isiViolations<{} and spikeShapeQuality>{} and inTargetArea==True and metBehavCriteria==True and consistentFiring==True'.format(ISIcutoff, qualityThreshold))
## Calculate and save event-aligned spike times for all trials of each cell in database. Script: generate_evlock_spktimes_celldb.py
#* Naming convention is (full path): 'home/languo/data/ephys/evlock_spktimes/{subject}_{date}_{depth}_T{tetrode}_c{cluster}_{alignment}.npz'. 
#* Each file contains these keys: spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial, timeRange, alignment.
## Evaluate sound responsiveness: using tuning curve and 2afc session, calculate Z score (0-100ms window after sound onset), (run script:reward_change_generate_cell_database.py, with CASE=3), generate columns 'tuningFreqs', 'tuningZscore','tuningPval','tuningRespIndex','tuningResp' for tuning curve session and 'behavFreqs','behavZscore','behavPval','behavRespIndex','behavResp' for 2afc session in database.
## Check whether cell is duplicated within('self') or across('cross') session, only use the duplicate with highest sound Z score in 2afc for subsequent analysis (run script:reward_change_generate_cell_database.py, with CASE=4). Generate columns 'duplicateSelf', 'duplicateCross','duplicateSelfDiscard','duplicateCrossDiscard', and 'keepAfterDupTest' in database.
## Evaluate movement direction selectivity (run script:reward_change_generate_cell_database.py, with CASE=5), generate columns with names like 'movementModI_TIMEWINDOW' and 'movementModS_TIMEWINDOW' for movement selectivity index and p value, respectively.
## Evaluate reward modulation in different time windows with different alignments (sound, center-out, side-in), do this separately for each of the frequencies presented in the task (usually one low freq and one high freq). Generate column with names like 'modInd_FREQ_ALIGNMENT_WINDOW' and 'modSig_FREQ_ALIGNMENT_WINDOW', for modulation index and p value respectively in the database.
## Check reward modulation direction in different time windows with different alignments, do this separately for each of the frequencies presented in the task. Generate columns with names like 'modDir_FREQ_ALIGNMENT_WINDOW' in the database.
