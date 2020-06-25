'''
Speech discrimination peformance examples (bili mice).

Dates were chose according to Erin: 
http://jarahub.uoregon.edu/wiki/Study:_Second_language_learning_in_mice#Reports
'''

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from jaratoolbox import behavioranalysis
#from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
from statsmodels.stats.proportion import proportion_confint #Used to compute confidence interval for the error bars. 
from jaratoolbox import settings 
import figparams

SAVE_FIGURE = 1
outputDir = '/tmp/'

figFilename = 'speech_discrim_spectral'
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [5,4]


'''
subjects = ['bili001','bili002','bili003','bili004','bili005','bili006','bili007']
session = '20180724a'
paradigm = '2afc'
'''

# Spectral bili007 from 2018-10-24 through 2018-10-28
# Temporal bili006 from 2018-10-26 through 2018-11-02

CASE = 0
if CASE==0:
    subject = 'bili007'
    sessions = ['20181024a','20181025a','20181027a','20181028a']
    taskLabel = 'spectral'
    #xLabel = 'Formant transition slope (Hz/oct)'
    xLabel = 'Formant transition slope (%)'
elif CASE==1:
    subject = 'bili006'
    sessions = ['20181027a','20181029a','20181030a','20181101a']
    taskLabel = 'temporal'
    xLabel = 'Voice Onset Time (ms)'
    
fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 1)
gs.update(left=0.15, right=0.97, top=0.9, bottom=0.15)

bdata = behavioranalysis.load_many_sessions(subject,sessions)

targetPercentage = bdata['targetFrequency'] # I used name 'frequency' initially
choiceRight = bdata['choice']==bdata.labels['choice']['right']
valid=bdata['valid']& (bdata['choice']!=bdata.labels['choice']['none'])
(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
       behavioranalysis.calculate_psychometric(choiceRight,targetPercentage,valid)

ax1 = plt.subplot(gs[0])
plt.title('{0} [{1}-{2}]'.format(subject,sessions[0],sessions[-1]))

(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(possibleValues,fractionHitsEachValue,
                                                            ciHitsEachValue, xscale='linear')

plotColor = [0,0.4,0.7]
plt.setp([pline,pcaps,pbars,pdots], color=plotColor)
plt.setp(pdots, mfc=plotColor, mec=plotColor)
ax1.set_xticks([0,25,50,75,100])
ax1.set_xticklabels(['-100','','0','','100'])
plt.xlabel(xLabel,fontsize=figparams.fontSizeLabels)
plt.ylabel('Rightward trials (%)',fontsize=figparams.fontSizeLabels)
extraplots.set_ticks_fontsize(plt.gca(),figparams.fontSizeTicks)

plt.show()


if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
