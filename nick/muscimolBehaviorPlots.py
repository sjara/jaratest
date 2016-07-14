'''
For compiling the behavior data from muscimol and saline days
'''
import sys
from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis
# from jaratoolbox import behavioranalysis
reload(behavioranalysis)

# # subjects = ['amod001', 'amod002', 'amod003', 'amod004', 'amod005']

# if len(sys.argv)>1:
#     subject = sys.argv[1]
#     sessions = sys.argv[2:]
#     #sessions = input("Enter sessions (in a list of strings ['','']) to check behavior performance:")

# behavioranalysis.behavior_summary(subject,sessions,trialslim=[0,1000],outputDir='/home/nick/data/behavior_reports')


def muscimol_plot(animal, muscimolSessions, salineSessions):
    muscimolData = behavioranalysis.load_many_sessions(animal, muscimolSessions)
    plineM, pcapsM, pbarsM, pdotsM = behavioranalysis.plot_frequency_psycurve(muscimolData)
    setp(plineM, color='r')
    setp(pcapsM, color='r')
    setp(pbarsM, color='r')
    setp(pdotsM, markerfacecolor='r')

    salineData = behavioranalysis.load_many_sessions(animal, salineSessions)
    plineS, pcapsS, pbarsS, pdotsS = behavioranalysis.plot_frequency_psycurve(salineData)
    # setp(plineS, color='r')
    # setp(pcapsS, color='r')
    # setp(pbarsS, color='r')
    # setp(pdotsS, markerfacecolor='r')
    title(animal)

figure()
animal = 'amod001'
muscimolSessions = ['20160214a', '20160317a', '20160319a', '20160321a', '20160323a']
salineSessions = ['20160315a', '20160318a', '20160320a', '20160322a']
muscimol_plot(animal, muscimolSessions, salineSessions)

figure()
animal = 'amod005'
muscimolSessions = ['20160215a', '20160317a', '20160319a', '20160321a', '20160323a']
salineSessions = ['20160316a', '20160318a', '20160320a', '20160322a']
muscimol_plot(animal, muscimolSessions, salineSessions)

figure()
animal = 'adap016'
# muscimolSessions = ['20160317a', '20160319a', '20160321a']
muscimolSessions = ['20160319a', '20160321a']
salineSessions = ['20160316a', '20160318a', '20160320a', '20160322a']
muscimol_plot(animal, muscimolSessions, salineSessions)

figure()
animal = 'adap019'
muscimolSessions = ['20160317a', '20160319a','20160323a']
salineSessions = ['20160316a', '20160318a', '20160320a', '20160322a']
muscimol_plot(animal, muscimolSessions, salineSessions)

figure()
animal = 'adap019'
# muscimolSessions = ['20160317a', '20160319a']
muscimolSessions = ['20160322a']
salineSessions = ['20160316a', '20160318a', '20160320a']
muscimol_plot(animal, muscimolSessions, salineSessions)
