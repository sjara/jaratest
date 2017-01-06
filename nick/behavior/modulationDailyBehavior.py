#!/usr/bin/python

import sys
sys.path.append('/home/nick/src/')
from jaratest.nick.behavior import soundtypes
from jaratest.nick.utils import transferutils
reload(soundtypes)
from matplotlib import pyplot as plt
import datetime


# subjects = ['amod006', 'amod007', 'amod008', 'amod009', 'amod010']
subjects = ['amod011', 'amod012', 'amod013', 'amod014']

if len(sys.argv)>1:
    if sys.argv[1]=='today':
        today = datetime.datetime.today()
        session = '{}a'.format(today.strftime('%Y%m%d'))
    elif sys.argv[1]=='yesterday':
        yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
        session = '{}a'.format(yesterday.strftime('%Y%m%d'))
    else:
        session = sys.argv[1]

for subject in subjects:
    behavFile = '{}_2afc_{}.h5'.format(subject, session)
    transferutils.rsync_behavior(subject, behavFile)

soundtypes.sound_type_behavior_summary(subjects, session, '', trialslim=[0, 1200])
fig = plt.gcf()
fig.set_size_inches(8.5, 11)
plt.show()
plt.savefig('/home/nick/Dropbox/jaralab/reports/amodbehav/{}-{}_{}.png'.format(subjects[0], subjects[-1], session)) 

