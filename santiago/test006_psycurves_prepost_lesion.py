
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint #Used to compute confidence interval for the error bars. 
from jaratoolbox import settings 
from jaratoolbox import extraplots
import sys, os

#animalsNames = ['test012','test020']
animalsNames = ['test012']
sessionsPre = ['20150106a','20150108a','20150109a','20150110a'] # Pre-lesion
sessionsPost = ['20150115a','20150116a','20150117a','20150118a'] # Post-lesion
sessionsMorePost = ['20150126a','20150127a','20150128a','20150129a']
#sessionsMorePost = ['20150129a']
#sessions = ['20150119a'] # Post-lesion
allSessions = [sessionsPre,sessionsPost,sessionsMorePost]
'''
'''

'''
animalsNames = ['test011','test015','test016']
sessionsPre = ['20150210a','20150211a','20150212a','20150213a','20150214a','20150215a',] # Pre-lesion
sessionsPost = ['20150220a','20150221a','20150222a','20150223a','20150225a','20150226a','20150227a'] # Post-lesion
sessionsPost = ['20150220a','20150221a','20150222a'] # Post-lesion (first)
sessionsPost = ['20150223a','20150225a','20150226a','20150227a'] # Post-lesion (last)
sessionsPost = ['20150221a','20150222a','20150223a']
allSessions = [sessionsPre,sessionsPost]
'''

'''
animalsNames = ['test052','test057']
sessionsPre = ['20150223a','20150224a','20150225a','20150226a','20150227a'] # Pre-lesion
sessionsPost = ['20150311a','20150312a','20150313a','20150314a','20150315a'] # Post-lesion
allSessions = [sessionsPre,sessionsPost]
'''

nAnimals = len(animalsNames)
nSets = len(allSessions)

fontSize = 12

clf()
gcf().subplots_adjust(bottom=0.15)
markerFaceColors = ['k','w','w']
plotHandles = []
for inda, animalName in enumerate(animalsNames):#enumerate(subjects):
    subplot(1,len(animalsNames),inda+1)
    for indset,sessions in enumerate(allSessions[:2]):
        bdata = behavioranalysis.load_many_sessions(animalName,sessions)
        targetFrequency=bdata['targetFrequency']
        choice=bdata['choice']
        valid=bdata['valid'] & (choice!=bdata.labels['choice']['none'])
        intensities=bdata['targetIntensity']
        choiceRight = choice==bdata.labels['choice']['right']

        possibleFreq = np.unique(targetFrequency)
        nFreq = len(possibleFreq) 
        trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency,possibleFreq)

        (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
           behavioranalysis.calculate_psychometric(choiceRight,targetFrequency,valid)

        hold(True)
        (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(possibleValues,fractionHitsEachValue,ciHitsEachValue)
        setp(pdots,ms=6,mec='k',mew=2,mfc=markerFaceColors[indset])
        plotHandles.append(pdots[0])
    xlabel('Frequency (Hz)',fontsize=fontSize)
    ylabel('Rightward choice (%)',fontsize=fontSize)
    legend(plotHandles,['pre','post'],numpoints=1,loc='upper left',fontsize=fontSize-2)
    title(animalName)

show()

# -- Save figure --
outputDir = '/tmp/'#figparams.figuresDir
PRINT_FIGURE = 1
figFormat = 'svg'
if PRINT_FIGURE:
    plt.gcf().set_size_inches((5,4)) # for paper
    figName = 'psycurve_prepost_{0}.{1}'.format(animalName,figFormat)
    fullName = os.path.join(outputDir,figName)
    print 'Saving figure to %s'%fullName
    plt.gcf().set_frameon(False)
    plt.savefig(fullName,format=figFormat)#,facecolor=figparams.colBG)
    plt.gcf().set_frameon(True)
    print '... figure saved.'
    pass

sys.exit()


########## BELOW IS OLD CODE FOR PLOTTING EACH CURVE IN ONE PANEL ##########

figure(2)
clf()
for inda, animalName in enumerate(animalsNames):#enumerate(subjects):
    for indset,sessions in enumerate(allSessions):
        subplot2grid((nSets,nAnimals),(indset, inda))
        try:
            #bdata=loadbehavior.BehaviorData(fname)
            bdata = behavioranalysis.load_many_sessions(animalName,sessions)
        except IOError:
            continue

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
        title(animalName)

suptitle(', '.join(sessions))
show()

