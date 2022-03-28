'''
Change Detection Task in Freely Moving Rigs
'''
import time
import os
import numpy as np
from qtpy import QtWidgets
from taskontrol import rigsettings
from taskontrol import dispatcher
from taskontrol import statematrix
from taskontrol import savedata
from taskontrol import paramgui
from taskontrol import utils
from taskontrol.plugins import templates
from taskontrol.plugins import performancedynamicsplot
from taskontrol.plugins import soundclient
from taskontrol.plugins import speakercalibration


LONGTIME = 100

PUNISHMENT_DURATION = 0.5

#SOUND_DIR = '../jarasounds/fmsounds'
#soundFilesStr = 'fm_{0}Hz_f{1}_{2}s_{3:03.0f}.wav'

if 'outBit1' in rigsettings.OUTPUTS:
    trialStartSync = ['outBit1'] # Sync signal for trial-start.
else:
    trialStartSync = []
if 'outBit0' in rigsettings.OUTPUTS:
    stimSync = ['outBit0'] # Sync signal for sound stimulus
else:
    stimSync = []
    
class Paradigm(templates.Paradigm2AFC):
    def __init__(self,parent=None, paramfile=None, paramdictname=None):
        super(Paradigm, self).__init__(parent)
        
        #Performance Dynamics Plot
        performancedynamicsplot.set_pg_colors(self)
        self.myPerformancePlot = performancedynamicsplot.PerformanceDynamicsPlot(nTrials=400,winsize=10)
        
        #Add Parameters
        self.params['timeWaterValveL'] = paramgui.NumericParam('Time valve left',value=0.03,
                                                                units='s',group='Water delivery')
        self.params['timeWaterValveC'] = paramgui.NumericParam('Time valve center',value=0.03,
                                                                units='s',group='Water delivery')
        self.params['timeWaterValveR'] = paramgui.NumericParam('Time valve right',value=0.03,
                                                                units='s',group='Water delivery')
        waterDelivery = self.params.layout_group('Water delivery')
        
        self.params['outcomeMode'] = paramgui.MenuParam('Outcome mode',
                                                        ['sides_direct', 'direct', 'on_next_correct',
                                                         'only_if_correct', 'on_any_poke', 'passive_exposure'],
                                                         value=3,group='Choice parameters')
        self.params['activePort'] = paramgui.MenuParam('Active port',
                                                        ['both','left','right'],
                                                         value=0, group='Choice parameters')
        self.params['fractionRewarded'] = paramgui.NumericParam('Fraction rewarded',
                                                        value=1, units='',group='Choice parameters')
        self.params['allowEarlyWithdrawal'] = paramgui.MenuParam('Allow early withdraw',
                                                                 ['off','on'], enabled=True,
                                                                 value=1, group='Choice parameters')
        self.params['antibiasMode'] = paramgui.MenuParam('Anti-bias mode',
                                                        ['off','repeat_mistake'],
                                                        value=0,group='Choice parameters')
        choiceParams = self.params.layout_group('Choice parameters')
        
        self.params['delayToTargetMean'] = paramgui.NumericParam('Mean delay to target',value=0.2,
                                                                 units='s',decimals=3, group='Timing parameters')
        self.params['delayToTargetHalfRange'] = paramgui.NumericParam('+/-',value=0.05,
                                                        units='s',group='Timing parameters')
        self.params['delayToTarget'] = paramgui.NumericParam('Delay to target',value=0.2,
                                                        units='s',group='Timing parameters',
                                                        enabled=False,decimals=3)
        self.params['targetDuration'] = paramgui.NumericParam('Target duration',value=0.2,
                                                              units='s',group='Timing parameters',enabled=True)
        self.params['rewardAvailability'] = paramgui.NumericParam('Reward availability',value=4,
                                                        units='s',group='Timing parameters')
        self.params['punishTimeError'] = paramgui.NumericParam('Punishment (error)',value=0,
                                                        units='s',group='Timing parameters')
        self.params['punishTimeEarly'] = paramgui.NumericParam('Punishment (early)',value=0.5,
                                                        units='s',group='Timing parameters')
        timingParams = self.params.layout_group('Timing parameters')
        
        self.params['relevantFeature'] = paramgui.MenuParam('Relevant feature',
                                                         ['spectral','temporal'],
                                                            value=0,group='Categorization parameters', enabled=False)
        self.params['soundActionMode'] = paramgui.MenuParam('Sound-action mode',
                                                            ['low_left','high_left'],
                                                            value=0,group='Categorization parameters', enabled=False)
        categorizationParams = self.params.layout_group('Categorization parameters')

        self.params['maxNtrials'] = paramgui.NumericParam('Max N trials',value=4000,decimals=0,
                                                             group='Automation',enabled=True)
        self.params['postSoundDelay'] = paramgui.NumericParam('Delay after sound',value=0.3,
                                                              units='s',group='Automation', enabled=False)
        self.params['interTrialInterval'] = paramgui.NumericParam('Inter-trial interval',value=1.5,
                                                        units='s',group='Automation', enabled=False)
        self.params['automationMode'] = paramgui.MenuParam('Automation Mode',
                                                           ['off','increase_delay'],
                                                           value=0,group='Automation')
        automationParams = self.params.layout_group('Automation')
        
        self.params['highFreq'] = paramgui.NumericParam('High frequency', value=13000, units='Hz',
                                                        group='Sound parameters')
        self.params['lowFreq'] = paramgui.NumericParam('Low frequency', value=6000, units='Hz',
                                                        group='Sound parameters')
        self.params['startFreq'] = paramgui.NumericParam('Start frequency', value=0, units='Hz', decimals=0,
                                                         enabled=False, group='Sound parameters')
        self.params['endFreq'] = paramgui.NumericParam('End frequency', value=0, units='Hz', decimals=0,
                                                         enabled=False, group='Sound parameters')
        self.params['targetFMslope'] = paramgui.NumericParam('Target FM slope', value=1,
                                                             decimals=2, units='', enabled=False,
                                                             group='Sound parameters')
        self.params['nFreqs'] = paramgui.NumericParam('N frequencies', value=6, units='',
                                                        group='Sound parameters')
        self.params['minFreqRatio'] = paramgui.NumericParam('Min freq ratio', value=2.0, units='',
                                                        group='Sound parameters')
        self.params['preFreq'] = paramgui.NumericParam('Pre frequency', value=0,
                                                               decimals=0, units='Hz', enabled=False,
                                                               group='Sound parameters')
        self.params['postFreq'] = paramgui.NumericParam('Post frequency', value=0,
                                                               decimals=0, units='Hz', enabled=False,
                                                               group='Sound parameters')
        self.params['preDuration'] = paramgui.NumericParam('Pre duration', value=1.0, units='s',
                                                              group='Sound parameters')
        self.params['postDuration'] = paramgui.NumericParam('Post duration', value=1.0, units='s',
                                                              group='Sound parameters')
        self.params['preSoundAmplitude'] = paramgui.NumericParam('Pre sound amplitude',value=0.0,
                                                                 units='[0-1]', enabled=False,
                                                                 decimals=4, group='Sound parameters')
        self.params['postSoundAmplitude'] = paramgui.NumericParam('Post sound amplitude',value=0.0,
                                                                  units='[0-1]',enabled=False,
                                                                  decimals=4, group='Sound parameters')
        self.params['targetIntensityMode'] = paramgui.MenuParam('Intensity mode',
                                                                ['fixed','randMinus20'],
                                                                value=0,group='Sound parameters')
        # This intensity corresponds to the intensity of each component of the chord
        self.params['targetMaxIntensity'] = paramgui.NumericParam('Max intensity',value=70,
                                                                  units='dB-SPL',group='Sound parameters')
        self.params['targetIntensity'] = paramgui.NumericParam('Intensity',value=0.0,units='dB-SPL',
                                                               enabled=False,group='Sound parameters')
        self.params['targetAmplitude'] = paramgui.NumericParam('Target amplitude',value=0.0,units='[0-1]',
                                                        enabled=False,decimals=4,group='Sound parameters')
        self.params['punishSoundIntensity'] = paramgui.NumericParam('Punish intensity',value=50,
                                                              units='dB-SPL',enabled=True,
                                                              group='Sound parameters')
        self.params['punishSoundAmplitude'] = paramgui.NumericParam('Punish amplitude',value=0.01,
                                                              units='[0-1]',enabled=False,
                                                              group='Sound parameters')
        soundParams = self.params.layout_group('Sound parameters')
        
        
        self.params['nValid'] = paramgui.NumericParam('N valid',value=0,
                                                      units='',enabled=False,
                                                      group='Report')
        self.params['nRewarded'] = paramgui.NumericParam('N rewarded',value=0,
                                                         units='',enabled=False,
                                                         group='Report')
        reportParams = self.params.layout_group('Report')

        #
        self.params['experimenter'].set_value('santiago')
        self.params['subject'].set_value('test')
        
        # -- Add graphical widgets to main window --
        self.centralWidget = QtWidgets.QWidget()
        layoutMain = QtWidgets.QVBoxLayout()
        layoutTop = QtWidgets.QVBoxLayout()
        layoutBottom = QtWidgets.QHBoxLayout()
        layoutCol1 = QtWidgets.QVBoxLayout()
        layoutCol2 = QtWidgets.QVBoxLayout()
        layoutCol3 = QtWidgets.QVBoxLayout()
        layoutCol4 = QtWidgets.QVBoxLayout()

        layoutMain.addLayout(layoutTop)
        layoutMain.addSpacing(0)
        layoutMain.addLayout(layoutBottom)

        layoutTop.addWidget(self.mySidesPlot)
        layoutTop.addWidget(self.myPerformancePlot)

        layoutBottom.addLayout(layoutCol1)
        layoutBottom.addLayout(layoutCol2)
        layoutBottom.addLayout(layoutCol3)
        layoutBottom.addLayout(layoutCol4)

        layoutCol1.addWidget(self.saveData)
        layoutCol1.addWidget(self.sessionInfo)
        layoutCol1.addWidget(self.dispatcher.widget)

        layoutCol2.addWidget(self.manualControl)
        layoutCol2.addStretch()
        layoutCol2.addWidget(waterDelivery)
        layoutCol2.addStretch()
        layoutCol2.addWidget(choiceParams)
        layoutCol2.addStretch()

        layoutCol3.addWidget(timingParams)
        layoutCol3.addStretch()
        layoutCol3.addWidget(categorizationParams)
        layoutCol3.addStretch()
        layoutCol3.addWidget(automationParams)
        layoutCol3.addStretch()


        layoutCol4.addWidget(soundParams)
        layoutCol4.addStretch()
        layoutCol4.addWidget(reportParams)
        layoutCol4.addStretch()

        self.centralWidget.setLayout(layoutMain)
        self.setCentralWidget(self.centralWidget)
        
        maxNtrials = 4000 # Preallocating space for each vector makes things easier
        self.results = utils.EnumContainer()
        self.results.labels['rewardSide'] = {'left':0,'right':1}
        self.results['rewardSide'] = np.random.randint(2,size=maxNtrials)
        self.results.labels['choice'] = {'left':0,'right':1,'none':2}
        self.results['choice'] = np.empty(maxNtrials,dtype=int)
        self.results.labels['outcome'] = {'correct':1,'error':0,'invalid':2,
                                          'free':3,'nochoice':4,'aftererror':5,'aborted':6}
        self.results['outcome'] = np.empty(maxNtrials,dtype=int)
        # Saving outcome as bool creates an 'enum' vector, so I'm saving as 'int'
        self.results['valid'] = np.zeros(maxNtrials,dtype='int8') # redundant but useful
        self.results['timeTrialStart'] = np.empty(maxNtrials,dtype=float)
        self.results['timeTarget'] = np.empty(maxNtrials,dtype=float)
        self.results['timeCenterIn'] = np.empty(maxNtrials,dtype=float)
        self.results['timeCenterOut'] = np.empty(maxNtrials,dtype=float)
        self.results['timeSideIn'] = np.empty(maxNtrials,dtype=float)

        # -- Load parameters from a file --
        self.params.from_file(paramfile,paramdictname)

        # -- Load speaker calibration --
        self.sineCal = speakercalibration.Calibration(rigsettings.SPEAKER_CALIBRATION_SINE)
        self.chordCal = speakercalibration.Calibration(rigsettings.SPEAKER_CALIBRATION_CHORD)
        self.noiseCal = speakercalibration.NoiseCalibration(rigsettings.SPEAKER_CALIBRATION_NOISE)
        
        print('Conecting to soundserver (waiting for 200ms) ...')
        time.sleep(0.2)
        self.soundClient = soundclient.SoundClient()
        self.targetSoundID = 1
        self.punishSoundID = 3   
        self.soundClient.start()

        # -- Specify state matrix with extratimer --
        self.sm = statematrix.StateMatrix(inputs=rigsettings.INPUTS,
                                          outputs=rigsettings.OUTPUTS,
                                          readystate='readyForNextTrial',
                                          extratimers=['laserTimer'])
    
    def prepare_sounds(self):
        #targetFrequency = 6000
        soundIntensity = self.params['soundIntensity'].get_value()
        # FIXME: currently I am averaging calibration from both speakers (not good)
        preFreq = self.params['preFreq'].get_value()
        postFreq = self.params['postFreq'].get_value()
        preSoundAmp = self.spkCal.find_amplitude(preFreq,soundIntensity).mean()
        postSoundAmp = self.spkCal.find_amplitude(postFreq,soundIntensity).mean()
        self.params['preSoundAmplitude'].set_value(preSoundAmp)
        self.params['postSoundAmplitude'].set_value(postSoundAmp)
        preDuration = self.params['preDuration'].get_value()
        postDuration = self.params['postDuration'].get_value()
        sPre = {'type':'chord', 'frequency':preFreq, 'ntones':12, 'factor':1.2,
                'duration':preDuration, 'amplitude':preSoundAmp}
        sPost = {'type':'chord', 'frequency':postFreq, 'ntones':12, 'factor':1.2,
                 'duration':postDuration, 'amplitude':postSoundAmp} #, 'delay':preDuration}
        self.soundClient.set_sound(self.preSoundID, sPre)
        self.soundClient.set_sound(self.postSoundID,sPost)

        # -- Prepare punishment noise --
        punishIntensity = self.params['punishIntensity'].get_value()
        targetAmp = self.noiseCal.find_amplitude(punishIntensity).mean()
        sNoise = {'type':'noise', 'duration': PUNISHMENT_DURATION, 'amplitude':targetAmp}
        self.soundClient.set_sound(self.punishSoundID,sNoise)
        
    def prepare_next_trial(self, nextTrial):
        # -- Calculate results from last trial (update outcome, choice, etc) --
        if nextTrial>0:
            self.params.update_history()
            self.calculate_results(nextTrial-1)
            
        # -- Prepare next trial --
        taskMode = self.params['taskMode'].get_string()
        rewardAvailability = self.params['rewardAvailability'].get_value()
        preDuration = self.params['preDuration'].get_value()
        postDuration = self.params['postDuration'].get_value()
        soundDuration = preDuration + postDuration
        timeWaterValve = self.params['timeWaterValve'].get_value()
        interTrialIntervalMean = self.params['interTrialIntervalMean'].get_value()
        interTrialIntervalHalfRange = self.params['interTrialIntervalHalfRange'].get_value()
        randNum = (2*np.random.random(1)[0]-1)
        interTrialInterval = interTrialIntervalMean + randNum*interTrialIntervalHalfRange
        self.params['interTrialInterval'].set_value(interTrialInterval)
    
    def set_state_matrix(self,nextCorrectChoice):
        self.sm.reset_transitions()

        laserDuration = self.params['laserDuration'].get_value()
        self.sm.set_extratimer('laserTimer', duration=laserDuration)

        if self.params['laserTrial'].get_value():
            laserOutput = ['stim1','stim2']
        else:
            laserOutput = []

        targetDuration = self.params['targetDuration'].get_value()
        relevantFeature = self.params['relevantFeature'].get_string()
        stimOutput = stimSync+laserOutput
        if nextCorrectChoice==self.results.labels['rewardSide']['left']:
            rewardDuration = self.params['timeWaterValveL'].get_value()
        lastRewardSide = self.params['rewardSide'].get_string()
        rewardSideMode = self.params['rewardSideMode'].get_string()
        possibleSides = ['left','right']
        if rewardSideMode=='sides_direct':
            if lastRewardSide=='left':
                nextRewardSide = 'right'
            else:
                nextRewardSide = 'left'
        elif rewardSideMode=='only_if_correct':
            nextRewardSide = possibleSides[np.random.randint(2)]
        elif rewardSideMode=='onlyL':
                nextRewardSide = 'left'
        elif rewardSideMode=='onlyR':
                nextRewardSide = 'right'
        
        maxFreq = self.params['maxFreq'].get_value()
        minFreq = self.params['minFreq'].get_value()
        nFreqs = self.params['nFreqs'].get_value()
        allFreq = np.logspace(np.log10(minFreq),np.log10(maxFreq),nFreqs)
        randPre = np.random.randint(nFreqs)  # Which sound will be the "pre" sound
        preFreq = allFreq[randPre]
        minRatio = self.params['minFreqRatio'].get_value() # Min ratio between pre and post frequency
        possiblePostBool = np.logical_or( (preFreq/allFreq)>=minRatio, (allFreq/preFreq)>=minRatio )
        possiblePostInds = np.flatnonzero(possiblePostBool)
        #print('=======================================')
        #print(possiblePostInds)
        if len(possiblePostInds)==0:
            self.dispatcherView.stop()
            raise ValueError('There are no frequencies in the range far enough'+\
                             ' from {:0.0f} Hz.'.format(allFreq[randPre]))
        randPost = np.random.choice(possiblePostInds)
        #allFreq = [minFreq, maxFreq]
        #randPre = np.random.randint(2)  # Which sound will be the "pre" sound
        randNum = (2*np.random.random(1)[0]-1) # In range [-1,1)
        delayToTarget = self.params['delayToTargetMean'].get_value() + \
            self.params['delayToTargetHalfRange'].get_value()*randNum
        self.params['delayToTarget'].set_value(delayToTarget)
        rewardAvailability = self.params['rewardAvailability'].get_value()
        punishTimeError = self.params['punishTimeError'].get_value()
        punishTimeEarly = self.params['punishTimeEarly'].get_value()
        allowEarlyWithdrawal = self.params['allowEarlyWithdrawal'].get_string()

        if nextRewardSide=='left':
            self.params['rewardSide'].set_string('left')
            rewardedEvent = 'Lin'
            punishedEvent = 'Rin'
            rewardOutput = 'leftWater'
            postFreq = preFreq
            stateAfterPre = 'morePre'
            timeInWaitForLick = rewardAvailability
            timeInPost = postDuration
            timeInMorePost = 0
            stateAfterPost = 'waitForLick'
            correctSidePort = 'Lin'
        elif nextRewardSide=='right':
            self.params['rewardSide'].set_string('right')
            rewardEvent = 'Rin'
            punishedEvent = 'Lin'
            rewardOutput = 'rightWater'
            correctSidePort = 'Rin'
            postFreq = allFreq[randPost]
            stateAfterPre = 'playPost'
            timeInWaitForLick = max(0,rewardAvailability-postDuration)
            timeInMorePost = max(0,postDuration-rewardAvailability)
            timeInPost = postDuration-timeInMorePost
            if rewardAvailability > postDuration:
                # If rewardAvailability > postDuration, finish post and go to waitForLick
                stateAfterPost = 'waitForLick'
            else:
                # If rewardAvailability < postDuration, make post shorter
                # (but continue playing sound) and go to morePost (with no reward)
                stateAfterPost = 'morePost'
                
        if self.params['punishMode'].get_string()=='noise':
            punishSoundID = self.punishSoundID
        else:
            punishSoundID = soundclient.STOP_ALL_SOUNDS
        
        self.params['preFreq'].set_value(preFreq)
        self.params['postFreq'].set_value(postFreq)
        self.prepare_sounds()

        self.sm.reset_transitions()
        
        
         # -- Set state matrix --
        outcomeMode = self.params['outcomeMode'].get_string()
        outcomeMode = self.params['outcomeMode'].get_string()
        if outcomeMode=='passive_exposure':
            self.sm.add_state(name='startTrial', statetimer=0,
                              transitions={'Tup':'waitForCenterPoke'},
                              outputsOn=trialStartSync)
            self.sm.add_state(name='waitForCenterPoke', statetimer=delayToTarget,
                              transitions={'Tup':'playStimulus'})
            self.sm.add_state(name='playStimulus', statetimer=targetDuration,
                              transitions={'Tup':'iti'},
                              outputsOn=stimOutput,serialOut=self.targetSoundID,
                              outputsOff=trialStartSync)
            self.sm.add_state(name='iti', statetimer=rewardAvailability,
                              transitions={'Tup':'readyForNextTrial'},
                              outputsOff=stimOutput)
        elif outcomeMode=='on_any_poke':
            rewardedTrial = np.random.random(1)[0] < self.params['fractionRewarded'].get_value()
            if rewardedTrial:
                rewardNorewardState = 'reward'
            else:
                rewardNorewardState = 'noReward'
            activePort = self.params['activePort'].get_string()
            activeOutput = activePort+'Water'
            if activePort=='left':
                activeEvent = 'Lin'
            elif activePort=='right':
                activeEvent = 'Rin'
            else:
                activeEvent = 'Cin'
        if outcomeMode=='sides_direct':
            self.sm.add_state(name='startTrial', statetimer=0,
                              transitions={'Tup':'waitForCenterPoke'},
                              outputsOn=trialStartSync)
            self.sm.add_state(name='waitForCenterPoke', statetimer=LONGTIME,
                              transitions={'Cin':'playStimulus', correctSidePort:'playStimulus'})
            self.sm.add_state(name='playStimulus', statetimer=targetDuration,
                              transitions={'Tup':'reward'},
                              outputsOn=stimOutput,serialOut=self.targetSoundID,
                              outputsOff=trialStartSync)
            self.sm.add_state(name='reward', statetimer=rewardDuration,
                              transitions={'Tup':'stopReward'},
                              outputsOn=[rewardOutput],
                              outputsOff=stimOutput)
            self.sm.add_state(name='stopReward', statetimer=0,
                              transitions={'Tup':'readyForNextTrial'},
                              outputsOff=[rewardOutput])
            postSoundDelay = self.params['postSoundDelay'].get_value()
            interTrialInterval = self.params['interTrialInterval'].get_value()
            self.sm.add_state(name='startTrial', statetimer=interTrialInterval,
                              transitions={'Tup':'waitForCenterPoke'},
                              outputsOn=trialStartSync)
            self.sm.add_state(name='waitForCenterPoke', statetimer=LONGTIME,
                              transitions={activeEvent:'delayPeriod'})
            self.sm.add_state(name='delayPeriod', statetimer=delayToTarget,
                              transitions={'Tup':'playStimulus','Cout':'waitForCenterPoke'})
            self.sm.add_state(name='playStimulus', statetimer=targetDuration,
                              transitions={'Tup':'postSoundDelay'},
                              outputsOn=stimOutput,serialOut=self.targetSoundID,
                              outputsOff=trialStartSync)
            self.sm.add_state(name='postSoundDelay', statetimer=postSoundDelay,
                              transitions={'Tup':rewardNorewardState}, outputsOff=stimOutput)
            self.sm.add_state(name='reward', statetimer=rewardDuration,
                              transitions={'Tup':'stopReward'},
                              outputsOn=[activeOutput])
            self.sm.add_state(name='noReward', statetimer=0,
                              transitions={'Tup':'stopReward'},
                              outputsOff=[activeOutput])
            self.sm.add_state(name='stopReward', statetimer=0,
                              transitions={'Tup':'readyForNextTrial'},
                              outputsOff=[activeOutput])
        
        elif outcomeMode=='direct':
            self.sm.add_state(name='startTrial', statetimer=0,
                              transitions={'Tup':'waitForCenterPoke'},
                              outputsOn=trialStartSync)
            self.sm.add_state(name='waitForCenterPoke', statetimer=LONGTIME,
                              transitions={'Cin':'playStimulus'})
            self.sm.add_state(name='playStimulus', statetimer=targetDuration,
                              transitions={'Tup':'reward'},
                              outputsOn=stimOutput,serialOut=self.targetSoundID,
                              outputsOff=trialStartSync)
            self.sm.add_state(name='reward', statetimer=rewardDuration,
                              transitions={'Tup':'stopReward'},
                              outputsOn=[rewardOutput],
                              outputsOff=stimOutput)
            self.sm.add_state(name='stopReward', statetimer=0,
                              transitions={'Tup':'readyForNextTrial'},
                              outputsOff=[rewardOutput])
        elif outcomeMode=='on_next_correct':
            self.sm.add_state(name='startTrial', statetimer=0,
                              transitions={'Tup':'waitForCenterPoke'},
                              outputsOn=trialStartSync)
            self.sm.add_state(name='waitForCenterPoke', statetimer=LONGTIME,
                              transitions={'Cin':'delayPeriod'})
            self.sm.add_state(name='delayPeriod', statetimer=delayToTarget,
                              transitions={'Tup':'playStimulus','Cout':'waitForCenterPoke'})
            if allowEarlyWithdrawal=='on':
                self.sm.add_state(name='playStimulus', statetimer=targetDuration,
                                  transitions={'Tup':'waitForSidePoke','Cout':'waitForSidePoke',
                                               'laserTimer':'turnOffLaserAndWaitForPoke'},
                                  outputsOn=stimOutput, serialOut=self.targetSoundID,
                                  outputsOff=trialStartSync)
            else:
                self.sm.add_state(name='playStimulus', statetimer=targetDuration,
                                  transitions={'Tup':'waitForSidePoke','Cout':'earlyWithdrawal'},
                                  outputsOn=stimOutput, serialOut=self.targetSoundID,
                                  outputsOff=trialStartSync)
            # NOTE: this is not ideal because it sends the system out of playStimulus
            #       onto waitForSidePoke (even if stim has not finished.
            self.sm.add_state(name='turnOffLaserAndWaitForPoke', statetimer=0,
                              transitions={'Tup':'waitForSidePoke'},
                              outputsOff=laserOutput)
            self.sm.add_state(name='waitForSidePoke', statetimer=rewardAvailability,
                              transitions={'Lin':'choiceLeft','Rin':'choiceRight',
                                           'Tup':'noChoice','laserTimer':'turnOffLaserAndWaitForPoke'},
                              outputsOff=stimSync)
            self.sm.add_state(name='keepWaitForSide', statetimer=rewardAvailability,
                              transitions={'Lin':'choiceLeft','Rin':'choiceRight',
                                           'Tup':'noChoice'},
                              outputsOff=stimOutput)
            if correctSidePort=='Lin':
                self.sm.add_state(name='choiceLeft', statetimer=0,
                                  transitions={'Tup':'reward'})
                self.sm.add_state(name='choiceRight', statetimer=0,
                                  transitions={'Tup':'keepWaitForSide'})
            elif correctSidePort=='Rin':
                self.sm.add_state(name='choiceLeft', statetimer=0,
                                  transitions={'Tup':'keepWaitForSide'})
                self.sm.add_state(name='choiceRight', statetimer=0,
                                  transitions={'Tup':'reward'})
            self.sm.add_state(name='earlyWithdrawal', statetimer=0,
                              transitions={'Tup':'playPunishment'},
                              outputsOff=stimOutput, serialOut=soundclient.STOP_ALL_SOUNDS)
            self.sm.add_state(name='playPunishment', statetimer=punishTimeEarly,
                              transitions={'Tup':'readyForNextTrial'},
                              serialOut=self.punishSoundID)
            self.sm.add_state(name='reward', statetimer=rewardDuration,
                              transitions={'Tup':'stopReward'},
                              outputsOn=[rewardOutput])
            self.sm.add_state(name='stopReward', statetimer=0,
                              transitions={'Tup':'readyForNextTrial'},
                              outputsOff=[rewardOutput])
            self.sm.add_state(name='punishError', statetimer=punishTimeError,
                              transitions={'Tup':'readyForNextTrial'})
            self.sm.add_state(name='noChoice', statetimer=0,
                              transitions={'Tup':'readyForNextTrial'})
        elif outcomeMode=='only_if_correct':
            self.sm.add_state(name='startTrial', statetimer=0,
                              transitions={'Tup':'waitForCenterPoke'},
                              outputsOn=trialStartSync)
            self.sm.add_state(name='waitForCenterPoke', statetimer=LONGTIME,
                              transitions={'Cin':'delayPeriod'})
            self.sm.add_state(name='delayPeriod', statetimer=delayToTarget,
                              transitions={'Tup':'playStimulus','Cout':'waitForCenterPoke'})
            # Note that 'delayPeriod' may happen several times in a trial, so
            # trialStartSync going off would only meaningful for the first time in the trial.
            if allowEarlyWithdrawal=='on':
                self.sm.add_state(name='playStimulus', statetimer=targetDuration,
                                  transitions={'Tup':'waitForSidePoke','Cout':'waitForSidePoke',
                                               'laserTimer':'turnOffLaserAndWaitForPoke'},
                                  outputsOn=stimOutput, serialOut=self.targetSoundID,
                                  outputsOff=trialStartSync,
                                  trigger=['laserTimer'])
            else:
                self.sm.add_state(name='playStimulus', statetimer=targetDuration,
                                  transitions={'Tup':'waitForSidePoke','Cout':'earlyWithdrawal'},
                                  outputsOn=stimOutput, serialOut=self.targetSoundID,
                                  outputsOff=trialStartSync)
            self.sm.add_state(name='turnOffLaserAndWaitForPoke', statetimer=0,
                              transitions={'Tup':'waitForSidePoke'},
                              outputsOff=laserOutput)
            self.sm.add_state(name='waitForSidePoke', statetimer=rewardAvailability,
                              transitions={'Lin':'choiceLeft','Rin':'choiceRight',
                                           'Tup':'noChoice','laserTimer':'turnOffLaserAndWaitForPoke'},
                              outputsOff=stimSync)
            if correctSidePort=='Lin':
                self.sm.add_state(name='choiceLeft', statetimer=0,
                                  transitions={'Tup':'reward'}, outputsOff=laserOutput)
                self.sm.add_state(name='choiceRight', statetimer=0,
                                  transitions={'Tup':'punishError'}, outputsOff=laserOutput)
            elif correctSidePort=='Rin':
                self.sm.add_state(name='choiceLeft', statetimer=0,
                                  transitions={'Tup':'punishError'}, outputsOff=laserOutput)
                self.sm.add_state(name='choiceRight', statetimer=0,
                                  transitions={'Tup':'reward'}, outputsOff=laserOutput)
            self.sm.add_state(name='earlyWithdrawal', statetimer=0,
                              transitions={'Tup':'playPunishment'},
                              outputsOff=stimOutput, serialOut=soundclient.STOP_ALL_SOUNDS)
            self.sm.add_state(name='playPunishment', statetimer=punishTimeEarly,
                              transitions={'Tup':'readyForNextTrial'},
                              serialOut=self.punishSoundID)
            self.sm.add_state(name='reward', statetimer=rewardDuration,
                              transitions={'Tup':'stopReward'},
                              outputsOn=[rewardOutput])
            self.sm.add_state(name='stopReward', statetimer=0,
                              transitions={'Tup':'readyForNextTrial'},
                              outputsOff=[rewardOutput]+stimOutput)
            self.sm.add_state(name='punishError', statetimer=punishTimeError,
                              transitions={'Tup':'readyForNextTrial'})
            self.sm.add_state(name='noChoice', statetimer=0,
                              transitions={'Tup':'readyForNextTrial'})

        else:
            raise TypeError('outcomeMode={0} has not been implemented'.format(outcomeMode))
        
    def calculate_results(self,trialIndex):
        # -- Find outcomeMode for this trial --
        outcomeModeID = self.params.history['outcomeMode'][trialIndex]
        outcomeModeString = self.params['outcomeMode'].get_items()[outcomeModeID]

        eventsThisTrial = self.dispatcher.events_one_trial(trialIndex)
        statesThisTrial = eventsThisTrial[:,2]
        #print(eventsThisTrial)

        # -- Find beginning of trial --
        startTrialStateID = self.sm.statesNameToIndex['startTrial']
        # FIXME: Next line seems inefficient. Is there a better way?
        startTrialInd = np.flatnonzero(statesThisTrial==startTrialStateID)[0]
        self.results['timeTrialStart'][trialIndex] = eventsThisTrial[startTrialInd,0]

        # ===== Calculate times of events =====
        # -- Check if it's an aborted trial --
        lastEvent = eventsThisTrial[-1,:]
        if lastEvent[1]==-1 and lastEvent[2]==0:
            self.results['timeTarget'][trialIndex] = np.nan
            self.results['timeCenterIn'][trialIndex] = np.nan
            self.results['timeCenterOut'][trialIndex] = np.nan
            self.results['timeSideIn'][trialIndex] = np.nan
        # -- Otherwise evaluate times of important events --
        else:
            # -- Store time of stimulus --
            targetStateID = self.sm.statesNameToIndex['playStimulus']
            targetEventInd = np.flatnonzero(statesThisTrial==targetStateID)[0]
            self.results['timeTarget'][trialIndex] = eventsThisTrial[targetEventInd,0]

            # -- Find center poke-in time --
            if outcomeModeString in ['on_next_correct', 'only_if_correct', 'on_any_poke']:
                seqCin = [self.sm.statesNameToIndex['waitForCenterPoke'],
                          self.sm.statesNameToIndex['delayPeriod'],
                          self.sm.statesNameToIndex['playStimulus']]
            elif outcomeModeString in ['simulated', 'sides_direct', 'direct', 'passive_exposure']:
                seqCin = [self.sm.statesNameToIndex['waitForCenterPoke'],
                          self.sm.statesNameToIndex['playStimulus']]
            else:
                print('CenterIn time cannot be calculated for this Outcome Mode.')
            seqPos = np.flatnonzero(utils.find_state_sequence(statesThisTrial,seqCin))
            timeValue = eventsThisTrial[seqPos[0]+1,0] if len(seqPos) else np.nan
            self.results['timeCenterIn'][trialIndex] = timeValue




            ############# FIXME: create a state for Cout so it's easy to get timing ########



            # -- Find center poke-out time --
            if len(seqPos):
                cInInd = seqPos[0]+1
                cOutInd = np.flatnonzero(eventsThisTrial[cInInd:,1]==self.sm.eventsDict['Cout'])
                timeValue = eventsThisTrial[cOutInd[0]+cInInd,0] if len(cOutInd) else np.nan
            else:
                timeValue = np.nan
            self.results['timeCenterOut'][trialIndex] = timeValue

            # -- Find side poke time --
            if outcomeModeString in ['on_next_correct','only_if_correct']:
                leftInInd = utils.find_transition(statesThisTrial,
                                                  self.sm.statesNameToIndex['waitForSidePoke'],
                                                  self.sm.statesNameToIndex['choiceLeft'])
                rightInInd = utils.find_transition(statesThisTrial,
                                                   self.sm.statesNameToIndex['waitForSidePoke'],
                                                   self.sm.statesNameToIndex['choiceRight'])
                if len(leftInInd):
                    timeValue = eventsThisTrial[leftInInd[0],0]
                elif len(rightInInd):
                    timeValue = eventsThisTrial[rightInInd[0],0]
                else:
                    timeValue = np.nan
            elif outcomeModeString in ['simulated','sides_direct','direct']:
                timeValue = np.nan
            self.results['timeSideIn'][trialIndex] = timeValue

        # ===== Calculate choice and outcome =====
        # -- Check if it's an aborted trial --
        lastEvent = eventsThisTrial[-1,:]
        if lastEvent[1]==-1 and lastEvent[2]==0:
            self.results['outcome'][trialIndex] = self.results.labels['outcome']['aborted']
            self.results['choice'][trialIndex] = self.results.labels['choice']['none']
        # -- Otherwise evaluate 'choice' and 'outcome' --
        else:
            if outcomeModeString in ['on_any_poke']:
                if self.sm.statesNameToIndex['reward'] in eventsThisTrial[:,2]:
                    self.results['outcome'][trialIndex] = self.results.labels['outcome']['free']
                    self.params['nRewarded'].add(1)
                else:
                    self.results['outcome'][trialIndex] = self.results.labels['outcome']['nochoice']
                self.results['choice'][trialIndex] = self.results.labels['choice']['none']
                self.params['nValid'].add(1)
                self.results['valid'][trialIndex] = 1
            if outcomeModeString in ['simulated','sides_direct','direct']:
                self.results['outcome'][trialIndex] = self.results.labels['outcome']['free']
                self.results['choice'][trialIndex] = self.results.labels['choice']['none']
                self.params['nValid'].add(1)
                self.params['nRewarded'].add(1)
                self.results['valid'][trialIndex] = 1
            if outcomeModeString=='on_next_correct' or outcomeModeString=='only_if_correct':
                if self.sm.statesNameToIndex['choiceLeft'] in eventsThisTrial[:,2]:
                    self.results['choice'][trialIndex] = self.results.labels['choice']['left']
                elif self.sm.statesNameToIndex['choiceRight'] in eventsThisTrial[:,2]:
                    self.results['choice'][trialIndex] = self.results.labels['choice']['right']
                else:
                    self.results['choice'][trialIndex] = self.results.labels['choice']['none']
                    self.results['outcome'][trialIndex] = \
                        self.results.labels['outcome']['nochoice']
                if self.sm.statesNameToIndex['reward'] in eventsThisTrial[:,2]:
                   self.results['outcome'][trialIndex] = \
                        self.results.labels['outcome']['correct']
                   self.params['nRewarded'].add(1)
                   if outcomeModeString=='on_next_correct' and \
                           self.sm.statesNameToIndex['keepWaitForSide'] in eventsThisTrial[:,2]:
                       self.results['outcome'][trialIndex] = \
                           self.results.labels['outcome']['aftererror']
                else:
                    if self.sm.statesNameToIndex['earlyWithdrawal'] in eventsThisTrial[:,2]:
                        self.results['outcome'][trialIndex] = \
                            self.results.labels['outcome']['invalid']
                    elif self.sm.statesNameToIndex['punishError'] in eventsThisTrial[:,2]:
                        self.results['outcome'][trialIndex] = \
                            self.results.labels['outcome']['error']
                # -- Check if it was a valid trial --
                if self.sm.statesNameToIndex['waitForSidePoke'] in eventsThisTrial[:,2]:
                    self.params['nValid'].add(1)
                    self.results['valid'][trialIndex] = 1

    def execute_automation(self,nextTrial):
        automationMode = self.params['automationMode'].get_string()
        nValid = self.params['nValid'].get_value()
        if automationMode=='increase_delay':
            if nValid>0 and self.results['valid'][nextTrial-1] and not nValid%10:
                self.params['delayToTargetMean'].add(0.010)

    def closeEvent(self, event):
        '''
        Executed when closing the main window.
        This method is inherited from QtWidgets.QMainWindow, which explains
        its camelCase naming.
        '''
        self.soundClient.shutdown()
        self.dispatcher.die()
        event.accept()

if __name__ == '__main__':
    (app,paradigm) = paramgui.create_app(Paradigm)
        