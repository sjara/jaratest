
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint #Used to compute confidence interval for the error bars. 

#subjects = ['test065','test067','test068','test070']
#subjects = ['test064']
#session = '20141116a' #20141116-20141119
#session = '20141117a' #20141116-20141119
#animalNames = ['test064']
animalNames = ['test070']
sessions = ['20141116a','20141117a','20141118a','20141119a'] # Pre-lesion
#sessions = ['20141201a','20141202a','20141203a','20141204a'] # Post-lesion
#sessions = ['20141204a'] # Post-lesion


animalNames = ['test012']
animalNames = ['test020']
#sessions = ['20150110a'] # Pre-lesion
sessions = ['20150106a','20150108a','20150109a','20150110a'] # Pre-lesion
sessions = ['20150115a','20150116a','20150117a','20150118a'] # Post-lesion
#sessions = ['20150119a'] # Post-lesion


clf()
for ind, subject in enumerate(animalNames):#enumerate(subjects):
    #fname=loadbehavior.path_to_behavior_data(subject,'santiago','2afc',session)

    try:
        #bdata=loadbehavior.BehaviorData(fname)
        bdata = behavioranalysis.load_many_sessions(animalNames,sessions)
    except IOError:
        continue
    from jaratoolbox import settings 

    targetFrequency=bdata['targetFrequency']
    valid=bdata['valid']
    choice=bdata['choice']
    intensities=bdata['targetIntensity']
    choiceRight = choice==bdata.labels['choice']['right'] ########## FIX ME : HARDCODED!


    possibleFreq = np.unique(targetFrequency)
    nFreq = len(possibleFreq) 
    fractionRightEachFreq=np.zeros(nFreq)
    confLimitsEachFreq=np.zeros([2, nFreq]) #Upper and lower confidence limitsi
    trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency,possibleFreq)

    #positions=[(0,0), (0,1), (1,0), (1,1), (2,0)]
    #ax1=plt.subplot2grid((3,2), positions[ind])

    nTrialsEachFreq = np.empty(nFreq)
    nRightwardEachFreq = np.empty(nFreq)
    for indf,thisFreq in enumerate(possibleFreq):

        nTrialsThisFreq = sum(valid & trialsEachFreq[:,indf])
        nRightwardThisFreq =  sum(valid & choiceRight & trialsEachFreq[:,indf])
        conf = np.array(proportion_confint(nRightwardThisFreq, nTrialsThisFreq, method = 'wilson'))
        
        nTrialsEachFreq[indf] = nTrialsThisFreq
        nRightwardEachFreq[indf] = nRightwardThisFreq
        confLimitsEachFreq[0, indf] = conf[0] # Lower ci
        confLimitsEachFreq[1, indf] = conf[1] # Upper ci

    fractionRightEachFreq = nRightwardEachFreq/nTrialsEachFreq.astype(float)

    #plot(possibleFreq,fractionRightEachFreq,'-o')
    #gca().set_xscale('log')
    upperWhisker = confLimitsEachFreq[1, :] - fractionRightEachFreq #Find lengths of whiskers for plotting function
    lowerWhisker = fractionRightEachFreq - confLimitsEachFreq[0,:]
    #x = range(nFreq)
    x = possibleFreq
    errorbar(x, 100*fractionRightEachFreq, yerr = [100*lowerWhisker, 100*upperWhisker])
    axhline(y=50, color = 'red')
    ax=gca()
    ax.set_xscale('log')
    #ax.set_xticks([3000,5000,7000,10000,14000,20000,40000])
    ax.set_xticks([3000,7000,16000])
    ax.set_xticks(np.arange(1000,40000,1000),minor=True)
    from matplotlib.ticker import ScalarFormatter
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_formatter(ScalarFormatter())

    ylim([0,100])
    xlim([possibleFreq[0]/1.2,possibleFreq[-1]*1.2])
    xlabel('Frequency (kHz)')
    ylabel('Rightward trials (%)')
    title(subject)

suptitle(', '.join(sessions))
show()


'''
    fractionRightEachFreq = nRightwardEachFreq/nTrialsEachFreq.astype(float)

    #plot(possibleFreq,fractionRightEachFreq,'-o')
    #gca().set_xscale('log')
    positions=[(0,0), (0,1), (1,0), (1,1), (2,0)]
    ax1=plt.subplot2grid((3,2), positions[ind])
    ax1.plot(fractionRightEachFreq,'-o')
    title(subject)
    ylim([0,1])
show()
'''
