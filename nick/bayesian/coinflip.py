import numpy as np
from scipy import stats
from matplotlib import pyplot as plt

dist = stats.beta

n_trials = [0, 1, 2, 3, 4, 5, 8, 15, 50, 500]
data = stats.bernoulli.rvs(0.5, size = n_trials[-1])
x = np.linspace(0, 1, 100)

for indNumTrials, N in enumerate(n_trials):
    sx = plt.subplot(len(n_trials)/2, 2, indNumTrials+1)

    #This is a good trick to set a label only on some subplots
    plt.xlabel("$p$, prob of heads") if indNumTrials in [0, len(n_trials)-1] else None

    #The number of heads up to this point in the data stream
    heads = data[:N].sum()

    y = dist.pdf(x, 1+heads, 1+N-heads)
    plt.plot(x, y)

plt.show()
