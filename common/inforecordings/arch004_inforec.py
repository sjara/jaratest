# TODO:
#    Recordings will not have sound trigger because we need to
#    fix sound sync in jaratoolbox.SOUND_SERVER

# PLAN:
#   ISIs: for 100ms, 1.2 +/- 0.2; for 500ms, 2 +/- 0.4
#   60dB 100ms white noise, 100 trials
#   frequency tuning: 70dB 100ms pure tones, 2 to 40kHz, 16 freq, 320 trials (20 per cond)
#   frequency tuning (with laser, if see tuning): same as above but 50 and 70dB and
#                                                 0.5 proportion laser, 1320 trials (20 per cond)
#   am tuning (with laser): 9 rates from 4 to 64Hz, 60dB, 0.5 sec, 0.5 proportion with laser,
#                           360 trials (20 per cond)

from jaratoolbox import celldatabase

subject = 'arch004'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2021-05-26', 'left_AudStr', info=['TT1left', 'soundRight', 'A4x2-tet'])
experiments.append(exp0)

# Used right speaker; laser (520 nm) at 5mW; Probe DD02, no dye; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
1.0: 3.9, 20.5
2.0: 5.0, 36.6
3.0: 6.0, 52.1
4.0: 7.0, 68.6
5.0: 8.05, 84.8
"""

# Animal in rig at: 9:30
# Probe in at: 10:25

# probe oriented along ML axis, but gets pushed a little L due to thickness of middle glue wall
# may attempt recording with probe oriented along AP axis in future

exp0.add_site(2800, tetrodes=[2,4,5,6]) # TT3 reference
exp0.add_session('10-56-01', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('10-59-01', 'a', 'tuningTest', 'am_tuning_curve')
exp0.add_session('11-06-51', 'b', 'laserAM', 'am_tuning_curve')
exp0.add_session('11-22-48', 'c', 'laserTuningCurve', 'am_tuning_curve')

exp0.add_site(3000, tetrodes=[1,2,4,5,6]) # TT3 reference
exp0.add_session('12-01-05', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-04-02', 'd', 'tuningTest', 'am_tuning_curve')
exp0.add_session('12-11-34', 'e', 'laserAM', 'am_tuning_curve')
exp0.add_session('12-27-23', 'f', 'laserTuningCurve', 'am_tuning_curve')

exp0.add_site(3200, tetrodes=[1,2,4,5,6]) # TT3 reference
exp0.add_session('13-06-32', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-09-02', 'g', 'tuningTest', 'am_tuning_curve')
exp0.add_session('13-17-17', 'h', 'laserAM', 'am_tuning_curve')
exp0.add_session('13-33-11', 'i', 'laserTuningCurve', 'am_tuning_curve')

exp0.add_site(3400, tetrodes=[1,2,4,5,6]) # TT3 reference
exp0.add_session('14-12-28', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-15-22', 'j', 'tuningTest', 'am_tuning_curve')
exp0.add_session('14-23-00', 'k', 'laserAM', 'am_tuning_curve')
exp0.add_session('14-39-13', 'l', 'laserTuningCurve', 'am_tuning_curve')

exp0.add_site(3600, tetrodes=[1,2,4,5,6]) # TT3 reference
exp0.add_session('15-14-45', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-18-56', 'm', 'tuningTest', 'am_tuning_curve')
exp0.add_session('15-26-41', 'n', 'laserAM', 'am_tuning_curve')
exp0.add_session('15-44-14', 'o', 'laserTuningCurve', 'am_tuning_curve')

# Animal out at: 4:25
exp0.maxDepth = 3600


exp1 = celldatabase.Experiment(subject, '2021-05-27', 'left_AudStr', info=['TT1ant', 'soundRight', 'A4x2-tet'])
experiments.append(exp1)

# Used right speaker; laser (520 nm) at 5mW; Probe DD02, no dye; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
1.0: 3.9, 20.0
2.0: 4.9, 35.2
3.0: 5.9, 50.9
4.0: 6.9, 66.8
5.0: 7.85, 81.8
"""

# Animal in rig at: 8:43
# Probe in at: 9:01

# probe oriented along AP axis, inserted on medial side of craniotomy
# doing 160 trials of test tuning curve (10 trials per cond) to speed it up
# other sessions same as before

