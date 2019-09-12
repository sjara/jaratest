#Here is the readme place we will place codes for the paper

# Producing a database

## databasename.h5
### database_generation.py
This script will generate the database that's concatenated with all subjects defined as d1pimouse in studyparams.py. 
At first, it will generate the concatenated database, then calculate_base_stats will be called to run statistics 
testing to filter cells that we considered to have a good signal(ISI<0.02 and SpikeQuality >2), and to create the 
parameters that will be used in data analysis in further study, such as p-Values, R squared and 
frequency parameters(BW10 and intensity threshold). Next calculate_indices will be called to filter the cells with 
the statistically valid fitting models by using R squared value that's calculated from calculate_base_stats. Lastly, 
if the researcher desires, it will save the database to the local machine

This script uses following module:
### database_generation_funcs.py
Contains functions called during database generation.

# Database contents
## Generic database
This is the database initially produced by celldatabase.generate_cell_database_from_subjects(). 
The columns produced by this database can be found in the documentation for celldatabase.

## Base stats
These are the columns added to the generic database after calculation of base stats. They are grouped by their use in figures:

### Tuning curve heatmap
* *None*

### Bandwidth 10 above minimum intensity
* *upperFreq*: The highest frequency with a response 10 dB SPL above the sound intensity threshold. Calculated by 
database_generation_funcs.calculate_BW10_params.
* *lowerFreq*: The lowest frequency with a response 10 dB SPL above the sound intensity threshold. Calculated by 
database_generation_funcs.calculate_BW10_params.
* *RsquaredFit*: The mean of all of the r<sup>2</sup> values of the 10 dB SPL above the sound intensity 
threshold. Calculated by database_generation_funcs.calculate_BW10_params.
* *cf*: The characteristic frequency for peak firing rate at a given intensity. Found using the frequency index from
database_generation_funcs.calculate_intensity_threshold_and_CF_indices and indexing the unique frequencies (uniqFreq) 
for a session.
* *bw10*: The bandwidth 10 above the sound intenisty threshold. Calculated by the (*upperFreq* - *lowerFreq*) / *cf*
* *fitMidpoint*: The midpoint of the gaussian fit for the tuning curve calculated using the square root of the
*upperFreq* * *lowerFreq*

### Intensity Threshold
* *thresholfFRA*: The characteristic intensity for peak firing rate. Found using the intensity index from
database_generation_funcs.calculate_intensity_threshold_and_CF_indices and indexing the unique intensities (uniqueIntensity)
for a session.

### Latency
* *latency*: The time (in seconds) from when the stimulus is presented until the cell shows a response. Calculated using
database_generation_funcs.calculate_latency(). This looks at the *cf* on the tuning curve. Using a time range of 100 ms
before the stimulus it establishes a baseline firing rate. The value is then pulled by looking for where a PSTH of the curve crosses a
specific fraction of the maximum fire rate the cell reaches.

### Onset to sustained ratio
* *onsetRate*: The firing rate within the first 50 ms of the response as based on *latency*.
Calculated by database_generation_funcs.calculate_onset_to_sustained_ratio.
* *sustainedRate*: The number of spikes over time that occur 100 ms after the response as based on *latency*.
Calculated by database_generation_funcs.calculate_onset_to_sustained_ratio.
* *baseRate*: The number of spikes over time the occur from 100 ms before the stimulus to 50 ms before the
stimulus is presented. Calculated by database_generation_funcs.calculate_onset_to_sustained_ratio.
* *cfOnsetivityIndex*: The ratio of the difference between onset to sustained spike rates calculated by: 
(*onsetRate* - *sustainedRate*) / (*sustainedRate* + *onsetRate*) A positive number means there were more spikes at the
onset of the response than there were in the sustained.

### Monotonicity index
* *monotonicityIndex*: This value represents how the response firing rate changed with intensity after being normalized by the
baseline firing rate. Calculated by taking the mean number of spikes at the largest intensity and dividing by the mean number
of spikes at whichever intensity produced the greatest response.

# Defining parameters for names and paths for study and figures
### studyparams.py
### figureparams.py

# Figure 1 (Frequency)
## Figure script: `figure_frequency_characterization.py`
**Requires**:
`data_freq_tuning_examples.npz`
Produced by:
`generate_example_freq_tuning.py`

`{celldatabase_name}.h5` >> DB name to be determined

## Panels A, B
These panels are produced by the figure script `figure_frequency_characterization.py`.
To get tuning curve data, it requires `data_freq_tuning_examples.npz` which is produced by `generate_example_freq_tuning.py`

## Panels C, D
These panels are produced by the script `figure_frequency_characterization.py`

## Panel E
This panel data is generated by `generate_latency.py` as it adds the 'latency' column to the database. This panel is contained
in the script `figure_frequency_characterization.py`

## Panel F
MIA

## Panel G
This panel data is generated by `generate_monotonicity_index.py` as it adds the monotonicity index column to the database.
This calculation is done through dividing the average intensity by the max intensity for each cell. The panel is contained
in the script `figure_frequency_characterization.py`

# Exploring Data to produce stats and reports
### extras/generate_allCell_reports.py
This script generates reports for all cells belong to the given subject. The reports contain plots for 
noiseburst(raster,PSTH,ISI,waveform, spark rate over time), laserpulse(raster,PSTH,ISI,waveform, spark rate over time), 
tuningCurve(raster (for one intensity), waveform). This is used to give the researcher the high level overview of the cell 
responses and the characteristic of the neuronal signal on stimulus
