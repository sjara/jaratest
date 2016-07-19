from jaratoolbox.test.nick.database import cellDB
reload(cellDB)
from jaratoolbox.test.lan.Ephys import sitefuncs_vlan as sitefuncs
reload(sitefuncs)

sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse',
                'str':'sortedTuningRaster'}
 
exp0818 = cellDB.Experiment(animalName='d1pi002', date ='2015-08-18', experimenter='lan', defaultParadigm='laser_tuning_curve')

'''
site1 = exp0818.add_site(depth = 1600, tetrodes = [3]) #cortical laser response?laser responsive, may have weak sound response?
site1.add_session('13-42-11', None, sessionTypes['lp']) #comment ='power=2mW'
site1.add_session('13-47-02', None, sessionTypes['lt'])  #comment ='power=2mW'
site1.add_session('13-50-39', None, sessionTypes['nb']) #amp=0.3
site1.add_session('13-56-45', None, sessionTypes['nb']) #amp=0.35, weak response?

sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0, 1, 2, 3], mainTCind= None, mainSTRind=None)


site2 = exp0818.add_site(depth = 2450, tetrodes = [3]) #TT3 big unit laser inhibited, no obvious sound response. merged two depths.
site2.add_session('14-46-57', None, sessionTypes['lp'])#@2400um
site2.add_session('14-49-30', None, sessionTypes['lt'])
site2.add_session('14-56-30', None, sessionTypes['nb'])
site2.add_session('15-04-23', None, sessionTypes['nb'])#@2500um
site2.add_session('15-06-35', None, sessionTypes['lp'])
 
sitefuncs.nick_lan_daily_report(site2, 'site2', mainRasterInds=[0, 1, 2, 4], mainTCind = None, mainSTRind=None)


site3 = exp0818.add_site(depth = 2700, tetrodes = [3]) #laser response(ex+in), may be sound inhibited
site3.add_session('15-21-35', None, sessionTypes['nb']) #may have sound inhibition
site3.add_session('15-24-04', None, sessionTypes['lp']) #TT3 may be excited by laser then inhibited??
site3.add_session('15-26-28', None, sessionTypes['lt']) #TT3 has laser excitation.
site3.add_session('15-29-58', None, sessionTypes['nb']) #amp=0.45
site3.add_session('15-32-20', None, sessionTypes['lp']) #TT3 excited by laser then inhibited
site3.add_session('15-35-28', 'a', sessionTypes['tc'])

sitefuncs.nick_lan_daily_report(site3, 'site3', mainRasterInds=[1,2,3,4], mainTCind=5, mainSTRind=None)


site4 = exp0818.add_site(depth = 2900, tetrodes = [3])
site4.add_session('16-16-24', None, sessionTypes['lp']) #TT3 strong laser excitation, followed by inhibition of activity
site4.add_session('16-19-23', None, sessionTypes['lt'])
site4.add_session('16-22-52', None, sessionTypes['nb'])

sitefuncs.nick_lan_daily_report(site4, 'site4', mainRasterInds=[0,1,2], mainTCind= None, mainSTRind=None)


site5 = exp0818.add_site(depth = 3100, tetrodes = [3, 4])#TT3&4 prolonged laser inhibition
site5.add_session('16-44-15', None, sessionTypes['nb'])
site5.add_session('16-48-00', None, sessionTypes['lp'])
site5.add_session('16-51-45', None, sessionTypes['lt'])
site5.add_session('16-58-03', 'b', sessionTypes['str'])

sitefuncs.nick_lan_daily_report(site5, 'site5', mainRasterInds=[0,1,2], mainSTRind=3, mainTCind=None) 


site6 = exp0818.add_site(depth = 3200, tetrodes = [3, 4])
site6.add_session('17-08-34', None, sessionTypes['nb'])
site6.add_session('17-11-37', None, sessionTypes['lp']) #TT3 weak excitation, TT4 long inhibition. 
site6.add_session('17-14-15', None, sessionTypes['lt'])
site6.add_session('17-16-50', None, sessionTypes['nb'])
site6.add_session('17-22-41', 'c', sessionTypes['str'])

sitefuncs.nick_lan_daily_report(site6, 'site6', mainRasterInds=[0,1,2,3], mainSTRind=4, mainTCind=None) 

#cluster5 = site3.add_cluster(clusterNumber=5, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
#cluster4 = site3.add_cluster(clusterNumber=4, tetrode=6, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
'''

#second penetration
site7 = exp0818.add_site(depth = 3150, tetrodes = [3, 4])
site7.add_session('18-16-15', None, sessionTypes['nb'])
site7.add_session('18-18-43', None, sessionTypes['lt']) #TT3 has laser excitation, TT4 weak excitation.  
site7.add_session('18-21-45', None, sessionTypes['lp']) #TT3 has laser excitation, TT4 weak excitation. both followed by inhibition.
site7.add_session('18-23-49', None, sessionTypes['nb']) #amp=0.5

sitefuncs.nick_lan_daily_report(site7, 'site7', mainRasterInds=[0,1,2,3], mainSTRind=None, mainTCind=None) 



