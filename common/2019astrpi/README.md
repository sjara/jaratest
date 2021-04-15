# 2019astrpi
This project looks into characterizing MSN's on the direct and indirect striatal pathway

## Navigation
#### A - Generating and Using a Database 
1. General Instructions for Running Scripts
2. Creating a Basic Database
3. Selecting Reliable Cells and Adding Laserpulse Session Statistics
4. Adding Frequency Tuning Session Statistics
5. Adding Amplitude Modulated (AM) Session Statistics
6. Plotting Frequency Tuning Comparisons 
7. Plotting Amplitude Modulated (AM) Comparisons 

#### B - Database Contents 
1. Base Statistics
2. Laserpulse Statistics
3. Frequency Tuning Statistics
4. Amplitude Modulated (AM) Statistics 
5. Other/Unused Statistics 

#### C - Figure Contents 
1. Frequency Tuning Figure Panels
2. Amplitude Modulated (AM) Figure Panels 

#### D - Other Files
1. Parameter Files
2. Files in `extras`

# A - Generating and Using a Database
This section details steps from building a basic database, to plotting summary figures for data 
comparison. `database_add_tuning_stats.py` and `database_add_am_stats.py` can be run in any order,
the following is simply an example route of database creation. 

## 1. General Instructions for Running Scripts
When run without arguments, each script will use all animals and store in a default database. Each 
script can also be run using arguments. The two arguments are 'SUBJECT' and 'TAG'. Specific 
instructions can be found in the subsequent sections below, or in each script's docstring.

SUBJECT can be a single animal (example - `d1pi043`), `all`, or `test`. `all` will use all of the 
subjects listed in studyparams.py. `test` will use the test subject listed in studyparams.py. If 
nothing is specified, all subjects will be used. 

Optionally you can set a TAG on the database (using filename acceptable characters). You must enter 
a subject parameter before entering a tag. The tag will appear at the end of the database filename.

Run as (if not using tag)
`database_.py SUBJECT` or `figure_.py SUBJECT`

Run as (if using tag)
`database_.py SUBJECT TAG` or `figure_.py SUBJECT TAG`

The file `studyparams.py` contains a list of animals as well as statistical parameters for the 
database calculations. Database scripts use functions from the moddule 
`database_generation_funcs.py`.

## 2. Creating a Basic Database
The first step is to create a minimally filtered, basic database. This is done by running the file 
`database_basic_generation.py` 

Output is a file named `astrpi_all_clusters.h5` (modified if subjects or tag specified), 
containing the statistics under `Base statistics` in section `B - Database contents` 
below. 

## 3. Selecting Reliable Cells and Adding Laserpulse Session Statistics
After the creation of a basic database, run `database_select_reliable_cells.py` in order to filter
the database and calculate laserpulse session statistics. `cell_indices_manually_removed.txt` 
contains a list of manually-removed cells, found in `extras`. Other selection parameters can be
found in `studyparams.py`.
 
Output is a file named `astrpi_all_cells.h5` (modified if subjects or tag specified), 
containing the statistics under `Base statistics` and `Laserpulse statistics` in section 
`B - Database contents` below. Contains only rows that passed cell selection. Note, if this script 
is ran with a database that has had frequency tuning or amplitude modulated (AM) statistics added, 
they will be removed. 

## 4. Adding Frequency Tuning Session Statistics
In order to add frequency tuning session statistics, run `database_add_tuning_stats.py`. 

Output is a file named `astrpi_all_cells.h5` (modified if subjects or tag specified), 
containing the statistics under `Base statistics`, `Laserpulse statistics`, and 
`Frequency Tuning statistics`in section `B - Database contents` below. Note, if this script 
is ran with a database that has had frequency tuning previously added, these statistics will be
recalculated and replaced. 

## 5. Adding Amplitude Modulated (AM) Session Statistics
In order to add amplitude modulated (AM) session statistics, run `database_add_am_stats.py`. 

Output is a file named `astrpi_all_cells.h5` (modified if subjects or tag specified), 
containing the statistics under `Base statistics`, `Laserpulse statistics`, 
`Frequency Tuning statistics`, and `Amplitude Modulated (AM) statistics` in section 
`B - Database contents` below. Note, if this script is ran with a database that has had amplitude 
modulated (AM) previously added, these statistics will be recalculated and replaced. 

## 6. Plotting Frequency Tuning Comparisons 
Once a database has been created that contains frequency tuning session statistics, the file 
`figure_frequency_tuning` can be ran to generate a comparison figure.

Output is a figure containing the panels under `Frequency Tuning Figure Panels` in the section 
`C - Figure Contents` below. 

## 7. Plotting Amplitude Modulated (AM) Comparisons 
Once a database has been created that contains amplitude modulated (AM) session statistics, the file 
`figure_am` can be ran to generate a comparison figure.

