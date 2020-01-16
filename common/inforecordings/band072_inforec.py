from jaratoolbox import celldatabase

subject = 'band072'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-08-27', 'left_AC', info=['medialDiI','TT8ant','soundright'])
experiments.append(exp0)

exp0.laserCalibration = {
    '1.0':3.25,
    '2.0':3.7,
    '3.0':4.1,
    '4.0':4.6,
    '5.0':5.05,
    '7.5':6.2,
    '10.0':7.3
    }

# exp0.add_site(1200, tetrodes=[4,8])
# exp0.add_session('15-02-18', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('15-04-01', None, 'lasernoisebursts', 'bandwidth_am')
# exp0.add_session('15-06-18', 'a', 'tuningCurve', 'am_tuning_curve')
#
# exp0.add_site(1450, tetrodes=[2])
# exp0.add_session('15-44-23', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('15-45-50', None, 'lasernoisebursts', 'bandwidth_am')
# exp0.add_session('15-47-55', 'b', 'tuningCurve', 'am_tuning_curve')
#
# exp0.add_site(1500, tetrodes=[2])
# exp0.add_session('15-56-05', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('15-57-53', None, 'lasernoisebursts', 'bandwidth_am')
# exp0.add_session('15-59-41', 'c', 'tuningCurve', 'am_tuning_curve')
# #doing another tuning curve as mouse was asleep
# exp0.add_session('16-04-41', 'd', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(1550, tetrodes=[2])
exp0.add_session('16-15-27', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-17-02', None, 'lasernoisebursts', 'bandwidth_am')
exp0.add_session('16-19-03', 'e', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-23-51', 'f', 'AM', 'am_tuning_curve')
exp0.add_session('16-28-43', None, 'longLaser', 'am_tuning_curve')
exp0.add_session('16-31-46', 'g', 'laserBandwidth', 'bandwidth_am')
exp0.add_session('16-56-04', 'h', 'noiseAmps', 'am_tuning_curve')

# exp0.add_site(1650, tetrodes=[1,2,4])
# exp0.add_session('17-09-44', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('17-12-04', None, 'lasernoisebursts', 'bandwidth_am')
# exp0.add_session('17-14-24', 'i', 'tuningCurve', 'am_tuning_curve')
#
# exp0.add_site(1700, tetrodes=[1,2,4])
# exp0.add_session('17-31-30', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(1750, tetrodes=[1,2,4])
# exp0.add_session('17-38-36', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('17-41-24', None, 'lasernoisebursts', 'bandwidth_am')
# exp0.add_session('17-44-50', 'j', 'tuningCurve', 'am_tuning_curve')
# exp0.add_session('17-50-04', 'k', 'AM', 'am_tuning_curve')
# exp0.add_session('17-54-56', None, 'longLaser', 'am_tuning_curve')

exp0.maxDepth = 1750


exp1 = celldatabase.Experiment(subject, '2018-08-28', 'left_AC', info=['middleDiD','TT8ant','soundright'])
experiments.append(exp1)

exp1.laserCalibration = {
    '1.0':3.25,
    '2.0':3.7,
    '3.0':4.15,
    '4.0':4.6,
    '5.0':5.1,
    '7.5':6.35,
    '10.0':7.5
    }

# exp1.add_site(1000, tetrodes=[2,4])
# exp1.add_session('12-06-03', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1100, tetrodes=[6,7,8])
# exp1.add_session('12-16-34', None, 'noisebursts', 'am_tuning_curve') #Its possible one trial of the behavior ended up on the previous ephys recording
# #One would never guess when Matt started recording
#
# exp1.add_site(1200, tetrodes=[6,7,8])
# exp1.add_session('12-29-10', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1300, tetrodes=[2,6,7])
# exp1.add_session('12-36-41', None, 'noisebursts', 'am_tuning_curve')
#
# exp1.add_site(1600, tetrodes=[2])
# exp1.add_session('13-00-48', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('13-03-51', None, 'lasernoisebursts', 'bandwidth_am')
#
# exp1.add_site(1700, tetrodes=[2])
# exp1.add_session('13-13-23', None, 'noisebursts', 'am_tuning_curve')

exp1.maxDepth = 1700

exp2 = celldatabase.Experiment(subject, '2018-08-28', 'left_AC', info=['midlateralDiI','TT8ant','soundright'])
experiments.append(exp2)

exp2.laserCalibration = {
    '1.0':3.25,
    '2.0':3.7,
    '3.0':4.15,
    '4.0':4.6,
    '5.0':5.1,
    '7.5':6.35,
    '10.0':7.5
    }
    #Using same calibration as experiment 1 since they were done on the same day and no DiI appeared to be on the tetrode

# exp2.add_site(1000, tetrodes=[7,8])
# exp2.add_session('15-11-46', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('15-15-01', None, 'lasernoisebursts', 'bandwidth_am')
# exp2.add_session('15-18-14', 'a', 'tuningCurve', 'am_tuning_curve')
# #No frequency tuning
#
# exp2.add_site(1100, tetrodes=[7,8])
# exp2.add_session('15-29-51', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('15-32-11', None, 'lasernoisebursts', 'bandwidth_am')
# exp2.add_session('15-34-11', 'b', 'tuningCurve', 'am_tuning_curve')
# exp2.add_session('15-39-15', 'c', 'AM', 'am_tuning_curve')
# exp2.add_session('15-43-56', None, 'longLaser', 'am_tuning_curve')
# #No tuning
#
# exp2.add_site(1200, tetrodes=[7,8])
# exp2.add_session('15-54-06', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('15-55-48', None, 'lasernoisebursts', 'bandwidth_am')
# exp2.add_session('15-58-17', 'd', 'tuningCurve', 'am_tuning_curve')
# exp2.add_session('16-03-25', 'e', 'AM', 'am_tuning_curve')
# exp2.add_session('16-07-55', None, 'longLaser', 'am_tuning_curve')
#
# exp2.add_site(1300, tetrodes=[7,8])
# exp2.add_session('16-23-28', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('16-24-56', None, 'lasernoisebursts', 'bandwidth_am')
# exp2.add_session('16-26-47', 'f', 'tuningCurve', 'am_tuning_curve')
# exp2.add_session('16-32-01', 'g', 'AM', 'am_tuning_curve')
# exp2.add_session('16-36-42', None, 'longLaser', 'am_tuning_curve')

exp2.add_site(1400, tetrodes=[6,7,8])
exp2.add_session('16-48-29', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('16-50-29', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('16-52-07', 'h', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('16-56-50', 'i', 'AM', 'am_tuning_curve')
exp2.add_session('17-01-16', None, 'longLaser', 'am_tuning_curve')
#exp2.add_session('17-06-56', None, 'laserBandwidth', 'bandwidth_am') redone
exp2.add_session('17-11-41', 'j', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('17-36-49', 'k', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1500, tetrodes=[4,6,8])
exp2.add_session('17-50-45', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('17-52-18', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('17-54-21', 'l', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('17-58-46', 'm', 'AM', 'am_tuning_curve')
exp2.add_session('18-03-01', None, 'longLaser', 'am_tuning_curve')
exp2.add_session('18-05-58', 'n', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('18-29-59', 'o', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(1600, tetrodes=[2,4,6,7,8])
exp2.add_session('18-41-49', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('18-43-19', None, 'lasernoisebursts', 'bandwidth_am')
exp2.add_session('18-45-01', 'p', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('18-49-38', 'q', 'AM', 'am_tuning_curve')
exp2.add_session('18-54-14', None, 'longLaser', 'am_tuning_curve')
exp2.add_session('18-56-30', 'r', 'laserBandwidth', 'bandwidth_am')
exp2.add_session('19-20-26', 's', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 1600


exp3 = celldatabase.Experiment(subject, '2018-08-29', 'left_AC', info=['lateralDiD','TT8ant','soundright'])
experiments.append(exp3)

exp3.laserCalibration = {
    '1.0':3.25,
    '2.0':3.7,
    '3.0':4.2,
    '4.0':4.65,
    '5.0':5.15,
    '7.5':6.35,
    '10.0':7.55
    }

# exp3.add_site(1000, tetrodes=[8])
# exp3.add_session('11-35-27', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1100, tetrodes=[8])
# exp3.add_session('12-01-22', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1200, tetrodes=[7])
# exp3.add_session('12-12-09', None, 'noisebursts', 'am_tuning_curve')
# exp3.add_session('12-14-00', None, 'lasernoisebursts', 'bandwidth_am')
# exp3.add_session('12-15-38', 'a', 'tuningCurve', 'am_tuning_curve')
# exp3.add_session('12-21-50', 'b', 'AM', 'am_tuning_curve')
# exp3.add_session('12-26-25', None, 'longLaser', 'am_tuning_curve')
#
# exp3.add_site(1300, tetrodes=[7])
# exp3.add_session('12-38-33', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.add_site(1400, tetrodes=[1,2,4,6,8])
# exp3.add_session('12-47-38', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(1500, tetrodes=[4,6,8])
exp3.add_session('12-57-12', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-59-26', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('13-01-42', 'c', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-11-39', 'd', 'AM', 'am_tuning_curve')
exp3.add_session('13-16-31', None, 'longLaser', 'am_tuning_curve')
exp3.add_session('13-25-52', 'e', 'laserBandwidth', 'bandwidth_am') #10 kHz @ 64
exp3.add_session('13-50-53', 'f', 'noiseAmps', 'am_tuning_curve')
exp3.add_session('13-55-50', 'g', 'laserBandwidth', 'bandwidth_am') #20 kHz @ 32
exp3.add_session('14-27-41', 'h', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(1600, tetrodes=[2,6,8])
exp3.add_session('14-39-35', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-42-05', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('14-43-32', 'i', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('14-49-18', 'j', 'AM', 'am_tuning_curve')
exp3.add_session('14-54-05', None, 'longLaser', 'am_tuning_curve')
exp3.add_session('15-09-37', 'k', 'laserBandwidth', 'bandwidth_am') #16 kHz @ 64
exp3.add_session('15-35-07', 'l', 'noiseAmps', 'am_tuning_curve')
exp3.add_session('15-40-11', 'm', 'laserBandwidth', 'bandwidth_am') #13 kHz @ 32
exp3.add_session('16-04-28', 'n', 'noiseAmps', 'am_tuning_curve')

exp3.add_site(1700, tetrodes=[2,3,4,6,7,8])
exp3.add_session('16-20-21', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('16-22-28', None, 'lasernoisebursts', 'bandwidth_am')
exp3.add_session('16-24-05', 'o', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('16-29-33', 'p', 'AM', 'am_tuning_curve')
exp3.add_session('16-33-54', None, 'longLaser', 'am_tuning_curve') #Cluster 2 on tetrodes 2 and 3 may be receiving from the same neuron as the shapes of the responses for tuning are very similar in both frequency and AM
exp3.add_session('16-54-17', 'q', 'laserBandwidth', 'bandwidth_am') #5 kHz @ 32
exp3.add_session('17-19-07', 'r', 'noiseAmps', 'am_tuning_curve')
exp3.add_session('17-24-13', 's', 'laserBandwidth', 'bandwidth_am') #24 kHz @ 32
exp3.add_session('17-48-58', 't', 'noiseAmps', 'am_tuning_curve')
exp3.add_session('17-53-35', 'u', 'laserBandwidth', 'bandwidth_am') #9 kHz @ 64
exp3.add_session('18-17-47', 'v', 'noiseAmps', 'am_tuning_curve')
exp3.add_session('18-30-17', 'w', 'laserBandwidth', 'bandwidth_am') #14 kHz @ 64
exp3.add_session('18-55-42', 'x', 'noiseAmps', 'am_tuning_curve')
exp3.add_session('19-00-46', 'y', 'laserBandwidth', 'bandwidth_am') #12 kHz @ 64
exp3.add_session('19-28-42', 'z', 'noiseAmps', 'am_tuning_curve')
exp3.add_session('19-33-42', 'aa', 'laserBandwidth', 'bandwidth_am') #17 kHz @ 64
exp3.add_session('20-01-06', 'ab', 'noiseAmps', 'am_tuning_curve')
#Mouse appears quite stressed by current predicament

exp3.maxDepth = 1700


exp4 = celldatabase.Experiment(subject, '2018-08-30', 'left_AC', info=['lateralDiI','TT8ant','soundright'])
experiments.append(exp4)

exp4.laserCalibration = {
    '1.0':3.25,
    '2.0':3.75,
    '3.0':4.25,
    '4.0':4.75,
    '5.0':5.2,
    '7.5':6.5,
    '10.0':7.75
    }

# exp4.add_site(900, tetrodes=[4,6,8])
# exp4.add_session('11-55-38', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('11-57-56', None, 'lasernoisebursts', 'bandwidth_am')
# exp4.add_session('12-00-09', 'a', 'tuningCurve', 'am_tuning_curve' )
# #No frequency tuning
#
# exp4.add_site(1000, tetrodes=[1,2,3,4,6,7,8])
# exp4.add_session('12-13-01', None, 'noisebursts', 'am_tuning_curve')
# #No sound resposne
#
# exp4.add_site(1100, tetrodes=[1,2,8])
# exp4.add_session('12-21-58', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('12-23-37', None, 'lasernoisebursts', 'bandwidth_am')
# exp4.add_session('12-25-13', 'b', 'tuningCurve', 'am_tuning_curve')
# #No frequency tuning
#
# exp4.add_site(1200, tetrodes=[1,4])
# exp4.add_session('12-56-21', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('12-58-01', None, 'lasernoisebursts', 'bandwidth_am')
# exp4.add_session('12-59-30', 'c', 'tuningCurve', 'am_tuning_curve')
#No noticeable frequency tuning

exp4.add_site(1300, tetrodes=[4,8])
exp4.add_session('13-29-40', None, 'nosiebursts', 'am_tuning_curve')
exp4.add_session('13-31-54', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('13-33-52', 'd', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-38-34', 'e', 'AM', 'am_tuning_curve')
exp4.add_session('13-43-31', None, 'longLaser', 'am_tuning_curve')
exp4.add_session('13-47-32', 'f', 'laserBandwidth', 'bandwidth_am') #18 kHz @ 64
exp4.add_session('14-12-02', 'g', 'noiseAmps', 'am_tuning_curve')
exp4.add_session('14-16-40', 'h', 'laserBandwidth', 'bandwidth_am') #10 kHz @ 32
exp4.add_session('14-41-02', 'i', 'noiseAmps', 'am_tuning_curve')

exp4.add_site(1400, tetrodes=[4,8])
exp4.add_session('14-56-58', None, 'nosiebursts', 'am_tuning_curve')
exp4.add_session('14-58-55', None, 'lasernoisebursts', 'bandwidth_am')
exp4.add_session('15-00-29', 'j', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('15-05-16', 'k', 'AM', 'am_tuning_curve')
exp4.add_session('15-09-46', None, 'longLaser', 'am_tuning_curve')
exp4.add_session('15-26-23', 'l', 'laserBandwidth', 'bandwidth_am') #22 kHz @ 32
exp4.add_session('15-50-40', 'm', 'noiseAmps', 'am_tuning_curve')
exp4.add_session('15-55-30', 'n', 'laserBandwidth', 'bandwidth_am') #22 kHz @ 64
exp4.add_session('16-20-03', 'o', 'noiseAmps', 'am_tuning_curve')
exp4.add_session('16-24-36', 'p', 'laserBandwidth', 'bandwidth_am') #10 kHz @ 64

exp4.maxDepth = 1400


exp5 = celldatabase.Experiment(subject, '2018-08-31', 'right_AC', info=['medialDiD','TT1ant','soundleft'])
experiments.append(exp5)

exp5.laserCalibration = {
    '1.0':3.25,
    '2.0':3.7,
    '3.0':4.2,
    '4.0':4.8,
    '5.0':5.1,
    '7.5':6.3,
    '10.0':7.5
    }

exp5.add_site(1100, tetrodes=[1,2,6,7,8])
exp5.add_session('12-11-35', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('12-13-12', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('12-14-45', 'a', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('12-19-22', 'b', 'AM', 'am_tuning_curve')
exp5.add_session('12-23-45', None, 'longLaser', 'am_tuning_curve')
exp5.add_session('12-26-22', 'c', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('12-51-09', 'd', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(1200, tetrodes=[1,2,5,6,7,8])
exp5.add_session('13-02-21', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-03-59', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('13-06-00', 'e', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('13-10-59', 'f', 'AM', 'am_tuning_curve')
exp5.add_session('13-15-14', None, 'longLaser', 'am_tuning_curve')
exp5.add_session('13-18-07', 'g', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('13-43-13', 'h', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(1300, tetrodes=[1,2,4,5,6,7,8])
exp5.add_session('13-55-31', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-57-04', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('13-58-41', 'i', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('14-03-12', 'j', 'AM', 'am_tuning_curve')
exp5.add_session('14-07-30', None, 'longLaser', 'am_tuning_curve')
exp5.add_session('14-11-41', 'k', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('14-37-37', 'l', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('15-01-50', 'm', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(1400, tetrodes=[1,2,4,5,6,7,8])
exp5.add_session('15-15-18', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('15-16-52', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('15-19-07', 'n', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('15-24-20', 'o', 'AM', 'am_tuning_curve')
exp5.add_session('15-28-36', None, 'longLaser', 'am_tuning_curve')
exp5.add_session('15-31-44', 'p', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('15-56-00', 'q', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(1500, tetrodes=[1,2,3,5,6,7,8])
exp5.add_session('16-08-31', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('16-10-03', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('16-12-07', 'r', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('16-16-42', 's', 'AM', 'am_tuning_curve')
exp5.add_session('16-21-20', None, 'longLaser', 'am_tuning_curve')
exp5.add_session('16-26-16', 't', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('16-50-07', 'u', 'noiseAmps', 'am_tuning_curve')

exp5.add_site(1600, tetrodes=[1,2,3,5,6,7,8])
exp5.add_session('17-14-24', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('17-15-59', None, 'lasernoisebursts', 'bandwidth_am')
exp5.add_session('17-17-33', 'v', 'tuningCurve', 'am_tuning_curve')
exp5.add_session('17-22-17', 'w', 'AM', 'am_tuning_curve')
exp5.add_session('17-26-52', None, 'longLaser', 'am_tuning_curve')
exp5.add_session('17-32-17', 'x', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('17-56-44', 'y', 'laserBandwidth', 'bandwidth_am')
exp5.add_session('18-20-43', 'z', 'noiseAmps', 'am_tuning_curve')

exp5.maxDepth = 1600


exp6 = celldatabase.Experiment(subject, '2018-09-02', 'right_AC', info=['middleDiO','TT1ant','soundleft'])
experiments.append(exp6)

exp6.laserCalibration = {
    '1.0':3.25,
    '2.0':3.7,
    '3.0':4.15,
    '4.0':4.65,
    '5.0':5.1,
    '7.5':6.25,
    '10.0':7.4
    }

# exp6.add_site(950, tetrodes=[8])
# exp6.add_session('11-52-14', None, 'noisebursts', 'am_tuning_curve')

exp6.add_site(1000, tetrodes=[6,8])
exp6.add_session('11-59-04', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('12-00-25', None, 'lasernoisebursts', 'bandwidth_am')
exp6.add_session('12-01-57', 'a', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('12-06-46', 'b', 'AM', 'am_tuning_curve')
exp6.add_session('12-11-01', None, 'longLaser', 'am_tuning_curve')
exp6.add_session('12-13-38', 'c', 'laserBandwidth', 'bandwidth_am')
exp6.add_session('12-37-37', 'd', 'noiseAmps', 'am_tuning_curve')

exp6.add_site(1100, tetrodes=[6,8])
exp6.add_session('12-55-46', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('12-57-17', None, 'lasernoisebursts', 'bandwidth_am')
exp6.add_session('12-58-57', 'e', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('13-03-31', 'f', 'AM', 'am_tuning_curve')
exp6.add_session('13-07-45', None, 'longLaser', 'am_tuning_curve')
exp6.add_session('13-10-08', 'g', 'laserBandwidth', 'bandwidth_am')
exp6.add_session('13-35-02', 'h', 'laserBandwidth', 'bandwidth_am')
exp6.add_session('14-00-00', 'i', 'noiseAmps', 'am_tuning_curve')

exp6.add_site(1200, tetrodes=[6,8])
exp6.add_session('14-12-17', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('14-13-45', None, 'lasernoisebursts', 'bandwidth_am')
exp6.add_session('14-15-36', 'j', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('14-20-52', 'k', 'AM', 'am_tuning_curve')
exp6.add_session('14-25-28', None, 'longLaser', 'am_tuning_curve')
exp6.add_session('14-29-20', 'l', 'laserBandwidth', 'bandwidth_am')
exp6.add_session('14-55-54', 'm', 'noiseAmps', 'am_tuning_curve')

exp6.add_site(1300, tetrodes=[6,7,8])
exp6.add_session('15-07-44', None, 'noisebursts', 'am_tuning_curve')
exp6.add_session('15-09-22', None, 'lasernoisebursts', 'bandwidth_am')
exp6.add_session('15-10-55', 'n', 'tuningCurve', 'am_tuning_curve')
exp6.add_session('15-15-36', 'o', 'AM', 'am_tuning_curve')
exp6.add_session('15-19-52', None, 'longLaser', 'am_tuning_curve')
exp6.add_session('15-22-00', 'p', 'laserBandwidth', 'bandwidth_am')
exp6.add_session('15-47-33', 'q', 'noiseAmps', 'am_tuning_curve')

#shank 1 flexing
exp6.maxDepth = 1300


exp7 = celldatabase.Experiment(subject, '2018-09-03', 'right_AC', info=['middleDiD','TT1ant','soundleft'])
experiments.append(exp7)

#control day, tether not attached to probe
exp7.laserCalibration = {
    '1.0':3.05,
    '2.0':3.25,
    '3.0':3.45,
    '4.0':3.7,
    '5.0':3.9,
    '7.5':4.5,
    '10.0':5.0
    }

#shank 1 not penetrating

exp7.add_site(1100, tetrodes=[6,8])
exp7.add_session('12-33-01', None, 'noisebursts', 'am_tuning_curve')
exp7.add_session('12-34-36', None, 'lasernoisebursts', 'bandwidth_am')
exp7.add_session('12-36-09', 'a', 'tuningCurve', 'am_tuning_curve')
exp7.add_session('12-41-01', 'b', 'AM', 'am_tuning_curve')
exp7.add_session('12-45-21', None, 'longLaser', 'am_tuning_curve')
exp7.add_session('12-47-52', 'c', 'laserBandwidthControl', 'bandwidth_am')
exp7.add_session('13-11-57', 'd', 'noiseAmps', 'am_tuning_curve')

exp7.add_site(1200, tetrodes=[4,5,6,7,8])
exp7.add_session('13-24-36', None, 'noisebursts', 'am_tuning_curve')
exp7.add_session('13-26-04', None, 'lasernoisebursts', 'bandwidth_am')
exp7.add_session('13-27-47', 'e', 'tuningCurve', 'am_tuning_curve')
exp7.add_session('13-32-31', 'f', 'AM', 'am_tuning_curve')
exp7.add_session('13-36-52', None, 'longLaser', 'am_tuning_curve')
exp7.add_session('13-41-51', 'g', 'laserBandwidthControl', 'bandwidth_am')
exp7.add_session('14-05-53', 'h', 'laserBandwidthControl', 'bandwidth_am')
exp7.add_session('14-29-49', 'i', 'noiseAmps', 'am_tuning_curve')

exp7.add_site(1300, tetrodes=[4,5,6,7,8])
exp7.add_session('14-44-58', None, 'noisebursts', 'am_tuning_curve')
exp7.add_session('14-46-27', None, 'lasernoisebursts', 'bandwidth_am')
exp7.add_session('14-48-10', 'j', 'tuningCurve', 'am_tuning_curve')
exp7.add_session('14-52-49', 'k', 'AM', 'am_tuning_curve')
exp7.add_session('14-57-36', None, 'longLaser', 'am_tuning_curve')
exp7.add_session('15-01-17', 'l', 'laserBandwidthControl', 'bandwidth_am')
exp7.add_session('15-25-20', 'm', 'noiseAmps', 'am_tuning_curve')

exp7.maxDepth = 1300


exp8 = celldatabase.Experiment(subject, '2018-09-04', 'right_AC', info=['lateralDiO','TT1ant','soundleft'])
experiments.append(exp8)

exp8.laserCalibration = {
    '1.0':3.2,
    '2.0':3.65,
    '3.0':4.1,
    '4.0':4.55,
    '5.0':5.0,
    '7.5':6.15,
    '10.0':7.25
    }

#shank 2 not penetrating well
exp8.add_site(1100, tetrodes=[6,8])
exp8.add_session('11-17-25', None, 'noisebursts', 'am_tuning_curve')
exp8.add_session('11-19-01', None, 'lasernoisebursts', 'bandwidth_am')
exp8.add_session('11-20-38', 'a', 'tuningCurve', 'am_tuning_curve')
exp8.add_session('11-25-17', 'b', 'AM', 'am_tuning_curve')
exp8.add_session('11-29-41', None, 'longLaser', 'am_tuning_curve')
exp8.add_session('11-31-46', 'c', 'laserBandwidth', 'bandwidth_am')
exp8.add_session('11-57-20', 'd', 'noiseAmps', 'am_tuning_curve')

exp8.add_site(1400, tetrodes=[2,5,6,7,8])
exp8.add_session('12-59-56', None, 'noisebursts', 'am_tuning_curve')
exp8.add_session('13-01-20', None, 'lasernoisebursts', 'bandwidth_am')
exp8.add_session('13-02-54', 'e', 'tuningCurve', 'am_tuning_curve')
exp8.add_session('13-07-45', 'f', 'AM', 'am_tuning_curve')
exp8.add_session('13-13-30', None, 'longLaser', 'am_tuning_curve')
#nothing but garbage
exp8.add_session('13-19-05', None, 'noisebursts', 'am_tuning_curve')
exp8.add_session('13-20-40', 'g', 'tuningCurve', 'am_tuning_curve')
exp8.add_session('13-25-40', 'h', 'AM', 'am_tuning_curve')
exp8.add_session('13-29-56', None, 'longLaser', 'am_tuning_curve')
exp8.add_session('13-32-05', 'i', 'laserBandwidth', 'bandwidth_am')
exp8.add_session('13-58-24', 'j', 'noiseAmps', 'am_tuning_curve')

exp8.add_site(1500, tetrodes=[2,5,6,7,8])
exp8.add_session('14-27-34', None, 'noisebursts', 'am_tuning_curve')
exp8.add_session('14-29-09', None, 'lasernoisebursts', 'bandwidth_am')
exp8.add_session('14-30-52', 'k', 'tuningCurve', 'am_tuning_curve')
exp8.add_session('14-36-47', 'l', 'AM', 'am_tuning_curve')
exp8.add_session('14-41-37', None, 'longLaser', 'am_tuning_curve')
exp8.add_session('14-45-25', 'm', 'laserBandwidth', 'bandwidth_am')
exp8.add_session('15-10-54', 'n', 'laserBandwidth', 'bandwidth_am')
exp8.add_session('15-35-22', 'o', 'noiseAmps', 'am_tuning_curve')

exp8.maxDepth = 1500
