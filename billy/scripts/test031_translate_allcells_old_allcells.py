'''
Translate information from Billy about ephys sessions to files needed by Lan.

Lan's format looks something like this:

exp = cellDB.Experiment(animalName='adap013', date ='2016-02-22', experimenter='billy', defaultParadigm='tuning_curve') 
site1 = exp.add_site(depth=, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('', None, sessionTypes['nb']) 
site1.add_session('', 'a', sessionTypes['tc']) 
site1.add_session('12-44-19', 'a', sessionTypes['2afc'], paradigm='2afc')
'''


import re

# --- Define string format ---
header = '''
sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse',
                '2afc':'2afc'}
'''

############################## THIS IS FOR THE CORRECT DEPTH #######################################

initialDepth = 2 # initial depth of tetrodes when implanting in mm
depthPerTurn = 0.317 #in mm, one turn is 0.317 mm

####################################################################################################


formatExperiment = '''exp = cellDB.Experiment(animalName='{subject}', date ='{date}', experimenter='{experimenter}', defaultParadigm='{defparadigm}')'''
formatSite = '''site1 = exp.add_site(depth={depth}, tetrodes=[1,2,3,4,5,6,7,8])'''
formatSessionTraining = '''site1.add_session('{ephysTime}', 'a', sessionTypes['2afc'], paradigm='2afc')'''
formatSessionTuning = '''site1.add_session('{ephysTime}', 'a', sessionTypes['tc'])'''
formatTuningHeader = '''oneES = eSession(animalName='{subject}','''
formatTuningEphys = '''                 tuningSession = '{tuningEphysName}','''
formatSessionEphys = '''                 ephysSession = '{ephysName}','''
clusterTetrodes = '''                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},'''
formatTuningBehavior = '''                 tuningBehavior = '{behavName}')'''
formatSessionBehavior = '''                 behavSession = '{behavName}')'''
formatDepth = '''                 depth = {siteDepth},'''
clusterQuality = '''                 clusterQuality = {1:[]},'''

# --- Read Billy's wiki info ---
experimenter = ''
defaultParadigm = 'tuning_curve'
subject = 'adap020'
filename = '{0}_wiki.txt'.format(subject)
content = [line.rstrip('\n') for line in open(filename)]

### re.search(r'\* \d.\d+ turns, \d\d\d\d-\d\d-\d\d', oneline).group()

trainingDateLine = re.compile(r'\* (\d.\d+) turns, (\d\d\d\d-\d\d-\d\d)')
tuningLine = re.compile(r'\* (\d.\d+) turns, presented frequencies')
ephysLine = re.compile(r'\*\* ephys recording name: (\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d)')
behavLine = re.compile(r'\*\* behavior recording name: \w{7}_tuning_curve_(\d\d\d\d\d\d\d\d\w).h5')
rewardchangeLine = re.compile(r'\*\* Reward change')
dbase = {}


def test_turns(sessionDate, oneSession,lastTurns):
    if oneSession.has_key('turns'):
        try:
            assert float(oneSession['turns'])==float(lastTurns)
        except AssertionError:
            print 'WARNING! Turns do not match for {0}: {1} , {2}'.format(sessionDate,lastTurns,
                                                                          oneSession['turns'])
print 'testing'######################
sessionDate= ''
for indline,oneline in enumerate(content):
    matchEphys = ephysLine.search(oneline)
    #matchBehav = behavLine.search(oneline)
    '''
    if matchBehav:
        
        #print matchBehav.groups()
        behavSession = matchBehav.groups()[0]
        sessionDate = ephysSession[:10]
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
            dbase[sessionDate].update({'turns':lastTurns,'ephysSessionTuning':ephysSession},)#'behavSessionTuning':)
    '''
    if matchEphys:
        ephysSession = matchEphys.groups()[0]
        sessionDate = ephysSession[:10]
        matchTraining = trainingDateLine.search(content[indline-1])
        matchTuning = tuningLine.search(content[indline-1])
        matchBehav = behavLine.search(content[indline+1])

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
            dbase[sessionDate].update({'turns':lastTurns,'ephysSessionTuning':ephysSession,'behavSessionTuning':matchBehav.groups()[0]})
           

# --- Write Lan's format ---
#print header
for oneDate,oneSession in sorted(dbase.items()):
    #if not oneSession.has_key('ephysSessionTraining') or not oneSession.has_key('ephysSessionTuning'):
    #if not oneSession.has_key('ephysSessionTraining'):
    #if not oneSession.has_key('ephysSessionTraining') or not oneSession['type']=='rewardchange':
        #continue
    #ephysTimeTraining = oneSession['ephysSessionTraining'][-8:]
    #print formatExperiment.format(subject=subject,date=oneDate,
                                  #experimenter=experimenter,defparadigm=defaultParadigm)
    #print formatSite.format(depth=oneSession['turns'])
    if oneSession.has_key('ephysSessionTraining') & oneSession.has_key('ephysSessionTuning'):
        tuningEphys = oneSession['ephysSessionTuning']
        ephysSession = oneSession['ephysSessionTraining']
        tuningBehav = oneSession['behavSessionTuning']#oneSession['ephysSessionTuning'][-8:]
        tuningDepth = oneSession['turns']
        depthSite = initialDepth + (depthPerTurn*float(tuningDepth))
        print formatTuningHeader.format(subject=subject)
        print formatSessionEphys.format(ephysName=ephysSession)
        print formatTuningEphys.format(tuningEphysName=tuningEphys)
        print clusterTetrodes
        print clusterQuality
        print formatDepth.format(siteDepth = depthSite)
        print formatTuningBehavior.format(behavName=tuningBehav)
        print formatSessionBehavior.format(behavName=(tuningBehav[:-1]+'a'))
        ephysTimeTuning = oneSession['ephysSessionTuning'][-8:]
        print '''cellDB.append_session(oneES)'''#####################################
        #print formatSessionTuning.format(ephysTime=ephysTimeTuning)
    #print formatSessionTraining.format(ephysTime=ephysTimeTraining)
    #print oneSession['type']
        print ''###################################################################


