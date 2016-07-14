import cluster_cutting
from jaratoolbox import settings
import os
import numpy as np



animalName = 'test055'
ephysSession = '2015-05-28_12-49-35'
tetrode = 7
#cluster = 12
Feature = 0
electrodeNumber = 4


ephysRootDir = settings.EPHYS_PATH
dataDir = os.path.join(settings.EPHYS_PATH,animalName,ephysSession)
clustersDir = os.path.join(settings.EPHYS_PATH,animalName,ephysSession+'_kk')
#tetrodeFile = os.path.join(self.dataDir,'Tetrode{0}.spikes'.format(tetrode))
fetFilename = os.path.join(clustersDir,'Tetrode{0}.fet.1'.format(tetrode))
cluFilename =  os.path.join(clustersDir,'Tetrode{0}.clu.1'.format(tetrode))
processedDir = os.path.join(settings.EPHYS_PATH,animalName+'_processed')
cutFilename = os.path.join(processedDir,'cutCluster_'+ephysSession+'_'+'T'+str(tetrode))


cutClusterFile = open(cutFilename, 'w')


for cluster in range(1,13):
    cluFile = open(cluFilename, 'r')
    cluFile.readline()
    totalLineCount = sum(1 for _ in cluFile)
    cluFile.close()

    cluFile = open(cluFilename, 'r')
    cluFile.readline()

    clusterBoolArray = np.zeros([totalLineCount],dtype = bool)

    for lineCount,line in enumerate(cluFile):
        oneCluVal = int(line)
        clusterBoolArray[lineCount] = (oneCluVal == cluster)

    cluFile.close()

    fetFile = open(fetFilename, 'r')
    fetFile.readline()

    featureValues = np.empty([totalLineCount,12])*np.nan



    for lineCount,line in enumerate(fetFile):
        oneFetValStr = line.split()
        oneFetVal = np.array(map(float,oneFetValStr))
        featureValues[lineCount] = oneFetVal#(oneFetVal[(Feature*electrodeNumber):((1+Feature)*electrodeNumber)])

    fetFile.close()

    numClusterSpikes = sum(clusterBoolArray)
    clusterFetVals = featureValues[clusterBoolArray]

    cw = cluster_cutting.ClusterCutter(clusterFetVals[:,0:4])

    raw_input('press Enter to finish cutting...')

    cut_spikes = cw.output_cut_points()

    cutClusterBoolArray = np.zeros([totalLineCount],dtype = bool)
    cutClusterCount = 0
    for cluCount,spikeBool in enumerate(clusterBoolArray):
        if spikeBool:
            cutClusterBoolArray[cluCount] = cut_spikes[cutClusterCount]
            cutClusterCount+=1

    cutClusterFile.write(cutClusterBoolArray)
    cutClusterFile.write('\n')

cutClusterFile.close()
