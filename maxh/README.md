# 2023acid
Effects of DOI on the sound responses of auditory cortical neurons.

# Producing databases

The file `studyparams.py` contains the list of animals used in this study as well as relevant file paths and commonly used parameters.
You need to run the database generation scripts in the order listed here, as most scripts load the previous and adds to that.

- `database_generation.py`: Uses the inforec, ephys data, and behavior data to create a database of cells. Creates `celldb_SUBJECT.h5`
- `database_cell_locations.py`: **UNFINISHED** 
- `database_generate_running_boolean.py`: Generates a 3d numpy array of running or nonrunning trials. 
    - Currently only gets trials for oddball_sequence paradigm sessions.
    - Creates either: 
        - `SUBJECT_runningBooleanArrayNon.npy` 
        - `SUBJECT_runningBooleanArrayRun.npy`
    - You will need to run it twice: once for running and once for nonrunning.
- `database_puretone_and_oddball_calcs.py`: 
    - Calculates statistics for puretone and oddball trials. Can be used for all trials, running trials, or nonrunning trials.
    - Run each animal individually, takes around ~22min. for each.
    - Selecting for running or nonrunning currently only changes oddball_sequence calculations. 
    - Creates either: 
        - `SUBJECT_puretone_and_oddball_calcs_all.h5` 
        - `SUBJECT_puretone_and_oddball_calcs_nonRunning.h5`
        - `SUBJECT_puretone_and_oddball_calcs_running.h5`
    - You will need to run it twice: once for running and once for nonrunning. (Optional third time for all trials.)
- `database_combine_subjects.py`: **UNFINISHED** Combines the databases of all subjects into one database.
    - Creates either:
        - `allMice_puretone_and_oddball_calcs_all.h5` 
        - `allMice_puretone_and_oddball_calcs_nonRunning.h5`
        - `allMice_puretone_and_oddball_calcs_running.h5`

# Database contents

- `celldb_SUBJECT.h5`: The initial database is generated in `database_generation.py` by using `celldatabase.generate_cell_database()`.
    - It contains columns according to the inforec files (``subject``, ``date``, etc)
    - And the spike sorting results (``cluster``, ``spikeShape``, etc).
- `SUBJECT_runningBooleanArray[Non/Run].npy`: Generated from `database_generate_running_boolean.py`.
    - File is a 3D numpy array with [running or nonrunning] trials generated from proc_files via jarafacemap.
        - array[0]: date (typ: string) 
        - array[1]: reagent (typ: string)
        - array[2]: HighFreq trials (type: array of bool)
        - array[3]: LowFreq trials (type: array of bool)
        - array[4]: FM_Down trials (type: array of bool)
        - array[5]: FM_Up trials (type: array of bool)

- `SUBJECT_puretone_and_oddball_calcs_[all/nonRunning/running].h5`: Generated from `database_puretone_and_oddball_calcs.py`. 
    - Each column has three versions for Saline/DOI/Pre:
    - **Pure tones / frequency tuning**
        - `baselineFiringRatePureTones[Saline/DOI/Pre]`: The firing rate of the average spikes during baseline [-200ms to 0ms] of stimulus.
        - `stimFiringRatePureTones[Saline/DOI/Pre]`: The average firing rate of the average firing rates of each tone during stimulus [15ms to 115ms].
        - `stimMaxAvgFiringRatePureTones[Saline/DOI/Pre]`: The highest average firing rate during stimulus [15ms to 115ms].
        - `stimBestFrequencyPureTones[Saline/DOI/Pre]`: The frequency that had the highest average firing rate.
        - `gaussianAmplitude[Saline/DOI/Pre]`: Amplitude of gaussian curve fit.
        - `gaussianMean[Saline/DOI/Pre]`: Mean of gaussian curve fit.
        - `gaussianSigma[Saline/DOI/Pre]`: Sigma of gaussian curve fit.
        - `rSquaredColumn[Saline/DOI/Pre]`: rSquared of gaussian fit.
    - **Oddball sweeps / oddball sequence:**
        - `upOddSpikesAvgFiringRate[Saline/DOI/Pre]`: The firing rate of the average spike count during FM upsweep oddball stimulus [15ms to 115ms].
        - `downStandardSpikesAvgFiringRate[Saline/DOI/Pre]`: The firing rate of the average spike count during FM downsweep standard stimulus [15ms to 115ms].
        - `downOddSpikesAvgFiringRate[Saline/DOI/Pre]`: The firing rate of the average spike count during FM downsweep oddball stimulus [15ms to 115ms].
        - `upStandardSpikesAvgFiringRate[Saline/DOI/Pre]`: The firing rate of the average spike count during FM upsweep standard stimulus [15ms to 115ms].
        - `baselineUpStandardFiringRate[Saline/DOI/Pre]`: The firing rate of the average baseline spike count before FM upsweep standard stimulus [-200ms to 0ms].
        - `baselineDownStandardFiringRate[Saline/DOI/Pre]`: The firing rate of the average baseline spike count before FM downsweep standard stimulus [-200ms to 0ms].
        - `baselineUpOddFiringRate[Saline/DOI/Pre]`: The firing rate of the average baseline spike count before FM upsweep oddball stimulus [-200ms to 0ms].
        - `baselineDownOddFiringRate[Saline/DOI/Pre]`: The firing rate of the average baseline spike count before FM downsweep oddball stimulus [-200ms to 0ms].
        - `upOddballIndex[Saline/DOI/Pre]`: The oddball enhancement index of FM upsweep.
        - `downOddballIndex[Saline/DOI/Pre]`: The oddball enhancement index of FM downsweep.

    - **Oddball Chords:**
        - `highOddSpikesAvgFiringRate[Saline/DOI/Pre]`: The firing rate of the average spike count during HighFreq chord oddball stimulus [15ms to 65ms].
        - `lowStandardSpikesAvgFiringRate[Saline/DOI/Pre]`: The firing rate of the average spike count during LowFreq chord standard stimulus [15ms to 65ms].
        - `lowOddSpikesAvgFiringRate[Saline/DOI/Pre]`: The firing rate of the average spike count during LowFreq chord oddball stimulus [15ms to 65ms].
        - `highStandardSpikesAvgFiringRate[Saline/DOI/Pre]`: The firing rate of the average spike count during HighFreq chord standard stimulus [15ms to 65ms].
        - `baselineHighStandardFiringRate[Saline/DOI/Pre]`: The firing rate of the average baseline spike count before HighFreq chord standard stimulus [-200ms to 0ms].
        - `baselineLowStandardFiringRate[Saline/DOI/Pre]`: The firing rate of the average baseline spike count before LowFreq chord standard stimulus [-200ms to 0ms].
        - `baselineHighOddFiringRate[Saline/DOI/Pre]`: The firing rate of the average baseline spike count before HighFreq chord oddball stimulus [-200ms to 0ms].
        - `baselineLowOddFiringRate[Saline/DOI/Pre]`: The firing rate of the average baseline spike count before LowFreq chord oddball stimulus [-200ms to 0ms].
        - `highOddballIndex[Saline/DOI/Pre]`: The oddball enhancement index of HighFreq chord.
        - `lowOddballIndex[Saline/DOI/Pre]`: The oddball enhancement index of LowFreq chord.

