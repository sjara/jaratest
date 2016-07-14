import sys
from jaratoolbox.test.nick import soundtypes
from matplotlib import pyplot as plt


subjects = ['amod006', 'amod007', 'amod008', 'amod009', 'amod010']

if len(sys.argv)>1:
    sessions = sys.argv[1:]
    #sessions = input("Enter sessions (in a list of strings ['','']) to check behavior performance:")

else:
    sessions = ['20160621a', '20160622a', '20160623a', '20160624a', '20160625a', '20160626a', '20160627a', '20160628a', '20160629a', '20160630a', '20160701a', '20160702a', '20160703a', '20160704a', '20160705a', '20160706a', '20160707a', '20160708a', '20160709a', '20160710a']

for session in sessions:
    soundtypes.sound_type_behavior_summary(subjects, session, '', trialslim=[0, 1200])
    plt.show()
    plt.savefig('/tmp/{}-{}_{}.png'.format(subjects[0], subjects[-1], session))


