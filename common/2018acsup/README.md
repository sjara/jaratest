# Producing databases
## `database_generation_workflow.py`
This script will generate the databases used (cells from ChR2 mice and cells from Arch mice). You can run this script from an iPython terminal with the appropriate argument for the database you want (0 for ChR2 mice, 1 for ArchT mice), and it will perform all the steps required to create one complete database from the raw data and inforec. This script can also be used as a guide of what functions to use to make specific changes to your database.

This script uses the following modules (which can be used outside this script as well):

## `cluster_ephys_data.py`
Contains two functions. One (cluster_spike_data) takes a list of subject names and saves clustered data (.clu files) using the Klustakwik algorithm. The second (cluster_rescue) takes a database and a desired ISI threshold, then prunes clusters that do not pass the ISI criterion by removing spikes furthest from the centroid until the cluster passes the ISI threshold. This function also saves new .clu files for these modified clusters, but does not overwrite the original .clu files.

## `database_photoidentification.py`
This contains three functions that add various columns to an existing database.

photoID_base_stats loops through each cluster passing an ISI and spike quality threshold and computes statistics that will be later used to select specific cells for our study. Because these stats are used in filtering cells by their responses, they must be calculated for each cluster. Example stats include laser responsiveness, sound responsiveness, and preferred frequency.

photoID_indices loops through each cluster passing some criteria based on the base stats and calculates more complex stats, such as suppresion index and model fit. The criteria used here are less strict that those used in the final study, in case we want to relax our standards in the future without having to remake the database.

photoDB_cell_locations loops through each cluster that has had indices calculated for it and calculates the anatomical location and depth of each cell. This portion relies on allensdk for finding the anatomical locations of cells, so needs to be run in a virtual environment. This phase requires a tracks file for each subject, and histology images that have been aligned to the Allen atlas with the recording track marked.

## `database_inactivation.py`
This produces a database of cells from Arch mice for our inactivation experiments.
This takes as input a database and for every cell calculates stats such as sound response and preferred frequency. For cells passing certain criteria, change in suppression stats are also calculated.

## `database_generation_funcs.py`
Contains functions called during database generation.

## `database_bandwidth_tuning_fit_funcs.py`
Contains functions called during database generation. Yashar's functions for modeling sound responses. Quarantined because Yashar made them and they're special.

# Database contents
## Generic database
This is the database initially produced by celldatabase.generate_cell_database_from_subjects. It contains the following columns:

* *behavSuffix*: the suffixes for the behaviour files associated with the sessions this cell is from
* *brainArea*: which part of the brain this cell is from

## Base stats
These are the columns added to the generic database after calculation of base stats:

### Common
These columns appear for both the photoidentification and inactivation database:

