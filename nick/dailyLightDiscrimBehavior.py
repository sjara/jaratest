import sys
from jaratoolbox.test.nick import light_discrim_behavior
import matplotlib.pyplot as plt

subjects = ['adap022', 'adap026', 'adap027', 'adap030']
sessions = ['20160612a', '20160613a', '20160614a', '20160615a', '20160616a', '20160617a', '20160618a', '20160619a', '20160620a', '20160621a', '20160622a', '20160623a', '20160624a']

# if len(sys.argv)>1:
#     sessions = sys.argv[1:]

light_discrim_behavior.light_discrim_behavior_report(subjects, sessions, outputDir='/tmp/')
plt.show()
