'''
This data was collected the day before we RF shielded the speakers and recalibrated them. We need to be extra careful with anything related to noise and tuning curve presentations.
'''


from jaratoolbox.test.nick.database import cellDB as db
from jaratoolbox.test.nick.database import sitefuncs

rd = cellDB.Experiment('pinp003', '2015-06-30', 'nick', 'laser_tuning_curve')

gc = []


dbFn='/home/nick/data/database/pinp003_thalamus_cells.json'
db = cellDB.CellDB()
db.load_from_json(dbFn)




site1 = rd.add_site(depth = 3325, tetrodes = [3, 6])
site1.add_session('12-21-34', None, 'LaserPulse')
site1.add_session('12-25-12', None, 'NoiseBurst')
site1.add_session('12-28-19', None, 'LaserTrain')
site1.add_session('12-32-31', 'a', 'TuningCurve')
site1.add_session('12-46-58', None, 'BestFreq') #7-8kHz, 70dB
#site1.add_session('12-50-43', None, 'LaserPulse3mW')
#site1.add_session('12-53-09', None, 'LaserPulse1mW')
# sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds = [0, 1, 2, 4], mainTCind = 3)

# gc.append(sitefuncs.find_good_clusters(site1, 'site1', soundInd = 1, laserInd=0))



site4 = rd.add_site(depth = 3825, tetrodes = [3, 6])
site4.add_session('14-21-48', None, 'LaserPulse')
site4.add_session('14-24-29', None, 'NoiseBurst')
site4.add_session('14-26-46', None, 'LaserTrain')
site4.add_session('14-30-24', 'c', 'TuningCurve')
site4.add_session('14-43-14', None, 'BestFreq') #8-9kHz, 70dB
# sitefuncs.nick_lan_daily_report(site4, 'site4', mainRasterInds = [1, 0, 2, 4], mainTCind = 3)
# site4.add_cluster(3, 11, comment="Low ISI violation, sound responseve, not much laser response")
# gc4 = sitefuncs.find_good_clusters(site4, 'site4', soundInd = 1, laserInd = 0, maxISI = 0.03)

# gc.append(sitefuncs.find_good_clusters(site4, 'site4', soundInd = 1, laserInd=0))

# site4.add_cluster(6, 2)
# db.add_clusters(site4.clusterList)


site5 = rd.add_site(depth = 3875, tetrodes = [3, 6])
site5.add_session('14-54-11', None, 'NoiseBurst')
site5.add_session('14-57-06', None, 'LaserPulse')
site5.add_session('14-59-21', None, 'LaserTrain')
site5.add_session('15-03-22', 'd', 'TuningCurve')
site5.add_session('15-16-21', None, 'BestFreq')
# sitefuncs.nick_lan_daily_report(site5, 'site5', mainRasterInds = [0, 1, 2, 4], mainTCind = 3)
# gc5 = sitefuncs.find_good_clusters(site5, 'site5', soundInd = 0, laserInd = 1, maxISI = 0.06)

# gc.append(sitefuncs.find_good_clusters(site5, 'site5', soundInd = 0, laserInd=1))

reload(sitefuncs)
# site6 = rd.add_site(depth = 3925, tetrodes = [3, 6])
site6 = rd.add_site(depth = 3925, tetrodes = [6])
site6.add_session('15-30-36', None, 'LaserPulse')
site6.add_session('15-33-02', None, 'LaserTrain')
site6.add_session('15-36-46', 'e', 'TuningCurve')
site6.add_session('15-51-29', None, 'BestFreq') #8000-9000Hz, 70dB
# sitefuncs.nick_lan_daily_report(site6, 'site6', mainRasterInds = [0, 1, 3], mainTCind = 2)
# sitefuncs.nick_lan_daily_report(site6, 'site6_recluster_2', mainRasterInds = [0, 1, 3], mainTCind = 2)
# isi_2 = sitefuncs.calculate_site_ISI_violations(site6, 'site6_recluster_2')
# soundMaxZ = sitefuncs.calculate_site_response(site6, 'site6_recluster_2', sessionInd = 3, maxZonly=True)
# laserMaxZ = sitefuncs.calculate_site_response(site6, 'site6_recluster_2', sessionInd = 0, maxZonly=True)
# gc = sitefuncs.find_good_clusters(site6, 'site6_recluster_2', soundInd = 3, laserInd = 0)

