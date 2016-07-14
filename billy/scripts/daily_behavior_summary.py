'''
Show performance report for each animal

Example (on how to run):
python daily_behavior_summary.py 20150212
'''

from jaratoolbox import behavioranalysis
from pylab import *
import sys

datestring = str(sys.argv[1])
print datestring

sessions = datestring+'a'

subjects = ['adap017','adap015','adap013']#['adap021','adap022','adap023','adap024','adap025','adap018','adap020']#['test089','adap015','adap013']#['test059','test055','test053','test086']

figure()

try:
    behavioranalysis.behavior_summary(subjects,sessions,trialslim=[0,1000],outputDir='/home/billywalker/data/behavior_reports/')
except:
    print 'Something is wrong with this session'
    pass

