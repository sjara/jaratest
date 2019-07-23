lengths = {'TT4':0, 'TT3':159, 'TT5':159, 'TT6':0}

impedence = {
    'TT3':[143, 321, 164, 180],
    'TT4':[248, 271, 291, 194],
    'TT5':[250, 589, 394, 198],
    'TT6':[243, 264, 175, 262]}



lasercalibration = {
    0.2:0.75 
    0.5:1.25,
    1.0:2.15,
    1.5:2.70,
    2.0:3.25,
    2.5:3.75,
    3.0:4.2}


'''
THALAMUS RECORDING
1147 - mouse is on rig with tetrodes in the right craniotomy. This recording site is on the posterior side of the well at about 7 o clock. My intention was to be posterior and medial of the center, where we were seeing visual responses before. 


1156 - 706um - nice spikes on tt4 that are responsive to the flashlight but not to noise bursts at 60dB. 
they also do not respond to laser pulses at 1mW.

746um - good spikes, collecting laser responses - 12-00-32
Not very stable but some long-latency responses to the laser pulses - could be visual. 

We switched the laser cable so that the pulses were just flashing in the box instead of going into the fiber. We recorded some trials - 12-08-13
There are clear responses on TT4 with a latency of about 50 msec.

We still need to determine whether the long-latency responses we see when the laser is coupled to the fiber is due to leakage around the fiber coupling (through the front of the eyes) or that the light is exciting the retina through the back. 

###### visual cortex experiments ##########
12-18-22 - pre light block, laser coupled to fiber. 

12-30-09 - light block in front of mouse's eyes - no laser responses

12-31-31 - light block removed - laser responses again. 

12-36-49 - does visual cortex respond to noise bursts? no
#####################

1239 - moving down. 

1241 - 1060um - all is quiet. We have passed the cortex. 

1241 - 1171um - small spikes on TT4
12-42-45 - sample of the small spikes for analysis - are they axons?

1245 - 1229um, huge rhythmic spikes on TT5
12-44-45 - sample for later analysis


1248 - 1434um - large spikes again on TT4 - also LFP that might indicate we are getting close to hippocampus
12-48-20 - sample
12-49-25 - another sample from 1459um with what I think are sharp wave ripples

1251 - 1509um - cells are starting to scream on TT4, I think i am hitting CA1

12-51-11 - recording as I move from 1500 to 1700um, showing loud cells and then quiet afterwards.

12-53-39 - 1705um - TT4 is past but there are spikes on TT5 and 6 - does the hippocampus respond to noise bursts at 60dB? 

12-54-59 - 1705um - laser pulses at 1mW - there are some visual-type responses here on TT5 and 6. 

##

1259 - still quiet on TT4, we have arrived at 2000um. Letting things settle for 5 mins. 


1312 - 2200um - spikes on TT4 - no clear responses to noise bursts yet.

1319 - 2400 - spikes on TT4, 5, 6. No sound responses. There are some long-latency laser responses.
13-19-25 laser pulses at 1mW

1327 - 2602um hint of sound responses on TT5, waiting for a few mins for things to settle and I will re-test

13-30-42 - noise bursts, 2602um - sound responses on TT5
13-32-15 - laser pulses at 1mW, 2602um - still long-latency laser responses


1340 - 3000um - all quiet, letting things rest for a few minutes

1347 - the sweet sweet sound of multi-unit noise responses in the background. No good spikes yet. I will move a little to try and find some spikes. 

1350 - 3050um - beginnings of sound responses on TT4 - will keep moving to find better spikes

13-51-05 - noise bursts at 3101um, Clear but strange looking sound responses on tt4. Testing laser

13-54-14 - laser pulses at 1mW

13-56-38 - laser pulses at 0.2soa (10Hz) 

13-59-37 - tuningAM, behavior = a (Starting a site below)
'''



from jaratoolbox.test.nick.database import cellDB
rd = cellDB.Experiment('pinp007', '2015-12-02', 'nick', 'am_tuning_curve')

site1 = rd.add_site(depth = 3101, tetrodes = [4, 6])
site1.add_session('13-51-05', None, 'NoiseBurst') #
site1.add_session('13-54-14', None, 'LaserPulse') #
site1.add_session('13-56-38', None, 'LaserTrain') # 1mW
site1.add_session('13-59-37', 'a', 'AM') #
site1.add_session('14-28-13', None, 'LaserTrain0.5mW') # 0.5mW
site1.add_session('14-31-49', None, 'LaserTrain0.2mW') # 0.2mW Neurons still responsive at this lower laser power
site1.add_session('14-35-30', None, 'LaserPulse0.2mW') #
site1.add_session('14-38-44', None, 'LaserPulse0.2mWOutsideBrain') #0.2mW laser pulses through the other cable

'''
Some weak long-latency visual responses on TT6 - none on TT4 at the low power.




'''
#The threshold at this site is higher, hopefully leads to better clustering for tt4
site2 = rd.add_site(depth = 3150, tetrodes = [4])
site2.add_session('14-45-15', None, 'NoiseBurst') #
site2.add_session('14-47-43', None, 'LaserPulse') # 0.2mW
site2.add_session('14-50-11', None, 'LaserPulse2') # 1mW
site2.add_session('14-52-44', None, 'LaserTrain') # 1mW
site2.add_session('14-56-18', 'b', 'AM') #

site3 = rd.add_site(depth = 3250, tetrodes = [4])
site3.add_session('15-24-42', None, 'NoiseBurst') #
site3.add_session('15-27-29', None, 'LaserPulse') #1mW
site3.add_session('15-29-37', None, 'LaserTrain') #1mW
site3.add_session('15-32-33', 'c', 'AM') #
site3.add_session('15-57-23', 'd', 'TuningCurve') #

site4 = rd.add_site(depth = 3431, tetrodes = [4])
site4.add_session('16-15-45', None, 'NoiseBurst') # Thresholds at 39mV
site4.add_session('16-18-34', 'lpa', 'LaserPulse') # 1mW
site4.add_session('16-21-13', 'lta', 'LaserTrain') # 1mW
site4.add_session('16-24-14', 'e', 'AM') # 1mW
site4.add_session('16-50-17', 'f', 'TuningCurve') # 1mW


site5 = rd.add_site(depth = 3554, tetrodes = [4, 6])
site5.add_session('17-03-37', None, 'NoiseBurst') # Thresholds at 42mV
site5.add_session('17-05-59', None, 'LaserPulse') # 1mW
site5.add_session('17-08-15', None, 'LaserTrain') # 1mW
site5.add_session('17-11-32', 'g', 'AM') # 1mW
site5.add_session('17-37-55', 'h', 'TuningCurve') # 1mW

site6 = rd.add_site(depth = 3663, tetrodes = [4, 6])
site6.add_session('17-56-48', None, 'NoiseBurst') # Thresholds at 42mV
site6.add_session('18-00-27', 'lpi', 'LaserPulse') # 1mW



noiseBurstType = 'NoiseBurst'
laserPulseType = 'LaserPulse'
experimentObj = rd

siteNums = [1, 2, 4, 5, 6]

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
