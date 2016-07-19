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
                '2afc':'2afc'}

expList=[]
soundResponsiveCellCount=0
laserResponsiveCellCount=0
soundnlaserResponsiveCellCount=0
soundResponsiveTuned=0
###################Add all experiments that had good cells; recluster data using updated features, plot report for all clusters of the site, then pick out good clusters##############################

exp0701 = cellDB.Experiment(animalName = 'd1pi001', date = '2015-07-01', experimenter = 'lan', defaultParadigm='laser_tuning_curve')
expList.append(exp0701)

site3 = exp0701.add_site(depth = 2710, tetrodes = [6])
site3.add_session('19-09-42', None, sessionTypes['nb'])
site3.add_session('19-13-36', None, sessionTypes['lp'])
site3.add_session('19-16-32', None, sessionTypes['lt'])
site3.add_session('19-23-35', None, sessionTypes['1p'])  
site3.add_session('19-30-41', 'c', sessionTypes['tc'])
cluster2 = site3.add_cluster(cluster=2, tetrode=6) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='fair cell, no obvious tuning')
cluster3 = site3.add_cluster(cluster=3, tetrode=6) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments = 'tuned')
cluster4 = site3.add_cluster(cluster=4, tetrode=6) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='tuned')
cluster5 = site3.add_cluster(cluster=5, tetrode=6) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments = 'tuned')
cluster11 = site3.add_cluster(cluster=11, tetrode=6) #soundResponsive=True, laserPulseResponse=True,followsLaserTrain=True, comments='inhibited by laser, not tuned')
soundResponsiveCellCount+=5
laserResponsiveCellCount+=1
soundnlaserResponsiveCellCount+=1
soundResponsiveTuned=+3
#sitefuncs.plot_report_only_good_clusters(site3, 'site3', mainRasterInds=[0,1,2], mainTCind=4)
sitefuncs.nick_lan_daily_report_v2(site3, 'site3', mainRasterInds=[0,1,2], mainTCind=4)       

site4 = exp0701.add_site(depth = 2800, tetrodes = [6])
site4.add_session('19-49-07', None, sessionTypes['lp'])
site4.add_session('19-52-08', None, sessionTypes['nb'])
site4.add_session('19-54-43', None, sessionTypes['lt'])
site4.add_session('19-58-34', 'd', sessionTypes['tc'])
site4.add_session('20-11-17', None, sessionTypes['3p'])
site4.add_session('20-14-20', None, sessionTypes['1p'])                     
cluster3 = site4.add_cluster(cluster=3, tetrode=6) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=False, comments='fair cell')
cluster4 = site4.add_cluster(cluster=4, tetrode=6) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='fair cell, ISI violation')
cluster7 = site4.add_cluster(cluster=7, tetrode=6) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='good cell')
#sitefuncs.plot_report_only_good_clusters(site4, 'site4', mainRasterInds=[0,1,2], mainTCind=3)
sitefuncs.nick_lan_daily_report_v2(site4, 'site4', mainRasterInds=[0,1,2], mainTCind=3)

site5 = exp0701.add_site(depth = 2900, tetrodes = [3, 6])
site5.add_session('20-25-09', None, sessionTypes['lp'])
site5.add_session('20-28-03', None, sessionTypes['lt'])
site5.add_session('20-31-44', None, sessionTypes['nb'])
site5.add_session('20-34-08', None, sessionTypes['3p']) 
site5.add_session('20-39-59', 'e', sessionTypes['tc'])
cluster5 = site5.add_cluster(cluster=5, tetrode=3) #soundResponsive=False, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
cluster6 = site5.add_cluster(cluster=6, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='a bit small amp,tuned')
cluster8 = site5.add_cluster(cluster=8, tetrode=3) #soundResponsive=False, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
cluster12 = site5.add_cluster(cluster=12, tetrode=3) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned,good cell')
#sitefuncs.plot_report_only_good_clusters(site5, 'site5', mainRasterInds=[0,1,2], mainTCind=4)
#TT6 no good cells
sitefuncs.nick_lan_daily_report_v2(site5, 'site5', mainRasterInds=[0,1,2], mainTCind=4)

