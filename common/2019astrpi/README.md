# 2019astrpi
This project looks into characterizing MSN's on the direct and indirect striatal pathway

## How to run a database_ or figure_ script
When run normally, each script will use all animals and store in a default database. Each 
script can also be run using arguments. The two arguements are 'SUBJECT' and 'TAG'.  

SUBJECT can be a singular subject, 'all', or 'test'. 'all' will use all of the subjects listed in 
studyparams.py. 'test' will use the test subject listed in studyparams.py. If nothing is 
specified, all subjects will be ran. 

Optionally you can set a TAG on the database (using file name acceptable characters). You must enter 
a subject parameter before entering a tag. Aditionally, these two must be the first two parameters 
entered, any subsequent will not be used. If 'AM' or 'TC' are in the tag, 'AM' or 'TC' will not be 
added when each respective statistics script is run.

Run as:
`database_.py SUBJECT TAG` or `figure_.py SUBJECT TAG`

More specific instructions can be found on each script's docstring.
## Database
The file `studyparams.py` contains a list of animals as well as statistical parameters for the 
database calculations. Database scripts use functions from the moddule 
`database_generation_funcs.py`.

### Producing a database
#### database_basic_generation.py
Generates a minimally filtered basic database. 

Output is an h5 file containing the statistics under the `Base stats` section in `Database contents` 
below. 

### Manipulating a database
#### database_select_reliable_cells.py
Using an existing database, selects for reliable cells that have data for cell comparison. Includes 
the removal of manually selected cells, listed in `cell_indices_manually_removed.txt`, found in the 
extras folder. 

Calculates statistics using laserpulse session data. Used for D1 vs. nD1 cell type characterization. 

Output is an h5 file with the information under the `Laserpulse stats` section in 
`Database contents` below added. contains only rows that passed cell selection. 

#### database_add_tuning_stats.py
Using an existing database, calculates statistics using tuning curve session data. These statistics 
are used for pure tone sound response comparison. 

Output is an h5 file with the information under the `Tuning stats` section in `Database contents` 
below added.

#### database_am_am_stats.py
Using an existing database, calculates statistics using amplitude modulated (AM) session data. Used 
for AM sound response comparison. 

Output is an h5 file with the information under the `AM stats` section in `Database contents` below
added. 

### Database contents
These statistics are used to address the following questions. Each statistic is labelled with a
number corresponding to what question it addresses. 

1. Are cells identifiable *in vivo* and do they respond differently to basic sounds? (Figure 1)
2. Is there a difference in the basic responses of the cells to different sounds? (Figure 2)
3. Do the cells prefer different properties of pure tone sounds? (Figure 3)
4. Do the cell populations prefer different properties of amplitude modulated sounds? (Figure 4)

#### Base stats
Columns added when the basic database is created with `database_basic_generation.py`

TODO: create column descriptions for base stats  

* *behavSuffix*:

* *brainArea*:

* *cluster*:

* *date*: The data that the data was collected

* *depth*:

* *ephysTime*:

* *index*:

* *info*:

* (1) *isiViolations*:

* *maxDepth*:

* *nSpikes*:

* *paradigm*:

* *recordingTrack*:

* *sessionType*:

* *spikePeakAmplitudes*:

* *spikePeakTimes*:

* *spikeShape*:

* (1) *spikeShapeQuality*:

* *spikeShapeSD*:

* *subject*: The mouse that the data was recorded from

* *tetrode*: The tetrode that recorded the data.

#### Laserpulse stats
Columns added with `database_select_reliable_cells.py`, using a baseline period of [-100 ms, 0 ms].
This corresponds to a response period of [0 ms, 100 ms]. There are two additional sets of statistics
generated using baseline periods of [-50 ms, 0 ms] and [-200 ms, 0 ms] respectively. These sets
are named identical to those below, but with '50' or '200' following each column name. 

* (1) *laserpulseBaselineFR*: The baseline laserpulse mean firing rate. Baseline period was 
[-100 ms, 0 ms]

* (1) *laserpulseResponseFR*: The response laserpulse mean firing rate. Response period was 
[0 ms, 100 ms]

* (1) *laserpulseFRChange*: The change in firing rate for the laserpulse as calculated by
`response - baseline`

* (1) *laserpulsePval*: The p-value for comparing the baseline and response firing rates of the 
laserpulse paradigm using a Mann-Whitney U test.

