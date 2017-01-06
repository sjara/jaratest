from jaratest.nick.behavior import soundtypes
from jaratest.nick.utils import transferutils
from matplotlib import pyplot as plt

# subjects = ['amod006','amod007','amod008','amod009','amod010']
subjects = ['amod006']

# sessions = ['20160922a', '20160923a', '20160926a', '20160927a', '20160928a', '20160929a']
sessions = ['20161003a', '20161005a', '20161007a', '20161008a']


for subject in subjects:
    for session in sessions:
        behavFile = '{}_2afc_{}.h5'.format(subject, session)
        transferutils.rsync_behavior(subject, behavFile)
    # fig = plt.cla()
    fig = plt.figure()
    soundtypes.sound_type_behavior_summary(subject, sessions, '', trialslim=[0, 1200])

    plt.show()
