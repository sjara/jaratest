from jaratoolbox import celldatabase

subject = 'pinp009'
experiments = []

exp0 = celldatabase.Experiment(subject, '2016-01-27')
experiments.append(exp0)

# ac = cellDB.Experiment('pinp009', '2016-01-27', experimenter='nick', defaultParadigm='am_tuning_curve')
# site1 = ac.add_site(depth=707, tetrodes=[6])

exp0.add_site(707, tetrodes=[6])
exp0.add_session('16-33-48', None, 'NoiseBurst', 'am_tuning_curve')
exp0.add_session('16-36-03', None, 'LaserPulse', 'am_tuning_curve') #0.2mW
exp0.add_session('16-38-50', None, 'LaserTrain', 'am_tuning_curve') #0.2mW
exp0.add_session('16-42-10', 'aca', 'AM', 'am_tuning_curve') # Stopped after 440 trials - rate coding motha
exp0.add_session('17-02-02', None, 'LaserPulse2', 'am_tuning_curve') # 
exp0.add_session('17-04-24', None, 'LaserTrain2', 'am_tuning_curve') # 

# site2 = ac.add_site(depth=863, tetrodes=[4, 5, 6])

exp0.add_site(863, tetrodes=[4, 5, 6])
exp0.add_session('17-14-57', None, 'NoiseBurst', 'am_tuning_curve')
exp0.add_session('17-17-35', None, 'LaserPulse', 'am_tuning_curve') #0.2-0.5mW
exp0.add_session('17-19-44', None, 'LaserTrain', 'am_tuning_curve') #0.2-0.5mW
exp0.add_session('17-23-19', 'acb', 'AM', 'am_tuning_curve')
exp0.add_session('17-42-52', None, 'LaserPulse2', 'am_tuning_curve') #0.2-0.5mW
exp0.add_session('17-45-04', None, 'LaserTrain2', 'am_tuning_curve') #0.2-0.5mW
exp0.add_session('17-49-18', 'acc', 'TuningCurve', 'am_tuning_curve') #only 60dB
exp0.add_session('17-53-22', 'acd', 'TuningCurve2', 'am_tuning_curve') #30-60dB


