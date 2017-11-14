'''
For Daily Behavior Monitoring.
Loads behavior data from mounted jarahub/data/behavior for animals of interest, plot psychometric curve and dynamics data.
'''
import sys
# from jaratest.nick import behavioranalysis_vnick as behavioranalysis
from jaratoolbox import behavioranalysis
reload(behavioranalysis)
import numpy as np
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
from matplotlib import pyplot as plt

fontsize = 18
#fontsize = 24
colors = ['k', 'b', 'g', 'r', 'y']

# subjects = ['amod001', 'amod002', 'amod003', 'amod004', 'amod005']
# subjects = ['adap026', 'adap027', 'adap028', 'adap029', 'adap030', ]
# subjects = ['adap021', 'adap022', 'adap023', 'adap024', 'adap025' ]
# subjects = ['adap022', 'adap026', 'adap027', 'adap030'] #New muscimol animals
# subjects = ['adap025', 'adap028', 'adap029']

subjects = ['amod012']
#subjects = ['amod013']
#subjects = ['amod012', 'amod013']
# sessions = ['20160711a', '20160712a', '20160713a', '20160714a', '20160715a', '20160716a', '20160718a','20160719a', '20160720a', '20160721a', '20160722a']
#sessions = ['20170504a']
'''
#amod012 sessions
sessions = ['20170506a', #laser days
			'20170507a', 
			'20170508a', 
			'20170509a', 
			'20170510a', 
			'20170511a', 
			'20170512a',
			'20170513a'
			]

sessions = ['20170514a', #laser control (taped to tether) days
			'20170515a',
			'20170516a',
			'20170517a',
			'20170518a'
			]

#Repeat laser sessions (bilateral stimulation)

sessions = ['20170525a',
			'20170526a',
			'20170527a',
			'20170528a'
			]

#New laser controls
sessions = ['20170529a',
			'20170530a',
			'20170531a',
			'20170601a'
			]

'''


#amod013 sessions
'''
#Laser sessions
sessions = ['20170512a',
			'20170513a', 
			'20170514a', 
			'20170515a',
			'20170516a',
			'20170517a',
			'20170518a'
			]

#Laser control sessions
sessions = ['20170519a',
			'20170520a', 
			'20170521a', 
            '20170522a',
            '20170523a',
			]

#Extra laser controls (taped to sides of box, pointing back)
sessions = ['20170524a',
			'20170525a',
			'20170526a',
			'20170527a'
			]

#Repeat laser sessions (bilateral stimulation)
sessions = ['20170528a',
			'20170529a',
			'20170530a',
			'20170531a',
			'20170601a'
			]

sessions = ['20170603a',
			'20170604a',
			'20170605a',]
'''

#sessions = ['20170607a', '20170609a', '20170615a', '20170616a'] #Laser sessions
#sessions = ['20170608a', '20170617a', '20170619a', '20170620a'] #amod012 laser controls
#sessions = ['20170608a', '20170617a', '20170619a', '20170621a'] #amod013 laser controls
#sessions = ['20170610a', '20170611a', '20170613a', '20170614a'] #extreme controls
#sessions = ['20170622a'] #0.5 mW, lasers in
#sessions = ['20170623a'] #0.5 mW, lasers on side
#sessions = ['20170624a'] #0.25 mW, lasers in
#sessions = ['20170626a', '20170627a'] #0.25 mW, lasers on side
#sessions = ['20170628a'] #0.1 mW, lasers in
#sessions = ['20170629a'] #0.1 mW, lasers on side
sessions = ['20170630a'] #for amod012: I:0.3, II:2.0; for amod013, I:0.3, II:1.5, lasers on side

if len(sys.argv)>1:
    sessions = sys.argv[1:]
    #sessions = input("Enter sessions (in a list of strings ['','']) to check behavior performance:")
