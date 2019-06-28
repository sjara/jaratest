README file contains instructions for processing data and generating figures
#Here is the readme place we will place codes for the paper

# Producing a database

## databasename.h5
### database_generation.py
This script will generate the database that's concatenated with all subjects defined as d1pimouse in studyparams.py. At First, it will generate the concatenated database, then calculate_base_stats will be called to run statistics testing to filter cells that we considered to have a good signal(ISI<0.02 and SpikeQuality >2), and to create the parameters that will be used in data analysis in further study, such as p-Values, R squared and frequency parameters(BW10 and intensity threshold). Next calculate_indices will be called to filter the cells with the statistically valid fitting models by using R squared value that's calculated from calculate_base_stats. Lastly, if the researcher desires, it will save the database to the local machine

This script uses following module:
### database_generation_funcs.py
Contains functions called during database generation.

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


# Exploring Data to produce stats and reports
### extras/generate_allCell_reports.py
This script generates reports for all cells belong to the given subject. The reports contain plots for noiseburst(raster,PSTH,ISI,waveform, spark rate over time), laserpulse(raster,PSTH,ISI,waveform, spark rate over time), tuningCurve(raster (for one intensity), waveform). This is used to give the researcher the high level overview of the cell responses and the characteristic of the neuronal signal on stimulus
