
impedences = {
3: [198, 199, 195, 285], 
4: [370, 180, 272, 283], 
5: [200, 210, 317, 246], 
6: [185, 205, 215, 170]}



laser_calib = {
    1:1.85,
    1.5:2.0,
    2:2.2,
    2.5:2.4,
    3:2.6, 
    3.5:2.8}


'''
Running regular tuning curve with the electrodes not in saline. 

file = noisetest/2015-08-10_10-13-55
behav = 'a'

at 1339 um we have a sound responsive site with (several?) large neurons. I am waiting a few mins for stability and then I will start recording
'''

from jaratoolbox.test.nick.database import cellDB as db
from jaratoolbox.test.nick.database import sitefuncs

rd = db.Experiment('pinp005', '2015-08-10', 'nick', 'laser_tuning_curve')

site1 = rd.add_site(depth = 1399, tetrodes = [3, 6])

site1.add_session('11-33-40', None, 'NoiseBurst') #Ref channel 19
site1.add_session('11-37-15', None, 'LaserPulse') #Good laser responses T3 and T6
site1.add_session('11-39-34', None, 'LaserTrain') #Ref channel 19
site1.add_session('11-43-28', 'a', 'TuningCurve') #30-60dB 16freqs
site1.add_session('11-56-52', 'b', 'auxTuningCurve') #adding trials at 20dB and 70dB
site1.add_session('12-03-03', 'c', 'bestfreq') #7000-8000, 60db, 100 trials
#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds = [0, 1, 2, 5], mainTCind=3)



site2 = rd.add_site(depth = 1491, tetrodes = [3, 5, 6]) #Ref channel 14

site2.add_session('12-10-28', None, 'NoiseBurst') #Good sound responses on T3 and T6
site2.add_session('12-12-52', None, 'LaserPulse') 
site2.add_session('12-15-14', None, 'LaserTrain')
site2.add_session('12-19-09', 'd', 'TuningCurve')
site2.add_session('12-30-44', 'e', 'auxTuningCurve') #16 freqs at 20 and 70 db. I think we should include these by default. 
site2.add_session('12-37-34', 'f', 'BestFreq') #7000-8000, 60db, 100 trials
sitefuncs.nick_lan_daily_report(site2, 'site2', mainRasterInds = [0, 1, 2, 5], mainTCind=3)
    
site3 = rd.add_site(depth = 1567, tetrodes = [3, 5, 6]) #Ref channel 14
site3.add_session('12-42-15', None, 'NoiseBurst') #Good noise response on T3 and T6
site3.add_session('12-44-36', None, 'LaserPulse') #
site3.add_session('12-47-04', None, 'LaserTrain') #
site3.add_session('12-51-00', 'g', 'TuningCurve') #20-70dB
site3.add_session('13-08-31', 'h', 'BestFreq') #7000-8000Hz
sitefuncs.nick_lan_daily_report(site3, 'site3', mainRasterInds = [0, 1, 2, 4], mainTCind=3)

site4 = rd.add_site(depth = 1655, tetrodes = [3, 5, 6]) #Ref channel 14
site4.add_session('13-12-16', None, 'NoiseBurst') #Best responses on T3
site4.add_session('13-14-48', None, 'LaserPulse') #
site4.add_session('13-17-08', None, 'LaserTrain') #
site4.add_session('13-20-50', None, 'TuningCurve') #20-70dB
#sitefuncs.nick_lan_daily_report(site3, 'site3', mainRasterInds = [0, 1, 2, 4], mainTCind=3)



noiseBurstType = 'NoiseBurst'
laserPulseType = 'LaserPulse'
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
