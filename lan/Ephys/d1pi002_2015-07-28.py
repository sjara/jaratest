#Write into JSON database only cells with good amp (>=40uV), consistent firing throughout recording, good waveform, with either sound or laser response or both.

from jaratoolbox.test.nick.ephysExperiments import recordingday as rd
reload(rd)
from jaratoolbox.test.nick.ephysExperiments import ephys_experiment_v3 as ee3
reload(ee3)
import matplotlib.pyplot as plt
import os
from jaratoolbox import settings

sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse'}
 

exp0728 = rd.Recording(animalName = 'd1pi002', date = '2015-07-28', experimenter = 'lan', paradigm='laser_tuning_curve')

site1 = exp0728.add_site(depth = 1300, goodTetrodes = [3]) #cortical laser response
site1.add_session('13-13-39', None, sessionTypes['1p']).set_plot_type('raster', report='main')
site1.add_session('13-15-55', None, sessionTypes['lt']).set_plot_type('raster', report='main')  #comment ='power=1.5mW'
site1.add_session('13-22-26', None, sessionTypes['lp']).set_plot_type('raster', report='main') #comment ='power=2mW'
site1.add_session('13-24-13', None, sessionTypes['nb']).set_plot_type('raster', report='main')  #no response
cluster2 = site1.add_cluster(clusterNumber=2, tetrode=3, soundResponsive=False, laserPulseResponse=True, followsLaserTrain=True, comments='fair')


site2 = exp0728.add_site(depth = 2730, goodTetrodes = [3,4])
site2.add_session('14-12-21', None, sessionTypes['lp']).set_plot_type('raster', report='main')  #power=2.0mW. no response
site2.add_session('14-13-39', None, sessionTypes['nb']).set_plot_type('raster', report='main') #amp=0.5
site2.add_session('14-18-55', 'a', sessionTypes['tc']).set_plot_type('tc_heatmap', report='main') #weird-looking multiunit tuning curve, in sorted raster looks like two range of preferred frequencies
site2.add_session('14-34-27', None, sessionTypes['lt']).set_plot_type('raster', report='main') #power=2.0mW. no response
cluster3 = site2.add_cluster(clusterNumber=3, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='fair')


site3 = exp0728.add_site(depth = 3277, goodTetrodes = [3])
site3.add_session('15-14-45', None, sessionTypes['lp']).set_plot_type('raster', report='main')
site3.add_session('15-26-27', None, sessionTypes['lt']).set_plot_type('raster', report='main')
site3.add_session('15-30-09', None, sessionTypes['nb']).set_plot_type('raster', report='main') #amp=0.5
site3.add_session('15-32-15', 'b', sessionTypes['tc']).set_plot_type('tc_heatmap', report='main')
site3.add_session('15-44-32', None, sessionTypes['bf']).set_plot_type('raster', report='main') #4freq from 15k-22kHz, @60dB
site3.add_session('15-51-42', None, sessionTypes['1p']).set_plot_type('raster', report='main')
cluster8 = site3.add_cluster(clusterNumber=8, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='good cell')
cluster9 = site3.add_cluster(clusterNumber=9, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='inhibited by sound')


site4 = exp0728.add_site(depth = 3351, goodTetrodes = [3, 5])
site4.add_session('15-59-40', None, sessionTypes['nb']).set_plot_type('raster', report='main')
site4.add_session('16-02-06', None, sessionTypes['1p'])
site4.add_session('16-04-04', None, sessionTypes['lt']).set_plot_type('raster', report='main') #power=1mW
site4.add_session('16-06-17', None, sessionTypes['nb'])
site4.add_session('16-08-53', 'c', sessionTypes['tc']).set_plot_type('tc_heatmap', report='main')
site4.add_session('16-22-29', None, sessionTypes['bf']).set_plot_type('raster', report='main') #4freq from 15k-22kHz @60dB
site4.add_session('16-26-04', None, sessionTypes['lp']).set_plot_type('raster', report='main') #power=2mW
cluster4 = site4.add_cluster(clusterNumber=4, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='weak sound response')
cluster6 = site4.add_cluster(clusterNumber=6, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='weak sound response')
TT3cluster8 = site4.add_cluster(clusterNumber=8, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments = 'may have some spikes from another cluster mixed in')
cluster9 = site4.add_cluster(clusterNumber=9, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='weak laser response')
TT5cluster8 = site4.add_cluster(clusterNumber=8, tetrode=5, soundResponsive=False, laserPulseResponse=True, followsLaserTrain=True, comments='clusters2,4,6,7,8 on TT5 have very similar waveform, cell likely inhibited by high freq sound')


'''
for site in exp0728.siteList:
    site.generate_main_report()
'''

'''
ephys0728 = ee3.EphysExperiment(animalName = 'd1pi002', date = '2015-07-28', experimenter = 'lan')

for indS, Site in enumerate(exp0728.siteList): 
    for Session in Site.sessionList:
        if Session.sessionType == 'tuningCurve':
            for Tetrode in Site.goodTetrodes:
                plt.figure()
                ephys0728.plot_session_tc_heatmap(Session.session, Tetrode, Session.behavFileIdentifier)
                fig_path = os.path.join(settings.EPHYS_PATH,Site.animalName,Site.date,'tcheatmap')
                fig_name = '{}tetrode{}site{}{}.png'.format(Site.date, Tetrode, (indS+1), Session.session)
                full_fig_path = os.path.join(fig_path, fig_name)
                plt.show()
                if not os.path.exists(fig_path):
                    os.makedirs(fig_path)
                plt.savefig(full_fig_path)
                plt.close()
                
                plt.figure()
                ephys0728.plot_sorted_tuning_raster(Session.session, Tetrode, Session.behavFileIdentifier)
                fig_path = os.path.join(settings.EPHYS_PATH,Site.animalName,Site.date,'sortedraster')
                fig_name = '{}tetrode{}site{}{}.png'.format(Site.date, Tetrode, (indS+1), Session.session)
                full_fig_path = os.path.join(fig_path, fig_name)
                plt.show()
                if not os.path.exists(fig_path):
                    os.makedirs(fig_path)
                plt.savefig(full_fig_path)
                plt.close()
'''
