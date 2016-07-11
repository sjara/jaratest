'''
Show psychometric curves for cued data.
'''

from jaratoolbox import behavioranalysis
from pylab import *
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
import sys

animalName = 'cued004'

sessions = ['20150618a','20150619a','20150620a','20150621a','20150622a','20150623a','20150624a']
sessions = ['20150621a','20150623a','20150624a']

'''
if len(sys.argv)>1:
    session = sys.argv[1]+'a'
else:
    session = '20150624a'
'''

#fname = loadbehavior.path_to_behavior_data(animalName,'santiago','2afc',session)
#bdata=loadbehavior.BehaviorData(fname)
bdata = behavioranalysis.load_many_sessions(animalName,sessions)

nReward = bdata['nRewarded'][-1]
nValid = bdata['nValid'][-1]
fractionCorrect = nReward/float(nValid)

targetFrequency = bdata['targetFrequency']
possibleTarget = unique(targetFrequency)
cueFrequency = bdata['cueFrequency']
possibleCue = unique(cueFrequency)

trialsEachCue = behavioranalysis.find_trials_each_type(cueFrequency,possibleCue)
choiceRight = bdata['choice']==(bdata.labels['choice']['right'])


colorEachCond = ['g','r']
clf()
hold(True)
for indcue,cueFreq in enumerate(possibleCue):
    (possibleValues,fractionHitsEachValue,ciHitsEachValue,
     nTrialsEachValue,nHitsEachValue)=\
       behavioranalysis.calculate_psychometric(choiceRight,
                                               targetFrequency,
                                               trialsEachCue[:,indcue])
    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(possibleValues,
                                                                fractionHitsEachValue,
                                                                ciHitsEachValue)
    setp([pline,pcaps,pbars],color=colorEachCond[indcue])
    setp(pdots,mec=colorEachCond[indcue],mfc=colorEachCond[indcue])
xlabel('Target frequency')
ylabel('% rightward')
show()


