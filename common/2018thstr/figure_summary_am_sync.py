import os
from jaratoolbox import settings
from jaratoolbox import extraplots
from matplotlib import pyplot as plt
from collections import Counter
from jaratoolbox import colorpalette
import numpy as np
import pandas as pd
import figparams

STUDY_NAME = '2018thstr'
dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
db = pd.read_hdf(dbPath, key='dataframe')

soundResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')

plotOnlyIdentified = True

if plotOnlyIdentified:
    soundLaserResponsive = soundResponsive.query('pulsePval<0.05 and trainRatio>0.8')
    thal1 = soundLaserResponsive.groupby('brainarea').get_group('rightThal')
    thal2 = soundLaserResponsive.groupby('brainarea').get_group('rightThalamus')
    thal = pd.concat([thal1, thal2])
    ac = soundLaserResponsive.groupby('brainarea').get_group('rightAC')
else:
    thal1 = soundResponsive.groupby('brainarea').get_group('rightThal')
    thal2 = soundResponsive.groupby('brainarea').get_group('rightThalamus')
    thal = pd.concat([thal1, thal2])
    ac = soundResponsive.groupby('brainarea').get_group('rightAC')

astrR = soundResponsive.groupby('brainarea').get_group('rightAstr')
astrL = soundResponsive.groupby('brainarea').get_group('rightAstr')
astr = pd.concat([astrR, astrL])

lowFreq = 4
highFreq = 128
nFreqs = 11
freqs = np.logspace(np.log10(lowFreq),np.log10(highFreq),nFreqs)
freqs = np.round(freqs, decimals=1)
freqs = np.r_[0, freqs]

feature = 'highestSync'

tdata = np.round(thal[feature][pd.notnull(thal[feature])], decimals=1)
tCount = Counter(tdata)
tHeights = [100*tCount[freq]/np.double(len(tdata)) for freq in freqs]

acdata = np.round(ac[feature][pd.notnull(ac[feature])], decimals=1)
acCount = Counter(acdata)
acHeights = [100*acCount[freq]/np.double(len(acdata)) for freq in freqs]

astrdata = np.round(astr[feature][pd.notnull(astr[feature])], decimals=1)
astrCount = Counter(astrdata)
astrHeights = [100*astrCount[freq]/np.double(len(astrdata)) for freq in freqs]

index = np.arange(len(freqs))

bar_width=0.35
plt.clf()
fig = plt.gcf()
# fig.set_size_inches(10.5, 3.7)
linewidth=2
fontsize=20

ax = plt.subplot(311)
rects11 = plt.bar(index+0.5*bar_width,
                tHeights,
                bar_width,
                label='Thalamus',
                facecolor='w',
                edgecolor=colorpalette.TangoPalette['Chameleon3'],
                linewidth = linewidth)
plt.xticks(index + bar_width, freqs)
plt.ylabel('% cells')
plt.title('Thalamus, N={}'.format(len(tdata)))

ax = plt.subplot(312)
rects11 = plt.bar(index+0.5*bar_width,
                acHeights,
                bar_width,
                label='AC',
                facecolor='w',
                edgecolor=colorpalette.TangoPalette['ScarletRed2'],
                linewidth = linewidth)
plt.xticks(index + bar_width, freqs)
plt.ylabel('% cells')
plt.title('AC, N={}'.format(len(acdata)))

ax = plt.subplot(313)
rects11 = plt.bar(index+0.5*bar_width,
                astrHeights,
                bar_width,
                label='AC',
                facecolor='w',
                edgecolor=colorpalette.TangoPalette['SkyBlue2'],
                linewidth = linewidth)
plt.xticks(index + bar_width, freqs)
plt.xlabel('Highest AM rate to which cell could sync')
plt.ylabel('% cells')
plt.title('AStr, N={}'.format(len(astrdata)))

plt.show()
