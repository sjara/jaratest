from jaratoolbox.test.nick.database import cellDB


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
CORTEX RECORDING
Running regular tuning curve with the electrodes not in saline. 

file = noisetest/2015-08-10_10-13-55
behav = 'a'

at 1339 um we have a sound responsive site with (several?) large neurons. I am waiting a few mins for stability and then I will start recording
'''

rd = cellDB.Experiment('pinp005', '2015-08-10', 'nick', 'laser_tuning_curve')

site1 = rd.add_site(depth = 1399, tetrodes = [3, 6])

site1.add_session('11-33-40', None, 'NoiseBurst') #Ref channel 19
site1.add_session('11-37-15', None, 'LaserPulse') #Good laser responses T3 and T6
site1.add_session('11-39-34', None, 'LaserTrain') #Ref channel 19
site1.add_session('11-43-28', 'a', 'TuningCurve') #30-60dB 16freqs
site1.add_session('11-56-52', 'b', 'auxTuningCurve') #adding trials at 20dB and 70dB
site1.add_session('12-03-03', 'c', 'bestfreq') #7000-8000, 60db, 100 trials



site2 = rd.add_site(depth = 1491, tetrodes = [3, 5, 6]) #Ref channel 14

site2.add_session('12-10-28', None, 'NoiseBurst') #Good sound responses on T3 and T6
site2.add_session('12-12-52', None, 'LaserPulse') 
site2.add_session('12-15-14', None, 'LaserTrain')
site2.add_session('12-19-09', 'd', 'TuningCurve')
site2.add_session('12-30-44', 'e', 'auxTuningCurve') #16 freqs at 20 and 70 db. I think we should include these by default. 
site2.add_session('12-37-34', 'f', 'BestFreq') #7000-8000, 60db, 100 trials
    
site3 = rd.add_site(depth = 1567, tetrodes = [3, 5, 6]) #Ref channel 14
site3.add_session('12-42-15', None, 'NoiseBurst') #Good noise response on T3 and T6
site3.add_session('12-44-36', None, 'LaserPulse') #
site3.add_session('12-47-04', None, 'LaserTrain') #
site3.add_session('12-51-00', 'g', 'TuningCurve') #20-70dB
site3.add_session('13-08-31', 'h', 'BestFreq') #7000-8000Hz

site4 = rd.add_site(depth = 1655, tetrodes = [3, 5, 6]) #Ref channel 14
site4.add_session('13-12-16', None, 'NoiseBurst') #Best responses on T3
site4.add_session('13-14-48', None, 'LaserPulse') #
site4.add_session('13-17-08', None, 'LaserTrain') #
site4.add_session('13-20-50', 'i', 'TuningCurve') #20-70dB
site4.add_session('13-39-05', 'j', 'BestFreq') #7000-8000, 60dB

'''
1655um, taking the electrodes out and letting the mouse rest. 
'''

'''
New penetration with the same array - this time in the medial side of the right thalamus well.

1732hrs - electrodes at 1546um and fairly quiet. mouse waking up now.
Small spikes on TT3 that respond to visual stimuli
lots of spiking around 1750um

Tons of spiking around 2500um

Went straight to 3000um - will wait for the electrodes to stabilize for 5 mins before continuing. 
'''


# rd2 = Experiment('pinp005', '2015-08-10', 'nick', 'laser_tuning_curve')

# r2site1 = rd2.add_site(depth = 3664, tetrodes = [3])
# r2site1.add_session('17-54-41', None, 'NoiseBurst')
# r2site1.add_session('17-57-34', None, 'LaserPulse') #No laser responses yet, moving on. 

# '''
# Tuning curve 'k' - 18-14-06

# '''
# r2site2 = rd2.add_site(depth = 3682, tetrodes = [3])







noiseBurstType = 'NoiseBurst'
laserPulseType = 'LaserPulse'
experimentObj = rd

siteNums = [1, 2, 3, 4]

#Number of cells recorded

numSound = []
for indsite, site in enumerate(experimentObj.siteList):
    sitename = 'site{}'.format(siteNums[indsite])
    soundInd = site.get_session_types().index(noiseBurstType)
    laserInd = site.get_session_types().index(laserPulseType)

    good = sitefuncs.find_good_clusters(site, sitename, soundInd, laserInd, maxISI = 0.02, minSoundZ=2, minLaserZ=0)
    numSound.extend(good)

soundTetrodes = unique([x[:7] for x in numSound])

numCells = []
for indsite, site in enumerate(experimentObj.siteList):
    sitename = 'site{}'.format(siteNums[indsite])
    soundInd = site.get_session_types().index(noiseBurstType)
    laserInd = site.get_session_types().index(laserPulseType)

    good = sitefuncs.find_good_clusters(site, sitename, soundInd, laserInd, maxISI = 0.02, minSoundZ=0, minLaserZ=0)
    numCells.extend(good)

soundCells = [cell for cell in numCells if any([x in cell for x in soundTetrodes])]

#Number ID neurons
numID = []
for indsite, site in enumerate(experimentObj.siteList):
    sitename = 'site{}'.format(siteNums[indsite])
    soundInd = site.get_session_types().index(noiseBurstType)
    laserInd = site.get_session_types().index(laserPulseType)

    good = sitefuncs.find_good_clusters(site, sitename, soundInd, laserInd, maxISI = 0.02, minSoundZ=0, minLaserZ=2)
    numID.extend(good)

soundID = [cell for cell in numID if any([x in cell for x in soundTetrodes])]

#Number ID neurons that are sound responsive
numIDSound = []
for indsite, site in enumerate(experimentObj.siteList):
    sitename = 'site{}'.format(siteNums[indsite])
    soundInd = site.get_session_types().index(noiseBurstType)
    laserInd = site.get_session_types().index(laserPulseType)

    good = sitefuncs.find_good_clusters(site, sitename, soundInd, laserInd, maxISI = 0.02, minSoundZ=2, minLaserZ=2)
    numIDSound.extend(good)

print "Total neurons:", soundCells, len(soundCells), '\n'
print "ID neurons:", soundID, len(soundID), '\n'
print "Sound responsive neurons:", numSound, len(numSound), '\n'
print "Sound responsive ID neurons:", numIDSound, len(numIDSound), '\n'
