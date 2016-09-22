'''
Psychometric curves during photoinactivation.
'''

import numpy as np
#from jaratoolbox import extrastats
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt

subject = 'adap031'
session = '20160916a'

behavFile = loadbehavior.path_to_behavior_data(subject,'2afc',session)
bdata = loadbehavior.BehaviorData(behavFile)

targetFrequency = bdata['targetFrequency']
choice = bdata['choice']
valid = bdata['valid'] & (choice!=bdata.labels['choice']['none'])
choiceRight = (choice==bdata.labels['choice']['right'])
laserTrials = (bdata['trialType']==bdata.labels['trialType']['laser_left'])

validControl = valid & ~laserTrials
validLaser = valid & laserTrials

# -- Calculate and plot psychometric points --
(possibleValuesControl,fractionHitsEachValueControl,ciHitsEachValueControl,
    nTrialsEachValueControl,nHitsEachValueControl)=\
        behavioranalysis.calculate_psychometric(choiceRight,targetFrequency,validControl)
(possibleValuesLaser,fractionHitsEachValueLaser,ciHitsEachValueLaser,
    nTrialsEachValueLaser,nHitsEachValueLaser)=\
        behavioranalysis.calculate_psychometric(choiceRight,targetFrequency,validLaser)

plt.clf()
plt.hold(True)
(plineC, pcapsC, pbarsC, pdotsC) = extraplots.plot_psychometric(possibleValuesControl,
                                                            fractionHitsEachValueControl,
                                                            ciHitsEachValueControl)
(plineL, pcapsL, pbarsL, pdotsL) = extraplots.plot_psychometric(possibleValuesLaser,
                                                            fractionHitsEachValueLaser,
                                                            ciHitsEachValueLaser)
plt.setp([plineL,pcapsL,pbarsL],color='g')
plt.setp(pdotsL,mfc='g',mec='g')

plt.hold(False)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Rightward choice (%)')
plt.title('{0} - {1}'.format(subject,session))
plt.legend([plineC,plineL],['Control','Laser'],loc='upper left')
plt.show()
