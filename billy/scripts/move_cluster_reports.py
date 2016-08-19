import os
import sys
import glob
from jaratoolbox import settings

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use  


fileName = 'multisession_cluster_reports'
copyToDir = '/home/billywalker/data/ephys/'+fileName+'/'+mouseName+'/'
if not os.path.exists(copyToDir):
    os.makedirs(copyToDir)

#'/home/billywalker/data/ephys/'
mainDir = settings.EPHYS_PATH+mouseName+'/'

for multiFolder in glob.glob(mainDir+'multi*'):
    for clusterReport in glob.glob(multiFolder+'/[1-8].png'):
        clusterDay = clusterReport.split('_')[1]
        clusterNum = clusterReport.split('/')[-1]
        newFilename = copyToDir+mouseName+'_'+clusterDay+'_'+clusterNum
        os.system('cp '+clusterReport+' '+newFilename)
        print newFilename

        
    

#os.system('cp /home/billywalker/Pictures/switching_tuning_reports/%s/tuning_report_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/switching_tuning_reports/%s/%s/' % (subject,subject,behavSession,str(tetrode),str(cluster),subject,minFileName))#############################################################################
