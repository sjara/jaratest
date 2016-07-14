muscimolSessions = ['20160413a']
salineSessions = ['20160412a']
animal = 'amod002'

muscimolChordsData = behavioranalysis.load_many_sessions(animal, muscimolSessions)
muscimolModData = behavioranalysis.load_many_sessions(animal, muscimolSessions)
salineChordsData = behavioranalysis.load_many_sessions(animal, salineSessions)
salineModData = behavioranalysis.load_many_sessions(animal, salineSessions)

salineChordsTrials = np.flatnonzero(salineChordsData['soundType']==salineData.labels['soundType']['chords'])
salineModTrials = np.flatnonzero(salineChordsData['soundType']==salineData.labels['soundType']['amp_mod'])

muscimolChordsTrials = np.flatnonzero(muscimolChordsData['soundType']==muscimolData.labels['soundType']['chords'])
muscimolModTrials = np.flatnonzero(muscimolChordsData['soundType']==muscimolData.labels['soundType']['amp_mod'])

salineChordsData.remove_trials(salineModTrials)
salineModData.remove_trials(salineChordsTrials)

muscimolChordsData.remove_trials(muscimolModTrials)
muscimolModData.remove_trials(muscimolChordsTrials)

sChoice = salineChordsData['choice']
sRewSide = salineChordsData['rewardSide']

#0 is left, 1 is right

#Hits are when the choice was right and the reward side was right
sHits = (sChoice==1) & (sRewSide==1)
#Misses are when the choice was left and the reward side was right
sMisses = (sChoice==0) & (sRewSide==1)
#Correct rejections are when the choice was left and the reward side was left
sCR = (sChoice==0) & (sRewSide==0)
#False alarms are when the choice was right and the reward side was left
sFA = (sChoice==1) & (sRewSide==0)

def split_by(boolArray, splitArray):
    '''
    Sum up a boolean array in categories defined by another array
    '''
    splitSums = [sum(boolArray[splitArray==thisVal]) for thisVal in np.unique(splitArray)]
    return splitSums


sHitsByFreq = split_by(sHits, salineChordsData['targetFrequency'])
sMissesByFreq = split_by(sMisses, salineChordsData['targetFrequency'])
sCRByFreq = split_by(sCR, salineChordsData['targetFrequency'])
sFAByFreq = split_by(sFA, salineChordsData['targetFrequency'])

x = range(len(sHitsByFreq))
plot(x, sHitsByFreq, 'bo', label='Hits')
plot(x, sFAByFreq, 'ro', label='False Alarms')
plot(x, sMissesByFreq, 'co', label = 'Misses')
plot(x, sCRByFreq, 'mo', label='Correct Rejections')


choiceL = salineChordsData['choice']==salineChordsData.labels['choice']['left']
choiceLSplit = split_by(choiceL, salineChordsData['targetFrequency'])
plot(choiceLSplit)

choiceR = salineChordsData['choice']==salineChordsData.labels['choice']['right']
choiceRSplit = split_by(choiceR, salineChordsData['targetFrequency'])
plot(choiceRSplit)





figure()
choiceL = muscimolChordsData['choice']==muscimolChordsData.labels['choice']['left']
choiceLSplit = split_by(choiceL, muscimolChordsData['targetFrequency'])
plot(choiceLSplit)

choiceR = muscimolChordsData['choice']==muscimolChordsData.labels['choice']['right']
choiceRSplit = split_by(choiceR, muscimolChordsData['targetFrequency'])
plot(choiceRSplit)






figure()
choiceL = salineModData['choice']==salineModData.labels['choice']['left']
choiceLSplit = split_by(choiceL, salineModData['targetFrequency'])
plot(choiceLSplit)

choiceR = salineModData['choice']==salineModData.labels['choice']['right']
choiceRSplit = split_by(choiceR, salineModData['targetFrequency'])
plot(choiceRSplit)


figure()
choiceL = muscimolModData['choice']==muscimolModData.labels['choice']['left']
choiceLSplit = split_by(choiceL, muscimolModData['targetFrequency'])
plot(choiceLSplit)

choiceR = muscimolModData['choice']==muscimolModData.labels['choice']['right']
choiceRSplit = split_by(choiceR, muscimolModData['targetFrequency'])
plot(choiceRSplit)



array(choiceLSplit)/len(salineChordsData['targetFrequency'])
