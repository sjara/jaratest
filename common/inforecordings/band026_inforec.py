from jaratoolbox import celldatabase

subject = 'band026'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-04-26', 'right_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '0.5':0.65,
    '1.0':0.95,
    '1.5':1.25,
    '2.0':1.55,
    '2.5':1.9,
    '3.0':2.3,
    '3.5':2.65
}

# exp0.add_site(850, tetrodes = [4,7,8])
# exp0.add_session('10-49-47', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('10-52-29', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('10-55-09', None, 'laserTrain', 'am_tuning_curve')
# # clustering shows laser responsive cells are not sound responsive...
#
# exp0.add_site(1010, tetrodes = [4,5,6,8])
# exp0.add_session('11-05-16', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1096, tetrodes = [4,5,6,7,8])
exp0.add_session('11-13-02', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('11-15-15', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('11-19-34', None, 'laserTrain', 'am_tuning_curve')
exp0.add_session('11-21-54', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('11-27-23', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('11-33-21', 'c', 'bandwidth', 'bandwidth_am') #9kHz, 32Hz for maximum coverage
exp0.add_session('11-53-29', 'd', 'noiseAmps', 'am_tuning_curve')
exp0.add_session('11-57-50', None, 'laserPulse', 'am_tuning_curve')

# exp0.add_site(1322, tetrodes = [4,6,7,8])
# exp0.add_session('12-06-10', None, 'laserPulse', 'am_tuning_curve')
# exp0.add_session('12-08-59', None, 'noisebursts', 'am_tuning_curve')
# #bad sound responses in laser responsive cells

exp0.add_site(1470, tetrodes = [4,5,6,7,8])
exp0.add_session('12-17-51', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('12-20-25', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-22-44', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-28-16', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('12-33-21', 'g', 'bandwidth', 'bandwidth_am')
exp0.add_session('12-51-58', 'h', 'noiseAmps', 'am_tuning_curve')
exp0.add_session('12-56-59', None, 'laserPulse', 'am_tuning_curve')
exp0.add_session('12-59-17', None, 'laserTrain', 'am_tuning_curve')

exp0.maxDepth = 1470


exp1 = celldatabase.Experiment(subject, '2017-04-27', 'right_AC', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '0.5':0.65,
    '1.0':0.95,
    '1.5':1.25,
    '2.0':1.6,
    '2.5':2.0,
    '3.0':2.35,
    '3.5':2.75
}

exp1.add_site(1190, tetrodes = [4,6,7,8])
exp1.add_session('10-40-38', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('10-47-03', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('10-49-25', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('10-55-05', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('10-59-49', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('11-02-04', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('11-04-57', 'c', 'bandwidth', 'bandwidth_am') #7kHz, 64Hz for TT4 PV cell
exp1.add_session('11-27-59', 'd', 'noiseAmps', 'am_tuning_curve')

# exp1.add_site(1310, tetrodes = [4,6,8])
# exp1.add_session('11-43-36', None, 'laserPulse', 'am_tuning_curve')
# exp1.add_session('11-46-23', None, 'noisebursts', 'am_tuning_curve')
# #not that great responses

exp1.add_site(1350, tetrodes = [4,6,8])
exp1.add_session('11-50-04', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('11-51-53', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('11-54-00', 'e', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-00-01', 'f', 'AM', 'am_tuning_curve')
exp1.add_session('12-04-17', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-06-25', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('12-08-55', 'g', 'bandwidth', 'bandwidth_am') #7kHz, 64Hz for TT4 PV cell and TT8 excitatory cell
exp1.add_session('12-29-48', 'h', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1410, tetrodes = [4,6,8])
exp1.add_session('12-38-36', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-40-00', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-42-19', 'i', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-48-58', 'j', 'AM', 'am_tuning_curve')
exp1.add_session('12-53-35', None, 'laserPulse', 'am_tuning_curve')
exp1.add_session('12-55-40', None, 'laserTrain', 'am_tuning_curve')
exp1.add_session('12-58-39', 'k', 'bandwidth', 'bandwidth_am') #yet another 7kHz, 64Hz
exp1.add_session('13-20-30', 'l', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1410


exp2 = celldatabase.Experiment(subject, '2017-04-28', 'right_AC', info=['lateralDiI','TT1ant','sound_left'])
experiments.append(exp2)

exp2.laserCalibration = {
    '0.5':0.7,
    '1.0':1.0,
    '1.5':1.3,
    '2.0':1.65,
    '2.5':2.05,
    '3.0':2.45,
    '3.5':2.8
}

# exp2.add_site(1000, tetrodes = [4,6,8])
# exp2.add_session('09-48-29', None, 'laserPulse', 'am_tuning_curve')
# # weak-sauce laser responses
#
# exp2.add_site(1050, tetrodes = [4,6,8])
# exp2.add_session('09-56-05', None, 'laserPulse', 'am_tuning_curve')
# # better, still not that great

exp2.add_site(1087, tetrodes = [4,6,8])
exp2.add_session('09-59-36', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('10-01-11', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('10-03-27', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('10-09-15', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('10-13-28', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('10-15-40', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('10-18-39', 'c', 'bandwidth', 'bandwidth_am') #9kHz, 32Hz for TT8 and one of TT4 clusters
exp2.add_session('10-37-50', 'd', 'bandwidth', 'bandwidth_am') #6kHz, 32Hz for second TT4 cluster
exp2.add_session('10-57-02', 'e', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1160, tetrodes = [4,6,8])
exp2.add_session('11-08-55', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('11-11-45', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-13-59', 'f', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('11-20-05', 'g', 'AM', 'am_tuning_curve')
exp2.add_session('11-25-08', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('11-27-17', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('11-30-42', 'h', 'bandwidth', 'bandwidth_am') #6kHz, 32Hz
exp2.add_session('11-56-38', 'i', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1220, tetrodes = [4,6,8])
exp2.add_session('12-03-06', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('12-04-25', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-06-36', 'j', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-13-42', 'k', 'AM', 'am_tuning_curve')
exp2.add_session('12-18-15', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('12-20-21', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('12-24-27', 'l', 'bandwidth', 'bandwidth_am')
exp2.add_session('12-45-19', 'm', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1304, tetrodes = [4,6,8])
exp2.add_session('12-52-06', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('12-53-44', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-55-40', 'n', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-01-06', 'o', 'AM', 'am_tuning_curve')
exp2.add_session('13-05-21', None, 'laserPulse', 'am_tuning_curve')
exp2.add_session('13-08-00', None, 'laserTrain', 'am_tuning_curve')
exp2.add_session('13-10-09', 'p', 'bandwidth', 'bandwidth_am') #9kHz, 64Hz
exp2.add_session('13-28-36', 'q', 'bandwidth', 'bandwidth_am') #22kHz, 64Hz for nice TT4 spike
exp2.add_session('13-47-19', 'r', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 1304


exp3 = celldatabase.Experiment(subject, '2017-04-29', 'right_AC', info=['posteriormiddleDiI','TT1ant','sound_left'])
experiments.append(exp3)

exp3.laserCalibration = {
    '0.5':0.65,
    '1.0':0.9,
    '1.5':1.25,
    '2.0':1.55,
    '2.5':1.9,
    '3.0':2.35,
    '3.5':2.7
}

exp3.add_site(1060, tetrodes = [4,6,8])
exp3.add_session('12-28-58', None, 'laserPulse', 'am_tuning_curve') #strong TT6 laser response
exp3.add_session('12-30-47', None, 'noisebursts', 'am_tuning_curve') #TT6 not responsive to noise, but could be to tones?
exp3.add_session('12-32-13', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-38-00', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('12-42-45', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('12-45-06', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('12-47-42', 'c', 'bandwidth', 'bandwidth_am') #9kHz, 64Hz for laser responsive TT8 cell
exp3.add_session('13-06-07', 'd', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(1240, tetrodes = [4,6,7,8])
exp3.add_session('13-14-29', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-15-48', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-22-30', 'e', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-28-00', 'f', 'AM', 'am_tuning_curve')
exp3.add_session('13-32-28', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('13-34-57', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('13-37-33', 'g', 'bandwidth', 'bandwidth_am') #9kHz, 64Hz
exp3.add_session('13-56-11', 'h', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(1387, tetrodes = [4,6,8])
exp3.add_session('14-10-44', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-11-53', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-13-43', 'i', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-19-17', 'j', 'AM', 'am_tuning_curve')
exp3.add_session('14-24-20', None, 'laserPulse', 'am_tuning_curve')
exp3.add_session('14-27-03', None, 'laserTrain', 'am_tuning_curve')
exp3.add_session('14-29-16', 'k', 'bandwidth', 'bandwidth_am')
exp3.add_session('14-48-01', 'l', 'noiseAmps', 'am_tuning_curve')

exp3.maxDepth = 1387


exp4 = celldatabase.Experiment(subject, '2017-04-30', 'right_AC', info=['posteriorlateralDiD','TT1ant','sound_left'])
experiments.append(exp4)

exp4.laserCalibration = {
    '0.5':0.7,
    '1.0':0.95,
    '1.5':1.3,
    '2.0':1.65,
    '2.5':2.05,
    '3.0':2.4,
    '3.5':2.85
}

# exp4.add_site(1125, tetrodes = [3,4,6,8])
# exp4.add_session('11-36-26', None, 'laserPulse', 'am_tuning_curve')
# # pretty crappy laser response
#
# exp4.add_site(1341, tetrodes = [4,6,8])
# exp4.add_session('11-41-23', None, 'laserPulse', 'am_tuning_curve')
# exp4.add_session('11-42-48', None, 'noisebursts', 'am_tuning_curve')
# # shitty laser response, bad sound response

exp4.add_site(1370, tetrodes = [4,6,8])
exp4.add_session('11-45-59', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('11-47-27', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('11-49-54', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('11-55-36', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('12-02-13', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('12-04-27', 'c', 'bandwidth', 'bandwidth_am') #7kHz, 64Hz
exp4.add_session('12-26-37', 'd', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1500, tetrodes = [4,8])
exp4.add_session('12-36-01', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('12-37-18', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-38-59', 'e', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('12-44-27', 'f', 'AM', 'am_tuning_curve')
exp4.add_session('12-48-38', None, 'laserPulse', 'am_tuning_curve')
exp4.add_session('12-50-46', None, 'laserTrain', 'am_tuning_curve')
exp4.add_session('12-53-22', 'g', 'bandwidth', 'bandwidth_am') #32kHz, 64Hz for laser responsive TT8 cell
exp4.add_session('13-14-49', 'h', 'bandwidth', 'bandwidth_am') #9kHz, 64Hz for TT4 cells
exp4.add_session('13-33-20', 'i', 'noiseAmps', 'am_tuning_curve')

exp4.maxDepth = 1500
