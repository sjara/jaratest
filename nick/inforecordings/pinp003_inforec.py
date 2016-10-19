from jaratoolbox import celldatabase

subject = 'pinp003'
experiments = []

sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tc_heatmap',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse'}

exp0 = celldatabase.Experiment(subject, '2015-06-24')
experiments.append(exp0)

# site1 = today.add_site(depth = 3543, tetrodes = [6])

exp0.add_site(3543)
exp0.add_session('15-22-29', None, sessionTypes['nb'], 'laser_tuning_curve')
exp0.add_session('15-25-08', None, sessionTypes['lp'], 'laser_tuning_curve')
exp0.add_session('15-27-37', None, sessionTypes['lt'], 'laser_tuning_curve')
exp0.add_session('15-31-48', 'a', sessionTypes['tc'], 'laser_tuning_curve')
exp0.add_session('15-45-22', 'b', sessionTypes['bf'], 'laser_tuning_curve')


# site2 = today.add_site(depth = 3623, tetrodes = [6])

exp0.add_site(3623)
exp0.add_session('15-54-56', None, sessionTypes['nb'], 'laser_tuning_curve')
exp0.add_session('15-57-33', None, sessionTypes['lp'], 'laser_tuning_curve')
exp0.add_session('16-00-02', None, sessionTypes['lt'], 'laser_tuning_curve')
exp0.add_session('16-04-48', 'c', sessionTypes['tc'], 'laser_tuning_curve')
exp0.add_session('16-17-30', 'd', sessionTypes['bf'], 'laser_tuning_curve')
exp0.add_session('16-20-11', None, sessionTypes['3p'], 'laser_tuning_curve')
exp0.add_session('16-22-37', None, sessionTypes['1p'], 'laser_tuning_curve')


# site3 = today.add_site(depth = 3700, tetrodes = [6])

exp0.add_site(3700)
exp0.add_session('16-40-44', None, sessionTypes['nb'], 'laser_tuning_curve')
exp0.add_session('16-44-01', None, sessionTypes['lp'], 'laser_tuning_curve')
exp0.add_session('16-46-20', None, sessionTypes['lt'], 'laser_tuning_curve')
exp0.add_session('16-50-03', 'e', sessionTypes['tc'], 'laser_tuning_curve')
exp0.add_session('17-03-10', None, sessionTypes['bf'], 'laser_tuning_curve')
exp0.add_session('17-06-10', None, sessionTypes['3p'], 'laser_tuning_curve')
exp0.add_session('17-09-06', None, sessionTypes['1p'], 'laser_tuning_curve')


# site4 = today.add_site(depth = 3757, tetrodes = [3, 6])

exp0.add_site(3757)
exp0.add_session('17-15-58', None, sessionTypes['nb'], 'laser_tuning_curve')
exp0.add_session('17-18-57', None, sessionTypes['lp'], 'laser_tuning_curve')
exp0.add_session('17-21-29', None, sessionTypes['lt'], 'laser_tuning_curve')
exp0.add_session('17-25-16', 'g', sessionTypes['tc'], 'laser_tuning_curve')
exp0.add_session('17-37-45', 'af', sessionTypes['bf'], 'laser_tuning_curve')
exp0.add_session('17-41-31', None, sessionTypes['3p'], 'laser_tuning_curve')
exp0.add_session('17-44-25', None, sessionTypes['1p'], 'laser_tuning_curve')


# site5 = today.add_site(depth = 3805, tetrodes = [3, 6])

exp0.add_site(3805)
exp0.add_session('17-59-53', None, sessionTypes['nb'], 'laser_tuning_curve')
exp0.add_session('18-03-50', None, sessionTypes['lp'], 'laser_tuning_curve')
exp0.add_session('18-06-31', None, sessionTypes['lt'], 'laser_tuning_curve')
exp0.add_session('18-10-38', 'h', sessionTypes['tc'], 'laser_tuning_curve')
exp0.add_session('18-24-47', None, sessionTypes['bf'], 'laser_tuning_curve')
exp0.add_session('18-29-24', None, sessionTypes['3p'], 'laser_tuning_curve')
exp0.add_session('18-33-08', None, sessionTypes['1p'], 'laser_tuning_curve')


# site6 = today.add_site(depth = 3855, tetrodes = [6])

exp0.add_site(3855)
exp0.add_session('18-44-21', None, sessionTypes['nb'], 'laser_tuning_curve')
exp0.add_session('18-47-59', None, sessionTypes['lp'], 'laser_tuning_curve')
exp0.add_session('18-51-29', None, sessionTypes['lt'], 'laser_tuning_curve')
exp0.add_session('18-55-40', 'i', sessionTypes['tc'], 'laser_tuning_curve')
exp0.add_session('19-10-27', None, sessionTypes['bf'], 'laser_tuning_curve')
exp0.add_session('19-13-33', None, sessionTypes['3p'], 'laser_tuning_curve')
exp0.add_session('19-16-41', None, sessionTypes['1p'], 'laser_tuning_curve')

exp1 = celldatabase.Experiment(subject, '2015-06-30')
experiments.append(exp1)

