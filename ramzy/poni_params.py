"""
This file contains the default names and queries used for this study.
"""

from jaratoolbox import colorpalette as cp
import matplotlib
import itertools

STUDY_NAME = 'patternedOpto'

SESSION_TYPES = ['poniFreq_4x4','poniFreq_4x1','poniFreq_1x4', 'poniFreq_4x4_CiRj_2x2']

SUBJECTS = ['poni001']
REAGENTS = {
    'poniFreq':['off']+[f'C{i}R{j}' for i,j in itertools.product(range(4),range(1))],
    'poniFreqC4R1':['off']+[f'C{i}R{j}' for i,j in itertools.product(range(4),range(1))],
    'poniFreqC1R4':['off']+[f'C{i}R{j}' for i,j in itertools.product(range(1),range(4))],
    'poniAM':['off']+[f'C{i}R{j}' for i,j in itertools.product(range(4),range(1))],
    'optoFreq':['off','on'],
    'optoAM':['off','on']
}

SOUND_PREFIXES = {
    'Freq':'Tone',
    'AM':'Rate'
}

SESSION_PREFIXES = {}

# for nCol, nRow in itertools.product(range(1,5),range(1,5)):
#     for soundType in ['Freq','AM']:
#         sessionType1 = f'poni{soundType}_{nCol}x{nRow}'
#         REAGENTS[sessionType1] = ['off']+[f'C{i}R{j}' \
#                                             for i,j in itertools.product(range(nCol),range(nRow))]
#         SESSION_PREFIXES[sessionType1] = SOUND_PREFIXES[soundType]
#         for nColInner in range(1,5):
#             for nRowInner in range(1,5):
#                 for x,y in itertools.product(range(nCol),range(nRow)):
#                     sessionType2 = f'poni{soundType}_{nCol}x{nRow}_C{x}R{y}_{nColInner}x{nRowInner}'
#                     REAGENTS[sessionType2] = \
#                         ['off']+[f'C{i}R{j}' for i,j in itertools.product(range(nColInner),range(nRowInner))]
#                     SESSION_PREFIXES[sessionType2] = SOUND_PREFIXES[soundType]

for sessionType in SESSION_TYPES:
    sessionParams = sessionType.split('_')
    gridToUse = sessionParams[-1].split('x')
    nCol = int(gridToUse[0])
    nRow = int(gridToUse[1])
    soundType = sessionParams[0][4:]
    if len(sessionParams) > 2:
        gridToUse = sessionParams[1].split('x')
        nColOuter = int(gridToUse[0])
        nRowOuter = int(gridToUse[1])
        for i, j in itertools.product(range(nColOuter),range(nRowOuter)):
            nameThisSession = sessionType.replace("CiRj",f"C{i}R{j}")
            REAGENTS[nameThisSession] = ['off']+[f'C{col}R{row}' \
                                            for col,row in itertools.product(range(nCol),range(nRow))]
            SESSION_PREFIXES[nameThisSession] = SOUND_PREFIXES[soundType]
    else:
        REAGENTS[sessionType] = ['off']+[f'C{col}R{row}' \
                                    for col,row in itertools.product(range(nCol),range(nRow))]
        SESSION_PREFIXES[sessionType] = SOUND_PREFIXES[soundType]

REAGENTS_LASER = ['off','on']
REAGENTS_IMAGE = ['off']+[f'C{i}R{j}' for i,j in itertools.product(range(4),range(1))]

# SESSION_PREFIXES = {
#     'poniFreq':'Tone',
#     'poniFreqC4R1':'Tone',
#     'poniFreqC1R4':'Tone',
#     'optoFreq':'Tone',
#     'poniAM':'Rate',
#     'optoAM':'Rate'
# }



N_FREQ = 16     # number of unique tone frequencies
N_RATE = 11     # number of unique AM rates

STIMULI = ['high', 'low', 'down', 'up']


TIME_RANGES = {
                'Full':         [-1.0,  0.45],
                'Baseline':     [-1.0,  0],
                'Evoked':       [0.015, 0.115],
                'Onset':        [0.015, 0.065],
                'Sustained':    [0.065, 0.115],
                'Offset':       [0.115, 0.165],
                'Delayed':      [0.115, 0.315],
                'FullResponse':   [0.015,0.315]
            }

TIME_RANGES_AM = {
                'Full':         [-1.0,  1.0],
                'Baseline':     [-0.5,  0],
                'Evoked':       [0.015, 0.515],
                'Onset':        [0.015, 0.065],
                'Sustained':    [0.065, 0.515],
                'Offset':       [0.515, 0.565],
                'Delayed':      [0.515, 0.815],
                'FullResponse':   [0.015,0.815]
}

EVENT_KEYS = ['Evoked','Onset','Offset','Sustained','Delayed','FullResponse']

METRICS = ['BaselineFiringRate', 'Ntrials', 'FiringRateEachFreq',
                'ResponseMinPval', 'SelectivityPval', 'FiringRateBestFreq', 'BestFreq', 
                'AvgEvokedFiringRate', 'GaussianA', 'GaussianX0', 'GaussianSigma', 
                'GaussianY0', 'GaussianRsquare']

RUNNING_THRESHOLD = 3

MIN_R_SQUARED = 0.01 #0.1 #0.05

MIN_SIGMA = 0.15  # Minimum value of Sigma for the Gaussian fit.
MAX_SIGMA = 6     # Maximum value of Sigma for the Gaussian fit.

FR_THRESHOLD = 5  # Minimum evoked firing rate to consider a cell responsive.

MAX_CHANGE_FACTOR = 1.3  # Maximum change factor to consider a cell steady

TIME_KEY_METRIC = 'GaussianRsquare'