exp1.add_site(3000, tetrodes=[1,2,3,5,6]) # TT4 reference
exp1.add_session('09-07-50', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('09-10-21', 'a', 'tuningTest', 'am_tuning_curve')
exp1.add_session('09-14-41', 'b', 'laserAM', 'am_tuning_curve')
exp1.add_session('09-31-28', 'c', 'laserTuningCurve', 'am_tuning_curve')

exp1.add_site(3200, tetrodes=[1,2,4,5,6]) # TT3 reference
exp1.add_session('10-11-12', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('10-13-44', 'd', 'tuningTest', 'am_tuning_curve')
exp1.add_session('10-17-45', 'e', 'laserAM', 'am_tuning_curve')

exp1.add_site(3400, tetrodes=[1,2,3,4,6]) # TT5 reference
exp1.add_session('10-41-33', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('10-44-05', 'f', 'tuningTest', 'am_tuning_curve')
exp1.add_session('10-48-08', 'g', 'laserAM', 'am_tuning_curve')
exp1.add_session('11-03-57', 'h', 'laserTuningCurve', 'am_tuning_curve')

exp1.add_site(3600, tetrodes=[1,2,3,4,5]) # TT6 reference
exp1.add_session('11-45-47', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('11-48-19', 'i', 'tuningTest', 'am_tuning_curve')
exp1.add_session('11-52-16', 'j', 'laserAM', 'am_tuning_curve')
exp1.add_session('12-08-06', 'k', 'laserTuningCurve', 'am_tuning_curve')

exp1.add_site(3700, tetrodes=[1,2,3,4,6]) # TT5 reference
exp1.add_session('12-44-47', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('12-47-22', 'l', 'tuningTest', 'am_tuning_curve')
exp1.add_session('12-51-22', 'm', 'laserAM', 'am_tuning_curve')
exp1.add_session('13-07-26', 'n', 'laserTuningCurve', 'am_tuning_curve')

# Animal out at: 1:48
exp1.maxDepth = 3700


exp2 = celldatabase.Experiment(subject, '2021-05-29', 'left_AudStr', info=['TT1ant', 'soundRight', 'A4x2-tet'])
experiments.append(exp2)

# Used right speaker; laser (520 nm) at 5mW; Probe DD02, no dye; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
1.0: 4.1, 23.0
2.0: 5.25, 40.6
3.0: 6.4, 58.9
4.0: 7.55, 77.1
5.0: 8.75, 96.1
"""

# Animal in rig at: 9:29
# Probe in at: 9:46

# probe oriented along AP axis, inserted on medial side of craniotomy
# doing 160 trials of test tuning curve (10 trials per cond) to speed it up
# adding 'laser' sessions consisting of 200 trials, 50/50 with 500 ms laser

exp2.add_site(3000, tetrodes=[4,5,6]) # TT1 ref
exp2.add_session('09-50-34', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('09-53-10', 'a', 'tuningTest', 'am_tuning_curve')
# no sound responses

exp2.add_site(3400, tetrodes=[3,4,5,6]) # TT1 ref
exp2.add_session('10-08-27', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('10-11-01', 'b', 'tuningTest', 'am_tuning_curve')
exp2.add_session('10-15-05', 'c', 'laserAM', 'am_tuning_curve')
exp2.add_session('10-30-52', 'd', 'laserTuningCurve', 'am_tuning_curve')

exp2.add_site(3600, tetrodes=[2,3,4,5,6]) # TT1 ref
exp2.add_session('11-11-50', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-14-18', 'e', 'tuningTest', 'am_tuning_curve')
exp2.add_session('11-18-18', 'f', 'laserAM_bad', 'am_tuning_curve') # cut short, ephys computer ran out of space
exp2.add_session('11-55-26', 'g', 'laserAM', 'am_tuning_curve')
exp2.add_session('12-11-22', 'h', 'laser', 'am_tuning_curve')

exp2.add_site(3700, tetrodes=[1,2,3,4,6]) # TT5 ref
exp2.add_session('12-27-05', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-32-24', 'i', 'tuningTest', 'am_tuning_curve')
exp2.add_session('12-36-28', 'j', 'laserAM', 'am_tuning_curve')
exp2.add_session('12-52-28', 'k', 'laser', 'am_tuning_curve')
exp2.add_session('13-01-26', 'l', 'laserTuningCurve', 'am_tuning_curve')

exp2.maxDepth = 3700

# --- exp3 is a control penetration (laser not plugged in, tether taped to headbar) ---
exp3 = celldatabase.Experiment(subject, '2021-05-29', 'left_AudStr', info=['TT1ant', 'soundRight', 'A4x2-tet'])
experiments.append(exp3)

# Used right speaker; laser (520 nm) at 5mW; Probe DD02, no dye; Rig 2
# same laser calibration as exp2

# Probe in at: 13:52
# tried to go in same general area as exp2 (probe AP, medial edge of craniotomy)

exp3.add_site(3200, tetrodes=[1,2,5,6]) # TT3 ref
exp3.add_session('13-56-43', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-59-17', 'm', 'tuningTest', 'am_tuning_curve')
# no sound response

exp3.add_site(3400, tetrodes=[1,2,4,5,6]) # TT3 ref
exp3.add_session('14-11-39', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-14-20', 'n', 'tuningTest', 'am_tuning_curve')
# no sound response

exp3.add_site(3600, tetrodes=[1,2,3,4,6]) # TT5 reference
exp3.add_session('14-25-51', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-28-23', 'o', 'tuningTest', 'am_tuning_curve')
# no sound response

exp3.add_site(3800, tetrodes=[1,2,3,4,6]) # TT5 reference
exp3.add_session('14-38-32', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('14-41-02', 'p', 'tuningTest', 'am_tuning_curve')
exp3.add_session('14-45-07', 'q', 'laserAM', 'am_tuning_curve')
exp3.add_session('15-01-18', 'r', 'laser', 'am_tuning_curve')
exp3.add_session('15-10-33', 's', 'laserTuningCurve', 'am_tuning_curve')

exp3.maxDepth = 3800


exp4 = celldatabase.Experiment(subject, '2021-05-30', 'left_AudStr', info=['medialDiI', 'TT1ant', 'soundRight', 'A4x2-tet'])
experiments.append(exp4)

# Used right speaker; laser (520 nm) at 5mW; Probe DD02, DiI used; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
1.0: 4.05, 22.5
2.0: 5.3, 41.5
3.0: 6.55, 61.2
4.0: 7.75, 80.1
5.0: 9.0, 100.2
"""

# Animal in rig at: 9:16
# Probe in at: 9:33

# probe oriented along AP axis, inserted on medial side of craniotomy
# doing 160 trials of test tuning curve (10 trials per cond) to speed it up
# adding 'laser' sessions consisting of 200 trials, 50/50 with 500 ms laser

exp4.add_site(3000, tetrodes=[2,4]) # TT3 ref
exp4.add_session('09-35-25', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('09-38-02', 'a', 'tuningTest', 'am_tuning_curve')
# no sound response

exp4.add_site(3200, tetrodes=[2,4,5,6]) # TT3 ref
exp4.add_session('09-46-05', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('09-48-36', 'b', 'tuningTest', 'am_tuning_curve')
exp4.add_session('09-52-35', 'c', 'laserAM', 'am_tuning_curve')
exp4.add_session('10-08-29', 'd', 'laser', 'am_tuning_curve')

exp4.add_site(3400, tetrodes=[1,2,4,6]) # TT5 ref
exp4.add_session('10-28-39', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('10-31-16', 'e', 'tuningTest', 'am_tuning_curve')
exp4.add_session('10-36-53', 'f', 'laserAM', 'am_tuning_curve')
exp4.add_session('10-52-45', 'g', 'laser', 'am_tuning_curve')

exp4.add_site(3600, tetrodes=[1,2,4,5,6]) # TT3 reference
exp4.add_session('11-07-34', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('11-10-06', 'h', 'tuningTest', 'am_tuning_curve')
exp4.add_session('11-15-03', 'i', 'laserAM', 'am_tuning_curve')
exp4.add_session('11-31-05', 'j', 'laser', 'am_tuning_curve')
exp4.add_session('11-40-07', 'k', 'laserTuningCurve', 'am_tuning_curve')

exp4.add_site(3700, tetrodes=[1,2,4,5,6])
exp4.add_session('12-14-36', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-17-11', 'l', 'tuningTest', 'am_tuning_curve')
# no sound response

exp4.add_site(3800, tetrodes=[1,2,3,4])
exp4.add_session('12-26-55', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-29-26', 'm', 'tuningTest', 'am_tuning_curve')
# no sound response

# doing a site on the way out
exp4.add_site(3500, tetrodes=[1,2,3,4,6]) # TT5 reference
exp4.add_session('12-39-40', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('12-42-21', 'n', 'tuningTest', 'am_tuning_curve')
# no sound response

exp4.maxDepth = 3800


exp5 = celldatabase.Experiment(subject, '2021-06-01', 'left_AudStr', info=['middleDiD', 'TT1ant', 'soundRight', 'A4x2-tet'])
experiments.append(exp5)

# Used right speaker; laser (520 nm) at 5mW; Probe DD02, DiD used; Rig 2

"""
Laser Calibration
Power: Value on laser dial, value in output level
1.0: 3.85, 19.3
2.0: 5.05, 37.3
3.0: 6.19, 54.9
4.0: 7.26, 72.0
5.0: 8.32, 88.7
"""

# Animal in rig at: 12:57
# Probe in at: 13:17

# probe oriented along AP axis, inserted on medial side of craniotomy
# doing 160 trials of test tuning curve (10 trials per cond) to speed it up
# adding 'laser' sessions consisting of 200 trials, 50/50 with 500 ms laser

exp5.add_site(3200, tetrodes=[1,2,5,6]) # TT3 reference
exp5.add_session('13-24-34', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('13-27-13', 'a', 'tuningTest', 'am_tuning_curve')
exp5.add_session('13-31-35', 'b', 'laserAM', 'am_tuning_curve')
exp5.add_session('13-47-33', 'c', 'laser', 'am_tuning_curve')

exp5.add_site(3400, tetrodes=[1,2,4,5,6])
exp5.add_session('14-09-01', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-12-15', 'd', 'tuningTest', 'am_tuning_curve')

exp5.add_site(3600, tetrodes=[1,2,4,5,6])
exp5.add_session('14-27-01', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-30-04', 'e', 'tuningTest', 'am_tuning_curve')

exp5.add_site(3700, tetrodes=[1,2,3,4,6]) # TT5 reference
exp5.add_session('14-39-38', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-42-07', 'f', 'tuningTest', 'am_tuning_curve')

exp5.add_site(3300, tetrodes=[1,2,4])
exp5.add_session('14-53-37', None, 'noisebursts', 'am_tuning_curve')
exp5.add_session('14-59-29', 'g', 'tuningTest', 'am_tuning_curve')

exp5.maxDepth = 3700
