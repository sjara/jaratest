'''
studyparams contains the default names and queries used in experiment and analysis
'''
STUDY_NAME = '2019astrpi'
PATH_TO_STUDY = '/home/jarauser/src/jaratest/common/2019astrpi'
# List of animals used in this study
ASTR_D1_CHR2_MICE = ['d1pi026','d1pi032','d1pi033']
#ASTR_D2_CHR2_MICE


# --- individual parameters for cell selection ---
ISI_THRESHOLD = 0.02 #maximum allowed % ISI violations per cluster
SPIKE_QUALITY_THRESHOLD = 2

R2_CUTOFF = 0.04 #minimum R^2 value for a cell to be considered frequency tuned

noiseburst_pVal = 0.05
laserpulse_pVal = 0.05#0.001 if want to be EXTRA sure not to include false positives


## --- queries to get specific cell populations ---
FIRST_FLTRD_CELLS = 'isiViolations<{} and spikeShapeQuality>{}'.format(ISI_THRESHOLD, SPIKE_QUALITY_THRESHOLD)

# D1 cells
D1_CELLS = 'laserpulse_pVal<{} and noiseburst_pVal<{}'.format(noiseburst_pVal,laserpulse_pVal) #Responded to laser, thus D1 cells
nD1_CELLS = 'laserpulse_pVal>{} and noiseburst_pVal<{}'.format(noiseburst_pVal,laserpulse_pVal)#Not responded to laser, thus non-D1 cells

## D2 cells
#D2_CELLS = 'laserpulse_pVal<{} and noiseburst_pVal<{}'.format(noiseburst_pVal,laserpulse_pVal) #Responded to laser, thus D2 cells
#nD2_CELLS = 'laserpulse_pVal>{} and noiseburst_pVal<{}'.format(noiseburst_pVal,laserpulse_pVal)#Not responded to laser, thus non-D2 cells
