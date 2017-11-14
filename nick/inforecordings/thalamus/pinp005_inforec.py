from jaratoolbox import celldatabase


subject = 'pinp005'
experiments = []

exp0 = celldatabase.Experiment(subject, '2015-07-30')
experiments.append(exp0)

# site1 = rd.add_site(depth = 3200, tetrodes = [3, 4, 5, 6])

exp0.add_site(3200, tetrodes=[3, 4, 5, 6])
exp0.add_session('19-12-32', None, 'NoiseBurst', 'laser_tuning_curve')
exp0.add_session('19-14-54', None, 'LaserPulse', 'laser_tuning_curve')
exp0.add_session('19-17-44', None, 'LaserTrain', 'laser_tuning_curve')
exp0.add_session('19-22-06', 'a', 'TuningCurve', 'laser_tuning_curve')
exp0.add_session('19-35-43', None, 'BestFreq', 'laser_tuning_curve') #7000-8000 2 freqs at 60dB

# site2 = rd.add_site(depth = 3250, tetrodes = [3, 4, 5, 6])

exp0.add_site(3250, tetrodes=[3, 4, 5, 6])
exp0.add_session('19-43-32', None, 'NoiseBurst', 'laser_tuning_curve')
exp0.add_session('19-47-14', None, 'LaserPulse', 'laser_tuning_curve') #Sweet laser responses on TT4
exp0.add_session('19-49-40', None, 'LaserTrain', 'laser_tuning_curve')
exp0.add_session('19-53-23', 'b', 'TuningCurve', 'laser_tuning_curve') #30-60dB, 2-40kHz
exp0.add_session('20-07-03', 'c', 'QuietTuningCurve', 'laser_tuning_curve') #20-50dB, 2-40kHz
exp0.add_session('20-19-09', 'd', 'RepeatTuningCurve', 'laser_tuning_curve') #40-60dB, 2-40kHz
#The threshold has shifted up by the second TC session
exp0.add_session('20-32-48', 'e', 'BestFreq', 'laser_tuning_curve') #7000-8000, 60dB


# site3 = rd.add_site(depth = 3370, tetrodes = [3, 4, 5, 6])

exp0.add_site(3370, tetrodes=[3, 4, 5, 6])
exp0.add_session('20-41-13', None, 'NoiseBurst', 'laser_tuning_curve') #Some responses still on TT4 - have we not really moved?
exp0.add_session('20-46-28', None, 'LaserPulse', 'laser_tuning_curve') #Crazy responses on all tetrodes. 
exp0.add_session('20-49-17', None, 'LaserTrain', 'laser_tuning_curve') #Still some crazy responses on all tetrodes. 
exp0.add_session('20-53-19', 'f', 'TuningCurve', 'laser_tuning_curve') #40-60dB, 2-40kHz Crappy TC.

# site4 = rd.add_site(depth = 3460, tetrodes = [3, 4, 5, 6])

exp0.add_site(3460, tetrodes=[3, 4, 5, 6])
exp0.add_session('21-08-38', None, 'NoiseBurst', 'laser_tuning_curve') #Some responses on TT4 that might be different
exp0.add_session('21-12-27', None, 'LaserPulse', 'laser_tuning_curve') #TT4 has responses that look like they may be direct
exp0.add_session('21-15-42', None, 'LaserTrain', 'laser_tuning_curve') #Some weak responses on T4. May get better with clustering.
exp0.add_session('21-19-30', 'g', 'TuningCurve', 'laser_tuning_curve') #TT4 is tuned but the threshold is high.
exp0.add_session('21-33-42', 'h', 'LoudTuningCurve', 'laser_tuning_curve') #40-70dB, 2-40kHz
exp0.add_session('21-46-11', None, 'BestFreq', 'laser_tuning_curve') #7-8kHz at 70dB for 100 trials

# site5 = rd.add_site(depth = 3675, tetrodes = [3, 4, 5, 6])

exp0.add_site(3675, tetrodes=[3, 4, 5, 6])
exp0.add_session('22-05-24', None, 'NoiseBurst', 'laser_tuning_curve') #Good responses on TT4
exp0.add_session('22-07-44', None, 'LaserPulse', 'laser_tuning_curve') # Not very laser responsive
exp0.add_session('22-10-33', None, 'LaserTrain', 'laser_tuning_curve') #Way more laser responsive than the last session. I accidentally added several extra events to the end when I tried to start the session below
exp0.add_session('22-14-59', None, 'LaserPulse2', 'laser_tuning_curve') # Repeating the pulses because it was so responsive in the last session
#It hardly responds at all to the single pulses

