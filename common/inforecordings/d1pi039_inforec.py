from jaratoolbox import celldatabase

subject = 'd1pi039'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2019-07-30', 'right_AudStr',
                               recordingTrack='MedialDiI', probe='A4x2-tet',
                               info=['TT1ant', 'soundLeft', 'A4x2-tet'])
#experiments.append(exp0)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe M629; Rig 2

"""
Laser Calibration
Power: Value on laser dial
0.5: 1.95
1.0: 3.1
1.5: 4.5
2.0: 6.25
2.5: 9.5
"""

# Animal in rig at: 09:26
# Probe in at: 9:50

# exp0.add_site(2902, egroups=[1,2,3,4,6])
# exp0.add_session('10-26-48', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('10-28-21', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('10-30-08', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('10-32-58', 'a', 'tuningTest', 'am_tuning_curve')
# No cells of note

# exp0.add_site(3100, egroups=[1,2,3,4,6])
# exp0.add_session('11-24-17', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('11-25-48', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('11-27-06', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('11-29-37', 'b', 'tuningTest', 'am_tuning_curve')
# No sound or laser responsive cells

# exp0.add_site(3200, egroups=[1,2,3,4,6])
# exp0.add_session('11-45-54', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('11-47-11', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('11-48-24', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('11-49-57', 'c', 'tuningTest', 'am_tuning_curve')

# exp0.add_site(3300, egroups=[1,2,3,4,6])
# exp0.add_session('12-58-36', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('13-11-11', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('13-12-31', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('13-14-09', 'd', 'tuningTest', 'am_tuning_curve')

# exp0.add_site(3400, egroups=[1,2,3,4,6])
# exp0.add_session('13-29-29', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('13-30-43', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('13-32-19', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('13-34-07', 'e', 'tuningTest', 'am_tuning_curve')

# exp0.add_site(3500, egroups=[1,2,3,4])
# exp0.add_session('14-00-04', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('14-01-15', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('14-02-27', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('14-04-21', 'f', 'tuningTest', 'am_tuning_curve')

# exp0.add_site(3600, egroups=[1,2,3,4,6])
# exp0.add_session('14-21-33', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('14-22-47', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('14-24-39', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('14-26-20', 'g', 'tuningTest', 'am_tuning_curve')

# exp0.add_site(3700, egroups=[1,2,3,4,6])
# exp0.add_session('14-50-46', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('14-54-21', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('14-55-34', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('14-57-13', 'h', 'tuningTest', 'am_tuning_curve')

# exp0.add_site(3800, egroups=[1,2,3,4,6])
# exp0.add_session('15-22-17', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('15-23-53', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('15-25-07', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('15-26-48', 'i', 'tuningTest', 'am_tuning_curve')

# exp0.add_site(3900, egroups=[1,2,3,4,5])
# exp0.add_session('15-40-55', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('15-45-59', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('15-47-53', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('15-50-13', 'j', 'tuningTest', 'am_tuning_curve')

# exp0.add_site(4000, egroups=[1,2,3,5,6])
# exp0.add_session('16-25-26', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('16-26-42', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('16-29-19', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('16-33-01', 'k', 'tuningTest', 'am_tuning_curve')

# exp0.add_site(4100, egroups=[1,2,3,5,6])
# exp0.add_session('16-48-14', None, 'noisebursts', 'am_tuning_curve')
# exp0.add_session('16-49-51', None, 'laserpulse', 'am_tuning_curve')
# exp0.add_session('16-51-04', None, 'lasertrain', 'am_tuning_curve')
# exp0.add_session('16-52-43', 'l', 'tuningTest', 'am_tuning_curve')

exp0.maxDepth = 4100


exp1 = celldatabase.Experiment(subject, '2019-07-31', 'right_AudStr',
                               recordingTrack='MiddleDiD', probe='A4x2-tet',
                               info=['TT1ant', 'soundLeft', 'A4x2-tet'])
experiments.append(exp1)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used left speaker;laser (445 nm) set to 2.0 mW; Probe CEC2; Rig 2

"""
Laser Calibration
Power: Value on laser dial
0.5: 1.65
1.0: 2.4
1.5: 3.3
2.0: 4.2
2.5: 5.5
3.0: 6.75
3.5: 8.6
"""

# Animal in rig at: 09:29
# Probe in at: 09:41

