from matplotlib import pyplot as plt
from collections import Counter
from jaratest.nick.stats import am_funcs
reload(am_funcs)
import pandas
import numpy as np
from jaratoolbox import colorpalette

thaldbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb_q10.pickle'
cortdbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb_q10.pickle'
thaldb = pandas.read_pickle(thaldbfn)
cortdb = pandas.read_pickle(cortdbfn)

laserTrainThresh = 1.5
noiseBurstThresh = 2
isiThresh = 4

thalNonID = thaldb[(thaldb['isiViolations']<isiThresh) & (thaldb['noiseburstMaxZ']>noiseBurstThresh) & (thaldb['lasertrainMaxZ']<laserTrainThresh)]
cortNonID = cortdb[(cortdb['isiViolations']<isiThresh) & (cortdb['noiseburstMaxZ']>noiseBurstThresh) & (cortdb['lasertrainMaxZ']<laserTrainThresh)]

thalID = thaldb[(thaldb['isiViolations']<isiThresh) & (thaldb['noiseburstMaxZ']>noiseBurstThresh) & (thaldb['lasertrainMaxZ']>laserTrainThresh)]
cortID = cortdb[(cortdb['isiViolations']<isiThresh) & (cortdb['noiseburstMaxZ']>noiseBurstThresh) & (cortdb['lasertrainMaxZ']>laserTrainThresh)]

thalamQNonID = thalNonID['Q10']
cortamQNonID = cortNonID['Q10']

thalamQID = thalID['Q10']
cortamQID = cortID['Q10']

# Dependence of mean FR on AM rate

plt.clf()
stdev = 0.05
markersize = 8
linewidth = 2

plt.plot(np.random.normal(1, stdev, len(thalamQNonID.dropna())),
         1/thalamQNonID.dropna(), 'o', ms=markersize,
         markeredgecolor=colorpalette.TangoPalette['Orange2'],
         markerfacecolor='None',
         markeredgewidth = linewidth)

plt.plot(np.random.normal(1, stdev, len(thalamQID.dropna())),
         1/thalamQID.dropna(), 'o', ms=markersize,
         markeredgecolor=colorpalette.TangoPalette['Orange2'],
         markerfacecolor=colorpalette.TangoPalette['Orange2'],
         markeredgewidth=linewidth)

plt.hold(True)

plt.plot(np.random.normal(2, stdev, len(cortamQNonID.dropna())),
         1/cortamQNonID.dropna(), 'o', ms=markersize,
         markeredgecolor=colorpalette.TangoPalette['Plum2'],
         markerfacecolor='None',
         markeredgewidth=linewidth)

plt.plot(np.random.normal(2, stdev, len(cortamQID.dropna())),
         1/cortamQID.dropna(), 'o', ms=markersize,
         markeredgecolor=colorpalette.TangoPalette['Plum2'],
         markerfacecolor=colorpalette.TangoPalette['Plum2'],
         markeredgewidth=linewidth)

plt.xlim([0.5, 2.5])

ax = plt.gca()
ax.set_xticks([1, 2])
ax.set_ylim([0, 1.4])

ax.set_xticklabels(['Thalamus', 'Cortex'])
plt.ylabel('BW10')
plt.show()
