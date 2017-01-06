from jaratoolbox import celldatabase

subject = 'pinp007'
experiments = []

# rd = cellDB.Experiment('pinp007', '2015-11-18', 'nick', 'more_sounds_tuning')
exp0 = celldatabase.Experiment(subject, '2015-11-18')
experiments.append(exp0)

# site1 = rd.add_site(depth = 3100, tetrodes = [3, 4, 5, 6])

exp0.add_site(3100, tetrodes=[3, 4, 5, 6])
exp0.add_session('16-56-20', None, 'NoiseBurst', 'more_sounds_tuning') #Amplitude at 0.02, onset and offset responses on TT4
exp0.add_session('16-59-10', None, 'LaserPulse', 'laser_tuning_curve') #Paradigm=laser_tuning_curve, 1mW  - Responds but is then inhibited, TT4
exp0.add_session('17-02-10', None, 'LaserTrain', 'laser_tuning_curve') #Paradigm=laser_tuning_curve, 1mW  -
exp0.add_session('17-07-37', 'a', 'AM', 'more_sounds_tuning') # Cool offset responses

# site2 = rd.add_site(depth = 3300, tetrodes = [3, 4, 5, 6])

exp0.add_site(3300, tetrodes=[3, 4, 5, 6])
exp0.add_session('17-52-33', None, 'NoiseBurst', 'more_sounds_tuning') #Amplitude at 0.02,
exp0.add_session('17-55-32', None, 'LaserPulse', 'laser_tuning_curve') #Paradigm=laser_tuning_curve, 1mW  - Fast response and then inhibited
exp0.add_session('17-58-23', None, 'LaserPulse', 'laser_tuning_curve') #Paradigm=laser_tuning_curve, 1mW  -
exp0.add_session('18-02-53', 'b', 'AM', 'more_sounds_tuning') #

# site3 = rd.add_site(depth = 3463, tetrodes = [3, 4, 5, 6])

exp0.add_site(3463, tetrodes=[3, 4, 5, 6])
exp0.add_session('18-37-51', None, 'NoiseBurst', 'more_sounds_tuning') #Amplitude at 0.02,
exp0.add_session('18-40-23', None, 'LaserPulse', 'more_sounds_tuning')
exp0.add_session('18-42-33', None, 'LaserTrain', 'more_sounds_tuning')
exp0.add_session('18-49-14', 'c', 'AM', 'more_sounds_tuning') #

# site4 = rd.add_site(depth = 3582, tetrodes = [3, 4, 5, 6])

exp0.add_site(3582, tetrodes=[3, 4, 5, 6])
exp0.add_session('19-15-56', None, 'NoiseBurst', 'more_sounds_tuning') #Still mostly on and offset resp.
exp0.add_session('19-20-01', None, 'LaserPulse', 'more_sounds_tuning')
exp0.add_session('19-23-55', None, 'LaserTrain', 'more_sounds_tuning')
exp0.add_session('19-28-25', 'd', 'AM', 'more_sounds_tuning')

exp1 = celldatabase.Experiment(subject, '2015-12-02')
experiments.append(exp1)

#The threshold at this site is higher, hopefully leads to better clustering for tt4
# site2 = rd.add_site(depth = 3150, tetrodes = [4])

exp1.add_site(3150, tetrodes=[4])
exp1.add_session('14-45-15', None, 'NoiseBurst', 'am_tuning_curve') #
exp1.add_session('14-47-43', None, 'LaserPulse', 'am_tuning_curve') # 0.2mW
exp1.add_session('14-50-11', None, 'LaserPulse2', 'am_tuning_curve') # 1mW
exp1.add_session('14-52-44', None, 'LaserTrain', 'am_tuning_curve') # 1mW
exp1.add_session('14-56-18', 'b', 'AM', 'am_tuning_curve') #

# site3 = rd.add_site(depth = 3250, tetrodes = [4])

exp1.add_site(3250, tetrodes=[4])
exp1.add_session('15-24-42', None, 'NoiseBurst', 'am_tuning_curve') #
exp1.add_session('15-27-29', None, 'LaserPulse', 'am_tuning_curve') #1mW
exp1.add_session('15-29-37', None, 'LaserTrain', 'am_tuning_curve') #1mW
exp1.add_session('15-32-33', 'c', 'AM', 'am_tuning_curve') #
exp1.add_session('15-57-23', 'd', 'TuningCurve', 'am_tuning_curve') #

# site4 = rd.add_site(depth = 3431, tetrodes = [4])

exp1.add_site(3431, tetrodes=[4])
exp1.add_session('16-15-45', None, 'NoiseBurst', 'am_tuning_curve') # Thresholds at 39mV
exp1.add_session('16-18-34', 'lpa', 'LaserPulse', 'am_tuning_curve') # 1mW
exp1.add_session('16-21-13', 'lta', 'LaserTrain', 'am_tuning_curve') # 1mW
exp1.add_session('16-24-14', 'e', 'AM', 'am_tuning_curve') # 1mW
exp1.add_session('16-50-17', 'f', 'TuningCurve', 'am_tuning_curve') # 1mW

# site5 = rd.add_site(depth = 3554, tetrodes = [4, 6])

exp1.add_site(3554, tetrodes=[4, 6])
exp1.add_session('17-03-37', None, 'NoiseBurst', 'am_tuning_curve') # Thresholds at 42mV
exp1.add_session('17-05-59', None, 'LaserPulse', 'am_tuning_curve') # 1mW
exp1.add_session('17-08-15', None, 'LaserTrain', 'am_tuning_curve') # 1mW
exp1.add_session('17-11-32', 'g', 'AM', 'am_tuning_curve') # 1mW
exp1.add_session('17-37-55', 'h', 'TuningCurve', 'am_tuning_curve') # 1mW

