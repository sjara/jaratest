'''
Load in behavior data corresponding to the LFP data.

Create uncollapsed PSTH given a stimulus type of interest. A figure is made illustrating
stimulus onset and 
'''

from jaratoolbox import loadneuropix
from jaratoolbox import loadbehavior, behavioranalysis
from jaratoolbox import settings
import matplotlib.pyplot as plt
import jeremy_psth as jpsth
import numpy as np
import os


subject = 'feat018'
session = '2024-06-14_11-20-22'
dataStream = 'Neuropix-PXI-100.1'
rawDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject+'_raw', session)

events = loadneuropix.RawEvents(rawDataPath, dataStream)
eventOnsetTimes = events.get_onset_times() # Stimulus onset times ... 331 in total

contData = loadneuropix.Continuous(rawDataPath, dataStream)
sampleRate = contData.sampleRate
nChannels = contData.nChannels
bitVolts = contData.bitVolts

## Load in behavior data corresponding to the LFP data.
subject = 'feat018'
paradigm = 'am_tuning_curve'
session = '20240614a'
behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
bdata = loadbehavior.BehaviorData(behavFile)

eventOnsetTimes = jpsth.fix_stimuli_number_mismatch(bdata, 'currentFreq', eventOnsetTimes)

frequencies_each_trial = bdata['currentFreq']
array_of_frequencies = np.unique(bdata['currentFreq'])
trialsEachCond = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)

time_upper = 0.1 # Ex: 0.2 seconds after stimulus onset.
time_lower = 0.1 # Ex: 0.2 seconds before stimulus onset.
psth_upper = jpsth.time_to_indices(time_upper, sampleRate, 's') # Ex: Collect 3 seconds of datapoints BEYOND stimulus onset
psth_lower = jpsth.time_to_indices(time_lower, sampleRate, 's') # Ex: Collect 3 seconds of datapoints BEFORE stimulus onset
print(f"Indices below: {psth_lower}\nIndices above: {psth_upper}")

# Grab your trials of interest

psth_uncollapsed_all_trials = []
collection_outcome_list_all_trials = []
for indx, trials in enumerate(trialsEachCond.T):
    psth_uncollapsed, collection_outcome_list = jpsth.get_psth_uncollapsed(
        contData.data, contData.timestamps, eventOnsetTimes, trials, psth_upper, psth_lower
        )
    psth_uncollapsed_all_trials.append(psth_uncollapsed)
    collection_outcome_list_all_trials.append(collection_outcome_list)

'''
Estimate CSD in 1D
'''

from elephant.current_source_density import estimate_csd
from neo import AnalogSignal
import quantities as pq
import jeremy_utils as jutils

# Check with santiago if 'Record Node 101/settings.xml' needs to be modular.
xmlfile = os.path.join(rawDataPath, r'Record Node 101/settings.xml')

probeMap, probeName = jutils.get_probemap(xmlfile)

## Parse single columns
allCoords = np.array([[xcoord,ycoord] for xcoord,ycoord in zip(probeMap['xc'],probeMap['yc'])])
uniqueXCoords = np.unique(allCoords[:,0])  # Get all unique x coordinates
columnInfo = {
    f'{xCoord}': {
        "indices": np.where(allCoords[:, 0] == xCoord)[0],
        "coordinates": allCoords[allCoords[:, 0] == xCoord]
    }
    for xCoord in uniqueXCoords
}


## Grab the y-position of a single column '11'
column_identity = '11'
## Define the number of channel divisions
channel_divisions = 10 # Number of channel divisions

print(f"\nAll possible columns: {columnInfo.keys()}")
print(f"Chosen column: {column_identity}\n")

csd_list = []
for n_psth, grab_psth_uncollapsed in enumerate(psth_uncollapsed_all_trials):

    print(f"Processing PSTH [{n_psth+1}/{len(psth_uncollapsed_all_trials)}]")

    # Coordinates and psth for channel column at position 11
    coords = columnInfo[column_identity]['coordinates'][:,1]
    mean_psth = grab_psth_uncollapsed.mean(axis=0)
    mean_psth = mean_psth[:, columnInfo['11']['indices']]

    coords = coords[::channel_divisions]
    coords = np.expand_dims(coords, axis=1) ## Get the coords in the correct NxM formatting for elephant's estimate_csd function
    mean_psth = mean_psth[...,::channel_divisions]

    neo_lfp_personal = AnalogSignal(mean_psth*bitVolts, units="uV", sampling_rate = sampleRate*pq.Hz)
    neo_lfp_personal.annotate(coordinates = coords * pq.um)

    ### Available CSD functions from the Elephant package.
    '''
    available_1d = ['StandardCSD', 'DeltaiCSD', 'StepiCSD', 'SplineiCSD', 'KCSD1D']
    available_2d = ['KCSD2D', 'MoIKCSD']
    available_3d = ['KCSD3D']

    kernel_methods = ['KCSD1D', 'KCSD2D', 'KCSD3D', 'MoIKCSD']
    icsd_methods = ['DeltaiCSD', 'StepiCSD', 'SplineiCSD']
    '''

    csd_not_np = estimate_csd(neo_lfp_personal, method="KCSD1D")
    csd = np.array(csd_not_np)
    csd_list.append(csd.T)

'''
Display all csd figures in a 4x4 subplot.
'''

jutils.make_4xN_subplots(csd_list, time_lower, time_upper, nChannels, sampleRate, amplitude_units = 'μV/μm²')