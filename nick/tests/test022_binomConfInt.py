'''
We can model each trial as a Bernoulli trial since there are essentially two outcomes:
either the mouse went right or it did not. Since this is the case, the outcome of each
trial can be determined by P(went to the right) = p, since the probability of going 
to the left is 1-p. The expected number of times that a mouse goes to the right in a given
set of trials is n*p, and the variance should be n*p(1-p)

Supose x_1, x_2, ..., x_n are a sample of size n from a bernoulli distribution. The sum 
of all the successes (success = 1, failure = 0) follows a binomial distribution. 

The probability mass function (pmf) of this distribution is 

P(number of times right) = n!/(k! * (n-k)!) * p**k * (1-p)**(n-k)

This formula can be understood like this: We want exactly k successes (p**k) and n-k 
failures (1-p)**(n-k). However, the successes and failures can occur anywhere within the
n trials, and there are n!/(k! * (n-k)!) ways of distributing k successes in a sequence of 
n trials. 

We can estimate p as the sum of the successes over the number of trials. 

The variance of p is p(1-p)/n, and the standard deviation is sqrt(p(1-p)/n)

'''
