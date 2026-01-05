# Scripts by Ramzy Al-Mulla

## ./general_scripts

* [cell_response_summary.py](./general_scripts/cell_response_summary.py): Load data and create raster plots of multiple sessions from a particular recording site.

* [recursive_trialscomb_test.py](./general_scripts/recursive_trialscomb_test.py):
    * Unit tests for ```beavioranalysis.find_trials_each_combination_n()``` in [jaratoolbox](https://github.com/sjara/jaratoolbox)

* [neuropix_multisort.py](./general_scripts/neuropix_multisort.py):
    * Wrapper script to kilosort multiple neuropixels ephys sessions from the terminal

* [neuropix_sort_multidepth.py](./general_scripts/neuropix_sort_multidepth.py) and [neuropix_sort_multidepth_alt.py](./general_scripts/neuropix_sort_multidepth_alt.py)
    * preliminary versions of [neuropix_multisort.py](./general_scripts/neuropix_multisort.py)

* [test190_eventlocked_lfp.py](./general_scripts/test190_eventlocked_lfp.py): 
    * Modified version of `../santiago/test190_eventlocked_lfp.py`. 
    * Calculates stimulus-evoked local field potentials 

* [test191_filtered_avgLFP.py](./general_scripts/test191_filtered_avgLFP.py): 
    * Modified version of `../santiago/test191_filtered_avgLFP.py`. 
    * Plots averaged LFPs for a neuropixels ephys session (must run [test190_eventlocked_lfp.py](./general_scripts/test190_eventlocked_lfp.py) first!)

* [test193_multiunit_firing_rate.py](./general_scripts/test193_multiunit_firing_rate.py):
    * Modified version of `../santiago/test193_multiunit_firing_rate.py`
    * Extracts and plots mutiunit spiking activity for each channel

* [test194_amplitude_modulated_tones.py](./general_scripts/test194_amplitude_modulated_tones.py)
    * Modified version of `../santiago/test194_amplitude_modulated_tones.py`
    * Preliminary version of `tkparadigms/am_tone_tuning.py`
    * Similar to am_tuning.py, with the addition of amplitude-modulated pure tones

* [sound_PCA_analysis.ipynb](./general_scripts/sound_PCA_analysis.ipynb):
    * python notebook for exploring use of PCA to analysis 

## ./hemisym_preliminary_testing
**NOTE**: everything in hemisym_preliminary_testing is a retired version of the scripts in [2025hemisym](./2025hemisym/README.md)

* [database_laser_analysis.py (preliminary version)](./hemisym_preliminary_testing/database_laser_analysis.py): 
    * generates cell databases for a particular subject with 'optoTuningAMtone' and 'optoTuningFreq' with analyses of single unit spiking activity (takes 2~8 minutes per mouse depending on the number of cells)

* [figure_optoAMtone_freqtuning.py](./hemisym_preliminary_testing/figure_optoAMtone_freqtuning.py):
    * generates summary figure for an individual mouse/session

* [figure_compare_freqtuning.py](./hemisym_preliminary_testing/figure_compare_freqtuning.py):
    * generates summary figure comparing the pooled data for each of the two study groups

* [figure_sessions_compare_freqtuning.py](./hemisym_preliminary_testing/figure_sessions_compare_freqtuning.py):
    * same as [figure_compare_freqtuning.py](./hemisym_preliminary_testing/figure_compare_freqtuning.py), but overlays with summary statistics for each individual recording session

* [figure_compare_optoSham.py](./hemisym_preliminary_testing/figure_compare_optoSham.py):
    * same as [figure_compare_freqtuning.py](./hemisym_preliminary_testing/figure_compare_freqtuning.py), but does it for the sham control sessions
    * for [2025hemisym](./2025hemisym/README.md), this is baked into [figure_sessions_comparison.py](./2025hemisym/figure_sessions_comparison.py)

## ./minidisplay_related

* [minidisplayer.py](./minidisplay_related/minidisplayer.py): 
    * basic demonstration of minidisplay controls (requires pygame-ce and screeninfo modules!)

    * Install dependencies ```pip install pygame-ce``` and ```pip install screeninfo```

* [imagesoundclient.py](./minidisplay_related/imagesoundclient.py):
    * beta version of [taskontrol plugin](https://github.com/sjara/taskontrol/tree/master/taskontrol/plugins) for projecting images on the minidisplay during sound presentation

* [image_sound_v2.py](./minidisplay_related/image_sound_v2.py):
    * beta version of [tkparadigms.am_image_tuning.py](https://github.com/sjara/tkparadigms/tree/master/tkparadigms/am_image_tuning.py) for running paradigms using [imagesoundclient.py](./minidisplay_related/imagesoundclient.py)

* [poni_hemisym/](./minidisplay_related/poni_hemisym/):
    * scripts for analyses and figures similar to [hemisym_preliminary_testing/](./hemisym_preliminary_testing/), but with image presentation instead of normal laser
