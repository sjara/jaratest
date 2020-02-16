"""
Plot summary of behavior effect in humans when comparing
active+active vs active+passive, etc
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import extraplots
from matplotlib import gridspec
import matplotlib
from scipy import stats

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # So font is selectable in SVG

np.random.seed(3)

dataFilename = './data_human_behavior.txt'

dframe = pd.read_csv(dataFilename, sep='\t')

dataBySchedule = dframe.groupby('Schedule')
#schedLabels = {'Act':'AA', 'AP':'AP', 'Pass':'PP', 'SA':'A_'}
schedMapping = {'Act':0, 'AP':1, 'Pass':2, 'SA':3}
schedSorted = ['AA', 'AP', 'PP', 'Ax'] # Because dicts don't always return keys sorted (pre Py3)
nSched = len(schedMapping)
#featureToPlot = 'Difference'
#featureToPlot = 'Day1pre'
featureToPlot = 'Day2post'


dataMedian = dataBySchedule.median()
#dataMedian = dataBySchedule.mean()
#day2median = dataMedian['Day2post']
#stest = stats.ranksums
stest = stats.mannwhitneyu

zstat,pval = stest(dataBySchedule.get_group('Act')[featureToPlot],
                   dataBySchedule.get_group('Pass')[featureToPlot])
print('p-value (AA-PP) = {}'.format(pval))
zstat,pval = stest(dataBySchedule.get_group('Act')[featureToPlot],
                   dataBySchedule.get_group('SA')[featureToPlot])
print('p-value (AA-Ax) = {}'.format(pval))
zstat,pval = stest(dataBySchedule.get_group('Act')[featureToPlot],
                   dataBySchedule.get_group('AP')[featureToPlot])
print('p-value (AA-AP) = {}'.format(pval))
zstat,pval = stest(dataBySchedule.get_group('AP')[featureToPlot],
                   dataBySchedule.get_group('Pass')[featureToPlot])
print('p-value (AP-PP) = {}'.format(pval))
zstat,pval = stest(dataBySchedule.get_group('AP')[featureToPlot],
                   dataBySchedule.get_group('SA')[featureToPlot])
print('p-value (AP-Ax) = {}'.format(pval))


plt.clf()
gs = gridspec.GridSpec(ncols=1, nrows=1, left=0.2)
ax0 = plt.gcf().add_subplot(gs[0])

labelsFontSize = 20
ticksFontSize = 14
pointsColor = '0.5'
barEdgeColor = '0.25'
barFaceColor = '0.85'

for schedName, schedData in dataBySchedule:
    nSamplesThisSched = len(schedData)
    xvals = np.tile(schedMapping[schedName],nSamplesThisSched) + 0.1*np.random.rand(nSamplesThisSched)
    plt.plot(xvals, schedData[featureToPlot], 'o', mfc='none', mec=pointsColor)
    thisMedian = dataMedian[featureToPlot][schedName]
    plt.bar(schedMapping[schedName],thisMedian, width=0.75, lw=2,
            fc=barFaceColor, ec=barEdgeColor)
            
#plt.ylabel(featureToPlot, fontsize=labelFontSize)
plt.ylabel('Performance (%)', fontsize=labelsFontSize)

ax0.set_xticks(np.arange(nSched))
ax0.set_xticklabels(schedSorted, fontsize=labelsFontSize)
if featureToPlot == 'Difference':
    plt.ylim([-20,50])
else:
    plt.ylim([50,100])
extraplots.boxoff(ax0)
extraplots.set_ticks_fontsize(ax0,ticksFontSize)

plt.show()
    
SAVEFIG = 1
if SAVEFIG:
    figname = 'behavior_effect_{}'.format(featureToPlot)
    extraplots.save_figure(figname, 'svg', [4.5, 3], facecolor='w', outputDir='/tmp/')