Output is a figure containing the panels under `Amplitude Modulated (AM) Figure Panels` in the 
section `C - Figure Contents` below. 

# B - Database Contents 
Each following section details statistics generated and added to a database when the corresponding
database file is ran. These statistics are used to address the following questions. 

TODO: Update these questions once comparions have been plotted 

1. Are cells identifiable *in vivo* and do they respond differently to basic sounds? (Figure 1)
2. Is there a difference in the basic responses of the cells to different sounds? (Figure 2)
3. Do the cells prefer different properties of pure tone sounds? (Figure 3)
4. Do the cell populations prefer different properties of amplitude modulated sounds? (Figure 4)

## 1. Base Statistics
Columns added when the basic database is created with `database_basic_generation.py`

* *behavSuffix*:

* *brainArea*:

* *cluster*:

* *date*: The date that the data was collected

* *depth*:

* *ephysTime*:

* *index*:

* *info*:

* *isiViolations*:

* *maxDepth*:

* *nSpikes*:

* *paradigm*:

* *recordingTrack*:

* *sessionType*:

* *spikePeakAmplitudes*:

* *spikePeakTimes*:

* *spikeShape*:

* *spikeShapeQuality*:

* *spikeShapeSD*:

* *subject*: The mouse that the data was recorded from

* *tetrode*: The tetrode that recorded the data.

## 2. Laserpulse Statistics
Columns added with `database_select_reliable_cells.py`, using a baseline period of [-100 ms, 0 ms].
This corresponds to a response period of [0 ms, 100 ms]. There are two additional sets of statistics
generated using baseline periods of [-50 ms, 0 ms] and [-200 ms, 0 ms] respectively. These sets
are named identical to those below, but with '50' or '200' following each column name. 

* *laserpulseBaselineFR100*: The baseline laserpulse mean firing rate. Baseline period was 
[-100 ms, 0 ms]

* *laserpulseBaselineFR200*: The baseline laserpulse mean firing rate. Baseline period was 
[-200 ms, 0 ms]

* *laserpulseBaselineFR50*: The baseline laserpulse mean firing rate. Baseline period was 
[-50 ms, 0 ms]

* *laserpulseFRChange100*: The change in firing rate for the laserpulse as calculated by
`response - baseline`, using 100 ms baseline and response periods 

* *laserpulseFRChange200*: The change in firing rate for the laserpulse as calculated by
`response - baseline`, using 200 ms baseline and response periods 

* *laserpulseFRChange50*: The change in firing rate for the laserpulse as calculated by
`response - baseline`, using 50 ms baseline and response periods 

* *laserpulsePval100*: The p-value for comparing the baseline and response firing rates of the 
laserpulse paradigm using a Mann-Whitney U test, using 100 ms baseline and response periods 

* *laserpulsePval200*: The p-value for comparing the baseline and response firing rates of the 
laserpulse paradigm using a Mann-Whitney U test, using 200 ms baseline and response periods 

* *laserpulsePval50*: The p-value for comparing the baseline and response firing rates of the 
laserpulse paradigm using a Mann-Whitney U test, using 50 ms baseline and response periods 

* *laserpulseResponseFR100*: The response laserpulse mean firing rate. Response period was 
[0 ms, 100 ms]

* *laserpulseResponseFR200*: The response laserpulse mean firing rate. Response period was 
[0 ms, 200 ms]

* *laserpulseResponseFR50*: The response laserpulse mean firing rate. Response period was 
[0 ms, 50 ms]

* *laserpulseZstat100*: The corresponding U-statistic for the above p-value, using 100 ms baseline 
and response periods. 

* *laserpulseZstat200*: The corresponding U-statistic for the above p-value, using 200 ms baseline 
and response periods. 

* *laserpulseZstat50*: The corresponding U-statistic for the above p-value, using 50 ms baseline 
and response periods. 

## 3. Frequency Tuning Statistics
Columns added with `database_add_tuning_stats.py`

* *bw10*: The bandwidth 10 above the sound intenisty threshold. Calculated by the equation: 
(*upperFreq* - *lowerFreq*) / *cf*

* *cf*: The characteristic frequency, the frequency that is most sensitive to sound.

* *cfOnsetivityIndex*: The ratio of the difference between onset to sustained spike rates 
calculated by: (*onsetRate* - *sustainedRate*) / (*sustainedRate* + *onsetRate*). A positive number 
means there were more spikes at the onset of the response than there were in the sustained.

* *latency*: The time (in seconds) from when the stimulus is presented until the cell shows a 
response. Calculated using `database_generation_funcs.calculate_latency()`. This looks at the *cf* 
on the tuning curve. Using a time range of 100 ms before the stimulus it establishes a baseline 
firing rate. The value is then pulled by looking for where a PSTH of the curve crosses a specific 
fraction of the maximum fire rate the cell reaches.

