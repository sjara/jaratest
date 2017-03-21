
impedences = {
3: [190, 193, 194, 303], 
4: [368, 166, 282, 300], 
5: [188, 194, 323, 259], 
6: [234, 188, 246, 184]}



laser_calib = {
    1:1.75,
    1.5:1.9,
    2:2.00,
    2.5:2.1,
    3:2.25, 
    3.5:2.35}

lengths = {TT3: 0, TT6: 273, TT5: 466, TT4: 594} 


'''
THALAMUS RECORDING
1514hrs - mouse is on the rig and awake, tetrodes at 1081um. 
visually responsive units on T3


'''

rd = Experiment('pinp005', '2015-08-06', 'nick', 'laser_tuning_curve')

site1 = rd.add_site(depth=3537, tetrodes=[3,4,5,6])

site1.add_session('16-16-50', None, 'NoiseBurst')
site1.add_session('16-20-56', None, 'LaserPulse')


site2 = rd.add_site(depth=3570, tetrodes=[3,4,5,6])
site2.add_session('16-27-50', None, 'NoiseBurst') #Looks like onset and offset responses on T3
site2.add_session('16-30-21', None, 'LaserPulse') #No Laser response
site2.add_session('16-33-17', 'j', 'TuningCurve') #Looks like onset and offset responses on T3


site3 = rd.add_site(depth=3603, tetrodes=[3,4,5,6])
#No laser response at this site. 16-50-27
site3.add_session('16-52-36', None, 'NoiseBurst') #Looks like onset and offset responses on T3
site3.add_session('16-55-27', 'k', 'ShortTC') #Just looking at the response to freqs, all 60dB

site4 = rd.add_site(depth=4114, tetrodes=[3,4,5,6])
site4.add_session('18-05-16', None, 'NoiseBurst')
site4.add_session('18-07-57', None, 'LaserPulse')
site4.add_session('18-10-23', None, 'LaserTrain')
site4.add_session('18-14-06', 'l', 'TuningCurve')


'''
1837hrs - by 4200um sound responses are gone. Removing the electrodes and calling it a day.
'''

noiseBurstType = 'NoiseBurst'
laserPulseType = 'LaserPulse'
experimentObj = rd

siteNums = [1, 2, 4]

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
