lengths = {'TT3':230, 'TT4':230, 'TT5':0, 'TT6':100}

impedence = {
    'TT3':[339, 230, 296, 397],
    'TT4':[120, 334, 121, 343],
    'TT5':[326, 218, 327, 326],
    'TT6':[184, 328, 261, 345]}



lasercalibration = {
    0.2:1.00,
    0.5:1.55,
    1.0:2.50,
    1.5:3.25,
    2.0:3.90,
    2.5:4.40,
    3.0:4.80}


'''

2001hrs - electrodes are in the brain at 639um. The last recording was conducted near the center of the craniotomy, and I hit the visual thalamus. I moved to the very back of the craniotomy in the hope that I just needed to be a bit more posterior. This recording is in the back of the craniotomy (AP) and the middle (ML).


676um - spikes on TT5, sound like they respond ot the light. 

806um - large spikes TT5 respond to flashlight



1482um - giant spikes TT5, hippocampus probably

2000um, letting the brain rest for 5 mins


'''


from jaratoolbox.test.nick.database import cellDB
rd = cellDB.Experiment('pinp008', '2016-01-08', 'nick', 'am_tuning_curve')

site1 = rd.add_site(depth = 3100, goodTetrodes = [5])
site1.add_session('20-19-40', 'nb1', 'NoiseBurst') #
site1.add_session('20-22-29', 'lp1', 'LaserPulse') #1mW No laser response
#Also tried 1.5mW, no laser response. Moving on

site2 = rd.add_site(depth = 3402, goodTetrodes = [5, 6])
site2.add_session('20-51-44', 'nb2', 'NoiseBurst') # Not much of a response on TT5, good response on 6 - response on 5 my be masked by noise
site2.add_session('20-54-35', 'lp2', 'LaserPulse') #1.5mW - good response
site2.add_session('20-57-23', 'lt2', 'LaserTrain') #1.5mW - good response
site2.add_session('21-00-29', 'am2', 'AM') #
#Some changes during the recording possible, but still really nice responses
site2.add_session('21-28-12', 'tc2', 'tuningCurve') #Tuning around 6


site3 = rd.add_site(depth = 3452, goodTetrodes = [5, 6])
site3.add_session('21-42-54', 'nb3', 'NoiseBurst') #
site3.add_session('21-45-24', 'lp3', 'LaserPulse') #1.5mW
site3.add_session('21-47-52', 'lt3', 'LaserTrain') #1.5mW
site3.add_session('21-51-24', 'am3', 'AM') #Craziness, stopped after 432 trials. Ground problems???

#Going to re-record a new site without moving. 



site4 = rd.add_site(depth = 3452, goodTetrodes = [5, 6])
site4.add_session('22-12-30', 'nb4', 'NoiseBurst') #
site4.add_session('22-15-32', 'lp4', 'LaserPulse') #1.5mW
site4.add_session('22-18-10', 'lp4.2', 'LaserPulse2') #2.5mW Still no response on TT6, which is the tetrode with the sound responses. I am going to try to move a bit


#3600 - not much laser response, some long-latency laser responses which is strange. 


#3650um - obvious long-latency laser responses (22-24-09). I am going to try to just shine the light in the box and see what happesn

#22-27-28 - light shining through other fiber optic cable, obvious visual responses on TT5 - where am I? Not much going on on TT6

#3750 - no more sound responses. I am going to wrap it up for today. 

