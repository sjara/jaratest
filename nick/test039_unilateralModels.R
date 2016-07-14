
sessionInd <- c(0, 1, 2, 3, 0, 1, 2, 3) #The session number
nCorrChords <- c(407, 409, 460, 416, 364, 394, 389, 423) #Number of correct trials, chords
nValChords <- c(479, 499, 538, 501, 451, 466, 441, 468) #Number of valid trials, chords
nCorrMod <- c(333, 373, 360, 376, 304, 354, 298, 330) # Number of correct trials, amp mod
nValMod <- c(480, 500, 539, 501, 452, 466, 441, 469) # Number of valid trials, amp mod
animalInd <- c(0, 0, 0, 0, 1, 1, 1, 1) #The animal (0 - amod002, 1 - amod003)
side <- c(0, 1, 0, 1, 0, 1, 0, 1 ) # 0 - Right, 1 - Left



random.model.fit.chords <- glmer(nCorrChords/nValChords ~ side + sessionInd + (1 | animalInd), weights = nValChords, family = binomial)
random.model.fit.mod <- glmer(nCorrMod/nValMod ~ side + sessionInd + (1 | animalInd), weights = nValMod, family = binomial)

summary(random.model.fit.chords)
summary(random.model.fit.mod)