* *lowerFrequency*: The lowest frequency with a response 10 dB SPL above the sound intensity 
threshold. Calculated by `database_generation_funcs.calculate_BW10_params()`.

* *rSquaredFit*: The mean of all of the r<sup>2</sup> values of the 10 dB SPL above the sound 
intensity threshold. Calculated by `database_generation_funcs.calculate_BW10_params`.

* *thresholdFRA*: The characteristic intensity for peak firing rate. Found using the intensity 
index from `database_generation_funcs.calculate_intensity_threshold_and_CF_indices()` and indexing 
the unique intensities (uniqueIntensity) for a session.

* *tuningBaselineFR*: The number of spikes over time the occur from 100 ms before the stimulus to 
50 ms before the stimulus is presented. Calculated by 
`database_generation_funcs.calculate_onset_to_sustained_ratio()`.

* *tuningOnsetFR*: The firing rate within the first 50 ms of the response as based on 
*latency*. Calculated by `database_generation_funcs.calculate_onset_to_sustained_ratio()`.

* *tuningPval*: The p-value from comparing the baseline firing rate vs response firing rate of 
all frequencies at the highest intensity for the tuningCurve paradigm with a Mann-Whitney U test

* *tuningResponseFR*: The firing rate within the 100 ms response period as based on *latency*. 
Calculated by `database_generation_funcs.calculate_onset_to_sustained_ratio()`.

* *tuningResponseFRIndex*: Index (between 0 and 1) for the ratio between response and base firing 
rates caculated with the expression (response - baseline) / (response + baseline).

* *tuningSustainedFR*: The firing rate within the period of 50 ms to 100 ms of the response as 
based on *latency*. Calculated by database_generation_funcs.calculate_onset_to_sustained_ratio.

* *tuningZstat*: Corresponding U-statistic for the p-value

* *upperFrequency*: The highest frequency with a response 10 dB SPL above the sound intensity 
threshold. Calculated by `database_generation_funcs.calculate_BW10_params()`.

## 4. Amplitude Modulated (AM) Statistics 
Columns added with `database_add_am_stats.py`

* *AMBestRateOnset*: The amplitude modulation rate that yielded the best onset
response

* *AMBestRateSustained*: The amplitude modulation rate that produced the highest
sustained response

* *AMPval*: The best p-value calculated for a cell's response compared to the baseline firing rate 
using a Mann-Whitney U test

* *AMZstat*: Corresponding U-statistic for the above p-value

* *AMsynchronizationPval*: The best p-value calculated for synchronization of a cell from Rayleigh's 
Test

* *AMsynchronizationZstat*: The corresponding statistic for the p-value from
Rayleigh's test

* *highestSync*: The highest AM rate that was significantly synchronized (p<0.05)

* *highestSyncCorrected*: The highest AM rate that was significantly synchronized after a Bonferroni 
correction

* *highestUSync*: The highest AM rate that is unsynchonized, used if the cell becomes synchonized at 
higher rates, but is not synchronized at lower rates

* *phaseDiscrimAccuracy_{}Hz*: The accuracy of a cell determining the phase of the amplitude 
modulation at a specific rate. There is one value for every rate used

* *rateDiscrimAccuracy*: The accuracy of a cell determining the amplitude modulation rate for a 
trial

## 5. Other/Unused Statistics
Columns not being added to database currently.

* *noiseburst_pVal*: The p-value for comparing the baseline and response firing
rates of the noiseburst paradigm using a Mann-Whitney U test.

* *noiseburst_ZStat*: The corresponding U-statistic for the above p-value

* *noiseburst_baselineSpikeCount*: The baseline noiseburst mean spike count. Baseline period 
was [-100 ms, 0 ms] 

* *noiseburst_responseSpikeCount*: The response noiseburst mean spike count. Response period
was [0 ms, 100 ms] 

* *tuningTest_pVal*: The p-value found from comparing the baseline firing rate of
all frequencies at the maximum intensity to the response using a Mann-Whitney U
test. Baseline period was [-100 ms, 0 ms] and response period was [0 ms, 100 ms]

* *tuningTest_ZStat*: The corresponding U-statistic for the above p-value

* *ttR2Fit*: The R^2 value of the Gaussian fit to the tuning test paradigm.

* *tuningBaseFRBestFreqMaxInt*: The corresponding baseline firing rate for the
frequency that had the largest response firing rate. Baseline period was
[-100 ms, 0 ms]

* *tuningRespFRBestFreqMaxInt*: The firing rate for the best frequency at maximum
intensity. Response period was [0 ms, 100 ms]

* *tuningBestFreqMaxInt*: The frequency that had the highest response firing rate
at the maximum intensity presented

* *fitMidpoint*: The midpoint of the gaussian fit for the tuning curve calculated
 using the square root of the *upperFreq* * *lowerFreq*

