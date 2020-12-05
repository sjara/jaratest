import sys
sys.path.append('..')
import os
import numpy as np
from scipy import stats
import statsmodels.stats.power

from jaratoolbox import settings

POWER = 0.8
ALPHA = 0.05

# calculate Cohen's d
# POSSIBLE ISSUE: Cohen's d assumes independent samples, but some of these samples are paired
def cohenD(sample1, sample2):
    stdev1 = stats.tstd(sample1, ddof=1)
    stdev2 = stats.tstd(sample2, ddof=1)
    pooledstdev = np.sqrt(((len(sample1) - 1) * stdev1**2 + (len(sample2) - 1) * stdev2**2) / (len(sample1) + len(sample2) - 2))
    return (np.mean(sample1) - np.mean(sample2)) / pooledstdev

# --- power analysis for AC inactivation data ---
FIGNAME = 'figure_ac_inactivation'
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)
dataFullPath = os.path.join(inactDataDir, 'all_behaviour_ac_inactivation.npz')
data = np.load(dataFullPath)

power_analysis = statsmodels.stats.power.TTestPower() # the one to use for dependent samples

# --- change in accuracy ---
laserAccuracy = data['laserAccuracy'][:,0]
controlAccuracy = data['controlAccuracy'][:,0]

effectSize = cohenD(controlAccuracy, laserAccuracy)
nobs = power_analysis.solve_power(effect_size=effectSize, power=POWER, alpha=ALPHA)
print(f"{nobs} samples needed to detect effect on accuracy of AC inactivation with power {POWER} and alpha {ALPHA}.")

# --- change in bias ---
laserBias = data['laserBias'][:,0]
controlBias = data['controlBias'][:,0]

effectSize = cohenD(controlBias, laserBias)
nobs = power_analysis.solve_power(effect_size=effectSize, power=POWER, alpha=ALPHA)
print(f"{nobs} samples needed to detect effect on bias of AC inactivation with power {POWER} and alpha {ALPHA}.")


# --- power analysis for PV and SOM inactivation data ---
FIGNAME = 'figure_inhibitory_inactivation'
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)
dataFullPath = os.path.join(inactDataDir, 'all_behaviour_inhib_inactivation.npz')
data = np.load(dataFullPath)

power_analysis = statsmodels.stats.power.TTestPower() # the one to use for dependent samples

# --- change in accuracy (PV) ---
PVlaserAccuracy = data['PVlaserAccuracy'][:,0]
PVcontrolAccuracy = data['PVcontrolAccuracy'][:,0]

effectSize = cohenD(PVcontrolAccuracy, PVlaserAccuracy)
nobs = power_analysis.solve_power(effect_size=effectSize, power=POWER, alpha=ALPHA)
print(f"{nobs} samples needed to detect effect on accuracy of PV inactivation with power {POWER} and alpha {ALPHA}.")

# --- change in accuracy (SOM) ---
SOMlaserAccuracy = data['SOMlaserAccuracy'][:,0]
SOMcontrolAccuracy = data['SOMcontrolAccuracy'][:,0]

effectSize = cohenD(SOMcontrolAccuracy, SOMlaserAccuracy)
nobs = power_analysis.solve_power(effect_size=effectSize, power=POWER, alpha=ALPHA)
print(f"{nobs} samples needed to detect effect on accuracy of SOM inactivation with power {POWER} and alpha {ALPHA}.")

# --- change in bias (PV) ---
PVlaserBias = data['PVlaserBias'][:,0]
PVcontrolBias = data['PVcontrolBias'][:,0]

effectSize = cohenD(PVcontrolBias, PVlaserBias)
nobs = power_analysis.solve_power(effect_size=effectSize, power=POWER, alpha=ALPHA)
print(f"{nobs} samples needed to detect effect on bias of PV inactivation with power {POWER} and alpha {ALPHA}.")

# --- change in bias (SOM) ---
SOMlaserBias = data['SOMlaserBias'][:,0]
SOMcontrolBias = data['SOMcontrolBias'][:,0]

effectSize = cohenD(SOMcontrolBias, SOMlaserBias)
nobs = power_analysis.solve_power(effect_size=effectSize, power=POWER, alpha=ALPHA)
print(f"{nobs} samples needed to detect effect on bias of SOM inactivation with power {POWER} and alpha {ALPHA}.")

# --- PV vs SOM change in accuracy ---
power_analysis = statsmodels.stats.power.TTestIndPower() # the one to use for independent samples

SOMchangeAccuracy = SOMlaserAccuracy - SOMcontrolAccuracy
PVchangeAccuracy = PVlaserAccuracy - PVcontrolAccuracy

effectSize = cohenD(SOMchangeAccuracy, PVchangeAccuracy)
nobs = power_analysis.solve_power(effect_size=effectSize, power=POWER, alpha=ALPHA)
print(f"{nobs} samples needed to detect different effects on accuracy of PV and SOM inactivation with power {POWER} and alpha {ALPHA}.")

# --- PV vs SOM change in bias ---
SOMchangeBias = SOMlaserBias - SOMcontrolBias
PVchangeBias = PVlaserBias - PVcontrolBias

effectSize = cohenD(SOMchangeBias, PVchangeBias)
nobs = power_analysis.solve_power(effect_size=effectSize, power=POWER, alpha=ALPHA)
print(f"{nobs} samples needed to detect different effects on bias of PV and SOM inactivation with power {POWER} and alpha {ALPHA}.")
