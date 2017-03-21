from jaratoolbox.test.nick.database import cellDB

#The session types to use for this kind of experiment
#Can use a dict like this or simply write the sesison types directly
#I used this to avoid typing errors and to save time
sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse'} 

# dbFn='/home/nick/data/database/nick_thalamus_cells.json'
dbFn='/home/nick/data/database/pinp003_thalamus_cells.json'
db = cellDB.CellDB()
db.load_from_json(dbFn)

gc = []

rd = cellDB.Experiment('pinp003', '2015-07-06', 'nick', 'laser_tuning_curve')

site1 = rd.add_site(depth = 3509, tetrodes = [3, 6])
site1.add_session('11-15-56', None, sessionTypes['nb'])
site1.add_session('11-18-36', None, sessionTypes['lp'])
site1.add_session('11-21-26', None, sessionTypes['lt'])
site1.add_session('11-25-58', 'a', sessionTypes['tc'])
site1.add_session('11-39-46', None, sessionTypes['bf'])
site1.add_session('11-42-37', None, sessionTypes['3p'])
site1.add_session('11-45-22', None, sessionTypes['1p'])


gc.append(sitefuncs.find_good_clusters(site1, 'site1', soundInd = 0, laserInd=1))


site2 = rd.add_site(depth = 3550, tetrodes = [3, 6])
site2.add_session('11-51-47', None, sessionTypes['nb'])
site2.add_session('11-54-51', None, sessionTypes['lp'])
site2.add_session('11-58-17', None, sessionTypes['lt'])
site2.add_session('12-01-53', 'b', sessionTypes['tc'])
site2.add_session('12-14-53', None, sessionTypes['bf'])
site2.add_session('12-17-13', None, sessionTypes['3p'])
site2.add_session('12-19-34', None, sessionTypes['1p'])

gc.append(sitefuncs.find_good_clusters(site2, 'site2', soundInd = 0, laserInd=1))

site2.add_cluster(3, 10)
db.add_clusters(site2.clusterList)

site3 = rd.add_site(depth = 3606, tetrodes = [3, 6])
site3.add_session('12-28-47', None, sessionTypes['nb'])
site3.add_session('12-31-21', None, sessionTypes['lp'])
site3.add_session('12-34-00', None, sessionTypes['lt'])
site3.add_session('12-37-29', 'c', sessionTypes['tc'])
site3.add_session('12-50-34', None, sessionTypes['bf'])
site3.add_session('12-53-57', None, sessionTypes['3p'])
site3.add_session('12-56-04', None, sessionTypes['1p'])

gc.append(sitefuncs.find_good_clusters(site3, 'site3', soundInd = 0, laserInd=1))

site4 = rd.add_site(depth = 3654, tetrodes = [3, 6])
site4.add_session('13-06-27', None, sessionTypes['nb'])
site4.add_session('13-09-00', None, sessionTypes['lp'])
site4.add_session('13-11-25', None, sessionTypes['lt'])
site4.add_session('13-15-01', 'd', sessionTypes['tc'])
site4.add_session('13-28-12', None, sessionTypes['bf'])
site4.add_session('13-30-00', None, sessionTypes['3p'])
site4.add_session('13-31-58', None, sessionTypes['1p'])

gc.append(sitefuncs.find_good_clusters(site4, 'site4', soundInd = 0, laserInd=1))

# site4.add_cluster(3, 10, comments='STAR: Good laser responses')
# site4.add_cluster(3, 12, comments='Ok responses')

# site4.add_cluster(6, 2)

# db.add_clusters(site4.clusterList)
db.write_to_json(dbFn)

noiseBurstType = 'bestFreq'
laserPulseType = 'laserPulse'
experimentObj = rd

siteNums = [1, 2, 3, 4]

#Number of cells recorded
numCells = []
for indsite, site in enumerate(experimentObj.siteList):
    sitename = 'site{}'.format(siteNums[indsite])
    soundInd = site.get_session_types().index(noiseBurstType)
    laserInd = site.get_session_types().index(laserPulseType)

    good = sitefuncs.find_good_clusters(site, sitename, soundInd, laserInd, maxISI = 0.02, minSoundZ=0, minLaserZ=0)
    numCells.extend(good)

#Number ID neurons
numID = []
for indsite, site in enumerate(experimentObj.siteList):
    sitename = 'site{}'.format(siteNums[indsite])
    soundInd = site.get_session_types().index(noiseBurstType)
    laserInd = site.get_session_types().index(laserPulseType)

    good = sitefuncs.find_good_clusters(site, sitename, soundInd, laserInd, maxISI = 0.02, minSoundZ=0, minLaserZ=2)
    numID.extend(good)

numSound = []
for indsite, site in enumerate(experimentObj.siteList):
    sitename = 'site{}'.format(siteNums[indsite])
    soundInd = site.get_session_types().index(noiseBurstType)
    laserInd = site.get_session_types().index(laserPulseType)

    good = sitefuncs.find_good_clusters(site, sitename, soundInd, laserInd, maxISI = 0.02, minSoundZ=2, minLaserZ=0)
    numSound.extend(good)

#Number ID neurons that are sound responsive
numIDSound = []
for indsite, site in enumerate(experimentObj.siteList):
    sitename = 'site{}'.format(siteNums[indsite])
    soundInd = site.get_session_types().index(noiseBurstType)
    laserInd = site.get_session_types().index(laserPulseType)

    good = sitefuncs.find_good_clusters(site, sitename, soundInd, laserInd, maxISI = 0.02, minSoundZ=2, minLaserZ=2)
    numIDSound.extend(good)

print "Total neurons:", numCells, len(numCells), '\n'
print "ID neurons:", numID, len(numID), '\n'
print "Sound responsive neurons:", numSound, len(numSound), '\n'
print "Sound responsive ID neurons:", numIDSound, len(numIDSound), '\n'
