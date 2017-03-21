from jaratoolbox.test.nick.database import cellDB

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

impedence = {
'TT3' : [369, 389, 327, 362],
'TT4' : [356, 284, 291, 363],
'TT5' : [350, 334, 348, 292],
'TT6' : [428, 185, 242, 232]}


laserCalibration = {
'1.0mW':2.3, 
'1.5mW':2.8, 
'2.0mW':3.2, 
'2.5mW':3.5, 
'3.0mW':4.1, 
'3.5mW':4.45}

comments = []

paradigm = 'laser_tuning_curve'
rd = cellDB.Experiment('pinp003','2015-07-20','nick', 'laser_tuning_curve')

# dbFn='/home/nick/data/database/nick_thalamus_cells.json'
# db = cellDB.CellDB()
# db.load_from_json(dbFn)

dbFn='/home/nick/data/database/pinp003_thalamus_cells.json'

db = cellDB.CellDB()
db.load_from_json(dbFn)

gc = []

comments.append('0919hrs - mouse on rig with tetrodes at 1002um. I am in the previous best location, in the middle of the well (AP) and as close as possible to the medial wall. I have coated the electrodes with DiI and I will try to get as much good data from this site as possible this morning.')

comments.append('0936hrs - tetrodes are at 3004um, holding for 5 mins. No spikes from hippocampus on any tetrode on the way down - damaged tract from many recordings? I will keep moving deeper than I have gone today looking for sound and laser responses')

comments.append('0958hrs - there are tiny spikes at 3206um that appear to be responsive to the laser, not much response to 0.4amp noise. Re-testing with 0.5amp and more trials.  - Not obviously responsive, moving on')

site1 = rd.add_site(depth = 3425, tetrodes = [4, 5, 6])
site1.add_session('10-21-34', None, 'NB0.5')
site1.add_session('10-24-16', None, 'LP2.5')
site1.add_session('10-26-57', None, 'LT2.5')
site1.add_session('10-30-48', 'a', 'TC_2k-40k_16f_40-70_4ints')

gc.append(sitefuncs.find_good_clusters(site1, 'site1', soundInd = 0, laserInd=1))

#site1.generate_main_report()


comments.append('site 2 has a reference for the spikes as well as the LFPs. spikes = channel 14, lfp = channel 11')
site2 = rd.add_site(depth = 3451, tetrodes = [5, 6])
site2.add_session('10-58-42', None, 'LP2.5')
site2.add_session('11-01-08', None, 'LT2.5')
site2.add_session('11-05-29', None, 'NB0.3')
site2.add_session('11-08-42', 'b', 'TC_2k-40k_16f_40-70_4ints')
#site2.add_session('11-08-42', 'b', 'TC_2k-40k_16f_40-70_4ints')
site2.add_session('11-23-51', 'c', 'TC_3k-13k_16f_20-50_4ints')
#site2.generate_main_report()


gc.append(sitefuncs.find_good_clusters(site2, 'site2', soundInd = 2, laserInd=0))

# site2.add_cluster(6, 2, comments='Good sound responses, good tuning shapes')
# db.add_clusters(site2.clusterList)


site3 = rd.add_site(depth = 3602, tetrodes = [5, 6])
site3.add_session('11-51-31', None, 'NB0.3')
site3.add_session('11-54-05', None, 'LP2.5')
site3.add_session('11-56-36', None, 'LT2.5')
#synaptic excitation if anything at all, moving on

comments.append('1230hrs - no more sound responses at 4000um. I am removing the electrodes')

db.write_to_json(dbFn)


noiseBurstType = 'NB0.3'
laserPulseType = 'LP2.5'
experimentObj = rd

siteNums = [2, 3]

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