exp0.add_session('22-18-20', 'i', 'TuningCurve', 'laser_tuning_curve') # 30-70dB 5 ints, 2-40kHz 16 freqs. 800 trials total
exp0.add_session('22-34-36', None, 'BestFreq', 'laser_tuning_curve') # 7000-8000Hz, 70dB


# site6 = rd.add_site(depth = 3750, tetrodes = [3, 4, 5, 6])

exp0.add_site(3750, tetrodes=[3, 4, 5, 6])
exp0.add_session('22-37-41', None, 'NoiseBurst', 'laser_tuning_curve') # Good responses on TT4, some on T5 and 6
exp0.add_session('22-39-45', None, 'LaserPulse', 'laser_tuning_curve') # Best responses are on TT5
exp0.add_session('22-42-03', None, 'LaserTrain', 'laser_tuning_curve') # 
exp0.add_session('22-47-37', 'j', 'TuningCurve', 'laser_tuning_curve') # 2-40, 40-70 8 ints
exp0.add_session('23-12-05', 'k', 'TuningCurveLower', 'laser_tuning_curve') #2-40, just 30dB, 160 trials (10 each freq)
#I can start to hear some ringing from the speaker because the ground is getting dry
exp0.add_session('23-17-35', 'l', 'TuningCurveLower_again', 'laser_tuning_curve') #Doing the same thing again with saline in the wells

exp1 = celldatabase.Experiment(subject, '2015-08-03')
experiments.append(exp1)


# site3 = rd.add_site(depth=3500, tetrodes=[4])

exp1.add_site(3500, tetrodes=[4])
exp1.add_session('17-18-46', None, 'NoiseBurst', 'laser_tuning_curve')
exp1.add_session('17-21-20', None, 'LaserPulse', 'laser_tuning_curve')
exp1.add_session('17-24-58', None, 'LaserTrain', 'laser_tuning_curve')
exp1.add_session('17-28-54', 'b', 'TuningCurve', 'laser_tuning_curve')

# site4 = rd.add_site(depth=3600, tetrodes=[ 3, 4, 5, 6 ])

exp1.add_site(3600, tetrodes=[3, 4, 5, 6])
exp1.add_session('17-42-30', None, 'NoiseBurst', 'laser_tuning_curve')
exp1.add_session('17-44-40', None, 'LaserPulse', 'laser_tuning_curve')
exp1.add_session('17-47-16', None, 'LaserTrain', 'laser_tuning_curve')
exp1.add_session('17-51-47', 'c', 'TuningCurve', 'laser_tuning_curve')


# site6 = rd.add_site(depth=3800, tetrodes=[3, 4, 5, 6]) #Good cells on T4

exp1.add_site(3800, tetrodes=[3, 4, 5, 6])
exp1.add_session('18-30-14', None, 'NoiseBurst', 'laser_tuning_curve')
exp1.add_session('18-32-30', None, 'LaserPulse', 'laser_tuning_curve') #The cells on T4 look good but do not seem to respond to the laser at all.  
exp1.add_session('18-34-55', None, 'LaserTrain', 'laser_tuning_curve')
exp1.add_session('18-39-39', 'd', 'TuningCurve', 'laser_tuning_curve')


exp2 = celldatabase.Experiment(subject, '2015-08-06')
experiments.append(exp2)

# site4 = rd.add_site(depth=4114, tetrodes=[3,4,5,6])

exp2.add_site(4144, tetrodes=[3, 4, 5, 6])
exp2.add_session('18-05-16', None, 'NoiseBurst', 'laser_tuning_curve')
exp2.add_session('18-07-57', None, 'LaserPulse', 'laser_tuning_curve')
exp2.add_session('18-10-23', None, 'LaserTrain', 'laser_tuning_curve')
exp2.add_session('18-14-06', 'l', 'TuningCurve', 'laser_tuning_curve')

exp3 = celldatabase.Experiment(subject, '2015-08-12')
experiments.append(exp3)

# site1 = rd.add_site(depth=3833, tetrodes = [3, 4])

