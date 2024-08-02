# Neural activity trajectories in response to natural sounds

This study uses the data obtained from the Auditory cortex of a head-fixed mouse while it was presented with multiple 
instances of natural sounds of different categories (recored with Neuropixel version 1). We will use dimensionality 
reduction on the population activity and measure the distance between the trajectories as a function of time.

## Scripts

1. **allRasters_feat017.py**:
   - Generates a raster plot for select 28 cells for feat017 on naturalSound presentation.

2. **feat015_additional_session.py**:
   - Loads multiple sessions in the celldb for feat015 and generates a raster plot for selected cells on naturalSound
   presentation.

3. **load_neuropix_ensemble.py**:
   - Generates rasters (with trials sorted by stimulus type) for a subset of cells from an ensemble for feat015 and 
   counts the number of spikes for each cell in a particular time period

4. **load_neuropix_test.py**:
   - An extension of load_neuropix notebook that uses extraplots to generate raster plot for AM sound

5. **neural_trajectory.py**:
   - Computes firing rates for each neuron in an ensemble and generates raster plots followed by a neural trajectory 
   for two selected neurons

6. **save_all_rasters_pdf.py**:
   - For a subject, generates raster plots for all the cells; 28 rasters per page for each experiment and saves them in
   a pdf file

7. **spike_count.py**:
   - Computes & prints spike count for each cell in an ensemble for trials where a select stimulus (naturalSound) was 
   presented

8. **test161_raster_natural_sounds.py**:
   - Test script that generates raster plots for selected cells of a specific session on feat015

## Usage

Each script is designed to perform a specific task within the project. To run a script, use the following command:

```sh
python script_name.py
