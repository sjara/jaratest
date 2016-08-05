'''
This script contain all the photostim experiments I conducted with d1pi mice (bilateral fiber+4tetrode implanted targetting auditory striatum)

Lan Guo 20160803
'''
import os
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from jaratest.lan import test053_photostim_ephys_behav_container as photostimExp
reload(photostimExp)

##### Mapping tetrodes to hemisphere in each mice ######
tetrodesDict={'d1pi015_righthemi':[5,6,7,8], 'd1pi015_lefthemi':[1,2,3,4], 'd1pi016_righthemi':[1,2,7,8], 'd1pi016_lefthemi':[3,4,5,6]}

##### For now just plotting one intensity 50dB #######
intensityToPlot = 50.0 


###### Make list of all experiments ######
expList=[]

######### d1pi015 ##########
'''
exp = photostimExp.PhotostimSession(animalName='d1pi015',date='2016-08-03',ephysSession='12-28-05',tuningSurffix='a',behavSurffix='a',tetrodes=tetrodesDict['d1pi015_righthemi']) #right hemi photostim
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi015',date='2016-08-04',ephysSession='13-49-26',tuningSurffix='a',behavSurffix='a',tetrodes=tetrodesDict['d1pi015_lefthemi']) #right hemi photostim
expList.append(exp)
'''

######### d1pi015 ##########
exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-07-29',ephysSession='13-44-18',tuningSurffix='a',behavSurffix='a',tetrodes=tetrodesDict['d1pi016_righthemi'])
expList.append(exp)

'''
exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-07-30',ephysSession='12-58-22',tuningSurffix='a',behavSurffix='a',tetrodes=tetrodesDict['d1pi016_lefthemi'])
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-01',ephysSession='13-51-14',tuningSurffix='a',behavSurffix='a',tetrodes=tetrodesDict['d1pi016_lefthemi'])
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-02',ephysSession='14-29-07',tuningSurffix='a',behavSurffix='a',tetrodes=tetrodesDict['d1pi016_lefthemi'])
expList.append(exp)

#exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-03',ephysSession='14-07-35',tuningSurffix='a',behavSurffix='a',tetrodes=tetrodesDict['d1pi016_righthemi'])
exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-03',ephysSession='14-19-09',tuningSurffix='b',behavSurffix='a',tetrodes=tetrodesDict['d1pi016_righthemi'])
expList.append(exp)
'''
exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-04',ephysSession='16-15-43',tuningSurffix='d',behavSurffix='a',tetrodes=tetrodesDict['d1pi016_righthemi'])
expList.append(exp)


##### Plot and save tuning and psy curve reports for all experiments ######
for exp in expList:
    
    numberTetrodes=len(exp.tetrodes) 
    plt.subplots(figsize=(20, 8))
    plt.clf()
    #gs = gridspec.GridSpec(1,1+numberTetrodes)
    for ind,tetrode in enumerate(exp.tetrodes):
        plt.subplot2grid((3,3*(numberTetrodes+1)+1),(0,ind*3),colspan=3,rowspan=3)
        exp.plot_tuning_raster_one_intensity(tetrode,intensityToPlot)
        #plt.subplots_adjust(hspace=0.25, wspace=0.6)
    plt.hold(True)
    plt.subplot2grid((3,3*(numberTetrodes+1)+1),(0,3*numberTetrodes),colspan=4,rowspan=3)
    exp.plot_photostim_psycurve()
    plt.tight_layout()
    #plt.subplots_adjust(hspace=0.25, wspace=0.6)
    plt.title('%s %s' %(exp.animalName, exp.date))
    plt.show()

    outputDir=os.path.join('/home/languo/data/behavior_reports',exp.animalName) 
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    filename = 'tuning_behavior_summary_%s_%s.%s'%(exp.animalName,exp.date,'png')
    fullFileName = os.path.join(outputDir,filename)
    print 'saving figure to %s'%fullFileName
    plt.gcf().savefig(fullFileName)
    plt.close()
