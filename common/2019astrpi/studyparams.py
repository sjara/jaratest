"""
studyparams contains the default names and queries used in experiment and analysis
"""
STUDY_NAME = '2019astrpi'
PATH_TO_STUDY = '/home/jarauser/src/jaratest/common/2019astrpi'
PATH_TO_TEST = '/home/jarauser/src/jaratest/allison/d1pi032'
DATABASE_NAME = 'direct_and_indirect_cells'
# List of animals used in this study
ASTR_D1_CHR2_MICE = ['d1pi026', 'd1pi032', 'd1pi033', 'd1pi036', 'd1pi039', 'd1pi040', 'd1pi041', 'd1pi042', 'd1pi043', 'd1pi044', 'd1pi045', 'd1pi046', 'd1pi047', 'd1pi048']
SINGLE_MOUSE = ['d1pi041']  # for data exploration/testing

# --- session name --- add new session names here if used the new names
# ideally, let's use the same session name throughout
tuningcurve = ['tuningCurve', 'tuningCurve(tc)']

# --- individual parameters for cell selection ---
ISI_THRESHOLD = 0.02  # maximum allowed % ISI violations per cluster
SPIKE_QUALITY_THRESHOLD = 2

R2_CUTOFF = 0.03  # minimum R^2 value for a cell to be considered frequency tuned

noiseburst_pVal_threshold = 0.05
laserpulse_pVal_threshold = 0.05  # 0.001 if want to be EXTRA sure not to include false positives
am_pVal_threshold = 0.05
corrected_am_pVal_threshold = 0.05/11
tuning_pVal_threshold = 0.05


# --- queries to get specific cell populations ---
FIRST_FLTRD_CELLS = 'isiViolations<{} and spikeShapeQuality>{}'.format(ISI_THRESHOLD, SPIKE_QUALITY_THRESHOLD)

# D1 cells
D1_CELLS = 'laserpulse_pVal<{} and laserpulse_dFR>0'.format(laserpulse_pVal_threshold)  # Respond to laser, thus D1-expressing cells
nD1_CELLS = 'not (laserpulse_pVal<{} and laserpulse_dFR>0)'.format(laserpulse_pVal_threshold)
# nD1_CELLS = 'laserpulse_pVal>{0} or (laserpulse_pVal<{0} and laserpulse_dFR<0)'.format(laserpulse_pVal_threshold)  # Not responded to laser, thus non-D1-expressing cells
AM_FILTER = 'am_response_pVal<{}'.format(am_pVal_threshold)
TUNING_FILTER = 'tuning_pVal<{} and rsquaredFit>{}'.format(tuning_pVal_threshold, R2_CUTOFF)

# D2 cells
# D2_CELLS = 'laserpulse_pVal<{} and noiseburst_pVal<{}'.format(noiseburst_pVal,laserpulse_pVal)  # Responded to laser, thus D2 cells
# nD2_CELLS = 'laserpulse_pVal>{} and noiseburst_pVal<{}'.format(noiseburst_pVal,laserpulse_pVal)  # Not responded to laser, thus non-D2 cells
