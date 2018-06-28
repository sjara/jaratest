from jaratoolbox import celldatabase

subject = 'pinp031'
experiments = []

exp0 = celldatabase.Experiment(subject,
                               '2018-06-22',
                               brainarea='rightAC',
                               info='NBQX')

# The impedances on this older probe are not terrible, with about 1/2 of sites
# around 800-900kohms and the other 1/2 around 1.1Mohms. I am going to use it.
# 0.5 = 1.45
# 1.0 = 1.9
# 1.5 = 2.4
# 2.0 = 2.9
# 2.5 = 3.45
# 3.0 = 3.9

# Mouse on the rig for the first time at 12:20pm, giving him a few minutes to chill.
# Pipette and electrodes in the brain at 1:12pm
# Very quiet at the beginning. Waited until 1:24, now starting to see some events
# but they do not look like neurons yet. At 1470um.
# By 1:39 starting to see some spikes.
experiments.append(exp0)
exp0.add_site(1407, tetrodes=range(1, 9))
exp0.add_session('13-45-38', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('13-49-10', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(1507, tetrodes=range(1, 9))
exp0.add_session('13-58-15', None, 'laserpulse', 'am_tuning_curve')# All inhibited, moving on.

exp0.add_site(1551, tetrodes=range(1, 9))
exp0.add_session('14-09-42', None, 'laserpulse', 'am_tuning_curve')# No responses, moving on.

exp0.add_site(1606, tetrodes=range(1, 9))
exp0.add_session('14-14-43', None, 'laserpulse', 'am_tuning_curve')# All inhibited, moving on.

exp0.add_site(1657, tetrodes=range(1, 9))
exp0.add_session('14-25-02', None, 'laserpulse', 'am_tuning_curve')# All inhibited, moving on.

exp0.add_site(1704, tetrodes=range(1, 9))
# 1439 hrs - I added saline to the wells at this point, and the activity started to look strange.
# It went back to being the way it was at the beginning. Too much saline??
# I reduced the amount of saline in the well, and the signals went back to looking
# neuronal.

exp0.add_session('14-45-56', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('14-49-43', None, 'laserpulse', 'am_tuning_curve')# All inhibited, moving on.

exp0.add_site(1753, tetrodes=range(1, 9))
exp0.add_session('14-56-40', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(1806, tetrodes=range(1, 9))
exp0.add_session('15-03-53', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(1852, tetrodes=range(1, 9))
exp0.add_session('15-08-41', None, 'laserpulse', 'am_tuning_curve')

exp0.add_site(1903, tetrodes=range(1, 9))
exp0.add_session('15-27-04', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-29-11', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('15-32-13', None, 'lasertrain', 'am_tuning_curve') #Starting to get something

exp0.add_site(1951, tetrodes=range(1, 9))
exp0.add_session('15-45-57', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('15-53-07', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('15-57-09', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-00-55', None, 'lasertrain2', 'am_tuning_curve')
exp0.add_session('16-08-20', None, 'laserpulse2', 'am_tuning_curve')
exp0.add_session('16-11-11', None, 'lasertrain3', 'am_tuning_curve')

exp0.add_site(1976, tetrodes=range(1, 9))
exp0.add_session('16-16-15', None, 'lasertrain', 'am_tuning_curve')

exp0.add_site(2000, tetrodes=range(1, 9))
#exp0.add_session('16-23-35', None, 'laserpulse', 'am_tuning_curve')
#exp0.add_session('16-25-39', None, 'lasertrain', 'am_tuning_curve')
#exp0.add_session('16-29-19', None, 'laserpulse2', 'am_tuning_curve')
exp0.add_session('16-38-29', None, 'noiseburst', 'am_tuning_curve') #Starting real data collection
exp0.add_session('16-42-35', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('16-45-59', None, 'lasertrain', 'am_tuning_curve')
# I injected 45nL of 1mM NBQX at 4:50. It went smoothly.
exp0.add_session('16-54-42', None, 'noiseburst', 'am_tuning_curve')
# I had to put saline after this session
exp0.add_session('16-59-00', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-01-50', None, 'lasertrain', 'am_tuning_curve')
exp0.add_session('17-04-28', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-09-20', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-12-52', None, 'lasertrain', 'am_tuning_curve')

#Starting over
exp0.add_session('17-17-41', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('17-20-02', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('17-22-42', None, 'lasertrain', 'am_tuning_curve')
#I injected 180nL of NBQX at 5:27pm. It went slow and smooth.
exp0.add_session('17-32-05', None, 'noiseburst', 'am_tuning_curve') #No effect of the drug.
#I INjected 180nL of NBQX at 5:35pm.
exp0.add_session('17-40-54', None, 'noiseburst', 'am_tuning_curve')
#I added another 90nL of NBQX at 5:44pm
exp0.add_session('17-49-43', None, 'noiseburst', 'am_tuning_curve')
#I Added another 90nL of NBQX at 5:51pm
exp0.add_session('17-55-06', None, 'noiseburst', 'am_tuning_curve')
exp0.add_session('18-00-48', None, 'noiseburst', 'am_tuning_curve') #Wait 10 mins
exp0.add_session('18-09-55', None, 'noiseburst', 'am_tuning_curve') #Wait 10 mins
exp0.add_session('18-20-31', None, 'noiseburst', 'am_tuning_curve') #Wait 10 mins
# I added saline at 6:25
exp0.add_session('18-30-54', None, 'noiseburst', 'am_tuning_curve') #Wait 10 mins
exp0.add_session('18-41-39', None, 'noiseburst', 'am_tuning_curve') #Wait 10 mins

exp0.add_session('18-49-16', None, 'noiseburst', 'am_tuning_curve') #Done waiting...
exp0.add_session('18-51-49', None, 'laserpulse', 'am_tuning_curve')
exp0.add_session('18-55-28', None, 'lasertrain', 'am_tuning_curve')
#Done for the day

exp1 = celldatabase.Experiment(subject,
                               '2018-06-23',
                               brainarea='rightAC',
                               info='NBQX')
#Probes and pipette are in the brain at 5:57pm
experiments.append(exp1)
exp1.add_site(1702, tetrodes=range(1, 9))
exp1.add_session('18-25-37', None, 'laserpulse', 'am_tuning_curve')

exp1.add_site(1800, tetrodes=range(1, 9))
exp1.add_session('18-39-57', None, 'laserpulse', 'am_tuning_curve')

exp1.add_site(1850, tetrodes=range(1, 9))
exp1.add_session('18-47-51', None, 'laserpulse', 'am_tuning_curve')

exp1.add_site(1901, tetrodes=range(1, 9))
exp1.add_session('19-02-14', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('19-05-21', None, 'lasertrain', 'am_tuning_curve')
exp1.add_session('19-09-45', None, 'noiseburst', 'am_tuning_curve') #This is a good site.
# Adding saline to the brain surface at 1910hrs and waiting for stability.
# 1932 hrs, done waiting. I am going to start collecting the data now.

exp1.add_session('19-35-05', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('19-37-22', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('19-40-22', None, 'lasertrain', 'am_tuning_curve')
# Injected 180nL of 1mM NBQX at 1944hrs.
exp1.add_session('19-50-01', None, 'noiseburst', 'am_tuning_curve')
# injected 180nL of 1mM NBQX at 1952hrs
exp1.add_session('19-58-35', None, 'noiseburst', 'am_tuning_curve')
#2005hrs Added 180nL NBQX, then moved the pipette a small amount forward
#with the coarse adjust (not sure the fine adjust does anything) and added another 90nL.
exp1.add_session('20-13-00', None, 'noiseburst', 'am_tuning_curve')# Responses noticibly weaker
exp1.add_session('20-17-04', None, 'laserpulse', 'am_tuning_curve') #Still have responses
exp1.add_session('20-19-20', None, 'lasertrain', 'am_tuning_curve')

# 2023hrs - pushed the pipette a little farther with the coarse adjust,
# The added the rest of the NBQX - about 180nL.
exp1.add_session('20-29-12', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('20-37-25', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('20-43-23', None, 'noiseburst', 'am_tuning_curve')

#2050hrs - removed the pipette and filled it with 10mM NBQX. Re-inserted it and
#delivered 180nL.
exp1.add_session('20-51-50', None, 'noiseburst', 'am_tuning_curve')
#Some strange simulatneous bursts of activity across different sites, sounds neural.
exp1.add_session('20-53-29', None, 'laserpulse', 'am_tuning_curve') #I see LFP deflections and a cell on T4 that responds
exp1.add_session('20-55-41', None, 'lasertrain', 'am_tuning_curve') #Nothing.
exp1.add_session('20-53-29', None, 'laserpulse', 'am_tuning_curve') #Still the cell on T4.
#I turned the laser power up to 2.5mW
exp1.add_session('21-05-09', None, 'lasertrain', 'am_tuning_curve') #Locked responses
exp1.add_session('21-09-54', None, 'noiseburst', 'am_tuning_curve') #No Responses
exp1.add_session('21-12-24', None, 'laserpulse', 'am_tuning_curve')
# Had to add saline at 2116
exp1.add_session('21-17-35', None, 'lasertrain', 'am_tuning_curve') #Response fades in.
exp1.add_session('21-23-14', None, 'noiseburst', 'am_tuning_curve') #No Responses
exp1.add_session('21-26-10', None, 'lasertrain', 'am_tuning_curve') #Strong locked responses
exp1.add_session('21-30-45', None, 'laserpulse', 'am_tuning_curve') #Nice cell here.
exp1.add_session('21-33-22', None, 'noiseburst', 'am_tuning_curve')

#Done for the day.


# Mouse on the rig at 1508hrs
# Probes and pipette in the brain at 1400um, 1529hrs
exp1 = celldatabase.Experiment(subject,
                               '2018-06-25',
                               brainarea='rightAC',
                               info='NBQX')

experiments.append(exp1)
exp1.add_site(1400, tetrodes=[1, 2, 3, 4, 5, 7])
exp1.add_session('15-32-26', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('15-35-34', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('15-37-18', None, 'lasertrain', 'am_tuning_curve')
#This is a good site, waiting 20 mins
exp1.add_session('15-59-24', None, 'noiseburst', 'am_tuning_curve') #100 trials
exp1.add_session('16-01-41', None, 'laserpulse', 'am_tuning_curve') #100 trials
exp1.add_session('16-03-48', None, 'lasertrain', 'am_tuning_curve') #100 trials
#Injected 180nl of 10mM NBQX at 1609hrs
exp1.add_session('16-08-09', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-12-19', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-13-45', None, 'noiseburst', 'am_tuning_curve')

exp1.add_session('16-15-43', None, 'noiseburst', 'am_tuning_curve')#Real data time
exp1.add_session('16-17-57', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('16-20-08', None, 'lasertrain', 'am_tuning_curve')

exp1.add_session('16-24-13', None, 'noiseburst', 'am_tuning_curve') #Noise responses coming back
exp1.add_session('16-27-56', None, 'laserpulse', 'am_tuning_curve') #Looks totally different
exp1.add_session('16-30-51', None, 'lasertrain', 'am_tuning_curve')

exp1.add_session('16-34-47', None, 'noiseburst', 'am_tuning_curve') #Reliable 100msec latency responses
exp1.add_session('16-44-58', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('16-47-53', None, 'laserpulse', 'am_tuning_curve') #Responses are back??
exp1.add_session('16-50-42', None, 'lasertrain', 'am_tuning_curve')

#Big injection PRE
exp1.add_session('17-30-53', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('17-34-03', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('17-36-36', None, 'lasertrain', 'am_tuning_curve')
#Finished injecting 360nL 10mM NBQX at 1742hrs - injection went very slow (like there was a clog)

exp1.add_session('17-45-14', None, 'noiseburst', 'am_tuning_curve') #50 trials
exp1.add_session('17-46-41', None, 'laserpulse', 'am_tuning_curve') #100 trials
exp1.add_session('17-49-07', None, 'lasertrain', 'am_tuning_curve') #100 trials
exp1.add_session('17-52-53', None, 'noiseburst', 'am_tuning_curve') #100 trials
exp1.add_session('17-56-56', None, 'lasertrain', 'am_tuning_curve') #100 trials

exp1.add_session('18-05-36', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('18-19-30', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('18-38-25', None, 'noiseburst', 'am_tuning_curve')
exp1.add_session('18-56-13', None, 'noiseburst', 'am_tuning_curve')

#Removed the pipette, put a new one with saline, and re-inserted it at 1906hrs
exp1.add_session('19-14-41', None, 'noiseburst', 'am_tuning_curve')

exp1.add_session('19-19-47', None, 'noiseburst', 'am_tuning_curve')#100 trials
exp1.add_session('19-22-39', None, 'laserpulse', 'am_tuning_curve')
exp1.add_session('19-24-53', None, 'lasertrain', 'am_tuning_curve')
# Added 360nL saline at 1929hrs

exp1.add_session('19-32-37', None, 'noiseburst', 'am_tuning_curve')#100 trials
exp1.add_session('19-35-15', None, 'laserpulse', 'am_tuning_curve')#100 trials
exp1.add_session('19-37-54', None, 'lasertrain', 'am_tuning_curve')#100 trials

exp1.add_session('19-47-36', None, 'noiseburst', 'am_tuning_curve')#100 trials


#1506 Just put the pipette with 10mM NBQX
exp3 = celldatabase.Experiment(subject,
                               '2018-06-26',
                               brainarea='rightAC',
                               info='NBQX')
experiments.append(exp3)
exp3.add_site(1400, tetrodes=[1, 2, 3, 4, 5, 6, 7, 8])
exp3.add_session('15-34-48', None, 'noiseburst', 'am_tuning_curve')

exp3.add_site(1551, tetrodes=[1, 2, 3, 4, 5, 6, 7, 8])
exp3.add_session('15-43-38', None, 'noiseburst', 'am_tuning_curve')

exp3.add_site(1803, tetrodes=[1, 2, 3, 4, 5, 6, 7, 8])
exp3.add_session('15-56-22', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('15-59-47', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('16-01-18', None, 'lasertrain', 'am_tuning_curve')
# Looks like a good site, I'm going to wait for 20 mins starting at 1604hrs

exp3.add_session('16-27-28', None, 'noiseburst', 'am_tuning_curve') # testing
# Several electrodes started to be extremely noisy. I restarted the recording software,
# which fixed the problem.
exp3.add_session('16-40-06', None, 'noiseburst', 'am_tuning_curve') # 100 trials
exp3.add_session('16-42-47', None, 'laserpulse', 'am_tuning_curve') # 100 trials
# I lost almost everything I was recording. I'm not sure what happened

exp3.add_session('16-46-13', None, 'laserpulse', 'am_tuning_curve') # 100 trials
#Now things are coming back
exp3.add_session('16-49-14', None, 'noiseburst', 'am_tuning_curve') # 100 trials
exp3.add_session('16-51-31', None, 'lasertrain', 'am_tuning_curve') # 100 trials
exp3.add_session('16-57-24', None, 'noiseburst', 'am_tuning_curve') # 100 trials
#Had to change reference, collecing again

exp3.add_session('17-05-01', None, 'noiseburst', 'am_tuning_curve') # 100 trials
exp3.add_session('17-07-37', None, 'laserpulse', 'am_tuning_curve') # 100 trials

exp3.add_site(1901, tetrodes=[1, 2, 3, 4, 5, 6, 7, 8])
exp3.add_session('17-27-08', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('17-29-36', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('17-31-58', None, 'lasertrain', 'am_tuning_curve')
#Finished injecting 180nL 10mM NBQX at 1741hrs. The injection took a very long time and was
# slow and steady. At the end, I dropped the syringe and the tube probably pulled on the pipette.
exp3.add_session('17-42-13', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('17-44-24', None, 'laserpulse', 'am_tuning_curve')
exp3.add_session('17-46-50', None, 'lasertrain', 'am_tuning_curve')
exp3.add_session('17-50-35', None, 'laserpulse', 'am_tuning_curve')
# The responses are gone. I am going to wait to see if I get the cells back at all.
exp3.add_session('17-56-32', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('18-03-53', None, 'noiseburst', 'am_tuning_curve')
exp3.add_session('18-11-03', None, 'noiseburst', 'am_tuning_curve') #Responses are coming back, we can see if our cells are still here.


# New experiment, Mouse on the rig chilling out from 1555hrs.
# Pipette with 10mM NBQX inserted along with probe at 1611hrs.
exp4 = celldatabase.Experiment(subject,
                               '2018-06-27',
                               brainarea='rightAC',
                               info='NBQX')
experiments.append(exp4)
exp4.add_site(1436, tetrodes=[1, 2, 3, 4, 5, 6, 7, 8])
exp4.add_session('16-25-59', None, 'noiseburst', 'am_tuning_curve')

exp4.add_site(1604, tetrodes=[1, 2, 3, 4, 5, 6, 7, 8])
exp4.add_session('16-39-09', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('16-46-46', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('16-48-33', None, 'lasertrain', 'am_tuning_curve')

exp4.add_session('17-00-22', None, 'noiseburst_pre', 'am_tuning_curve')
exp4.add_session('17-02-43', None, 'laserpulse_pre', 'am_tuning_curve')
exp4.add_session('17-05-14', None, 'lasertrain_pre', 'am_tuning_curve')
#180nL 10mM NBQX injected at 1709hrs
exp4.add_session('17-10-39', None, 'noiseburst', 'am_tuning_curve')

exp4.add_session('17-12-13', None, 'noiseburst_post', 'am_tuning_curve')
exp4.add_session('17-15-18', None, 'laserpulse_post', 'am_tuning_curve')
exp4.add_session('17-17-27', None, 'lasertrain_post', 'am_tuning_curve')

exp4.add_session('17-43-22', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('17-53-10', None, 'noiseburst', 'am_tuning_curve')
exp4.add_session('17-55-50', None, 'laserpulse', 'am_tuning_curve')
exp4.add_session('17-58-34', None, 'lasertrain', 'am_tuning_curve')

exp4.add_site(1879, tetrodes=[1, 2, 3, 4, 5, 6, 7, 8])
exp4.add_session('18-50-57', None, 'noiseburst', 'am_tuning_curve') #100 trials
exp4.add_session('18-53-13', None, 'laserpulse', 'am_tuning_curve') #100 trials
exp4.add_session('18-56-10', None, 'lasertrain', 'am_tuning_curve') #100 trials
# The pipette was clogged, so I had to remove and change it. I am filling the new pipette with new 10mM NBQX

exp4.add_session('19-16-41', None, 'noiseburst_pre', 'am_tuning_curve') #100 trials
exp4.add_session('19-19-29', None, 'laserpulse_pre', 'am_tuning_curve') #100 trials
exp4.add_session('19-22-28', None, 'lasertrain_pre', 'am_tuning_curve') #100 trials
#Infused 180nL 10mM NBQX
exp4.add_session('19-27-16', None, 'noiseburst_post', 'am_tuning_curve') #100 trials
exp4.add_session('19-30-40', None, 'laserpulse_post', 'am_tuning_curve') #100 trials
exp4.add_session('19-33-54', None, 'lasertrain_post', 'am_tuning_curve') #100 trials

exp4.add_session('19-47-12', None, 'noiseburst', 'am_tuning_curve') #100 trials
exp4.add_session('20-01-49', None, 'noiseburst', 'am_tuning_curve') #100 trials
exp4.add_session('20-17-18', None, 'noiseburst', 'am_tuning_curve') #100 trials