exp1.add_site(2501, egroups=[2,3,4,6])
exp1.add_session('11-05-36', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('11-06-59', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('11-08-15', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('11-09-48', 'a', 'tuningTest', 'am_tuning_curve')
exp1.add_session('11-17-46', 'b', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('11-53-56', 'c', 'am', 'am_tuning_curve')

# exp1.add_site(2600, egroups=[2,3,6])
# exp1.add_session('12-30-43', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('12-32-42', None, 'laserpulse', 'am_tuning_curve')
# exp1.add_session('12-33-54', None, 'lasertrain', 'am_tuning_curve')
# exp1.add_session('12-35-44', 'd', 'tuningTest', 'am_tuning_curve')

# exp1.add_site(2700, egroups=[1,2,3,4,6])
# exp1.add_session('13-06-26', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('13-08-36', None, 'laserpulse', 'am_tuning_curve')
# exp1.add_session('13-10-24', None, 'lasertrain', 'am_tuning_curve')
# exp1.add_session('13-12-15', 'e', 'tuningTest', 'am_tuning_curve')

# exp1.add_site(2800, egroups=[1,2,3,4,6])
# exp1.add_session('13-29-58', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('13-31-06', None, 'laserpulse', 'am_tuning_curve')
# exp1.add_session('13-32-20', None, 'lasertrain', 'am_tuning_curve')
# exp1.add_session('13-33-52', 'f', 'tuningTest', 'am_tuning_curve')

exp1.add_site(2900, egroups=[1,2,3,4,6])
exp1.add_session('16-00-21', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-01-50', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-03-01', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('16-04-39', 'g', 'tuningTest', 'am_tuning_curve')
exp1.add_session('16-09-08', 'h', 'tuningCurve', 'am_tuning_curve') # accidentally stopped openEphys beofre paradigm
exp1.add_session('16-40-26', 'i', 'am', 'am_tuning_curve')

exp1.add_site(3000, egroups=[1,2,3,4,6])
exp1.add_session('17-06-30', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('17-07-46', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('17-08-54', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('17-10-29', 'j', 'tuningTest', 'am_tuning_curve')
exp1.add_session('17-13-52', 'k', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('17-43-04', 'l', 'am', 'am_tuning_curve')

exp1.maxDepth = 3000

exp2 = celldatabase.Experiment(subject, '2019-08-06', 'left_AudStr',
                               recordingTrack='middleDiI', probe='A4x2-tet',
                               info=['TT1lateral', 'soundRight', 'A4x2-tet'])
experiments.append(exp2)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used right speaker;laser (445 nm) set to 2.0 mW; Probe M632; Rig 2

"""
Laser Calibration
Power: Value on laser dial
0.5: 1.65
1.0: 2.55
1.5: 3.55
2.0: 4.75
2.5: 6.0
3.0: 7.75
"""

# Animal in rig at: 10:10
# Probe in at: 11:25

exp2.add_site(2200, egroups=[1,2,3,6,7])
exp2.add_session('12-13-05', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('12-14-56', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('12-16-37', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('12-18-17', 'a', 'tuningTest', 'am_tuning_curve')
exp2.add_session('12-23-37', 'b', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-05-56', 'c', 'am', 'am_tuning_curve')

# exp2.add_site(2300, egroups=[1,2,3,7,8])
# exp2.add_session('13-33-14', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('13-36-47', None, 'laserpulse', 'am_tuning_curve')
# exp2.add_session('13-38-34', None, 'lasertrain', 'am_tuning_curve')
# exp2.add_session('13-40-32', 'd', 'tuningTest', 'am_tuning_curve')

# exp2.add_site(2400, egroups=[1,2,3])
# exp2.add_session('13-57-40', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('13-58-48', None, 'laserpulse', 'am_tuning_curve')
# exp2.add_session('14-01-58', None, 'lasertrain', 'am_tuning_curve')
# exp2.add_session('14-09-15', 'e', 'tuningTest', 'am_tuning_curve')

# exp2.add_site(2500, egroups=[1,2,3,7,8])
# exp2.add_session('14-25-48', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('14-27-57', None, 'laserpulse', 'am_tuning_curve')
# exp2.add_session('14-29-32', None, 'lasertrain', 'am_tuning_curve')
# exp2.add_session('14-31-20', 'f', 'tuningTest', 'am_tuning_curve')

# exp2.add_site(2600, egroups=[1,2,3,6,7,8])
# exp2.add_session('15-01-03', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('15-02-15', None, 'laserpulse', 'am_tuning_curve')
# exp2.add_session('15-04-26', None, 'lasertrain', 'am_tuning_curve')
# exp2.add_session('15-06-03', 'g', 'tuningTest', 'am_tuning_curve')

# exp2.add_site(2700, egroups=[1,2,3,7,8])
# exp2.add_session('15-32-07', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('15-33-44', None, 'laserpulse', 'am_tuning_curve')
# exp2.add_session('15-35-03', None, 'lasertrain', 'am_tuning_curve')
# exp2.add_session('15-36-34', 'h', 'tuningTest', 'am_tuning_curve')

# exp2.add_site(2800, egroups=[1,2,3,4,6,7,8])
# exp2.add_session('16-04-31', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('16-05-53', None, 'laserpulse', 'am_tuning_curve')
# exp2.add_session('16-07-04', None, 'lasertrain', 'am_tuning_curve')
# exp2.add_session('16-10-39', 'i', 'tuningTest', 'am_tuning_curve')

# exp2.add_site(2900, egroups=[1,2,3,6,7,8])
# exp2.add_session('16-25-05', None, 'noisebursts', 'am_tuning_curve')
# exp2.add_session('16-26-13', None, 'laserpulse', 'am_tuning_curve')
# exp2.add_session('16-27-22', None, 'lasertrain', 'am_tuning_curve')
# exp2.add_session('16-29-30', 'j', 'tuningTest', 'am_tuning_curve')

# Tetrode 3 has the reference
exp2.add_site(3000, egroups=[1,2,4,5,6,7,8])
exp2.add_session('16-43-34', None, 'noiseburst', 'am_tuning_curve')
exp2.add_session('16-44-53', None, 'laserpulse', 'am_tuning_curve')
exp2.add_session('16-46-06', None, 'lasertrain', 'am_tuning_curve')
exp2.add_session('16-47-45', 'k', 'tuningTest', 'am_tuning_curve')
exp2.add_session('16-56-25', 'l', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('17-28-42', 'm', 'am', 'am_tuning_curve')

exp2.maxDepth = 3000


# exp3 = celldatabase.Experiment(subject, '2019-08-07', 'left_AudStr', 'anteriorDiD',
    # info=['TT1ant', 'soundRight', 'A4x2-tet'])
# experiments.append(exp3)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used right speaker;laser (445 nm) set to 2.0 mW; Probe M632; Rig 2

"""
Laser Calibration
Power: Value on laser dial
0.5: 2.11
1.0: 3.60
1.5: 5.00
2.0: 6.84
2.5: 9.5
3.0: N/A
"""

# Animal in rig at: 10:31
# Probe in at: 10:43
# Probe reinserted at 11:53

# Tetrode 3 has the reference
# exp3.add_site(2900, egroups=[1,2,4,5,6,7,8])
# exp3.add_session('11-18-14', None, 'noisebursts', 'am_tuning_curve')

#NOTE The probe was pulled out and reinserted close to the same position at this point

# exp3.add_site(2900, egroups=[1,2,4,5,6,7,8])
# exp3.add_session('12-01-30', None, 'noisebursts', 'am_tuning_curve')
#
# exp3.maxDepth = 2900


exp4 = celldatabase.Experiment(subject, '2019-08-08', 'left_AudStr',
                               recordingTrack='posteriourDiD', probe='A4x2-tet',
                               info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp4)

#50 noiseburst, 50 laser pulse, 40 laser train, 160 tuningTest, 1760 tc, 220 AM
#Used right speaker;laser (445 nm) set to 2.0 mW; Probe M677; Rig 2

"""
Laser Calibration
Power: Value on laser dial
0.5: 1.45
1.0: 1.9
1.5: 2.45
2.0: 3.05
2.5: 3.6
3.0: 4.45
3.5: 5.5
4.0: 7.25
"""

# Animal in rig at: 11:35
# Probe in at: 11:45

# exp4.add_site(2800, egroups=[7,8])
# exp4.add_session('12-27-51', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(2900, egroups=[1,2,3,4,6,7,8])
exp4.add_session('13-14-47', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('13-16-10', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('13-17-26', 'a', 'tuningTest', 'am_tuning_curve')
exp4.add_session('13-20-20', None, 'lasertrain', 'am_tuning_curve')
exp4.add_session('13-23-47', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('13-25-36', 'b', 'tuningCurve', 'am_tuning_curve') #channels went quiet halfway through, paused paradigm to add saline to well

exp4.maxDepth = 2900
