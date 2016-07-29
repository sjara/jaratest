from jaratoolbox import loadbehavior
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

animals = ['adap012','adap013','adap005']

#experimenter = 'lan'

#if len(sys.argv)>1:
    #sessions = sys.argv[1:]

for animal in animals:
    #timePreSound=np.array([])
    #timeAfterSound=np.array([])
    timeToSideLeft=np.array([])
    timeToSideRight=np.array([])

    if animal == 'adap012':
        experimenter='lan'
        sessions=['20160206a','20160217a','20160301a','20160329a']
    elif animal == 'adap013':
        experimenter='billy'
        sessions=['20160226a','20160316a','20160321a']
    elif animal == 'adap005':
        experimenter='lan'
        sessions=['20151218a','20151222a','20160108a']


    for session in sessions:
        behavFilename=animal+'_2afc_'+session+'.h5' 

        behavPath = '/home/languo/data/behavior/'+experimenter+'/'+animal+'/'+behavFilename

        bdata = loadbehavior.BehaviorData(behavPath)
        ###Get event times, only looking at valid trials###
        valid=bdata['valid']& (bdata['choice']!=bdata.labels['choice']['none'])
        #print valid[0:5]
        #correctTrials = bdata['outcome']==bdata.labels['outcome']['correct']
        #errorTrials = bdata['outcome']==bdata.labels['outcome']['error']
        #invalidTrials = bdata['outcome']==bdata.labels['outcome']['invalid']
        goLeft = bdata['choice']==bdata.labels['choice']['left']
        goRight =  bdata['choice']==bdata.labels['choice']['right']

        timeCenterIn = bdata['timeCenterIn']
        timeTone = bdata['timeTarget']
        timeCenterOut = bdata['timeCenterOut']
        timeSideIn = bdata['timeSideIn'] #invalid trials does not have side in time recorded

        #timePreSoundThis=(timeTone-timeCenterIn) #initiates trial before soundonset
        #timePreSoundThis=timePreSoundThis[valid.astype(bool)]
        #timePreSound=np.concatenate((timePreSound,timePreSoundThis))
        #print len(preSound),preSound[0:5]

        #timeAfterSoundThis=(timeCenterOut-timeTone) #presentation of tone before withdrawal from center port
        #timeAfterSoundThis=timeAfterSoundThis[valid.astype(bool)]
        #timeAfterSound=np.concatenate((timeAfterSound,timeAfterSoundThis))
        #print len(afterSound),afterSound[0:5]

        timeToSideThis=(timeSideIn-timeCenterOut) #executes movement to side port
        timeToSideThisLeft=timeToSideThis[valid.astype(bool)&goLeft]
        timeToSideThisRight=timeToSideThis[valid.astype(bool)&goRight]
        timeToSideLeft=np.concatenate((timeToSideLeft,timeToSideThisLeft))
        timeToSideRight=np.concatenate((timeToSideRight,timeToSideThisRight))

        #print len(timeToSide),timeToSide[0:5], np.mean(timeToSide)

        #centerInToNextTrial=timeCenterIn[1:]-timeSideIn[:-1]
        #centerInToNextTrial=np.insert(centerInToNextTrial,0,0)
        #centerInToNextTrial=centerInToNextTrial[valid.astype(bool)] #This still has NaN values??
        #print len(phase4Length), phase4Length[0:5], np.mean(phase4Length)

 

    plt.figure()
    plt.title(animal+' Time From Center-out To Side-in_Left')
    bins=np.linspace(0.1,1,10)
    plt.hist(timeToSideLeft,bins=bins,facecolor='green')
    plt.figure()
    plt.title(animal+' Time From Center-out To Side-in_Right')
    plt.hist(timeToSideRight,bins=bins,facecolor='blue')
    #line2, = plt.plot(phase2Length,'.b',label='Phase2')
    
    #line3, = plt.plot(phase3Length, '.r',label='Phase3')
    
    #line4, = plt.plot(phase4Length, '.y',label='Phase4')
    
    #plt.legend([line1,line2,line3,line4],loc=2)
    
    #plt.title(behavFilename)

    plt.show()
    
