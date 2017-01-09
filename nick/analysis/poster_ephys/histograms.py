from matplotlib import pyplot as plt
import numpy as np
import pandas
thaldb = pandas.read_pickle('./thalamusdb_q10.pickle')
cortexdb = pandas.read_pickle('./cortexdb_q10.pickle')

goodthalcells = thaldb[(thaldb['noiseburstMaxZ']>2) & (thaldb['isiViolations']<4)]
goodcortexcells = cortexdb[(cortexdb['noiseburstMaxZ']>2) & (cortexdb['isiViolations']<4)]

IDthalcells = thaldb[(thaldb['noiseburstMaxZ']>2) & (thaldb['laserpulseMaxZ']>2) & (thaldb['lasertrainMaxZ']>2) & (thaldb['isiViolations']<4)]
IDcortexcells = cortexdb[(cortexdb['noiseburstMaxZ']>2) & (cortexdb['laserpulseMaxZ']>2) & (cortexdb['lasertrainMaxZ']>2) & (cortexdb['isiViolations']<4)]

def plot_hists(group1, group2, label1=None, label2=None):
    bins = np.linspace(0, 2, 20)

    plt.hist(group1, bins, alpha=0.5, label=label1, histtype='step')
    plt.hist(group2, bins, alpha=0.5, label=label2, histtype='step')
    plt.legend(loc='upper left')


plt.clf()
plot_hists(goodthalcells['Q10'].dropna(), goodcortexcells['Q10'].dropna(), 'Sound-responsive thalamic cells', 'Sound-responsive cortical cells')
plt.xlabel('BW10')
plt.ylabel('# Neurons')
plt.show()

# plt.clf()
# plot_hists(1/IDthalcells['Q10'].dropna(), 1/IDcortexcells['Q10'].dropna(), 'Identified thalamo-striatal cells', 'Identified cortico-striatal cells')
# plt.xlabel('Q10')
# plt.ylabel('# Neurons')
# plt.show()
