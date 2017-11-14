from jaratoolbox.test.nick.database import cellDB
from jaratoolbox.test.nick.database import sitefuncs
reload(cellDB)

#The session types to use for this kind of experiment
#Can use a dict like this or simply write the sesison types directly
#I used this to avoid typing errors and to save time
sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tc_heatmap',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse'} 

today = cellDB.Experiment('pinp003', '2015-06-24', 'nick', 'laser_tuning_curve')

# dbFn='/home/nick/data/database/nick_thalamus_cells.json'
dbFn='/home/nick/data/database/pinp003_thalamus_cells.json'

db = cellDB.CellDB()

gc = []

site1 = today.add_site(depth = 3543, tetrodes = [6])
site1.add_session('15-22-29', None, sessionTypes['nb'])
site1.add_session('15-25-08', None, sessionTypes['lp'])
site1.add_session('15-27-37', None, sessionTypes['lt'])
site1.add_session('15-31-48', 'a', sessionTypes['tc'])
site1.add_session('15-45-22', 'b', sessionTypes['bf'])

# site1.add_cluster(6, 3, comments='Might not be neuronal, but interesting')
# site1.add_cluster(6, 6, comments='STAR Probably synaptic, but has sound response')
# db.add_clusters(site1.clusterList)

# site1.add_cluster(6, 10)
# db.add_clusters(site1.clusterList)


# gc.append(sitefuncs.find_good_clusters(site1, 'site1', soundInd=0, laserInd=1))


site2 = today.add_site(depth = 3623, tetrodes = [6])
site2.add_session('15-54-56', None, sessionTypes['nb'])
site2.add_session('15-57-33', None, sessionTypes['lp'])
site2.add_session('16-00-02', None, sessionTypes['lt'])
site2.add_session('16-04-48', 'c', sessionTypes['tc'])
site2.add_session('16-17-30', 'd', sessionTypes['bf'])
site2.add_session('16-20-11', None, sessionTypes['3p'])
site2.add_session('16-22-37', None, sessionTypes['1p'])

# site2.add_cluster(6, 3, comments='Sound responsive but not laser responsive, good tuning curve')
# site2.add_cluster(6, 4, comments='Likely good synaptic response')
# site2.add_cluster(6, 6, comments='STAR Good tuning curve but likely synaptic')
# db.add_clusters(site2.clusterList)

# gc.append(sitefuncs.find_good_clusters(site2, 'site2', soundInd=0, laserInd=1))

site3 = today.add_site(depth = 3700, tetrodes = [6])
site3.add_session('16-40-44', None, sessionTypes['nb'])
site3.add_session('16-44-01', None, sessionTypes['lp'])
site3.add_session('16-46-20', None, sessionTypes['lt'])
site3.add_session('16-50-03', 'e', sessionTypes['tc'])
site3.add_session('17-03-10', None, sessionTypes['bf'])
site3.add_session('17-06-10', None, sessionTypes['3p'])
site3.add_session('17-09-06', None, sessionTypes['1p'])

# sitefuncs.nick_lan_daily_report(site3, 'site3_recluster', mainRasterInds=[0, 1, 2, 4], mainTCind=3)

#I reclustered this session, I think there are some really bad noise issues. Reclustering did not help

# site3.add_cluster(6, 5, comments='Are the responses same as basal for shapes?')
# site3.add_cluster(6, 6, comments='Spike shapes are good')
# site3.add_cluster(6, 11, comments='STAR good tuning and sound resp, good shapes, (part of c6?)')
# db.add_clusters(site3.clusterList)

# gc.append(sitefuncs.find_good_clusters(site3, 'site3_recluster', soundInd=0, laserInd=1))


site4 = today.add_site(depth = 3757, tetrodes = [3, 6])
site4.add_session('17-15-58', None, sessionTypes['nb'])
site4.add_session('17-18-57', None, sessionTypes['lp'])
site4.add_session('17-21-29', None, sessionTypes['lt'])
site4.add_session('17-25-16', 'g', sessionTypes['tc'])
site4.add_session('17-37-45', 'af', sessionTypes['bf'])
site4.add_session('17-41-31', None, sessionTypes['3p'])
site4.add_session('17-44-25', None, sessionTypes['1p'])

# gc.append(sitefuncs.find_good_clusters(site4, 'site4', soundInd=0, laserInd=1))



site5 = today.add_site(depth = 3805, tetrodes = [3, 6])
site5.add_session('17-59-53', None, sessionTypes['nb'])
site5.add_session('18-03-50', None, sessionTypes['lp'])
site5.add_session('18-06-31', None, sessionTypes['lt'])
site5.add_session('18-10-38', 'h', sessionTypes['tc'])
site5.add_session('18-24-47', None, sessionTypes['bf'])
site5.add_session('18-29-24', None, sessionTypes['3p'])
site5.add_session('18-33-08', None, sessionTypes['1p'])

# site5.add_cluster(6, 7, comments='Responds to laser but has bad shape')
# db.add_clusters(site5.clusterList)



# gc.append(sitefuncs.find_good_clusters(site5, 'site5', soundInd=0, laserInd=1))

site6 = today.add_site(depth = 3855, tetrodes = [6])
site6.add_session('18-44-21', None, sessionTypes['nb'])
site6.add_session('18-47-59', None, sessionTypes['lp'])
site6.add_session('18-51-29', None, sessionTypes['lt'])
site6.add_session('18-55-40', 'i', sessionTypes['tc'])
site6.add_session('19-10-27', None, sessionTypes['bf'])
site6.add_session('19-13-33', None, sessionTypes['3p'])
site6.add_session('19-16-41', None, sessionTypes['1p'])
# sitefuncs.nick_lan_daily_report(site6, 'site6_recluster', mainRasterInds=[0, 1, 2, 4], mainTCind=3)

# gc.append(sitefuncs.find_good_clusters(site6, 'site6_recluster', soundInd=0, laserInd=1))

# site6.add_cluster(6, 3, comments='DOUBLE STAR: Good laser and sound responses (try to clean this cluster)')
# site6.add_cluster(6, 10, comments='Very nice sound response and shape')
# db.add_clusters(site6.clusterList)

#The data from this day seems quite poor, although there are some sites at the beginning that look promising


# db.write_to_json(dbFn)



#Number of neurons
# for indsite, site in enumerate(today.siteList):
#     sitename = 'site{}'.format(indsite+1)
#     violations = sitefuncs.calculate_site_ISI_violations(site, sitename)
#     for clust, isi in violations.iteritems():
#         if isi<0.02:
#             print clust

noiseBurstType = 'noiseBurst'
laserPulseType = 'laserPulse'
experimentObj = today

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