* (1) *laserpulseZstat*: The corresponding U-statistic for the above p-value

#### Tuning stats
Columns added with `database_add_tuning_stats.py`

* (3) *tuningBaseFR*: The number of spikes over time the occur from 100 ms before the stimulus to 
50 ms before the stimulus is presented. Calculated by 
`database_generation_funcs.calculate_onset_to_sustained_ratio()`.

* (2) *tuningResponseFR*: The firing rate within the 100 ms response period as based on *latency*. 
Calculated by `database_generation_funcs.calculate_onset_to_sustained_ratio()`.

* (3) *tuningOnsetFR*: The firing rate within the first 50 ms of the response as based on 
*latency*. Calculated by `database_generation_funcs.calculate_onset_to_sustained_ratio()`.

* (3) *tuningSustainedFR*: The firing rate within the period of 50 ms to 100 ms of the response as 
based on *latency*. Calculated by database_generation_funcs.calculate_onset_to_sustained_ratio.

* (2) *tuningResponseFRIndex*: Index (between 0 and 1) for the ratio between response and base firing 
rates caculated with the expression (response - baseline) / (response + baseline).

* (2) *tuningPval*: The p-value from comparing the baseline firing rate vs response firing rate of 
all frequencies at the highest intensity for the tuningCurve paradigm with a Mann-Whitney U test

* (2) *tuningZstat*: Corresponding U-statistic for the p-value

* (3) *latency*: The time (in seconds) from when the stimulus is presented until the cell shows a 
response. Calculated using `database_generation_funcs.calculate_latency()`. This looks at the *cf* 
on the tuning curve. Using a time range of 100 ms before the stimulus it establishes a baseline 
firing rate. The value is then pulled by looking for where a PSTH of the curve crosses a specific 
fraction of the maximum fire rate the cell reaches.

* (3) *cf*: The characteristic frequency is the frequency that is most sensitive to sound.

* (3) *upperFrequency*: The highest frequency with a response 10 dB SPL above the sound intensity 
threshold. Calculated by `database_generation_funcs.calculate_BW10_params()`.

* (3) *lowerFrequency*: The lowest frequency with a response 10 dB SPL above the sound intensity 
threshold. Calculated by `database_generation_funcs.calculate_BW10_params()`.

* (3) *bw10*: The bandwidth 10 above the sound intenisty threshold. Calculated by the equation: 
(*upperFreq* - *lowerFreq*) / *cf*

* (3) *cfOnsetivityIndex*: The ratio of the difference between onset to sustained spike rates 
calculated by: (*onsetRate* - *sustainedRate*) / (*sustainedRate* + *onsetRate*). A positive number 
means there were more spikes at the onset of the response than there were in the sustained.

* (3) *rSquaredFit*: The mean of all of the r<sup>2</sup> values of the 10 dB SPL above the sound 
intensity threshold. Calculated by `database_generation_funcs.calculate_BW10_params`.

* (3) *thresholdFRA*: The characteristic intensity for peak firing rate. Found using the intensity 
index from `database_generation_funcs.calculate_intensity_threshold_and_CF_indices()` and indexing the 
unique intensities (uniqueIntensity) for a session.

#### AM stats
Columns added with `database_add_am_stats.py`

TODO: Add stats to this section after `database_add_am_stats.py` finished

#### Unused stats
Columns not being added to database currently.

TODO: Move stats to 'AM stats' after `database_add_am_stats.py` finished

* (1) *noiseburst_pVal*: The p-value for comparing the baseline and response firing
rates of the noiseburst paradigm using a Mann-Whitney U test.

* (1) *noiseburst_ZStat*: The corresponding U-statistic for the above p-value

* (1) *noiseburst_baselineSpikeCount*: The baseline noiseburst mean spike count. Baseline period 
was [-100 ms, 0 ms] 

* (1) *noiseburst_responseSpikeCount*: The response noiseburst mean spike count. Response period
was [0 ms, 100 ms] 

* (1) *tuningTest_pVal*: The p-value found from comparing the baseline firing rate of
all frequencies at the maximum intensity to the response using a Mann-Whitney U
test. Baseline period was [-100 ms, 0 ms] and response period was [0 ms, 100 ms]

* (1) *tuningTest_ZStat*: The corresponding U-statistic for the above p-value

