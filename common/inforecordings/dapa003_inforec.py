from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'dapa003'
experiments=[]


exp0 = celldatabase.Experiment(subject, '2017-08-25', 'right_AudStr', info='midAnteriorfacingAnterior')
experiments.append(exp0)

exp0.add_site(2050, tetrodes=[1,2,3,4,5,6])
exp0.add_session('15-44-34', None, 'noisebursts', 'am_tuning_curve')


exp0.add_site(2100, tetrodes=[1,2,3,4,5,6])
exp0.add_session('16-37-38', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('16-41-14', 'a', 'tuningCurve', 'am_tuning_curve')

exp0.add_site(2150, tetrodes=[1,2,3,4,5,6])
exp0.add_session('17-04-14', None, 'noisebursts', 'am_tuning_curve') #channel 7 (weird, high activity - looks like broken probes) included with this and previous sessions
exp0.add_session('17-08-41', None, 'noisebursts', 'am_tuning_curve') #channel 7 excluded
exp0.add_session('17-20-51', None, 'tuningCurve', 'am_tuning_curve') #Forgot to save behavior

exp0.add_site(2275, tetrodes=[1,2,3,4,5,6])
exp0.add_session('18-02-39', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('18-05-15', None, 'tuningCurve', 'am_tuning_curve') #Forgot to save behavior

exp0.add_site(2350, tetrodes=[1,2,3,4,5,6])
exp0.add_session('18-41-50', None, 'noisebursts', 'am_tuning_curve')
exp0.add_session('18-44-59', 'b', 'tuningCurve', 'am_tuning_curve')

