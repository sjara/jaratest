# 2019astrpi
This project looks into characterizing MSN's on the direct and indirect striatal
pathway

# Producing a database
The file `studyparams.py` contains a list of animals as well as statistical 
parameters for the database calculations

## direct_and_indirect_cells2.h5

### database_generation.py
This script will generate the database with all subjects defined
as d1pi mice in studyparams.py. This script can create databases for individual
mice or concatenate previously made databases together. Output is an h5 file 
containing all the below information in `Database contents` Check the docstring
for info on how to run the script. 

This script uses following module:
### database_generation_funcs.py
Contains functions called during database generation.

# Database contents
## Generic database
This is the database initially produced by 
celldatabase.generate_cell_database_from_subjects(). The columns produced by 
this database can be found in the documentation for celldatabase.

## Base stats
These are the columns added to the generic database after calculation of base stats. 
They are grouped by questions they were used to answer:

### Are cells identifiable *in vivo* and do they respond differently to basic sounds? (Figure 1)
* *laserpulse_pVal*: The p-value for comparing the baseline and response firing
rates of the laserpulse paradigm using a Mann-Whitney U test.

* *laserpulse_ZStat*: The corresponding U-statistic for the above p-value

* *laserpulse_SpikeCountChange*: The change in spike count for the laserpulse as calculated by
`response - baseline`

* *laserpulse_baselineSpikeCount*: The baseline laserpulse mean spike count. Baseline period
was [-100 ms, 0 ms]

* *laserpulse_responseSpikeCount*: The response laserpulse mean spike count. Response period
was [0 ms, 100 ms]

* *noiseburst_pVal*: The p-value for comparing the baseline and response firing
rates of the noiseburst paradigm using a Mann-Whitney U test.

* *noiseburst_ZStat*: The corresponding U-statistic for the above p-value

* *noiseburst_baselineSpikeCount*: The baseline noiseburst mean spike count. Baseline period 
was [-100 ms, 0 ms] 

* *noiseburst_responseSpikeCount*: The response noiseburst mean spike count. Response period
was [0 ms, 100 ms] 

* *tuningTest_pVal*: The p-value found from comparing the baseline firing rate of
all frequencies at the maximum intensity to the response using a Mann-Whitney U
test. Baseline period was [-100 ms, 0 ms] and repsonse period was [0 ms, 100 ms]

* *tuningTest_ZStat*: The corresponding U-statistic for the above p-value

* *ttR2Fit*: The R^2 value of the Gaussian fit to the tuning test paradigm.

### Is there a difference in the basic responses of the cells to different sounds? (Figure 2)
* *AMBaseFROnset*: The corresponding baseline firing rate for the best onset
response firing rate for a cell. Baseline period was [-100 ms, 0 ms]

* *AMRespFROnset*: The highest onset response firing rate of all the rates 
presented. Onset period was [0 ms, 100 ms]

* *AMBestRateOnset*: The amplitude modulation rate that yielded the best onset
response

* *AMBaseFRSustained*: The corresponding baseline firing rate for the best 
sustained response. Baseline period was [-500 ms, -100 ms]

* *AMRespFRSustained*: The highest sustained firing rate of all the rates 
presented. Sustained period was [100 ms, 500 ms]

* *AMBestRateSustained*: The amplitude modulation rate that produced the highest
sustained response

* *tuning_pVal*: The p-value from comparing the baseline firing rate vs response 
firing rate of all frequencies at the highest intensity for the tuningCurve
paradigm with a Mann-Whitney U test

* *tuning_ZStat*: Corresponding U-statistic for the p-value

* *tuningBaseFRBestFreqMaxInt*: The corresponding baseline firing rate for the
frequency that had the largest response firing rate. Baseline period was
[-100 ms, 0 ms]

* *tuningRespFRBestFreqMaxInt*: The firing rate for the best frequency at maximum
intensity. Response period was [0 ms, 100 ms]

* *tuningBestFreqMaxInt*: The frequency that had the highest response firing rate
at the maximum intensity presented

### Do the cells prefer different properties of pure tone sounds? (Figure 3)
* *upperFreq*: The highest frequency with a response 10 dB SPL above the sound 
intensity threshold. Calculated by database_generation_funcs.calculate_BW10_params.

* *lowerFreq*: The lowest frequency with a response 10 dB SPL above the sound 
intensity threshold. Calculated by 
database_generation_funcs.calculate_BW10_params.

