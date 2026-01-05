"""
This file contains the default names and queries used for this study.
"""

from jaratoolbox import colorpalette as cp
import matplotlib
import itertools

STUDY_NAME = 'hemisym'

OFF_RATE = {
    'poni001':(4,64),
    'poni008':(4,64),
    'poni009':(4,64),
    'poni005':(64,4),
    'poni007':(64,4),
    'LR':(4,64),
    'RL':(64,4)
}

SESSION_TYPES = ['optoTuningAMtone']

SUBJECTS = ['poni001',
            'poni005',
            'poni007',
            'poni008',
            'poni009']

SHAM_SUBJECTS= ['poni001',
                'poni005',
                'poni007',
                'poni008',
                'poni009']


PDEPTH_EACH_SUBJECT = {'poni001':[2360],
                      'poni005':[2250],
                      'poni007':[1580,2300],
                      'poni008':[1530],
                      'poni009':[1520]}



SESSION_DATES_EACH_SUBJECT = {  'poni001':['2025-11-03','2025-11-07','2025-11-12'],
                                'poni005':['2025-11-06','2025-11-07','2025-11-12'],
                                'poni007':['2025-10-29','2025-11-18','2025-11-21',
                                           '2025-11-06','2025-11-11','2025-11-13'],
                                'poni008':['2025-11-17','2025-11-19','2025-11-21'],
                                'poni009':['2025-11-05','2025-11-11','2025-11-17']   }

SESSION_DATES_EACH_SITE = {     2360:['2025-11-03','2025-11-07','2025-11-12'],
                                2250:['2025-11-06','2025-11-07','2025-11-12'],
                                2300:['2025-10-29','2025-11-18','2025-11-21'],
                                1580:['2025-11-06','2025-11-07','2025-11-11','2025-11-13'],
                                1530:['2025-11-17','2025-11-19','2025-11-21'],
                                1520:['2025-11-05','2025-11-11','2025-11-12','2025-11-17']   }

SHAM_DATES_EACH_SITE = {
                                2360:['2025-12-03'],
                                2250:['2025-12-03'],
                                2300:['2025-12-05'],
                                1580:['2025-12-04'],
                                1530:['2025-12-05'],
                                1520:['2025-12-04']
}


SHAM_DATES_EACH_SUBJECT = {     'poni001':['2025-12-03'],
                                'poni005':['2025-12-03'],
                                'poni007':['2025-12-04','2025-12-05'],
                                'poni008':['2025-12-05'],
                                'poni009':['2025-12-04']}



SUBJECTS_EACH_IMPLANT = {
    'LR'    :   ['poni001','poni008','poni009'],
    'RL'    :   ['poni005','poni007']
}

SITES_EACH_IMPLANT = {
    'LR'    :   [2360,1530,1520],
    'RL'    :   [2250,1580,2300]
}

SUBJECT_EACH_SITE = {
    2360:'poni001',
    2250:'poni005',
    1580:'poni007',
    2300:'poni007',
    1530:'poni008',
    1520:'poni009'
}

SUBJECTS_EACH_SHAM = {
    'LR'    :   ['poni001','poni008','poni009'],
    'RL'    :   ['poni005','poni007']
}

REAGENTS_ALL = [str(i)+'Hz_off' for i in [0,4,64]]+[str(i)+'Hz_on' for i in [0,4,64]]
MOD_RATES_ALL = [0,4,64]

REAGENTS = {
    'poniFreq':['off']+[f'C{i}R{j}' for i,j in itertools.product(range(4),range(1))],
    'poniFreqC4R1':['off']+[f'C{i}R{j}' for i,j in itertools.product(range(4),range(1))],
    'poniFreqC1R4':['off']+[f'C{i}R{j}' for i,j in itertools.product(range(1),range(4))],
    'poniAM':['off']+[f'C{i}R{j}' for i,j in itertools.product(range(4),range(1))],
    'optoTuningFreq':['0Hz_off','0Hz_on'],
    'optoAM':['off','on'],
    'optoTuningAMtone':[str(i)+'Hz_off' for i in [4,64]]+[str(i)+'Hz_on' for i in [4,64]],
    'optoShamAMtone':[str(i)+'Hz_off' for i in [4,64]]+[str(i)+'Hz_on' for i in [4,64]],
    'poniAMtone_2x1': [str(i)+'Hz_off' for i in [4,64]]\
                        +[str(i)+'Hz_C1' for i in [4,64]]\
                            +[str(i)+'Hz_C2' for i in [4,64]],
    # 'optoTuningAMtone': [4,64],
    'AMtone':[str(i) for i in [4,8,16,32,64]]
}

