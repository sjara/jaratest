from jaratoolbox import celldatabase as cellDB
subject = 'adap005'
experiments = []

exp1214 = cellDB.Experiment(subject, date ='2015-12-14', brainarea='rightAStr', info='') 
experiments.append(exp1214)
site1 = exp1214.add_site(depth=2260, tetrodes=[1,3,7]) 
site1.add_session('15-51-40', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
site1.add_session('15-55-38', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('16-01-03', 'b', 'tc', 'laser_tuning_curve') #5.4,6.6,8.1kHz chords, 50dB
site1.add_session('16-05-18', None, 'noiseburst', 'laser_tuning_curve') #amp=0.2
site1.add_session('16-08-53', 'c', 'tc', 'laser_tuning_curve') #6.2&9.9kHz chords, 50dB
site1.add_session('16-13-08', 'd', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('16-23-21', 'a', 'behavior', paradigm='2afc')

exp1215 = cellDB.Experiment(subject, date ='2015-12-15', brainarea='rightAStr', info='') 
experiments.append(exp1215)
site1 = exp1215.add_site(depth=2260, tetrodes=[1,2,3,4,5,6,7,8]) 
site1.add_session('13-30-00', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
site1.add_session('13-33-21', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('13-55-21', 'c', 'tc', 'laser_tuning_curve') #4.4to9.9kHz, 5 freqs chords, 50dB
site1.add_session('14-02-08', 'a', 'behavior', paradigm='2afc')
#site2 = exp1215.add_site(depth=2260, tetrodes=[1,2,3,4,5,6,7,8]) #these recordings were done at site1 but removed ref channel
#site2.add_session('13-39-33', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
#site2.add_session('13-43-22', 'b', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB

exp1216 = cellDB.Experiment(subject, date ='2015-12-16', brainarea='rightAStr', info='') 
experiments.append(exp1216)
site1 = exp1216.add_site(depth=2420, tetrodes=[1,2,3,4,5,6,7,8]) 
site1.add_session('15-46-32', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
site1.add_session('15-49-43', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('16-00-15', 'b', 'tc', 'laser_tuning_curve') #6.6to9.9kHz,50dB
site1.add_session('16-10-19', 'c', 'tc', 'laser_tuning_curve') #18to22kHz,50dB
site1.add_session('16-15-56', 'a', 'behavior', paradigm='2afc')

exp1217 = cellDB.Experiment(subject, date ='2015-12-17', brainarea='rightAStr', info='') 
experiments.append(exp1217)
site1 = exp1217.add_site(depth=2420, tetrodes=[8]) 
site1.add_session('15-02-53', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
site1.add_session('15-05-44', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('15-10-44', 'b', 'tc', 'laser_tuning_curve') #6.6to9.9kHz,50dB
site1.add_session('15-14-40', 'c', 'tc', 'laser_tuning_curve') #18to22kHz,50dB
site1.add_session('15-19-45', 'a', 'behavior', paradigm='2afc')

exp1218 = cellDB.Experiment(subject, date ='2015-12-18', brainarea='rightAStr', info='') 
experiments.append(exp1218)
site1 = exp1218.add_site(depth=2420, tetrodes=[1,2,3,4,5,6,7,8]) 
site1.add_session('13-31-21', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
site1.add_session('13-34-39', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('13-43-35', 'b', 'tc', 'laser_tuning_curve') #8to12kHz,50dB
site1.add_session('13-50-13', 'a', 'behavior', paradigm='2afc')

exp1219 = cellDB.Experiment(subject, date ='2015-12-19', brainarea='rightAStr', info='') 
experiments.append(exp1219)
site1 = exp1219.add_site(depth=2420, tetrodes=[1,2,3,4,5,6,7,8]) 
site1.add_session('17-46-45', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
site1.add_session('17-50-03', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('17-56-05', 'b', 'tc', 'laser_tuning_curve') #8to12kHz,50dB
site1.add_session('18-00-14', 'a', 'behavior', paradigm='2afc')

exp = cellDB.Experiment(subject, date ='2015-12-21', brainarea='rightAStr', info='') 
experiments.append(exp)
site1 = exp.add_site(depth=2520, tetrodes=[7,8]) 
site1.add_session('16-34-14', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
site1.add_session('16-36-48', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('16-46-41', 'b', 'tc', 'laser_tuning_curve') #6.6&12.1kHz,50dB
site1.add_session('16-50-58', 'a', 'behavior', paradigm='2afc')

exp = cellDB.Experiment(subject, date ='2015-12-22', brainarea='rightAStr', info='') 
experiments.append(exp)
site1 = exp.add_site(depth=2520, tetrodes=[1,2,3,4,5,6,7,8]) 
site1.add_session('15-02-25', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
site1.add_session('15-05-43', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('15-17-02', 'b', 'tc', 'laser_tuning_curve') #6.6&12.1kHz,50dB
site1.add_session('15-24-04', 'a', 'behavior', paradigm='2afc')

exp = cellDB.Experiment(subject, date ='2015-12-23', brainarea='rightAStr', info='') 
experiments.append(exp)
site1 = exp.add_site(depth=2520, tetrodes=[1,2,3,4,5,6,7,8]) 
site1.add_session('14-22-52', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
site1.add_session('14-26-02', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('14-36-07', 'b', 'tc', 'laser_tuning_curve') #6.6&12.1kHz,50dB
site1.add_session('14-41-00', 'a', 'behavior', paradigm='2afc')

exp = cellDB.Experiment(subject, date ='2015-12-24', brainarea='rightAStr', info='') 
experiments.append(exp)
site1 = exp.add_site(depth=2520, tetrodes=[1,2,3,4,5,6,7,8]) 
site1.add_session('14-26-05', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
site1.add_session('14-29-00', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('14-38-29', 'b', 'tc', 'laser_tuning_curve') #6.6&12.1kHz,50dB
site1.add_session('14-43-57', 'a', 'behavior', paradigm='2afc')

exp = cellDB.Experiment(subject, date ='2016-01-08', brainarea='rightAStr', info='') 
experiments.append(exp)
site1 = exp.add_site(depth=2520, tetrodes=[5,7,8]) 
site1.add_session('11-18-21', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
site1.add_session('11-21-36', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('11-30-03', 'b', 'tc', 'laser_tuning_curve') #6.6&12.1kHz,50dB
site1.add_session('11-38-00', 'a', 'behavior', paradigm='2afc')

exp = cellDB.Experiment(subject, date ='2016-01-09', brainarea='rightAStr', info='') 
experiments.append(exp)
site1 = exp.add_site(depth=2520, tetrodes=[1,2,3,4,5,6,7,8]) 
site1.add_session('14-02-54', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
site1.add_session('14-10-44', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('14-21-47', 'a', 'behavior', paradigm='2afc')

exp = cellDB.Experiment(subject, date ='2016-01-10', brainarea='rightAStr', info='') 
experiments.append(exp)
site1 = exp.add_site(depth=2520, tetrodes=[1,2,3,4,5,6,7,8]) 
site1.add_session('15-43-52', None, 'noiseburst', 'laser_tuning_curve') #amp=0.15
site1.add_session('15-48-05', 'a', 'tc', 'laser_tuning_curve') #2-40Hz chords, 50dB
site1.add_session('15-55-57', 'a', 'behavior', paradigm='2afc')

for exp in experiments:
    for site in exp.sites:
        site.clusterFolder = 'multisession_{}site1'.format(site.date)

tetrodeLengthList = [520,850,850,650,520,110,0,430] #0 is the longest tetrode, other numbers means tetrode is x um shorter than longest tetrode.
targetRangeLongestTt = (2260, 2520)
