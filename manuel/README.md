# Manuel's scripts
*Here you will find the most used files*
- extracting_time_windows.py: Code that shows how to obtain the corresponding pupil area data within an arbitrary defined time window (in seconds) and plot it in a pupil dilation study for rodents.
- pAreaAverage_BarPlots.py: Code that shows how to obtain avarage pupil size for a stimulus and create a bar plot.
- pupilDilationPlots.py: code to obtain mean pupil area and plot it in slope and bar plots vs conditions of the stimulus.  
- functionsTest.py: file to test functions that will be used for the project.
- comparisonPupilPlotsPureXXX.py: code to plot data from 2 videofiles at the same time (draft)
- mp4ComparisonPlotsMp4PureXXX.py: works just as "comparisonPupilPlotsPureXXX.py" but with .mp4 files

## testFiles directory
*Here you will find test files*
- check_facemap_rois_dtype.py: contains a function to find any given item from a dictionary within the output "proc" file generated from the Facemap videos.
- facemap_shareaxis_plotting.py: shows how to share axis with matplotlib.pyplot. In this case, the data from the output "proc" file from Facemap was used.
-  how_to_plot1.py: code to plot the following plot https://matplotlib.org/stable/_images/sphx_glr_simple_plot_001.png
-  how_to_plot2.py: code to plot the following plot https://matplotlib.org/stable/_images/sphx_glr_subplot_001.png
-  list_of_variables.py: contains the expected variables from the "proc" file and what should they contain.
-  plotting_8_figures.py: how to plot 8 consecutive figures (each one with 2 subplots) with matplotlib.pyplot. The data used was from the output "proc" file from Facemap.
-  plotting_with_time_axis.py: code that shows how to obtain the time of a video so it can be plotted in the X axis with a matplotlib.pyplot plot against the pupil area of a rodent (or any other given stimulus). The data used comes from a "proc" file as well. This is only a draft.
-  plotting_with_time_axis_2.py: this code shows how a plot about pupil dilation vs time should look like in a pupil dilation study with rodents.
-  testingScripts.py: this code has nothing important. Its intended use is to try and play with commands related to plot creation, data slicing, indexing, or any other strategy to obtain desired results.
-  test_plot_with_axis.py: this code contains a draft to play with plots creation, axis sharing, etc. Nothing important is contained in here.
-  - pupil_change_onsetStimulus.py: Code that shows how to obtain the onset values for a stimulus.
