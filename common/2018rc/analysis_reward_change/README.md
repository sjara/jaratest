# This README documents the 'Work-flow' to go from raw data to a full database for the reward change study.

* All scripts in this section live in 'jaratest/common/2018rc/analysis_reward_change/'

1. Cluster ephys recording (run script:reward_change_generate_cell_database.py, with CASE=1) 
	* While clustering, we also calculate spike shape quality, add column 'spikeShapeQuality' in database.
	* And calculate percent isi violation , add column 'isiViolations' in database.
	* Note: the clustering would take overnight.
2. Check if cell 1) is recorded from a session that met the behavior criteria, 2) depth falls inside the range for the targeted brain region based on histology, 3) cell fires consistently for the 2afc session (run script: reward_change_generate_cell_database.py, with CASE=2)
	* This step adds columns: 'metBehavCriteria', 'inTargetArea', 'consistentFiring' in the database.
	* CASE=2 takes 40 minutes or so to process all clusters from 11 mice. 
3. **Based on all the measurements above, *save out a sub database with only the good quality cells* for subsequent analysis. Naming convention is 'ANIMALNAME_database.h5'.**	
	* In code this looks like: 
	> ISIcutoff = 0.02
	> qualityThreshold = 3
	> goodQualCells = fullDb.query('isiViolations<{} and spikeShapeQuality>{} and inTargetArea==True and metBehavCriteria==True and consistentFiring==True'.format(ISIcutoff, qualityThreshold))
4. Calculate and save event-aligned spike times for all trials of each cell in database. Script: generate_evlock_spktimes_celldb.py
	* Naming convention is (full path): 'home/languo/data/ephys/evlock_spktimes/{subject}_{date}_{depth}_T{tetrode}_c{cluster}_{alignment}.npz'. 
	* Each file contains these keys: spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial, timeRange, alignment.
5. Evaluate sound responsiveness: using tuning curve and 2afc session, calculate Z score (0-100ms window after sound onset), (run script:reward_change_generate_cell_database.py, with CASE=3).
 	* Generate columns 'tuningFreqs', 'tuningZscore','tuningPval','tuningRespIndex','tuningAveResp' for tuning curve session and 'behavFreqs','behavZscore','behavPval','behavRespIndex','behavAveResp' for 2afc session in database. 
 	* Note: This takes about 30 minutes for all good cells from 11 mice.
6. Check whether cell is duplicated within('self') or across('cross') session, only use the duplicate with highest sound Z score in 2afc for subsequent analysis (run script:reward_change_generate_cell_database.py, with CASE=4). 
	* Generate columns 'duplicateSelf', 'duplicateCross','duplicateSelfDiscard','duplicateCrossDiscard', and 'keepAfterDupTest' in database. 
	* Note: This takes about 1 hour for all good cells from 11 mice.
7. Evaluate movement direction selectivity (run script:reward_change_generate_cell_database.py, with CASE=5). 
	* Generate columns with names like 'movementModI_TIMEWINDOW' and 'movementModS_TIMEWINDOW' for movement selectivity index and p value, respectively.  
	* Note: This takes about 1.5-2 hours for all good cells from 11 mice.
8. Evaluate reward modulation in different time windows with different alignments (sound, center-out, side-in), do this separately for each of the frequencies presented in the task (usually one low freq and one high freq). Run script:reward_change_generate_cell_database.py, with CASE=6.
	* Generate column with names like 'modInd_FREQ_ALIGNMENT_WINDOW', 'modSig_FREQ_ALIGNMENT_WINDOW', and 'modDir_FREQ_ALIGNMENT_WINDOW', for modulation index, p value, and modulation direction respectively in the database.
	* Note: This takes a few hours for all good cells from 11 mice.
9. Merge databases from all mice to form a master database for reward change study. Run script:reward_change_generate_cell_database.py, with CASE=7.