"""
This file contains the default names and queries used for this study.
"""

from jaratoolbox import colorpalette as cp
import matplotlib


STUDY_NAME = 'patternedOpto'

SUBJECTS = ['poni001']
REAGENTS = ['off','on']

# Date when pre/post sync light was added to videos.
PREPOST_SYNC_LIGHT_START_DATE = '2023-08-08'

# Date of session with no sync light.
N0_LIGHT_DATE = '2023-03-22'

N_FREQ = 16

STIMULI = ['high', 'low', 'down', 'up']


TIME_RANGES = {
                'Full':         [-1.0,  0.45],
                'Baseline':     [-1.0,  0],
                'Evoked':       [0.015, 0.115],
                'Onset':        [0.015, 0.065],
                'Offset':       [0.115, 0.165],
                'Sustained':    [0.065, 0.315],
                'FullEvoked':   [0.015,0.315]
            }

EVENT_KEYS = ['Evoked','Onset','Offset','Sustained','FullEvoked']

METRICS = ['ToneBaselineFiringRate', 'ToneNtrials', 'ToneFiringRateEachFreq',
                'ToneResponseMinPval', 'ToneSelectivityPval', 'ToneFiringRateBestFreq', 'ToneBestFreq', 
                'ToneAvgEvokedFiringRate', 'ToneGaussianA', 'ToneGaussianX0', 'ToneGaussianSigma', 
                'ToneGaussianY0', 'ToneGaussianRsquare']

RUNNING_THRESHOLD = 3

MIN_R_SQUARED = 0.01 #0.1 #0.05

MIN_SIGMA = 0.15  # Minimum value of Sigma for the Gaussian fit.
MAX_SIGMA = 6     # Maximum value of Sigma for the Gaussian fit.

FR_THRESHOLD = 5  # Minimum evoked firing rate to consider a cell responsive.

MAX_CHANGE_FACTOR = 1.3  # Maximum change factor to consider a cell steady

TIME_KEY_METRIC = 'ToneGaussianRsquare'