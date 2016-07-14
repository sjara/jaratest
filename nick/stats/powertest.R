# Plot sample size curves for t-tests with various effect sizes

library(pwr)

# range of correlations
## r <- seq(.1,.5,.01)
d <- seq(0.2, 0.8, 0.1)
## nr <- length(r)
nd <-  length(d)

# power values
p <- seq(.4,.9,.1)
np <- length(p)

# obtain sample sizes
samsize <- array(numeric(nd*np), dim=c(nd,np))
for (i in 1:np){
  for (j in 1:nd){
    result <- pwr.t.test(n = NULL, d = d[j],
    sig.level = .05, power = p[i],
    type = "two.sample")
    samsize[j,i] <- ceiling(result$n)
  }
}

# set up graph
xrange <- range(d)
yrange <- round(range(samsize))
colors <- rainbow(length(p))
png('/home/nick/src/jaratoolbox/test/nick/stats/ttestPower.png')
plot(xrange, yrange, type="n",
  xlab="Cohen's D (d)",
  ylab="Sample Size (n)" )

# add power curves
for (i in 1:np){
  lines(d, samsize[,i], type="l", lwd=2, col=colors[i])
}

# add annotation (grid lines, title, legend)
abline(v=0, h=seq(0,yrange[2],50), lty=2, col="grey89")
abline(h=0, v=seq(xrange[1],xrange[2],.02), lty=2,
   col="grey89")
title("Sample Size Estimation for Two-sample Unpaired t-Test\n
  Sig=0.05")
legend("topright", title="Power", as.character(p),
   fill=colors)
dev.off()

