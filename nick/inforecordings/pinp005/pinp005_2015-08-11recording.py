impedences = {
3: [213, 212, 225, 284], 
4: [386, 213, 299, 345], 
5: [244, 228, 332, 237], 
6: [271, 229, 274, 202]}



laser_calib = {
    1:2.0,
    1.5:2.3,
    2:2.55,
    2.5:2.85,
    3:3.15, 
    3.5:3.4}

'''
Recording laser artifact first
'''

la = Experiment('noisetest', '2015-08-11', 'nick', 'laser_tuning_curve')

site1 = la.add_site(depth=0, tetrodes = [3, 4, 5, 6])
site1.add_session('15-01-41', None, 'LaserPulse2.5mW')
site1.add_session('15-03-52', None, 'LaserPulse3.5mW')
site1.add_session('15-06-20', None, 'LaserPulse1.5mW')


'''
Recording from the middle of the left thalamus well.
1533hrs - mouse is on the rig with the electrodes at 1535um. Not much activity except for movement-related noise. No obvious visual responses yet. 

at 1556um there are cells on T6 - obvious visual responses. 
spikes between 1600 and 1900um, now silence



'''

rd = Experiment('pinp005', '2015-08-11', 'nick', 'laser_tuning_curve')

site2 = rd.add_site(depth=3001, tetrodes = [3, 4, 5, 6])

'''
Went all the way to 3700um - long latency laser responses, fast spikes, not much we want here. I am going to remove the electrodes and do another penetration more medially.

1646hrs - Electrodes are now in the most medial location (ML) and centered in the craniotomy (AP). 

Went all the way to 4100um - no robust sound responses and no laser responses at all. I found fast spikes with thin waveforms. I am removing the electrodes and finding a new spot


I am re-inserting the electrodes more anterior near the middle (ML) of the craniotomy. 

I am at 2139um and I do not see anything yet. 
Now there is a lot of activity on T3 at 2299um. 

Some responses to the laser (long latency) at 3200, but no responses to the sound.

No responses to sound by 3623um

No responses to laser or sound by 4024um. I am removing the electrodes for now. 
'''
