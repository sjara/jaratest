from jaratoolbox import settings
from jaratoolbox.test.nick.ephysExperiments import ephys_experiment
reload(ephys_experiment)
from jaratoolbox.test.nick.ephysExperiments.ephys_experiment import RecordingSite
from jaratoolbox.test.nick.ephysExperiments.ephys_experiment import EphysExperiment
import matplotlib.pyplot as plt
import os
plt.ioff() #Turn off interactive plottting, save figs to png instead

animal = 'd1pi001'
date = '2015-07-07'
experimenter = 'lan'

exp0707 = EphysExperiment(animal,date,experimenter)

goodTetrode = 3

#tuningCurveSessions = [('2015-07-07_14-17-54', 'a'), ('2015-07-07_15-18-44', 'b'), ('2015-07-07_16-12-41', 'c'), ('2015-07-07_16-42-17', 'd'), ('2015-07-07_17-10-30', 'e'), ('2015-07-07_17-39-12', 'f'), ('2015-07-07_18-08-36', 'g'), ('2015-07-07_18-42-14', 'h')]

tuningCurveSessions = [('2015-07-07_16-42-17', 'd'), ('2015-07-07_17-10-30', 'e'), ('2015-07-07_17-39-12', 'f'), ('2015-07-07_18-08-36', 'g'), ('2015-07-07_18-42-14', 'h')]

for ind, (tuningsession, behavID) in enumerate(tuningCurveSessions):
    plt.figure()
    exp0707.sorted_tuning_raster(tuningsession, goodTetrode, behavID)   
    #fig_path = 'home/languo/data/ephys/{}/{}/'.format(animal, date)
    fig_path = os.path.join(settings.EPHYS_PATH,animal,date)
    fig_name = '{}site{}sortedraster.png'.format(date, (ind+4))
    full_fig_path = os.path.join(fig_path, fig_name)
    plt.show()
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
    plt.savefig(full_fig_path)
    plt.close()

    #plt.figure()   
    #exp0707.plot_session_tc_heatmap(tuningsession, goodTetrode, behavID)
    #plt.savefig(fname = '~/data/ephys/d1pi001/d1pi001_0707_site%shtmap.png'%(ind+1))