* (1) *ttR2Fit*: The R^2 value of the Gaussian fit to the tuning test paradigm.

* (2) *AMBaseFROnset*: The corresponding baseline firing rate for the best onset
response firing rate for a cell. Baseline period was [-100 ms, 0 ms]

* (2) *AMRespFROnset*: The highest onset response firing rate of all the rates 
presented. Onset period was [0 ms, 100 ms]

* (2) *AMBestRateOnset*: The amplitude modulation rate that yielded the best onset
response

* (2) *AMBaseFRSustained*: The corresponding baseline firing rate for the best 
sustained response. Baseline period was [-500 ms, -100 ms]

* (2) *AMRespFRSustained*: The highest sustained firing rate of all the rates presented. Sustained 
period was [100 ms, 500 ms]

* (2) *AMBestRateSustained*: The amplitude modulation rate that produced the highest
sustained response

* (2) *tuningBaseFRBestFreqMaxInt*: The corresponding baseline firing rate for the
frequency that had the largest response firing rate. Baseline period was
[-100 ms, 0 ms]

* (2) *tuningRespFRBestFreqMaxInt*: The firing rate for the best frequency at maximum
intensity. Response period was [0 ms, 100 ms]

* (2) *tuningBestFreqMaxInt*: The frequency that had the highest response firing rate
at the maximum intensity presented

* (3) *fitMidpoint*: The midpoint of the gaussian fit for the tuning curve calculated
 using the square root of the *upperFreq* * *lowerFreq*

* (3) *monotonicityIndex*: This value represents how the response firing rate changed 
with intensity after being normalized by the baseline firing rate. Calculated by 
taking the mean number of spikes at the largest intensity and dividing by the mean 
number of spikes at whichever intensity produced the greatest response.

* (4) *highestSync*: The highest AM rate that was significantly synchronized (p<0.05)

* (4) *highestUSync*: The highest AM rate that is unsynchonized, used if the cell
becomes synchonized at higher rates, but is not synchronized at lower rates

* (4) *highestSyncCorrected*: The highest AM rate that was significantly synchronized
after a Bonferroni correction

* (4) *rateDiscrimAccuracy*: The accuracy of a cell determining the amplitude
modulation rate for a trial

* (4) *phaseDiscrimAccuracy_{}Hz*: The accuracy of a cell determining the phase of
the amplitude modulation at a specific rate. There is one value for every rate
used

* (4) *am_synchronization_pVal*: The best p-value calculated for synchronization of a
cell from Rayleigh's Test

* (4) *am_synchronization_ZStat*: The corresponding statistic for the p-value from
Rayleigh's test

* (4) *am_response_pVal*: The best p-value calculated for a cell's response compared
to the baseline firing rate using a Mann-Whitney U test

* (4) *am_response_ZStat*: Corresponding U-statistic for the above p-value

## Figures
The file `figparams.py` contains common parameters for figures and data related to these figures.

TODO: Update this section

### Pure tone characterization
#### figure_frequency_tuning.py
This script creates a summary plot for tuning curve data comparison using a database that has had
statistics added with `database_add_tuning_stats.py`.  

**Requires**:
`data_freq_tuning_examples.npz`
Produced by:
`generate_example_freq_tuning.py`

`direct_and_indirect_cells2.h5` Produced by: `database_generation.py`

figure parameters from figparams.py

### Panels A, B
These panels are produced by the figure script `figure_frequency_tuning.py`.
To get tuning curve data, it requires `data_freq_tuning_examples.npz` which is 
produced by `generate_example_freq_tuning.py`

### Panel C
This panel uses *bw10* column of the database calculated in `base stats`. Shows 
how the bandwidth varies between cell types and the bar representing the median.

### Panel D
This panel uses the *threshold* column of the database calulated in `base stats`. 
Displays different threshold values between cell populations with the bar representing
the median threshold for each population

### Panel E
This panel uses the *latency* column of the database calculated in `base stats`.
It compares cell latency between populations with the bar representing the median
latency time for each population.

### Panel F
This panel uses the  *cfOnsetivityIndex* column of the database calulated in `base stats`.
It compares how the indices of the populations varies with the bar being the median.

### Panel G
This panel uses the *monotonicityIndex* column of the database calculated in `base stats`.
It compares how the indices of the populations varies with the bar being the median.

### AM characterization
#### figure_am.py
**Requires**:
`data_am_examples.npz`
Produced by: `generate_example_am_rasters.py`