exp3.add_site(3833, tetrodes=[3, 4])
exp3.add_session('11-34-42', None, 'NoiseBurst', 'laser_tuning_curve')
exp3.add_session('11-37-03', None, 'LaserPulse', 'laser_tuning_curve') #2.5mW - strong onset response
exp3.add_session('11-42-57', None, 'LaserPulseLowerPower', 'laser_tuning_curve') #1.5mW - Still onset response
exp3.add_session('11-45-32', None, 'LaserPulseHigherPower', 'laser_tuning_curve') #3.5mW - Still onset response
exp3.add_session('11-48-13', None, 'LaserTrain', 'laser_tuning_curve') #2.5m
exp3.add_session('11-52-04', 'a', 'TuningCurve', 'laser_tuning_curve') #20-70dB
exp3.add_session('12-11-03', None, 'BestFreq', 'laser_tuning_curve') #7-8kHz, 60dB

# site2 = rd.add_site(depth=3921, tetrodes = [3, 4, 5, 6])

exp3.add_site(3921, tetrodes=[3, 4, 5, 6])
exp3.add_session('12-23-35', None, 'NoiseBurst', 'laser_tuning_curve')
exp3.add_session('12-25-47', None, 'LaserPulse', 'laser_tuning_curve')
exp3.add_session('12-28-16', None, 'LaserTrain', 'laser_tuning_curve')
exp3.add_session('12-32-46', 'b', 'TuningCurve', 'laser_tuning_curve')
exp3.add_session('12-51-13', None, 'BestFreq', 'laser_tuning_curve') #7-8kHz, 60dB

# site3 = rd.add_site(depth=4001, tetrodes = [3, 4, 5, 6])

exp3.add_site(4001, tetrodes=[3, 4, 5, 6])
exp3.add_session('12-58-13', None, 'NoiseBurst', 'laser_tuning_curve')
exp3.add_session('13-01-25', None, 'LaserPulse', 'laser_tuning_curve') #Only onset response
exp3.add_session('13-03-59', None, 'LaserTrain', 'laser_tuning_curve')
exp3.add_session('13-07-39', 'c', 'TuningCurve', 'laser_tuning_curve')
exp3.add_session('13-25-01', None, 'BestFreq', 'laser_tuning_curve') #7-8kHz, 60dB

# site5 = rd.add_site(depth=4236, tetrodes = [3, 4, 5, 6])

exp3.add_site(4236, tetrodes=[3, 4, 5, 6])
exp3.add_session('13-50-28', None, 'NoiseBurst', 'laser_tuning_curve')
exp3.add_session('13-53-50', None, 'LaserPulse', 'laser_tuning_curve')
exp3.add_session('13-58-15', None, 'LaserTrain', 'laser_tuning_curve')
exp3.add_session('14-02-32', 'd', 'TuningCurve', 'laser_tuning_curve')
exp3.add_session('14-20-51', None, 'BestFreq', 'laser_tuning_curve') #7-8kHz, 60dB


exp4 = celldatabase.Experiment(subject, '2015-08-13')
experiments.append(exp4)

# site1 = rd.add_site(depth=3902, tetrodes=[3, 4, 5, 6])

exp4.add_site(3902, tetrodes=[3, 4, 5, 6])
exp4.add_session('12-48-14', None, 'NoiseBurst', 'laser_tuning_curve')
exp4.add_session('12-50-27', None, 'LaserPulse', 'laser_tuning_curve')
exp4.add_session('12-53-02', None, 'LaserTrain', 'laser_tuning_curve')
# exp4.add_session('12-57-12', 'a', 'AM', 'laser_tuning_curve')
# exp4.add_session('13-11-52', 'b', 'AM', 'laser_tuning_curve')
exp4.add_session('13-24-17', 'c', 'TuningCurve', 'laser_tuning_curve')
exp4.add_session('13-41-46', 'd', 'BestFreq', 'laser_tuning_curve') #6000-7000Hz, 60dB
exp4.add_session('13-52-29', 'e', 'AM', 'laser_tuning_curve')


# site2 = rd.add_site(depth=3970, tetrodes=[3, 4, 5, 6]) #threshold = 23uV

exp4.add_site(3970, tetrodes=[3, 4, 5, 6])
exp4.add_session('14-36-57', None, 'NoiseBurst', 'laser_tuning_curve')
exp4.add_session('14-42-41', None, 'LaserPulse', 'laser_tuning_curve')
exp4.add_session('14-46-14', None, 'LaserTrain', 'laser_tuning_curve')
exp4.add_session('14-50-18', 'f', 'AM', 'laser_tuning_curve')
exp4.add_session('15-15-40', 'g', 'TuningCurve', 'laser_tuning_curve')
exp4.add_session('15-33-58', 'h', 'BestFreq', 'laser_tuning_curve') #6000-7000, 60dB
