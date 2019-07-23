from jaratoolbox.test.nick.database import cellDB
rec = cellDB.Experiment('pinp013', '2016-05-25', '', 'am_tuning_curve')

site1 = rec.add_site(depth = 3011, tetrodes = [1,2,3,4,5,6,7,8])
site1.add_session('14-32-32', None, 'Noiseburst')
site1.add_session('14-37-43', None, 'NoiseburstRefT8')
site1.add_session('14-41-52', 'a', 'TuningCurve')
site1.add_session('14-56-38', 'b', 'AM')

site2 = rec.add_site(depth = 3011, tetrodes = [1,2,3,4,5,6,7,8])
site2.add_session('15-18-46', None, 'Noiseburst')
site2.add_session('15-22-29', 'c', 'TuningCurve')
site2.add_session('15-35-27', 'd', 'AM')

site3 = rec.add_site(depth = 3300, tetrodes = [1,2,3,4,5,6,7,8])
site3.add_session('15-56-32', None, 'Noiseburst') #Sweet offset responses
site3.add_session('16-02-29', None, 'Noiseburst_again') #after resting more time .
site3.add_session('16-04-59', 'e', 'TuningCurve') 
site3.add_session('16-21-45', 'f', 'AM') 

from jaratoolbox.test.nick.database import sitefuncs

sitefuncs.nick_lan_daily_report(site1, 'site1_PCA_Report', mainRasterInds = [0, 1], mainTCind=2)
sitefuncs.nick_lan_daily_report(site2, 'site2_PCA_Report', mainRasterInds = [0], mainTCind=1)
sitefuncs.nick_lan_daily_report(site3, 'site3_PCA_Report', mainRasterInds = [0, 1], mainTCind=2)

for tetrode in site1.tetrodes:
    sitefuncs.cluster_site_PCA(site1, 'site1_PCA', tetrode)
