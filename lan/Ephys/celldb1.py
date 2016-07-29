from jaratoolbox.test.nick.ephysExperiments import recordingday as rd
reload(rd)

exp0701 = rd.RecordingDay(animalName = 'd1pi001', date = '2015-07-01', experimenter = 'lan')

site3 = exp0701.add_site(depth = 2710, goodTetrodes = [6])

s3NB = site3.add_session('19-09-42', None, 'NoiseBurst')
s3LP = site1.add_session('19-13-36', None, 'LaserPulse')
s3LT = site1.add_session('19-16-32', None, 'LaserTrain')
s3TC = site1.add_session('19-30-41', 'c', 'TuningCurve')
#s3BF = site1.add_session('15-45-22', 'b', 'BestFreq')

cluster4 = site3.add_cluster(4, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
cluster6 = site3.add_cluster(6, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments = 'good cell')
cluster10 = site3.add_cluster(10, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='good cell')
cluster12 = site3.add_cluster(12, soundResponsive=True, laserPulseResponse=True,followsLaserTrain=True, comments='inhibited by laser')



cluster4 = site1.add_cluster(7, soundResponsive=True, comments='sound responsive only')


cellDB = rd.JSONCellDB('/tmp/celldb1.json')
cellDB.add_clusters([cluster1, cluster2, cluster3, cluster4])
cellDB.write_database()
