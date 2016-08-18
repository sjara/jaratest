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

##### For now just plotting one intensity (50dB) for tuning curve data #######
intensityToPlot = 50.0 


###### Make list of all experiments ######
expList=[]

######### d1pi015 ##########
'''
exp = photostimExp.PhotostimSession(animalName='d1pi015',date='2016-08-03', stimHemi='right', ephysSession='12-28-05',tuningSurffix='a',behavSurffix='a', depth=2100, tetrodes=tetrodesDict['d1pi015_righthemi']) #right hemi photostim
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi015',date='2016-08-04', stimHemi='left', ephysSession='13-49-26',tuningSurffix='a',behavSurffix='a', depth=2100, tetrodes=tetrodesDict['d1pi015_lefthemi'])
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi015',date='2016-08-05', stimHemi='right', ephysSession='12-29-14',tuningSurffix='a',behavSurffix='a', depth=2180, tetrodes=tetrodesDict['d1pi015_righthemi']) 
#clustered. T6c2 responsive to 14.3-23.5kHz, T7c2,c3 responsive to 8.8-23.5kHz. T8c4 inhibited 5.4-23.5kHz, T8c6 responsive 14.3-18.3kHz 
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi015',date='2016-08-07', stimHemi='right', ephysSession='16-48-07',tuningSurffix='a',behavSurffix='a', depth=2180, tetrodes=tetrodesDict['d1pi015_righthemi']) 
#clustered, T6c7 look like multiunit activity tuned 8.8-23.5kHz most strong at 14.3kHz; T7c4 waveform not too pretty tuned 11.2-18.3kHz, T7c10&11 tuned 14.3-23.5kHz; T8c2 (multiunit?) tuned 11.2-23.5kHz
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi015',date='2016-08-09', stimHemi='right', ephysSession='14-04-54',tuningSurffix='b',behavSurffix='a', depth=2180, tetrodes=tetrodesDict['d1pi015_righthemi']) 
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi015',date='2016-08-10', stimHemi='left', ephysSession='16-07-12',tuningSurffix='a',behavSurffix='a', depth=2180, tetrodes=tetrodesDict['d1pi015_lefthemi']) 
expList.append(exp)
'''
#exp = photostimExp.PhotostimSession(animalName='d1pi015',date='2016-08-15', stimHemi='right', ephysSession='13-17-45',tuningSurffix='b',behavSurffix='a', depth=2180, tetrodes=tetrodesDict['d1pi015_righthemi']) 
exp = photostimExp.PhotostimSession(animalName='d1pi015',date='2016-08-15', stimHemi='right', ephysSession='13-08-29',tuningSurffix='a',behavSurffix='a', depth=2180, tetrodes=tetrodesDict['d1pi015_righthemi']) 
expList.append(exp)

