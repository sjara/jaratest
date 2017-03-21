lengths = {'TT4':0, 'TT3':159, 'TT5':159, 'TT6':0}

impedence = {
    'TT3':[35.6, 88.2, 75.9, 54.4],
    'TT4':[29.2, 70.3, 65.8, 51.5],
    'TT5':[91, 61.8, 87.3, 110],
    'TT6':[103, 37.8, 184, 67.8]}



lasercalibration = {
    0.5:0.90,
    1.0:1.40,
    1.5:1.90,
    2.0:2.35,
    2.5:2.75,
    3.0:3.05}


'''
1112 - 931um - Mouse is on the rig with the tetrodes in the Right craniotomy. Waiting for 10 mins for the mouse to wake up and the brain to settle


1129 - 931um - possible background visual responses


The electrode impedences must be way too low - I cannot pick up any spikes. I can hear multi-unit activity but I need to remove the electrodes and try cutting them again. 
'''

lengths = {'TT3':117, 'TT4':0, 'TT5':117, 'TT6':0}

impedence = {
    'TT3':[399, 445, 447, 500],
    'TT4':[329, 398, 453, 340],
    'TT5':[508, 482, 292, 294],
    'TT6':[512, 330, 405, 345]}



'''

1342 - 877um - mouse is back on the rig with tetrodes in the right craniotomy again,
waiting 10 mins. Excellent visually-responsive neurons

1349 - 1171um - quiet

1353 - 1680um - lots of spikes on TT4, 5, 6

1354 - 1820um - probably through CA1

1406 - 2989 - had many spikes, just got quiet again - waiting for 5 mins

1418 - 3117um - good laser responses on TT4 but no sound responses yet


'''

from jaratoolbox.test.nick.database import cellDB
rd = cellDB.Experiment('pinp007', '2015-11-25', 'nick', 'am_tuning')

site1 = rd.add_site(depth = 3750, goodTetrodes = [3, 4, 5, 6])
site1.add_session('14-44-56', None, 'NoiseBurst') #
site1.add_session('14-48-12', None, 'LaserPulse') #
site1.add_session('14-51-18', None, 'LaserTrain') #
site1.add_session('15-07-13', 'a', 'AM') #


'''
2mw - 15-40-02
1mw - 15-43-38
0.5mw - 15-46-52
less - 

05mW, 0.1sec soa - 

16-08-30 0.05sec soa, all the responses blend together
16-11-58 - 0.1sec soa, 0.5mW BUT with the filter engaged.




1618 - We have determined that the site we are recording from responds to visual stimuli. The site
seemed laser responsive, but at long latency and would respond each time to a train of laser pulses

The neurons here respond to the flashlight.

I am calling it a day and removing the electrodes


'''