site6 = exp0701.add_site(depth = 3025, tetrodes = [6])
site6.add_session('21-01-24', None, sessionTypes['nb'])
site6.add_session('21-03-51', None, sessionTypes['lp'])
site6.add_session('21-06-10', None, sessionTypes['lt'])
site6.add_session('21-09-42', None, sessionTypes['1p'])
site6.add_session('21-12-07', 'f', sessionTypes['tc'])
cluster6 = site6.add_cluster(cluster=6, tetrode=6) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned')
cluster9 = site6.add_cluster(cluster=9, tetrode=6) #soundResponsive=False, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
cluster10 = site6.add_cluster(cluster=10, tetrode=6) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='tuned')
#sitefuncs.plot_report_only_good_clusters(site6, 'site6', mainRasterInds=[0,1,2], mainTCind=4)
sitefuncs.nick_lan_daily_report_v2(site6, 'site6', mainRasterInds=[0,1,2], mainTCind=4)

exp0707 = cellDB.Experiment(animalName = 'd1pi001', date = '2015-07-07', experimenter = 'lan', defaultParadigm='laser_tuning_curve')
expList.append(exp0707)
site3 = exp0707.add_site(depth = 3025, tetrodes = [3, 6])
site3.add_session('16-04-26', None, sessionTypes['nb'])
site3.add_session('16-06-32', None, sessionTypes['lp'])
site3.add_session('16-08-28', None, sessionTypes['lt'])
site3.add_session('16-12-41', 'c', sessionTypes['tc'])
cluster4 = site3.add_cluster(cluster=4, tetrode=3) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned')
cluster5 = site3.add_cluster(cluster=5, tetrode=3) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned')
TT6cluster7 = site3.add_cluster(cluster=7, tetrode=6) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned, sound inhibited')

#sitefuncs.plot_report_only_good_clusters(site3, 'site3', mainRasterInds=[0,1,2], mainTCind=3)
sitefuncs.nick_lan_daily_report_v2(site3, 'site3', mainRasterInds=[0,1,2], mainTCind=3)

site4 = exp0707.add_site(depth = 3075, tetrodes = [3, 6])
site4.add_session('16-34-24', None, sessionTypes['nb'])
site4.add_session('16-36-42', None, sessionTypes['lp'])
site4.add_session('16-38-59', None, sessionTypes['lt'])
site4.add_session('16-42-17', 'd', sessionTypes['tc'])
site4.add_session('16-55-51', None, sessionTypes['1p'])
site4.add_session('16-57-40', None, sessionTypes['3p'])
cluster8 = site4.add_cluster(cluster=8, tetrode=3) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned')
cluster9 = site4.add_cluster(cluster=9, tetrode=3) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned')
#sitefuncs.plot_report_only_good_clusters(site4, 'site4', mainRasterInds=[0,1,2], mainTCind=3)
sitefuncs.nick_lan_daily_report_v2(site4, 'site4', mainRasterInds=[0,1,2], mainTCind=3)

site5 = exp0707.add_site(depth = 3125, tetrodes = [3, 6])
site5.add_session('17-02-39', None, sessionTypes['nb'])
site5.add_session('17-05-02', None, sessionTypes['lp'])
site5.add_session('17-07-13', None, sessionTypes['lt'])
site5.add_session('17-10-30', 'e', sessionTypes['tc'])
site5.add_session('17-25-32', None, sessionTypes['1p'])
site5.add_session('17-26-58', None, sessionTypes['3p'])
cluster5 = site5.add_cluster(cluster=5, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=False, comments='tuned')
cluster8 = site5.add_cluster(cluster=8, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=False, comments='tuned')
cluster9 = site5.add_cluster(cluster=9, tetrode=3) #soundResponsive=True, laserPulseResponse=Inhibited, followsLaserTrain=False, comments='tuned')
cluster10 = site5.add_cluster(cluster=10, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='tuned')
cluster11 = site5.add_cluster(cluster=11, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='tuned')

#sitefuncs.plot_report_only_good_clusters(site5, 'site5', mainRasterInds=[0,1,2], mainTCind=3)
sitefuncs.nick_lan_daily_report_v2(site5, 'site5', mainRasterInds=[0,1,2], mainTCind=3)

site6 = exp0707.add_site(depth = 3200, tetrodes = [3, 6])
site6.add_session('17-31-32', None, sessionTypes['nb'])
site6.add_session('17-33-53', None, sessionTypes['lp'])
site6.add_session('17-36-05', None, sessionTypes['lt'])
site6.add_session('17-39-12', 'f', sessionTypes['tc'])
site6.add_session('17-52-09', None, sessionTypes['3p'])
site6.add_session('17-54-00', None, sessionTypes['1p'])
cluster2 = site6.add_cluster(cluster=2, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='tuned')
cluster4 = site6.add_cluster(cluster=4, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='tuned')
cluster6 = site6.add_cluster(cluster=6, tetrode=3) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned')
cluster10 = site6.add_cluster(cluster=10, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='tuned')
TT6cluster3=site6.add_cluster(cluster=3, tetrode=6) #soundResponsive=False, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
TT6cluster4=site6.add_cluster(cluster=4, tetrode=6) #soundResponsive=False, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
TT6cluster9 = site6.add_cluster(cluster=9, tetrode=6) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned')
#sitefuncs.plot_report_only_good_clusters(site6, 'site6', mainRasterInds=[0,1,2], mainTCind=3)
sitefuncs.nick_lan_daily_report_v2(site6, 'site6', mainRasterInds=[0,1,2], mainTCind=3)


