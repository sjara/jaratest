'''
For Daily Behavior Monitoring.
Loads behavior data from mounted jarahub/data/behavior for animals of interest, plot psychometric curve and dynamics data.
'''
import sys
from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis
reload(behavioranalysis)

# subjects = ['amod001', 'amod002', 'amod003', 'amod004', 'amod005']

if len(sys.argv)>1:
    subject = sys.argv[1]
    sessions = sys.argv[2:]
    #sessions = input("Enter sessions (in a list of strings ['','']) to check behavior performance:")

behavioranalysis.behavior_summary(subject,sessions,trialslim=[0,1000],outputDir='/home/nick/data/behavior_reports')