# Oddball Enhancement Index

The oddball enhancement index calculates the change in stimulus evoked neuronal firing rate when a stimulus was an oddball versus when the same stimulus was a standard.
- The index is on a scale of (-1 to +1).
    - Closer to -1 means the firing rate evoked from the stimulus as standard was higher.
    - Closer to +1 means the firing rate evoked from the stimulus as oddball was higher.


**Calculation for oddball enhancement index:**

$$\frac{(OddSpikesAvgFiringRate - StandardSpikesAvgFiringRate)}{(OddSpikesAvgFiringRate + StandardSpikesAvgFiringRate)}$$

# Study functions
- `oddball_analysis_functions.py`: This script has functions that were created for this study.
    - **Most relevant functions in script**:
        - `load_data(cell, session, timeRange)`: Loads ephys and behav from session of cell. Locks spikes to trials, sorts and seperates trials by each condition.
            - Returns: spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial, trialsLowFreq, trialsHighFreq.
        - `trials_before_oddball(oddballTrials)`: Creats a boolean array of the trials directly before oddball stimulus as True.
            - Returns: trialsBeforeOddball
        - `find_sync_light_onsets(sync_light)`: Find the onsents in sync light array. Can also detect pre/post manual lights and fill in missing sync lights.
            - This is an edited version from `facemapanalysis.py` that checks for repeated onsets before checking for pre/post.
            - Returns: fixed_sync_light_onset 
        - `combine_index_limits(spikeTimes1, spikeTimes2, indexLimits1, indexLimits2)`: Combines the spikeTimesFromEventOnset and indexLimitsEachTrial from two sessions.
            - Only used for making cell reports.
            - Returns: combinedSpikeTimes, combinedIndexLimits
        - `combine_trials(trials1, trials2)`: Combine two trial arrays into one 2d array. Matche
            - Only used for making cell reports.
            - Returns: combinedTrials



        

# Figures
- `figure_oddball_response_summary.py`: generates a figure showing the change in oddball enhancement effect between each injection type for each session type.
    - Parameters to change figure results:
        - `database_type`: Changes which database is loaded.
        - `cell_selection_type`: Changes the criteria for selecting cells to use.
        - `firingThreshold`: The minimum threshold of firing rate for selecting cells.
 

# Extras
- `make_acid_oddball_cell_reports.py`: generates figures for each cell that has raster and psth plots for each session type and injection.
- `make_acid_tuning_freq_raster`: generates figures for each cell that shows frequency tuning raster plots for each injection.
- `figure_freq_tuning_stim_base_max`: generates a figure showing the change between saline and doi for am_tuning pureTones. Plots change in:
    - avg firing rate during stimulus
    - avg firing rate during baseline
    - max firing rate during stimulus
- `make_acid_tuning_curve_comparison.py`: generates a figure from a selected cell that shows DOI and Saline tuningfreq rasters and an overlapped gaussian fit tuning curve plot.
- `figure_running_trial_count_comparison.py`: Shows the change in the number of trials the mouse was running for each session between injection types.
- `test_load_facemap_data.py`: loads and plots the proc file from facemap and compares it to behavior data.
- `test_sync_light_function.py`: loads and plots proc file after sync light fixes have been made.

