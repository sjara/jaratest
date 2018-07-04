from jaratoolbox import celldatabase
reload(celldatabase)

subject = 'd1pi026'
experiments=[]

exp0 = celldatabase.Experiment(subject, '2018-07-03', 'right_AudStr', info=['FacingPosterior', 'Anterior'])
experiments.append(exp0)
#Used left speaker; 2.5 mW for laser; probe DAF8
#
# exp0.laserCalibration = {
#     '0.5':1.45,
#     '1.0':2.75,
#     '1.5':4.4,
#     '2.0':6.1,
#     '2.5':7.5,
#     '3.0':10.05,
#     #'3.5':3.0,
#     #'4.0':3.6
# }

#Tetrode 4 has reference; threshold set to 55mV
exp0.add_site(2073, tetrodes=[3,4,6,7,8])
exp0.add_session('12-10-39', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(2180, tetrodes=[3,8])
exp0.add_session('12-19-13', None, 'noisebursts', 'am_tuning_curve')

exp0.add_site(2502, tetrodes=[3,8])
exp0.add_session('12-19-13', None, 'noisebursts', 'am_tuning_curve')

exp0.maxDepth = 2502
