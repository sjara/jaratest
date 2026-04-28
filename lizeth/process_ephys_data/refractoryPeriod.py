"""
Load neuropixels data and show raster plots.
"""

import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

SAVE_FIGS = 0

subject = 'arch032'
sessionDate = '2025-10-16'
probeDepth = 2780

outputDir = f'/data/reports/{subject}/'

# -- Create database of cells --
inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
celldb = celldatabase.generate_cell_database(inforecFile, ignoreMissing=True)

# -- Create subset of database for just one session --
celldbSubset = celldb[(celldb.date==sessionDate) & (celldb.pdepth==probeDepth)]

# -- Load the data --
ensemble = ephyscore.CellEnsemble(celldbSubset)

sessionType = 'optoTuningAM'
ephysData, bdata = ensemble.load(sessionType)

# -- Align spikes to sound onset --
currentStim = bdata['currentFreq']
eventOnsetTimes = ephysData['events']['stimOn']
laserTrial = bdata['laserTrial']
possibleLaser = [0, 1]  # 0:NoLaser, 1:Laser
nTrials = len(currentStim)

# If we have one more (incomplete) trial in the behavior file, remove it.
if len(currentStim) == len(eventOnsetTimes)-1:
        eventOnsetTimes = eventOnsetTimes[:nTrials]

timeRange = [-0.5, 1]        
spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = \
    ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)

#################################

# import pandas as pd

# # ----- USER SETTINGS -----
# sorting_folder = f"/data/neuropixels/{subject}/multisession_{sessionDate}_{probeDepth}um_processed"      # current folder
# sampling_rate = 30000     # Hz, change if your recording used a different rate
# threshold_ms = 2          # refractory period threshold
# # -------------------------

# spike_times_path = os.path.join(sorting_folder, "spike_times.npy")
# spike_clusters_path = os.path.join(sorting_folder, "spike_clusters.npy")

# spike_times = np.load(spike_times_path).squeeze()
# spike_clusters = np.load(spike_clusters_path).squeeze()

# # Convert spike times from samples to seconds
# spike_times_sec = spike_times / sampling_rate

# threshold_sec = threshold_ms / 1000

# results = []

# for cluster_id in np.unique(spike_clusters):
#     cluster_spike_times = spike_times_sec[spike_clusters == cluster_id]
#     cluster_spike_times = np.sort(cluster_spike_times)

#     isi = np.diff(cluster_spike_times)
#     isi = isi[isi > 0]

#     total_isi = len(isi)

#     if total_isi == 0:
#         rpv = np.nan
#         n_violations = 0
#     else:
#         n_violations = np.sum(isi < threshold_sec)
#         rpv = (n_violations / total_isi) * 100

#     results.append({
#         "cluster_id": cluster_id,
#         "n_spikes": len(cluster_spike_times),
#         "n_isi": total_isi,
#         "n_refractory_violations": n_violations,
#         "rpv_percent": rpv
#     })

# df = pd.DataFrame(results)

# df["suggested_label"] = "keep"
# df.loc[df["rpv_percent"] > 1, "suggested_label"] = "questionable"
# df.loc[df["rpv_percent"] > 2, "suggested_label"] = "noise_or_MUA"

# df.to_csv(f"/data/neuropixels/{subject}/multisession_{sessionDate}_{probeDepth}um_processed/rpv_{subject}_{sessionDate}_{probeDepth}.csv", index=False)

# print(df)
# print(f"\nSaved: rpv_{subject}_{sessionDate}_{probeDepth}.csv")
#================================================================================================================================================
#################################

# import shutil
# import pandas as pd


# # =========================
# # USER SETTINGS
# # =========================

# sorting_folder = f"/data/neuropixels/{subject}/multisession_{sessionDate}_{probeDepth}um_processed" # current folder     
# sampling_rate = 30000     # Hz; change if your recording has a different sampling rate
# threshold_ms = 2          # refractory period threshold

# questionable_threshold = 1.0   # %
# noise_threshold = 2.0          # %

# # =========================
# # PATHS
# # =========================

# spike_times_path = os.path.join(sorting_folder, "spike_times.npy")
# spike_clusters_path = os.path.join(sorting_folder, "spike_clusters.npy")
# cluster_info_path = os.path.join(sorting_folder, "cluster_info.tsv")

# rpv_csv_path = os.path.join(sorting_folder, "refractory_period_violations.csv")
# backup_path = os.path.join(sorting_folder, "cluster_info_backup_before_rpv.tsv")


# # =========================
# # LOAD DATA
# # =========================

# spike_times = np.load(spike_times_path).squeeze()
# spike_clusters = np.load(spike_clusters_path).squeeze()

# spike_times_sec = spike_times / sampling_rate
# threshold_sec = threshold_ms / 1000


# # =========================
# # COMPUTE RPV PER CLUSTER
# # =========================

# results = []

# for cluster_id in np.unique(spike_clusters):
#     cluster_id = int(cluster_id)

