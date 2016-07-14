
from jaratoolbox.test.nick.ephysExperiments import ephys_experiment_v2 as ee
from pylab import *
reload(ee)


ex = ee.EphysExperiment('pinp003', '2015-07-06')

#ex.plot_session_raster('2015-07-06_11-15-56', 3)


bdata = ex.get_session_behav_data('2015-07-06_11-25-58', 'a')

freqEachTrial = bdata['currentFreq']
intensityEachTrial = bdata['currentIntensity']

#ex.plot_session_raster('2015-07-06_11-25-58', 3, sortArray = freqEachTrial)
#ex.plot_session_raster('2015-07-06_11-25-58', 3)

ex.plot_array_raster('2015-07-06_11-25-58')