# gc.append(sitefuncs.find_good_clusters(site6, 'site6_recluster_2', soundInd = 3, laserInd=0))


site7 = rd.add_site(depth = 3975, tetrodes = [3, 6])
site7.add_session('16-01-48', None, 'NoiseBurst')
site7.add_session('16-04-17', None, 'LaserPulse')
site7.add_session('16-06-40', None, 'LaserTrain')
site7.add_session('16-10-28', 'f', 'TuningCurve')
site7.add_session('16-25-53', None, 'BestFreq') #5-7kHz
# sitefuncs.nick_lan_daily_report(site7, 'site7', mainRasterInds = [0, 1, 2, 4], mainTCind = 3)
# site7.add_cluster(6, 4, comment="Low ISI violation, Sound responsive, not laser responsive")
# site7.add_cluster(6, 5, comment="Low ISI violation, soind and possibly laser responsive")

# gc.append(sitefuncs.find_good_clusters(site7, 'site7', soundInd = 0, laserInd=1))

site8 = rd.add_site(depth = 4025, tetrodes = [3, 6])
site8.add_session('16-45-16', None, 'NoiseBurst')
site8.add_session('16-48-00', None, 'LaserPulse')
site8.add_session('16-50-51', None, 'LaserTrain')
site8.add_session('16-56-14', 'g', 'TuningCurve')
site8.add_session('17-09-09', None, 'BestFreq') #7-8kHz
# sitefuncs.nick_lan_daily_report(site8, 'site8', mainRasterInds = [0, 1, 2, 4], mainTCind = 3)

# gc.append(sitefuncs.find_good_clusters(site8, 'site8', soundInd = 0, laserInd=1))


# '''Out[122]: [[], [], ['site6_recluster_2T6c5'], [], []]'''

# db.write_to_json(dbFn)

noiseBurstType = 'BestFreq'
laserPulseType = 'LaserPulse'
experimentObj = rd

#Number of cells recorded
numCells = []
for indsite, site in enumerate(experimentObj.siteList):
    sitename = 'site{}'.format(indsite+1)
    soundInd = site.get_session_types().index(noiseBurstType)
    laserInd = site.get_session_types().index(laserPulseType)

    good = sitefuncs.find_good_clusters(site, sitename, soundInd, laserInd, maxISI = 0.02, minSoundZ=0, minLaserZ=0)
    numCells.extend(good)

#Number ID neurons
numID = []
for indsite, site in enumerate(experimentObj.siteList):
    sitename = 'site{}'.format(indsite+1)
    soundInd = site.get_session_types().index(noiseBurstType)
    laserInd = site.get_session_types().index(laserPulseType)

    good = sitefuncs.find_good_clusters(site, sitename, soundInd, laserInd, maxISI = 0.02, minSoundZ=0, minLaserZ=2)
    numID.extend(good)

#Number ID neurons that are sound responsive
numIDSound = []
for indsite, site in enumerate(experimentObj.siteList):
    sitename = 'site{}'.format(indsite+1)
    soundInd = site.get_session_types().index(noiseBurstType)
    laserInd = site.get_session_types().index(laserPulseType)

    good = sitefuncs.find_good_clusters(site, sitename, soundInd, laserInd, maxISI = 0.02, minSoundZ=2, minLaserZ=2)
    numIDSound.extend(good)

print "Total neurons:", numCells, len(numCells), '\n'
print "ID neurons:", numID, len(numID), '\n'
print "Sound responsive ID neurons:", numIDSound, len(numIDSound), '\n'

