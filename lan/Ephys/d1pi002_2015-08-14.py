from jaratoolbox.test.nick.database import cellDB
reload(cellDB)
from jaratoolbox.test.nick.database import sitefuncs
reload(sitefuncs)

sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse'}
 
exp0814 = cellDB.Experiment(animalName = 'd1pi002', date = '2015-08-14', experimenter = 'lan', defaultParadigm='laser_tuning_curve')

#First penetration
'''
site1 = exp0814.add_site(depth = 2000, tetrodes = [6]) #cortical laser response?
site1.add_session('13-40-57', None, sessionTypes['lp']) #comment ='power=2mW'
site1.add_session('13-49-20', None, sessionTypes['lt'])  #comment ='power=2mW'
site1.add_session('13-52-45', None, sessionTypes['nb']) #no response

sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0, 1, 2], mainTCind= None)
'''

site2 = exp0814.add_site(depth = 3500, tetrodes = [3,6]) #TT6 long-lasting laser inhibition; TT3 sound-inhibited?
site2.add_session('14-52-30', None, sessionTypes['lp'])
site2.add_session('14-55-22', 'a', sessionTypes['tc'])
site2.add_session('15-20-21', None, sessionTypes['nb'])
site2.add_session('15-22-40', None, sessionTypes['lp'])
site2.add_session('15-25-19', None, sessionTypes['lt']) 
sitefuncs.nick_lan_daily_report(site2, 'site2', mainRasterInds=[0, 2, 3, 4], mainTCind = 1)
#bData has 962 trials while eventOnsetTimes has 963, probably ended ephys recording 1 trial after ending behavior paradigm.

'''
site3 = exp0814.add_site(depth = 3650, tetrodes = [3,4,6])
site3.add_session('15-33-44', None, sessionTypes['lp'])  #2mW
site3.add_session('15-36-07', None, sessionTypes['lt']) #2mW
site3.add_session('15-39-21', None, sessionTypes['nb']) #amp=0.4
site3.add_session('15-42-36', 'b', sessionTypes['tc'])
site3.add_session('16-03-25', None, sessionTypes['nb']) #amp=0.3
site3.add_session('16-05-20', None, sessionTypes['lp']) #3mW
sitefuncs.nick_lan_daily_report(site3, 'site3', mainRasterInds=[1,2,5], mainTCind=3)
#bData has 999 trials while len(eventOnsetTimes)=996

#Second penetration
site4 = exp0814.add_site(depth = 2700, tetrodes = [6])
site4.add_session('17-46-21', None, sessionTypes['lt'])
site4.add_session('17-48-23', None, sessionTypes['lp'])
site4.add_session('17-50-46', None, sessionTypes['nb'])
site4.add_session('18-00-04', None, sessionTypes['lp'])
#another nb here? amp=0.5
sitefuncs.nick_lan_daily_report(site4, 'site4', mainRasterInds=[0,1,2,3], mainTCind= None)
'''
'''
site5 = exp0814.add_site(depth = 3400, tetrodes = [3, 6])
site5.add_session('19-09-31', None, sessionTypes['nb'])
site5.add_session('19-12-43', None, sessionTypes['lt'])
site5.add_session('19-16-30', None, sessionTypes['lp'])
site5.add_session('19-19-49', None, sessionTypes['nb'])
site5.add_session('19-23-04', 'd', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site5, 'site5', mainRasterInds=[1,2,3], mainTCind=4) 

#Encountered issue when plotting TC,
#len(eventOnsetTimes)=972; but have 977 behav trials.
'''
#cluster5 = site3.add_cluster(clusterNumber=5, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
#cluster4 = site3.add_cluster(clusterNumber=4, tetrode=6, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')





