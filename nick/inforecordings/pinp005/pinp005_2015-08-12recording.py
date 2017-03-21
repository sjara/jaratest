
impedences = {
3: [197, 190, 203, 230],
4: [389, 243, 205, 174],
5: [222, 197, 243, 184],
6: [194, 399, 331, 239]}

laser_calib = {
    1:1.95,
    1.5:2.2,
    2:2.45,
    2.5:2.75,
    3:3.0,
    3.5:3.2}

'''
Noisetest - 2015-08-12_10-23-47 = laser pulse 1mW (no ref LFP/Spikes, spike thresh=0mV)
10-26-03: Laser 2mW
10-28-13: Laser 3mW
'''

'''
THALAMUS RECORDING
1054hrs - mouse on rig with electrodes at 1002um - waiting for 10 mins
'''
from jaratoolbox.test.nick.database import cellDB
rd = cellDB.Experiment('pinp005', '2015-08-12', 'nick', 'laser_tuning_curve')
'''
Lots of spikes on T3 around 2700um
1113hrs - letting the electrodes rest at 3000um for 5 mins.
'''



site1 = rd.add_site(depth=3833, tetrodes = [3, 4])
site1.add_session('11-34-42', None, 'NoiseBurst')
site1.add_session('11-37-03', None, 'LaserPulse') #2.5mW - strong onset response
site1.add_session('11-42-57', None, 'LaserPulseLowerPower') #1.5mW - Still onset response
site1.add_session('11-45-32', None, 'LaserPulseHigherPower') #3.5mW - Still onset response
site1.add_session('11-48-13', None, 'LaserTrain') #2.5m
site1.add_session('11-52-04', 'a', 'TuningCurve') #20-70dB
site1.add_session('12-11-03', None, 'BestFreq') #7-8kHz, 60dB

site2 = rd.add_site(depth=3921, tetrodes = [3, 4, 5, 6])
site2.add_session('12-23-35', None, 'NoiseBurst')
site2.add_session('12-25-47', None, 'LaserPulse')
site2.add_session('12-28-16', None, 'LaserTrain')
site2.add_session('12-32-46', 'b', 'TuningCurve')
site2.add_session('12-51-13', None, 'BestFreq') #7-8kHz, 60dB

site3 = rd.add_site(depth=4001, tetrodes = [3, 4, 5, 6])

site3.add_session('12-58-13', None, 'NoiseBurst')
site3.add_session('13-01-25', None, 'LaserPulse') #Only onset response
site3.add_session('13-03-59', None, 'LaserTrain')
site3.add_session('13-07-39', 'c', 'TuningCurve')
site3.add_session('13-25-01', None, 'BestFreq') #7-8kHz, 60dB



site4 = rd.add_site(depth=4101, tetrodes = [3, 4, 5, 6])
site4.add_session('13-35-02', None, 'NoiseBurst')
site4.add_session('13-37-50', None, 'LaserPulse')
site4.add_session('13-40-28', None, 'LaserTrain')


site5 = rd.add_site(depth=4236, tetrodes = [3, 4, 5, 6])
site5.add_session('13-50-28', None, 'NoiseBurst')
site5.add_session('13-53-50', None, 'LaserPulse')
site5.add_session('13-58-15', None, 'LaserTrain')
site5.add_session('14-02-32', 'd', 'TuningCurve')
site5.add_session('14-20-51', None, 'BestFreq') #7-8kHz, 60dB

'''
Responses are gone by 4650um. calling it a day.
'''

noiseBurstType = 'NoiseBurst'
laserPulseType = 'LaserPulse'
experimentObj = rd

siteNums = [1, 2, 5]

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
