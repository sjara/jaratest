from jaratoolbox import celldatabase
experiments = []

laserCal = {
    '0.5':1.5,
    '1.0':1.3, #Mistake here??
    '1.5':1.75,
    '2.0':2.25,
    '2.5':2.9,
    '3.0':3.55
}

#Impedence between 1.5 and 2.5MOhm for all existing trodes, saved as csv

#Laser setting (on the dial, have to re-calibrate because I didn't go high enough
#Session

#100msec laser pulses, 0.5+/-0sec isi

#1.5 on dial - 1.6mW

exp0 = celldatabase.Experiment('lasertest', '2016-08-22')
experiments.append(exp0)
exp0.add_site(0)

#1.5 on dial, 1.7mW
exp0.add_session('16-03-24', None, '1.7mW', paradigm='am_tuning_curve')

#2.5 on dial - 2.7mW
exp0.add_session('16-05-57', None, '2.7mW', paradigm='am_tuning_curve')

#3.5 on dial - 3.3mW
exp0.add_session('16-06-50', None, '3.3mW', paradigm='am_tuning_curve')

#4.5 - 4.1mW
exp0.add_session('16-07-42', None, '4.1mW', paradigm='am_tuning_curve')

#5.5 - 4.9mW
exp0.add_session('16-08-33', None, '4.9mW', paradigm='am_tuning_curve')

#6.5 - 5.9mW
exp0.add_session('16-09-24', None, '5.9mW', paradigm='am_tuning_curve')

#7.5 - 6.5mW #72 trials
exp0.add_session('16-10-12', None, '4.9mW', paradigm='am_tuning_curve')

#8.5 - 6.9mW
exp0.add_session('16-11-20', None, '4.9mW', paradigm='am_tuning_curve')

#9.5 - 7.2mW
exp0.add_session('16-12-06', None, '4.9mW', paradigm='am_tuning_curve')

