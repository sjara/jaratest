rand1 <- rnorm(1000, mean=0, sd=1)
rand2 <- rnorm(1000, mean=0.5, sd=1)
hist(rand1)

library(pROC)

auc(rand1, rand2)
