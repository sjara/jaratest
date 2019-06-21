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

# Figure 1 (Characterisation of responses)
## Panel a
This panel has a cartoon of the sound stimuli used during recordings, created in Inkscape
## Panel b
