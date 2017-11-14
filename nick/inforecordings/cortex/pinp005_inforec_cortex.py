from jaratoolbox import celldatabase

subject = 'pinp005'
experiments = []

exp0 = celldatabase.Experiment(subject, '2015-08-05', brainarea='cortex')
experiments.append(exp0)

# site1=rd.add_site(depth=1135, tetrodes=[ 3 ])

exp0.add_site(1135, tetrodes=[3])
exp0.add_session('21-10-44', None, 'NoiseBurst', 'laser_tuning_curve')
exp0.add_session('21-13-44', None, 'LaserPulse', 'laser_tuning_curve')
exp0.add_session('21-16-19', None, 'LaserTrain', 'laser_tuning_curve')
exp0.add_session('21-20-41', 'a', 'TuningCurve', 'laser_tuning_curve')

# site2=rd.add_site(depth=1192, tetrodes=[ 3 , 6 ])

exp0.add_site(1192, tetrodes=[3, 6])
exp0.add_session('21-40-59', None, 'NoiseBurst', 'laser_tuning_curve')
exp0.add_session('21-43-40', None, 'LaserPulse', 'laser_tuning_curve') #Not laser responsive
exp0.add_session('21-46-24', 'b', 'ShortTC', 'laser_tuning_curve') #Only at 60dB 

# site4=rd.add_site(depth=1722, tetrodes=[ 3, 4, 5, 6 ])

exp0.add_site(1722, tetrodes=[3, 4, 5, 6])
exp0.add_session('23-25-52', None, 'NoiseBurst', 'laser_tuning_curve')
exp0.add_session('23-28-19', None, 'LaserPulse', 'laser_tuning_curve') #Good responses on TT4
exp0.add_session('23-30-52', None, 'LaserTrain', 'laser_tuning_curve') #All the laser responses went away
exp0.add_session('23-36-02', 'e', 'TuningCurve', 'laser_tuning_curve') # Great tc for TT3
exp0.add_session('23-49-05', 'f', 'TuningCurveLower', 'laser_tuning_curve') #Another 160 trials at 20dB to try to resolve the threshold at cf

# site5=rd.add_site(depth=1776, tetrodes=[ 3, 4, 5, 6 ])

exp0.add_site(1776, tetrodes=[3, 4, 5, 6])
exp0.add_session('23-54-31', None, 'LaserPulse', 'laser_tuning_curve') #Laser responses on TT4
exp0.add_session('23-57-52', None, 'NoiseBurst', 'laser_tuning_curve') #Laser responses on TT4
exp0.add_session('00-04-11', 'g', 'TuningCurve', 'laser_tuning_curve', date='2015-08-06') #Laser responses on TT4
exp0.add_session('00-17-11', 'h', 'TuningCurveLower', 'laser_tuning_curve', date='2015-08-06') #Another 160 trials to get the cf
exp0.add_session('00-20-17', None, 'LaserTrain', 'laser_tuning_curve', date='2015-08-06')
exp0.add_session('00-24-39', 'i', 'TuningCurveHigher', 'laser_tuning_curve', date='2015-08-06') #Another 160 trials at 70dB to get a better TC for TT4 - it has a very high threshold

exp1 = celldatabase.Experiment(subject, '2015-08-10', brainarea='cortex')
experiments.append(exp1)

# site1 = rd.add_site(depth = 1399, tetrodes = [3, 6])

exp1.add_site(1399, tetrodes=[3, 6])
exp1.add_session('11-33-40', None, 'NoiseBurst', 'laser_tuning_curve') #Ref channel 19
exp1.add_session('11-37-15', None, 'LaserPulse', 'laser_tuning_curve') #Good laser responses T3 and T6
exp1.add_session('11-39-34', None, 'LaserTrain', 'laser_tuning_curve') #Ref channel 19
exp1.add_session('11-43-28', 'a', 'TuningCurve', 'laser_tuning_curve') #30-60dB 16freqs
exp1.add_session('11-56-52', 'b', 'auxTuningCurve', 'laser_tuning_curve') #adding trials at 20dB and 70dB
exp1.add_session('12-03-03', 'c', 'bestfreq', 'laser_tuning_curve') #7000-8000, 60db, 100 trials

# site2 = rd.add_site(depth = 1491, tetrodes = [3, 5, 6]) #Ref channel 14

exp1.add_site(1491, tetrodes=[3, 5, 6])
exp1.add_session('12-10-28', None, 'NoiseBurst', 'laser_tuning_curve') #Good sound responses on T3 and T6
exp1.add_session('12-12-52', None, 'LaserPulse', 'laser_tuning_curve') 
exp1.add_session('12-15-14', None, 'LaserTrain', 'laser_tuning_curve')
exp1.add_session('12-19-09', 'd', 'TuningCurve', 'laser_tuning_curve')
exp1.add_session('12-30-44', 'e', 'auxTuningCurve', 'laser_tuning_curve') #16 freqs at 20 and 70 db. I think we should include these by default. 
exp1.add_session('12-37-34', 'f', 'BestFreq', 'laser_tuning_curve') #7000-8000, 60db, 100 trials

# site3 = rd.add_site(depth = 1567, tetrodes = [3, 5, 6]) #Ref channel 14

exp1.add_site(1567, tetrodes=[3, 5, 6])
exp1.add_session('12-42-15', None, 'NoiseBurst', 'laser_tuning_curve') #Good noise response on T3 and T6
exp1.add_session('12-44-36', None, 'LaserPulse', 'laser_tuning_curve') #
exp1.add_session('12-47-04', None, 'LaserTrain', 'laser_tuning_curve') #
exp1.add_session('12-51-00', 'g', 'TuningCurve', 'laser_tuning_curve') #20-70dB
exp1.add_session('13-08-31', 'h', 'BestFreq', 'laser_tuning_curve') #7000-8000Hz

# site4 = rd.add_site(depth = 1655, tetrodes = [3, 5, 6]) #Ref channel 14

exp1.add_site(1655, tetrodes=[3, 5, 6])
exp1.add_session('13-12-16', None, 'NoiseBurst', 'laser_tuning_curve') #Best responses on T3
exp1.add_session('13-14-48', None, 'LaserPulse', 'laser_tuning_curve') #
exp1.add_session('13-17-08', None, 'LaserTrain', 'laser_tuning_curve') #
exp1.add_session('13-20-50', 'i', 'TuningCurve', 'laser_tuning_curve') #20-70dB
exp1.add_session('13-39-05', 'j', 'BestFreq', 'laser_tuning_curve') #7000-8000, 60dB