#     cluster_spike_times = spike_times_sec[spike_clusters == cluster_id]
#     cluster_spike_times = np.sort(cluster_spike_times)

#     isi = np.diff(cluster_spike_times)
#     isi = isi[isi > 0]

#     total_isi = len(isi)

#     if total_isi == 0:
#         n_violations = 0
#         rpv_percent = np.nan
#     else:
#         n_violations = int(np.sum(isi < threshold_sec))
#         rpv_percent = (n_violations / total_isi) * 100

#     if np.isnan(rpv_percent):
#         suggested_label = "insufficient_spikes"
#     elif rpv_percent > noise_threshold:
#         suggested_label = "noise_or_MUA"
#     elif rpv_percent > questionable_threshold:
#         suggested_label = "questionable"
#     else:
#         suggested_label = "keep"

#     results.append({
#         "cluster_id": cluster_id,
#         "n_spikes": len(cluster_spike_times),
#         "n_isi": total_isi,
#         "n_violations": n_violations,
#         "rpv_percent": rpv_percent,
#         "rpv_suggested_label": suggested_label
#     })


# rpv_df = pd.DataFrame(results)


# # =========================
# # SAVE STANDALONE CSV
# # =========================



# rpv_df.to_csv(f"/data/neuropixels/{subject}/multisession_{sessionDate}_{probeDepth}um_processed/rpv_{subject}_{sessionDate}_{probeDepth}.csv", index=False)
# print(f"\nSaved: rpv_{subject}_{sessionDate}_{probeDepth}.csv")

# # =========================
# # ADD TO PHY cluster_info.tsv
# # =========================

# if not os.path.exists(cluster_info_path):
#     raise FileNotFoundError(
#         "cluster_info.tsv was not found. Open Phy once first, or check your folder."
#     )

# cluster_info = pd.read_csv(cluster_info_path, sep="\t")

# cluster_info["cluster_id"] = cluster_info["cluster_id"].astype(int)
# rpv_df["cluster_id"] = rpv_df["cluster_id"].astype(int)


# # Safety check
# phy_ids = set(cluster_info["cluster_id"])
# rpv_ids = set(rpv_df["cluster_id"])

# missing_from_phy = sorted(rpv_ids - phy_ids)
# missing_from_rpv = sorted(phy_ids - rpv_ids)

# if missing_from_phy:
#     print("\nWarning: RPV contains cluster IDs not found in cluster_info.tsv:")
#     print(missing_from_phy[:20])

# if missing_from_rpv:
#     print("\nWarning: cluster_info.tsv contains cluster IDs not found in RPV results:")
#     print(missing_from_rpv[:20])


# # Backup cluster_info.tsv
# if not os.path.exists(backup_path):
#     shutil.copy(cluster_info_path, backup_path)
#     print(f"Backup saved: {backup_path}")
# else:
#     print(f"Backup already exists: {backup_path}")


# # Remove old RPV columns if script was run before
# columns_to_remove = [
#     "n_spikes",
#     "n_isi",
#     "n_refractory_violations",
#     "rpv_percent",
#     "rpv_suggested_label"
# ]

# cluster_info = cluster_info.drop(
#     columns=[col for col in columns_to_remove if col in cluster_info.columns],
#     errors="ignore"
# )


# # Merge new RPV results
# columns_to_add = [
#     "cluster_id",
#     "n_spikes",
#     "n_isi",
#     "n_refractory_violations",
#     "rpv_percent",
#     "rpv_suggested_label"
# ]

# updated_cluster_info = cluster_info.merge(
#     rpv_df[columns_to_add],
#     on="cluster_id",
#     how="left"
# )


# # Save updated cluster_info.tsv
# updated_cluster_info.to_csv(f"/data/neuropixels/{subject}/multisession_{sessionDate}_{probeDepth}um_processed/rpv_{subject}_{sessionDate}_{probeDepth}_merged.csv", sep="\t", index=False)

# print(f"Updated Phy file: {cluster_info_path}")
# print("\nDone. Reopen Phy to see the new columns.")


#=======================================================================================================================================
#################################

import os
import numpy as np
import pandas as pd


# =========================
# USER SETTINGS
# =========================

sorting_folder = f"/data/neuropixels/{subject}/multisession_{sessionDate}_{probeDepth}um_processed" # current folder     
sampling_rate = 30000     # Hz; change if your recording has a different sampling rate
threshold_ms = 2          # refractory period threshold

questionable_threshold = 1.0   # %
noise_threshold = 2.0          # %


# =========================
# PATHS
# =========================

spike_times_path = os.path.join(sorting_folder, "spike_times.npy")
spike_clusters_path = os.path.join(sorting_folder, "spike_clusters.npy")

rpv_csv_path = os.path.join(sorting_folder, "refractory_period_violations.csv")
cluster_rpv_path = os.path.join(sorting_folder, "cluster_RPV.tsv")


