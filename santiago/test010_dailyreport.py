'''
Show performance report for each animal
'''

from jaratoolbox import behavioranalysis
from pylab import *

'''
subjects = ['test011','test012','test013','test014','test015',
            'test016','test017','test018','test019','test020']
subjects = ['test050','test051','test052','test053','test054',
            'test055','test056','test057','test058','test059']
subjects = ['test064','test065','test067','test068','test070','test071'] #'test066','test069',
subjects = ['test011','test012','test013','test014','test015',
            'test016','test017','test018','test019','test020']
'''

if len(sys.argv)>1:
    session = sys.argv[1]+'a'
else:
    session = '20150308a'


for CASE in [6,7,8]:#[3,4,5]:#[1,2,3,4]:

    if CASE==1:
        subjects = ['test085','test086','test087', 'test088','test089']
    elif CASE==2:
        subjects = ['adap001','adap002','adap003','adap004','adap005']
    elif CASE==3:
        subjects = ['adap006','adap007','adap008','adap009','adap010']
    elif CASE==4:
        subjects = ['d1pi003','d1pi004','d1pi005','d1pi006']
    elif CASE==5:
        subjects = ['adap011','adap012','adap013','adap014','adap015']
    elif CASE==6:
        subjects = ['adap016','adap017','adap018','adap019','adap020']
    elif CASE==7:
        subjects = ['adap021','adap022','adap023','adap024','adap025']
    elif CASE==8:
        subjects = ['d1pi008','d1pi009','d1pi010','d1pi011','d1pi012']
    elif CASE==0:
        subjects = ['adap010']

    figure(CASE)
    # subjects = ['test011','test015','test016','test017', 'test012','test013','test014','test018','test019','test020']
    #    subjects = ['test011','test015','test016','test017','test018']
    #    subjects = ['test050','test052','test053',
    #                'test055','test056','test057','test058','test059']

    #sessions = '20150311a'
    try:
        behavioranalysis.behavior_summary(subjects,session,trialslim=[0,1000],outputDir='/var/tmp/behavior_reports/')
    except:
        print 'Something is wrong with this session'
        raise
        pass


'''
subjects = ['test011','test015','test016']
sessions = ['20150222a','20150223a']
behavioranalysis.behavior_summary(subjects,sessions,trialslim=[0,1000],outputDir='/tmp/')
'''