* *bestBandSession*: the index of the bandwidth session  whose centre frequency was closest to this cell's preferred frequency (useful when multiple bandwidth sessions were recorded at one site).
* *gaussFit*: the parameters of the Gaussian curve that best fits this cell's frequency tuning curve. The parameters are (in order as saved in the database): mean, amplitude, standard deviation, offset.
* *tuningTimeRange*: the time range over which the cell's pure tone responses are analysed to calculate a tuning curve.
* *tuningFitR2*: the R^2 value of the Gaussian curve fit to this cell's frequency tuning.
* *prefFreq*: this cell's estimated preferred frequency, calculated from the location of the peak of the Gaussian curve fit to this cell's tuning data.
* *octavesFromPrefFreq*: the difference (in octaves) between this cell's estimated preferred frequency (*prefFreq*) and the centre frequency used during the bandwidth trials.
* *soundResponseUStat*: the test statistic obtained when testing for significance between baseline firing rate and sound-induced firing rate for any combination of parameters during the bandwidth session. The time ranges used (in seconds from sound onset) were -1.2 to -0.2 for baseline and 0.0 to 1.0 for sound.
* *soundResponsePVal*: the resulting p value of the test for significant differences in firing rate between baseline firing and sound-induced firing. The test statistic is stored in *soundResponseUStat*.
* *onsetSoundResponseUStat*: as *soundResponseUStat*, but looking at sound onset. The time ranges used (in seconds from sound onset), were -0.25 to -0.2 for baseline and 0.0 to 0.05 for sound.
* *onsetSoundResponsePVal*: the resulting p value of the test for significant differences in firing rate between baseline firing and firing at sound onset. The test statistic is stored in *onsetSoundResponsePVal*.
* *sustainedSoundResponseUStat*: as *soundResponseUStat*, but looking at sustained sound response. The time ranges used (in seconds from sound onset), were -1.0 to -0.2 for baseline and 0.2 to 1.0 for sound.
* *sustainedSoundResponsePVal*: the resulting p value of the test for significant differences in firing rate between baseline firing and sustained sound-induced firing. The test statistic is stored in *sustainedSoundResponseUStat*.
* *laserUStat*: the test statistic obtained when testing for significance between baseline firing rate and laser-induced firing rate. The time ranges used (in seconds from laser onset) were (for photoID) -0.05 to -0.04 for baseline and 0.0 to 0.01 for laser, and (for inactivation) -0.3 to -0.2 for baseline and 0.0 to 0.1 for laser.
* *laserPVal*: the resulting p value of the test for significant differences in firing rate between baseline firing and laser-induced firing. The test statistic is stored in *laserUStat*.

### PhotoID
These columns only appear in the photoidentification database:

* *AMRate*: the amplitude modulation rate used during the bandwidth session for this cell.
* *laserChangeFR*: the difference in firing rate (in spikes/second) between the spontaneous firing rate and the laser firing rate. Positive values mean the laser evoked a positive change in firing rate.
* *spikeWidth*: the average difference in time between the sodium peak and potassium peak. 

### Inactivation
These columns only appear in the inactivation database:

* *controlSession*: 0 for cells inactivated normally, 1 for cells in the control condition (laser on, not directed at AC)
* *baselineFRnoLaser*: spontaneous firing rate without laser during bandwidth session. The time range used was (in seconds from sound onset) -0.05 to 0.0, since laser turns on 100ms before sound.
* *baselineFRLaser*: spontaneous firing rate with laser during bandwidth session. The time range used was (in seconds from sound onset) -0.05 to 0.0, since laser turns on 100ms before sound. First 50ms of laser are excluded to remove effects of laser onset.
* *baselineChangeFR*: change in spontaneous firing rate between the laser and no laser condition. Difference between *baselineFRLaser* and *baselineFRnoLaser*.

## Indices
These are the columns added to the database only for cells passing certain criteria in their base stats. The criteria set during database creation are more generous than those used in the final study, to allow us to relax them if needed without regenerating the database.

### PhotoID
These columns appear in the photoidentification database:

* *R0*, *RD*, *RS*, *m*, *sigmaD*, *sigmaS*: the parameters of the Carandini fit used to model this cell's bandwidth tuning curve. Different versions of these columns exist for different methods of calculating the tuning curve (e.g. *R0noZero*).
* *bandwidthTuningR2*: the R^2 value of the Carandini model fit to the bandwidth tuning data.
* *fitSustainedSuppressionIndex*: the suppression index, the normalised ratio between the peak response and white noise response, calculated using predicted firing rates from the model fit.
* *fitSustainedPrefBandwidth*: the bandwidth eliciting the highest firing rate in this cell, estimated using the predicted firing rates from the model fit.

### Inactivation
The columns in the photoidentification database also appear here, though split by laser and no laser trials (e.g. *fitSustainedSuppressionIndexLaser* and *fitSustainedSuppressionIndexNoLaser*).

These columns only appear in the inactivation database:

