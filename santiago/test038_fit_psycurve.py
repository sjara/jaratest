'''
Fitting psychometric curve.
'''

from jaratoolbox import extrastats
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt

subject = 'adap034'
session = '20160824a'

behavFile = loadbehavior.path_to_behavior_data(subject,'2afc',session)
bdata = loadbehavior.BehaviorData(behavFile)

targetFrequency=bdata['targetFrequency']
choice=bdata['choice']
valid=bdata['valid'] & (choice!=bdata.labels['choice']['none'])
choiceRight = choice==bdata.labels['choice']['right']

#possibleFreq = np.unique(targetFrequency)
#nFreq = len(possibleFreq) 
#trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency,possibleFreq)

# -- Calculate and plot psychometric points --
(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
    behavioranalysis.calculate_psychometric(choiceRight,targetFrequency,valid)

plt.clf()
(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(possibleValues,fractionHitsEachValue,ciHitsEachValue)
plt.setp(pdots,ms=6,mec='k',mew=2,mfc='k')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Rightward choice (%)')

plt.show()

# -- Calculate and plot psychometric fit --
constraints = None
constraints = ['flat', 'Uniform(0,0.3)' ,'Uniform(0,0.2)', 'Uniform(0,0.2)', constraints]
curveParams = extrastats.psychometric_fit(possibleValues,nTrialsEachValue, nHitsEachValue)

plt.hold(True)
(hp,hfit) = extraplots.plot_psychometric_fit(possibleValues,nTrialsEachValue,
                                           nHitsEachValue,curveParams)
plt.hold(False)

plt.draw()
