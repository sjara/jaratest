'''
amodSidesDirect = {'outcomeMode':'sides_direct', 'soundTypeMode':'amp_mod'}
amodDirect = {'outcomeMode':'direct', 'soundTypeMode':'amp_mod'}
amodNextCorrectAM = {'outcomeMode':'on_next_correct', 'soundTypeMode':'amp_mod'}
amodIfCorrectAM = {'outcomeMode':'only_if_correct', 'soundTypeMode':'amp_mod'}
amodPsycurveAM = {'outcomeMode':'only_if_correct', 'soundTypeMode':'amp_mod', 'psycurveMode':'uniform'}
amodIfCorrectTones = {'outcomeMode':'only_if_correct', 'soundTypeMode':'tones'}
amodPsycurveTones = {'outcomeMode':'only_if_correct', 'soundTypeMode':'tones', 'psycurveMode':'uniform'}
amodPsycurveMixed = {'outcomeMode':'only_if_correct', 'soundTypeMode':'mixed_tones', 'psycurveMode':'uniform'}
'''

statesNames = [
    'amodSidesDirect',
    'amodDirect',
    'amodNextCorrectAM',
    'amodIfCorrectAM',
    'amodPsycurveAM',
    'amodIfCorrectTones',
    'amodPsycurveTones',
    'amodPsycurveMixed'
]

statesParams = [
    {'outcomeMode':'sides_direct', 'soundTypeMode':'amp_mod'},
    {'outcomeMode':'direct', 'soundTypeMode':'amp_mod'},
    {'outcomeMode':'on_next_correct', 'soundTypeMode':'amp_mod'},
    {'outcomeMode':'only_if_correct', 'soundTypeMode':'amp_mod'},
    {'outcomeMode':'only_if_correct', 'soundTypeMode':'amp_mod', 'psycurveMode':'uniform'},
    {'outcomeMode':'only_if_correct', 'soundTypeMode':'tones'},
    {'outcomeMode':'only_if_correct', 'soundTypeMode':'tones', 'psycurveMode':'uniform'},
    {'outcomeMode':'only_if_correct', 'soundTypeMode':'mixed_tones', 'psycurveMode':'uniform'}
]

from jaratest.nick.behavior import behavtests
reload(behavtests)

statesTests = [
    behavtests.ValidTrialsAbove(200),
    behavtests.ValidTrialsAbove(200),
    behavtests.ValidTrialsAbove(500),
    behavtests.PercentCorrectAbove(80),
    behavtests.PsycurveEndFreqsPercentCorrectAbove(80),
    behavtests.PercentCorrectAbove(80),
    behavtests.PsycurveEndFreqsPercentCorrectAbove(80),
    behavtests.PercentCorrectAbove(80), #Needs to work for both freq and AM
    behavtests.PsycurveEndFreqsPercentCorrectAbove(80), #Needs to work for both freq and AM
]

mouseState = 5 # Just switched to if correct tones for session 20160714a
subject = 'amod006'
paradigm = '2afc'
sessionstr = '20160714a'

test = statesTests[mouseState]
assert test.passes_test(subject, paradigm, sessionstr), "Mouse not ready"


def mouse_dict_factory(self, mouseFile):
    '''
    Reads a h5 file, tests mouse behavior, returns the the appropriate param dict
    '''



amod006 = mouse_dict_factory('/home/nick/data/mousefiles/amod006.h5')


class ShapeFile(object):
