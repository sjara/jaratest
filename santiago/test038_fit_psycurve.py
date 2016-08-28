'''
Fitting psychometric curve.

The current version plots the psychometric in log(Hz)
'''

import numpy as np
from jaratoolbox import extrastats
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt

subject = 'adap031'
session = '20160824a'

behavFile = loadbehavior.path_to_behavior_data(subject,'2afc',session)
bdata = loadbehavior.BehaviorData(behavFile)

targetFrequency=bdata['targetFrequency']
choice=bdata['choice']
valid=bdata['valid'] & (choice!=bdata.labels['choice']['none'])
choiceRight = choice==bdata.labels['choice']['right']

# -- Calculate and plot psychometric points --
(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
    behavioranalysis.calculate_psychometric(choiceRight,targetFrequency,valid)

logPossibleValues = np.log2(possibleValues)

plt.clf()
#(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(possibleValues,fractionHitsEachValue,ciHitsEachValue)
#plt.setp(pdots,ms=6,mec='k',mew=2,mfc='k')
plt.plot(logPossibleValues,fractionHitsEachValue,'o')
plt.xlabel('Frequency (log2(Hz))')
plt.ylabel('Rightward choice (%)')

plt.show()


# -- Calculate and plot psychometric fit --
#constraints = None
constraints = ['Uniform(10,15)', 'Uniform(0,5)' ,'Uniform(0,1)', 'Uniform(0,1)']
curveParams = extrastats.psychometric_fit(logPossibleValues, nTrialsEachValue,
                                          nHitsEachValue, constraints)

print 'Psychometric parameters (bias, slope, upper, lower):'
print curveParams

plt.hold(True)

xValues = logPossibleValues
xRange = xValues[-1]-xValues[1]
fitxval = np.linspace(xValues[0]-0.1*xRange,xValues[-1]+0.1*xRange,40)
fityval = extrastats.psychfun(fitxval,*curveParams)
hfit = plt.plot(fitxval,fityval,'-',linewidth=2,color='k')

#(hp,hfit) = extraplots.plot_psychometric_fit(possibleValues,nTrialsEachValue,
#                                           nHitsEachValue,curveParams)

plt.hold(False)

plt.draw()
