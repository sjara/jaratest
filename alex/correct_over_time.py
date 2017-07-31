from jaratoolbox import loadbehavior
reload(loadbehavior)
import copy
from jaratest.nick.behavior import soundtypes
from jaratoolbox import behavioranalysis
from matplotlib import pyplot as plt
import numpy as np
from jaratoolbox import extraplots
from jaratoolbox import colorpalette
fontsize = 24
from statsmodels.stats.proportion import proportion_confint

#subjects = ['gosi002', 'gosi006']
subjects = ['adap051', 'gosi013']
#subjects = ['gosi002', 'gosi006', 'adap051', 'gosi013']
'''
sessions = ['20170410a', '20170411a',
            '20170412a', '20170413a', 
            '20170414a', '20170415a', 
            '20170416a', '20170423a', 
            '20170424a', '20170425a', 
            '20170426a', '20170427a', 
            '20170428a', '20170429a', 
            '20170430a']
'''
'''
sessions = ['20170524a', '20170525a',
            '20170526a', '20170527a', 
            '20170603a', '20170604a', 
            '20170605a', '20170606a',
            '20170607a']
'''
'''
allSessions = [['20170413a', '20170414a', '20170415a', '20170416a', 
                '20170423a', '20170424a', '20170425a', '20170426a', '20170427a'],
                ['20170524a', '20170525a', '20170526a', '20170527a', 
                 '20170603a', '20170604a', '20170605a', '20170606a', '20170607a']]
'''
sessions = ['20170524a', '20170525a', '20170526a', '20170527a', 
                 '20170603a', '20170604a', '20170605a', '20170606a', '20170607a']
#dayLengths = [[x for x in range(7)], [6,7], [x for x in range(7,15)]]
dayLengths = [[x for x in range(4)], [3,4], [x for x in range(4, 9)]]
'''
sessions = ['20170524a', '20170525a',
            '20170526a', '20170527a']
dayLengths = [[x for x in range(4)]]
'''
nSessions = len(sessions)
#bdataPath = loadbehavior.path_to_behavior_data(subjects[0], '2afc', '20170411a')

plt.figure()
percentCorrect = []
nTrialsEachValue = np.empty(nSessions,dtype=int)
nHitsEachValue = np.empty(nSessions,dtype=int)
for indSubject, subject in enumerate(subjects):
    percentCorrect.append([])
    #sessions = allSessions[indSubject/2]
    for indSession, session in enumerate(sessions):
        bdata = behavioranalysis.load_many_sessions(subject, [session])

        rewarded = float(bdata['nRewarded'][-1])
        valid = float(sum(bdata['valid']))
        
        percentCorrect[indSubject].append(np.divide(rewarded, valid))
        nHitsEachValue[indSession] = rewarded
        nTrialsEachValue[indSession] = valid


    ciHitsEachValue = np.array(proportion_confint(nHitsEachValue, nTrialsEachValue, method = 'wilson'))        

    #plt.subplot(len(subjects), 1, indSubject+1)

    upperWhisker = ciHitsEachValue[1,:]-percentCorrect[indSubject]
    lowerWhisker = percentCorrect[indSubject]-ciHitsEachValue[0,:]
    '''
    (pline, pcaps, pbars) = plt.errorbar(dayLengths[0], percentCorrect[indSubject][:7], yerr = [lowerWhisker[:7], upperWhisker[:7]],color='b')
    (pline, pcaps, pbars) = plt.errorbar(dayLengths[2], percentCorrect[indSubject][7:15], yerr = [lowerWhisker[7:15], upperWhisker[7:15]],color='b')
    '''
    (pline, pcaps, pbars) = plt.errorbar(dayLengths[0], percentCorrect[indSubject][:4], yerr = [lowerWhisker[:4], upperWhisker[:4]],color='k')
    (pline, pcaps, pbars) = plt.errorbar(dayLengths[2], percentCorrect[indSubject][4:9], yerr = [lowerWhisker[4:9], upperWhisker[4:9]],color='k')
    
    ax = pline.axes
    extraplots.boxoff(ax)
    extraplots.set_ticks_fontsize(ax, fontsize)

    #plt.title(subject, fontsize=fontsize)
    plt.xlabel('Sessions',fontsize=fontsize)
    plt.ylabel('Percent Correct',fontsize=fontsize)
    plt.ylim(0.5, 1.0)
    plt.xlim(0, len(sessions)-1)    
    plt.setp(pline, color='k')
    plt.setp(pcaps, color='k')
    plt.setp(pbars, color='k')


    '''
    plt.plot(dayLengths[0], percentCorrect[indSubject][:7], '-ob')
    plt.plot(dayLengths[1], percentCorrect[indSubject][6:8], '--ob')
    plt.plot(dayLengths[2], percentCorrect[indSubject][7:15], '-ob')
    '''
    plt.plot(dayLengths[0], percentCorrect[indSubject][:4], '-ok')
    plt.plot(dayLengths[1], percentCorrect[indSubject][3:5], '--ok')
    plt.plot(dayLengths[2], percentCorrect[indSubject][4:9], '-ok')
    plt.plot(9)

plt.show()