'''
This data was collected the day before we RF shielded the speakers and recalibrated them. We need to be extra careful with anything related to noise and tuning curve presentations.
'''


# site1 = rd.add_site(depth = 3325, tetrodes = [3, 6])
exp1.add_site(3325)

exp1.add_session('12-21-34', None, 'LaserPulse', 'laser_tuning_curve')
exp1.add_session('12-25-12', None, 'NoiseBurst', 'laser_tuning_curve')
exp1.add_session('12-28-19', None, 'LaserTrain', 'laser_tuning_curve')
exp1.add_session('12-32-31', 'a', 'TuningCurve', 'laser_tuning_curve')
exp1.add_session('12-46-58', None, 'BestFreq', 'laser_tuning_curve') #7-8kHz, 70dB

# site4 = rd.add_site(depth = 3825, tetrodes = [3, 6])

exp1.add_site(3825)
exp1.add_session('14-21-48', None, 'LaserPulse', 'laser_tuning_curve')
exp1.add_session('14-24-29', None, 'NoiseBurst', 'laser_tuning_curve')
exp1.add_session('14-26-46', None, 'LaserTrain', 'laser_tuning_curve')
exp1.add_session('14-30-24', 'c', 'TuningCurve', 'laser_tuning_curve')
exp1.add_session('14-43-14', None, 'BestFreq', 'laser_tuning_curve') #8-9kHz, 70dB

# site5 = rd.add_site(depth = 3875, tetrodes = [3, 6])

exp1.add_site(3875)
exp1.add_session('14-54-11', None, 'NoiseBurst', 'laser_tuning_curve')
exp1.add_session('14-57-06', None, 'LaserPulse', 'laser_tuning_curve')
exp1.add_session('14-59-21', None, 'LaserTrain', 'laser_tuning_curve')
exp1.add_session('15-03-22', 'd', 'TuningCurve', 'laser_tuning_curve')
exp1.add_session('15-16-21', None, 'BestFreq', 'laser_tuning_curve')

# site6 = rd.add_site(depth = 3925, tetrodes = [6])

exp1.add_site(3925)
exp1.add_session('15-30-36', None, 'LaserPulse', 'laser_tuning_curve')
exp1.add_session('15-33-02', None, 'LaserTrain', 'laser_tuning_curve')
exp1.add_session('15-36-46', 'e', 'TuningCurve', 'laser_tuning_curve')
exp1.add_session('15-51-29', None, 'BestFreq', 'laser_tuning_curve') #8000-9000Hz, 70dB


# site7 = rd.add_site(depth = 3975, tetrodes = [3, 6])

exp1.add_site(3925)
exp1.add_session('16-01-48', None, 'NoiseBurst', 'laser_tuning_curve')
exp1.add_session('16-04-17', None, 'LaserPulse', 'laser_tuning_curve')
exp1.add_session('16-06-40', None, 'LaserTrain', 'laser_tuning_curve')
exp1.add_session('16-10-28', 'f', 'TuningCurve', 'laser_tuning_curve')
exp1.add_session('16-25-53', None, 'BestFreq', 'laser_tuning_curve') #5-7kHz



# site8 = rd.add_site(depth = 4025, tetrodes = [3, 6])

exp1.add_site(4025)
exp1.add_session('16-45-16', None, 'NoiseBurst', 'laser_tuning_curve')
exp1.add_session('16-48-00', None, 'LaserPulse', 'laser_tuning_curve')
exp1.add_session('16-50-51', None, 'LaserTrain', 'laser_tuning_curve')
exp1.add_session('16-56-14', 'g', 'TuningCurve', 'laser_tuning_curve')
exp1.add_session('17-09-09', None, 'BestFreq', 'laser_tuning_curve') #7-8kHz


exp2 = celldatabase.experiment(subject, '2015-07-06')
experiments.append(exp2)


# site1 = rd.add_site(depth = 3509, tetrodes = [3, 6])

exp2.add_site(3509)
exp2.add_session('11-15-56', None, sessionTypes['nb'], 'laser_tuning_curve')
exp2.add_session('11-18-36', None, sessionTypes['lp'], 'laser_tuning_curve')
exp2.add_session('11-21-26', None, sessionTypes['lt'], 'laser_tuning_curve')
exp2.add_session('11-25-58', 'a', sessionTypes['tc'], 'laser_tuning_curve')
exp2.add_session('11-39-46', None, sessionTypes['bf'], 'laser_tuning_curve')
exp2.add_session('11-42-37', None, sessionTypes['3p'], 'laser_tuning_curve')
exp2.add_session('11-45-22', None, sessionTypes['1p'], 'laser_tuning_curve')


# site2 = rd.add_site(depth = 3550, tetrodes = [3, 6])

exp2.add_site(3550)
exp2.add_session('11-51-47', None, sessionTypes['nb'], 'laser_tuning_curve')
exp2.add_session('11-54-51', None, sessionTypes['lp'], 'laser_tuning_curve')
exp2.add_session('11-58-17', None, sessionTypes['lt'], 'laser_tuning_curve')
exp2.add_session('12-01-53', 'b', sessionTypes['tc'], 'laser_tuning_curve')
exp2.add_session('12-14-53', None, sessionTypes['bf'], 'laser_tuning_curve')
exp2.add_session('12-17-13', None, sessionTypes['3p'], 'laser_tuning_curve')
exp2.add_session('12-19-34', None, sessionTypes['1p'], 'laser_tuning_curve')


