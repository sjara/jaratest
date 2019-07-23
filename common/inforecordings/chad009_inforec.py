from jaratoolbox import celldatabase

subject = 'chad009'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2018-10-03',
                               brainarea='rightAC',
                               info='mid')
experiments.append(exp0)

exp0.add_site(894, tetrodes=[1,2,3,4,5,6,8]) 
#tetrode 7 has reference
#exp0.add_session('13-28-05', None, 'noiseburst', 'am_tuning_curve'
#Behavior suffix 'a'

exp0.maxDepth = 894

exp1 = celldatabase.Experiment(subject,
                               '2018-10-04', 
                               brainarea='rightAC',
                               info='mid')
experiments.append(exp1)

exp1.add_site(1250, tetrodes=[1,2,3,4,8]) #tetrode 6 (channel 3) has reference
#exp1.add_site(1250, tetrodes=[2]) #Limit just to TT2 for cluster color plotting
exp1.add_session('13-49-05', None, 'noiseburst', 'am_tuning_curve') #Good sound responses on TT2
#Behavior suffix 'a'

exp1.maxDepth = 1250

exp2 = celldatabase.Experiment(subject, '2018-11-15', 'right_AC', info=['midMedial' 'facingAnterior' 'soundLeft'])
experiments.append(exp2)

exp2.add_site(1100, tetrodes=[1,2,3,4])
#exp2.add_session('12-48-25', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'a'
#Raster plot does not show clear indication of cell presence.

exp2.add_site(1150, tetrodes=[1,2,3,4,5])
#exp2.add_session('12-50-37', None, 'noiseburst', 'am_tuning_curve')
#Behavior suffix 'b'
#Raster plot does not show good indication of cell presence.
exp2.maxDepth = 1150
