lengths = {'TT4':0, 'TT3':80, 'TT5':204, 'TT6':510}

impedence = {
    'TT3':[307, 344, 172, 235],
    'TT4':[266, 237, 166, 302],
    'TT5':[314, 258, 347, 306],
    'TT6':[318, 328, 241, 342]}


lasercalibration = {
    0.5:1.89,
    1.0:3.05,
    1.5:4.00,
    2.0:4.80,
    2.5:6.05,
    3.0:6.50}

'''
THALAMUS RECORDING

1328 - mouse is on the rig with tetrodes in the center of the right craniotomy.
The craniotomy is not aligned with the well, so the site is anteromedial to the
center of the well. The tetrodes are a lot longer than I usually leave them, and



the portions of the tetrodes that will be entering the brain are far from the
site where I applied sylgard. This makes the tetrodes more prone to bending
when being advanced into the brain. This happened several times when I was
inserting them, and each time I had to reverse the tetrodes and re-insert them
more slowly.

1331 - tetrodes are at 820 from pia, waiting for brain to stabilize and mouse
to awaken.

1340 - 820um still, clear visually-evoked responses.

1345 - 889um, good spikes on TT4

1346 - 980um, large fast spikes on TT4, some on TT3
then the mouse started moving around and the spikes went away, all is quiet now.

1350 - 1100um, still mostly quiet

1356 - 1412um, starting to getmany spikes on TT4 - probably hippocampus

1400 - 1684um, spikes are gone. Probably through hippocampus and about to reach the thalamus. I am going to let the brin rest for a few minutes here.



1416 - 1747um - looks like the beginnings of sound responses,

1445 - 2625um - I have been advancing, searching for laser and sound responses
without luck. I just hit a giant poplation of fast spiking, non sound-responseive
cells that went nuts when I pushed through them. Much quieter on the other side.
I wonder where I am...


1454 - at 3000um, no good spikes, no sound responses. I will wait here for a few
minutes for things to settle, then continue on for about another 1000um before
moving to a more medial site

1535 - 4200um, no sound responses here. Removing the electrodes and trying a new spot.

I am realizing now that my recording site was very lateral in the craniotomy.

I have re-inserted it more medially, closer to the center of the craniotomy.

1542 - tetrodes at 703um, waiting for 10 mins

1554 - 895um, visually evoked responses

1555 - 1009um, many spikes on TT4

1556 - 1150um, more large spikes

1557 - 1445um, more large spikes

1558 - 1618um, spikes on TT4 are gone

1601 - 2000um, waiting for things to settle before moving on.

1645 - 3000um, no sound or laser responses. Waiting for a few mins before moving on.

'''

from jaratoolbox.test.nick.database import cellDB
rd = cellDB.Experiment('pinp007', '2015-11-18', 'nick', 'more_sounds_tuning')

site1 = rd.add_site(depth = 3100, tetrodes = [3, 4, 5, 6])
site1.add_session('16-56-20', None, 'NoiseBurst') #Amplitude at 0.02, onset and offset responses on TT4
site1.add_session('16-59-10', None, 'LaserPulse') #Paradigm=laser_tuning_curve, 1mW  - Responds but is then inhibited, TT4
site1.add_session('17-02-10', None, 'LaserTrain') #Paradigm=laser_tuning_curve, 1mW  -
site1.add_session('17-07-37', 'a', 'AM') # Cool offset responses





site2 = rd.add_site(depth = 3300, tetrodes = [3, 4, 5, 6])
site2.add_session('17-52-33', None, 'NoiseBurst') #Amplitude at 0.02,

site2.add_session('17-55-32', None, 'LaserPulse') #Paradigm=laser_tuning_curve, 1mW  - Fast response and then inhibited
site2.add_session('17-58-23', None, 'LaserPulse') #Paradigm=laser_tuning_curve, 1mW  -
site2.add_session('18-02-53', 'b', 'AM') #


site3 = rd.add_site(depth = 3463, tetrodes = [3, 4, 5, 6])
site3.add_session('18-37-51', None, 'NoiseBurst') #Amplitude at 0.02,
site3.add_session('18-40-23', None, 'LaserPulse')
site3.add_session('18-42-33', None, 'LaserTrain')
site3.add_session('18-49-14', 'c', 'AM') #

site4 = rd.add_site(depth = 3582, tetrodes = [3, 4, 5, 6])
site4.add_session('19-15-56', None, 'NoiseBurst') #Still mostly on and offset resp.
site4.add_session('19-20-01', None, 'LaserPulse')
site4.add_session('19-23-55', None, 'LaserTrain')
site4.add_session('19-28-25', 'd', 'AM')


'''
1954 - removing the tetrodes and calling it a day.
'''




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
