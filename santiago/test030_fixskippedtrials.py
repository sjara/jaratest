'''
Fixing skipped behavior trials

sshfs -o idmap=user jarauser@jarahub:/data/jarashare/ /mnt/jarashare
rsync -a --progress --exclude *.continuous sjara@jarahub:/data/ephys/adap005/2015-12-15_14-02-08 ./
'''

from jaratoolbox import loadbehavior
reload(loadbehavior)
from jaratoolbox import behavioranalysis
reload(behavioranalysis)
from jaratoolbox import loadopenephys
from jaratoolbox import settings
import os
import numpy as np
from pylab import *

SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial

subject = 'adap005'
experimenter = 'lan'
paradigm = '2afc'
behavSession = '20151215a'
ephysSession = '2015-12-15_14-02-08'

#--------------- THIS PART JUST LOADS THE DATA ---------------
# -- Load behavior data --
behavDataFileName = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
bdata = loadbehavior.FlexCategBehaviorData(behavDataFileName,readmode='full')
soundOnsetTimeBehav = bdata['timeTarget']

# -- Load event data and convert event timestamps to ms --
ephysDir = os.path.join(settings.EPHYS_PATH, subject, ephysSession)
eventFilename = os.path.join(ephysDir, 'all_channels.events')
events = loadopenephys.Events(eventFilename) # Load events data
eventTimes = np.array(events.timestamps)/SAMPLING_RATE # in sec
soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)
soundOnsetTimeEphys = eventTimes[soundOnsetEvents]

#------------- THE IMPORTANT PART FOR FIXING ALIGNMENT -------------
# Find missing trials
missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)

# Remove missing trials
bdata.remove_trials(missingTrials)
bdata.find_trials_each_block()  # If this is needed, it should be done after bdata has been fixed
soundOnsetTimeBehav = bdata['timeTarget']


nTrialsBehav = len(soundOnsetTimeBehav)
nTrialsEphys = len(soundOnsetTimeEphys)
print 'N (behav) = {0}'.format(nTrialsBehav)
print 'N (ephys) = {0}'.format(nTrialsEphys)
