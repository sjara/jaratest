'''
For Daily Behavior Monitoring.
Loads behavior data from mounted jarahub/data/behavior for animals of interest, plot psychometric curve and dynamics data.
'''
import sys
import os
from jaratest.lan import behavioranalysis_vlan as behavioranalysis
reload(behavioranalysis)
from jaratoolbox import settings_2 as settings
reload(settings)

#settings.BEHAVIOR_PATH = '/home/languo/data/mnt/jarahubdata'
#settings.DEFAULT_EXPERIMENTER = 'billy'

#subjects = ['d1pi014','d1pi018','d1pi019','d1pi020']
subjects = ['gosi010']

if len(sys.argv)>1:
    sessions = sys.argv[1:]
    #sessions = input("Enter sessions (in a list of strings ['','']) to check behavior performance:")

behavioranalysis.behavior_summary(subjects,sessions,trialslim=[0,1000],outputDir='/home/languo/data/behavior_reports')

