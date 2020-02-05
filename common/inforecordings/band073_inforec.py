from jaratoolbox import celldatabase

subject = 'band073'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-09-05', 'right_AC', info=['medialDiD','TT1ant','soundleft'])
experiments.append(exp0)

exp0.laserCalibration = {
    '1.0':3.6,
    '2.0':4.45,
    '3.0':5.3,
    '4.0':6.15,
    '5.0':7.0,
    '7.5':9.2
    }

exp0.add_site(1200, tetrodes=[2])
exp0.add_session('12-42-55', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-45-11', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('12-46-49', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-51-25', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('12-55-45', None, 'longLaser', 'am_tuning_curve')
exp0.add_session('12-57-52', 'c', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('13-22-04', 'd', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1300, tetrodes=[1,2,4])
# exp0.add_session('13-46-21', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1400, tetrodes=[1,2,6,8])
exp0.add_session('14-04-07', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-05-38', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('14-07-22', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-13-21', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('14-17-36', None, 'longLaser', 'am_tuning_curve')
exp0.add_session('14-19-41', 'g', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('14-45-07', 'h', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1500, tetrodes=[6,8])
# exp0.add_session('15-30-49', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(1600, tetrodes=[2,4,7,8])
exp0.add_session('16-06-39', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-08-06', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('16-10-21', 'i', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-15-06', 'j', 'AM', 'am_tuning_curve')
exp0.add_session('16-19-23', None, 'longLaser', 'am_tuning_curve')
exp0.add_session('16-21-31', 'k', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('16-45-37', 'l', 'noiseAmps', 'am_tuning_curve')

exp0.maxDepth = 1600


# exp1 = celldatabase.Experiment(subject, '2018-09-07', 'right_AC', info=['middleDiO','TT1ant','soundleft'])
# experiments.append(exp1)
#
# exp1.laserCalibration = {
#     '1.0':3.8,
#     '2.0':4.9,
#     '3.0':6.0,
#     '4.0':7.15,
#     '5.0':8.2
#     }
# failed to penetrate cortex, mouse bled heavily upon tissue removal

exp1 = celldatabase.Experiment(subject, '2018-09-10', 'left_AC', info=['medialDiD','TT8ant','soundright'])
experiments.append(exp1)

exp1.laserCalibration = {
    '1.0':3.85,
    '2.0':4.85,
    '3.0':6.0,
    '4.0':7.05,
    '5.0':8.1
    }

exp1.add_site(1050, tetrodes=[2,6,8])
exp1.add_session('12-17-26', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-18-52', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('12-20-35', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-25-30', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('12-30-13', None, 'longLaser', 'am_tuning_curve')
exp1.add_session('12-32-19', 'c', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('13-00-17', 'd', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1150, tetrodes=[1,2,4,6,7,8])
exp1.add_session('13-16-55', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('13-18-27', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('13-20-02', 'e', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('13-24-42', 'f', 'AM', 'am_tuning_curve')
exp1.add_session('13-29-09', None, 'longLaser', 'am_tuning_curve')
exp1.add_session('13-31-48', 'g', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('13-55-41', 'h', 'noiseAmps', 'am_tuning_curve')

# exp1.add_site(1250, tetrodes=[2,4,7,8])
# exp1.add_session('14-46-04', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('14-47-51', None, 'lasernoisebursts', 'bandwidth_am')
# exp1.add_session('14-49-45', 'i', 'tuningCurve', 'am_tuning_curve')
#very unimpressive frequency tuning

# exp1.add_site(1350, tetrodes=[1,2,7,8])
# exp1.add_session('15-02-11', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('15-03-38', None, 'lasernoisebursts', 'bandwidth_am')
# exp1.add_session('15-05-16', 'j', 'tuningCurve', 'am_tuning_curve')

exp1.add_site(1450, tetrodes=[1,2,7,8])
exp1.add_session('15-21-00', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('15-22-45', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('15-25-02', 'k', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('15-29-31', 'l', 'AM', 'am_tuning_curve')
exp1.add_session('15-34-12', None, 'longLaser', 'am_tuning_curve')
exp1.add_session('15-41-11', 'm', 'laserBandwidth', 'bandwidth_am')
exp1.add_session('16-14-58', 'n', 'noiseAmps', 'am_tuning_curve')

exp1.add_site(1550, tetrodes=[7,8])
exp1.add_session('17-12-27', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('17-13-58', None, 'lasernoisebursts', 'bandwidth_am')
exp1.add_session('17-15-36', 'o', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('17-20-28', 'p', 'AM', 'am_tuning_curve')
exp1.add_session('17-25-18', None, 'longLaser', 'am_tuning_curve')
exp1.add_session('17-33-28', 'q', 'laserBandwidth', 'bandwidth_am')#27 kHz @ 32
exp1.add_session('17-59-18', 'r', 'noiseAmps', 'am_tuning_curve')

exp1.maxDepth = 1550

# exp2 = celldatabase.Experiment(subject, '2018-09-11', 'left_AC', info=['midlateralDiO','TT8ant','soundright'])
# experiments.append(exp2)
#
# exp2.laserCalibration = {
#     '1.0':4.0,
#     '2.0':5.40,
#     '3.0':8.0,
#     '4.0':9.89,
#     #'5.0':7.0,
#     #'7.5':9.2
#     }
# #Unable to run experiment. As laser stayed on, it grew weaker, not stronger. Also appears to be varying greatly over time +-0.5 mW at any set power level

exp2 = celldatabase.Experiment(subject, '2018-09-12', 'left_AC', info=['midlateralDiO','TT8ant','soundright'])
experiments.append(exp2)

exp2.laserCalibration = {
    '1.0':3.70,
    '2.0':4.75,
    '3.0':5.80,
    '4.0':6.90,
    '5.0':7.95,
    #'7.5':9.2 Could not calibrate above 5.8ish
    }

#Laser set to 5 mW, tetrode 3 has the reference
# exp2.add_site(1300, tetrodes=[5])
# exp2.add_session('15-15-31', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(1400, tetrodes=[4])
exp2.add_session('15-25-43', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('15-30-03', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('15-35-03', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-41-59', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('15-46-27', None, 'longLaser', 'am_tuning_curve')
exp2.add_session('15-48-49', 'c', 'laserBandwidth', 'bandwidth_am')#10 kHz @ 32
exp2.add_session('16-15-23', 'd', 'noiseAmps', 'am_tuning_curve')

# exp2.add_site(1600, tetrodes=[1,2,5,6,7,8])
# exp2.add_session('16-33-10', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('16-35-16', None, 'lasernoisebursts', 'bandwidth_am')
# exp2.add_session('16-37-40', 'e', 'tuningCurve', 'am_tuning_curve')
# exp2.add_session('16-44-14', 'f', 'AM', 'am_tuning_curve')
# exp2.add_session('16-49-07', None, 'longLaser', 'am_tuning_curve')
# #No AM response
#
# exp2.add_site(1700, tetrodes=[1])
# exp2.add_session('17-05-50', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('17-07-30', None, 'lasernoisebursts', 'bandwidth_am')
# exp2.add_session('16-37-40', 'g', 'tuningCurve', 'am_tuning_curve')
#No frequency tuning

exp2.maxDepth = 1700

exp3 = celldatabase.Experiment(subject, '2018-09-13', 'left_AC', info=['LateralmidlateralDiD','TT8ant','soundright'])
experiments.append(exp3)

exp3.laserCalibration = {
    '1.0':3.70,
    '2.0':4.80,
    '3.0':5.80,
    '4.0':6.85,
    '5.0':7.95,
    #'7.5':9.2 Could not calibrate above 6.2ish
    }

#Laser set to 5 mW, tetrode 3 has the reference
# exp3.add_site(1000, tetrodes=[2,4])
# exp3.add_session('15-17-48', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1200, tetrodes=[5,6,7,8])
# exp3.add_session('15-34-43', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1300, tetrodes=[2,4,5,6,7,8])
# exp3.add_session('15-42-56', None, 'noisebursts', 'am_tuning_curve')
#TT1 was flexing and under Nick's advisement I removed the probe as he said if I go any further it will break
#Flexation started at ~1050 and was more prominant while mouse was running. Severe flexation did not occur until ~1250. Flexation disappeared upon returning to 950 um.

exp3.maxDepth = 1300

exp4 = celldatabase.Experiment(subject, '2018-09-14', 'right_AC', info=['middleDiO','TT1ant','soundleft'])
experiments.append(exp4)

exp4.laserCalibration = {
    '1.0':3.80,
    '2.0':4.80,
    '3.0':5.85,
    '4.0':6.95,
    '5.0':7.85,
    #'7.5':9.2 Could not calibrate above 6.2ish
    }

exp4.add_site(900, tetrodes=[1,2,4,6,7,8])
exp4.add_session('12-54-55', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-56-16', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('12-57-51', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-08-07', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('13-12-57', None, 'longLaser', 'am_tuning_curve')
exp4.add_session('13-17-32', 'c', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('13-41-52', 'd', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('14-07-07', 'e', 'noiseAmps', 'am_tuning_curve')
exp4.add_session('14-11-26', 'f', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1000, tetrodes=[1,2,4,6,7,8])
exp4.add_session('14-22-18', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('14-23-43', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('14-25-20', 'g', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('14-29-50', 'h', 'AM', 'am_tuning_curve')
exp4.add_session('14-34-05', None, 'longLaser', 'am_tuning_curve')
exp4.add_session('14-39-47', 'i', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('15-04-35', 'j', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1100, tetrodes=[1,2,3,4,6,7,8])
exp4.add_session('15-19-38', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('15-21-10', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('15-23-27', 'k', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-27-57', 'l', 'AM', 'am_tuning_curve')
exp4.add_session('15-32-11', None, 'longLaser', 'am_tuning_curve')
exp4.add_session('15-36-29', 'm', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('16-05-53', 'n', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('16-29-54', 'o', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1200, tetrodes=[1,2,3,4,6,7,8])
exp4.add_session('16-49-45', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('16-51-27', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('16-53-02', 'p', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('16-59-45', 'q', 'AM', 'am_tuning_curve')
exp4.add_session('17-04-37', None, 'longLaser', 'am_tuning_curve')
exp4.add_session('17-09-41', 'r', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('17-36-47', 's', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('18-00-52', 't', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1300, tetrodes=[1,2,3,4,6,7,8])
exp4.add_session('18-18-43', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('18-21-17', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('18-23-34', 'u', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('18-28-26', 'v', 'AM', 'am_tuning_curve')
exp4.add_session('18-32-41', None, 'longLaser', 'am_tuning_curve')
exp4.add_session('18-38-23', 'w', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('19-03-54', 'x', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1400, tetrodes=[1,2,3,4,6,7,8])
exp4.add_session('19-17-10', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('19-18-59', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('19-20-44', 'y', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('19-25-31', 'z', 'AM', 'am_tuning_curve')
exp4.add_session('19-29-50', None, 'longLaser', 'am_tuning_curve')
exp4.add_session('19-34-53', 'aa', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('19-59-24', 'ab', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('20-24-31', 'ac', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1500, tetrodes=[1,2,3,4,6,7,8])
exp4.add_session('20-39-49', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('20-41-31', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('20-43-16', 'ad', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('20-47-46', 'ae', 'AM', 'am_tuning_curve')
exp4.add_session('20-52-01', None, 'longLaser', 'am_tuning_curve')
exp4.add_session('20-56-54', 'af', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('21-20-57', 'ag', 'laserBandwidth', 'bandwidth_am')
exp4.add_session('21-45-42', 'ah', 'noiseAmps', 'am_tuning_curve')
exp4.add_session('21-50-10', 'ai', 'noiseAmps', 'am_tuning_curve')

exp4.maxDepth = 1500


exp5 = celldatabase.Experiment(subject, '2018-09-17', 'right_AC', info=['lateralDiD','TT1ant','soundleft'])
experiments.append(exp5)

#Control day, tether not plugged in
exp5.laserCalibration = {
    '1.0':3.0,
    '2.0':3.25,
    '3.0':3.45,
    '4.0':3.65,
    '5.0':3.85,
    '7.5':4.45,
    '10.0':5.0
    }

#shank 1 not penetrating well

# exp5.add_site(950, tetrodes=[3,4,6,7,8])
# exp5.add_session('12-02-48', None, 'noiseburst', 'am_tuning_curve')

# exp5.add_site(1150, tetrodes=[4,6,7,8])
# exp5.add_session('12-12-55', None, 'noiseburst', 'am_tuning_curve')

exp5.add_site(1250, tetrodes=[3,4,6,7,8])
exp5.add_session('12-25-10', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('12-27-24', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('12-29-22', 'a', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('12-36-15', 'b', 'AM', 'am_tuning_curve')
exp5.add_session('12-40-42', None, 'longLaser', 'am_tuning_curve')
exp5.add_session('12-44-20', 'c', 'laserBandwidthControl', 'bandwidth_am')
exp5.add_session('13-09-42', 'd', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(1350, tetrodes=[3,4,6,7,8])
exp5.add_session('13-26-09', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('13-30-35', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('13-34-29', 'e', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('13-39-15', 'f', 'AM', 'am_tuning_curve')
exp5.add_session('13-43-52', None, 'longLaser', 'am_tuning_curve')
exp5.add_session('13-49-34', 'g', 'laserBandwidthControl', 'bandwidth_am')
exp5.add_session('14-48-11', 'h', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(1450, tetrodes=[3,4,6])
exp5.add_session('15-04-37', None, 'noiseburst', 'am_tuning_curve')
exp5.add_session('15-54-10', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('15-56-16', 'i', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('16-16-25', 'j', 'AM', 'am_tuning_curve')
exp5.add_session('16-35-38', None, 'longLaser', 'am_tuning_curve')
#32 KhZ @ 64, 9 @ 64
exp5.add_session('16-47-03', 'k', 'laserBandwidthControl', 'bandwidth_am')
exp5.add_session('17-14-06', 'l', 'noiseAmps', 'am_tuning_curve')
exp5.add_session('17-19-45', 'm', 'laserBandwidthControl', 'bandwidth_am')

exp5.maxDepth = 1450
