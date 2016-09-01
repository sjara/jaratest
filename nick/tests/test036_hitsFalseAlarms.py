

def hitFA(bdata):

    correctTrials = bdata['outcome'] == bdata.labels['outcome']['correct']
    rightTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['right']
    leftTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['left']

    validTrials = bdata['valid']
    nValid = sum(validTrials)

    #Hits = right/correct
    hitFrac = sum(rightTrials & correctTrials)/nValid.astype(float)

    #False Alarms = 1-left/correct
    faFrac = 1-(sum(leftTrials & correctTrials)/nValid.astype(float))

    return array([hitFrac, faFrac])

muscimolSessions = ['20160413a','20160415a','20160417a', '20160419a', '20160421a']
salineSessions = ['20160412a','20160414a','20160416a', '20160418a', '20160420a']

musAmpHitFA = np.zeros([len(muscimolSessions), 2])
musChordHitFA = np.zeros([len(muscimolSessions), 2])
salineAmpHitFA = np.zeros([len(salineSessions), 2])
salineChordHitFA = np.zeros([len(salineSessions), 2])


for indSession, session in enumerate(muscimolSessions):
    muscimolDataObjs, muscimolSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, [session])
    musAmpHitFA[indSession, :] = hitFA(muscimolDataObjs[0]) #The amp_mod session
    musChordHitFA[indSession, :] = hitFA(muscimolDataObjs[1])

for indSession, session in enumerate(salineSessions):
    salineDataObjs, salineSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, [session])
    salineAmpHitFA[indSession, :] = hitFA(salineDataObjs[0]) #The amp_mod session
    salineChordHitFA[indSession, :] = hitFA(salineDataObjs[1])
