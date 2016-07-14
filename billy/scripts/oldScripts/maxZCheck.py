import allcells_test017_quality as allcells
from jaratoolbox import settings
import os

clusNum = 12 #Number of clusters that Klustakwik speparated into

class nestedDict(dict):
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value


subject = allcells.cellDB[0].animalName
processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')
maxZFilename = os.path.join(processedDir,'maxZVal.txt')
maxZFile = open(maxZFilename, 'r')

maxZFile.readline()
maxZDict = nestedDict()
behavName = ''
for line in maxZFile:
    behavLine = line.split(':')
    freqLine = line.split()
    if (behavLine[0] == 'Behavior Session'):
        behavName = behavLine[1][:-1]
    else:
        maxZDict[behavName][freqLine[0]] = freqLine[1].split(',')[0:-1]

maxZFile.close()

behavSession = raw_input("behavior session")
freq = raw_input("frequency")
print behavSession
print freq
numVal = len(maxZDict[behavSession][freq])
count = 0
while (count<numVal): 
    print (count+1),' ',maxZDict[behavSession][freq][count]
    count +=1
    raw_input("Press Enter...")