site7 = exp0707.add_site(depth = 3275, tetrodes = [3,4,6])
site7.add_session('18-01-55', None, sessionTypes['nb'])
site7.add_session('18-03-53', None, sessionTypes['lp'])
site7.add_session('18-05-36', None, sessionTypes['lt'])
site7.add_session('18-08-36', 'g', sessionTypes['tc'])
site7.add_session('18-22-56', None, sessionTypes['3p'])
site7.add_session('18-24-20', None, sessionTypes['1p'])
cluster2 = site7.add_cluster(cluster=2, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='tuned')
cluster3 = site7.add_cluster(cluster=3, tetrode=3) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned')
cluster4=site7.add_cluster(cluster=4, tetrode=3) #soundResponsive=False, laserPulseResponse=False, followsLaserTrain=False, comments='good cell')
cluster9 = site7.add_cluster(cluster=9, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='tuned, but activity not consistent'
#sitefuncs.plot_report_only_good_clusters(site7, 'site7', mainRasterInds=[0,1,2], mainTCind=3)
sitefuncs.nick_lan_daily_report_v2(site7, 'site7', mainRasterInds=[0,1,2], mainTCind=3)


site8 = exp0707.add_site(depth = 3325, tetrodes = [3,4,6])
site8.add_session('18-29-42', None, sessionTypes['nb'])
site8.add_session('18-32-16', None, sessionTypes['lp'])
site8.add_session('18-34-54', None, sessionTypes['lt'])
site8.add_session('18-42-14', 'h', sessionTypes['tc'])
site8.add_session('18-53-39', None, sessionTypes['3p'])
cluster2 = site8.add_cluster(cluster=2, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='tuned')
cluster5 = site8.add_cluster(cluster=5, tetrode=3) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned')

#sitefuncs.plot_report_only_good_clusters(site8, 'site8', mainRasterInds=[0,1,2], mainTCind=3)
sitefuncs.nick_lan_daily_report_v2(site8, 'site8', mainRasterInds=[0,1,2], mainTCind=3)


exp0726 = cellDB.Experiment(animalName = 'd1pi002', date = '2015-07-26', experimenter = 'lan', defaultParadigm='laser_tuning_curve')
expList.append(exp0726)
site1 = exp0726.add_site(depth = 2702, tetrodes = [3])
site1.add_session('15-26-00', None, sessionTypes['nb'])  #amp = 0.45
site1.add_session('15-28-10', None, sessionTypes['lp']) #power=2.5mW
site1.add_session('15-29-48', None, sessionTypes['lt']) #power=2.5mW
site1.add_session('15-32-31', 'a', sessionTypes['tc'])
site1.add_session('15-47-57', 'b', sessionTypes['tc'])
site1.add_session('16-00-02', None, sessionTypes['3p'])
site1.add_session('16-01-34', None, sessionTypes['nb']) #comment='amp = 0.5'
cluster3 = site1.add_cluster(cluster=3, tetrode=3) #soundResponsive=False, laserPulseResponse=True, followsLaserTrain=True, comments='not tuned')
cluster9 = site1.add_cluster(cluster=9, tetrode=3) #soundResponsive=False, laserPulseResponse=False, followsLaserTrain=False, comments='fair')
#sitefuncs.plot_report_only_good_clusters(site1, 'site1', mainRasterInds=[0,1,2], mainTCind=3)
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0,1,2], mainTCind=3)


site3 = exp0726.add_site(depth = 2936, tetrodes = [3, 4])
site3.add_session('16-57-55', None, sessionTypes['lp'])
site3.add_session('17-02-35', None, sessionTypes['lt'])
site3.add_session('17-05-19', None, sessionTypes['nb']) #comment='amp=0.5')
site3.add_session('17-07-37', None, sessionTypes['bf']) #comment='4freq from 15k-40kHz, 40-70dB')
site3.add_session('17-09-20', 'd', sessionTypes['tc'])
cluster4 = site3.add_cluster(cluster=4, tetrode=4) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='tuned, inverted spike')
#sitefuncs.plot_report_only_good_clusters(site3, 'site3', mainRasterInds=[0,1,2,3], mainTCind=4)
sitefuncs.nick_lan_daily_report_v2(site3, 'site3', mainRasterInds=[0,1,2,3], mainTCind=4)

