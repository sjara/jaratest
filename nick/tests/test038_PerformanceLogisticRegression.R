# Random effects logistic regression models for average percent correct performance data over multiple days of muscimol 

#DONE
sessionInd <- c(0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4)

## animalInd <- c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
animalInd <-  c(rep('amod002', 20), rep('amod003', 20))

allnCorr <- c(377, 306, 429, 294, 394, 329, 403, 276, 363, 282, 420, 404, 480, 433, 492, 430, 491, 453, 427, 382, 322, 279, 353, 341, 411, 322, 327, 241, 348, 245, 392, 335, 371, 311, 452, 383, 482, 425, 439, 376)

allnVal <- c(547, 547, 574, 574, 591, 591, 521, 521, 484, 484, 482, 482, 537, 537, 552, 553, 572, 572, 484, 485, 486, 487, 539, 540, 570, 571, 448, 449, 479, 480, 445, 446, 431, 432, 502, 503, 535, 536, 484, 485)

soundType <- c(0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1)

soundType <- factor(soundType, labels=c('chord', 'AM'))

muscimol <- c(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
muscimol <- factor(muscimol, labels=c('saline', 'mus'))


library(lme4)


data <- data.frame(sessionInd, animalInd, allnCorr, allnVal, soundType, muscimol)


## model0 <- glm(allnCorr/allnVal ~ muscimol*soundType*sessionInd, weights = allnVal, data = split(data, animalInd)$`0`, family=binomial)
## model1 <- glm(allnCorr/allnVal ~ muscimol*soundType*sessionInd, weights = allnVal, data = split(data, animalInd)$`1`, family=binomial)


#Fixed effect of muscimol and soundType. random slopes and intercepts for the effect of soundtype within each animal and the effect of muscimol within each animal
## model <- glmer(allnCorr/allnVal ~ muscimol*soundType + (1 + soundType | animalInd) + (1 + muscimol | animalInd) , weights = allnVal, family = binomial)
model <- glmer(allnCorr/allnVal ~ muscimol*soundType + (1 + soundType*muscimol | animalInd), weights = allnVal, family = binomial)

summary(model)



## random.model.fit.mod <- glmer(nCorrMod/nValMod ~ sessionInd + (1 | animalInd), weights = nValMod, family = binomial)


summary(random.model.fit.chords)
summary(random.model.fit.mod)

plot(model.fit)

plot(nCorrChords/nValChords ~ sessionInd)
plot(nCorrMod/nValMod ~ sessionInd)



