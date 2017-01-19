from matplotlib import pyplot as plt
from collections import Counter
from jaratest.nick.stats import am_funcs
reload(am_funcs)
import pandas
import numpy as np
from jaratoolbox import colorpalette
from jaratoolbox import extraplots
import matplotlib
matplotlib.rcParams['svg.fonttype'] = 'none'
import matplotlib.pyplot as plt
# import seaborn


thaldbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb_q10.pickle'
cortdbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb_q10.pickle'
thaldb = pandas.read_pickle(thaldbfn)
cortdb = pandas.read_pickle(cortdbfn)

laserTrainThresh = 1.5
noiseBurstThresh = 2
isiThresh = 4

thalNonID = thaldb[(thaldb['isiViolations']<isiThresh) & (thaldb['noiseburstZ']>noiseBurstThresh) & (thaldb['lasertrainZ']<laserTrainThresh)]
cortNonID = cortdb[(cortdb['isiViolations']<isiThresh) & (cortdb['noiseburstZ']>noiseBurstThresh) & (cortdb['lasertrainZ']<laserTrainThresh)]

thalID = thaldb[(thaldb['isiViolations']<isiThresh) & (thaldb['noiseburstZ']>noiseBurstThresh) & (thaldb['lasertrainZ']>laserTrainThresh)]
cortID = cortdb[(cortdb['isiViolations']<isiThresh) & (cortdb['noiseburstZ']>noiseBurstThresh) & (cortdb['lasertrainZ']>laserTrainThresh)]

thalamHSNonID = thalNonID['highestSync']
cortamHSNonID = cortNonID['highestSync']

thalamHSID = thalID['highestSync']
cortamHSID = cortID['highestSync']



# Percentage of neurons that sync to the freqs we tested
lowFreq = 4
highFreq = 128
nFreqs = 11
freqs = np.logspace(np.log10(lowFreq),np.log10(highFreq),nFreqs)
freqs = np.round(freqs, decimals=1)
freqs = np.r_[0, freqs]

thalHighestNonID = np.round(thalamHSNonID.dropna(), decimals=1)
thalHighestID = np.round(thalamHSID.dropna(), decimals=1)
nThal = len(thalHighestNonID) + len(thalHighestID)

cortHighestNonID = np.round(cortamHSNonID.dropna(), decimals=1)
cortHighestID = np.round(cortamHSID.dropna(), decimals=1)
nCort = len(cortHighestNonID) + len(cortHighestID)

thalCounterNonID = Counter(thalHighestNonID)
thalCounterID = Counter(thalHighestID)

cortCounterNonID = Counter(cortHighestNonID)
cortCounterID = Counter(cortHighestID)

thalcountsNonID = [100*thalCounterNonID[freq]/np.double(nThal) for freq in freqs]
thalcountsID = [100*thalCounterID[freq]/np.double(nThal) for freq in freqs]

cortcountsNonID = [100*cortCounterNonID[freq]/np.double(nCort) for freq in freqs]
cortcountsID = [100*cortCounterID[freq]/np.double(nCort) for freq in freqs]

index = np.arange(len(freqs))
bar_width=0.35
plt.clf()
fig = plt.gcf()
fig.set_size_inches(10.5, 3.7)
linewidth=2
fontsize=20

rects11 = plt.bar(index,
                  thalcountsID,
                  bar_width,
                  label='Tagged thalamo-striatal',
                  facecolor=colorpalette.TangoPalette['Orange2'],
                  edgecolor=colorpalette.TangoPalette['Orange2'],
                  linewidth = linewidth)

rects12 = plt.bar(index,
                  thalcountsNonID,
                  bar_width,
                  label='Thalamus, non-tagged',
                  facecolor='w',
                  edgecolor=colorpalette.TangoPalette['Orange2'],
                  bottom=thalcountsID,
                  linewidth=linewidth)

rects21 = plt.bar(index+bar_width+0.04,
                  cortcountsID,
                  bar_width,
                  label='Tagged cortico-striatal',
                  facecolor=colorpalette.TangoPalette['Plum2'],
                  edgecolor=colorpalette.TangoPalette['Plum2'],
                  linewidth=linewidth)

rects22 = plt.bar(index+bar_width+0.04,
                  cortcountsNonID,
                  bar_width,
                  label='Cortex, non-tagged',
                  facecolor='w',
                  edgecolor=colorpalette.TangoPalette['Plum2'],
                  bottom=cortcountsID,
                  linewidth=linewidth)

plt.xlabel('Maximum AM rate to which responses\nwere synchronized (Hz)', fontsize=fontsize)
plt.ylabel('% Neurons', fontsize=fontsize)
# plt.title('Scores by group and gender')
plt.xticks(index + bar_width, freqs)
plt.legend(loc='upper left', prop={'size':15})
plt.tight_layout()
ax = plt.gca()
ax.set_yticks(np.linspace(0, 40, 5))
extraplots.set_ticks_fontsize(ax, fontsize)
extraplots.boxoff(ax)

plt.show()

# Dependence of mean FR on AM rate
# thalamR = thalCells['amRval']
# cortamR = cortCells['amRval']
# plt.clf()
# plt.plot(np.random.normal(1, 0.05, len(thalamR.dropna())), thalamR.dropna(), '.', ms=10)
# plt.hold(True)
# plt.plot(np.random.normal(3, 0.05, len(cortamR.dropna())), cortamR.dropna(), '.', ms=10)
# plt.xlim([0.5, 3.5])
# ax = plt.gca()
# ax.set_xticks([1, 3])
# ax.set_xticklabels(['Thalamus', 'Cortex'])
# plt.ylabel('Correlation coefficient between\nfiring rate and AM rate')
# plt.show()

### EXAMPLE NEURON HUNT
# corrCells = thalCells[np.abs(thalCells['amRval'])>0.5]
# corrCells = cortCells[np.abs(cortCells['amRval'])>0.5]

# for indCell, cell in corrCells.iterrows():
#     plt.clf()
#     try:
#         sessiontypeIndex = cell['sessiontype'].index('AM')
#     except ValueError: #The cell does not have this session type
#         continue
#     print indCell
#     # r_val, frArray = am_funcs.am_dependence(cell, frArray=True)
#     # plt.plot(frArray)
#     # plt.waitforbuttonpress()
#     plt.subplot(3, 1, 1)
#     am_funcs.plot_am_raster(cell)
#     plt.subplot(3, 1, 2)
#     am_funcs.plot_am_psth(cell)
#     plt.subplot(3, 1, 3)
#     r_val, frArray, possibleFreq = am_funcs.am_dependence(cell, frArray=True)
#     plt.plot(frArray)
#     ax = plt.gca()
#     ax.set_xticks(np.arange(len(possibleFreq)))
#     ax.set_xticklabels(np.round(possibleFreq, decimals=1))
#     plt.xlabel(r_val)
#     plt.waitforbuttonpress()