* *RsquaredFit*: The mean of all of the r<sup>2</sup> values of the 10 dB SPL above 
the sound intensity threshold. Calculated by database_generation_funcs.calculate_BW10_params.

* *cf*: The characteristic frequency is the frequency that is most sensitive to
sound.

* *bw10*: The bandwidth 10 above the sound intenisty threshold. Calculated by the 
equation: (*upperFreq* - *lowerFreq*) / *cf*

* *fitMidpoint*: The midpoint of the gaussian fit for the tuning curve calculated
 using the square root of the *upperFreq* * *lowerFreq*

* *thresholdFRA*: The characteristic intensity for peak firing rate. Found using 
the intensity index from 
database_generation_funcs.calculate_intensity_threshold_and_CF_indices and 
indexing the unique intensities (uniqueIntensity) for a session.

* *latency*: The time (in seconds) from when the stimulus is presented until the 
cell shows a response. Calculated using database_generation_funcs.calculate_latency(). 
This looks at the *cf* on the tuning curve. Using a time range of 100 ms before the 
stimulus it establishes a baseline firing rate. The value is then pulled by looking 
for where a PSTH of the curve crosses a specific fraction of the maximum fire rate 
the cell reaches.

* *tuningOnsetRate*: The firing rate within the first 50 ms of the response as based 
on *latency*. Calculated by 
database_generation_funcs.calculate_onset_to_sustained_ratio.

* *tuningSustainedRate*: The number of spikes over time that occur 100 ms after the 
response as based on *latency*. Calculated by 
database_generation_funcs.calculate_onset_to_sustained_ratio.

* *tuningBaseRate*: The number of spikes over time the occur from 100 ms before the 
stimulus to 50 ms before the stimulus is presented. Calculated by 
database_generation_funcs.calculate_onset_to_sustained_ratio.

* *cfOnsetivityIndex*: The ratio of the difference between onset to sustained spike 
rates calculated by: (*onsetRate* - *sustainedRate*) / (*sustainedRate* + *onsetRate*) 
A positive number means there were more spikes at the onset of the response than 
there were in the sustained.

* *monotonicityIndex*: This value represents how the response firing rate changed 
with intensity after being normalized by the baseline firing rate. Calculated by 
taking the mean number of spikes at the largest intensity and dividing by the mean 
number of spikes at whichever intensity produced the greatest response.

### Do the cell populations prefer different properties of amplitude modulated sounds? (Figure 4)
* *highestSync*: The highest AM rate that was significantly synchronized (p<0.05)

* *highestUSync*: The highest AM rate that is unsynchonized, used if the cell
becomes synchonized at higher rates, but is not synchronized at lower rates

* *highestSyncCorrected*: The highest AM rate that was significantly synchronized
after a Bonferroni correction

* *rateDiscrimAccuracy*: The accuracy of a cell determining the amplitude
modulation rate for a trial

* *phaseDiscrimAccuracy_{}Hz*: The accuracy of a cell determining the phase of
the amplitude modulation at a specific rate. There is one value for every rate
used

* *am_synchronization_pVal*: The best p-value calculated for synchronization of a
cell from Rayleigh's Test

* *am_synchronization_ZStat*: The corresponding statistic for the p-value from
Rayleigh's test

* *am_response_pVal*: The best p-value calculated for a cell's response compared
to the baseline firing rate using a Mann-Whitney U test

* *am_response_ZStat*: Corresponding U-statistic for the above p-value

# Figure Pure tone characterization
## Figure script: `figure_frequency_tuning.py`
**Requires**:
`data_freq_tuning_examples.npz`
Produced by:
`generate_example_freq_tuning.py`

`direct_and_indirect_cells2.h5` Produced by: `database_generation.py`

figure parameters from figparams.py

## Panels A, B
These panels are produced by the figure script `figure_frequency_tuning.py`.
To get tuning curve data, it requires `data_freq_tuning_examples.npz` which is 
produced by `generate_example_freq_tuning.py`

## Panel C
This panel uses *bw10* column of the database calculated in `base stats`. Shows 
how the bandwidth varies between cell types and the bar representing the median.

## Panel D
This panel uses the *threshold* column of the database calulated in `base stats`. 
Displays different threshold values between cell populations with the bar representing
the median threshold for each population

