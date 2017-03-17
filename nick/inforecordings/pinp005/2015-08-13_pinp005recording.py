

impedences = {
3: [170, 168, 207, 192], 
4: [325, 263, 207, 209], 
5: [98.3, 98.1, 208, 197], 
6: [157, 346, 237, 204]}

#Laser power measured at the tip of the fiber -> dial setting to produce this power
laser_calib = {
    1:2.0,
    1.5:2.2,
    2:2.4,
    2.5:2.6,
    3:2.8, 
    3.5:3.05}


'''
Today we are going to record responses to some amplitude-modulated noises. We will begin recording in the right thalamus well because there were good sound responses there yesterday. We will switch to cortex if we need to find better responses. 


1217hrs - mouse is on the rig, electrodes at 1037um, waiting for 10 mins. 
'''


from jaratoolbox.test.nick.database import sitefuncs
from jaratoolbox.test.nick.database import cellDB
rd = cellDB.Experiment('pinp005', '2015-08-13', 'nick', 'laser_tuning_curve')

site1 = rd.add_site(depth=3902, tetrodes=[3, 4, 5, 6])
site1.add_session('12-48-14', None, 'NoiseBursts')
site1.add_session('12-50-27', None, 'LaserPulse')
site1.add_session('12-53-02', None, 'LaserTrain')
# site1.add_session('12-57-12', 'a', 'AM')
# site1.add_session('13-11-52', 'b', 'AM')
site1.add_session('13-24-17', 'c', 'TuningCurve')
site1.add_session('13-41-46', 'd', 'BestFreq') #6000-7000Hz, 60dB
site1.add_session('13-52-29', 'e', 'AM')
# site1.add_session('14-29-13', None, 'LaserPulse') #Higher thresholds (44uV) Too high



site2 = rd.add_site(depth=3970, tetrodes=[3, 4, 5, 6]) #threshold = 23uV
site2.add_session('14-36-57', None, 'NoiseBursts')
site2.add_session('14-42-41', None, 'LaserPulse')
site2.add_session('14-46-14', None, 'LaserTrain')
site2.add_session('14-50-18', 'f', 'AM')
site2.add_session('15-15-40', 'g', 'TuningCurve')
site2.add_session('15-33-58', 'h', 'BestFreq') #6000-7000, 60dB
# sitefuncs.nick_lan_daily_report(site2, 'site2', mainRasterInds=[0, 1, 2, 5], mainTCind=4)
# sitefuncs.am_mod_report(site2, 'site2', amSessionInd=3)
site2.add_cluster(3, 3, comments = "Best unit for AM modulation. Also sound/laser responsive thalamus unit for B/C/D")

'''
'''
site3 = rd.add_site(depth=4050, tetrodes=[3, 4, 5, 6]) #threshold = 23uV
site3.add_session('15-43-47', None, 'NoiseBursts')
site3.add_session('15-45-57', None, 'LaserPulse') #No more laser responses

amdbFn = '/home/nick/Desktop/amdatabase.json'
amdb = cellDB.CellDB()
amdb.load_from_json(amdbFn)
amdb.add_clusters(site2.clusterList)
amdb.write_to_json(amdbFn)



'''
Removing the electrodes and evaluating whether I should go to the cortex and record or just put DiI. I need to put DiI in the cortex anyway, so I will probably record while I am there. 

The thalamis site is just anterior and medial of the center of the craniotomy
I coated the electrodes in DiI and re-inserted them in the same thalamic site from this morning. I went to a depth of 4000um. I will leave them in for 5 minutes, then remove them and clean them slightly with water before going into the cortex well. 


1622hrs - electrodes (with a fresh coat of DiI) are at 700um in the right cortex well. Mouse is waking up from iso
Max depth in cortex = 2600um

1647hrs - I am now inserting the electrodes with DiI into the left thalamus well, in the very center of the well. 
Max depth = 4050um. Went at medium speed. Will wait for a few mins here. The mouse is under anaesthesia. 

'''


noiseBurstType = 'NoiseBursts'
laserPulseType = 'LaserPulse'
experimentObj = rd

siteNums = [1, 2]

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
print "Sound responsive ID neurons:", numIDSound, len(numIDSound), '\n'
