from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'band025'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-04-19', 'left_AC', info=['medialDiI','TT1ant','sound_left'])
experiments.append(exp0)

exp0.laserCalibration = {
    '1.0':3.1,
    '2.0':5.0,
    '3.0':5.8,
    '4.0':6.6,
    '5.0':7.3,
    '6.0':8.3,
    '7.0':9.3
}

exp0.add_site(900, tetrodes = [4,6,8])
exp0.add_session('13-12-12', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-21-37', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('13-25-38', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-33-26', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('13-50-33', 'c', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('14-12-01', 'd', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(975, tetrodes = [4,6,8])
exp0.add_session('14-21-09', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-23-12', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('14-26-27', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-32-42', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('14-38-17', 'g', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('15-00-39', 'h', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1100, tetrodes = [4,6,8])
exp0.add_session('15-11-00', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-13-00', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('15-15-13', 'i', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-20-47', 'j', 'AM', 'am_tuning_curve')
exp0.add_session('15-26-22', 'k', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('15-47-37', 'l', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1100


exp1 = celldatabase.Experiment(subject, '2017-04-20', 'left_AC', info=['middleDiD','TT1ant','sound_left'])
experiments.append(exp1)

exp1.laserCalibration = {
    '1.0':3.1,
    '2.0':4.9,
    '3.0':5.7,
    '4.0':6.5,
    '5.0':7.2,
    '6.0':8.2,
    '7.0':9.1
}

# exp1.add_site(1020, tetrodes = [4,6,7,8])
# exp1.add_session('12-34-57', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('12-37-35', None, 'lasernoisebursts', 'bandwidth_am') #pretty unimpressive responses

exp1.add_site(1100, tetrodes = [4,5,6,7,8])
exp1.add_session('12-49-14', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-51-26', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('12-55-38', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-01-11', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('13-05-59', 'c', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('13-28-55', 'd', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1200, tetrodes = [4,6,8])
exp1.add_session('13-39-16', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-42-33', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('13-46-57', 'e', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-53-16', 'f', 'AM', 'am_tuning_curve')
exp1.add_session('13-58-40', 'g', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('14-23-05', 'h', 'noiseAmps', 'am_tuning_curve')

# exp1.add_site(1300, tetrodes = [3,4,6,7,8])
# exp1.add_session('14-52-33', None, 'noisebursts', 'am_tuning_curve') #no sound response except TT3, which is probably TT4 from prev site

exp1.add_site(1400, tetrodes = [4,6,7,8])
exp1.add_session('14-59-39', None, 'noisebursts', 'am_tuning_curve') #pos delayed sound response on TT4?
exp1.add_session('15-01-35', None, 'lasernoisebursts', 'bandwidth_am') #weird responses, but might as well check tuning
exp1.add_session('15-04-52', 'i', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-10-18', 'j', 'AM', 'am_tuning_curve')
exp1.add_session('15-16-29', 'k', 'laserBandwidth', 'bandwidth_am') #4kHz, 16Hz for TT4 maybe laser responsive cell
exp1.add_session('15-45-43', 'l', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1400


exp2 = celldatabase.Experiment(subject, '2017-04-22', 'left_AC', info=['lateralDiI','TT1ant','sound_left'])
experiments.append(exp2)

# exp2.add_site(850, tetrodes = [6,8])
# exp2.add_session('14-07-40', None, 'noisebursts', 'am_tuning_curve')
# 
# exp2.add_site(900, tetrodes = [6,8])
# exp2.add_session('14-13-10', None, 'noisebursts', 'am_tuning_curve')
# 
# exp2.add_site(1000, tetrodes = [4,6,7,8])
# exp2.add_session('14-18-38', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-22-22', None, 'lasernoisebursts', 'bandwidth_am')
# 
# exp2.add_site(1100, tetrodes = [3,4,5,6,8])
# exp2.add_session('14-27-35', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-29-25', None, 'lasernoisebursts', 'bandwidth_am')

#looks like fiber isn't penetrating into brain due to it being too far lateral... stopping for the day

exp3 = celldatabase.Experiment(subject, '2017-04-23', 'left_AC', info=['lateralDiD','TT1ant','sound_left'])
experiments.append(exp3)

# exp3.add_site(1100, tetrodes = [4,5,6,7,8])
# exp3.add_session('14-35-06', None, 'noisebursts', 'am_tuning_curve') #no sound responses

#at 1400um, started seeing spooky signals that looked the same on all channels, thought shanks broken, pulled out, probe is fine
