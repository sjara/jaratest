from jaratoolbox import settings
from jaratoolbox import ephyscore
import os
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys

subject = 'd1pi039'
paradigm = 'am_tuning_curve'
session = '20190731h'
ephysSession = '2019-07-31_16-09-08'

# subject = 'd1pi039'
# paradigm = 'am_tuning_curve'
# session = '20190731b'
# ephysSession = '2019-07-31_11-17-46'

eventsFilename = os.path.join(settings.EPHYS_PATH, subject, ephysSession,
                              'all_channels.events')

behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
behavData = loadbehavior.BehaviorData(behavFile, readmode='full')

eventData = loadopenephys.Events(eventsFilename)
channelID = 0
thisChannelOn = eventData.get_event_onset_times(eventID=1,
                                                eventChannel=channelID)

behavDataSize = len(behavData['currentAmpL'])
ephysDataSize = len(thisChannelOn)

print('Behavior: {}'.format(behavDataSize))
print('Ephys:    {}'.format(ephysDataSize))

trialsToRemove = behavDataSize - ephysDataSize + 1
if trialsToRemove > 0:
    for key, value in behavData.items():
        behavData[key] = value[0:-trialsToRemove]

    print('Behavior: {}'.format(len(behavData['currentAmpL'])))
    print('Ephys:    {}'.format(len(thisChannelOn)))

# Save this edited behavior data
