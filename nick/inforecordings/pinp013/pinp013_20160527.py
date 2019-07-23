
from jaratoolbox.test.nick.database import cellDB
rec = cellDB.Experiment('pinp013', '2016-05-27', 'nick', 'am_tuning_curve')

site1 = rec.add_site(depth = 691, tetrodes = [1,2,3,4,5,6,7,8])
site1.add_session('13-39-19', None, 'Noiseburst')

#I am splitting this site into 2 and clustering each
# site1a = rec.add_site(depth = 691, tetrodes = [1,2,3,4,5,6,7,8])
# site1a.add_session('13-37-12', None, 'NoStim_lowThresh')
# site1a.add_session('13-45-36', None, 'NoStim_highThresh') #Only spikes on TT3 and 4

site1a = rec.add_site(depth = 691, tetrodes = [3,4])
site1a.add_session('13-37-12', None, 'NoStim_lowThresh')
sitefuncs.cluster_site(site1a, 'site1a_lowThresh', 3)
sitefuncs.cluster_site(site1a, 'site1a_lowThresh', 4)

site1b = rec.add_site(depth = 691, tetrodes = [3,4])
site1b.add_session('13-45-36', None, 'NoStim_highThresh') #Only spikes on TT3 and 4
sitefuncs.cluster_site(site1b, 'site1b_highThresh', 3)
sitefuncs.cluster_site(site1b, 'site1b_highThresh', 4)

site2 = rec.add_site(depth = 1585, tetrodes = [1,2,3,4,5,6,7,8])
site2.add_session('13-54-37', None, 'Noiseburst') #Thresholds at 73

site3 = rec.add_site(depth = 2506, tetrodes = [1,2,3,4,5,6,7,8])
site3.add_session('14-01-12', None, 'Noiseburst') #Thresholds at 72

# site4 = rec.add_site(depth = 3204, tetrodes = [1,2,3,4,5,6,7,8])
site4 = rec.add_site(depth = 3204, tetrodes = [6,7,8]) #DEBUG
site4.add_session('14-08-54', None, 'Noiseburst') #I set the thresholds manually for each channel.
site4.add_session('14-13-26', 'a', 'TuningCurve')
site4.add_session('14-26-37', 'b', 'AM')
sitefuncs.nick_lan_daily_report(site4, 'site4', mainRasterInds=[0], mainTCind=1)
sitefuncs.am_mod_report(site4, 'site4', amSessionInd=2)

site5 = rec.add_site(depth = 3303, tetrodes = [1,2,3,4,5,6,7,8])
site5.add_session('14-52-13', None, 'Noiseburst') #I set the thresholds manually for each channel.
site5.add_session('14-54-52', 'c', 'TuningCurve')
site5.add_session('15-10-12', 'd', 'AM')
sitefuncs.nick_lan_daily_report(site5, 'site5', mainRasterInds=[0], mainTCind=1)
sitefuncs.am_mod_report(site5, 'site5', amSessionInd=2)

site6 = rec.add_site(depth = 3402, tetrodes = [1,2,3,4,5,6,7,8])
site6.add_session('15-40-19', None, 'Noiseburst') #I set the thresholds manually for each channel.
site6.add_session('15-44-29', 'e', 'TuningCurve')
site6.add_session('15-55-47', 'f', 'AM')
sitefuncs.nick_lan_daily_report(site6, 'site6', mainRasterInds=[0], mainTCind=1)
sitefuncs.am_mod_report(site6, 'site6', amSessionInd=2)

site7 = rec.add_site(depth = 3505, tetrodes = [1,2,3,4,5,6,7,8])
site7.add_session('16-23-34', None, 'Noiseburst') #I set the thresholds manually for each channel.
site7.add_session('16-26-53', 'g', 'TuningCurve')
site7.add_session('16-42-10', 'h', 'AM')
sitefuncs.nick_lan_daily_report(site7, 'site7', mainRasterInds=[0], mainTCind=1)
sitefuncs.am_mod_report(site7, 'site7', amSessionInd=2)

site8 = rec.add_site(depth = 3505, tetrodes = [1,2,3,4,5,6,7,8])
site8.add_session('17-01-48', None, 'Noiseburst')
site8.add_session('17-08-23', 'i', 'TuningCurve') #All thresholds set at 107uV
site8.add_session('17-19-39', 'j', 'AM') #All thresholds set at 107uV
sitefuncs.nick_lan_daily_report(site8, 'site8', mainRasterInds=[0], mainTCind=1)
sitefuncs.am_mod_report(site8, 'site8', amSessionInd=2)
