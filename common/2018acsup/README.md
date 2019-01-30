# Producing databases
## `database_generation_workflow.py`
This script will generate both databases used (cells from ChR2 mice and cells from Arch mice). It runs the following within:
## `database_generic.py`
This takes as input a list of mice and produces a generic database containing only basic stats like ISI and spike shape.
## `database_photoidentification.py`
This produces a database of cells from ChR2 mice for our photoidentification experiments.
This takes as input a database and for every cell calculates stats such as laser response, sound response, and preferred frequency. For cells passing certain criteria, suppression stats are also calculated.
## `database_inactivation.py`
This produces a database of cells from Arch mice for our inactivation experiments.
This takes as input a database and for every cell calculates stats such as sound response and preferred frequency. For cells passing certain criteria, change in suppression stats are also calculated.
## `database_generation_funcs.py`
Contains functions called during database generation.
## `database_bandwidth_tuning_fit_funcs.py`
Contains functions called during database generation. Yashar's functions for modeling sound responses.

# Figure 1 (Characterisation of responses)
## Panel a
This panel has a cartoon of the sound stimuli used during recordings, created in Inkscape
## Panel b