`direct_and_indirect_cells2.h5` Produced by: `database_generation.py`

figure parameters from figparams.py

### Panels A, D
These panels include example raster plots of a single D1 cell (A) and single nD1
cell (D). Next to the rasters is a plot of the mean firing rate and standard
deviations at each modulation rate. Uses data stores in `data_am_examples.npz`.

### Panel B
Pie charts that show percentages of D1 and nD1 cells that are synchronized to at
least one modulation rate. Uses the *highestSyncCorrected* column of the database
calculated in `base stats`.

### Panel C
Plot comparing the highest synchonization rate of D1 cells and nD1 cells. Uses
the *highestSyncCorrected* column of the database calculated in `base stats`.

### Panel E
Plot of the accuracy of cells in discriminating the rate of amplitude modulation.
Uses the *rateDiscrimAccuracy* column of the database calculated in `base stats`

### Panel F
Plot of the accuracy of cells in discriminating the phase of amplitude modulation.
Use the *phaseDiscrimAccuracy_{}Hz* where the {} is replaced by the specific rate.
Calculated in `base stats`

## Extras
### Manual cell selection
#### cell_indices_coded.txt
List of all indices for the database of all animals. Each index is formatted as: index,X

X is a value between 1 and 4 that corresponds to type of manual selection, or nothing if none apply:
1. Noise or no cell character
2. Some cell character, but unreliable or noisy
3. No laserpulse or sound response (may be nD1 with no sound response)
4. Laserpulse response, no sound response (may be D1 with no sound response)

#### cell_indices_manually_removed.txt
List of indices for cells that should be removed by manual selection. Cell indices come from
any indices with a number code in `cell_indices_coded`.

### Cell reports 
#### generate_cell_reports.py
This is used to give the researcher the high level overview of the cell responses and the 
characteristic of the neuronal signal on stimulus

Cell reports include the following plots for four sessions:
1. noiseburst: raster, PSTH, ISI, waverform, sparks over time
2. laserpulse: raster, PSTH, ISI, waveform, sparks over time
3. TuningCurve: raster plot(averaged across all intensities), waveform, heatmap
4. Amplitude modulation: raster plot

If run normally, it will use all animals and store the reports in 
`data/cellreports/2019astrpi/all_cells`. It can also be run using the 'SUBJECT' and 'TAG' 
arguements similiarilly to database_.py scripts.

Requires a dataframe with tuningTest calculations stored as it uses the R2 of the
Gaussian from the tuning test in a title as a reported value (line 741). This
can be generated by `extras/tuning_test_comparisons.py`

### Other 
TODO: The following information has not be reviewed yet

#### cluster_counts.py
Calculate number of clusters by D1 vs nD1, by brain region filters, by
tuning filters, etc. Needs a database that has calculations for tuningTest
paradigms stored (from `extras/tuning_test_comparisons.py`)

#### database_cell_locations.py
Takes as argument a pandas DataFrame and adds new columns. Computes the depths and cortical locations of all cells with suppression indices computed

#### figure_cell_sound_responses.py
Generates a figure used to explore all aspects of sound responses for the
various stimuli we presented to the mice. Panels from here may or may not make
it into the final paper.

#### fix_inforec.py
Fix inforec by moving recording track info from 'info' to 'recordingTrack'.
Currently, it only works for files in the format that Matt has where
the info argument is in a different line from the Experiment definition.

#### normalized_hist_plot_functions.py
Contains functions used for plotting normalized histograms for comparisons.
One function needs a datafrome, the other can use raw data fed to it.

#### power_analysis.py
A collection of functions for power analysis of data

#### sorted_reports.py
Using the list of quality spikes (manually picked by Matt Nardoci), this
program goes through the folder of reports and seperates the reports into
two new folders of 'Quality_tuning' and 'NonQuality_tuning'. It also saves
an h5 file that contains all the cell information for each cell for later
use incase cluster numbers in the database change.

#### sound_responses_outside_striatum.py
Calculating total number of cells that respond to sound while outside of
the striatum across all subjects histology data is known for.

#### tuning_test_comparisons.py
Calculates some statistics and sound response properties for tuningTest paradigm.
The database generated from here is needed by:
extras/cluster_counts.py
extras/generate_allCell_reports.py

## Archive
Contains old versions of scripts for reference. 