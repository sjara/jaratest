"""
Default names and queries used in experiment and analysis
"""

# For directory pathing 
STUDY_NAME = '2019astrpi'
PATH_TO_STUDY = '/home/jarauser/src/jaratest/common/2019astrpi'
PATH_TO_TEST = '/home/jarauser/src/jaratest/allison/d1pi032'
DATABASE_NAME = 'direct_and_indirect_cells2'

# List of animals used in this study
ASTR_D1_CHR2_MICE = ['d1pi026', 'd1pi032', 'd1pi033', 'd1pi036', 'd1pi039', 'd1pi040', 'd1pi041', 'd1pi042',
                     'd1pi043', 'd1pi044', 'd1pi045', 'd1pi046', 'd1pi047', 'd1pi048', 'd1pi049']

SINGLE_MOUSE = ['d1pi041'] # For data exploration and testing

BRAIN_AREA_DICT = {'left_AudStr': 'LeftAstr',
                   'right_AudStr': 'RightAstr',
                   }

tuningcurve = ['tuningCurve', 'tuningCurve(tc)']

# ========================== Parameters for Cell Selection ==========================

ISI_THRESHOLD = 0.02  # maximum allowed % ISI violations per cluster
SPIKE_QUALITY_THRESHOLD = 3.5

R2_CUTOFF = 0.03  # minimum R^2 value for a cell to be considered frequency tuned

noiseburst_pVal_threshold = 0.05
laserpulse_pVal_threshold = 0.05  # 0.001 if want to be extra sure not to include false positives
laserpulse_responseCount_threshold = 0.5
am_pVal_threshold = 0.05
corrected_am_pVal_threshold = 0.05/11
tuning_pVal_threshold = 0.05

z_slice_cutoff = 301

# ========================== Queries to get Specific Cell Populations ==========================

FIRST_FLTRD_CELLS = 'isiViolations<{} and spikeShapeQuality>{}'.format(ISI_THRESHOLD, SPIKE_QUALITY_THRESHOLD)

# Striatal cell filters
LABELLED_Z = "{0} <= {1}".format('z_coord', z_slice_cutoff)
BRAIN_REGION_QUERY = "recordingSiteName == 'Caudoputamen' or recordingSiteName == ''"
BRAIN_REGION_QUERY_STRIATUM_ONLY = "recordingSiteName == 'Caudoputamen'"
D1_CELLS = 'laserpulse_pVal<{} and laserpulse_dFR>0 and laserpulse_responseFR>{}'.format(laserpulse_pVal_threshold, laserpulse_responseCount_threshold)  # Respond to laser, thus D1-expressing cells
nD1_CELLS = 'not (laserpulse_pVal<{} and laserpulse_dFR>0)'.format(laserpulse_pVal_threshold)
# nD1_CELLS = 'laserpulse_pVal>{0} or (laserpulse_pVal<{0} and laserpulse_dFR<0)'.format(laserpulse_pVal_threshold)  # Not responded to laser, thus non-D1-expressing cells
AM_FILTER = 'am_response_pVal<{}'.format(am_pVal_threshold)
TUNING_FILTER = 'tuning_pVal<{} and rsquaredFit>{}'.format(tuning_pVal_threshold, R2_CUTOFF)
PURE_TONE_FILTER = 'tuning_pVal<{}'.format(tuning_pVal_threshold)
