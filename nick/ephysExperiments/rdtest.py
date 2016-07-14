from jaratoolbox.test.nick.ephysExperiments import recordingday as rd
reload(rd)

today = rd.Recording(animalName = 'pinp003',
                     date = '2015-06-24',
                     experimenter = 'nick',
                     paradigm='laser_tuning_curve')

site1 = today.add_site(depth = 3543, goodTetrodes = [6])

s1NB = site1.add_session('15-22-29', None, 'NoiseBurst')
s1NB.set_plot_type('raster', report='main')

s1LP = site1.add_session('15-25-08', None, 'LaserPulse')
s1LP.set_plot_type('raster', report='main')

s1LT = site1.add_session('15-27-37', None, 'LaserTrain')
s1LT.set_plot_type('raster', report='main')

s1TC = site1.add_session('15-31-48', 'a', 'TuningCurve')
s1TC.set_plot_type('tc_heatmap', report='main')

s1BF = site1.add_session('15-45-22', 'b', 'BestFreq')
s1BF.set_plot_type('raster', report='main')


#site1.generate_main_report(show=False, save=False, saveClusterReport=False)

site2 = today.add_site(depth = 3600, goodTetrodes = [4, 5, 6])
s2NB = site2.add_session('16-00-00', None, 'NoiseBurst')
s2LP = site2.add_session('16-00-01', None, 'LaserPulse')
s2LT = site2.add_session('16-00-02', None, 'LaserTrain')

#site2.generate_main_report(show=False, save=False, saveClusterReport=False)


site1.add_cluster(clusterNumber=2, tetrode=6, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='good cell')
site1.add_cluster(clusterNumber=5, tetrode=6, soundResponsive=True, laserPulseResponse=True, comments='probably synaptic') 
site1.add_cluster(clusterNumber=5, tetrode=6, soundResponsive=True, laserPulseResponse=True, comments='probably synaptic') #A repeat cluster
site1.add_cluster(clusterNumber=7, tetrode=6, soundResponsive=True, comments='sound responsive only')

site2.add_cluster(clusterNumber=2, tetrode=6, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='good cell')
site2.add_cluster(clusterNumber=5, tetrode=6, soundResponsive=True, laserPulseResponse=True, comments='probably synaptic')

cellDB = rd.JSONCellDB('/tmp/celldb2.json')
cellDB.add_clusters(site1.clusterList)
cellDB.add_clusters(site2.clusterList)
cellDB.write_database()