SESSION_MODRATES = {'optoTuningFreq':[0],
                    'optoTuningAMtone':[4,64],
                    'optoShamAMtone':[4,64]}

SOUND_PREFIXES = {
    'Freq':'Tone',
    'AM':'Rate',
    'AMtone':'Tone'
}

SESSION_PREFIXES = {'AMtone':'Tone','optoTuningAMtone':'Tone','optoShamAMtone':'Tone','poniAMtone_2x1':'Tone',
                    'optoTuningFreq':'Tone'}




N_FREQ = 16     # number of unique tone frequencies
N_RATE = 2     # number of unique AM rates

STIMULI = ['high', 'low', 'down', 'up']

TIME_RANGES_AM = {
                'Full':         [-1.0,  1.0],
                'Baseline':     [-0.75, -0.25],
                'Evoked':       [0.010, 0.510],
                'Onset':        [0.010, 0.260],
                'Interim':      [0.135, 0.385],
                'Sustained':    [0.260, 0.510],
                'Offset':       [0.385, 0.635]
            }

TIME_RANGES_FREQ = {
                'Full':         [-1.0,  1.0],
                'Baseline':     [-0.5,  -0.25],
                'Evoked':       [0.010, 0.260],
                'Onset':        [0.010, 0.135],
                'Interim':      [0.072, 0.197],
                'Sustained':    [0.135, 0.260],
                'Offset':       [0.197, 0.322]
}

# TIME_RANGES_AM = {
#                 'Full':         [-1.0,  1.0],
#                 'Baseline':     [-0.75,  0.25],
#                 'Evoked':       [0.015, 0.515],
#                 'Onset':        [0.015, 0.265],
#                 'Offset':       [0.265, 0.515],
#                 'Sustained':    [0.140, 0.390]
#             }

# TIME_RANGES_FREQ = {
#                 'Full':         [-1.0,  1.0],
#                 'Baseline':     [-0.50,  0.25],
#                 'Evoked':       [0.015, 0.265],
#                 'Onset':        [0.015, 0.140],
#                 'Offset':       [0.140, 0.265],
#                 'Sustained':    [0.077, 0.202]
# }

EVENT_KEYS = ['Evoked','Onset','Interim','Sustained','Offset']

METRICS = ['BaselineFiringRate', 'Ntrials', 'BaselineSigma', 
           'LaserFiringRate','LaserSigma','LaserPval',
           'ResponseMinPval', 'SelectivityPval', 'SelectivityKstat', 
            'FiringRateBestFreq', 'BestFreq', 'DiscrimRatio','EvokedSigmaRMS','ClusteringIndex','PooledSigma',
            'AvgEvokedFiringRate', 'GaussianA', 'GaussianX0', 'GaussianSigma', 'FanoIndex',
            'GaussianY0', 'GaussianRsquare','MeanDiscrimRaw','MeanDiscrim','DiscrimBestFreq',
            'SigmaAvgFR','FanoFactor','FanoFactorSmoothed','SelectivityIndex','VariabilityIndex',
            'FiringRateEachFreq','FiringRateEachFreqSmoothed','DiscrimEachFreq', #'ZscoreEachFreq',
            'SigmaEachFreq','NormResponseEachOctave','FiringRateEachOctave']

MEASUREMENTS = [['BaselineFiringRate', 'Ntrials', 'BaselineSigma'], 
                ['ResponseMinPval', 'SelectivityPval', 'SelectivityKstat', 
                'FiringRateBestFreq', 'BestFreq', 
                'AvgEvokedFiringRate', 'GaussianA', 'GaussianX0', 'GaussianSigma', 
                'GaussianY0', 'GaussianRsquare','MeanDiscrim','DiscrimBestFreq',
                'SigmaAvgFR','NormChangeIndex','FanoFactor','VariabilityIndex',
                'FiringRateEachFreq','DiscrimEachFreq','SigmaEachFreq','NormResponseEachOctave']]


BLNORM = True
BLNORM = False

# TEST = True
TEST = False

RUNNING_THRESHOLD = 3

SMOOTHING_WINDOW = 2

MIN_R_SQUARED = 0.2 #0.1 #0.05
MIN_PVAL = 0.05
MIN_DPRIME = 1
MIN_FANO = 1

MIN_SIGMA = 0.15  # Minimum value of Sigma for the Gaussian fit.
MAX_SIGMA = 6     # Maximum value of Sigma for the Gaussian fit.

FR_THRESHOLD = 1 if BLNORM else 2 # Minimum evoked firing rate to consider a cell responsive.

MAX_CHANGE_FACTOR = 1.3  # Maximum change factor to consider a cell steady


MIN_MODULATION = 0.05

TIME_KEY_METRIC = 'SelectivityIndex'