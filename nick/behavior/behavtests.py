'''
Tests that can be applied to behavior files for making alarms or autotrainers

Ideas

Number of valid trials above/below x
Percent correct above/below x
Behavior stable for x number of days
Biased behavior
Percent early withdrawals above x

Data not on jarahub

'''
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratest.nick import soundtypes
import numpy as np

import subprocess
import os

def get_behavior(subject):
    '''
    rsync the behavior from jarahub to the local computer for the animal
    '''

    remoteBehavLocation = 'jarauser@jarahub:/data/behavior/{}'.format(subject)
    localBehavPath = settings.BEHAVIOR_PATH
    transferCommand = ['rsync', '-a', '--progress', remoteBehavLocation, localBehavPath]
    print ' '.join(transferCommand)
    subprocess.call(transferCommand)

class BehaviorTest():
    def passes_test(self, subject, paradigm, sessionstr):
        self.behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, sessionstr)
        if not os.path.exists(self.behavFile):
            get_behavior(subject)
        self.bdata = loadbehavior.BehaviorData(self.behavFile)
        return self.test()
    def test(self):
        '''
        Overwrite this method in all subclasses
        e.g. do something with self.bdata and return true/false for whether the test was passed
        '''
        raise NotImplementedError

class ValidTrialsAbove(BehaviorTest):
    def __init__(self, threshold):
        self.threshold = threshold
    def test(self):
        totalValid = self.bdata['nValid'][-1]
        print 'Total Valid Trials: {}'.format(totalValid)
        print 'Threshold: {}'.format(self.threshold)
        return totalValid>self.threshold

class PercentCorrectAbove(BehaviorTest):
    def __init__(self, threshold):
        self.threshold = threshold
    def test(self):
        totalValid = self.bdata['nValid'][-1]
        totalRewarded = self.bdata['nRewarded'][-1]
        perCorr = 100*(totalRewarded/double(totalValid))
        print 'Percent Correct: {}'.format(perCorr)
        print 'Threshold: {}'.format(self.threshold)
        return perCorr>self.threshold

class PercentCorrectAboveAllSoundType(BehaviorTest):
    def __init__(self, threshold):
        self.threshold = threshold
        self.message = []
    def passes_test(self, subject, paradigm, sessionstr):
        '''
        Re-define to allow multiple sound types
        '''
        self.behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, sessionstr)
        if not os.path.exists(self.behavFile):
            get_behavior(subject)
        self.message.append('Threshold: {}'.format(self.threshold))
        #Load all sound types
        (self.dataObjs,
         self.dataSoundTypes) = soundtypes.load_behavior_sessions_sound_type(subject,
                                                                             [sessionstr])
        return all([self.test(bdata, soundType) for bdata, soundType in zip(self.dataObjs, self.dataSoundTypes)])
    def test(self, bdata, soundType):
        totalValid = bdata['nValid'][-1]
        totalRewarded = bdata['nRewarded'][-1]
        perCorr = 100*(totalRewarded/np.double(totalValid))
        self.message.append('Percent Correct for {}: {}'.format(soundType, perCorr))
        # print 'Threshold: {}'.format(self.threshold)
        return perCorr>self.threshold
    def __str__(self):
        return "Percent correct for all sound types above {}".format(self.threshold)


class PsycurveEndFreqsPercentCorrectAbove(BehaviorTest):
    def __init__(self, threshold):
        self.threshold = threshold
    def test(self):
        hits = bdata['outcome']==bdata.labels['outcome']['correct']
        freqEachTrial = bdata['targetFrequency']
        valid = bdata['valid']
        (possibleValues,
         fractionHitsEachValue,
         ciHitsEachValue,
         nTrialsEachValue,
         nHitsEachValue) = behavioranalysis.calculate_psychometric(hits,
                                                                   freqEachTrial,
                                                                   valid)
        #Get the percent correct for the low and high freqs and test against the threshol
        lowPerCorr = 100*fractionHitsEachValue[0]
        highPerCorr = 100*fractionHitsEachValue[-1]
        print 'Low Freq Percent Correct: {}'.format(lowPerCorr)
        print 'High Freq Percent Correct: {}'.format(highPerCorr)
        print 'Threshold: {}'.format(self.threshold)
        return ((lowPerCorr>self.threshold) & (highPerCorr>self.threshold))


# class mouse
# has training history, written as h5 file


if __name__ == '__main__':

    subject = 'amod006'
    paradigm = '2afc'
    sessionstr = '20160713a'
    behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, sessionstr)
    bdata = loadbehavior.BehaviorData(behavFile)

    #Build the tester
    trialtest = ValidTrialsAbove(200)

    #Call the tester on a behavior session
    if trialtest.passes_test(subject, paradigm, sessionstr):
        print 'passes the test'

    perCorrTest = PercentCorrectAbove(80)

    if perCorrTest.passes_test(subject, paradigm, sessionstr):
        print 'passes the test'

    endFreqTest = PsycurveEndFreqsPercentCorrectAbove(80)

    if endFreqTest.passes_test(subject, paradigm, sessionstr):
        print 'passes the test'

    perCorrTest = PercentCorrectAboveAllSoundType(70)
    if perCorrTest.passes_test(subject,paradigm, sessionstr):
        print '\n'.join(perCorrTest.message)


    ####Ideas for tests###
    threshold=200
    bdata['nValid'][-1] < threshold




    #Number of valid trials above x
    trialsThresh = 500
    if bdata['nValid'][-1] > trialsThresh:
        print 'yes'

    #Number of valid trials below x
    trialsThresh = 500
    assert bdata['nValid'][-1] < trialsThresh, "Number of trials not above "


    #Percent correct above/below x
    perCorrThresh = 50
    perCorr = (bdata['nRewarded'][-1] / bdata['nValid'][-1].astype(double)) * 100
    if perCorr > perCorrThresh:
        print 'yes'
