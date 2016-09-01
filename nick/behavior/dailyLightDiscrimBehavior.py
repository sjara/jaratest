import sys
from jaratest.nick import light_discrim_behavior
import matplotlib.pyplot as plt

subjects = ['adap025']
# sessions = ['20160612a', '20160613a', '20160614a', '20160615a', '20160616a', '20160617a', '20160618a', '20160619a', '20160620a', '20160621a', '20160622a', '20160623a', '20160624a']

sessions = ['20160712a', '20160713a', '20160714a', '20160715a', '20160716a', '20160718a', '20160719a', '20160720a']

# if len(sys.argv)>1:
#     sessions = sys.argv[1:]

light_discrim_behavior.light_discrim_behavior_report(subjects, sessions, outputDir='/tmp/')
plt.show()
