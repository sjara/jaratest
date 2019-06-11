from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots
import numpy as np
import matplotlib.pyplot as plt 
from statsmodels.stats.proportion import proportion_confint
from jaratoolbox import settings 
import sys

#subject = 'bili001'
#sessions = ['20181103a','20181029a','20181030a','20181031a','20181101a','20181102a']
#paradigm = '2afc'

#subject = 'bili005'
#sessions = ['20181103a','20181029a','20181030a','20181031a','20181101a','20181102a']
#paradigm = '2afc'

#subject = 'bili002'
#sessions = ['20180916a','20180918a','20180919a','20180920a','20180921a']
#paradigm = '2afc'


#subject = 'bili004'
#sessions = ['20181105a','20181106a']
#paradigm = '2afc'

#subject = 'bili006'
#sessions = ['20181025a','20181026a','20181027a','20181028a','20181029a','20181030a','20181031a','20181101a','20181102a']
#paradigm = '2afc'

#subject = 'bili007'
#sessions = ['20181024a','20181025a','20181026','20181027a','20181028a']
#paradigm = '2afc'

bdata = behavioranalysis.load_many_sessions(subject,sessions,paradigm)
Color = [0,0.50,1]
correct = bdata['outcome']==bdata.labels['outcome']['correct']
targetPercentage = bdata['targetFrequency'] 
choiceRight = bdata['choice']==bdata.labels['choice']['right']
valid = bdata['valid'].astype(bool) & (bdata['choice']!=bdata.labels['choice']['none'])
(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
       behavioranalysis.calculate_psychometric(choiceRight,targetPercentage,valid)
(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                               ciHitsEachValue,xTickPeriod=1, xscale='linear')
plt.setp([pline,pcaps,pbars,pdots],color=Color)
plt.setp(pdots,mfc=Color)

#Graphs for ba/da
#plt.text(-0.01, -8.5, r'$ 1.0 /ba/ $')
#plt.text(0.015, -8.5, r'$ 0.8 /ba/$')
#plt.text(0.035, -8.5, r'$ 0.6 /ba/$')
#plt.text(0.05, -8.5, r'$ 0.6 /da/ $')
#plt.text(0.075, -8.5, r'$ 0.8 /da/ $')
#plt.text(0.1, -8.5, r'$ 1.0 /da/ $')
#fractionCorrect = np.mean(correct[valid])

#if youre looking at a different week or set of days, these will print the amt correct and valid, so you can change the statements in the individual's data- example line 62 and 63
print ('Correct: ({})={:0.1%}'.format(valid,fractionCorrect))
print bdata  ['nValid']
fontsize = 12

#bili005 graph - ba/da
#plt.title('Bili005 Spectral Trials October 29, 2018 to November 3,2018')
#plt.xlabel('Stimulus',fontsize=fontsize)
#plt.ylabel('Rightward trials (%)',fontsize=fontsize)
#plt.text(0.035, 10, r'$ 85.3\ Percent\ of\ Trials\ Performed\ Correctly $')
#plt.text(0.035, 5, r'$ Average\ number\ of\ Trials\ Performed\ = 605 $')

#bili001 graph - ba/da
#plt.title('Bili001 Spectral Trials October 29, 2018 to November 3,2018')
#plt.xlabel('Stimulus',fontsize=fontsize)
#plt.ylabel('Rightward trials (%)',fontsize=fontsize)
#plt.text(0.035, 10, r'$ 80.3\ Percent\ of\ Trials\ Performed\ Correctly $')
#plt.text(0.035, 5, r'$ Average\ number\ of\ Trials\ Performed\ = 883 $')

#bili007 graph - ba/da
#plt.title('Bili007 Spectral Trials October 24, 2018 to October 28,2018' )
#plt.xlabel('Stimulus',fontsize=fontsize)
#plt.ylabel('Rightward trials (%)',fontsize=fontsize)
#plt.text(0.035, 10, r'$ 82.8\ Percent\ of\ Trials\ Performed\ Correctly $')
#plt.text(0.035, 5, r'$ Average\ number\ of\ Trials\ Performed\ = 1209 $')

#Graphs for ba/pa
#plt.text(-0.01, -8.5, r'$ 1.0 /ba/ $')
#plt.text(0.015, -8.5, r'$ 0.8 /ba/$')
#plt.text(0.035, -8.5, r'$ 0.6 /ba/$')
#plt.text(0.05, -8.5, r'$ 0.6 /pa/ $')
#plt.text(0.075, -8.5, r'$ 0.8 /pa/ $')
#plt.text(0.1, -8.5, r'$ 1.0 /pa/ $')

#bili004 graph ba/pa
#plt.title('Bili004 Temporal Trials November 5, 2018 to November 6, 2018')
#plt.xlabel('Stimulus',fontsize=fontsize)
#plt.ylabel('Rightward trials (%)',fontsize=fontsize)
#plt.text(0.035, 10, r'$ 79.8\ Percent\ of\ Trials\ Performed\ Correctly $')
#plt.text(0.035, 5, r'$ Average\ number\ of\ Trials\ Performed\ = 896$')

#bili002 graph ba/pa
#plt.title('Bili002 Temporal Trials October 16, 2018 to October 21,2018')
#plt.xlabel('Stimulus',fontsize=fontsize)
#plt.ylabel('Rightward trials (%)',fontsize=fontsize)
#plt.text(0.035, 10, r'$ 81.7\ Percent\ of\ Trials\ Performed\ Correctly $')
#plt.text(0.035, 5, r'$ Average\ number\ of\ Trials\ Performed\ = 644 $')


plt.show()
### STOP HERE ###
sys.exit()

