'''
Example for loading behavior data and calculating psychometric curve.
Santiago Jaramillo (2018-09-24)
'''

import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

#subject = 'adap012'
#session = '20160219a'

#subject = 'adap012'
#session = '20160214a'

subject = 'adap013'
#session = '20160404a' # 0331
session = '20160331a'
paradigm = '2afc'

behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
#behavFile = './adap012_2afc_20160219a.h5'
bdata = loadbehavior.BehaviorData(behavFile)

choice = bdata['choice']
choiceRight = (choice==bdata.labels['choice']['right'])
targetFrequency = bdata['targetFrequency']
valid = bdata['valid'] & (choice!=bdata.labels['choice']['none'])

(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(choiceRight,targetFrequency,valid)

plt.clf()
(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(possibleValues,fractionHitsEachValue,ciHitsEachValue)

plt.ylabel('Rightward trials (%)')
plt.xlabel('Frequency (Hz)')
plt.title('{0} [{1}]'.format(subject,session))
plt.show()
