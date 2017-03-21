from jaratoolbox import ephysinterface
import matplotlib.pyplot as plt
from jaratest.nick.database import dataplotter

experiments=[3,4,5,7,9,10,13,15] #Change this to include all experiments with different depths
tetrode = 8 #Change this to plot different tetrodes
ei = ephysinterface.EphysInterface('/home/jarauser/data/inforec/gosi008/gosi008_inforec.py') #Change this to plot for different mouse

for ind,experiment in enumerate(experiments):
	sessionObj = ei.get_session_obj(-2, experiment, 0)
        sessionDir = sessionObj.ephys_dir()
        behavFile = sessionObj.behav_filename()
	spikeData= ei.loader.get_session_spikes(sessionDir, tetrode)
        eventData = ei.loader.get_session_events(sessionDir)
        eventOnsetTimes = ei.loader.get_event_onset_times(eventData)
        spikeTimestamps=spikeData.timestamps
	bdata = ei.loader.get_session_behavior(behavFile)
        sortArray = bdata['currentFreq']
	plt.subplot(2,4,ind+1) #Change this to make more or fewer plots. First number=rows, second number=columns
	dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray = sortArray, timeRange=[-0.1,0.3])
	plt.title(sessionDir)
plt.show()

print experiments

