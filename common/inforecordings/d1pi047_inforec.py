from jaratoolbox import celldatabase

subject = 'd1pi047'
experiments=[]

# exp0 = celldatabase.Experiment(subject, '2020-02-22', 'right_AudStr', 'anteriorDiI',
    # info=['TT1left', 'soundLeft', 'A4x2-tet'])
# experiments.append(exp0)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used left speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 19.9
1.0: 1.85, 24.2
1.5: 2.3, 28.9
2.0: 2.95, 35.1
2.5: 3.35, 40.1
3.0: 3.95, 46.3
3.5: 4.85, 55.6
4.0: 5.7, 64.6
"""

# Animal in rig at: 11:47
# Animal out at: 1:12
# as per usual, mouse bled a ton from left craniotomy, so switched to right
# unfortunately, right craniotomy ALSO bled a ton
# decided not to record from him today seeing as he lost so much blood and should rest to recover
# mouse super unstable on feet when taken out of rig


exp0 = celldatabase.Experiment(subject, '2020-02-24', 'left_AudStr',
                               recordingTrack='anteriorDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp0)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.45, 19.9
1.0: 1.85, 24.2
1.5: 2.3, 28.9
2.0: 2.95, 35.1
2.5: 3.35, 40.1
3.0: 3.95, 46.3
3.5: 4.85, 55.6
4.0: 5.7, 64.6
"""

# Animal in rig at: 8:54
# Probe in at: 9:06