# =========================
# LOAD DATA
# =========================

spike_times = np.load(spike_times_path).squeeze()
spike_clusters = np.load(spike_clusters_path).squeeze()

spike_times_sec = spike_times / sampling_rate
threshold_sec = threshold_ms / 1000


# =========================
# COMPUTE RPV PER CLUSTER
# =========================

results = []

for cluster_id in np.unique(spike_clusters):
    cluster_id = int(cluster_id)

    cluster_spike_times = spike_times_sec[spike_clusters == cluster_id]
    cluster_spike_times = np.sort(cluster_spike_times)

    isi = np.diff(cluster_spike_times)
    isi = isi[isi > 0]

    total_isi = len(isi)

    if total_isi == 0:
        n_violations = 0
        rpv_percent = np.nan
    else:
        n_violations = int(np.sum(isi < threshold_sec))
        rpv_percent = (n_violations / total_isi) * 100

    if np.isnan(rpv_percent):
        suggested_label = "insufficient_spikes"
    elif rpv_percent > noise_threshold:
        suggested_label = "noise/MUA"
    elif rpv_percent > questionable_threshold:
        suggested_label = "check"
    else:
        suggested_label = "keep"

    results.append({
        "cluster_id": cluster_id,
        "n_spikes": len(cluster_spike_times),
        "n_isi": total_isi,
        "n_violations": n_violations,
        "rpv_percent": rpv_percent,
        "rpv_label": suggested_label
    })


rpv_df = pd.DataFrame(results)


# =========================
# SAVE FULL CSV
# =========================

rpv_df.to_csv(f"/data/neuropixels/{subject}/multisession_{sessionDate}_{probeDepth}um_processed/rpv_{subject}_{sessionDate}_{probeDepth}.csv", index=False)
print(f"\nSaved: rpv_{subject}_{sessionDate}_{probeDepth}.csv")


# =========================
# SAVE PHY-COMPATIBLE TSV
# =========================

phy_rpv_df = rpv_df[
    [
        "cluster_id",
        "rpv_percent",
        "n_violations",
        "rpv_label"
    ]
]

phy_rpv_df.to_csv(cluster_rpv_path, sep="\t", index=False)

print(f"Saved Phy-compatible file: {cluster_rpv_path}")
print("\nDone. Reopen Phy to see the new RPV columns.")

#################################

# -- Plot a raster for one cell (spikes in chronological order) --
if 0:
    cellID = 27
    plt.clf()
    plt.plot(spikeTimesFromEventOnsetAll[cellID], trialIndexForEachSpikeAll[cellID], '.')
    plt.xlabel('Time from sound onset (s)')
    plt.ylabel('Trial number')
    plt.show()

# -- Find trials of each type --    
possibleStim = np.unique(currentStim)
#trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStim)
#nTrialsEachCond = trialsEachCond.sum(axis=0)  # Not used, but in case you need it
trialsEachComb = behavioranalysis.find_trials_each_combination(currentStim, possibleStim, laserTrial, possibleLaser)

#condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)
#sortingInds = np.argsort(sortedTrials)  # This will be used to sort trialIndexForEachSpike
    
# -- Plot rasters --
colorEachCond = ['0.5', 'g']
nCells = len(celldbSubset)
nRows = 4
nCols = 7
nPages = int(np.ceil(nCells/(nRows*nCols)))
fig = plt.gcf()
figSize = [25, 12.8]
fig.set_size_inches(figSize)
for indpage in range(nPages):
    plt.clf()
    someCells = np.arange(0, nRows*nCols) + indpage*nRows*nCols
    for count, indcell in enumerate(someCells):
        if indcell >= len(celldbSubset):
            break
        #sortedIndexForEachSpike = sortingInds[trialIndexForEachSpikeAll[indcell]]
        plt.subplot(nRows, nCols, count+1)
        #plt.plot(spikeTimesFromEventOnsetAll[indcell], sortedIndexForEachSpike, '.k', ms=1)
        (pRaster,hcond,zline) = extraplots.raster_plot_multicond(spikeTimesFromEventOnsetAll[indcell],
                                 indexLimitsEachTrialAll[indcell],
                                 timeRange, trialsEachComb,
                                 colorEachCond=colorEachCond)
        plt.setp(pRaster, ms=1)
        plt.xlabel('Time (s)')
        plt.ylabel(f'[{indcell}] Sorted trials')
    plt.suptitle(f'{subject} {sessionDate} {probeDepth}um {sessionType} ({indpage+1}/{nPages})',
                 fontweight='bold')
    plt.tight_layout()
    plt.show()
    #break
    plt.pause(0.1)

    if SAVE_FIGS:
        figFilename = f'{subject}_{sessionType}_{sessionDate}_{probeDepth}um_{indpage+1:02d}'
        extraplots.save_figure(figFilename, 'png', figSize, outputDir=outputDir, facecolor='w')