## Panel E
This panel uses the *latency* column of the database calculated in `base stats`.
It compares cell latency between populations with the bar representing the median
latency time for each population.

## Panel F
This panel uses the  *cfOnsetivityIndex* column of the database calulated in `base stats`.
It compares how the indices of the populations varies with the bar being the median.

## Panel G
This panel uses the *monotonicityIndex* column of the database calculated in `base stats`.
It compares how the indices of the populations varies with the bar being the median.

# Figure AM
## Figure script: `figure_am.py`
**Requires**:
`data_am_examples.npz`
Produced by: `generate_example_am_rasters.py`

`direct_and_indirect_cells2.h5` Produced by: `database_generation.py`

figure parameters from figparams.py

## Panels A, D
These panels include example raster plots of a single D1 cell (A) and single nD1
cell (D). Next to the rasters is a plot of the mean firing rate and standard
deviations at each modulation rate. Uses data stores in `data_am_examples.npz`.

## Panel B
Pie charts that show percentages of D1 and nD1 cells that are synchronized to at
least one modulation rate. Uses the *highestSyncCorrected* column of the database
calculated in `base stats`.

## Panel C
Plot comparing the highest synchonization rate of D1 cells and nD1 cells. Uses
the *highestSyncCorrected* column of the database calculated in `base stats`.

## Panel E
Plot of the accuracy of cells in discriminating the rate of amplitude modulation.
Uses the *rateDiscrimAccuracy* column of the database calculated in `base stats`

## Panel F
Plot of the accuracy of cells in discriminating the phase of amplitude modulation.
Use the *phaseDiscrimAccuracy_{}Hz* where the {} is replaced by the specific rate.
Calculated in `base stats`

# Exploring Data to produce stats and reports
## Files in Extras
### cluster_counts.py
Calculate number of clusters by D1 vs nD1, by brain region filters, by
tuning filters, etc. Needs a database that has calculations for tuningTest
paradigms stored (from `extras/tuning_test_comparisons.py`)

### database_cell_locations.py
Takes as argument a pandas DataFrame and adds new columns. Computes the depths and cortical locations of all cells with suppression indices computed

### figure_cell_sound_responses.py
Generates a figure used to explore all aspects of sound responses for the
various stimuli we presented to the mice. Panels from here may or may not make
it into the final paper.

### fix_inforec.py
Fix inforec by moving recording track info from 'info' to 'recordingTrack'.
Currently, it only works for files in the format that Matt has where
the info argument is in a different line from the Experiment definition.

### generate_allCell_reports.py
This is used to give the researcher the high level overview of the cell
responses and the characteristic of the neuronal signal on stimulus

[For all cells in DB] create cell reports include the following plots for
four sessions:
1. noiseburst: raster, PSTH, ISI, waverform, sparks over time
2. laserpulse: raster, PSTH, ISI, waveform, sparks over time
3. TuningCurve: raster plot(averaged across all intensities), waveform, heatmap
4. Amplitude modulation: raster plot

By default, it generates for all animals in the dataframe. The user can pass an
optional parameter to specify either just pure tone responsive cells or AM
responsive cells.

Ex: 
    
    python3 generate_allCell_reports.py tuning (generates reports for tuned cells)
    
    python3 generate_allCell_reports.py (generates reports for all cells)
    
    python3 generate_allCell_reports.py am (generates reports for AM cells)

Requires a dataframe with tuningTest calculations stored as it uses the R2 of the
Gaussian from the tuning test in a title as a reported value (line 741). This
can be generated by `extras/tuning_test_comparisons.py`

### normalized_hist_plot_functions.py
Contains functions used for plotting normalized histograms for comparisons.
One function needs a datafrome, the other can use raw data fed to it.

### power_analysis.py
A collection of functions for power analysis of data

### sorted_reports.py
Using the list of quality spikes (manually picked by Matt Nardoci), this
program goes through the folder of reports and seperates the reports into
two new folders of 'Quality_tuning' and 'NonQuality_tuning'. It also saves
an h5 file that contains all the cell information for each cell for later
use incase cluster numbers in the database change.

### sound_responses_outside_striatum.py
Calculating total number of cells that respond to sound while outside of
the striatum across all subjects histology data is known for.

### tuning_test_comparisons.py
Calculates some statistics and sound response properties for tuningTest paradigm.
The database generated from here is needed by:
extras/cluster_counts.py
extras/generate_allCell_reports.py

