'''
Show performance report for each animal
'''

from jaratoolbox import behavioranalysis
from pylab import *
from jaratoolbox import loadbehavior
import sys

if len(sys.argv)>1:
    session = sys.argv[1]+'a'
else:
    session = '20150308a'
   
for CASE in [1]:

    if CASE==1:
        subjects = ['cued001','cued002','cued003','cued004','cued005','cued006']
    elif CASE==2:
        pass

    figure(CASE)
    #behavioranalysis.behavior_summary(subjects,sessions,trialslim=[0,1000],outputDir='/var/tmp/behavior_reports/')
    for inda,animalName in enumerate(subjects):
        fname=loadbehavior.path_to_behavior_data(animalName,'santiago','2afc',session)
        try:
            bdata=loadbehavior.BehaviorData(fname)
            nReward = bdata['nRewarded'][-1]
            nValid = bdata['nValid'][-1]
            correct = nReward/float(nValid)
            print '{0} (rew/valid): {1} / {2} = {3:0.0%}'.format(animalName,nReward,nValid,correct)
        except:
            print 'Something is wrong with this session'
            pass


'''
subjects = ['test011','test015','test016']
sessions = ['20150222a','20150223a']
behavioranalysis.behavior_summary(subjects,sessions,trialslim=[0,1000],outputDir='/tmp/')
'''
