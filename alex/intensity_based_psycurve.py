import sys
# from jaratest.nick import behavioranalysis_vnick as behavioranalysis
from jaratoolbox import behavioranalysis
reload(behavioranalysis)
import numpy as np
from jaratoolbox import extraplots
from matplotlib import pyplot as plt

fontsize = 12
colors = ['k', 'b', 'g', 'r', 'y']

#subjects = ['gosi002', 'gosi006']
subjects = ['gosi013', 'adap051']
#subjects = ['amod011', 'amod012', 'amod013']
# sessions = ['20160711a', '20160712a', '20160713a', '20160714a', '20160715a', '20160716a', '20160718a','20160719a', '20160720a', '20160721a', '20160722a']
#sessions = ['20170504a']
#sessions = ['20170510a']
sessions = ['20170608a']

if len(sys.argv)>1:
    sessions = sys.argv[1:]
    #sessions = input("Enter sessions (in a list of strings ['','']) to check behavior performance:")
plt.figure()
for indSubject, subject in enumerate(subjects):
	for indSession, session in enumerate(sessions):	
		plt.subplot(len(subjects), 1, indSubject+1)
		bdata = behavioranalysis.load_many_sessions(subject, [session])

		targetIntensity = bdata['targetIntensity']
		valid = bdata['valid']
		choice = bdata['choice']

		#Is this the correct thing to get to calculate psychometrics?
		choiceRight = choice==bdata.labels['choice']['right']
		targetFreq = bdata['targetFrequency']

		possibleInt = np.unique(targetIntensity)
		trialsEachInt = behavioranalysis.find_trials_each_type(targetIntensity,possibleInt)

		trialsInds = {}
		allPlines = []
		for indInt, inten in enumerate(possibleInt):
			trialsInds[inten] = valid&(bdata['targetIntensity']==inten)
			(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
			behavioranalysis.calculate_psychometric(choiceRight, targetFreq, trialsInds[inten])

			(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,ciHitsEachValue,xTickPeriod=1)

			allPlines.append(pline)

			plt.title(subject+' - '+session, fontsize=fontsize)
			plt.xlabel('Frequency (kHz)',fontsize=fontsize)
			plt.ylabel('Rightward trials (%)',fontsize=fontsize)
			extraplots.set_ticks_fontsize(plt.gca(),fontsize)
			plt.setp(pline, color=colors[indInt])
			plt.setp(pcaps, color=colors[indInt])
			plt.setp(pbars, color=colors[indInt])
			plt.setp(pdots, markerfacecolor=colors[indInt])
			legend = plt.legend(allPlines, possibleInt)

		


plt.show()
 


#behavioranalysis.behavior_summary(subjects,sessions,trialslim=[0,1000],outputDir='/home/nick/data/behavior_reports')

