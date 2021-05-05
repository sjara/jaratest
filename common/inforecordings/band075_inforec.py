from jaratoolbox import celldatabase

subject = 'band075'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-08-18', 'right_AC', info=['medialDiI','TT1ant','soundleft'])
experiments.append(exp0)

exp0.laserCalibration = {
    '1.0':3.3,
    '2.0':3.75,
    '3.0':4.25,
    '4.0':4.75,
    '5.0':5.2,
    '7.5':6.45,
    '10.0':7.65
    }

# exp0.add_site(1000, tetrodes=[2,4,6,8])
# exp0.add_session('13-52-57', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1050, tetrodes=[1,2,4,6])
# exp0.add_session('14-12-12', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('14-13-24', None, 'lasernoisebursts', 'bandwidth_am')
#
# exp0.add_site(1100, tetrodes=[1,2,4,6])
# exp0.add_session('14-45-35', None, 'lasernoisebursts', 'bandwidth_am')
# exp0.add_session('14-46-48', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1150, tetrodes=[1,2,4,6,8])
# exp0.add_session('14-52-50', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1175, tetrodes=[1,2,3,4,6,8])
# exp0.add_session('14-58-24', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('14-59-47', None, 'lasernoisebursts', 'bandwidth_am')

exp0.add_site(1200, tetrodes=[1,2,3,4,6,8])
exp0.add_session('15-05-09', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-06-14', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('15-09-08', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-13-40', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('15-19-39', None, 'longLaser', 'am_tuning_curve')
exp0.add_session('15-22-08', 'c', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('15-46-14', 'd', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1300, tetrodes=[1,2,3,4,6,8])
exp0.add_session('15-59-37', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-01-13', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('16-03-40', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-07-52', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('16-12-14', None, 'longLaser', 'am_tuning_curve')
exp0.add_session('16-15-42', 'g', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('16-39-40', 'h', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1400, tetrodes=[1,2,3,4,6,8])
exp0.add_session('16-51-15', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-52-53', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('16-55-09', 'i', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-59-20', 'j', 'AM', 'am_tuning_curve')
exp0.add_session('17-03-42', None, 'longLaser', 'am_tuning_curve')
exp0.add_session('17-06-41', 'k', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('17-30-40', 'l', 'noiseAmps', 'am_tuning_curve')

exp0.add_site(1500, tetrodes=[1,2,3,4,6,7,8])
exp0.add_session('17-43-07', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('17-44-46', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('17-47-22', 'm', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('17-51-49', 'n', 'AM', 'am_tuning_curve')
exp0.add_session('17-56-34', None, 'longLaser', 'am_tuning_curve')
exp0.add_session('18-00-22', 'o', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('18-24-19', 'p', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1500


exp1 = celldatabase.Experiment(subject, '2018-08-19', 'right_AC', info=['middleDiD','TT1ant','soundleft'])
experiments.append(exp1)

exp1.laserCalibration = {
    '1.0':3.3,
    '2.0':3.75,
    '3.0':4.2,
    '4.0':4.7,
    '5.0':5.2,
    '7.5':6.4,
    '10.0':7.65
    }

# exp1.add_site(1100, tetrodes=[2])
# exp1.add_session('13-28-11', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('13-29-52', None, 'lasernoisebursts', 'bandwidth_am')
#
# exp1.add_site(1200, tetrodes=[2,4,6])
# exp1.add_session('13-38-59', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(1250, tetrodes=[2,4,6,8])
exp1.add_session('13-44-48', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-46-08', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('13-48-25', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-52-58', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('13-57-22', None, 'longLaser', 'am_tuning_curve')
exp1.add_session('13-59-39', 'c', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('14-24-00', 'd', 'noiseAmps', 'am_tuning_curve')

# exp1.add_site(1350, tetrodes=[1,2,3,4,6])
# exp1.add_session('14-39-23', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1450, tetrodes=[1,2,3,4,5,6,8])
# exp1.add_session('14-50-03', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('14-51-46', None, 'lasernoisebursts', 'bandwidth_am')

exp1.add_site(1500, tetrodes=[1,2,3,4,5,6,8])
exp1.add_session('15-03-26', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-04-48', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('15-06-52', 'e', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-11-17', 'f', 'AM', 'am_tuning_curve')
exp1.add_session('15-15-33', None, 'longLaser', 'am_tuning_curve')
exp1.add_session('15-18-59', 'g', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('15-42-58', 'h', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1500


exp2 = celldatabase.Experiment(subject, '2018-08-21', 'right_AC', info=['lateralDiI','TT1ant','soundleft'])
experiments.append(exp2)

exp2.laserCalibration = {
    '1.0':3.15,
    '2.0':3.6,
    '3.0':4.00,
    '4.0':4.5,
    '5.0':4.95,
    '7.5':6.1,
    '10.0':7.2
    }
#tetrode 5 has the reference. Threshold set to 47 mV
# exp2.add_site(1200, tetrodes=[1,2,3,4])
# exp2.add_session('15-45-43', None, 'noisebursts', 'am_tuning_curve')
#
# #tetrode 3 has the reference
# exp2.add_site(1250, tetrodes=[1,2,4])
# exp2.add_session('16-01-17', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1300, tetrodes=[1,2,4])
# exp2.add_session('16-15-10', None, 'noisebursts', 'am_tuning_curve')
#
# exp2.add_site(1350, tetrodes=[1,2,4])
# exp2.add_session('16-25-56', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('16-28-41', None, 'lasernoisebursts', 'bandwidth_am')
# exp2.add_session('16-31-26', 'a', 'tuningCurve', 'am_tuning_curve')
# #shanks 3 and 4 are not penetrating
#
# exp2.add_site(1400, tetrodes=[1,2,4])
# exp2.add_session('16-44-05', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('16-46-35', None, 'lasernoisebursts', 'bandwidth_am')
# exp2.add_session('16-49-23', 'b', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(1500, tetrodes=[1,2,4])
exp2.add_session('17-05-45', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('17-07-12', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('17-09-42', 'c', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('17-14-37', 'd', 'AM', 'am_tuning_curve')
exp2.add_session('17-18-53', None, 'longLaser', 'am_tuning_curve')
exp2.add_session('17-21-42', 'e', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('17-45-46', 'f', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 1500

exp3 = celldatabase.Experiment(subject, '2018-08-22', 'left_AC', info=['medialDiD','TT8ant','soundright'])
experiments.append(exp3)

exp3.laserCalibration = {
    '1.0':3.25,
    '2.0':3.7,
    '3.0':4.15,
    '4.0':4.65,
    '5.0':5.10,
    '7.5':6.35,
    '10.0':7.5
    }

#tetrode 5 has the reference. Threshold ste to 47 mV
# exp3.add_site(900, tetrodes=[1,2,3,4])
# exp3.add_session('14-33-44', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1000, tetrodes=[1,2,4])
# exp3.add_session('14-49-15', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1100, tetrodes=[1,2,4])
# exp3.add_session('15-00-56', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('15-02-58', None, 'lasernoisebursts', 'bandwidth_am')
# exp3.add_session('15-06-43', 'a', 'tuningCurve', 'am_tuning_curve')

#Trode 3 has the reference
exp3.add_site(1200, tetrodes=[1,2])
exp3.add_session('15-26-11', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('15-34-16', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('15-46-13', 'b', 'tuningCurve', 'am_tuning_curve')#240
exp3.add_session('15-50-55', 'c', 'AM', 'am_tuning_curve')#150
exp3.add_session('15-55-30', None, 'longLaser', 'am_tuning_curve')#50
exp3.add_session('16-06-41', 'd', 'laserBandwidth', 'bandwidth_am')#420
exp3.add_session('16-55-04', 'e', 'noiseAmps', 'am_tuning_curve') #150 trials

exp3.add_site(1300, tetrodes=[1,2,8])
exp3.add_session('17-12-08', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('17-14-36', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('17-17-16', 'f', 'tuningCurve', 'am_tuning_curve')#240
exp3.add_session('17-22-49', 'g', 'AM', 'am_tuning_curve')#150
exp3.add_session('17-29-33', None, 'longLaser', 'am_tuning_curve')#50
exp3.add_session('17-33-28', 'h', 'laserBandwidth', 'bandwidth_am')#420
exp3.add_session('17-59-16', 'i', 'noiseAmps', 'am_tuning_curve') #150 trials

exp3.maxDepth = 1300

exp4 = celldatabase.Experiment(subject, '2018-08-23', 'left_AC', info=['middleDiI','TT8ant','soundright'])
experiments.append(exp4)

exp4.laserCalibration = {
    '1.0':3.20,
    '2.0':3.65,
    '3.0':4.15,
    '4.0':4.65,
    '5.0':5.15,
    '7.5':6.4,
    '10.0':7.6
    }

# exp4.add_site(900, tetrodes=[2,4,6,8])
# exp4.add_session('13-34-49', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('13-36-26', None, 'lasernoisebursts', 'bandwidth_am')
# exp4.add_session('13-39-03', 'a', 'tuningCurve', 'am_tuning_curve')
# exp4.add_session('13-43-48', 'b', 'AM', 'am_tuning_curve')
# exp4.add_session('13-48-15', None, 'longLaser', 'am_tuning_curve')
# # no good freq tuning

exp4.add_site(1000, tetrodes=[2,4,6,8])
exp4.add_session('13-58-51', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-00-24', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('14-02-56', 'c', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-07-29', 'd', 'AM', 'am_tuning_curve')
exp4.add_session('14-11-54', None, 'longLaser', 'am_tuning_curve')
exp4.add_session('14-15-05', 'e', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('14-39-05', 'f', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1100, tetrodes=[2,4,6,7,8])
exp4.add_session('14-55-02', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-56-51', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('14-59-38', 'g', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-03-52', 'h', 'AM', 'am_tuning_curve')
exp4.add_session('15-08-19', None, 'longLaser', 'am_tuning_curve')
exp4.add_session('15-14-01', 'i', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('15-40-19', 'j', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1200, tetrodes=[1,2,4,6,7,8])
exp4.add_session('15-54-21', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('15-56-02', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('15-57-44', 'k', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-02-23', 'l', 'AM', 'am_tuning_curve')
exp4.add_session('16-06-36', None, 'longLaser', 'am_tuning_curve')
exp4.add_session('16-11-04', 'm', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('16-35-04', 'n', 'noiseAmps', 'am_tuning_curve')

# exp4.add_site(1300, tetrodes=[1,2,3,4,6,7,8]) #Matt is now recording
# exp4.add_session('16-35-04', None, 'noisebursts', 'am_tuning_curve')#This trial is recorded in the ephys with the noiseAmps because SOMEBODY doesnt start a new session everytime they finish an ephys recording
# exp4.add_session('17-15-39', None, 'noisebursts', 'am_tuning_curve')#This is the actual nosieburst for this site
# #Both on- and off-set response to sound
# exp4.add_session('17-18-13', None, 'lasernoisebursts', 'bandwidth_am') #No notable laser responses on plausible cells. Is that possible?

exp4.maxDepth = 1300