# site3 = rd.add_site(depth = 3606, tetrodes = [3, 6])

exp2.add_site(3606)
exp2.add_session('12-28-47', None, sessionTypes['nb'], 'laser_tuning_curve')
exp2.add_session('12-31-21', None, sessionTypes['lp'], 'laser_tuning_curve')
exp2.add_session('12-34-00', None, sessionTypes['lt'], 'laser_tuning_curve')
exp2.add_session('12-37-29', 'c', sessionTypes['tc'], 'laser_tuning_curve')
exp2.add_session('12-50-34', None, sessionTypes['bf'], 'laser_tuning_curve')
exp2.add_session('12-53-57', None, sessionTypes['3p'], 'laser_tuning_curve')
exp2.add_session('12-56-04', None, sessionTypes['1p'], 'laser_tuning_curve')

# site4 = rd.add_site(depth = 3654, tetrodes = [3, 6])

exp2.add_site(3654)
exp2.add_session('13-06-27', None, sessionTypes['nb'], 'laser_tuning_curve')
exp2.add_session('13-09-00', None, sessionTypes['lp'], 'laser_tuning_curve')
exp2.add_session('13-11-25', None, sessionTypes['lt'], 'laser_tuning_curve')
exp2.add_session('13-15-01', 'd', sessionTypes['tc'], 'laser_tuning_curve')
exp2.add_session('13-28-12', None, sessionTypes['bf'], 'laser_tuning_curve')
exp2.add_session('13-30-00', None, sessionTypes['3p'], 'laser_tuning_curve')
exp2.add_session('13-31-58', None, sessionTypes['1p'], 'laser_tuning_curve')


exp3 = celldatabase.experiment(subject, '2015-07-13')
experiments.append(exp3)


# site2 = rd.add_site(depth = 3700, tetrodes = [5, 6])

exp3.add_site(3700)
exp3.add_session('20-11-35', None, sessionTypes['nb'], 'laser_tuning_curve')
exp3.add_session('20-21-34', None, sessionTypes['lp'], 'laser_tuning_curve') #Laser at 3mW
exp3.add_session('20-26-48', None, sessionTypes['lp'], 'laser_tuning_curve') #Laser at 1mW
exp3.add_session('20-32-21', None, sessionTypes['lt'], 'laser_tuning_curve')
exp3.add_session('20-37-10', 'b', sessionTypes['tc'], 'laser_tuning_curve')


# site3 = rd.add_site(depth = 3751, tetrodes = [5, 6])

exp3.add_site(3751)
exp3.add_session('21-11-00', None, sessionTypes['nb'], 'laser_tuning_curve') #Responses on TT6, maybe TT5
exp3.add_session('21-14-05', None, sessionTypes['lp'], 'laser_tuning_curve') #Laser at 1mW
exp3.add_session('21-16-36', None, sessionTypes['lt'], 'laser_tuning_curve') #Laser at 1mW
exp3.add_session('21-20-28', 'c', sessionTypes['tc'], 'laser_tuning_curve') #regular TC
exp3.add_session('21-34-28', 'd', sessionTypes['tc'], 'laser_tuning_curve') #zooming in on bf


exp4 = celldatabase.experiment(subject, '2015-07-20')
experiments.append(exp4)


# site1 = rd.add_site(depth = 3425, tetrodes = [4, 5, 6])

exp4.add_site(3425)
exp4.add_session('10-21-34', None, 'NB0.5', 'laser_tuning_curve')
exp4.add_session('10-24-16', None, 'LP2.5', 'laser_tuning_curve')
exp4.add_session('10-26-57', None, 'LT2.5', 'laser_tuning_curve')
exp4.add_session('10-30-48', 'a', 'TC_2k-40k_16f_40-70_4ints', 'laser_tuning_curve')


# site2 = rd.add_site(depth = 3451, tetrodes = [5, 6])

exp4.add_site(3451)
exp4.add_session('10-58-42', None, 'LP2.5', 'laser_tuning_curve')
exp4.add_session('11-01-08', None, 'LT2.5', 'laser_tuning_curve')
exp4.add_session('11-05-29', None, 'NB0.3', 'laser_tuning_curve')
exp4.add_session('11-08-42', 'b', 'TC_2k-40k_16f_40-70_4ints', 'laser_tuning_curve')
exp4.add_session('11-23-51', 'c', 'TC_3k-13k_16f_20-50_4ints', 'laser_tuning_curve')


# site3 = rd.add_site(depth = 3602, tetrodes = [5, 6])

exp4.add_site(3602)
exp4.add_session('11-51-31', None, 'NB0.3', 'laser_tuning_curve')
exp4.add_session('11-54-05', None, 'LP2.5', 'laser_tuning_curve')
exp4.add_session('11-56-36', None, 'LT2.5', 'laser_tuning_curve')