* *monotonicityIndex*: This value represents how the response firing rate changed 
with intensity after being normalized by the baseline firing rate. Calculated by 
taking the mean number of spikes at the largest intensity and dividing by the mean 
number of spikes at whichever intensity produced the greatest response.

* *AMBaseFROnset*: The corresponding baseline firing rate for the best onset
response firing rate for a cell. Baseline period was [-100 ms, 0 ms]

* *AMRespFROnset*: The highest onset response firing rate of all the rates 
presented. Onset period was [0 ms, 100 ms]

* *AMBaseFRSustained*: The corresponding baseline firing rate for the best 
sustained response. Baseline period was [-500 ms, -100 ms]

* *AMRespFRSustained*: The highest sustained firing rate of all the rates presented. Sustained 
period was [100 ms, 500 ms]

# C - Figure Contents 
The file `figparams.py` contains common parameters for figures and data related to these figures.

## 1. Frequency Tuning Figure Panels
The following panels are generated in the figure created by `figure_frequency_tuning.py`.

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

## 2. Amplitude Modulated (AM) Figure Panels (Update once script finished)
The following panels are generated in the figure created by `figure_am.py`.

TODO: Add this section once script finished 

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

# D - Other Files
The following files are used for various supplementary functions. Archived versions of various files
can be found in the folder `archive`

## 1. Parameter Files
### studyparams.py
Contains default names and queries used in experiment and analysis

### figparams.py
Contains common parameters for figures and data related to these figures.

## 2. Files in `extras`
### cell_indices_coded.txt
List of all indices for the database of all animals. Each index is formatted as: index,X

X is a value between 1 and 4 that corresponds to type of manual selection, or nothing if none apply:
1. Noise or no cell character
2. Some cell character, but unreliable or noisy
3. No laserpulse or sound response (may be nD1 with no sound response)
4. Laserpulse response, no sound response (may be D1 with no sound response)

### cell_indices_manually_removed.txt
List of indices for cells that should be removed by manual selection. Cell indices come from
any indices with a number code in `cell_indices_coded.txt`.

TODO: Check the following scripts, may not work with updates to database 

### cluster_counts.py (Check Functionality)
Calculate number of clusters by D1 vs nD1, by brain region filters, by tuning filters, etc. Needs a 
database that has calculations for tuningTest paradigms stored (from `extras/tuning_test_comparisons.py`)

### database_cell_locations.py (Check Functionality)
Takes as argument a pandas DataFrame and adds new columns. Computes the depths and cortical 
locations of all cells with suppression indices computed

### figure_cell_sound_responses.py (Check Functionality)
Generates a figure used to explore all aspects of sound responses for the various stimuli we 
presented to the mice. Panels from here may or may not make it into the final paper.

### fix_inforec.py (Check Functionality)
Fix inforec by moving recording track info from 'info' to 'recordingTrack'.
Currently, it only works for files in the format that Matt has where
the info argument is in a different line from the Experiment definition.

### generate_cell_reports.py
This is used to give the researcher the high level overview of the cell responses and the 
characteristic of the neuronal signal on stimulus

Cell reports include the following plots for four sessions:
1. noiseburst: raster, PSTH, ISI, waverform, sparks over time
2. laserpulse: raster, PSTH, ISI, waveform, sparks over time
3. TuningCurve: raster plot(averaged across all intensities), waveform, heatmap
4. Amplitude modulation: raster plot

If run normally, it will use all animals and store the reports in 
`data/cellreports/2019astrpi/all_cells`. It can also be run using the 'SUBJECT' and 'TAG' arguments 
similarly to database_.py scripts.

Requires a dataframe with tuningTest calculations stored as it uses the R2 of the Gaussian from the 
tuning test in a title as a reported value (line 741). This can be generated by 
`extras/tuning_test_comparisons.py`

### merge_clusters_multisession.py
This is used to merge clusters that appear to represent the same cell. 

### normalized_hist_plot_functions.py (Check Functionality)
Contains functions used for plotting normalized histograms for comparisons. One function needs a 
dataframe, the other can use raw data fed to it.

### power_analysis.py (Check Functionality)
A collection of functions for power analysis of data

### sorted_reports.py (Check Functionality)
Using the list of quality spikes (manually picked by Matt Nardoci), this program goes through the 
folder of reports and seperates the reports into two new folders of 'Quality_tuning' and 
'NonQuality_tuning'. It also saves an h5 file that contains all the cell information for each cell 
for later use incase cluster numbers in the database change.

### sound_responses_outside_striatum.py (Check Functionality)
Calculates the total number of cells that respond to sound while outside of the striatum across all 
subjects histology data is known for.

### tuning_test_comparisons.py (Check Functionality)
Calculates some statistics and sound response properties for tuningTest paradigm. The database 
generated from here is needed by: extras/cluster_counts.py