site4 = exp0726.add_site(depth = 3300, tetrodes = [3, 4])
site4.add_session('17-56-14', None, sessionTypes['lp'])
site4.add_session('17-57-56', None, sessionTypes['nb'])
site4.add_session('17-59-52', None, sessionTypes['lt'])
site4.add_session('18-01-59', 'e', sessionTypes['tc'])
site4.add_session('18-15-25', None, sessionTypes['bf']) # comment='4freq from 15k-30kHz @60dB')
cluster2 = site4.add_cluster(cluster=2, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='tuned,fair')
cluster4 = site4.add_cluster(cluster=4, tetrode=3) #soundResponsive=False, laserPulseResponse=True, followsLaserTrain=True, comments='no clear noise response but tuned,fair')
cluster7 = site4.add_cluster(cluster=7, tetrode=3) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned,fair')
cluster8 = site4.add_cluster(cluster=8, tetrode=3) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned,fair')
##########The same cell got clustered into cluster10 and 11 on TT3
#cluster10 = site4.add_cluster(cluster=10, tetrode=3) #soundResponsive=False, laserPulseResponse=True, followsLaserTrain=True, comments='tuned,fair')
#cluster11 = site4.add_cluster(cluster=11, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='tuned,fair')

TT4cluster5 = site4.add_cluster(cluster=5, tetrode=4) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='tuned,fair')
TT4cluster6 = site4.add_cluster(cluster=6, tetrode=4) #soundResponsive=False, laserPulseResponse=False, followsLaserTrain=False, comments='fair')

#sitefuncs.plot_report_only_good_clusters(site4, 'site4', mainRasterInds=[0,1,2,4], mainTCind=3)
sitefuncs.nick_lan_daily_report_v2(site4, 'site4', mainRasterInds=[0,1,2,4], mainTCind=3)


exp0728 = cellDB.Experiment(animalName = 'd1pi002', date = '2015-07-28', experimenter = 'lan', defaultParadigm='laser_tuning_curve')
expList.append(exp0728)
site1 = exp0728.add_site(depth = 1300, tetrodes = [3]) #cortical laser response
site1.add_session('13-13-39', None, sessionTypes['1p'])
site1.add_session('13-15-55', None, sessionTypes['lt'])  #comment ='power=1.5mW'
site1.add_session('13-22-26', None, sessionTypes['lp']) #comment ='power=2mW'
site1.add_session('13-24-13', None, sessionTypes['nb']) #no response
#cluster2 = site1.add_cluster(cluster=2, tetrode=3) #soundResponsive=False, laserPulseResponse=True, followsLaserTrain=True, comments='fair')
#sitefuncs.plot_report_only_good_clusters(site1, 'site1', mainRasterInds=[0,2,3], mainTCind=None)
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0,2,3], mainTCind=None)


site2 = exp0728.add_site(depth = 2730, tetrodes = [3,4])
site2.add_session('14-12-21', None, sessionTypes['lp'])  #power=2.0mW. no response
site2.add_session('14-13-39', None, sessionTypes['nb']) #amp=0.5
site2.add_session('14-18-55', 'a', sessionTypes['tc']) #weird-looking multiunit tuning curve, in sorted raster looks like two range of preferred frequencies
site2.add_session('14-34-27', None, sessionTypes['lt']) #power=2.0mW. no response
#cluster3 = site2.add_cluster(cluster=3, tetrode=3) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='fair')
#sitefuncs.plot_report_only_good_clusters(site2, 'site2', mainRasterInds=[0,1,3], mainTCind=2)
sitefuncs.nick_lan_daily_report_v2(site2, 'site2', mainRasterInds=[0,1,3], mainTCind=2)


