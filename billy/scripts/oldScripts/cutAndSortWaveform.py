'''

'''
from pylab import *
from jaratoolbox import waveformcutter
reload(waveformcutter)



animalName   = 'test089'
ephysSession = '2015-07-31_14-40-40'
tetrode = 5
wc = waveformcutter.WaveformCutterSession(animalName,ephysSession,tetrode)
cluster = 7 #STARTING FROM 0

#wc.add_cluster() #add cluster to look at (NO LONGER NEED)
wc.set_active_cluster(cluster)

wc.set_channel(0) #choose which channel to cut with

#wc.plot_waveforms(200) #plot all waveforms before cutting on set channel (NO LONGER NEED)



clf()

wc.plot_cluster_waveforms(cluster,200) #plot cluster waveforms (cluster #, # of waveforms to plot) (USE CLUSTER # MINUS 1, STARTS FROM CLUSTER 0)

show()

#wc.add_bound(0) #click for boundaries (NO LONGER NEED)

#wc.select_bound()

#wc.show_report_onecluster()
