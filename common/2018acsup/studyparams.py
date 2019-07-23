''' This file contains all the parameters used to identify good cells and sort cells by type.'''

STUDY_NAME = '2018acsup'

# --- list of animals included in each experimental group ---
PV_CHR2_MICE = ['band004', 'band026', 'band032', 'band033']
SOM_CHR2_MICE = ['band005', 'band015', 'band016', 'band027', 'band028', 'band029', 'band030', 'band031', 'band034','band037','band038','band044','band045','band054','band059','band060']
THAL_MICE = ['band022', 'band023']
PV_ARCHT_MICE = ['band056','band058','band062','band072']
SOM_ARCHT_MICE = ['band055', 'band057','band073']

# --- individual parameters for cell selection ---
ISI_THRESHOLD = 0.02 #maximum allowed % ISI violations per cluster
SPIKE_QUALITY_THRESHOLD = 2.5

R2_CUTOFF = 0.1 #minimum R^2 value for a cell to be considered frequency tuned
OCTAVES_CUTOFF = 0.3 #maximum octave difference between estimated best frequency and centre frequency presented

SOUND_RESPONSE_PVAL = 0.05
LASER_RESPONSE_PVAL = 0.001 #want to be EXTRA sure not to include false positives

EXC_LASER_RESPONSE_PVAL = 0.5 #for selecting putative excitatory cells NOT responsive to laser
EXC_SPIKE_WIDTH = 0.0004


# --- pandas queries to get specific cell populations ---
SINGLE_UNITS = '(isiViolations<{} or modifiedISI<{}) and spikeShapeQuality>{}'.format(ISI_THRESHOLD, ISI_THRESHOLD, SPIKE_QUALITY_THRESHOLD)
SINGLE_UNITS_INACTIVATION = 'isiViolations<{} and spikeShapeQuality>{}'.format(ISI_THRESHOLD, SPIKE_QUALITY_THRESHOLD) #the inactivation database does not have a column called "modified ISI"

# to run AFTER getting the single units, finds all cells that fit criteria for inclusion in figure 1/2
GOOD_CELLS = 'tuningFitR2>{} and octavesFromPrefFreq<{} and sustainedSoundResponsePVal<{}'.format(R2_CUTOFF, OCTAVES_CUTOFF, SOUND_RESPONSE_PVAL)

# divide cells into PV/SOM/Exc., run AFTER getting good cells
PV_CELLS = 'laserPVal<{} and laserUStat>0 and subject=={}'.format(LASER_RESPONSE_PVAL,PV_CHR2_MICE)
SOM_CELLS = 'laserPVal<{} and laserUStat>0 and subject=={}'.format(LASER_RESPONSE_PVAL,SOM_CHR2_MICE)
EXC_CELLS = '(laserPVal>{} or laserUStat<0) and spikeWidth>{} and subject=={}'.format(EXC_LASER_RESPONSE_PVAL,EXC_SPIKE_WIDTH,SOM_CHR2_MICE)

# get PV or SOM inactivated cells
PV_INACTIVATED_CELLS = 'baselineChangeFR>0 and controlSession==0 and subject=={}'.format(PV_ARCHT_MICE)
SOM_INACTIVATED_CELLS = 'baselineChangeFR>0 and controlSession==0 and subject=={}'.format(SOM_ARCHT_MICE)