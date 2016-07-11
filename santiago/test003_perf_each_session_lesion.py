'''
Plot the average performance for each session before and after a lesion.
'''

from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
import numpy as np
from pylab import *
from jaratoolbox import settings 
import os

experimenter = 'santiago'

'''
animalsNames = ['test052','test057']
#animalsNames = ['test057']
#sessionsPre = ['20150223a','20150224a','20150225a','20150226a','20150227a','20150228a','20150303a','20150304a'] # Including rig problems
sessionsPre = ['20150223a','20150224a','20150225a','20150226a','20150227a'] # Pre-lesion
sessionsPost = ['20150311a','20150312a','20150313a','20150314a','20150315a'] # Post-lesion
sessionsVisual = ['20150315b','20150316a','20150316b','20150317a','20150318a',
                  '20150319a','20150320a','20150321a'] # Visual
sessionsMorePost = ['20150322a','20150323a','20150324a','20150325a','20150326a']

typeEachSessionLabels = ['pre','post','visual','morepost']
typeEachSession = len(sessionsPre)*[0] + len(sessionsPost)*[1] + len(sessionsVisual)*[2] + len(sessionsMorePost)*[3]
allSessions = sessionsPre+sessionsPost+sessionsVisual+sessionsMorePost
'''

'''
animalsNames = ['test011','test015','test016']
sessionsPre = ['20150210a','20150211a','20150212a','20150213a','20150214a','20150215a',] # Pre-lesion
sessionsPost = ['20150220a','20150221a','20150222a','20150223a','20150225a','20150226a','20150227a'] # Post-lesion

typeEachSessionLabels = ['pre','post']
typeEachSession = len(sessionsPre)*[0] + len(sessionsPost)*[1]
allSessions = sessionsPre+sessionsPost
'''

#animalsNames = ['test012','test020']
animalsNames = ['test012']
sessionsPre = ['20150106a','20150108a','20150109a','20150110a'] # Pre-lesion
sessionsPost = ['20150115a','20150116a','20150117a','20150118a','20150119a'] # Post-lesion
sessionsVisual = ['20150120a','20150121a','20150122a','20150123a','20150124a','20150125a'] # Visual
sessionsMorePost = ['20150126a','20150127a','20150128a','20150129a']

typeEachSessionLabels = ['pre','post','visual','morepost']
typeEachSession = len(sessionsPre)*[0] + len(sessionsPost)*[1] + len(sessionsVisual)*[2] + len(sessionsMorePost)*[3]
allSessions = sessionsPre+sessionsPost+sessionsVisual+sessionsMorePost
'''
'''

nAnimals = len(animalsNames)
nSessions = len(allSessions)

nCorrectEachSession = np.empty(nSessions)
nValidEachSession = np.empty(nSessions)
#avPerfEachSession = []
#ciEachSession = []

clf()
gcf().subplots_adjust(bottom=0.15)
for inda, animalName in enumerate(animalsNames):
    subplot(1,nAnimals,inda+1)
    for inds,oneSession in enumerate(allSessions):
        typeThisSession = typeEachSessionLabels[typeEachSession[inds]]
        if (typeThisSession=='pre') | (typeThisSession=='post')| (typeThisSession=='morepost'):
            paradigm = '2afc'
        elif typeThisSession=='visual':
            paradigm = 'lightDiscrim'
        else:
            raise TypeError('This session type is not defined')

        try:
            fname = loadbehavior.path_to_behavior_data(animalName,experimenter,paradigm,oneSession)
            bdata=loadbehavior.BehaviorData(fname)
        except IOError:
            print 'It could not load {0}'.format(fname)
            continue

        '''
        print '-----------------------------'
        print bdata['nRewarded'][-1]
        print bdata['nValid'][-1]
        '''
        nCorrectEachSession[inds] = bdata['nRewarded'][-1]
        nValidEachSession[inds] = bdata['nValid'][-1]

    avPerfEachSession = nCorrectEachSession/nValidEachSession

    colorEachType = ['k','k','m','k']
    markerFaceEachType = ['k','w','w','w']
    fontSize = 12

    ax = gca()
    xValues = np.arange(nSessions)+1
    plot(xValues,100*avPerfEachSession,'-',color='0.5')
    axhline(100*0.5,color='0.75',ls='--')
    axhline(100*0.75,color='0.75',ls='--')
    for inds,perfOneSession in enumerate(avPerfEachSession):
        hold(True)
        thisColor = colorEachType[typeEachSession[inds]]
        thisFace = markerFaceEachType[typeEachSession[inds]]
        plot(xValues[inds],100*perfOneSession,'o',ms=6,mew=2,mec=thisColor,mfc=thisFace)
    ylim(100*np.array([0.4,1]))

    ax.set_ylabel('Trials correct (%)',fontsize=fontSize)
    xlabel('Session',fontsize=fontSize)
    #legend(['pre','post','visual'])

    title(animalName)


    draw()
    show()

#xlim([0,15])

# -- Save figure --
outputDir = '/tmp/'#figparams.figuresDir
PRINT_FIGURE = 1
figFormat = 'svg'
if PRINT_FIGURE:
    plt.gcf().set_size_inches((5,4)) # for paper
    figName = 'perf_prepostvis_{0}.{1}'.format(animalName,figFormat)
    fullName = os.path.join(outputDir,figName)
    print 'Saving figure to %s'%fullName
    plt.gcf().set_frameon(False)
    plt.savefig(fullName,format=figFormat)#,facecolor=figparams.colBG)
    plt.gcf().set_frameon(True)
    print '... figure saved.'
    pass
'''
'''