* *laserChangeResponse*: the change in the sustained sound response (200-1000 ms after sound onset) during the bandwidth session with laser presentation. Calculated as the sound response with laser minus the control sound response, averaged over all bandwidths.
* *fitPeakChangeFR*: the change in peak firing rate during the bandwidth session with laser presentation. Calculated as the model-estimated peak firing rate in the control condition subtracted from the firing rate at the same bandwidth in the laser condition.
* *fitWNChangeFR*: like *fitPeakChangeFR*, but for the white noise response instead of the peak response.

# Figures
All figures require access to the databases (`photoidentification_cells.h5` and `inactivation_cells.h5`), the clustered ephys data, and the behaviour data.

## Figure 1 (Photoidentification method)
This figure is produced by running `figure_photoID_method.py`.

### Panel A,D
These panels have a cartoon of a circuit consisting of an Excitatory, PV, and SOM cell, and showing the laser and recording electrode, created in Inkscape.
### Panel G
This panel has an example histology image with boundaries between auditory areas drawn in Inkscape. The image is `band055_outlines.jpg`, located on jarahub in data/figuresdata/2018acsup/supplement_figure_histology.
### All other panels
These panels are generated by the figure script using data generated by `supplement_generate_photoidentification.py`.

## Figure 2 (Characterisation of bandwidth tuning)
This figure is produced by running `figure_example_characterisation.py`.

### Panel A,B
These panels have cartoons of the recording setup and the sound stimuli used, created in Inkscape.
### Panel C,D,E
These panels show example responses of an excitatory, PV, and SOM cell. The data is generated by `generate_example_photoidentified_cells.py`.
### Panel F,G
These panels summarise the suppression and preferred bandwidth seen in excitatory, PV, and SOM cells. The data is generated by `generate_PV_SOM_Ex_aggregate_stats.py`.

## Figure 3 (Frequency tuning)
This figure is produced by running `figure_frequency_tuning.py`.

### Panel A,B
These panels show the frequency tuning of an example excitatory cell. The data is generated by `supplement_generate_example_frequency_tuning.py`.
### Panel C
This panel shows suppression as a function of significance of pure tone suppression. The data is generated by `supplement_generate_stats_by_tone_suppression.py`.

## Figure 4 (SI controls)
This figure is produced by running `figure_SI_controls.py`.

### Panel A
This panel shows suppression as a function of preferred frequency. The data is generated by `supplement_generate_stats_by_centre_freq.py`.
### Panel B
This panel shows suppression as a function of AM rate. The data is generated by `supplement_generate_stats_by_AM_rate.py`
### Panel C
This panel shows suppression as a function of intensity index. The data is generated by `supplement_generate_intensity_tuning.py`.

## Figure 5 (Differences in PV and SOM responses)
This figure is produced by running `figure_PV_SOM_comparison.py`.

### Panel A,B,C
These panels show the differences in firing rate at different time periods for PV and SOM cells. The data is generated by `generate_PV_SOM_Ex_aggregate_stats.py`.

## Figure 6 (Inactivation controls)
This figure is produced by running `figure_inactivation_controls.py`.

### Panel A,E
These panels have a cartoon of a circuit consisting of an Excitatory, PV, and SOM cell, and showing the laser and recording electrode, created in Inkscape.
### Panel B,F
These panels show example cells inactivated by laser presentation. The data is generated by `supplement_generate_cells_suppressed_by_ArchT.py`.
### Panel C,G
These panels show the onset and sustained laser responses of all sound-responsive cells. The data is generated by `supplement_generate_cells_suppressed_by_ArchT.py`.
### Panel D,H
These panels show the laser-induced changes in firing rate of all sound responsive cells in the experimental and control conditions. The data is generated by `supplement_generate_control_inactivation_stats.py`.

## Figure 7 (Effect of PV/SOM inactivation on suppression)
This figure is produced by running `figure_inactivation.py`.

### Panel A,B,C,D
These panels show responses of example exctatory cells with and without PV or SOM inactivation. The data is generated by `generate_example_inactivation_cells.py`.
### Panel E,F
These panels show summaries of the changes in suppression seen with PV and SOM inactivation. The data is generated by `generate_inactivation_aggregate_stats.py`.
