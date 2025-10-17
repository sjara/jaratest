# Scripts by Lizeth
* `old`: Tested some functions but those weren't finished.
* `process_ephys_data`: Codes related to the processing of electrophysiology data.

    * `test01_load_neuropix_onecell.py`: Load neuropixels data and show raster plots for one cell.
    * `test02_load_neuropix_ensemble.py`: Load neuropixels data and show raster plots for all the cells.
* `widefield`: Scripts used for widefield project.

    * `dynamics01.py`: Analysis of the change in activity over time for 1 session in a specific area of pixels.
    * `lizeth_utils.py`: Contains functions to process the widefield data and save it.
    * `load_images.py`: This code can be used to copy the different widefield recording sessions from all the mice. (We don't want to plot the change in activity with this code because it takes longer)
    * `multiple_sessions_one_mouse.py`: Last version. It plots the signal change per frequency, per mouse, for multiple sessions.
    * `odd_even_trials.py`: It uses the function on lizeth_utils.py to show how the change in the signal looks like for odd and even trials.
    * `one_session_analysis.py`: Analysis of one single session. It allows to see evoked, baseline and signal change.
    * `signal_thresholded.py`: Plots the change in the signal with different color per frequency and the signal thresholded.
    * `wifi008_info_widefield.py`: First version of possible info file for widefield recording sessions.                                             

