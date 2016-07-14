from jaratoolbox.test.nick import behavioranalysis_vnick as behavioranalysis

animals = ['amod002', 'amod003']
sessions = ['20160421a', '20160422a', '20160423a', '20160424a']

allnCorr = []
allnVal = []
allfracCorr = []

sessionInds = []
animalInds = []

for indAnimal, animal in enumerate(animals):
    for indSession, session in enumerate(sessions):
        (bdataObjs, bdataSoundTypes) = ba.load_behavior_sessions_sound_type(animal, [session])
        bdata = bdataObjs[0] #analyze chord discrim
        nCorr = sum(bdata['outcome']==bdata.labels['outcome']['correct'])
        nVal = sum(bdata['valid'])
        allfracCorr.append(nCorr.astype(float)/nVal)
        allnCorr.append(nCorr)
        allnVal.append(nVal)
        sessionInds.append(indSession)
        animalInds.append(indAnimal)


nRew = array(nRew)
nVal = array(nVal)

######### Try with the muscimol data and saline data in the same array ############

animals = ['amod002', 'amod003']
nAnimals = len(animals)

muscimolSessions = ['20160413a', '20160415a', '20160417a', '20160419a', '20160421a']
salineSessions = ['20160412a', '20160414a', '20160416a', '20160418a', '20160420a']



allnCorr = []
allnVal = []
allfracCorr = []

sessionInds = []
animalInds = []
soundType = [] #0 = chords, 1 = mod
muscimol = [] #0 = no muscimol, 1 = muscimol

for indAnimal, animal in enumerate(animals):
    for indSession, session in enumerate(muscimolSessions):
        muscimolDataObjs, muscimolSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, [session])

        mdataChords = muscimolDataObjs[muscimolSoundTypes['chords']]
        mdataMod = muscimolDataObjs[muscimolSoundTypes['amp_mod']]

        #Process muscimol data for chords
        bdata = mdataChords

        #Boilerplate
        nCorr = sum(bdata['outcome']==bdata.labels['outcome']['correct'])
        nVal = sum(bdata['valid'])
        allfracCorr.append(nCorr.astype(float)/nVal)
        allnCorr.append(nCorr)
        allnVal.append(nVal)
        sessionInds.append(indSession)
        animalInds.append(indAnimal)

        #Chords
        soundType.append(0)
        #Muscimol
        muscimol.append(1)


        #Process muscimol data for amp_mod
        bdata = mdataMod

        #Boilerplate
        nCorr = sum(bdata['outcome']==bdata.labels['outcome']['correct'])
        nVal = sum(bdata['valid'])
        allfracCorr.append(nCorr.astype(float)/nVal)
        allnCorr.append(nCorr)
        allnVal.append(nVal)
        sessionInds.append(indSession)
        animalInds.append(indAnimal)

        #Modulation
        soundType.append(1)
        #Muscimol
        muscimol.append(1)

    for indSession, session in enumerate(salineSessions):
        salineDataObjs, salineSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, [session])


        sdataChords = salineDataObjs[salineSoundTypes['chords']]
        sdataMod = salineDataObjs[salineSoundTypes['amp_mod']]

        #Process saline data for chords
        bdata = sdataChords

        #Boilerplate
        nCorr = sum(bdata['outcome']==bdata.labels['outcome']['correct'])
        nVal = sum(bdata['valid'])
        allfracCorr.append(nCorr.astype(float)/nVal)
        allnCorr.append(nCorr)
        allnVal.append(nVal)
        sessionInds.append(indSession)
        animalInds.append(indAnimal)

        #Chords
        soundType.append(0)
        #Saline
        muscimol.append(0)

        #Process saline data for mod
        bdata = sdataMod

        #Boilerplate
        nCorr = sum(bdata['outcome']==bdata.labels['outcome']['correct'])
        nVal = sum(bdata['valid'])
        allfracCorr.append(nCorr.astype(float)/nVal)
        allnCorr.append(nCorr)
        allnVal.append(nVal)
        sessionInds.append(indSession)
        animalInds.append(indAnimal)

        #Mod
        soundType.append(1)
        #Saline
        muscimol.append(0)


import rpy2

from rpy2.robjects.packages import importr

lme4 = importr('lme4')

from rpy2.robjects import IntVector, Formula


allnCorr = IntVector(allnCorr)
allnVal = IntVector(allnVal)
allfracCorr = IntVector(allfracCorr)
sessionInds = IntVector(sessionInds)
animalInds = IntVector(animalInds)
soundType = IntVector(soundType)
muscimol = IntVector(muscimol)

model = Formula('allnCorr/allnVal ~ sessionInds + (1 | animalInds), weights=allnVal, family=binomial')

env = model.environment
env['allnCorr'] = allnCorr
env['allnVal'] = allnVal
env['sessionInds'] = sessionInds
env['animalInds'] = animalInds

lme4.glmer(model)






# animal = 'amod003'
# sessions = ['20160412a', '20160413a', '20160414a', '20160415a', '20160416a', '20160417a', '20160418a', '20160419a', '20160420a', '20160421a', '20160422a', '20160423a', '20160424a', '20160425a', '20160426a', '20160427a', '20160428a', '20160429a', '20160430a', '20160501a', '20160502a']
# muscimol = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1]


