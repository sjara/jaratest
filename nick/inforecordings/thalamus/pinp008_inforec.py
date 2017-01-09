from jaratoolbox import celldatabase

subject = 'pinp008'
experiments = []

# rd = cellDB.Experiment('pinp008', '2016-01-08', 'nick', 'am_tuning_curve')
exp0 = celldatabase.Experiment(subject, '2016-01-08')
experiments.append(exp0)

# site2 = rd.add_site(depth = 3402, tetrodes = [5, 6])

exp0.add_site(3402, tetrodes=[5, 6])
exp0.add_session('20-51-44', 'nb2', 'NoiseBurst', 'am_tuning_curve') # Not much of a response on TT5, good response on 6 - response on 5 my be masked by noise
exp0.add_session('20-54-35', 'lp2', 'LaserPulse', 'am_tuning_curve') #1.5mW - good response
exp0.add_session('20-57-23', 'lt2', 'LaserTrain', 'am_tuning_curve') #1.5mW - good response
exp0.add_session('21-00-29', 'am2', 'AM', 'am_tuning_curve') #
#Some changes during the recording possible, but still really nice responses
# exp0.add_session('21-28-12', 'tc2', 'tuningCurve', 'am_tuning_curve') #Tuning around 6


# site3 = rd.add_site(depth = 3452, tetrodes = [5, 6])

exp0.add_site(3452, tetrodes=[5, 6])
exp0.add_session('21-42-54', 'nb3', 'NoiseBurst', 'am_tuning_curve') #
exp0.add_session('21-45-24', 'lp3', 'LaserPulse', 'am_tuning_curve') #1.5mW
exp0.add_session('21-47-52', 'lt3', 'LaserTrain', 'am_tuning_curve') #1.5mW
exp0.add_session('21-51-24', 'am3', 'AM', 'am_tuning_curve') #Craziness, stopped after 432 trials. Ground problems???
