# Danny's Scripts
This folder contains Danny's scripts for working with FaceMap-generated traces
of pupil area, and other mouse behaviors.

* comparisonplots.py: Produces a plot of pupil area, averaged across
trials that are locked to played sounds.  The trials are plotted by
condition, such that sound change trials are grouped into identical frequencies.
* comparisonplots_20sec.py: Produces a plot of pupil area, averaged across
trials that are locked to played sounds.  This plot also generates a plot of
running behavior, over the same trials.
* comparisonplots_forLightTests.py: Produces plots of pupil area and running
behavior, averaged across trials that are locked to played sounds.  The trials
can be broken out into various light settings (set manually), using the 'breakout'
feature.  'limitrunning' allows the user to limit to only trials in which running
behavior is below a numerical threshold at a given time before sound is played,
set in 'runThreshold' and 'runThresholdTime', respectively. Raw plots of pupil
area and running behavior across the entire session are also produced, with
vertical indicators of the sync light timing, when breakout = 0.
* facemapanalysis.py: Module for loading and preprocessing FaceMap data.
The module loads processed FaceMap data, and generates traces of pupil
area, experiment synchronization light, and mouse behaviors such as
whisking and running.