# fracCorr = []
# for session in sessions:
#     (bdataObjs, bdataSoundTypes) = ba.load_behavior_sessions_sound_type(animal, [session])
#     bdata = bdataObjs[1] #analyze chord discrim
#     nCorr = sum(bdata['outcome']==bdata.labels['outcome']['correct'])
#     nVal = sum(bdata['valid'])
#     fracCorr.append(nCorr.astype(float)/nVal)


#### amod004 stuff
animals = ['amod004']
muscimolSessions = ['20160427a', '20160429a', '20160501a', '20160503a', '20160505a', '20160507a', '20160509a']
salineSessions = ['20160426a', '20160428a', '20160430a', '20160502a', '20160504a', '20160506a', '20160508a']
###


allnCorr = []
allnVal = []
allfracCorr = []

sessionInds = []
animalInds = []
soundType = [] #0 = tones, 1 = mod
muscimol = [] #0 = no muscimol, 1 = muscimol

for indAnimal, animal in enumerate(animals):
    for indSession, session in enumerate(muscimolSessions):
        muscimolDataObjs, muscimolSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, [session])

        mdataChords = muscimolDataObjs[muscimolSoundTypes['tones']]
        mdataMod = muscimolDataObjs[muscimolSoundTypes['amp_mod']]

        #Process muscimol data for chords
        bdata = mdataChords

        #Boilerplate
        nCorr = sum(bdata['outcome']==bdata.labels['outcome']['correct'])
        nVal = sum(bdata['valid'])
        allfracCorr.append(nCorr.astype(float)/nVal)
        allnCorr.append(nCorr)
        allnVal.append(nVal)
        sessionInds.append(indSession)
        animalInds.append(indAnimal)

        #Chords
        soundType.append(0)
        #Muscimol
        muscimol.append(1)


        #Process muscimol data for amp_mod
        bdata = mdataMod

        #Boilerplate
        nCorr = sum(bdata['outcome']==bdata.labels['outcome']['correct'])
        nVal = sum(bdata['valid'])
        allfracCorr.append(nCorr.astype(float)/nVal)
        allnCorr.append(nCorr)
        allnVal.append(nVal)
        sessionInds.append(indSession)
        animalInds.append(indAnimal)

        #Modulation
        soundType.append(1)
        #Muscimol
        muscimol.append(1)

    for indSession, session in enumerate(salineSessions):
        salineDataObjs, salineSoundTypes = behavioranalysis.load_behavior_sessions_sound_type(animal, [session])


        sdataChords = salineDataObjs[salineSoundTypes['tones']]
        sdataMod = salineDataObjs[salineSoundTypes['amp_mod']]

        #Process saline data for chords
        bdata = sdataChords

        #Boilerplate
        nCorr = sum(bdata['outcome']==bdata.labels['outcome']['correct'])
        nVal = sum(bdata['valid'])
        allfracCorr.append(nCorr.astype(float)/nVal)
        allnCorr.append(nCorr)
        allnVal.append(nVal)
        sessionInds.append(indSession)
        animalInds.append(indAnimal)

        #Chords
        soundType.append(0)
        #Saline
        muscimol.append(0)

        #Process saline data for mod
        bdata = sdataMod

        #Boilerplate
        nCorr = sum(bdata['outcome']==bdata.labels['outcome']['correct'])
        nVal = sum(bdata['valid'])
        allfracCorr.append(nCorr.astype(float)/nVal)
        allnCorr.append(nCorr)
        allnVal.append(nVal)
        sessionInds.append(indSession)
        animalInds.append(indAnimal)

        #Mod
        soundType.append(1)
        #Saline
        muscimol.append(0)


'''
R code


# Random effects logistic regression models for average percent correct performance data over multiple days of muscimol 
sessionInd <- c(0, 1, 2, 3, 0, 1, 2, 3) #The session number
nCorrChords <- c(363, 440, 411, 444, 348, 443, 375, 438) #Number of correct trials, chords
nValChords <- c(484, 610, 565, 564, 479, 565, 473, 538) #Number of valid trials, chords
nCorrMod <- c(282, 360, 308, 317, 245, 311, 295, 306) # Number of correct trials, amp mod
nValMod <- c(484, 610, 566, 565, 480, 565, 474, 538) # Number of valid trials, amp mod
animalInd <- c(0, 0, 0, 0, 1, 1, 1, 1) #The animal (0 - amod002, 1 - amod003)

# load library for mixed-effect modeling
library(lme4)

#Model the data with a fixed effect of the session number and a random effect of the animal number
random.model.fit.chords <- glmer(nCorrChords/nValChords ~ sessionInd + (1 | animalInd), weights = nValChords, family = binomial)
random.model.fit.mod <- glmer(nCorrMod/nValMod ~ sessionInd + (1 | animalInd), weights = nValMod, family = binomial)

#Print model summary
summary(random.model.fit.chords)
summary(random.model.fit.mod)

#Plot the data
plot(nCorrChords/nValChords ~ sessionInd)
plot(nCorrMod/nValMod ~ sessionInd)



'''
