'''

Recording in AC!!!

TO DO: We need to be able to know where a recording came from just from the cluster information in the future. 

'''

lengths = {'TT3':230, 'TT4':230, 'TT5':0, 'TT6':100}

impedence = {
    'TT3':[440, 277, 351, 529],
    'TT4':[147, 423, 148, 393],
    'TT5':[354, 213, 381, 338],
    'TT6':[211, 330, 317, 372]}



lasercalibration = {
    0.2:1.00,
    0.5:1.55,
    1.0:2.50,
    1.5:3.30,
    2.0:4.00,
    2.5:4.50,
    3.0:4.90}


'''

Electrodes are in roughly the center of the new AC craniotomy, and are at 636um. Some spikes but not sound or laser responsive.

1250um - very laser responsive but not many spikes otherwise. No sound responses. 

1550 - also very large laser responses that do not really look like spikes. very short latency


1641 - quiet of spikes but still the giant laser response


2000um - nothing anymore. in pinp005 we saw fortical responses around 1400um, so I am going to remove the electrodes and move them more lateral. 



I re-inserted the tetrodes in the posterior-lateral corner of the well. They are currently at 419um

1000um - no sound or laser responses yet. I am waiting here for the brain to settle for a few mins.

1400um - nothing yet
 1950um - there is nothing here, I am going to call it a day.

'''