from jaratoolbox.test.nick import behavioranalysis_vnick as ba
animals = ['amod002', 'amod003']
sessions = ['20160426a', '20160427a', '20160428a', '20160429a']
side = [0, 1, 0, 1] #0 - Right, 1 - Left

allnCorr = []
allnVal = []
allfracCorr = []

sessionInds = []
animalInds = []
sides = []


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
        sides.append(side[indSession])
