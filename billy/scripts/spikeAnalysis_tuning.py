
'''
Example of using spikesorting module (which uses KlustaKwik) for spike sorting
'''

from jaratoolbox import spikesorting
from jaratoolbox import settings
import numpy as np
import sys
import importlib


mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to usec
allcellsFileName = 'allcells_'+mouseName+'_tuning'###########################################
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

outputDir = '/home/billywalker/data/ephys/tuning'##############################################
nameOfFile = 'ISI_Violations'



animalName = allcells.cellDB[0].animalName

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
numTetrodes = 8
numClusters = 12 #THIS IS KIND OF A HACK ASSUMING THERES 12 CLUSTERS ALL THE TIME

ISIviolationsDict = {}

ephysSessionEachCell = []
for cellID in range(0,numOfCells):
    ephysSessionEachCell.append(allcells.cellDB[cellID].ephysSession)

ephysSessionArray = np.unique(ephysSessionEachCell)

badSessionList = []#prints the sessions that crash
'''
for indEphys,ephysSession in enumerate(ephysSessionArray):
    try:
        ISIviolationsDict.update({ephysSession:np.empty([numTetrodes,numClusters])})
        for tetrode in range(1,(numTetrodes+1)):
            oneTT = spikesorting.TetrodeToCluster(animalName,ephysSession,tetrode,features=['peak','valleyFirstHalf'])#,'energySpikeFirstHalf2'])#'energyAllZeros'
            print 'here'
            oneTT.create_fet_files()
            oneTT.run_clustering()
            oneTT.save_report()
            ISIviolationsDict[ephysSession][tetrode-1]= oneTT.get_ISI_values() #you can only get the ISI values after running save_report()
    except:
        print "error with session "+ephysSession
        if (ephysSession not in badSessionList):
            badSessionList.append(ephysSession)
'''
for indEphys,ephysSession in enumerate(ephysSessionArray):
    #try:
        for tetrode in range(1,(numTetrodes+1)):
            oneTT = spikesorting.TetrodeToCluster(animalName,ephysSession,tetrode,features=['peak','valleyFirstHalf'])
            oneTT.create_fet_files()
            oneTT.run_clustering()
            oneTT.save_report('cluster_report_tuning')
    #except:
        #print "error with session "+ephysSession
        #if (ephysSession not in badSessionList):
            badSessionList.append(ephysSession)

#for session in badSessionList:
    #print session
        #oneTT.save_report()
        #ISIviolationsDict[ephysSession][tetrode-1]= oneTT.get_ISI_values() #you can only get the ISI values after running save_report()


'''
finalOutputDir = outputDir+'/'+animalName+'_processed'
ISIDict = {}
prevISIList = [] #List of behavior sessions that already have ISI values calculated
try:
    text_file = open("%s/%s.txt" % (finalOutputDir,nameOfFile), "r+") #open a text file to read and write in
    ephysName = ''
    for line in text_file:
        ephysLine = line.split(':')
        if (ephysLine[0] == 'Ephys Session'):
            ephysName = ephysLine[1][:-1]
            prevISIList.append(ephysName)

except:
    text_file = open("%s/%s.txt" % (finalOutputDir,nameOfFile), "w") #open a text file to read and write in


for indEphys,ephysSession in enumerate(ephysSessionArray):
    if ((ephysSession in prevISIList) or (ephysSession in badSessionList)):
        continue
    else:
        text_file.write("Ephys Session:%s\n" % ephysSession)
        ISIArray = ISIviolationsDict[ephysSession]
        for indTetrode,ISIlist in enumerate(ISIArray):
            text_file.write("tetrode:%s" % indTetrode)
            for ISIval in ISIlist:
                text_file.write(" %s" % ISIval)
            text_file.write("\n")

text_file.close()
'''