exp0.add_site(2900, egroups=[2,6,8])
exp0.add_session('09-20-33', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('09-21-43', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('09-23-19', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('09-25-39', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('09-28-11', 'b', 'am', 'am_tuning_curve')

exp0.add_site(3200, egroups=[1,2,3,4,6])
exp0.add_session('09-40-55', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('09-42-57', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('09-44-05', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('09-45-55', 'c', 'tuningTest', 'am_tuning_curve')
exp0.add_session('09-48-27', 'd', 'am', 'am_tuning_curve')
exp0.add_session('09-54-35', 'e', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3300, egroups=[1,2,3,4,6,8])
exp0.add_session('10-34-39', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('10-35-47', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('10-36-56', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('10-38-47', 'f', 'tuningTest', 'am_tuning_curve')
exp0.add_session('10-41-38', 'g', 'am', 'am_tuning_curve')
exp0.add_session('10-49-02', 'h', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3400, egroups=[2,4,6,8])
exp0.add_session('11-37-17', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('11-39-07', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('11-40-23', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('11-43-17', 'i', 'tuningTest', 'am_tuning_curve')
exp0.add_session('11-45-40', 'j', 'am', 'am_tuning_curve')
exp0.add_session('11-52-22', 'k', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3500, egroups=[1,2,3,4,6,7,8])
exp0.add_session('12-51-25', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('12-52-51', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('12-53-59', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('12-56-03', 'l', 'tuningTest', 'am_tuning_curve')
exp0.add_session('12-58-21', 'm', 'am', 'am_tuning_curve')
exp0.add_session('13-05-01', 'n', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(3600, egroups=[5,6,7,8])
exp0.add_session('14-18-44', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-20-18', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('14-23-21', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('14-25-16', 'o', 'tuningTest', 'am_tuning_curve')
exp0.add_session('14-27-51', 'p', 'am', 'am_tuning_curve')
exp0.add_session('14-34-44', 'q','tuningCurve','am_tuning_curve')

exp0.maxDepth = 3600

exp1 = celldatabase.Experiment(subject, '2020-02-25', 'left_AudStr',
                               recordingTrack='anteriorMidDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp1)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.52, 20.0
1.0: 2.10, 25.9
1.5: 2.70, 32.3
2.0: 3.50, 40.2
2.5: 4.20, 47.6 Nice
3.0: 5.50, 61.2
3.5: 6.50, 71.4
4.0: 8.10, 88.1
"""

# Animal in rig at: 10:39
# Probe in at: 10:45  # Accidentally drove down to 1600 and then switched to fast and went down to ~4k. Reset to 2200 and on slow went to 3000

exp1.add_site(3000, egroups=[2])
exp1.add_session('11-12-56', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('11-14-08', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('11-15-20', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('11-18-02', 'a', 'tuningTest', 'am_tuning_curve')
exp1.add_session('11-20-49', 'b', 'am', 'am_tuning_curve')

exp1.add_site(3500, egroups=[1,2,4,5,6,7,8])
exp1.add_session('13-43-02', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('13-44-34', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('13-46-39', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('13-50-14', 'c', 'tuningTest', 'am_tuning_curve')
exp1.add_session('13-52-51', 'd', 'am', 'am_tuning_curve')
exp1.add_session('14-00-37', 'e', 'tuningCurve', 'am_tuning_curve')

exp1.maxDepth = 3600

exp2 = celldatabase.Experiment(subject, '2020-02-26', 'left_AudStr',
                               recordingTrack='posteriorMidDiI', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp2)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.46, 19.3
1.0: 1.92, 24.0
1.5: 2.50, 30.0
2.0: 3.08, 35.8
2.5: 3.75, 42.7
3.0: 4.50, 50.5
3.5: 5.65, 62.5
4.0: 6.50, 71.3
"""

# Animal in rig at: 10:45
# Probe in at: 10:54

# HEY MR COPY PASTE WHAT'S THE ACTUAL DYE USED FOR THIS EXPERIMENT
exp2.add_site(3400, egroups=[1,2])
exp2.add_session('11-49-48', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('11-50-57', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('11-52-09', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('11-53-58', 'a', 'tuningTest', 'am_tuning_curve')
exp2.add_session('11-56-17', 'b', 'am', 'am_tuning_curve')

exp2.add_site(3500, egroups=[1,2,4])
exp2.add_session('12-25-54', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('12-27-02', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('12-28-11', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('12-30-09', 'c', 'tuningTest', 'am_tuning_curve')
exp2.add_session('12-33-00', 'd', 'am', 'am_tuning_curve')
exp2.add_session('12-39-05', 'e', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3700, egroups=[2,3,4])
exp2.add_session('13-39-40', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('13-40-50', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('13-43-33', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('13-45-07', 'f', 'tuningTest', 'am_tuning_curve')
exp2.add_session('13-47-45', 'g', 'am', 'am_tuning_curve')
exp2.add_session('13-55-40', 'h', 'tuningCurve', 'am_tuning_curve')

exp2.add_site(3800, egroups=[1,2,3,4])
exp2.add_session('16-01-00', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('16-03-26', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('16-07-23', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('16-11-37', 'i', 'tuningTest', 'am_tuning_curve')
exp2.add_session('16-14-08', 'j', 'am', 'am_tuning_curve')
exp2.add_session('16-27-05', 'k', 'tuningCurve', 'am_tuning_curve')  # Open ephys possibly crashed. The counter is still going but the LFP and spikes viewer froze
# Hard drive was full. Tuning curve likely lost

exp2.maxDepth = 3800

exp3 = celldatabase.Experiment(subject, '2020-02-27', 'left_AudStr',
                               recordingTrack='posteriorDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp3)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used right speaker; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.46, 19.3
1.0: 1.92, 24.0
1.5: 2.50, 30.0
2.0: 3.08, 35.8
2.5: 3.75, 42.7
3.0: 4.50, 50.5
3.5: 5.65, 62.5
4.0: 6.50, 71.3
"""

# Animal in rig at: 10:45
# Probe in at: 12:16

# COPY PASTER FAILS TO CHANGE THE DATE ON THE EXPERIMENT YET AGAIN. LISTEN THERE WAS A LOT GOING ON OKAY
exp3.add_site(3100, egroups=[1,2,4,5])
exp3.add_session('13-00-22', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('13-01-34', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('13-02-43', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('13-04-33', 'a', 'tuningTest', 'am_tuning_curve')
exp3.add_session('13-06-50', 'b', 'am', 'am_tuning_curve')

exp3.maxDepth = 3750

exp4 = celldatabase.Experiment(subject, '2020-02-28', 'right_AudStr',
                               recordingTrack='middleDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundLeft', 'A4x2-tet'])
experiments.append(exp4)

# 50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 220 AM, 1760 tuningCurve
# Used left; laser (445 nm) set to 2.0 mW; Probe D65D; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
0.5: 1.50, 19.3
1.0: 2.00, 24.5
1.5: 2.65, 31.0
2.0: 3.25, 37.4
2.5: 3.90, 44.2
3.0: 4.80, 53.4
3.5: 5.98, 65.5
4.0: 6.80, 73.4
"""

# Animal in rig at: 10:34
# Probe in at: 10:45

exp4.add_site(3100, egroups=[1,4,6,7,8])
exp4.add_session('11-02-11', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('11-03-22', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('11-04-35', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('11-06-05', 'a', 'tuningTest', 'am_tuning_curve')
exp4.add_session('11-09-03', 'b', 'am', 'am_tuning_curve')

exp4.add_site(3200, egroups=[8])
exp4.add_session('11-26-31', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('11-28-09', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('11-29-27', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('11-31-02', 'c', 'tuningTest', 'am_tuning_curve')
exp4.add_session('11-33-36', 'd', 'am', 'am_tuning_curve')

exp4.maxDepth = 3400
