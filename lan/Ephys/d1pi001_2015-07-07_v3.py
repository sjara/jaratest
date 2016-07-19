#Write into JSON database only cells with good amp (>=40uV), consistent firing throughout recording, good waveform, with either sound or laser response or both.

from jaratoolbox.test.nick.ephysExperiments import recordingday as rd
reload(rd)


sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse'}
 
exp0707 = rd.Recording(animalName = 'd1pi001', date = '2015-07-07', experimenter = 'lan', paradigm='laser_tuning_curve')

site1 = exp0707.add_site(depth = 2750, goodTetrodes = [3])
site1.add_session('14-10-13', None, sessionTypes['nb'])
site1.add_session('14-11-42', None, sessionTypes['lp'])
site1.add_session('14-14-00', None, sessionTypes['lt'])
site1.add_session('14-17-54', 'a', sessionTypes['tc'])

site2 = exp0707.add_site(depth = 2900, goodTetrodes = [3])
site2.add_session('15-12-17', None, sessionTypes['nb'])
site2.add_session('15-14-12', None, sessionTypes['lp'])
site2.add_session('15-16-18', None, sessionTypes['lt'])
site2.add_session('15-18-44', 'b', sessionTypes['tc'])

site3 = exp0707.add_site(depth = 3025, goodTetrodes = [3, 6])
site3.add_session('16-04-26', None, sessionTypes['nb'])
site3.add_session('16-06-32', None, sessionTypes['lp'])
site3.add_session('16-08-28', None, sessionTypes['lt'])
site3.add_session('16-12-41', 'c', sessionTypes['tc'])
cluster5 = site3.add_cluster(clusterNumber=5, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
cluster4 = site3.add_cluster(clusterNumber=4, tetrode=6, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')


site4 = exp0707.add_site(depth = 3075, goodTetrodes = [3, 6])
site4.add_session('16-34-24', None, sessionTypes['nb'])
site4.add_session('16-36-42', None, sessionTypes['lp'])
site4.add_session('16-38-59', None, sessionTypes['lt'])
site4.add_session('16-42-17', 'd', sessionTypes['tc'])
site4.add_session('16-55-51', None, sessionTypes['1p'])
site4.add_session('16-57-40', None, sessionTypes['3p'])
cluster4 = site4.add_cluster(clusterNumber=4, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
cluster6 = site4.add_cluster(clusterNumber=6, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='good cell')

site5 = exp0707.add_site(depth = 3125, goodTetrodes = [3, 6])
site5.add_session('17-02-39', None, sessionTypes['nb'])
site5.add_session('17-05-02', None, sessionTypes['lp'])
site5.add_session('17-07-13', None, sessionTypes['lt'])
site5.add_session('17-10-30', 'e', sessionTypes['tc'])
site5.add_session('17-25-32', None, sessionTypes['1p'])
site5.add_session('17-26-58', None, sessionTypes['3p'])
cluster11 = site5.add_cluster(clusterNumber=11, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
cluster12 = site5.add_cluster(clusterNumber=12, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
cluster2 = site5.add_cluster(clusterNumber=2, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='good cell')


site6 = exp0707.add_site(depth = 3200, goodTetrodes = [3, 6])
site6.add_session('17-31-32', None, sessionTypes['nb'])
site6.add_session('17-33-53', None, sessionTypes['lp'])
site6.add_session('17-36-05', None, sessionTypes['lt'])
site6.add_session('17-39-12', 'f', sessionTypes['tc'])
site6.add_session('17-52-09', None, sessionTypes['3p'])
site6.add_session('17-54-00', None, sessionTypes['1p'])
cluster9 = site6.add_cluster(clusterNumber=9, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
cluster10 = site6.add_cluster(clusterNumber=10, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
cluster4 = site6.add_cluster(clusterNumber=4, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='good cell')
cluster8 = site6.add_cluster(clusterNumber=8, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='good cell')

site7 = exp0707.add_site(depth = 3275, goodTetrodes = [3,4,6])
site7.add_session('18-01-55', None, sessionTypes['nb'])
site7.add_session('18-03-53', None, sessionTypes['lp'])
site7.add_session('18-05-36', None, sessionTypes['lt'])
site7.add_session('18-08-36', 'g', sessionTypes['tc'])
site7.add_session('18-22-56', None, sessionTypes['3p'])
site7.add_session('18-24-20', None, sessionTypes['1p'])
cluster10 = site7.add_cluster(clusterNumber=10, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')

site8 = exp0707.add_site(depth = 3325, goodTetrodes = [3,4,6])
site8.add_session('18-29-42', None, sessionTypes['nb'])
site8.add_session('18-32-16', None, sessionTypes['lp'])
site8.add_session('18-34-54', None, sessionTypes['lt'])
site8.add_session('18-42-14', 'h', sessionTypes['tc'])
site8.add_session('18-53-39', None, sessionTypes['3p'])
cluster4 = site8.add_cluster(clusterNumber=4, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
cluster5 = site8.add_cluster(clusterNumber=5, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
cluster6 = site8.add_cluster(clusterNumber=6, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')


cellDB = rd.JSONCellDB('/tmp/celldb1.json')
for site in exp0707.siteList:
    cellDB.add_clusters(site.clusterList)
    cellDB.write_database()



