impedences = {
3: [209, 261, 240, 279], 
4: [486, 389, 399, 568], 
5: [298, 342, 432, 437], 
6: [201, 231, 258, 202]}


laser_calib = {
    1:1.8,
    1.5:1.9,
    2:2.05,
    2.5:2.2,
    3:2.3, 
    3.5:2.4}

lengths = {TT3: 0, TT6: 273, TT5: 466, TT4: 594} 


'''
2026hrs - mouse is on the rig with the tetrodes in the Right cortex well - middle of the well AP but close to the lateral side. THey look like they might start to bend a little bit laterally as well due to the shape of them, which could be good for getting to ac. 


'''
from jartoolbox.test.nick.database import CellDB

rd = db.Experiment('pinp005', '2015-08-05','nick', 'laser_tuning_curve')

site1=rd.add_site(depth=1135, tetrodes=[ 3 ])

site1.add_session('21-10-44', None, 'NoiseBurst')
site1.add_session('21-13-44', None, 'LaserPulse')
site1.add_session('21-16-19', None, 'LaserTrain')
site1.add_session('21-20-41', 'a', 'TuningCurve')

site2=rd.add_site(depth=1192, tetrodes=[ 3 , 6 ])
site2.add_session('21-40-59', None, 'NoiseBurst')
site2.add_session('21-43-40', None, 'LaserPulse') #Not laser responsive
site2.add_session('21-46-24', 'b', 'ShortTC') #Only at 60dB 

#Interesting tuning curve at 1415um. 
site3=rd.add_site(depth=1451, tetrodes=[ 3 , 6 ])
site3.add_session('22-47-00', 'c', 'ShortTC') #Only at 60dB 
site3.add_session('22-52-45', 'd', 'TuningCurve') #30-60dB


site4=rd.add_site(depth=1722, tetrodes=[ 3, 4, 5, 6 ])
site4.add_session('23-25-52', None, 'NoiseBurst')
site4.add_session('23-28-19', None, 'LaserPulse') #Good responses on TT4
site4.add_session('23-30-52', None, 'LaserTrain') #All the laser responses went away
site4.add_session('23-36-02', 'e', 'TuningCurve') # Great tc for TT3
site4.add_session('23-49-05', 'f', 'TuningCurveLower') #Another 160 trials at 20dB to try to resolve the threshold at cf

site5=rd.add_site(depth=1776, tetrodes=[ 3, 4, 5, 6 ])
site5.add_session('23-54-31', None, 'LaserPulse') #Laser responses on TT4
site5.add_session('23-57-52', None, 'NoiseBurst') #Laser responses on TT4
site5.add_session('00-04-11', 'g', 'TuningCurve') #Laser responses on TT4
site5.add_session('00-17-11', 'h', 'TuningCurveLower') #Another 160 trials to get the cf
site5.add_session('00-20-17', None, 'LaserTrain')
site5.add_session('00-24-39', 'i', 'TuningCurveHigher') #Another 160 trials at 70dB to get a better TC for TT4 - it has a very high threshold

'''
0030hrs - taking the tetrodes out and letting the mouse go home
'''

noiseBurstType = 'NoiseBurst'
laserPulseType = 'LaserPulse'
experimentObj = rd

siteNums = [1, 2, 4, 5]

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
