'''
Updated 20170425 to new clustering and celldatabase format.
Translate information from Billy about ephys sessions to files needed by Lan.

Lan's format looks something like this:

exp = cellDB.Experiment(subject, date ='2016-02-22', brainarea='rightAStr', infor='') 
site1 = exp.add_site(depth=, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('', None, sessionTypes['nb']) 
site1.add_session('', 'a', sessionTypes['tc']) 
site1.add_session('12-44-19', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)


This reads the adap013_wiki.txt (a text copy of the wiki) in the allcells folder and translates it to the clustering format
'''


import re

# --- Define string format ---
header = '''
from jaratoolbox import celldatabase as cellDB
subject = '{subject}'
experiments = []
'''

formatExperiment = '''exp = cellDB.Experiment(subject, date ='{date}', brainarea='rightAStr', infor='')'''
formatSite = '''site1 = exp.add_site(depth={depth}, tetrodes=[1,2,3,4,5,6,7,8])'''
formatSessionTraining = '''site1.add_session('{ephysTime}', 'a', 'behavior', '2afc')'''
formatSessionTuning = '''site1.add_session('{ephysTime}', 'a', 'tc', 'laser_tuning_curve')'''


# --- Read Billy's wiki info ---
experimenter = ''
defaultParadigm = 'tuning_curve'
subject = 'adap017'
filename = '{0}_wiki.txt'.format(subject)  ##This file should be in the same directory
content = [line.rstrip('\n') for line in open(filename)]

### re.search(r'\* \d.\d+ turns, \d\d\d\d-\d\d-\d\d', oneline).group()

trainingDateLine = re.compile(r'(\d.\d+) turns, (\d\d\d\d-\d\d-\d\d)')#'\* (\d.\d+) turns, (\d\d\d\d-\d\d-\d\d)')
tuningLine = re.compile(r'\* (\d.\d+) turns, presented frequencies')
ephysLine = re.compile(r'\*\* ephys recording name: (\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d)')
rewardchangeLine = re.compile(r'\*\* Reward change')
dbase = {}


def test_turns(sessionDate, oneSession,lastTurns):
    if oneSession.has_key('turns'):
        try:
            assert float(oneSession['turns'])==float(lastTurns)
        except AssertionError:
            print 'WARNING! Turns do not match for {0}: {1} , {2}'.format(sessionDate,lastTurns,
                                                                          oneSession['turns'])


for indline,oneline in enumerate(content):
    matchEphys = ephysLine.search(oneline)
    if matchEphys:
        ephysSession = matchEphys.groups()[0]
        sessionDate = ephysSession[:10]
        #print content[indline-1]
        matchTraining = trainingDateLine.search(content[indline-1])
        matchTuning = tuningLine.search(content[indline-1])
        if matchTraining or matchTuning:
            if not dbase.has_key(sessionDate):
                dbase[sessionDate] = {}
        if matchTraining:
            lastTurns = matchTraining.groups()[0]
            test_turns(sessionDate, dbase[sessionDate],lastTurns)
            dbase[sessionDate].update({'turns':lastTurns,'ephysSessionTraining':ephysSession})
            matchRewardchange = rewardchangeLine.search(content[indline+4])
            if matchRewardchange:
                dbase[sessionDate].update({'type':'rewardchange'})
            else:
                dbase[sessionDate].update({'type':'psycurve'})
        elif matchTuning:
            lastTurns = matchTuning.groups()[0]
            test_turns(sessionDate, dbase[sessionDate],lastTurns)
            dbase[sessionDate].update({'turns':lastTurns,'ephysSessionTuning':ephysSession})
           

# --- Write Lan's format ---
print header.format(subject=subject)
for oneDate,oneSession in sorted(dbase.items()):
    #if not oneSession.has_key('ephysSessionTraining') or not oneSession.has_key('ephysSessionTuning'):
    #if not oneSession.has_key('ephysSessionTraining'):
    if not oneSession.has_key('ephysSessionTraining') or not oneSession['type']=='rewardchange':
        continue
    ephysTimeTraining = oneSession['ephysSessionTraining'][-8:]
    print formatExperiment.format(date=oneDate)
    print 'experiments.append(exp)'
    print formatSite.format(depth=oneSession['turns'])
    if oneSession.has_key('ephysSessionTuning'):
        ephysTimeTuning = oneSession['ephysSessionTuning'][-8:]
        print formatSessionTuning.format(ephysTime=ephysTimeTuning)
    print formatSessionTraining.format(ephysTime=ephysTimeTraining)
    
    print ''


