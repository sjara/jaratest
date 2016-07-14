'''
For Daily Behavior Monitoring.
Loads behavior data from mounted jarahub/data/behavior for animals of interest, plot psychometric curve and dynamics data.
'''
import sys
# from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis
from jaratoolbox import behavioranalysis
reload(behavioranalysis)

# subjects = ['amod001', 'amod002', 'amod003', 'amod004', 'amod005']
# subjects = ['adap026', 'adap027', 'adap028', 'adap029', 'adap030', ]
# subjects = ['adap021', 'adap022', 'adap023', 'adap024', 'adap025' ]
# subjects = ['adap022', 'adap026', 'adap027', 'adap030'] #New muscimol animals
subjects = ['adap025', 'adap028', 'adap029']

if len(sys.argv)>1:
    sessions = sys.argv[1:]
    #sessions = input("Enter sessions (in a list of strings ['','']) to check behavior performance:")

behavioranalysis.behavior_summary(subjects,sessions,trialslim=[0,1000],outputDir='/home/nick/data/behavior_reports')

