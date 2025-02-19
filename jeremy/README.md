Test code by Jeremy Guenza-Marcus

* `example_load_traces.py`: Example from Santiago showing how to read raw Neuropixels traces and events data.

* `jeremy_load_LFP.py`: Loads the raw LFP data. Displays a heatmap of a subset of LFP data. x-axis is time from sample 0 to sample 1000. y-axis is channel index. Intensity is proportional to electric potential.

* `jeremy_preprocess_for_CSD.py`: Load in raw LFP data. Create an uncollapsed PSTH of all stimulus types given an elapsed time before and after stimuli. Then creates a figure of one stimulus type and then a grid of all stimuli types with at most 4 columns.

* `jeremy_csd.py`: Load in raw LFP data. Create an uncollapsed PSTH of all stimulus types given an elapsed time before and after stimuli. Calculates a kCSD of N=10 channels on a single column for all stimuli types as calculated previously. Displays this in a 4 column subplot figure as done in jeremy_preprocess_for_CSD.py.

* `jeremy_psth.py`: All functions relevant to PSTH creation to be called when running the CSD analysis pipeline.

* `jeremy_utils.py`: All functions that do not clearly belong in PSTH creation which are to be placed into another .py file until further categorization.