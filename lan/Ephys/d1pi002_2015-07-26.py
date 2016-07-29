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
 
exp0726 = rd.Recording(animalName = 'd1pi002', date = '2015-07-26', experimenter = 'lan', paradigm='laser_tuning_curve')


site1 = exp0726.add_site(depth = 2702, goodTetrodes = [3])
site1.add_session('15-26-00', None, sessionTypes['nb']).set_plot_type('raster', report='main')  #amp = 0.45
site1.add_session('15-28-10', None, sessionTypes['lp']).set_plot_type('raster', report='main') #power=2.5mW
site1.add_session('15-29-48', None, sessionTypes['lt']).set_plot_type('raster', report='main') #power=2.5mW
site1.add_session('15-32-31', 'a', sessionTypes['tc']).set_plot_type('tc_heatmap', report='main')
site1.add_session('15-47-57', 'b', sessionTypes['tc'])
site1.add_session('16-00-02', None, sessionTypes['3p']).set_plot_type('raster', report='main')
site1.add_session('16-01-34', None, sessionTypes['nb']) #comment='amp = 0.5'
cluster3 = site1.add_cluster(clusterNumber=3, tetrode=3, soundResponsive=False, laserPulseResponse=True, followsLaserTrain=True, comments='fair')
cluster9 = site1.add_cluster(clusterNumber=9, tetrode=3, soundResponsive=True, laserPulseResponse=False, followsLaserTrain=False, comments='fair')


site2 = exp0726.add_site(depth = 2872, goodTetrodes = [3])
site2.add_session('16-36-35', None, sessionTypes['lp']).set_plot_type('raster', report='main')  #comment='no response')
site2.add_session('16-37-53', None, sessionTypes['nb']).set_plot_type('raster', report='main')
site2.add_session('16-39-40', None, sessionTypes['lt']).set_plot_type('raster', report='main') #comment='no response')
site2.add_session('16-42-14', 'c', sessionTypes['tc']).set_plot_type('tc_heatmap', report='main')


site3 = exp0726.add_site(depth = 2936, goodTetrodes = [3, 4])
site3.add_session('16-57-55', None, sessionTypes['lp']).set_plot_type('raster', report='main')
site3.add_session('17-02-35', None, sessionTypes['lt']).set_plot_type('raster', report='main')
site3.add_session('17-05-19', None, sessionTypes['nb']).set_plot_type('raster', report='main') #comment='amp=0.5')
site3.add_session('17-07-37', None, sessionTypes['bf']).set_plot_type('raster', report='main') #comment='4freq from 15k-40kHz, 40-70dB')
site3.add_session('17-09-20', 'd', sessionTypes['tc']).set_plot_type('tc_heatmap', report='main')
cluster3 = site3.add_cluster(clusterNumber=3, tetrode=4, soundResponsive=False, laserPulseResponse=True, followsLaserTrain=True, comments='fair')


site4 = exp0726.add_site(depth = 3300, goodTetrodes = [3, 4])
site4.add_session('17-56-14', None, sessionTypes['lp']).set_plot_type('raster', report='main')
site4.add_session('17-57-56', None, sessionTypes['nb']).set_plot_type('raster', report='main')
site4.add_session('17-59-52', None, sessionTypes['lt']).set_plot_type('raster', report='main')
site4.add_session('18-01-59', 'e', sessionTypes['tc']).set_plot_type('tc_heatmap', report='main')
site4.add_session('18-15-25', None, sessionTypes['bf']).set_plot_type('raster', report='main') # comment='4freq from 15k-30kHz @60dB')
cluster3 = site4.add_cluster(clusterNumber=3, tetrode=3, soundResponsive=True, laserPulseResponse=True, followsLaserTrain=True, comments='fair')


site5 = exp0726.add_site(depth = 3357, goodTetrodes = [3, 4])
site5.add_session('18-22-41', None, sessionTypes['nb']).set_plot_type('raster', report='main')
site5.add_session('18-25-06', None, sessionTypes['lp']).set_plot_type('raster', report='main')
site5.add_session('18-27-48', None, sessionTypes['lt']).set_plot_type('raster', report='main')
site5.add_session('18-32-17', 'f', sessionTypes['tc']).set_plot_type('tc_heatmap', report='main')
site5.add_session('18-44-29', None, sessionTypes['bf']).set_plot_type('raster', report='main') #comment='4freq from 15k-30kHz @60dB')
site5.add_session('18-46-11', None, sessionTypes['1p'])


site6 = exp0726.add_site(depth = 3402, goodTetrodes = [3, 4])
site6.add_session('18-48-41', None, sessionTypes['1p'])
site6.add_session('18-49-47', None, sessionTypes['nb']).set_plot_type('raster', report='main')
site6.add_session('18-51-43', None, sessionTypes['lp']).set_plot_type('raster', report='main')
site6.add_session('18-53-23', None, sessionTypes['lt']).set_plot_type('raster', report='main')
site6.add_session('18-55-37', 'g', sessionTypes['tc']).set_plot_type('tc_heatmap', report='main')
site6.add_session('19-07-31', None, sessionTypes['bf']) #comment='4freq from 8k-12kHz @60dB')
site6.add_session('19-08-55', None, sessionTypes['bf']).set_plot_type('raster', report='main')  #comment='4freq from 18k-27kHz @60dB')



'''
Code for generating main reports for all clusters at each site.
 
for site in exp0726.siteList:
    site.generate_main_report()
'''

'''
This code is for making tuning curve heatmap figures for each recording site before clustering

ephys0726 = ee3.EphysExperiment(animalName = 'd1pi002', date = '2015-07-26', experimenter = 'lan')

for indS, Site in enumerate(exp0726.siteList): 
    for Session in Site.sessionList:
        if Session.sessionType == 'tuningCurve':
            for Tetrode in Site.goodTetrodes:
                plt.figure()
                ephys0726.plot_session_tc_heatmap(Session.session, Tetrode, Session.behavFileIdentifier)
                fig_path = os.path.join(settings.EPHYS_PATH,Site.animalName,Site.date,'tcheatmap')
                fig_name = '{}tetrode{}site{}{}.png'.format(Site.date, Tetrode, (indS+1), Session.session)
                full_fig_path = os.path.join(fig_path, fig_name)
                plt.show()
                if not os.path.exists(fig_path):
                    os.makedirs(fig_path)
                plt.savefig(full_fig_path)
                plt.close()
'''