#plt.figure()
inds = 0
plt.figure()
for indSubject, subject in enumerate(subjects):
	#plt.subplot(len(subjects), 1, indSubject+1)
	allPlines = []
	bdata = behavioranalysis.load_many_sessions(subjects, sessions, 'simple2afc')
	'''
	for indSession, session in enumerate(sessions):	
		behavFile = loadbehavior.path_to_behavior_data(subject,'2afc',session)
		behavData = loadbehavior.BehaviorData(behavFile)
		#bdata = behavioranalysis.load_many_sessions(subject, [session])
		
		#copied from load_many_sessions
		if inds==0:
				allBehavData = behavData  # FIXME: Should it be .copy()?
				nTrials = len(behavData['outcome']) # FIXME: what if this key does not exist?
				allBehavData['sessionID'] = np.zeros(nTrials,dtype='i2')
				allBehavData['animalID'] = np.zeros(nTrials,dtype='i1')
		else:
				for key,val in behavData.iteritems():
					if not allBehavData.has_key(key):
						allBehavData[key]=val
					else:
						allBehavData[key] = np.concatenate((allBehavData[key],val))
				nTrials = len(behavData['outcome']) # FIXME: what if this key does not exist?
				allBehavData['sessionID'] = np.concatenate((allBehavData['sessionID'],
					np.tile(inds,nTrials)))
				allBehavData['animalID'] = np.concatenate((allBehavData['animalID'],
					np.tile(indSubject,nTrials)))
				inds += 1
	bdata = allBehavData
	'''
	valid = bdata['valid']
	choice = bdata['choice']

	print sum(valid)

	#Is this the correct thing to get to calculate psychometrics?
	choiceRight = choice==bdata.labels['choice']['right']
	targetFreq = bdata['targetFrequency']

	noLaserTrials = valid&(bdata['trialType']==0)

	(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
	behavioranalysis.calculate_psychometric(choiceRight, targetFreq, noLaserTrials)

	(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,ciHitsEachValue,xTickPeriod=1)

	allPlines.append(pline)

	ax = pline.axes
	extraplots.boxoff(ax)
	extraplots.set_ticks_fontsize(ax, fontsize)

	#plt.title(subject+' - '+sessions[0]+'-'+sessions[-1], fontsize=fontsize)
	plt.xlabel('Frequency (kHz)',fontsize=fontsize)
	plt.ylabel('Rightward trials (%)',fontsize=fontsize)
	extraplots.set_ticks_fontsize(plt.gca(),fontsize)
	plt.setp(pline, color='k')
	plt.setp(pcaps, color='k')
	plt.setp(pbars, color='k')
	plt.setp(pdots, markerfacecolor='k')
	legend = plt.legend(allPlines, ['No Laser', 'Laser'])

	plt.hold(True)
	
	laserTrials = valid&(bdata['trialType']==1)
	(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
	behavioranalysis.calculate_psychometric(choiceRight, targetFreq, laserTrials)
	
	(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,ciHitsEachValue,xTickPeriod=1)

	allPlines.append(pline)

	ax = pline.axes
	extraplots.boxoff(ax)
	extraplots.set_ticks_fontsize(ax, fontsize)


	plt.title(subject+' - '+sessions[0]+'-'+sessions[-1], fontsize=fontsize)
	plt.xlabel('Frequency (kHz)',fontsize=fontsize)
	plt.ylabel('Rightward trials (%)',fontsize=fontsize)
	extraplots.set_ticks_fontsize(plt.gca(),fontsize)
	plt.setp(pline, color='b')
	plt.setp(pcaps, color='b')
	plt.setp(pbars, color='b')
	plt.setp(pdots, markerfacecolor='b')
	legend2 = plt.legend(allPlines, ['No Laser', 'Laser'], bbox_to_anchor=(0.35, 0.875),
           bbox_transform=plt.gcf().transFigure)
	
	ax.xaxis.set_ticks_position('bottom')	


plt.show()
 


#behavioranalysis.behavior_summary(subjects,sessions,trialslim=[0,1000],outputDir='/home/nick/data/behavior_reports')

