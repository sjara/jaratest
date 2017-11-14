'''
Notes

1831hrs - mouse is on the rig with the electrodes in the middle of the right thalamus well. There is one bundle of electrodes that is a little more anterior, and one single electrode that is more posterior, so we are going to go to several different places today.

There are clear visual responses at 1000um on TT4. 

Awesome signals between 1500 and 2000um - probably hippocampus. 

Waiting at 2500um for 5 mins so the brain can settle. 

1856hrs - started testing for sound responses at 2600um, now at 2750. No responses yet. Very quiet in general. 

1907hrs - 3150um. Some small sound responses to noise bursts on TT4. file = 19-03-16
Testing laser response. There is a sort of buzzing noise when the laser is on. 
I see laser responses that do not sustain for the duration of the pulse. 

I will move another 50um to get better responses. 

1912hrs - 3200um Excellent cells on TT4, I am recording 100 trials of noise because I think it will be good. File = 19-12-32

TT4 has excellent noise responses. I am testing laser responses now. file = 19-14-54

Strange responses - TT4 has a response to the laser 100msec after the onset. It could be a laser ofset response, except that it does not look locked to the offset very sharply. Testing with trains of pulses. file = 19-17-44

Interesting responses on all tetrodes. I am recording a tuning curve. 30-60db, 2-40kHz
File = 19-22-06 
There does not appear to be any noise on the ephys. 

I presented 100 trials of 7-8kHz at 60dB. It is sad to leave such a nice cell, but I want better laser responses. 

1942hrs - at 3250um, waiting 5 mins before moving any farther. 

1949hrs - Cells on T4 that respond to sounds, with a latency of about 20-30ms. Testing laser pulses. 
Awesome laser responses at this site. I am recording laser trains now. File = 19-49-40
The cell/s on TT4 look like they may be directly excited. I am recording a tuning curve. 


'''

impedences = {
3: [395, 420, 599, 427], 
4: [321, 519, 537, 495], 
5: [253, 489, 454, 549], 
6: [484, 281, 523, 487]}

laser_calib = {
1: 1.75, 
1.5: 1.9, 
2: 2.05, 
2.5: 2.2, 
3: 2.3, 
3.5: 2.5}

from jaratoolbox.test.nick.database import cellDB
rd = cellDB.Experiment('pinp005', '2015-07-30', 'nick', 'laser_tuning_curve')

site1 = rd.add_site(depth = 3200, tetrodes = [3, 4, 5, 6])

site1.add_session('19-12-32', None, 'NoiseBurst')
site1.add_session('19-14-54', None, 'LaserPulse')
site1.add_session('19-17-44', None, 'LaserTrain')
site1.add_session('19-22-06', 'a', 'TuningCurve')
site1.add_session('19-35-43', None, 'BestFreq') #7000-8000 2 freqs at 60dB

site2 = rd.add_site(depth = 3250, tetrodes = [3, 4, 5, 6])
site2.add_session('19-43-32', None, 'NoiseBurst')
site2.add_session('19-47-14', None, 'LaserPulse') #Sweet laser responses on TT4
site2.add_session('19-49-40', None, 'LaserTrain')
site2.add_session('19-53-23', 'b', 'TuningCurve') #30-60dB, 2-40kHz
site2.add_session('20-07-03', 'c', 'QuietTuningCurve') #20-50dB, 2-40kHz
site2.add_session('20-19-09', 'd', 'RepeatTuningCurve') #40-60dB, 2-40kHz
#The threshold has shifted up by the second TC session
site2.add_session('20-32-48', 'e', 'BestFreq') #7000-8000, 60dB


site3 = rd.add_site(depth = 3370, tetrodes = [3, 4, 5, 6])
site3.add_session('20-41-13', None, 'NoiseBurst') #Some responses still on TT4 - have we not really moved?
site3.add_session('20-46-28', None, 'LaserPulse') #Crazy responses on all tetrodes. 
site3.add_session('20-49-17', None, 'LaserTrain') #Still some crazy responses on all tetrodes. 
site3.add_session('20-53-19', 'f', 'TuningCurve') #40-60dB, 2-40kHz Crappy TC.


site4 = rd.add_site(depth = 3460, tetrodes = [3, 4, 5, 6])
site4.add_session('21-08-38', None, 'NoiseBurst') #Some responses on TT4 that might be different
site4.add_session('21-12-27', None, 'LaserPulse') #TT4 has responses that look like they may be direct
site4.add_session('21-15-42', None, 'LaserTrain') #Some weak responses on T4. May get better with clustering.
site4.add_session('21-19-30', 'g', 'TuningCurve') #TT4 is tuned but the threshold is high.
site4.add_session('21-33-42', 'h', 'LoudTuningCurve') #40-70dB, 2-40kHz
site4.add_session('21-46-11', None, 'BestFreq') #7-8kHz at 70dB for 100 trials


'''
2113hrs - 3460um. I have been moving down to try to get away from site 3. Site 4 has different neurons for sure but may still be getting some of the neurons from site 3 (if this is possible, we may not really have moved much)
For site4 the second tuning curve is better. I think we can use this to calculate the BW20
I am moving on...

Sound responses at 3600 are weaker. Continuing to move
'''

site5 = rd.add_site(depth = 3675, tetrodes = [3, 4, 5, 6])
site5.add_session('22-05-24', None, 'NoiseBurst') #Good responses on TT4
site5.add_session('22-07-44', None, 'LaserPulse') # Not very laser responsive
site5.add_session('22-10-33', None, 'LaserTrain') #Way more laser responsive than the last session. I accidentally added several extra events to the end when I tried to start the session below
site5.add_session('22-14-59', None, 'LaserPulse') # Repeating the pulses because it was so responsive in the last session
#It hardly responds at all to the single pulses

site5.add_session('22-18-20', 'i', 'TuningCurve') # 30-70dB 5 ints, 2-40kHz 16 freqs. 800 trials total
site5.add_session('22-34-36', None, 'BestFreq') # 7000-8000Hz, 70dB


site6 = rd.add_site(depth = 3750, tetrodes = [3, 4, 5, 6])
site6.add_session('22-37-41', None, 'NoiseBurst') # Good responses on TT4, some on T5 and 6
site6.add_session('22-39-45', None, 'LaserPulse') # Best responses are on TT5
site6.add_session('22-42-03', None, 'LaserTrain') # 
site6.add_session('22-47-37', 'j', 'TuningCurve') # 2-40, 40-70 8 ints
site6.add_session('23-12-05', 'k', 'TuningCurveLower') #2-40, just 30dB, 160 trials (10 each freq)
#I can start to hear some ringing from the speaker because the ground is getting dry
site6.add_session('23-17-35', 'l', 'TuningCurveLower_again') #Doing the same thing again with saline in the wells

'''
2323hrs - 3748um. I am removing the electrodes and taking the mouse home. 
'''

noiseBurstType = 'NoiseBurst'
laserPulseType = 'LaserPulse'
experimentObj = rd

siteNums = [1, 2, 3, 4, 5, 6]

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
