"""
A collection of functions for power analysis of data
"""
import numpy as np
import statsmodels.stats.power as power
import scipy.stats as stats
import matplotlib.pyplot as plt


def cohens_D(pop1, pop2):
    """
    Takes the two populations given and calculates an effect size for them
    Args:
        pop1 (np.array, pd.series, or list): List of numbers to be compared
        pop2 (np.array, pd.series, or list): Second list of numbers to be compared

    Returns:
        effectSize (float): Apporximate effect size of the tested property between two populations

    """
    nPop1, nPop2 = len(pop1), len(pop2)
    stdDev1, stdDev2 = np.var(pop1, ddof=2), np.var(pop2, ddof=2)
    pooledDeviation = np.sqrt((((nPop1 - 1) * stdDev1) + ((nPop2 - 1) * stdDev2))/(nPop1 + nPop2 - 2))
    mean1, mean2 = np.mean(pop1), np.mean(pop2)
    return (mean1 - mean2)/pooledDeviation


# TODO: Add graph of power at differing effect sizes
def calculate_power(effectSize, powerThreshold=0.8, alpha=0.05):
    """
    Calculates the power at multiple different number of observations and will return
    a plot of the power curve as well as giving the minimum value to have a power over
    0.80 for the given effect size.
    Args:
        effectSize (list or array of floats): A value between 0 and 1 (calculated by cohens_D)
        powerThreshold (float): Value used to determine minimum number of observations needed to commit type II errors
        with a (1 - value) chance. ie a powerThreshold of 0.8 means that the output will be  the minimum number of
        observations needed  to only have a 20% chance of committing type II error
        alpha (float): Non-zero value that is less than 1 that acts as the threshold for significance

    Returns:
        Number of of observations needed to pass the specified power threshold for a given effect size

    """
    messages = []
    cellCount = np.arange(1, 100, 1)
    analysis = power.TTestIndPower()
    for size in effectSize:
        for count in cellCount:
            pow_value = analysis.power(size, count, alpha)
            if pow_value > powerThreshold:
                messages.append("Effect size of {0} requires {1} cells to have a power greater than {2}".format(size, count, powerThreshold))
                break
    for message in messages:
        print(message)