# Exploring Data to preform test calculations and comparisons 
## Files in test_scripts
### database_generation_test.py
This script will generate a simpler database with all subjects defined
as d1pi mice in studyparams.py. This script is useful for testing changes in calculations when generating a database and does not include all the calculations of 'database_generation.py' This script can create a database for one example mouse or all mice. Output is an h5 file containing all the below information in `Database 2 contents`

# Test database contents
* *laserpulse_pVal*: The p-value for comparing the baseline and response firing
rates of the laserpulse paradigm using a Mann-Whitney U test.

* *laserpulse_ZStat*: The corresponding U-statistic for the above p-value

* *laserpulse_SpikeCountChange*: The change in spike count for the laserpulse as calculated by
`response - baseline`

* *laserpulse_baselineSpikeCount*: The baseline laserpulse mean spike count. Baseline period
was [-100 ms, 0 ms]

* *laserpulse_responseSpikeCount*: The response laserpulse mean spike count. Response period
was [0 ms, 100 ms]

* *latency*: The time (in seconds) from when the stimulus is presented until the 
cell shows a response. Calculated using database_generation_funcs.calculate_latency(). 
This looks at the *cf* on the tuning curve. Using a time range of 100 ms before the 
stimulus it establishes a baseline firing rate. The value is then pulled by looking 
for where a PSTH of the curve crosses a specific fraction of the maximum fire rate 
the cell reaches.

* *tuningResponseRate*: The number of spikes over time that occur from 0 to 100 ms 
after the stimulus is presented. Calculated by database_generation_funcs.calculate_onset_to_sustained_ratio.

* *tuningBaseRate*: The number of spikes over time that occur from 100 ms before the 
stimulus to 0 ms before the stimulus is presented. Calculated by 
database_generation_funcs.calculate_onset_to_sustained_ratio.

* *tuningResponseRatio*: Index (between 0 and 1) for the ratio between response and base firing rates caculated with the expression (R - B) / (R + B) where R is response period firing rate and B is baseline period firing rate. 

* *bw10*: The bandwidth 10 above the sound intenisty threshold. Calculated by the 
equation: (*upperFreq* - *lowerFreq*) / *cf*

* *tuning_pVal*: The p-value from comparing the baseline firing rate vs response 
firing rate of all frequencies at the highest intensity for the tuningCurve
paradigm with a Mann-Whitney U test

* *tuning_ZStat*: Corresponding U-statistic for the p-value

* *thresholdFRA*: The characteristic intensity for peak firing rate. Found using 
the intensity index from 
database_generation_funcs.calculate_intensity_threshold_and_CF_indices and 
indexing the unique intensities (uniqueIntensity) for a session.

* *cf*: The characteristic frequency is the frequency that is most sensitive to
sound.

* *tuningOnsetRate*: The firing rate within the first 50 ms of the response as based 
on *latency*. Calculated by 
database_generation_funcs.calculate_onset_to_sustained_ratio.

* *tuningSustainedRate*: The number of spikes over time that occur 100 ms after the 
response as based on *latency*. Calculated by 
database_generation_funcs.calculate_onset_to_sustained_ratio.

* *lowerFreq*: The lowest frequency with a response 10 dB SPL above the sound 
intensity threshold. Calculated by 
database_generation_funcs.calculate_BW10_params.

* *upperFreq*: The highest frequency with a response 10 dB SPL above the sound 
intensity threshold. Calculated by database_generation_funcs.calculate_BW10_params.

* *cfOnsetivityIndex*: The ratio of the difference between onset to sustained spike 
rates calculated by: (*onsetRate* - *sustainedRate*) / (*sustainedRate* + *onsetRate*) 
A positive number means there were more spikes at the onset of the response than 
there were in the sustained.

### database_generation_one_cell.py
Generates a database for one cell. Useful for observing intermediate calculations 

### figure_generation.py
Generates a figure using laserpulse and tuning curve data. Useful for testing comparisons between data.

### generate_allCell_reports_test.py
generates simpler cell reports than that of 'generate_allCell_reports.py'. Useful for comparing cells for only some datasets

## Files in old_scripts
### database_generation_old.py
An old version of database_generation.py. 

### figure_am_old.py
An old version of figure_am.py

### studyparams_original.py
An old version of studyparams.py
