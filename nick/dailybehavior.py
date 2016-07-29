'''
For Daily Behavior Monitoring.
Loads behavior data from mounted jarahub/data/behavior for animals of interest, plot psychometric curve and dynamics data.
'''
import sys
# from jaratest.nick import behavioranalysis_vnick as behavioranalysis
from jaratoolbox import behavioranalysis
reload(behavioranalysis)

# subjects = ['amod001', 'amod002', 'amod003', 'amod004', 'amod005']
# subjects = ['adap026', 'adap027', 'adap028', 'adap029', 'adap030', ]
# subjects = ['adap021', 'adap022', 'adap023', 'adap024', 'adap025' ]
# subjects = ['adap022', 'adap026', 'adap027', 'adap030'] #New muscimol animals
# subjects = ['adap025', 'adap028', 'adap029']

subjects = ['adap028']
# sessions = ['20160711a', '20160712a', '20160713a', '20160714a', '20160715a', '20160716a', '20160718a','20160719a', '20160720a', '20160721a', '20160722a']
sessions = ['20160718a','20160719a', '20160720a', '20160721a', '20160722a', '20160723a', '20160725a', '20160726a', '20160727a']

if len(sys.argv)>1:
    sessions = sys.argv[1:]
    #sessions = input("Enter sessions (in a list of strings ['','']) to check behavior performance:")

behavioranalysis.behavior_summary(subjects,sessions,trialslim=[0,1000],outputDir='/home/nick/data/behavior_reports')

