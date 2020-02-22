"""
A collection of functions for power analysis of data
"""
import numpy as np
import statsmodels.stats.power as power
import scipy.stats as stats


def cohens_D(pop1, pop2):
    nPop1, nPop2 = len(pop1), len(pop2)
    stdDev1, stdDev2 = np.var(pop1, ddof=2), np.var(pop2, ddof=2)
    pooledDeviation = np.sqrt((((nPop1 - 1) * stdDev1) + ((nPop2 - 1) * stdDev2))/(nPop1 + nPop2 - 2))
    mean1, mean2 = np.mean(pop1), np.mean(pop2)
    return (mean1 - mean2)/pooledDeviation
