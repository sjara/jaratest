from jaratoolbox import celldatabase

subject = 'band022'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2017-03-02', brainarea='right_thalamus', info='lateralDiI')
experiments.append(exp0)

#crazy hippocampus lfp cleared up, now lots of spikes on TT2 while others quiet.
# exp0.add_site(3010, tetrodes = [2])
# exp0.add_session('11-42-47', None, 'noisebursts', 'am_tuning_curve')
#
# exp0.add_site(3425, tetrodes = [4])
# exp0.add_session('12-03-42', None, 'noisebursts', 'am_tuning_curve')

exp1 = celldatabase.Experiment(subject, '2017-03-17', brainarea='right_thalamus', info=['anteriorDiI','sitesAnt','sound_left'])
experiments.append(exp1)

exp1.add_site(3204, tetrodes = [1,3,5,6,7])
exp1.add_session('11-28-33', None, 'noisebursts', 'am_tuning_curve') #sound responses on all tetrodes!
exp1.add_session('11-36-36', 'a', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('11-49-48', 'b', 'AM', 'am_tuning_curve')
exp1.add_session('11-58-07', 'c', 'bandwidth', 'bandwidth_am') #6kHz for TT1,3
exp1.add_session('12-17-27', 'd', 'bandwidth', 'bandwidth_am') #14kHz for TT5,7

exp1.add_site(3301, tetrodes = [2,3,5,7,8])
exp1.add_session('12-41-16', None, 'noisebursts', 'am_tuning_curve') #all sound responsive
exp1.add_session('12-43-29', 'e', 'tuningCurve', 'am_tuning_curve')
exp1.add_session('12-54-44', 'f', 'AM', 'am_tuning_curve')
exp1.add_session('13-01-53', 'g', 'bandwidth', 'bandwidth_am') #6.5kHz for TT3
exp1.add_session('13-21-00', 'h', 'noiseAmps', 'am_tuning_curve')

# exp1.add_site(3395, tetrodes = [1,2,3,5,6,7,8])
# exp1.add_session('13-32-08', None, 'noisebursts', 'am_tuning_curve')
# exp1.add_session('13-35-28', 'i', 'tuningCurve', 'am_tuning_curve')
# exp1.add_session('13-46-10', 'j', 'AM', 'am_tuning_curve')
#nothing has good tuning, ending recording here

exp1.maxDepth = 3395


exp2 = celldatabase.Experiment(subject, '2017-03-18', brainarea='right_thalamus', info=['posteriorDiD','sitesAnt','sound_left'])
experiments.append(exp2)

exp2.add_site(3100, tetrodes = [1,2,3,4,6,7,8])
exp2.add_session('13-46-55', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('13-52-17', 'a', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-04-10', 'b', 'AM', 'am_tuning_curve')
exp2.add_session('14-11-46', 'c', 'bandwidth', 'bandwidth_am')
exp2.add_session('14-33-17', 'd', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(3205, tetrodes = [3,4,5,6,7,8])
exp2.add_session('14-40-17', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('14-44-22', 'e', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('14-57-47', 'f', 'AM', 'am_tuning_curve')
exp2.add_session('15-03-56', 'g', 'bandwidth', 'bandwidth_am')
exp2.add_session('15-26-12', 'h', 'noiseAmps', 'am_tuning_curve')

exp2.add_site(3290, tetrodes = [3,4,5,7])
exp2.add_session('15-35-24', None, 'noisebursts', 'am_tuning_curve')
exp2.add_session('15-37-57', 'i', 'tuningCurve', 'am_tuning_curve')
exp2.add_session('15-49-04', 'j', 'AM', 'am_tuning_curve')
exp2.add_session('15-55-17', 'k', 'bandwidth', 'bandwidth_am') #14 kHz for TT3,4
exp2.add_session('16-17-20', 'l', 'bandwidth', 'bandwidth_am') #5.5kHz for TT4
exp2.add_session('16-35-43', 'm', 'noiseAmps', 'am_tuning_curve')

exp2.maxDepth = 3290
