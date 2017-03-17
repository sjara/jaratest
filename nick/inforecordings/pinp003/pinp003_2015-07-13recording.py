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

'''
Impedence measurement

TT3 - 472, 576, 301, 510
TT4 - 285, 384, 383, 406
TT5 - 361, 355, 369, 326
TT6 - 550, 260, 270, 270


Laser calibration

1.9 - 1.0mW
2.15 - 1.5mW
2.4 - 2.0mW
2.65 - 2.5mW
2.92 - 3.0mW
3.15 - 3.5mW

1819hrs - mouse on the rig, tetrodes at 1010um. 
I am recording from the right well, more laterally than the last recordings but still in the middle of the well in the A-P direction. The bone is re-growing, so I am at the most medial possible site at this A-P location. The site is almost in the very center of the well. Additionally, the tetrodes are on the lateral side of the optical fiber, so this limits how close I will be able to get to the previous good recording sites.  
'''

rd= cellDB.Experiment('pinp003', '2015-07-13', 'nick', 'laser_tuning_curve')
# dbFn='/home/nick/data/database/nick_thalamus_cells.json'

# dbFn='/home/nick/data/database/pinp003_thalamus_cells.json'

# db = cellDB.CellDB()
# db.load_from_json(dbFn)

# gc = []


'''
At 1010 um there are good spikes on TT4 and some on TT5. It is hard to tell whether or not they are visually-responsive. THey have wide waveforms and are spiking very fast. 

At 1119 um there are visually-responsive spikes on TT5. THe spikes on TT4 went away. 

At 1772 um there are large spikes on TT6

at 1840um there was a ton of activity and screetching (cell death noises)

By 2060um it is much quieter. 

at 2435 there are spikes on TT6 again (the longest tetrode). I am going to wait here for 5 mins for the brain to settle and then start to evaluate sound responses. 

No sound responses here, moving further. 

Testing sound responses at 2564um

No sound responses yet. Moved to 3005um, waiting 5 mins for things to settle. 

There is a weak sound response at 3203um. It looks like it might be only a single cell or possibly noise artifact, although I do not hear any artifact through the speaker. It is on TT6. Testing laser responses. I see a single huge spike right after laser onset on all of the channels, so it is probably photovoltaic effect. File = 2015-07-13_19-05-32
The laser-evoked spike seems to be followed by a powerful silencing effect. I will record another noise-burst session and then a tuning curve here to see if we get anything. We are still shallow but i havent been to this area before so I dont't know what to expect. 

'''

# site1 = rd.add_site(depth = 3203, tetrodes = [6])
# s1s1 = site1.add_session('19-05-32', None, sessionTypes['lp'])

# #The below ephys session is incorrectly named
# s1s2 = site1.add_session('19-05-32', 'a', sessionTypes['nb']) #amp = 0.4


'''
THe sound response here is so weak/possibly not there that I am going to keep moving. 
'''
site2 = rd.add_site(depth = 3700, tetrodes = [5, 6])
site2.add_session('20-11-35', None, sessionTypes['nb'])
site2.add_session('20-21-34', None, sessionTypes['lp']) #Laser at 3mW
site2.add_session('20-26-48', None, sessionTypes['lp']) #Laser at 1mW
site2.add_session('20-32-21', None, sessionTypes['lt'])
site2.add_session('20-37-10', 'b', sessionTypes['tc'])




'''
I am going to keep moving. 
'''
site3 = rd.add_site(depth = 3751, tetrodes = [5, 6])
site3.add_session('21-11-00', None, sessionTypes['nb']) #Responses on TT6, maybe TT5
 
site3.add_session('21-14-05', None, sessionTypes['lp']) #Laser at 1mW
site3.add_session('21-16-36', None, sessionTypes['lt']) #Laser at 1mW
site3.add_session('21-20-28', 'c', sessionTypes['tc']) #regular TC
site3.add_session('21-34-28', 'd', sessionTypes['tc']) #zooming in on bf
#5000-22000, 16freqs, 20-50db, 4intensities, 0.1duration, 0.8isi

# gc.append(sitefuncs.find_good_clusters(site3, 'site3', soundInd = 0, laserInd=1))

# site3.add_cluster(6, 9, comments='Responses to Laser Trains')
# site3.add_cluster(6, 11, comments='Responses to Laser Trains')
# db.add_clusters(site3.clusterList)

# site3.add_cluster(6, 5)
# db.add_clusters(site3.clusterList)

# site4 = rd.add_site(depth = 3901, tetrodes = [5, 6])
# site4.add_session('21-54-42', None, sessionTypes['nb'])
# site4.add_session('21-58-54', 'e', sessionTypes['tc']) #BF still between 5 and 9



'''
Still getting best frequencies around 5-9kHz. Removing the electrodes at 2210hrs and putting the mouse away
'''


# db.write_to_json(dbFn)


noiseBurstType = 'noiseBurst'
laserPulseType = 'laserPulse'
experimentObj = rd

siteNums = [3]

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