######### d1pi016 ##########
'''
exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-07-29', stimHemi='right', ephysSession='13-44-18',tuningSurffix='a',behavSurffix='a', depth=2100, tetrodes=tetrodesDict['d1pi016_righthemi'])
expList.append(exp)


exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-07-30', stimHemi='left', ephysSession='12-58-22',tuningSurffix='a',behavSurffix='a', depth=2100, tetrodes=tetrodesDict['d1pi016_lefthemi'])
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-01', stimHemi='left', ephysSession='13-51-14',tuningSurffix='a',behavSurffix='a', depth=2100, tetrodes=tetrodesDict['d1pi016_lefthemi']) 
#clustered. T4c2 responsive 12.1-14.7kHz,T4c5 responsive 8.1-12.2kHz; T5c9 responsive to 26.8kHz
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-02', stimHemi='left', ephysSession='14-29-07',tuningSurffix='a',behavSurffix='a', depth=2100, tetrodes=tetrodesDict['d1pi016_lefthemi'])
expList.append(exp)

#exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-03', stimHemi='right', ephysSession='14-07-35',tuningSurffix='a',behavSurffix='a',depth=2180,tetrodes=tetrodesDict['d1pi016_righthemi']) 
#clustered, T2c7 responsive to all freqs in 2afc

exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-03', stimHemi='right', ephysSession='14-19-09',tuningSurffix='b',behavSurffix='a',depth=2180,tetrodes=tetrodesDict['d1pi016_righthemi']) #clustered, T2 no clear tuning
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-04', stimHemi='right', ephysSession='16-15-43',tuningSurffix='d',behavSurffix='a',depth=2180,tetrodes=tetrodesDict['d1pi016_righthemi'])
expList.append(exp)


exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-05', stimHemi='right', ephysSession='14-10-47',tuningSurffix='a',behavSurffix='a',depth=2260,tetrodes=tetrodesDict['d1pi016_righthemi'])
#clustered. T2c4 noise responsive, responsive at 5.4,6.8,11.2kHz
expList.append(exp)

#exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-06', stimHemi='right', ephysSession='17-06-06',tuningSurffix='c',behavSurffix='a',depth=2260,tetrodes=tetrodesDict['d1pi016_righthemi'])
exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-06', stimHemi='right', ephysSession='16-54-56',tuningSurffix='a',behavSurffix='a',depth=2260,tetrodes=tetrodesDict['d1pi016_righthemi'])
expList.append(exp)

#exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-08', stimHemi='left', ephysSession='16-01-36',tuningSurffix='b',behavSurffix='a',depth=2260,tetrodes=tetrodesDict['d1pi016_lefthemi'])
#clustered. T5c2 may be responsive at 13.9kHz  
exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-08', stimHemi='left', ephysSession='15-55-03',tuningSurffix='a',behavSurffix='a',depth=2260,tetrodes=tetrodesDict['d1pi016_lefthemi'])
#clustered. T5 tuning not obvious 
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-09', stimHemi='left', ephysSession='15-44-24',tuningSurffix='b',behavSurffix='a',depth=2260,tetrodes=tetrodesDict['d1pi016_lefthemi'])
#clustered. T5c9(multiunit?) weakly responsive around 13.9kHz 
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-10', stimHemi='right', ephysSession='13-49-27',tuningSurffix='b',behavSurffix='a',depth=2340,tetrodes=tetrodesDict['d1pi016_righthemi'])
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-11', stimHemi='right', ephysSession='15-27-36',tuningSurffix='b',behavSurffix='a',depth=2340,tetrodes=tetrodesDict['d1pi016_righthemi'])
expList.append(exp)

#exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-12', stimHemi='left', ephysSession='17-10-41',tuningSurffix='c',behavSurffix='a',depth=2260,tetrodes=tetrodesDict['d1pi016_lefthemi'])
exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-12', stimHemi='left', ephysSession='17-06-26',tuningSurffix='b',behavSurffix='a',depth=2260,tetrodes=tetrodesDict['d1pi016_lefthemi'])
expList.append(exp)

exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-13', stimHemi='left', ephysSession='16-15-26',tuningSurffix='b',behavSurffix='a',depth=2260,tetrodes=tetrodesDict['d1pi016_lefthemi'])
#exp = photostimExp.PhotostimSession(animalName='d1pi016',date='2016-08-13', stimHemi='left', ephysSession='16-07-52',tuningSurffix='a',behavSurffix='a',depth=2260,tetrodes=tetrodesDict['d1pi016_lefthemi'])
expList.append(exp)
'''

##### Plot and save tuning and psy curve reports for all experiments ######
for exp in expList:
    
    numberTetrodes=len(exp.tetrodes) 
    plt.subplots(figsize=(20, 8))
    plt.clf()
    #plt.title('%s %s %s hemi depth=%d' %(exp.animalName, exp.date, exp.stimHemi, exp.depth))
    
    for ind,tetrode in enumerate(exp.tetrodes):
        plt.subplot2grid((3,3*(numberTetrodes+1)+1),(0,ind*3),colspan=3,rowspan=3)
        exp.plot_tuning_raster_one_intensity(tetrode,intensityToPlot)
        
    plt.hold(True)
    plt.subplot2grid((3,3*(numberTetrodes+1)+1),(0,3*numberTetrodes),colspan=4,rowspan=3)
    exp.plot_photostim_psycurve()
    plt.tight_layout()
    #plt.subplots_adjust(hspace=0.25, wspace=0.6)
    plt.subplots_adjust(top=0.88)    
    plt.suptitle('%s %s %s hemi depth=%d' %(exp.animalName, exp.date, exp.stimHemi, exp.depth),fontsize=15)
   

    outputDir=os.path.join('/home/languo/data/behavior_reports',exp.animalName) 
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    filename = 'tuning_behavior_summary_%s_%s.%s'%(exp.animalName,exp.date,'png')
    fullFileName = os.path.join(outputDir,filename)
    print 'saving figure to %s'%fullFileName
    plt.gcf().savefig(fullFileName)
    plt.close()