site3 = exp0728.add_site(depth = 3277, tetrodes = [3])
site3.add_session('15-14-45', None, sessionTypes['lp'])
site3.add_session('15-26-27', None, sessionTypes['lt'])
site3.add_session('15-30-09', None, sessionTypes['nb']) #amp=0.5
site3.add_session('15-32-15', 'b', sessionTypes['tc'])
site3.add_session('15-44-32', None, sessionTypes['bf']) #4freq from 15k-22kHz, @60dB
site3.add_session('15-51-42', None, sessionTypes['1p'])
#cluster8 = site3.add_cluster(cluster=8, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='good cell')
#cluster9 = site3.add_cluster(cluster=9, tetrode=3) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='inhibited by sound')
#sitefuncs.plot_report_only_good_clusters(site3, 'site3', mainRasterInds=[0,1,2,4], mainTCind=3)
sitefuncs.nick_lan_daily_report_v2(site3, 'site3', mainRasterInds=[0,1,2,4], mainTCind=3)


site4 = exp0728.add_site(depth = 3351, tetrodes = [3, 5])
site4.add_session('15-59-40', None, sessionTypes['nb'])
site4.add_session('16-02-06', None, sessionTypes['1p'])
site4.add_session('16-04-04', None, sessionTypes['lt']) #power=1mW
site4.add_session('16-06-17', None, sessionTypes['nb'])
site4.add_session('16-08-53', 'c', sessionTypes['tc'])
site4.add_session('16-22-29', None, sessionTypes['bf']) #4freq from 15k-22kHz @60dB
site4.add_session('16-26-04', None, sessionTypes['lp']) #power=2mW
#cluster4 = site4.add_cluster(cluster=4, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='weak sound response')
#cluster6 = site4.add_cluster(cluster=6, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='weak sound response')
#TT3cluster8 = site4.add_cluster(cluster=8, tetrode=3) #soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments = 'may have some spikes from another cluster mixed in')
#cluster9 = site4.add_cluster(cluster=9, tetrode=3) #soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='weak laser response')
#TT5cluster8 = site4.add_cluster(cluster=8, tetrode=5) #soundResponsive=False, laserPulseResponse=True, followsLaserTrain=True, comments='clusters2,4,6,7,8 on TT5 have very similar waveform, cell likely inhibited by high freq sound')
#sitefuncs.plot_report_only_good_clusters(site4, 'site4', mainRasterInds=[0,2,5,6], mainTCind=4)
sitefuncs.nick_lan_daily_report_v2(site4, 'site4', mainRasterInds=[0,2,5,6], mainTCind=4)

##############################################################################################
#For good clusters:Plot rasters and tuning heatmap, also waveform, ISI, projection
##############################################################################################




'''
for Exp in expList:
    ephys_Exp = ee3.EphysExperiment(Exp.animalName, Exp.date, Exp.experimenter)
    plt.figure(figsize = (12,6))
    #plot raster for noise burst and laser pulse, heatmap for tuning curve session for only the clusters of interest.
    for indSite, Site in enumerate(Exp.siteList):
        for indCluster, Cluster in enumerate(Site.clusterList): 
            for indSession, Session in enumerate(Site.sessionList):
                if Session.sessionType == 'laserPulse':
                    plt.subplot2grid((2,6), (0, 0), rowspan=1, colspan=3)
                    ephys_Exp.plot_session_raster(Session.session,Cluster.tetrode,cluster=Cluster.clusterNumber,replace=1,ms=1)
                    plt.ylabel(Session.sessionType,fontsize=10)
                    ax = plt.gca()
                    extraplots.set_ticks_fontsize(ax, 6)
                if Session.sessionType == 'noiseBurst':       
                    plt.subplot2grid((2,6), (1, 0), rowspan=1, colspan=3)
                    ephys_Exp.plot_session_raster(Session.session,Cluster.tetrode,cluster=Cluster.clusterNumber,replace=1,ms=1)
                    plt.ylabel(Session.sessionType,fontsize=10)
                    ax = plt.gca()
                    extraplots.set_ticks_fontsize(ax, 6)
                if Session.sessionType == 'tuningCurve':
                    plt.subplot2grid((2,6), (0, 3), rowspan=2, colspan=3)
                    ephys_Exp.plot_session_tc_heatmap(Session.session,Cluster.tetrode,Session.behavFileIdentifier,replace=1,cluster=Cluster.clusterNumber)
                    plt.title(
                        "{0}\nBehavFileID = '{1}'".format(
                            Session.session,
                            Session.behavFileIdentifier), fontsize=10)
                    ax = plt.gca()
                    extraplots.set_ticks_fontsize(ax, 6)

            fig_path = '/tmp'
            fig_name = '{}{}D{}TT{}C{}.png'.format(Site.animalName,Site.date,Site.depth,Cluster.tetrode,Cluster.clusterNumber)
            full_fig_path = os.path.join(fig_path, fig_name)
            plt.savefig(full_fig_path, format='png')
'''

