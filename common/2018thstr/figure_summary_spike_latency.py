import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from jaratoolbox.colorpalette import TangoPalette
from jaratoolbox import extraplots
import pandas

STUDY_NAME = '2018thstr'
dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
db = pandas.read_hdf(dbPath, key='dataframe')

soundResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05 and noiseZscore>0')
thal1 = soundResponsive.groupby('brainarea').get_group('rightThal')
thal2 = soundResponsive.groupby('brainarea').get_group('rightThalamus')
thal = pandas.concat([thal1, thal2])
ac = soundResponsive.groupby('brainarea').get_group('rightAC')
astrR = soundResponsive.groupby('brainarea').get_group('rightAstr')
astrL = soundResponsive.groupby('brainarea').get_group('rightAstr')
astr = pandas.concat([astrR, astrL])

tlat = thal['medianFSLatency'][pandas.notnull(thal['medianFSLatency'])]
aclat = ac['medianFSLatency'][pandas.notnull(ac['medianFSLatency'])]
astrlat = astr['medianFSLatency'][pandas.notnull(astr['medianFSLatency'])]

plt.clf()

# plt.hist(tlat, histtype='step', color='g', normed=1)
# plt.hold(1)
# plt.hist(aclat, histtype='step', color='r', normed=1)
# plt.hist(astrlat, histtype='step', color='b', normed=1)
bins=10
thalcolor = TangoPalette['Chameleon3']
accolor = TangoPalette['ScarletRed2']
astrcolor = TangoPalette['SkyBlue2']
fontsize=15

ax = plt.subplot(311)
plt.hist(tlat, histtype='step', bins=bins, color=thalcolor, weights=np.zeros_like(tlat) + 1. / tlat.size, lw=2)
# ax.set_ylim([0, 0.25])
plt.xlim([0, 0.1])
ax.set_xticklabels([0, 20, 40, 60, 80, 100])
ax.set_yticks([0, 0.25])
ax.set_yticklabels([0, 25])
extraplots.boxoff(ax)
extraplots.set_ticks_fontsize(ax, fontsize)

ax = plt.subplot(312)
plt.hist(aclat, histtype='step', bins=bins, color=accolor, weights=np.zeros_like(aclat) + 1. / aclat.size, lw=2)
# ax.set_ylim([0, 0.25])
plt.xlim([0, 0.1])
ax.set_xticklabels([0, 20, 40, 60, 80, 100])
ax.set_yticks([0, 0.25])
ax.set_yticklabels([0, 25])
extraplots.boxoff(ax)
extraplots.set_ticks_fontsize(ax, fontsize)

ax = plt.subplot(313)
plt.hist(astrlat, histtype='step', bins=bins, color=astrcolor, weights=np.zeros_like(astrlat) + 1. / astrlat.size, lw=2)
# ax.set_ylim([0, 0.25])
plt.xlim([0, 0.1])
ax.set_xticklabels([0, 20, 40, 60, 80, 100])
ax.set_yticks([0, 0.25])
ax.set_yticklabels([0, 25])
extraplots.boxoff(ax)
extraplots.set_ticks_fontsize(ax, fontsize)

plt.show()
