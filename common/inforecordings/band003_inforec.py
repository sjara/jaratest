from jaratoolbox import celldatabase as celldb
reload(celldb)


#band003 = celldb.InfoRecording('band003')
subject = 'band003'
experiments = []

exp0 = celldb.Experiment(subject, '2016-08-18', 'left_AC', info=['lateralDiO','TT1ant','sound_left'])
experiments.append(exp0)

exp0.add_site(830, tetrodes = [2])
exp0.add_session('11-15-19', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('11-18-21', 'a', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('11-29-17', 'b', 'AM', 'am_tuning_curve')
exp0.add_session('11-36-55', 'c', 'bandwidth', 'bandwidth_am')

exp0.add_site(880, tetrodes = [1,2,8])
exp0.add_session('11-58-29', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-00-44', 'd', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-11-58', 'e', 'AM', 'am_tuning_curve')
exp0.add_session('12-20-31', 'f', 'bandwidth', 'bandwidth_am')

exp0.add_site(940, tetrodes = [1,2,4,6,8])
exp0.add_session('12-41-41', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('12-44-25', 'g', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('12-55-49', 'h', 'AM', 'am_tuning_curve')
exp0.add_session('13-18-59', 'i', 'bandwidth', 'bandwidth_am')

exp0.add_site(1000, tetrodes = [1,2,4,6,8])
exp0.add_session('13-40-16', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('13-42-08', 'j', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('13-53-19', 'k', 'AM', 'am_tuning_curve')
exp0.add_session('14-01-19', 'l', 'bandwidth' ,'bandwidth_am')

exp0.add_site(1040, tetrodes = [1,2,4,6,8])
exp0.add_session('14-22-14', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-24-22', 'm', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('14-36-38', 'n', 'AM', 'am_tuning_curve')
exp0.add_session('14-48-21', 'o', 'bandwidth', 'bandwidth_am')

exp0.add_site(1090, tetrodes = [1,2,3,4,6,8])
exp0.add_session('15-10-26', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-12-29', 'p', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('15-23-12', 'q', 'AM', 'am_tuning_curve')
exp0.add_session('15-32-17', 'r', 'bandwidth', 'bandwidth_am')

exp0.add_site(1150, tetrodes = [1,2,4,5,6,8])
exp0.add_session('15-53-43', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('15-55-47', 's', 'tuningCurve', 'am_tuning_curve')
exp0.add_session('16-06-21', 't', 'AM', 'am_tuning_curve')
exp0.add_session('16-16-47', 'u', 'bandwidth' , 'bandwidth_am')

exp0.maxDepth = 1150


exp1 = celldb.Experiment(subject, '2016-08-19', 'left_AC', info=['centerDiI','TT1ant','sound_left'])
experiments.append(exp1)

# exp1.add_site(789, tetrodes = [2])
# exp1.add_session('08-55-09', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(841, tetrodes = [2])
exp1.add_session('08-58-19', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('09-00-25', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('09-11-22', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('09-17-44', 'c', 'bandwidth', 'bandwidth_am')

# exp1.add_site(951, tetrodes = [1,2,4])
# exp1.add_session('09-49-35', None, 'noisebursts', 'am_tuning_curve')

exp1.add_site(987, tetrodes = [1,2,4,8])
exp1.add_session('09-52-55', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('09-54-34', 'd', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('10-05-07', 'e', 'AM', 'am_tuning_curve')
exp1.add_session('10-13-48', 'f', 'bandwidth', 'bandwidth_am')

exp1.add_site(1030, tetrodes = [1,2,4,6,8])
exp1.add_session('10-42-39', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('10-45-05', 'g', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('10-55-51', 'h', 'AM', 'am_tuning_curve')
exp1.add_session('11-05-44', 'i', 'bandwidth', 'bandwidth_am')

exp1.add_site(1110, tetrodes = [2,3,4,6,7,8])
exp1.add_session('11-26-56', None, 'noisebursts', 'am_tuning_curve')
exp1.add_session('11-29-14', 'j', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('11-39-54', 'k', 'AM', 'am_tuning_curve')
exp1.add_session('11-48-58', 'l', 'bandwidth', 'bandwidth_am')

exp1.maxDepth = 1110


exp2 = celldb.Experiment(subject, '2016-08-21', 'left_AC', info=['medialDiD','TT1ant','sound_left'])
experiments.append(exp2)

# exp2.add_site(880, tetrodes = [2])
# exp2.add_session('10-34-45', None, 'noisebursts', 'am_tuning_curve')
# 
# exp2.add_site(920, tetrodes = [2])
# exp2.add_session('10-39-23', None, 'noisebursts', 'am_tuning_curve')
# 
# exp2.add_site(950, tetrodes = [2])
# exp2.add_session('10-42-46', None, 'noisebursts', 'am_tuning_curve')
# 
# exp2.add_site(1000, tetrodes = [2])
# exp2.add_session('10-48-41', None, 'noisebursts', 'am_tuning_curve')
# 
# exp2.add_site(1080, tetrodes = [2])
# exp2.add_session('10-55-55', None, 'noisebursts', 'am_tuning_curve')

exp2.add_site(1120, tetrodes = [1,2])
exp2.add_session('11-01-56', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-03-51', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('11-14-28', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('11-21-02', 'c', 'bandwidth', 'bandwidth_am')

exp2.add_site(1170, tetrodes = [1,2])
exp2.add_session('11-42-50', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('11-45-13', 'd', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('11-56-00', 'e', 'AM', 'am_tuning_curve')
exp2.add_session('12-03-46', 'f', 'bandwidth', 'bandwidth_am')

exp2.add_site(1180, tetrodes = [1,2,4])
exp2.add_session('12-25-08', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('12-27-20', 'g', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('12-37-56', 'h', 'AM', 'am_tuning_curve')
exp2.add_session('12-45-43', 'i', 'bandwidth', 'bandwidth_am')

exp2.add_site(1250, tetrodes = [1,2,4])
exp2.add_session('13-08-21', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-10-14', 'j', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('13-20-48', 'k', 'AM', 'am_tuning_curve')
exp2.add_session('13-28-39', 'l', 'bandwidth', 'bandwidth_am')

exp2.add_site(1310, tetrodes = [1,2,4])
exp2.add_session('13-51-11', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-53-00', 'm', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-03-38', 'n', 'AM', 'am_tuning_curve')
exp2.add_session('14-12-19', 'o', 'bandwidth', 'bandwidth_am')

exp2.maxDepth = 1310


exp3 = celldb.Experiment(subject, '2016-08-22', 'right_AC', info=['unknown','TT1ant','sound_left'])
experiments.append(exp3)

# exp3.add_site(720, tetrodes = [2,6])
# exp3.add_session('09-44-29', None, 'noisebursts', 'am_tuning_curve')
# 
# exp3.add_site(750, tetrodes = [2])
# exp3.add_session('09-48-33', None, 'noisebursts', 'am_tuning_curve')

exp3.add_site(874, tetrodes = [1,2,4,6])
exp3.add_session('09-58-07', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('10-00-41', 'a', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('10-11-12', 'b', 'AM', 'am_tuning_curve')
exp3.add_session('10-19-35', 'c', 'bandwidth', 'bandwidth_am')

exp3.add_site(940, tetrodes = [1,2,4,8])
exp3.add_session('10-43-05', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('10-48-20', 'd', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('10-58-54', 'e', 'AM', 'am_tuning_curve')
exp3.add_session('11-08-10', 'f', 'bandwidth', 'bandwidth_am')

exp3.add_site(1020, tetrodes = [1,2,3,4,6,8])
exp3.add_session('11-33-55', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('11-36-30', 'g', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('11-47-02', 'h', 'AM', 'am_tuning_curve')
exp3.add_session('11-56-12', 'i', 'bandwidth', 'bandwidth_am')

exp3.add_site(1060, tetrodes = [1,2,3,4,6])
exp3.add_session('12-18-10', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('12-20-21', 'j', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('12-31-11', 'k', 'AM', 'am_tuning_curve')
exp3.add_session('12-40-24', 'l', 'bandwidth', 'bandwidth_am')

exp3.add_site(1120, tetrodes = [1,2,3,4,6,8])
exp3.add_session('13-04-13', None, 'noisebursts', 'am_tuning_curve')
exp3.add_session('13-06-22', 'm', 'tuningCurve', 'am_tuning_curve')
exp3.add_session('13-17-09', 'n', 'AM', 'am_tuning_curve')
exp3.add_session('13-25-18', 'o', 'bandwidth', 'bandwidth_am')

exp3.maxDepth = 1120


exp4 = celldb.Experiment(subject, '2016-08-23', 'right_AC', info=['unknown','TT1ant','sound_left'])
experiments.append(exp4)

# exp4.add_site(820, tetrodes = [4,6])
# exp4.add_session('10-11-50', None, 'noisebursts', 'am_tuning_curve')

exp4.add_site(860, tetrodes = [4,5,6])
exp4.add_session('10-15-40', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('10-17-27', 'a', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('10-29-26', 'b', 'AM', 'am_tuning_curve')
exp4.add_session('10-37-20', 'c', 'bandwidth', 'bandwidth_am')

exp4.add_site(940, tetrodes = [4,5,6])
exp4.add_session('11-04-30', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('11-07-04', 'd', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('11-19-04', 'e', 'AM', 'am_tuning_curve')
exp4.add_session('11-27-28' ,'f', 'bandwidth', 'bandwidth_am')

exp4.add_site(1000, tetrodes = [4,5,6])
exp4.add_session('11-49-57', None, 'noisebursts', 'am_tuning_curve')
exp4.add_session('11-52-12', 'g', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('12-03-12', 'h', 'AM', 'am_tuning_curve')
exp4.add_session('12-11-32', 'i', 'bandwidth', 'bandwidth_am')

# exp4.add_site(1069, tetrodes = [2,4,5,6])
# exp4.add_session('12-42-15', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('12-44-43', 'j', 'tuningCurve', 'am_tuning_curve')
# exp4.add_session('13-09-49', 'k', 'AM', 'am_tuning_curve')

exp4.add_site(1070, tetrodes = [2,4,5,6])
exp4.add_session('13-16-42', 'l', 'AM', 'am_tuning_curve')
exp4.add_session('13-22-04', 'm', 'tuningCurve', 'am_tuning_curve')
exp4.add_session('13-38-29', 'n', 'bandwidth', 'bandwidth_am')

# exp4.add_site(1120, tetrodes = [2,3,4,5,6])
# exp4.add_session('14-02-13', None, 'noisebursts', 'am_tuning_curve')
# exp4.add_session('14-04-45', 'o', 'tuningCurve', 'am_tuning_curve')
# exp4.add_session('14-15-23', 'p', 'AM', 'am_tuning_curve')
# #exp4.add_session('14-23-41', None, 'bandwidth', 'bandwidth_am')

exp4.maxDepth = 1120


exp5 = celldb.Experiment(subject, '2016-08-24', 'right_AC', info=['unknown','TT1ant','sound_left'])
experiments.append(exp5)

# exp5.add_site(860, tetrodes = [2])
# exp5.add_session('12-08-14', None, 'noisebursts', 'am_tuning_curve')
# exp5.add_session('12-10-04', 'a', 'tuningCurve', 'am_tuning_curve')
