from jaratoolbox.test.nick.ephysExperiments import recordingday as rd
reload(rd)
from jaratoolbox.test.nick.ephysExperiments import ephys_experiment_v3 as ee3
reload(ee3)
import matplotlib.pyplot as plt
import os
from jaratoolbox import settings
from jaratoolbox import extraplots

sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse'}

#Below I'm initializing an experiment and adding the recording sites that contained the cells of interest. At each site I added all the recorded sessions (with file name and session type); spikes from all the sessions were gathered together for clustering. But after clustering is done, individual sessions will have its own clu file saved (which I have synced back to jarahub). You can use the cluster informatin contained in the clu file in each session to plot a session for spikes of one cluster.  
#The good cells we want to plot are added as clusters to the recording site. As we discussed, the laser responsive clusters (also sound responsive) have a comment 'for panels BCD'; the ones that are sound responsive but not laser responsive have a comment 'for panels EFG'.  

exp0701 = rd.Recording(animalName = 'd1pi001', date = '2015-07-01', experimenter = 'lan', paradigm='laser_tuning_curve')
site3 = exp0701.add_site(depth = 2710, goodTetrodes = [6])
site3.add_session('19-09-42', None, sessionTypes['nb'])
site3.add_session('19-13-36', None, sessionTypes['lp'])
site3.add_session('19-16-32', None, sessionTypes['lt'])
site3.add_session('19-23-35', None, sessionTypes['1p'])  
site3.add_session('19-30-41', 'c', sessionTypes['tc'])
cluster10 = site3.add_cluster(clusterNumber=10, tetrode=6, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='for panels BCD')

site4 = exp0701.add_site(depth = 2800, goodTetrodes = [6])
site4.add_session('19-49-07', None, sessionTypes['lp'])
site4.add_session('19-52-08', None, sessionTypes['nb'])
site4.add_session('19-54-43', None, sessionTypes['lt'])
site4.add_session('19-58-34', 'd', sessionTypes['tc'])
site4.add_session('20-11-17', None, sessionTypes['3p'])
site4.add_session('20-14-20', None, sessionTypes['1p'])                     
cluster5 = site4.add_cluster(clusterNumber=5, tetrode=6, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='for panels BCD')

exp0707 = rd.Recording(animalName = 'd1pi001', date = '2015-07-07', experimenter = 'lan', paradigm='laser_tuning_curve')
site4 = exp0707.add_site(depth = 3075, goodTetrodes = [3, 6])
site4.add_session('16-34-24', None, sessionTypes['nb'])
site4.add_session('16-36-42', None, sessionTypes['lp'])
site4.add_session('16-38-59', None, sessionTypes['lt'])
site4.add_session('16-42-17', 'd', sessionTypes['tc'])
site4.add_session('16-55-51', None, sessionTypes['1p'])
site4.add_session('16-57-40', None, sessionTypes['3p'])
cluster6 = site4.add_cluster(clusterNumber=6, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='for panels BCD')

site5 = exp0707.add_site(depth = 3125, goodTetrodes = [3, 6])
site5.add_session('17-02-39', None, sessionTypes['nb'])
site5.add_session('17-05-02', None, sessionTypes['lp'])
site5.add_session('17-07-13', None, sessionTypes['lt'])
site5.add_session('17-10-30', 'e', sessionTypes['tc'])
site5.add_session('17-25-32', None, sessionTypes['1p'])
site5.add_session('17-26-58', None, sessionTypes['3p'])
cluster11 = site5.add_cluster(clusterNumber=11, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='for panels EFG')
cluster2 = site5.add_cluster(clusterNumber=2, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='for panels BCD')

site6 = exp0707.add_site(depth = 3200, goodTetrodes = [3, 6])
site6.add_session('17-31-32', None, sessionTypes['nb'])
site6.add_session('17-33-53', None, sessionTypes['lp'])
site6.add_session('17-36-05', None, sessionTypes['lt'])
site6.add_session('17-39-12', 'f', sessionTypes['tc'])
site6.add_session('17-52-09', None, sessionTypes['3p'])
site6.add_session('17-54-00', None, sessionTypes['1p'])
cluster4 = site6.add_cluster(clusterNumber=4, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='for panels BCD')
cluster8 = site6.add_cluster(clusterNumber=8, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='for panels BCD; could be merged with cluster4 because of similar wave form')


exp0728 = rd.Recording(animalName = 'd1pi002', date = '2015-07-28', experimenter = 'lan', paradigm='laser_tuning_curve')
site3 = exp0728.add_site(depth = 3277, goodTetrodes = [3])
site3.add_session('15-14-45', None, sessionTypes['lp']).set_plot_type('raster', report='main')
site3.add_session('15-26-27', None, sessionTypes['lt']).set_plot_type('raster', report='main')
site3.add_session('15-30-09', None, sessionTypes['nb']).set_plot_type('raster', report='main') #amp=0.5
site3.add_session('15-32-15', 'b', sessionTypes['tc']).set_plot_type('tc_heatmap', report='main')
site3.add_session('15-44-32', None, sessionTypes['bf']).set_plot_type('raster', report='main') #4freq from 15k-22kHz, @60dB
site3.add_session('15-51-42', None, sessionTypes['1p']).set_plot_type('raster', report='main')
cluster8 = site3.add_cluster(clusterNumber=8, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='for panels BCD')




#Here is the plotting part. I am using ephys_experiment_v3 because that holds the plotting functions for raster and tuning curve heatmap. The resulting graphs get saved to '/tmp' and can be changed by changing fig_path.
for Exp in [exp0701, exp0707, exp0728]:
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


