'''
Translate information from wiki page of Billy's recorded animals to allcells file. This allcells file includes depth, tuning, and quality of clusters.
'''


import re

#common to all allcells files
formatAllcells='''from jaratest.billy.scripts import celldatabase_quality_tuning as celldatabase\n

eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code\n

cellDB = celldatabase.CellDatabase()\n
'''


# --- Define string format ---

############################## THIS IS FOR THE CORRECT DEPTH #######################################

initialDepth = 2 # initial depth of tetrodes when implanting in mm
depthPerTurn = 0.317 #in mm, one turn is 0.317 mm

####################################################################################################


#formatExperiment = '''exp = cellDB.Experiment(animalName='{subject}', date ='{date}', experimenter='{experimenter}', defaultParadigm='{defparadigm}')'''
#formatSite = '''site1 = exp.add_site(depth={depth}, tetrodes=[1,2,3,4,5,6,7,8])'''
#formatSessionTraining = '''site1.add_session('{ephysTime}', 'a', sessionTypes['2afc'], paradigm='2afc')'''
#formatSessionTuning = '''site1.add_session('{ephysTime}', 'a', sessionTypes['tc'])'''

formatHeader = '''oneES = eSession(animalName='{subject}',\n'''
formatSessionEphys = '''                 ephysSession = '{ephysName}',\n'''
formatTuningEphys = '''                 tuningSession = '{tuningEphysName}',\n'''
clusterTetrodes = '''                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},\n'''
clusterQuality = '''                 clusterQuality = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]},\n'''
formatDepth = '''                 depth = {siteDepth},\n'''
formatTuningBehavior = '''                 tuningBehavior = '{behavName}',\n'''
formatSessionBehavior = '''                 behavSession = '{behavName}')\n'''


# --- Read Billy's wiki info ---

subject = 'adap024'
filename = '{0}_wiki.txt'.format(subject) #text file that contains wiki data
content = [line.rstrip('\n') for line in open(filename)]

### re.search(r'\* \d.\d+ turns, \d\d\d\d-\d\d-\d\d', oneline).group()

trainingDateLine = re.compile(r'\*  (\d.\d+) turns, (\d\d\d\d-\d\d-\d\d)')
tuningLine = re.compile(r'\* (\d.\d+) turns, presented frequencies')
ephysLine = re.compile(r'\*\* ephys recording name: (\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d)')
behavLine = re.compile(r'\*\* behavior recording name: \w{7}_tuning_curve_(\d\d\d\d\d\d\d\d\w).h5')

switchingLine = re.compile(r'\*\* Switching task') #This has to be set to 'psychometric or switching for billy's mice. !!No mice did both tasks!!

dbase = {}


def test_turns(sessionDate, oneSession,lastTurns):
    if oneSession.has_key('turns'):
        try:
            assert float(oneSession['turns'])==float(lastTurns)
        except AssertionError:
            print 'WARNING! Turns do not match for {0}: {1} , {2}'.format(sessionDate,lastTurns,
                                                                          oneSession['turns'])

sessionDate= ''
for indline,oneline in enumerate(content):
    matchEphys = ephysLine.search(oneline)
    #matchBehav = behavLine.search(oneline)
   
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
            matchSwitching = switchingLine.search(content[indline+4])
            if matchSwitching:
                dbase[sessionDate].update({'type':'switching'})
            else:
                dbase[sessionDate].update({'type':'psycurve'})
        elif matchTuning:
            lastTurns = matchTuning.groups()[0]
            test_turns(sessionDate, dbase[sessionDate],lastTurns)
            dbase[sessionDate].update({'turns':lastTurns,'ephysSessionTuning':ephysSession,'behavSessionTuning':matchBehav.groups()[0]})
           

# --- Write allcell file's format ---
outputFilePath = '/home/languo/src/jaratest/lan/Allcells/allcells_{0}_quality.py'.format(subject)
outputFile = open(outputFilePath, 'w')
 
outputFile.write(formatAllcells)

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
        
        outputFile.write(formatHeader.format(subject=subject))
        outputFile.write(formatSessionEphys.format(ephysName=ephysSession))
        outputFile.write(formatTuningEphys.format(tuningEphysName=tuningEphys))
        outputFile.write(clusterTetrodes)
        outputFile.write(clusterQuality)
        outputFile.write(formatDepth.format(siteDepth = depthSite))
        outputFile.write(formatTuningBehavior.format(behavName=tuningBehav))
        outputFile.write(formatSessionBehavior.format(behavName=(tuningBehav[:-1]+'a')))
        #ephysTimeTuning = oneSession['ephysSessionTuning'][-8:]
        outputFile.write('cellDB.append_session(oneES)\n')
        #print formatSessionTuning.format(ephysTime=ephysTimeTuning)
    #print formatSessionTraining.format(ephysTime=ephysTimeTraining)
    #print oneSession['type']
        outputFile.write('\n')


