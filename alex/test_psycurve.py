'''
For Daily Behavior Monitoring.
Loads behavior data from mounted jarahub/data/behavior for animals of interest, plot psychometric curve and dynamics data.
'''
import sys
# from jaratest.nick import behavioranalysis_vnick as behavioranalysis
from jaratoolbox import behavioranalysis
reload(behavioranalysis)
from jaratoolbox import extraplots
from matplotlib import pyplot as plt

fontsize = 24

colors = ['k', 'r', 'g', 'b', 'y']

# subjects = ['amod001', 'amod002', 'amod003', 'amod004', 'amod005']
# subjects = ['adap026', 'adap027', 'adap028', 'adap029', 'adap030', ]
# subjects = ['adap021', 'adap022', 'adap023', 'adap024', 'adap025' ]
# subjects = ['adap022', 'adap026', 'adap027', 'adap030'] #New muscimol animals
# subjects = ['adap025', 'adap028', 'adap029']

#subjects = ['gosi002', 'gosi006']
#subjects = ['gosi002']
#subjects = ['gosi006']
#subjects = ['gosi013']
#subjects = ['adap051']
subjects = ['amod014']

sessions = ['20170616a']

#sessions = ['20170608a']

#sessions = ['20170416a', '20170427a']
#sessions = ['20170527a', '20170606a']
'''
sessions = ['20170505a',
            #'20170506a', 
            #'20170507a', 
            #'20170508a'
            ]
'''
#sessions = ['20170609a']

if len(sys.argv)>1:
    sessions = sys.argv[1:]
    #sessions = input("Enter sessions (in a list of strings ['','']) to check behavior performance:")

plt.figure()

for indSubject, subject in enumerate(subjects):
    plt.subplot(len(subjects), 1, indSubject+1)
    bdata = behavioranalysis.load_many_sessions(subject, sessions, 'simple2afc')
    '''
    allPlines = []
    for indSession, session in enumerate(sessions):
        thisColor = colors[indSession]
        bdata = behavioranalysis.load_many_sessions(subjects[0], [session], 'simple2afc')
    '''
    valid = bdata['valid']
    choice = bdata['choice']

    print sum(valid)

    #Is this the correct thing to get to calculate psychometrics?
    choiceRight = choice==bdata.labels['choice']['right']
    targetFreq = bdata['targetFrequency']

    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
    behavioranalysis.calculate_psychometric(choiceRight, targetFreq, valid)

    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,ciHitsEachValue,xTickPeriod=1)

    #allPlines.append(pline)

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
    '''
    plt.setp(pline, color=thisColor)
    plt.setp(pcaps, color=thisColor)
    plt.setp(pbars, color=thisColor)
    plt.setp(pdots, markerfacecolor=thisColor)
    '''
    ax.xaxis.set_ticks_position('bottom')   
    '''
    legend2 = plt.legend(allPlines, ['Pre-Lesion', 'Post-Lesion'], bbox_to_anchor=(0.375, 0.875),
        bbox_transform=plt.gcf().transFigure)
    
    legend2 = plt.legend(allPlines, ['Pre-Lesion', 'Post-Lesion'], bbox_to_anchor=(0.875, 0.875),
        bbox_transform=plt.gcf().transFigure)
    '''

    #plt.hold(1)

plt.show()