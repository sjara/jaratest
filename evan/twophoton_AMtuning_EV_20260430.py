#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Amplitude modulation (AM) tuning of neurons recorded with two-photon imaging.
"""

import matplotlib.pyplot as plt
import numpy as np
from jaratoolbox import twophotonanalysis
from jaratoolbox import behavioranalysis

# -----------------------------
# SESSION INFO
# -----------------------------
subject = 'imag029'
date = '20260424'
session = '006'   # change if needed
plane = 0

# -----------------------------
# LOAD DATA
# -----------------------------
data2p = twophotonanalysis.TwoPhoton(
    subject, date, session, plane,
    paradigm='am_tuning'
)

print(f"Loaded {data2p.roiF.shape[0]} ROIs from {data2p.data_path}")
print(f"Sampling rate: {data2p.srate} Hz")

# In[24]:


print([attr for attr in dir(data2p) if 'roi' in attr.lower() or 'cell' in attr.lower()])

# In[2]:


# ============================================================
# SET PATHS + SAVE FLAG
# ============================================================

import os
from pathlib import Path
import numpy as np

# -----------------------------
# PROMPT USER
# -----------------------------
suite2p_dir = input("Enter path to Suite2p plane folder (e.g., .../suite2p/plane0):\n").strip()
output_dir  = input("Enter path for local analysis outputs:\n").strip()

save_flag = input("Do you want to save outputs? [y/n]: ").strip().lower()

# normalize paths
suite2p_dir = Path(suite2p_dir).expanduser().resolve()
output_dir  = Path(output_dir).expanduser().resolve()

# -----------------------------
# VALIDATE SUITE2P DIR
# -----------------------------
if not suite2p_dir.exists():
    raise FileNotFoundError(f"Suite2p directory not found:\n{suite2p_dir}")

required_files = ["ops.npy", "iscell.npy", "stat.npy"]

for f in required_files:
    if not (suite2p_dir / f).exists():
        raise FileNotFoundError(f"Missing {f} in:\n{suite2p_dir}")

# quick sanity check
iscell = np.load(suite2p_dir / "iscell.npy")
print(f"Suite2p ROIs: {iscell.shape[0]}")

# -----------------------------
# SAVE FLAG
# -----------------------------
SAVE_OUTPUTS = save_flag in ["y", "yes"]

# -----------------------------
# HANDLE OUTPUT DIR
# -----------------------------
if SAVE_OUTPUTS:
    if not output_dir.exists():
        create = input(f"Output directory does not exist. Create it? [y/n]: ").strip().lower()
        if create in ["y", "yes"]:
            output_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created: {output_dir}")
        else:
            raise ValueError("Output directory must exist if saving is enabled.")

# -----------------------------
# STORE GLOBALS
# -----------------------------
SUITE2P_DIR = suite2p_dir
OUTPUT_DIR  = output_dir

# -----------------------------
# SUMMARY
# -----------------------------
print("\nUsing directories:")
print(f"Suite2p dir : {SUITE2P_DIR}")
print(f"Output dir  : {OUTPUT_DIR}")
print(f"Save outputs: {SAVE_OUTPUTS}")

# In[3]:


vars(data2p);

# In[4]:


data2p.bdata;

# In[6]:


print(data2p.bdata.labels['stimType'][data2p.bdata['stimType'][0]])
print(np.unique(data2p.bdata['currentFreq']))
print(data2p.bdata['stimDur'][0])
print(data2p.bdata['isiMean'][0])

# In[6]:


print(data2p.bdata.keys())

# In[7]:


data2p.bdata['soundLocation']

# In[8]:


np.unique(data2p.bdata['currentFreq'])

# In[9]:


data2p.roiF.shape

# In[3]:


# ============================================================
# EVENT-LOCKED AVERAGE (DEFINE CELL SET ONCE)
# ============================================================

if 1:
    time_range = [-1, 3.0]

    # -----------------------------
    # DEFINE CELL POPULATION (DO THIS ONCE)
    # -----------------------------
    data2p.filter_cells(prob_threshold=0.001)

    signal_type = 'dF/F'

    # -----------------------------
    # EVENT-LOCKED DATA
    # -----------------------------
    eventlocked, tvec, valid_events = data2p.event_locked_average(
        time_range=time_range,
        dff=(signal_type == 'dF/F')
    )

    # eventlocked shape: (cells, trials, time)
    trialavg = eventlocked.mean(axis=1)

    n_cells = eventlocked.shape[0]
    print(f"Cells used (after filtering): {n_cells}")

    # -----------------------------
    # PLOT
    # -----------------------------
    fig = plt.figure(1)
    fig.clf()
    fig.set_constrained_layout(True)

    ax0 = plt.subplot(4, 1, (1, 3))
    plt.imshow(
        trialavg,
        interpolation='nearest',
        extent=[time_range[0], time_range[1], n_cells, 0],
        aspect='auto',
        cmap='viridis'
    )

    plt.colorbar(label=f'{signal_type}')
    plt.axvline(0, color='darkred')

    plt.title(f'Event-locked average (AM tuning)\n{subject} {date} {session} p{plane}')
    plt.ylabel('Neuron')
    plt.setp(ax0.get_xticklabels(), visible=False)

    ax1 = plt.subplot(4, 1, 4, sharex=ax0)
    plt.plot(tvec, np.nanmean(trialavg, axis=0), lw=2)
    plt.axvline(0, color='darkred')

    plt.xlabel('Time from sound onset (s)')
    plt.ylabel(f'Mean {signal_type}')

    plt.show()

    # -----------------------------
    # SAVE (OPTIONAL)
    # -----------------------------
    if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
        filename = f"{subject}_{date}_{session}_p{plane}_AM_eventlocked_avg.png"
        save_path = OUTPUT_DIR / filename

        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to:\n{save_path}")

# In[5]:


for k in data2p.bdata.keys():
    print(k)

# In[7]:


# ============================================================
# AM TUNING CURVES (ALL CELLS)
# ============================================================

if 1:

    time_range = [0, 1.0]

    # -----------------------------
    # AM VARIABLE (CORRECT)
    # -----------------------------
    current_am = data2p.bdata['currentFreq']   # AM rate (Hz)
    print("Using currentFreq as AM rate (Hz)")

    # -----------------------------
    # FIX TRIAL MISMATCH
    # -----------------------------
    n_trials_2p = len(data2p.event_onset)
    n_trials_behavior = len(current_am)

    if n_trials_2p < n_trials_behavior:
        current_am = current_am[:n_trials_2p]
    elif n_trials_2p > n_trials_behavior:
        data2p.event_onset = data2p.event_onset[:n_trials_behavior]

    # -----------------------------
    # EVENT-LOCKED
    # -----------------------------
    eventlocked, tvec, valid_events = data2p.event_locked_average(
        time_range=time_range,
        dff=True
    )

    n_cells, n_trials, _ = eventlocked.shape

    # align behavior to valid events
    current_am = current_am[valid_events]

    # -----------------------------
    # AM STRUCTURE
    # -----------------------------
    possible_am = np.unique(current_am)
    n_am = len(possible_am)

    trials_each_am = behavioranalysis.find_trials_each_type(
        current_am, possible_am
    )

    # -----------------------------
    # COMPUTE TUNING CURVES
    # -----------------------------
    tuning_curves = np.full((n_cells, n_am), np.nan)

    for k in range(n_am):
        trials = trials_each_am[:, k]

        if trials.sum() == 0:
            continue

        tuning_curves[:, k] = np.nanmean(
            eventlocked[:, trials, :],
            axis=(1, 2)
        )

    # -----------------------------
    # PLOT
    # -----------------------------
    fig = plt.figure(2)
    fig.clf()
    fig.set_constrained_layout(True)

    # -----------------------------
    # INDIVIDUAL CURVES
    # -----------------------------
    ax1 = plt.subplot(2, 1, 1)

    for i in range(n_cells):
        plt.plot(
            possible_am,
            tuning_curves[i],
            'o-',
            alpha=0.3,
            lw=0.5
        )

    plt.xscale('log')
    ax1.set_xticks(possible_am)
    ax1.set_xticklabels([f"{am:.0f}" for am in possible_am])

    plt.xlabel("AM rate (Hz)")
    plt.ylabel("Mean dF/F")
    plt.title(f"AM tuning curves - all cells ({subject} {date} {session} p{plane})")
    plt.grid(True, alpha=0.3)

    # -----------------------------
    # MEAN CURVE
    # -----------------------------
    ax2 = plt.subplot(2, 1, 2)

    mean_tuning = np.nanmean(tuning_curves, axis=0)
    sem_tuning  = np.nanstd(tuning_curves, axis=0) / np.sqrt(n_cells)

    plt.errorbar(
        possible_am,
        mean_tuning,
        yerr=sem_tuning,
        marker='o',
        capsize=5,
        lw=2
    )

    plt.xscale('log')
    ax2.set_xticks(possible_am)
    ax2.set_xticklabels([f"{am:.0f}" for am in possible_am])

    plt.xlabel("AM rate (Hz)")
    plt.ylabel("Mean dF/F")
    plt.title(f"Average AM tuning curve (n={n_cells} cells)")
    plt.grid(True, alpha=0.3)

    plt.show()

    # -----------------------------
    # SAVE (OPTIONAL)
    # -----------------------------
    if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
        filename = f"{subject}_{date}_{session}_p{plane}_AM_tuning_curves.png"
        save_path = OUTPUT_DIR / filename

        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to:\n{save_path}")

# In[12]:


possible_freq

# In[59]:


np.unique(data2p.bdata['currentFreq'], return_counts=True)

# In[20]:


# ============================================================
# RASTERMAP OF FREQUENCY TUNING (RESPONSIVE CELLS ONLY)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis

# -----------------------------
# PARAMETERS
# -----------------------------
time_range = [-1, 1.0]
baseline_win = lambda t: t < 0
response_win = lambda t: (t > 0) & (t < 0.5)

min_response = 0.02
min_trials = 3

# -----------------------------
# PREP DATA
# -----------------------------
data2p.filter_cells(prob_threshold=0.5)

# match trials
n_trials_2p = len(data2p.event_onset)
n_trials_behavior = len(data2p.bdata['currentFreq'])
if n_trials_2p < n_trials_behavior:
    data2p.bdata['currentFreq'] = data2p.bdata['currentFreq'][:n_trials_2p]
elif n_trials_2p > n_trials_behavior:
    data2p.event_onset = data2p.event_onset[:n_trials_behavior]

# event-locked
eventlocked, tvec, valid_events = data2p.event_locked_average(time_range=time_range, dff=True)
eventlocked = eventlocked[:, valid_events, :]

n_cells, n_trials, _ = eventlocked.shape

# -----------------------------
# FREQUENCY STRUCTURE
# -----------------------------
current_freq = data2p.bdata['currentFreq'][valid_events]
possible_freq = np.unique(current_freq)
n_freq = len(possible_freq)

trials_each_freq = behavioranalysis.find_trials_each_type(current_freq, possible_freq)

# -----------------------------
# COMPUTE TUNING CURVES
# -----------------------------
tuning_curves = np.zeros((n_cells, n_freq))

bwin = baseline_win(tvec)
rwin = response_win(tvec)

for k in range(n_freq):
    trials = trials_each_freq[:, k]
    
    if trials.sum() < min_trials:
        tuning_curves[:, k] = np.nan
        continue
    
    data_f = eventlocked[:, trials, :]
    
    baseline = np.nanmean(data_f[:, :, bwin], axis=(1,2))
    response = np.nanmean(data_f[:, :, rwin], axis=(1,2))
    
    tuning_curves[:, k] = response - baseline

# -----------------------------
# SELECT RESPONSIVE CELLS
# -----------------------------
peak_response = np.nanmax(tuning_curves, axis=1)

responsive = peak_response > min_response
tuning_curves_resp = tuning_curves[responsive]

print(f"{responsive.sum()} / {n_cells} cells responsive")

# -----------------------------
# SORT BY BEST FREQUENCY
# -----------------------------
best_idx = np.nanargmax(tuning_curves_resp, axis=1)
best_freq = possible_freq[best_idx]

sort_idx = np.argsort(best_freq)
tuning_sorted = tuning_curves_resp[sort_idx]

# normalize per neuron
tuning_norm = tuning_sorted / np.nanmax(tuning_sorted, axis=1, keepdims=True)

# -----------------------------
# PLOT
# -----------------------------
fig = plt.figure(figsize=(6, 8))

plt.imshow(
    tuning_norm,
    aspect='auto',
    cmap='viridis',
    interpolation='nearest'
)

plt.colorbar(label='Normalized response')

plt.xticks(
    np.arange(n_freq),
    [f"{f/1000:.1f}" for f in possible_freq],
    rotation=45
)

plt.xlabel("Frequency (kHz)")
plt.ylabel("Neurons (sorted by best frequency)")
plt.title("Frequency tuning raster (responsive cells)")

plt.tight_layout()
plt.show()

# -----------------------------
# SAVE (CONDITIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_tuning_raster.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[15]:


# ============================================================
# RASTERMAP OF FREQUENCY TUNING SPLIT BY RED CLASSIFICATION
# (LEFT: green-only, RIGHT: green + red)
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis

# -----------------------------
# PARAMETERS
# -----------------------------
time_range = [-1, 1.0]
baseline_win = lambda t: t < 0
response_win = lambda t: (t > 0) & (t < 0.5)

min_response = 0.02
min_trials = 3

# -----------------------------
# LOAD CELL CLASSIFICATION
# -----------------------------
assert 'SUITE2P_DIR' in globals(), "Define SUITE2P_DIR pointing to suite2p/plane0"

iscell_path  = os.path.join(SUITE2P_DIR, 'iscell.npy')
redcell_path = os.path.join(SUITE2P_DIR, 'redcell.npy')

assert os.path.exists(iscell_path), f"Missing: {iscell_path}"
assert os.path.exists(redcell_path), f"Missing: {redcell_path}"

iscell  = np.load(iscell_path)[:,0].astype(bool)
redcell = np.load(redcell_path)[:,0].astype(bool)

green_cells   = iscell
green_not_red = green_cells & (~redcell)
green_and_red = green_cells & redcell

# -----------------------------
# PREP DATA
# -----------------------------
data2p.filter_cells(prob_threshold=0.5)

# match trials
n_trials_2p = len(data2p.event_onset)
n_trials_behavior = len(data2p.bdata['currentFreq'])
if n_trials_2p < n_trials_behavior:
    data2p.bdata['currentFreq'] = data2p.bdata['currentFreq'][:n_trials_2p]
elif n_trials_2p > n_trials_behavior:
    data2p.event_onset = data2p.event_onset[:n_trials_behavior]

# event-locked
eventlocked, tvec, valid_events = data2p.event_locked_average(time_range=time_range, dff=True)
eventlocked = eventlocked[:, valid_events, :]

n_cells, n_trials, _ = eventlocked.shape

# -----------------------------
# FREQUENCY STRUCTURE
# -----------------------------
current_freq = data2p.bdata['currentFreq'][valid_events]
possible_freq = np.unique(current_freq)
n_freq = len(possible_freq)

trials_each_freq = behavioranalysis.find_trials_each_type(current_freq, possible_freq)

# -----------------------------
# COMPUTE TUNING CURVES
# -----------------------------
tuning_curves = np.zeros((n_cells, n_freq))

bwin = baseline_win(tvec)
rwin = response_win(tvec)

for k in range(n_freq):
    trials = trials_each_freq[:, k]
    
    if trials.sum() < min_trials:
        tuning_curves[:, k] = np.nan
        continue
    
    data_f = eventlocked[:, trials, :]
    
    baseline = np.nanmean(data_f[:, :, bwin], axis=(1,2))
    response = np.nanmean(data_f[:, :, rwin], axis=(1,2))
    
    tuning_curves[:, k] = response - baseline

# -----------------------------
# SELECT RESPONSIVE CELLS
# -----------------------------
peak_response = np.nanmax(tuning_curves, axis=1)
responsive = peak_response > min_response

print(f"{responsive.sum()} / {n_cells} cells responsive")

# -----------------------------
# SPLIT RESPONSIVE CELLS BY TYPE
# -----------------------------
responsive_idx = np.where(responsive)[0]

idx_green_not_red = responsive_idx[green_not_red[responsive_idx]]
idx_green_and_red = responsive_idx[green_and_red[responsive_idx]]

tuning_gnr = tuning_curves[idx_green_not_red]
tuning_gr  = tuning_curves[idx_green_and_red]

def sort_and_normalize(tuning):
    if tuning.shape[0] == 0:
        return tuning
    
    best_idx = np.nanargmax(tuning, axis=1)
    best_freq = possible_freq[best_idx]
    sort_idx = np.argsort(best_freq)
    
    tuning_sorted = tuning[sort_idx]
    tuning_norm = tuning_sorted / np.nanmax(tuning_sorted, axis=1, keepdims=True)
    
    return tuning_norm

tuning_gnr_norm = sort_and_normalize(tuning_gnr)
tuning_gr_norm  = sort_and_normalize(tuning_gr)

print(f"Green only: {tuning_gnr_norm.shape[0]} cells")
print(f"Green + red: {tuning_gr_norm.shape[0]} cells")

# -----------------------------
# PLOT SIDE-BY-SIDE
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 8), constrained_layout=True)

# LEFT: green only
if tuning_gnr_norm.shape[0] > 0:
    im0 = ax[0].imshow(
        tuning_gnr_norm,
        aspect='auto',
        cmap='viridis',
        interpolation='nearest'
    )
    ax[0].set_title("Green only (not red)")
else:
    im0 = None
    ax[0].set_title("Green only (none)")

# RIGHT: green + red
if tuning_gr_norm.shape[0] > 0:
    im1 = ax[1].imshow(
        tuning_gr_norm,
        aspect='auto',
        cmap='viridis',
        interpolation='nearest'
    )
    ax[1].set_title("Green + red (tdTomato+)")
else:
    im1 = None
    ax[1].set_title("Green + red (none)")

# formatting
for a in ax:
    a.set_xticks(np.arange(n_freq))
    a.set_xticklabels([f"{f/1000:.1f}" for f in possible_freq], rotation=45)
    a.set_xlabel("Frequency (kHz)")
    a.set_ylabel("Neurons (sorted by best frequency)")

# colorbar
im_for_cbar = im0 if im0 is not None else im1
if im_for_cbar is not None:
    cbar = fig.colorbar(im_for_cbar, ax=ax)
    cbar.set_label('Normalized response')

plt.show()

# -----------------------------
# SAVE (CONDITIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_tuning_raster_split_red.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[8]:


# ============================================================
# RASTERMAP OF AM TUNING SPLIT BY RED CLASSIFICATION
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis

# -----------------------------
# PARAMETERS
# -----------------------------
time_range = [-1, 1.0]
baseline_win = lambda t: t < 0
response_win = lambda t: (t > 0) & (t < 0.5)

min_trials = 3

# -----------------------------
# PATHS
# -----------------------------
assert 'SUITE2P_DIR' in globals(), "Define SUITE2P_DIR pointing to suite2p/plane0"

# -----------------------------
# PREP DATA (DO NOT FILTER AGAIN)
# -----------------------------
n_trials_2p = len(data2p.event_onset)
n_trials_behavior = len(data2p.bdata['currentFreq'])

if n_trials_2p < n_trials_behavior:
    data2p.bdata['currentFreq'] = data2p.bdata['currentFreq'][:n_trials_2p]
elif n_trials_2p > n_trials_behavior:
    data2p.event_onset = data2p.event_onset[:n_trials_behavior]

eventlocked, tvec, valid_events = data2p.event_locked_average(
    time_range=time_range, dff=True
)

n_cells, n_trials, _ = eventlocked.shape

# -----------------------------
# LOAD + ALIGN RED CELL LABELS
# -----------------------------
iscell_full  = np.load(os.path.join(SUITE2P_DIR, 'iscell.npy'))
redcell_full = np.load(os.path.join(SUITE2P_DIR, 'redcell.npy'))[:,0].astype(bool)

iscell_data = data2p.iscell

inds = []
for row in iscell_data:
    matches = np.where(
        (iscell_full[:,0] == row[0]) &
        (np.isclose(iscell_full[:,1], row[1]))
    )[0]
    if len(matches) == 0:
        raise ValueError("Could not match a cell between data2p and Suite2p")
    inds.append(matches[0])

inds = np.array(inds)
redcell = redcell_full[inds]

assert len(redcell) == n_cells, "Alignment failed"

green_not_red = ~redcell
green_and_red = redcell

print(f"Total cells: {n_cells}")
print(f"Green only: {green_not_red.sum()}")
print(f"Green + red: {green_and_red.sum()}")

# -----------------------------
# AM STRUCTURE (FIXED)
# -----------------------------
current_am = data2p.bdata['currentFreq'][valid_events]
possible_am = np.unique(current_am)
n_am = len(possible_am)

trials_each_am = behavioranalysis.find_trials_each_type(current_am, possible_am)

# -----------------------------
# COMPUTE TUNING CURVES
# -----------------------------
tuning_curves = np.zeros((n_cells, n_am))

bwin = baseline_win(tvec)
rwin = response_win(tvec)

for k in range(n_am):
    trials = trials_each_am[:, k]

    if trials.sum() < min_trials:
        tuning_curves[:, k] = np.nan
        continue

    data_f = eventlocked[:, trials, :]

    baseline = np.nanmean(data_f[:, :, bwin], axis=(1,2))
    response = np.nanmean(data_f[:, :, rwin], axis=(1,2))

    tuning_curves[:, k] = response - baseline

# -----------------------------
# SPLIT CELLS
# -----------------------------
idx_green_not_red = np.where(green_not_red)[0]
idx_green_and_red = np.where(green_and_red)[0]

tuning_gnr = tuning_curves[idx_green_not_red]
tuning_gr  = tuning_curves[idx_green_and_red]

def sort_and_normalize(tuning):
    if tuning.shape[0] == 0:
        return tuning

    best_idx = np.nanargmax(tuning, axis=1)
    best_am = possible_am[best_idx]

    sort_idx = np.argsort(best_am)

    tuning_sorted = tuning[sort_idx]
    tuning_norm = tuning_sorted / np.nanmax(tuning_sorted, axis=1, keepdims=True)

    return tuning_norm

tuning_gnr_norm = sort_and_normalize(tuning_gnr)
tuning_gr_norm  = sort_and_normalize(tuning_gr)

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 8), constrained_layout=True)

# LEFT: green only
if tuning_gnr_norm.shape[0] > 0:
    im0 = ax[0].imshow(tuning_gnr_norm, aspect='auto', cmap='viridis')
    ax[0].set_title("Green only (not red)")
else:
    im0 = None
    ax[0].set_title("Green only (none)")

# RIGHT: tdTomato+
if tuning_gr_norm.shape[0] > 0:
    im1 = ax[1].imshow(tuning_gr_norm, aspect='auto', cmap='viridis')
    ax[1].set_title("tdTomato+ (yellow cells)")
else:
    im1 = None
    ax[1].set_title("tdTomato+ (none)")

# X axis (AM rate)
for a in ax:
    a.set_xticks(np.arange(n_am))
    a.set_xticklabels([f"{am:.0f}" for am in possible_am], rotation=45)
    a.set_xlabel("AM rate (Hz)")
    a.set_ylabel("Neurons (sorted by best AM)")

# integer y ticks on right
if tuning_gr_norm.shape[0] > 0:
    step = max(1, tuning_gr_norm.shape[0] // 10)
    yticks = np.arange(0, tuning_gr_norm.shape[0], step)
    ax[1].set_yticks(yticks)
    ax[1].set_yticklabels([str(int(y)) for y in yticks])

# colorbar
im_for_cbar = im0 if im0 is not None else im1
if im_for_cbar is not None:
    cbar = fig.colorbar(im_for_cbar, ax=ax)
    cbar.set_label('Normalized response')

plt.show()

# In[13]:


# ============================================================
# RASTERMAP OF AM TUNING SPLIT BY RED CLASSIFICATION
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis

# -----------------------------
# PARAMETERS
# -----------------------------
time_range = [-1, 1.0]
baseline_win = lambda t: t < 0
response_win = lambda t: (t > 0) & (t < 0.5)

min_trials = 3

# -----------------------------
# PATHS
# -----------------------------
assert 'SUITE2P_DIR' in globals(), "Define SUITE2P_DIR pointing to suite2p/plane0"

# -----------------------------
# PREP DATA (DO NOT FILTER AGAIN)
# -----------------------------
n_trials_2p = len(data2p.event_onset)
n_trials_behavior = len(data2p.bdata['currentFreq'])

if n_trials_2p < n_trials_behavior:
    data2p.bdata['currentFreq'] = data2p.bdata['currentFreq'][:n_trials_2p]
elif n_trials_2p > n_trials_behavior:
    data2p.event_onset = data2p.event_onset[:n_trials_behavior]

eventlocked, tvec, valid_events = data2p.event_locked_average(
    time_range=time_range, dff=True
)

n_cells, n_trials, _ = eventlocked.shape

# -----------------------------
# LOAD + ALIGN RED CELL LABELS
# -----------------------------
iscell_full  = np.load(os.path.join(SUITE2P_DIR, 'iscell.npy'))
redcell_full = np.load(os.path.join(SUITE2P_DIR, 'redcell.npy'))[:,0].astype(bool)

iscell_data = data2p.iscell

inds = []
for row in iscell_data:
    matches = np.where(
        (iscell_full[:,0] == row[0]) &
        (np.isclose(iscell_full[:,1], row[1]))
    )[0]
    if len(matches) == 0:
        raise ValueError("Could not match a cell between data2p and Suite2p")
    inds.append(matches[0])

inds = np.array(inds)
redcell = redcell_full[inds]

assert len(redcell) == n_cells, "Alignment failed"

green_not_red = ~redcell
green_and_red = redcell

print(f"Total cells: {n_cells}")
print(f"Green only: {green_not_red.sum()}")
print(f"Green + red: {green_and_red.sum()}")

# -----------------------------
# AM STRUCTURE
# -----------------------------
current_am = data2p.bdata['currentFreq'][valid_events]
possible_am = np.unique(current_am)
n_am = len(possible_am)

trials_each_am = behavioranalysis.find_trials_each_type(current_am, possible_am)

# -----------------------------
# COMPUTE TUNING CURVES
# -----------------------------
tuning_curves = np.zeros((n_cells, n_am))

bwin = baseline_win(tvec)
rwin = response_win(tvec)

for k in range(n_am):
    trials = trials_each_am[:, k]

    if trials.sum() < min_trials:
        tuning_curves[:, k] = np.nan
        continue

    data_f = eventlocked[:, trials, :]

    baseline = np.nanmean(data_f[:, :, bwin], axis=(1,2))
    response = np.nanmean(data_f[:, :, rwin], axis=(1,2))

    tuning_curves[:, k] = response - baseline

# -----------------------------
# SPLIT CELLS
# -----------------------------
idx_green_not_red = np.where(green_not_red)[0]
idx_green_and_red = np.where(green_and_red)[0]

tuning_gnr = tuning_curves[idx_green_not_red]
tuning_gr  = tuning_curves[idx_green_and_red]

def sort_and_normalize(tuning):
    if tuning.shape[0] == 0:
        return tuning

    best_idx = np.nanargmax(tuning, axis=1)
    best_am = possible_am[best_idx]

    sort_idx = np.argsort(best_am)

    tuning_sorted = tuning[sort_idx]
    tuning_norm = tuning_sorted / np.nanmax(tuning_sorted, axis=1, keepdims=True)

    return tuning_norm

tuning_gnr_norm = sort_and_normalize(tuning_gnr)
tuning_gr_norm  = sort_and_normalize(tuning_gr)

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 8), constrained_layout=True)

# LEFT: green only
if tuning_gnr_norm.shape[0] > 0:
    im0 = ax[0].imshow(tuning_gnr_norm, aspect='auto', cmap='viridis')
    ax[0].set_title("Green only (not red)")
else:
    im0 = None
    ax[0].set_title("Green only (none)")

# RIGHT: tdTomato+
if tuning_gr_norm.shape[0] > 0:
    im1 = ax[1].imshow(tuning_gr_norm, aspect='auto', cmap='viridis')
    ax[1].set_title("tdTomato+ (yellow cells)")
else:
    im1 = None
    ax[1].set_title("tdTomato+ (none)")

# X axis (AM rate)
for a in ax:
    a.set_xticks(np.arange(n_am))
    a.set_xticklabels([f"{am:.0f}" for am in possible_am], rotation=45)
    a.set_xlabel("AM rate (Hz)")
    a.set_ylabel("Neurons (sorted by best AM)")

# integer y ticks on right
if tuning_gr_norm.shape[0] > 0:
    step = max(1, tuning_gr_norm.shape[0] // 10)
    yticks = np.arange(0, tuning_gr_norm.shape[0], step)
    ax[1].set_yticks(yticks)
    ax[1].set_yticklabels([str(int(y)) for y in yticks])

# colorbar
im_for_cbar = im0 if im0 is not None else im1
if im_for_cbar is not None:
    cbar = fig.colorbar(im_for_cbar, ax=ax)
    cbar.set_label('Normalized response')

plt.show()

# -----------------------------
# SAVE (CONDITIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_AM_raster_red_split.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[34]:


# ============================================================
# MEAN IMAGES WITH ROI OVERLAYS
# LEFT: green mean + red ROIs
# RIGHT: red mean + green ROIs
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# LOAD SUITE2P DATA
# -----------------------------
ops  = np.load(os.path.join(SUITE2P_DIR, 'ops.npy'), allow_pickle=True).item()
stat = np.load(os.path.join(SUITE2P_DIR, 'stat.npy'), allow_pickle=True)

mean_green = ops['meanImg']
mean_red   = ops['meanImg_chan2']

# -----------------------------
# EXTRACT ROI CENTROIDS (Suite2p space)
# -----------------------------
yc = np.array([s['med'][0] for s in stat])
xc = np.array([s['med'][1] for s in stat])

# -----------------------------
# USE YOUR EXISTING ALIGNMENT
# inds maps data2p → Suite2p
# redcell already aligned to data2p
# -----------------------------
yc_data = yc[inds]
xc_data = xc[inds]

# split
yc_red   = yc_data[green_and_red]
xc_red   = xc_data[green_and_red]

yc_green = yc_data[green_not_red]
xc_green = xc_data[green_not_red]

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

# LEFT: green mean + red ROIs
ax[0].imshow(mean_green, cmap='gray')
ax[0].scatter(
    xc_red, yc_red,
    facecolors='none',
    edgecolors='red',
    s=40,
    linewidths=1.5
)
ax[0].set_title("Green mean image + red ROIs")
ax[0].axis('off')

# RIGHT: red mean + green ROIs
ax[1].imshow(mean_red, cmap='gray')
ax[1].scatter(
    xc_green, yc_green,
    facecolors='none',
    edgecolors='lime',
    s=40,
    linewidths=1.5
)
ax[1].set_title("Red mean image + green ROIs")
ax[1].axis('off')

plt.show()

# In[35]:


# ============================================================
# MEAN IMAGES WITH ROI OVERLAYS + LABELS FOR RED CELLS
# LEFT: green mean + red (numbered) + green ROIs
# RIGHT: red mean + green ROIs
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# LOAD SUITE2P DATA
# -----------------------------
ops  = np.load(os.path.join(SUITE2P_DIR, 'ops.npy'), allow_pickle=True).item()
stat = np.load(os.path.join(SUITE2P_DIR, 'stat.npy'), allow_pickle=True)

mean_green = ops['meanImg']
mean_red   = ops.get('meanImg_chan2', None)

# -----------------------------
# EXTRACT ROI CENTROIDS (Suite2p space)
# -----------------------------
yc = np.array([s['med'][0] for s in stat])
xc = np.array([s['med'][1] for s in stat])

# -----------------------------
# ALIGN TO data2p (uses inds from previous cell)
# -----------------------------
yc_data = yc[inds]
xc_data = xc[inds]

# split
yc_red   = yc_data[green_and_red]
xc_red   = xc_data[green_and_red]

yc_green = yc_data[green_not_red]
xc_green = xc_data[green_not_red]

print(f"Red cells: {len(xc_red)} | Green-only cells: {len(xc_green)}")

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

# LEFT: green mean + BOTH ROI types
ax[0].imshow(mean_green, cmap='gray')

# green-only ROIs (green hollow)
ax[0].scatter(
    xc_green, yc_green,
    facecolors='none',
    edgecolors='lime',
    s=50,
    linewidths=1.2
)

# red ROIs (red hollow)
ax[0].scatter(
    xc_red, yc_red,
    facecolors='none',
    edgecolors='red',
    s=70,
    linewidths=1.6
)

# label red cells
for i, (x, y) in enumerate(zip(xc_red, yc_red), start=1):
    ax[0].text(
        x + 2, y + 2, str(i),
        color='red',
        fontsize=10,
        weight='bold'
    )

ax[0].set_title("Green mean image + green (lime) & red (numbered) ROIs")
ax[0].axis('off')

# RIGHT: red mean + green-only ROIs
if mean_red is not None:
    ax[1].imshow(mean_red, cmap='gray')
    ax[1].scatter(
        xc_green, yc_green,
        facecolors='none',
        edgecolors='lime',
        s=50,
        linewidths=1.2
    )
    ax[1].set_title("Red mean image + green ROIs")
else:
    ax[1].text(0.5, 0.5, "No red channel image", ha='center', va='center')
    ax[1].set_title("Red channel unavailable")

ax[1].axis('off')

plt.show()

# In[36]:


# ============================================================
# MEAN IMAGES WITH ROI OVERLAYS + LABELS FOR RED CELLS
# LEFT: green mean + red (numbered) + green ROIs
# RIGHT: red mean + green ROIs
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# LOAD SUITE2P DATA
# -----------------------------
ops  = np.load(os.path.join(SUITE2P_DIR, 'ops.npy'), allow_pickle=True).item()
stat = np.load(os.path.join(SUITE2P_DIR, 'stat.npy'), allow_pickle=True)

mean_green = ops['meanImg']
mean_red   = ops.get('meanImg_chan2', None)

# -----------------------------
# EXTRACT ROI CENTROIDS
# -----------------------------
yc = np.array([s['med'][0] for s in stat])
xc = np.array([s['med'][1] for s in stat])

# -----------------------------
# ALIGN TO data2p (using inds)
# -----------------------------
yc_data = yc[inds]
xc_data = xc[inds]

yc_red   = yc_data[green_and_red]
xc_red   = xc_data[green_and_red]

yc_green = yc_data[green_not_red]
xc_green = xc_data[green_not_red]

print(f"Red cells: {len(xc_red)} | Green-only cells: {len(xc_green)}")

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

# LEFT: green mean + BOTH ROI types
ax[0].imshow(mean_green, cmap='gray')

# Green-only ROIs (slightly larger so they remain visible)
ax[0].scatter(
    xc_green, yc_green,
    facecolors='none',
    edgecolors='lime',
    s=70,                # larger than red
    linewidths=1.2
)

# Red ROIs
ax[0].scatter(
    xc_red, yc_red,
    facecolors='none',
    edgecolors='red',
    s=50,                # slightly smaller
    linewidths=1.6
)

# Labels for red cells (offset more up-right)
for i, (x, y) in enumerate(zip(xc_red, yc_red), start=1):
    ax[0].text(
        x + 4, y + 4, str(i),   # increased offset
        color='red',
        fontsize=10,
        weight='bold'
    )

ax[0].set_title("Green mean image + green (lime) & red (numbered) ROIs")
ax[0].axis('off')

# RIGHT: red mean + green-only ROIs
if mean_red is not None:
    ax[1].imshow(mean_red, cmap='gray')
    ax[1].scatter(
        xc_green, yc_green,
        facecolors='none',
        edgecolors='lime',
        s=70,
        linewidths=1.2
    )
    ax[1].set_title("Red mean image + green ROIs")
else:
    ax[1].text(0.5, 0.5, "No red channel image", ha='center', va='center')
    ax[1].set_title("Red channel unavailable")

ax[1].axis('off')

plt.show()

# In[37]:


# ============================================================
# RED MEAN IMAGE + RED ROIs (HOLLOW RED CIRCLES)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# LOAD SUITE2P DATA
# -----------------------------
ops  = np.load(os.path.join(SUITE2P_DIR, 'ops.npy'), allow_pickle=True).item()
stat = np.load(os.path.join(SUITE2P_DIR, 'stat.npy'), allow_pickle=True)

mean_red = ops.get('meanImg_chan2', None)
if mean_red is None:
    raise ValueError("No red channel mean image (meanImg_chan2) found.")

# -----------------------------
# EXTRACT ROI CENTROIDS
# -----------------------------
yc = np.array([s['med'][0] for s in stat])
xc = np.array([s['med'][1] for s in stat])

# -----------------------------
# ALIGN TO data2p
# -----------------------------
yc_data = yc[inds]
xc_data = xc[inds]

# red cells only
yc_red = yc_data[green_and_red]
xc_red = xc_data[green_and_red]

print(f"Number of red cells: {len(xc_red)}")

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)

ax.imshow(mean_red, cmap='gray')

ax.scatter(
    xc_red, yc_red,
    facecolors='none',
    edgecolors='red',
    s=70,
    linewidths=1.5
)

ax.set_title("Red mean image with red ROIs")
ax.axis('off')

plt.show()

# In[38]:


# ============================================================
# RED MEAN IMAGE + RED ROIs (BRIGHTENED)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# LOAD DATA
# -----------------------------
ops  = np.load(os.path.join(SUITE2P_DIR, 'ops.npy'), allow_pickle=True).item()
stat = np.load(os.path.join(SUITE2P_DIR, 'stat.npy'), allow_pickle=True)

mean_red = ops.get('meanImg_chan2', None)
if mean_red is None:
    raise ValueError("No red channel mean image found.")

# -----------------------------
# BRIGHTEN IMAGE (PERCENTILE SCALING)
# -----------------------------
vmin, vmax = np.percentile(mean_red, [1, 99])

# -----------------------------
# ROI CENTROIDS
# -----------------------------
yc = np.array([s['med'][0] for s in stat])
xc = np.array([s['med'][1] for s in stat])

yc_data = yc[inds]
xc_data = xc[inds]

yc_red = yc_data[green_and_red]
xc_red = xc_data[green_and_red]

print(f"Number of red cells: {len(xc_red)}")

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)

ax.imshow(mean_red, cmap='gray', vmin=vmin, vmax=vmax)

ax.scatter(
    xc_red, yc_red,
    facecolors='none',
    edgecolors='red',
    s=70,
    linewidths=1.5
)

ax.set_title("Brightened red mean image with red ROIs")
ax.axis('off')

plt.show()

# In[40]:


# ============================================================
# RED MEAN IMAGE + ALL ROIs
# yellow = overlap (distance-based)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# LOAD DATA
# -----------------------------
ops  = np.load(os.path.join(SUITE2P_DIR, 'ops.npy'), allow_pickle=True).item()
stat = np.load(os.path.join(SUITE2P_DIR, 'stat.npy'), allow_pickle=True)

mean_red = ops.get('meanImg_chan2', None)
if mean_red is None:
    raise ValueError("No red channel mean image found.")

# -----------------------------
# BRIGHTEN IMAGE
# -----------------------------
vmin, vmax = np.percentile(mean_red, [1, 99])

# -----------------------------
# ROI CENTROIDS
# -----------------------------
yc = np.array([s['med'][0] for s in stat])
xc = np.array([s['med'][1] for s in stat])

yc_data = yc[inds]
xc_data = xc[inds]

# split populations
yc_red   = yc_data[green_and_red]
xc_red   = xc_data[green_and_red]

yc_green = yc_data[green_not_red]
xc_green = xc_data[green_not_red]

# -----------------------------
# FIND OVERLAPS (distance-based)
# -----------------------------
overlap_thresh = 3  # pixels

overlap_idx_red = []
overlap_idx_green = []

for i, (xr, yr) in enumerate(zip(xc_red, yc_red)):
    if len(xc_green) == 0:
        break
    dists = np.sqrt((xc_green - xr)**2 + (yc_green - yr)**2)
    close = np.where(dists < overlap_thresh)[0]
    if len(close) > 0:
        overlap_idx_red.append(i)
        overlap_idx_green.extend(close)

# FORCE integer dtype (fixes your error)
overlap_idx_red   = np.array(overlap_idx_red, dtype=int)
overlap_idx_green = np.array(overlap_idx_green, dtype=int)

# masks
red_overlap_mask   = np.zeros(len(xc_red), dtype=bool)
green_overlap_mask = np.zeros(len(xc_green), dtype=bool)

if overlap_idx_red.size > 0:
    red_overlap_mask[overlap_idx_red] = True

if overlap_idx_green.size > 0:
    green_overlap_mask[overlap_idx_green] = True

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)

ax.imshow(mean_red, cmap='gray', vmin=vmin, vmax=vmax)

# green-only (non-overlap)
ax.scatter(
    xc_green[~green_overlap_mask],
    yc_green[~green_overlap_mask],
    facecolors='none',
    edgecolors='lime',
    s=70,
    linewidths=1.2
)

# red-only (non-overlap)
ax.scatter(
    xc_red[~red_overlap_mask],
    yc_red[~red_overlap_mask],
    facecolors='none',
    edgecolors='red',
    s=60,
    linewidths=1.5
)

# overlap → yellow
ax.scatter(
    xc_red[red_overlap_mask],
    yc_red[red_overlap_mask],
    facecolors='none',
    edgecolors='yellow',
    s=75,
    linewidths=2
)

ax.scatter(
    xc_green[green_overlap_mask],
    yc_green[green_overlap_mask],
    facecolors='none',
    edgecolors='yellow',
    s=75,
    linewidths=2
)

ax.set_title("Red mean image with ROIs (yellow = overlap)")
ax.axis('off')

plt.show()

# In[41]:


# ============================================================
# LEFT: red mean image + ROIs
# RIGHT: green mean image + SAME ROIs
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# LOAD DATA
# -----------------------------
ops  = np.load(os.path.join(SUITE2P_DIR, 'ops.npy'), allow_pickle=True).item()
stat = np.load(os.path.join(SUITE2P_DIR, 'stat.npy'), allow_pickle=True)

mean_red   = ops.get('meanImg_chan2', None)
mean_green = ops.get('meanImg', None)

if mean_red is None:
    raise ValueError("No red mean image found.")
if mean_green is None:
    raise ValueError("No green mean image found.")

# -----------------------------
# BRIGHTEN BOTH IMAGES
# -----------------------------
vmin_r, vmax_r = np.percentile(mean_red,   [1, 99])
vmin_g, vmax_g = np.percentile(mean_green, [1, 99])

# -----------------------------
# ROI CENTROIDS
# -----------------------------
yc = np.array([s['med'][0] for s in stat])
xc = np.array([s['med'][1] for s in stat])

yc_data = yc[inds]
xc_data = xc[inds]

# split
yc_red   = yc_data[green_and_red]
xc_red   = xc_data[green_and_red]

yc_green = yc_data[green_not_red]
xc_green = xc_data[green_not_red]

# -----------------------------
# OVERLAP (distance-based)
# -----------------------------
overlap_thresh = 3

overlap_idx_red = []
overlap_idx_green = []

for i, (xr, yr) in enumerate(zip(xc_red, yc_red)):
    if len(xc_green) == 0:
        break
    dists = np.sqrt((xc_green - xr)**2 + (yc_green - yr)**2)
    close = np.where(dists < overlap_thresh)[0]
    if len(close) > 0:
        overlap_idx_red.append(i)
        overlap_idx_green.extend(close)

overlap_idx_red   = np.array(overlap_idx_red, dtype=int)
overlap_idx_green = np.array(overlap_idx_green, dtype=int)

red_overlap_mask   = np.zeros(len(xc_red), dtype=bool)
green_overlap_mask = np.zeros(len(xc_green), dtype=bool)

if overlap_idx_red.size > 0:
    red_overlap_mask[overlap_idx_red] = True
if overlap_idx_green.size > 0:
    green_overlap_mask[overlap_idx_green] = True

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

# LEFT: red mean
ax[0].imshow(mean_red, cmap='gray', vmin=vmin_r, vmax=vmax_r)

# RIGHT: green mean
ax[1].imshow(mean_green, cmap='gray', vmin=vmin_g, vmax=vmax_g)

for a in ax:
    # green-only
    a.scatter(
        xc_green[~green_overlap_mask],
        yc_green[~green_overlap_mask],
        facecolors='none',
        edgecolors='lime',
        s=70,
        linewidths=1.2
    )

    # red-only
    a.scatter(
        xc_red[~red_overlap_mask],
        yc_red[~red_overlap_mask],
        facecolors='none',
        edgecolors='red',
        s=60,
        linewidths=1.5
    )

    # overlap → yellow
    a.scatter(
        xc_red[red_overlap_mask],
        yc_red[red_overlap_mask],
        facecolors='none',
        edgecolors='yellow',
        s=75,
        linewidths=2
    )

    a.scatter(
        xc_green[green_overlap_mask],
        yc_green[green_overlap_mask],
        facecolors='none',
        edgecolors='yellow',
        s=75,
        linewidths=2
    )

    a.axis('off')

ax[0].set_title("Red mean image + ROIs")
ax[1].set_title("Green mean image + ROIs")

plt.show()

# In[42]:


# ============================================================
# LEFT: red mean image + ROIs
# RIGHT: green mean image + SAME ROIs
# yellow = green cells that contain red (tdTomato+)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# LOAD DATA
# -----------------------------
ops  = np.load(os.path.join(SUITE2P_DIR, 'ops.npy'), allow_pickle=True).item()
stat = np.load(os.path.join(SUITE2P_DIR, 'stat.npy'), allow_pickle=True)

mean_red   = ops.get('meanImg_chan2', None)
mean_green = ops.get('meanImg', None)

if mean_red is None:
    raise ValueError("No red mean image found.")
if mean_green is None:
    raise ValueError("No green mean image found.")

# -----------------------------
# BRIGHTEN IMAGES
# -----------------------------
vmin_r, vmax_r = np.percentile(mean_red,   [1, 99])
vmin_g, vmax_g = np.percentile(mean_green, [1, 99])

# -----------------------------
# ROI CENTROIDS
# -----------------------------
yc = np.array([s['med'][0] for s in stat])
xc = np.array([s['med'][1] for s in stat])

yc_data = yc[inds]
xc_data = xc[inds]

# split populations
yc_red   = yc_data[green_and_red]   # tdTomato+
xc_red   = xc_data[green_and_red]

yc_green = yc_data[green_not_red]   # green-only
xc_green = xc_data[green_not_red]

print(f"Green-only: {len(xc_green)} | Green+Red: {len(xc_red)}")

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

# LEFT: red mean
ax[0].imshow(mean_red, cmap='gray', vmin=vmin_r, vmax=vmax_r)

# RIGHT: green mean
ax[1].imshow(mean_green, cmap='gray', vmin=vmin_g, vmax=vmax_g)

for a in ax:
    # green-only
    a.scatter(
        xc_green, yc_green,
        facecolors='none',
        edgecolors='lime',
        s=70,
        linewidths=1.2
    )

    # tdTomato+ (green + red)
    a.scatter(
        xc_red, yc_red,
        facecolors='none',
        edgecolors='yellow',
        s=70,
        linewidths=2
    )

    a.axis('off')

ax[0].set_title("Red mean image (yellow = tdTomato+)")
ax[1].set_title("Green mean image (yellow = tdTomato+)")

plt.show()

# In[11]:


# ============================================================
# LEFT: preferred AM rate (color)
# RIGHT: dF/F skewness (color)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import skew

# -----------------------------
# LOAD DATA
# -----------------------------
ops  = np.load(os.path.join(SUITE2P_DIR, 'ops.npy'), allow_pickle=True).item()
stat = np.load(os.path.join(SUITE2P_DIR, 'stat.npy'), allow_pickle=True)

mean_red   = ops.get('meanImg_chan2', None)
mean_green = ops.get('meanImg', None)

# -----------------------------
# BRIGHTEN
# -----------------------------
vmin_r, vmax_r = np.percentile(mean_red,   [1, 99])
vmin_g, vmax_g = np.percentile(mean_green, [1, 99])

# -----------------------------
# ROI CENTROIDS
# -----------------------------
yc = np.array([s['med'][0] for s in stat])
xc = np.array([s['med'][1] for s in stat])

yc_data = yc[inds]
xc_data = xc[inds]

# -----------------------------
# AM TUNING
# -----------------------------
current_am = data2p.bdata['currentFreq']

eventlocked, tvec, valid_events = data2p.event_locked_average(
    time_range=[-1,1], dff=True
)

current_am = current_am[valid_events]
possible_am = np.unique(current_am)

trials_each_am = behavioranalysis.find_trials_each_type(current_am, possible_am)

n_cells = eventlocked.shape[0]
n_am = len(possible_am)

tuning_curves = np.zeros((n_cells, n_am))

for k in range(n_am):
    trials = trials_each_am[:, k]
    tuning_curves[:, k] = np.nanmean(eventlocked[:, trials, :], axis=(1,2))

best_idx = np.nanargmax(tuning_curves, axis=1)
pref_am = possible_am[best_idx]

# -----------------------------
# SKEWNESS
# -----------------------------
dff_flat = eventlocked.reshape(n_cells, -1)
skewness = skew(dff_flat, axis=1, nan_policy='omit')
skew_clipped = np.clip(skewness, -2, 2)

# -----------------------------
# EDGE COLORS (FIXED)
# -----------------------------
edgecolors = ['yellow' if r else 'lime' for r in green_and_red]
linewidths = [2 if r else 1.2 for r in green_and_red]

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

# LEFT: preferred AM
ax[0].imshow(mean_red, cmap='gray', vmin=vmin_r, vmax=vmax_r)

sc0 = ax[0].scatter(
    xc_data, yc_data,
    c=pref_am,
    cmap='plasma',
    s=70,
    edgecolors=edgecolors,
    linewidths=linewidths
)

ax[0].set_title("Preferred AM rate")
ax[0].axis('off')

# RIGHT: skewness
ax[1].imshow(mean_green, cmap='gray', vmin=vmin_g, vmax=vmax_g)

sc1 = ax[1].scatter(
    xc_data, yc_data,
    c=skew_clipped,
    cmap='coolwarm',
    vmin=-2, vmax=2,
    s=70,
    edgecolors=edgecolors,
    linewidths=linewidths
)

ax[1].set_title("dF/F skewness")
ax[1].axis('off')

# -----------------------------
# COLORBARS
# -----------------------------
cbar0 = fig.colorbar(sc0, ax=ax[0])
cbar0.set_label("Preferred AM rate (Hz)")

cbar1 = fig.colorbar(sc1, ax=ax[1])
cbar1.set_label("Skewness (clipped ±2)")

plt.show()

# In[12]:


# ============================================================
# LEFT: preferred AM rate (color)
# RIGHT: dF/F skewness (color)
# SAVES OUTPUT
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import skew

# -----------------------------
# LOAD DATA
# -----------------------------
ops  = np.load(os.path.join(SUITE2P_DIR, 'ops.npy'), allow_pickle=True).item()
stat = np.load(os.path.join(SUITE2P_DIR, 'stat.npy'), allow_pickle=True)

mean_red   = ops.get('meanImg_chan2', None)
mean_green = ops.get('meanImg', None)

# -----------------------------
# BRIGHTEN
# -----------------------------
vmin_r, vmax_r = np.percentile(mean_red,   [1, 99])
vmin_g, vmax_g = np.percentile(mean_green, [1, 99])

# -----------------------------
# ROI CENTROIDS
# -----------------------------
yc = np.array([s['med'][0] for s in stat])
xc = np.array([s['med'][1] for s in stat])

yc_data = yc[inds]
xc_data = xc[inds]

# -----------------------------
# AM TUNING
# -----------------------------
current_am = data2p.bdata['currentFreq']

eventlocked, tvec, valid_events = data2p.event_locked_average(
    time_range=[-1,1], dff=True
)

current_am = current_am[valid_events]
possible_am = np.unique(current_am)

trials_each_am = behavioranalysis.find_trials_each_type(current_am, possible_am)

n_cells = eventlocked.shape[0]
n_am = len(possible_am)

tuning_curves = np.zeros((n_cells, n_am))

for k in range(n_am):
    trials = trials_each_am[:, k]
    tuning_curves[:, k] = np.nanmean(eventlocked[:, trials, :], axis=(1,2))

best_idx = np.nanargmax(tuning_curves, axis=1)
pref_am = possible_am[best_idx]

# -----------------------------
# SKEWNESS
# -----------------------------
dff_flat = eventlocked.reshape(n_cells, -1)
skewness = skew(dff_flat, axis=1, nan_policy='omit')
skew_clipped = np.clip(skewness, -2, 2)

# -----------------------------
# EDGE COLORS
# -----------------------------
edgecolors = ['yellow' if r else 'lime' for r in green_and_red]
linewidths = [2 if r else 1.2 for r in green_and_red]

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

# LEFT: preferred AM
ax[0].imshow(mean_red, cmap='gray', vmin=vmin_r, vmax=vmax_r)

sc0 = ax[0].scatter(
    xc_data, yc_data,
    c=pref_am,
    cmap='plasma',
    s=70,
    edgecolors=edgecolors,
    linewidths=linewidths
)

ax[0].set_title("Preferred AM rate")
ax[0].axis('off')

# RIGHT: skewness
ax[1].imshow(mean_green, cmap='gray', vmin=vmin_g, vmax=vmax_g)

sc1 = ax[1].scatter(
    xc_data, yc_data,
    c=skew_clipped,
    cmap='coolwarm',
    vmin=-2, vmax=2,
    s=70,
    edgecolors=edgecolors,
    linewidths=linewidths
)

ax[1].set_title("dF/F skewness")
ax[1].axis('off')

# -----------------------------
# COLORBARS
# -----------------------------
cbar0 = fig.colorbar(sc0, ax=ax[0])
cbar0.set_label("Preferred AM rate (Hz)")

cbar1 = fig.colorbar(sc1, ax=ax[1])
cbar1.set_label("Skewness (clipped ±2)")

plt.show()

# -----------------------------
# SAVE (OPTIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_AM_spatial_maps.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[14]:


# ============================================================
# LEFT: preferred AM rate (color)
# RIGHT: dF/F skewness (color)
# SAVES COMPRESSED OUTPUT (~30% smaller)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import skew

# -----------------------------
# LOAD DATA
# -----------------------------
ops  = np.load(os.path.join(SUITE2P_DIR, 'ops.npy'), allow_pickle=True).item()
stat = np.load(os.path.join(SUITE2P_DIR, 'stat.npy'), allow_pickle=True)

mean_red   = ops.get('meanImg_chan2', None)
mean_green = ops.get('meanImg', None)

# -----------------------------
# BRIGHTEN
# -----------------------------
vmin_r, vmax_r = np.percentile(mean_red,   [1, 99])
vmin_g, vmax_g = np.percentile(mean_green, [1, 99])

# -----------------------------
# ROI CENTROIDS
# -----------------------------
yc = np.array([s['med'][0] for s in stat])
xc = np.array([s['med'][1] for s in stat])

yc_data = yc[inds]
xc_data = xc[inds]

# -----------------------------
# AM TUNING
# -----------------------------
current_am = data2p.bdata['currentFreq']

eventlocked, tvec, valid_events = data2p.event_locked_average(
    time_range=[-1,1], dff=True
)

current_am = current_am[valid_events]
possible_am = np.unique(current_am)

trials_each_am = behavioranalysis.find_trials_each_type(current_am, possible_am)

n_cells = eventlocked.shape[0]
n_am = len(possible_am)

tuning_curves = np.zeros((n_cells, n_am))

for k in range(n_am):
    trials = trials_each_am[:, k]
    tuning_curves[:, k] = np.nanmean(eventlocked[:, trials, :], axis=(1,2))

best_idx = np.nanargmax(tuning_curves, axis=1)
pref_am = possible_am[best_idx]

# -----------------------------
# SKEWNESS
# -----------------------------
dff_flat = eventlocked.reshape(n_cells, -1)
skewness = skew(dff_flat, axis=1, nan_policy='omit')
skew_clipped = np.clip(skewness, -2, 2)

# -----------------------------
# EDGE COLORS
# -----------------------------
edgecolors = ['yellow' if r else 'lime' for r in green_and_red]
linewidths = [2 if r else 1.2 for r in green_and_red]

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

# LEFT: preferred AM
ax[0].imshow(mean_red, cmap='gray', vmin=vmin_r, vmax=vmax_r)

sc0 = ax[0].scatter(
    xc_data, yc_data,
    c=pref_am,
    cmap='plasma',
    s=70,
    edgecolors=edgecolors,
    linewidths=linewidths
)

ax[0].set_title("Preferred AM rate")
ax[0].axis('off')

# RIGHT: skewness
ax[1].imshow(mean_green, cmap='gray', vmin=vmin_g, vmax=vmax_g)

sc1 = ax[1].scatter(
    xc_data, yc_data,
    c=skew_clipped,
    cmap='coolwarm',
    vmin=-2, vmax=2,
    s=70,
    edgecolors=edgecolors,
    linewidths=linewidths
)

ax[1].set_title("dF/F skewness")
ax[1].axis('off')

# -----------------------------
# COLORBARS
# -----------------------------
cbar0 = fig.colorbar(sc0, ax=ax[0])
cbar0.set_label("Preferred AM rate (Hz)")

cbar1 = fig.colorbar(sc1, ax=ax[1])
cbar1.set_label("Skewness (clipped ±2)")

plt.show()

# -----------------------------
# SAVE (OPTIONAL, COMPRESSED)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_AM_spatial_maps_small.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(
        save_path,
        dpi=220,                    # ↓ from 300 → ~30% smaller
        bbox_inches='tight',
        pil_kwargs={"compress_level": 9}  # max PNG compression
    )

    print(f"Saved compressed figure to:\n{save_path}")

# In[15]:


# ============================================================
# LEFT: preferred AM rate (color)
# RIGHT: dF/F skewness (color)
# SAVES HIGHLY COMPRESSED OUTPUT (~50% smaller again)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import skew

# -----------------------------
# LOAD DATA
# -----------------------------
ops  = np.load(os.path.join(SUITE2P_DIR, 'ops.npy'), allow_pickle=True).item()
stat = np.load(os.path.join(SUITE2P_DIR, 'stat.npy'), allow_pickle=True)

mean_red   = ops.get('meanImg_chan2', None)
mean_green = ops.get('meanImg', None)

# -----------------------------
# BRIGHTEN
# -----------------------------
vmin_r, vmax_r = np.percentile(mean_red,   [1, 99])
vmin_g, vmax_g = np.percentile(mean_green, [1, 99])

# -----------------------------
# ROI CENTROIDS
# -----------------------------
yc = np.array([s['med'][0] for s in stat])
xc = np.array([s['med'][1] for s in stat])

yc_data = yc[inds]
xc_data = xc[inds]

# -----------------------------
# AM TUNING
# -----------------------------
current_am = data2p.bdata['currentFreq']

eventlocked, tvec, valid_events = data2p.event_locked_average(
    time_range=[-1,1], dff=True
)

current_am = current_am[valid_events]
possible_am = np.unique(current_am)

trials_each_am = behavioranalysis.find_trials_each_type(current_am, possible_am)

n_cells = eventlocked.shape[0]
n_am = len(possible_am)

tuning_curves = np.zeros((n_cells, n_am))

for k in range(n_am):
    trials = trials_each_am[:, k]
    tuning_curves[:, k] = np.nanmean(eventlocked[:, trials, :], axis=(1,2))

best_idx = np.nanargmax(tuning_curves, axis=1)
pref_am = possible_am[best_idx]

# -----------------------------
# SKEWNESS
# -----------------------------
dff_flat = eventlocked.reshape(n_cells, -1)
skewness = skew(dff_flat, axis=1, nan_policy='omit')
skew_clipped = np.clip(skewness, -2, 2)

# -----------------------------
# EDGE COLORS
# -----------------------------
edgecolors = ['yellow' if r else 'lime' for r in green_and_red]
linewidths = [2 if r else 1.2 for r in green_and_red]

# -----------------------------
# PLOT (slightly smaller figure)
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(10, 5), constrained_layout=True)

# LEFT
ax[0].imshow(mean_red, cmap='gray', vmin=vmin_r, vmax=vmax_r)
sc0 = ax[0].scatter(
    xc_data, yc_data,
    c=pref_am,
    cmap='plasma',
    s=60,  # slightly smaller markers
    edgecolors=edgecolors,
    linewidths=linewidths
)
ax[0].set_title("Preferred AM rate")
ax[0].axis('off')

# RIGHT
ax[1].imshow(mean_green, cmap='gray', vmin=vmin_g, vmax=vmax_g)
sc1 = ax[1].scatter(
    xc_data, yc_data,
    c=skew_clipped,
    cmap='coolwarm',
    vmin=-2, vmax=2,
    s=60,
    edgecolors=edgecolors,
    linewidths=linewidths
)
ax[1].set_title("dF/F skewness")
ax[1].axis('off')

# COLORBARS
cbar0 = fig.colorbar(sc0, ax=ax[0])
cbar0.set_label("Preferred AM rate (Hz)")

cbar1 = fig.colorbar(sc1, ax=ax[1])
cbar1.set_label("Skewness (clipped ±2)")

plt.show()

# -----------------------------
# SAVE (HIGH COMPRESSION)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_AM_spatial_maps_tiny.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(
        save_path,
        dpi=140,  # aggressive reduction
        bbox_inches='tight',
        pil_kwargs={"compress_level": 9}
    )

    print(f"Saved highly compressed figure to:\n{save_path}")

# In[44]:


# ============================================================
# BEST tdTomato+ (YELLOW) CELL (2-PANEL PLOT)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis

# -----------------------------
# PARAMETERS
# -----------------------------
time_range = [-1, 1.5]
baseline_win = lambda t: t < 0
response_win = lambda t: (t > 0) & (t < 0.5)

# -----------------------------
# PREP DATA (DO NOT FILTER AGAIN)
# -----------------------------
n_trials_2p = len(data2p.event_onset)
n_trials_behavior = len(data2p.bdata['currentFreq'])
if n_trials_2p < n_trials_behavior:
    data2p.bdata['currentFreq'] = data2p.bdata['currentFreq'][:n_trials_2p]
elif n_trials_2p > n_trials_behavior:
    data2p.event_onset = data2p.event_onset[:n_trials_behavior]

eventlocked, tvec, valid_events = data2p.event_locked_average(
    time_range=time_range, dff=True
)

n_cells, n_trials, _ = eventlocked.shape

# -----------------------------
# FREQUENCY STRUCTURE
# -----------------------------
current_freq = data2p.bdata['currentFreq'][valid_events]
possible_freq = np.unique(current_freq)
n_freq = len(possible_freq)

trials_each_freq = behavioranalysis.find_trials_each_type(current_freq, possible_freq)

# -----------------------------
# TUNING CURVES
# -----------------------------
tuning_curves = np.zeros((n_cells, n_freq))

bwin = baseline_win(tvec)
rwin = response_win(tvec)

for k in range(n_freq):
    trials = trials_each_freq[:, k]
    data_f = eventlocked[:, trials, :]
    
    baseline = np.nanmean(data_f[:, :, bwin], axis=(1,2))
    response = np.nanmean(data_f[:, :, rwin], axis=(1,2))
    
    tuning_curves[:, k] = response - baseline

# -----------------------------
# SELECT BEST YELLOW CELL
# -----------------------------
idx_yellow = np.where(green_and_red)[0]

if len(idx_yellow) == 0:
    raise ValueError("No tdTomato+ cells found.")

peak_response = np.nanmax(tuning_curves, axis=1)

# pick strongest responder among yellow cells
cell_idx = idx_yellow[np.argmax(peak_response[idx_yellow])]

best_idx = np.argmax(tuning_curves[cell_idx])
best_freq = possible_freq[best_idx]

print(f"Selected yellow cell: {cell_idx}, best freq: {best_freq/1000:.2f} kHz")

# -----------------------------
# PANEL 1: EVENT-LOCKED RASTER
# -----------------------------
cell_data = eventlocked[cell_idx]

sort_trials = np.argsort(current_freq)
cell_data_sorted = cell_data[sort_trials]

# -----------------------------
# PLOT
# -----------------------------
fig, axes = plt.subplots(2, 1, figsize=(6, 8))

# Top panel: raster
im = axes[0].imshow(
    cell_data_sorted,
    aspect='auto',
    extent=[tvec[0], tvec[-1], 0, len(cell_data_sorted)],
    cmap='viridis',
    interpolation='nearest'
)

axes[0].axvline(0, color='red', lw=1)
axes[0].set_ylabel("Trials (sorted by freq)")
axes[0].set_title(f"tdTomato+ cell {cell_idx} response")

cbar = plt.colorbar(im, ax=axes[0])
cbar.set_label("dF/F")

# Bottom panel: tuning
axes[1].plot(possible_freq, tuning_curves[cell_idx], 'o-', lw=2)
axes[1].set_xscale('log')
axes[1].set_xticks(possible_freq)
axes[1].set_xticklabels([f"{f/1000:.1f}" for f in possible_freq])

axes[1].set_xlabel("Frequency (kHz)")
axes[1].set_ylabel("ΔF/F (resp - baseline)")
axes[1].set_title("Frequency tuning")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# -----------------------------
# SAVE (OPTIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_yellow_cell{cell_idx}.png"
    save_path = OUTPUT_DIR / filename
    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[45]:


# ============================================================
# BEST tdTomato+ (YELLOW) CELL (3-PANEL PLOT)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis

# -----------------------------
# PARAMETERS
# -----------------------------
time_range = [-1, 1.5]
baseline_win = lambda t: t < 0
response_win = lambda t: (t > 0) & (t < 0.5)

# -----------------------------
# PREP DATA (DO NOT FILTER AGAIN)
# -----------------------------
n_trials_2p = len(data2p.event_onset)
n_trials_behavior = len(data2p.bdata['currentFreq'])
if n_trials_2p < n_trials_behavior:
    data2p.bdata['currentFreq'] = data2p.bdata['currentFreq'][:n_trials_2p]
elif n_trials_2p > n_trials_behavior:
    data2p.event_onset = data2p.event_onset[:n_trials_behavior]

eventlocked, tvec, valid_events = data2p.event_locked_average(
    time_range=time_range, dff=True
)

n_cells, n_trials, _ = eventlocked.shape

# -----------------------------
# FREQUENCY STRUCTURE
# -----------------------------
current_freq = data2p.bdata['currentFreq'][valid_events]
possible_freq = np.unique(current_freq)
n_freq = len(possible_freq)

trials_each_freq = behavioranalysis.find_trials_each_type(current_freq, possible_freq)

# -----------------------------
# TUNING CURVES
# -----------------------------
tuning_curves = np.zeros((n_cells, n_freq))

bwin = baseline_win(tvec)
rwin = response_win(tvec)

for k in range(n_freq):
    trials = trials_each_freq[:, k]
    data_f = eventlocked[:, trials, :]
    
    baseline = np.nanmean(data_f[:, :, bwin], axis=(1,2))
    response = np.nanmean(data_f[:, :, rwin], axis=(1,2))
    
    tuning_curves[:, k] = response - baseline

# -----------------------------
# SELECT BEST YELLOW CELL
# -----------------------------
idx_yellow = np.where(green_and_red)[0]

if len(idx_yellow) == 0:
    raise ValueError("No tdTomato+ cells found.")

peak_response = np.nanmax(tuning_curves, axis=1)

cell_idx = idx_yellow[np.argmax(peak_response[idx_yellow])]

best_idx = np.argmax(tuning_curves[cell_idx])
best_freq = possible_freq[best_idx]

print(f"Selected yellow cell: {cell_idx}, best freq: {best_freq/1000:.2f} kHz")

# -----------------------------
# PANEL 1: EVENT-LOCKED RASTER
# -----------------------------
cell_data = eventlocked[cell_idx]

sort_trials = np.argsort(current_freq)
cell_data_sorted = cell_data[sort_trials]

# -----------------------------
# PANEL 3: MEAN TRACE @ BEST FREQ
# -----------------------------
best_trials = trials_each_freq[:, best_idx]
data_best = cell_data[best_trials]

mean_trace = np.nanmean(data_best, axis=0)
sem_trace  = np.nanstd(data_best, axis=0) / np.sqrt(data_best.shape[0])

# -----------------------------
# PLOT
# -----------------------------
fig, axes = plt.subplots(3, 1, figsize=(6, 10))

# Top: raster
im = axes[0].imshow(
    cell_data_sorted,
    aspect='auto',
    extent=[tvec[0], tvec[-1], 0, len(cell_data_sorted)],
    cmap='viridis',
    interpolation='nearest'
)

axes[0].axvline(0, color='red', lw=1)
axes[0].set_ylabel("Trials (sorted by freq)")
axes[0].set_title(f"tdTomato+ cell {cell_idx} response")

cbar = plt.colorbar(im, ax=axes[0])
cbar.set_label("dF/F")

# Middle: tuning
axes[1].plot(possible_freq, tuning_curves[cell_idx], 'o-', lw=2)
axes[1].set_xscale('log')
axes[1].set_xticks(possible_freq)
axes[1].set_xticklabels([f"{f/1000:.1f}" for f in possible_freq])

axes[1].set_xlabel("Frequency (kHz)")
axes[1].set_ylabel("ΔF/F")
axes[1].set_title("Frequency tuning")
axes[1].grid(True, alpha=0.3)

# Bottom: mean trace @ best frequency
axes[2].plot(tvec, mean_trace, color='black', lw=2)
axes[2].fill_between(
    tvec,
    mean_trace - sem_trace,
    mean_trace + sem_trace,
    color='gray',
    alpha=0.3
)

axes[2].axvline(0, color='red', linestyle='--')
axes[2].set_xlabel("Time from sound onset (s)")
axes[2].set_ylabel("dF/F")
axes[2].set_title(f"Mean response @ {best_freq/1000:.2f} kHz (± SEM)")

plt.tight_layout()
plt.show()

# -----------------------------
# SAVE (OPTIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_yellow_cell{cell_idx}_3panel.png"
    save_path = OUTPUT_DIR / filename
    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[126]:


# ============================================================
# EXAMPLE LOW-FREQUENCY NEURON (2-PANEL PLOT)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis

# -----------------------------
# PARAMETERS
# -----------------------------
time_range = [-1, 1.5]
baseline_win = lambda t: t < 0
response_win = lambda t: (t > 0) & (t < 0.5)

min_response = 0.03

# -----------------------------
# PREP DATA
# -----------------------------
data2p.filter_cells(prob_threshold=0.5)

n_trials_2p = len(data2p.event_onset)
n_trials_behavior = len(data2p.bdata['currentFreq'])
if n_trials_2p < n_trials_behavior:
    data2p.bdata['currentFreq'] = data2p.bdata['currentFreq'][:n_trials_2p]
elif n_trials_2p > n_trials_behavior:
    data2p.event_onset = data2p.event_onset[:n_trials_behavior]

eventlocked, tvec, valid_events = data2p.event_locked_average(time_range=time_range, dff=True)
eventlocked = eventlocked[:, valid_events, :]

n_cells, n_trials, _ = eventlocked.shape

# -----------------------------
# FREQUENCY STRUCTURE
# -----------------------------
current_freq = data2p.bdata['currentFreq'][valid_events]
possible_freq = np.unique(current_freq)
n_freq = len(possible_freq)

trials_each_freq = behavioranalysis.find_trials_each_type(current_freq, possible_freq)

# -----------------------------
# TUNING CURVES
# -----------------------------
tuning_curves = np.zeros((n_cells, n_freq))

bwin = baseline_win(tvec)
rwin = response_win(tvec)

for k in range(n_freq):
    trials = trials_each_freq[:, k]
    data_f = eventlocked[:, trials, :]
    
    baseline = np.nanmean(data_f[:, :, bwin], axis=(1,2))
    response = np.nanmean(data_f[:, :, rwin], axis=(1,2))
    
    tuning_curves[:, k] = response - baseline

# -----------------------------
# SELECT LOW-FREQ NEURON
# -----------------------------
best_idx = np.argmax(tuning_curves, axis=1)
best_freq = possible_freq[best_idx]

peak_response = np.max(tuning_curves, axis=1)

low_freq_threshold = np.percentile(possible_freq, 30)

candidates = np.where(
    (best_freq <= low_freq_threshold) &
    (peak_response > min_response)
)[0]

if len(candidates) == 0:
    raise ValueError("No good low-frequency neurons found.")

cell_idx = candidates[np.argmax(peak_response[candidates])]
print(f"Selected cell: {cell_idx}, best freq: {best_freq[cell_idx]/1000:.2f} kHz")

# -----------------------------
# PANEL 1: EVENT-LOCKED RASTER
# -----------------------------
cell_data = eventlocked[cell_idx]

sort_trials = np.argsort(current_freq)
cell_data_sorted = cell_data[sort_trials]

# -----------------------------
# PLOT
# -----------------------------
fig, axes = plt.subplots(2, 1, figsize=(6, 8), sharex=False)

# Top panel
im = axes[0].imshow(
    cell_data_sorted,
    aspect='auto',
    extent=[tvec[0], tvec[-1], 0, len(cell_data_sorted)],
    cmap='viridis',
    interpolation='nearest'
)

axes[0].axvline(0, color='red', lw=1)
axes[0].set_ylabel("Trials (sorted by freq)")
axes[0].set_title(f"Cell {cell_idx} event-locked response")

cbar = plt.colorbar(im, ax=axes[0])
cbar.set_label("dF/F")

# Bottom panel
axes[1].plot(possible_freq, tuning_curves[cell_idx], 'o-', lw=2)
axes[1].set_xscale('log')
axes[1].set_xticks(possible_freq)
axes[1].set_xticklabels([f"{f/1000:.1f}" for f in possible_freq])

axes[1].set_xlabel("Frequency (kHz)")
axes[1].set_ylabel("ΔF/F (resp - baseline)")
axes[1].set_title("Frequency tuning")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# -----------------------------
# SAVE (CONDITIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_cell{cell_idx}_example.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[137]:


# ============================================================
# EXAMPLE LOW-FREQUENCY NEURON (FREQ-ALIGNED RASTER + RESPONSE BOX)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis
from matplotlib.patches import Rectangle

# -----------------------------
# PARAMETERS
# -----------------------------
time_range = [-1, 1.5]
baseline_win = lambda t: t < 0
response_win = lambda t: (t > 0) & (t < 0.5)

min_response = 0.03

# -----------------------------
# PREP DATA
# -----------------------------
data2p.filter_cells(prob_threshold=0.5)

n_trials_2p = len(data2p.event_onset)
n_trials_behavior = len(data2p.bdata['currentFreq'])
if n_trials_2p < n_trials_behavior:
    data2p.bdata['currentFreq'] = data2p.bdata['currentFreq'][:n_trials_2p]
elif n_trials_2p > n_trials_behavior:
    data2p.event_onset = data2p.event_onset[:n_trials_behavior]

eventlocked, tvec, valid_events = data2p.event_locked_average(time_range=time_range, dff=True)
eventlocked = eventlocked[:, valid_events, :]

n_cells, n_trials, _ = eventlocked.shape

# -----------------------------
# FREQUENCY STRUCTURE
# -----------------------------
current_freq = data2p.bdata['currentFreq'][valid_events]
possible_freq = np.unique(current_freq)
n_freq = len(possible_freq)

trials_each_freq = behavioranalysis.find_trials_each_type(current_freq, possible_freq)

# -----------------------------
# TUNING CURVES
# -----------------------------
tuning_curves = np.zeros((n_cells, n_freq))

bwin = baseline_win(tvec)
rwin = response_win(tvec)

for k in range(n_freq):
    trials = trials_each_freq[:, k]
    data_f = eventlocked[:, trials, :]
    
    baseline = np.nanmean(data_f[:, :, bwin], axis=(1,2))
    response = np.nanmean(data_f[:, :, rwin], axis=(1,2))
    
    tuning_curves[:, k] = response - baseline

# -----------------------------
# SELECT LOW-FREQ NEURON
# -----------------------------
best_idx = np.argmax(tuning_curves, axis=1)
best_freq = possible_freq[best_idx]

peak_response = np.max(tuning_curves, axis=1)

low_freq_threshold = np.percentile(possible_freq, 30)

candidates = np.where(
    (best_freq <= low_freq_threshold) &
    (peak_response > min_response)
)[0]

if len(candidates) == 0:
    raise ValueError("No good low-frequency neurons found.")

cell_idx = candidates[np.argmax(peak_response[candidates])]
print(f"Selected cell: {cell_idx}, best freq: {best_freq[cell_idx]/1000:.2f} kHz")

# ============================================================
# BUILD FREQUENCY × TIME MATRIX
# ============================================================
cell_data = eventlocked[cell_idx]

freq_response = np.zeros((n_freq, len(tvec)))

for k in range(n_freq):
    trials = trials_each_freq[:, k]
    
    if trials.sum() > 0:
        freq_response[k] = np.nanmean(cell_data[trials], axis=0)
    else:
        freq_response[k] = np.nan

# -----------------------------
# SANITY CHECK
# -----------------------------
resp_win_mask = (tvec > 0) & (tvec < 0.5)

raster_peak_freq = possible_freq[
    np.nanargmax(freq_response[:, resp_win_mask].mean(axis=1))
]

print(f"Raster peak freq: {raster_peak_freq/1000:.2f} kHz")

# -----------------------------
# PLOT
# -----------------------------
fig, axes = plt.subplots(2, 1, figsize=(6, 8), sharex=False)

# ---- Top: frequency raster ----
im = axes[0].imshow(
    freq_response,
    aspect='auto',
    extent=[tvec[0], tvec[-1], 0, n_freq],
    cmap='viridis',
    interpolation='nearest',
    origin='lower'
)

axes[0].axvline(0, color='red', lw=1)

# ---- ADD DASHED RED BOX (response window) ----
resp_start, resp_end = 0, 0.5
rect = Rectangle(
    (resp_start, 0),               # (x, y)
    resp_end - resp_start,         # width
    n_freq,                        # height (all frequencies)
    linewidth=2,
    edgecolor='red',
    facecolor='none',
    linestyle='--'
)
axes[0].add_patch(rect)

# y-axis labels
axes[0].set_yticks(np.arange(n_freq) + 0.5)
axes[0].set_yticklabels([f"{f/1000:.1f}" for f in possible_freq])

axes[0].set_ylabel("Frequency (kHz)")
axes[0].set_title(f"Cell {cell_idx} frequency-resolved response")

cbar = plt.colorbar(im, ax=axes[0])
cbar.set_label("dF/F")

# ---- Bottom: tuning curve ----
axes[1].plot(possible_freq, tuning_curves[cell_idx], 'o-', lw=2)
axes[1].set_xscale('log')
axes[1].set_xticks(possible_freq)
axes[1].set_xticklabels([f"{f/1000:.1f}" for f in possible_freq])

axes[1].set_xlabel("Frequency (kHz)")
axes[1].set_ylabel("ΔF/F (resp - baseline)")
axes[1].set_title("Frequency tuning")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# -----------------------------
# SAVE (CONDITIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_cell{cell_idx}_freq_raster_box.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[138]:


# ============================================================
# EXAMPLE HIGH-FREQUENCY NEURON (2-PANEL PLOT)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis

# -----------------------------
# PARAMETERS
# -----------------------------
time_range = [-1, 1.5]
baseline_win = lambda t: t < 0
response_win = lambda t: (t > 0) & (t < 0.5)

min_response = 0.03

# -----------------------------
# PREP DATA
# -----------------------------
data2p.filter_cells(prob_threshold=0.5)

n_trials_2p = len(data2p.event_onset)
n_trials_behavior = len(data2p.bdata['currentFreq'])
if n_trials_2p < n_trials_behavior:
    data2p.bdata['currentFreq'] = data2p.bdata['currentFreq'][:n_trials_2p]
elif n_trials_2p > n_trials_behavior:
    data2p.event_onset = data2p.event_onset[:n_trials_behavior]

eventlocked, tvec, valid_events = data2p.event_locked_average(time_range=time_range, dff=True)
eventlocked = eventlocked[:, valid_events, :]

n_cells, n_trials, _ = eventlocked.shape

# -----------------------------
# FREQUENCY STRUCTURE
# -----------------------------
current_freq = data2p.bdata['currentFreq'][valid_events]
possible_freq = np.unique(current_freq)
n_freq = len(possible_freq)

trials_each_freq = behavioranalysis.find_trials_each_type(current_freq, possible_freq)

# -----------------------------
# TUNING CURVES
# -----------------------------
tuning_curves = np.zeros((n_cells, n_freq))

bwin = baseline_win(tvec)
rwin = response_win(tvec)

for k in range(n_freq):
    trials = trials_each_freq[:, k]
    data_f = eventlocked[:, trials, :]
    
    baseline = np.nanmean(data_f[:, :, bwin], axis=(1,2))
    response = np.nanmean(data_f[:, :, rwin], axis=(1,2))
    
    tuning_curves[:, k] = response - baseline

# -----------------------------
# SELECT HIGH-FREQ NEURON
# -----------------------------
best_idx = np.argmax(tuning_curves, axis=1)
best_freq = possible_freq[best_idx]

peak_response = np.max(tuning_curves, axis=1)

# define "high frequency" as top 30%
high_freq_threshold = np.percentile(possible_freq, 70)

candidates = np.where(
    (best_freq >= high_freq_threshold) &
    (peak_response > min_response)
)[0]

if len(candidates) == 0:
    raise ValueError("No good high-frequency neurons found.")

# pick strongest
cell_idx = candidates[np.argmax(peak_response[candidates])]
print(f"Selected cell: {cell_idx}, best freq: {best_freq[cell_idx]/1000:.2f} kHz")

# -----------------------------
# PANEL 1: EVENT-LOCKED RASTER
# -----------------------------
cell_data = eventlocked[cell_idx]

sort_trials = np.argsort(current_freq)
cell_data_sorted = cell_data[sort_trials]

# -----------------------------
# PLOT
# -----------------------------
fig, axes = plt.subplots(2, 1, figsize=(6, 8), sharex=False)

# Top panel
im = axes[0].imshow(
    cell_data_sorted,
    aspect='auto',
    extent=[tvec[0], tvec[-1], 0, len(cell_data_sorted)],
    cmap='viridis',
    interpolation='nearest'
)

axes[0].axvline(0, color='red', lw=1)
axes[0].set_ylabel("Trials (sorted by freq)")
axes[0].set_title(f"Cell {cell_idx} event-locked response")

cbar = plt.colorbar(im, ax=axes[0])
cbar.set_label("dF/F")

# Bottom panel
axes[1].plot(possible_freq, tuning_curves[cell_idx], 'o-', lw=2)
axes[1].set_xscale('log')
axes[1].set_xticks(possible_freq)
axes[1].set_xticklabels([f"{f/1000:.1f}" for f in possible_freq])

axes[1].set_xlabel("Frequency (kHz)")
axes[1].set_ylabel("ΔF/F (resp - baseline)")
axes[1].set_title("Frequency tuning")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# -----------------------------
# SAVE (CONDITIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_cell{cell_idx}_highfreq_example.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[142]:


# ============================================================
# RANDOM HIGH-FREQUENCY NEURON (FREQ RASTER + RESPONSE BOX)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis
from matplotlib.patches import Rectangle

# -----------------------------
# PARAMETERS
# -----------------------------
time_range = [-1, 1.5]
baseline_win = lambda t: t < 0
response_win = lambda t: (t > 0) & (t < 0.5)

min_response = 0.03

# -----------------------------
# PREP DATA
# -----------------------------
data2p.filter_cells(prob_threshold=0.5)

n_trials_2p = len(data2p.event_onset)
n_trials_behavior = len(data2p.bdata['currentFreq'])
if n_trials_2p < n_trials_behavior:
    data2p.bdata['currentFreq'] = data2p.bdata['currentFreq'][:n_trials_2p]
elif n_trials_2p > n_trials_behavior:
    data2p.event_onset = data2p.event_onset[:n_trials_behavior]

eventlocked, tvec, valid_events = data2p.event_locked_average(time_range=time_range, dff=True)
eventlocked = eventlocked[:, valid_events, :]

n_cells, n_trials, _ = eventlocked.shape

# -----------------------------
# FREQUENCY STRUCTURE
# -----------------------------
current_freq = data2p.bdata['currentFreq'][valid_events]
possible_freq = np.unique(current_freq)
n_freq = len(possible_freq)

trials_each_freq = behavioranalysis.find_trials_each_type(current_freq, possible_freq)

# -----------------------------
# TUNING CURVES
# -----------------------------
tuning_curves = np.zeros((n_cells, n_freq))

bwin = baseline_win(tvec)
rwin = response_win(tvec)

for k in range(n_freq):
    trials = trials_each_freq[:, k]
    data_f = eventlocked[:, trials, :]
    
    baseline = np.nanmean(data_f[:, :, bwin], axis=(1,2))
    response = np.nanmean(data_f[:, :, rwin], axis=(1,2))
    
    tuning_curves[:, k] = response - baseline

# -----------------------------
# SELECT RANDOM HIGH-FREQ NEURON
# -----------------------------
best_idx = np.argmax(tuning_curves, axis=1)
best_freq = possible_freq[best_idx]

peak_response = np.max(tuning_curves, axis=1)

high_freq_threshold = np.percentile(possible_freq, 70)

candidates = np.where(
    (best_freq >= high_freq_threshold) &
    (peak_response > min_response)
)[0]

if len(candidates) == 0:
    raise ValueError("No good high-frequency neurons found.")

# RANDOM instead of strongest
cell_idx = np.random.choice(candidates)

print(f"Selected cell: {cell_idx}, best freq: {best_freq[cell_idx]/1000:.2f} kHz")

# ============================================================
# BUILD FREQUENCY × TIME MATRIX
# ============================================================
cell_data = eventlocked[cell_idx]

freq_response = np.zeros((n_freq, len(tvec)))

for k in range(n_freq):
    trials = trials_each_freq[:, k]
    
    if trials.sum() > 0:
        freq_response[k] = np.nanmean(cell_data[trials], axis=0)
    else:
        freq_response[k] = np.nan

# -----------------------------
# SANITY CHECK
# -----------------------------
resp_win_mask = (tvec > 0) & (tvec < 0.5)

raster_peak_freq = possible_freq[
    np.nanargmax(freq_response[:, resp_win_mask].mean(axis=1))
]

print(f"Raster peak freq: {raster_peak_freq/1000:.2f} kHz")

# -----------------------------
# PLOT
# -----------------------------
fig, axes = plt.subplots(2, 1, figsize=(6, 8), sharex=False)

# ---- Top: frequency raster ----
im = axes[0].imshow(
    freq_response,
    aspect='auto',
    extent=[tvec[0], tvec[-1], 0, n_freq],
    cmap='viridis',
    interpolation='nearest',
    origin='lower'
)

axes[0].axvline(0, color='red', lw=1)

# ---- RESPONSE WINDOW BOX ----
resp_start, resp_end = 0, 0.5
rect = Rectangle(
    (resp_start, 0),
    resp_end - resp_start,
    n_freq,
    linewidth=2,
    edgecolor='red',
    facecolor='none',
    linestyle='--'
)
axes[0].add_patch(rect)

# y-axis labels
axes[0].set_yticks(np.arange(n_freq) + 0.5)
axes[0].set_yticklabels([f"{f/1000:.1f}" for f in possible_freq])

axes[0].set_ylabel("Frequency (kHz)")
axes[0].set_title(f"Cell {cell_idx} frequency-resolved response")

cbar = plt.colorbar(im, ax=axes[0])
cbar.set_label("dF/F")

# ---- Bottom: tuning curve ----
axes[1].plot(possible_freq, tuning_curves[cell_idx], 'o-', lw=2)
axes[1].set_xscale('log')
axes[1].set_xticks(possible_freq)
axes[1].set_xticklabels([f"{f/1000:.1f}" for f in possible_freq])

axes[1].set_xlabel("Frequency (kHz)")
axes[1].set_ylabel("ΔF/F (resp - baseline)")
axes[1].set_title("Frequency tuning")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# -----------------------------
# SAVE (CONDITIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_cell{cell_idx}_highfreq_random.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[128]:


# ============================================================
# SINGLE CELL: RESPONSES AT 2.4, 4.4, 9.9 kHz + BEST FREQ
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# GET BEST FREQUENCY
# -----------------------------
best_idx = np.argmax(tuning_curves[cell_idx])
best_freq = possible_freq[best_idx]

# -----------------------------
# TARGET FREQUENCIES (Hz)
# -----------------------------
target_freqs = np.array([2400, 4400, 9900, best_freq])

# match to nearest presented frequencies
possible_freq = np.unique(current_freq)
matched_freqs = []

for tf in target_freqs:
    idx = np.argmin(np.abs(possible_freq - tf))
    matched_freqs.append(possible_freq[idx])

# remove duplicates while preserving order
matched_freqs = list(dict.fromkeys(matched_freqs))

# -----------------------------
# EXTRACT CELL DATA
# -----------------------------
cell_data = eventlocked[cell_idx]

# -----------------------------
# PLOT
# -----------------------------
n_plots = len(matched_freqs)
fig, axes = plt.subplots(n_plots, 1, figsize=(6, 2.5*n_plots), sharex=True)

if n_plots == 1:
    axes = [axes]

for ax, freq_val in zip(axes, matched_freqs):
    
    trials = current_freq == freq_val
    data = cell_data[trials]
    
    if data.shape[0] == 0:
        ax.set_title(f"{freq_val/1000:.1f} kHz - no trials")
        continue
    
    mean_trace = np.nanmean(data, axis=0)
    sem_trace = np.nanstd(data, axis=0) / np.sqrt(data.shape[0])
    
    ax.plot(tvec, mean_trace, lw=2)
    ax.fill_between(tvec, mean_trace - sem_trace, mean_trace + sem_trace, alpha=0.3)
    
    ax.axvline(0, color='red', lw=1)
    ax.set_ylabel("dF/F")
    
    label = f"{freq_val/1000:.1f} kHz"
    if np.isclose(freq_val, best_freq):
        label += " (best)"
    
    ax.set_title(f"{label} (n={data.shape[0]} trials)")

axes[-1].set_xlabel("Time from sound onset (s)")

plt.tight_layout()
plt.show()

# -----------------------------
# SAVE (CONDITIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_cell{cell_idx}_freq_traces_with_best.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[129]:


# ============================================================
# TONOTOPIC MAP + CONTOURS + GRADIENT + SCALEBAR + HIGHLIGHT
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# -----------------------------
# PARAMETERS
# -----------------------------
min_response = 0.02
um_per_pix = 1.2
scalebar_um = 100

# -----------------------------
# SELECT RESPONSIVE CELLS
# -----------------------------
peak_response = np.nanmax(tuning_curves, axis=1)
responsive = peak_response > min_response
inds = np.where(responsive)[0]

# -----------------------------
# ROI CENTROIDS
# -----------------------------
xpos = np.array([np.mean(data2p.stat[i]['xpix']) for i in inds])
ypos = np.array([np.mean(data2p.stat[i]['ypix']) for i in inds])

# -----------------------------
# FIT TONOTOPIC PLANE
# -----------------------------
z = np.log10(best_freq[inds])
X = np.column_stack([xpos, ypos, np.ones_like(xpos)])
(a, b, c), *_ = np.linalg.lstsq(X, z, rcond=None)

grad_vec = np.array([a, b])
grad_dir = grad_vec / np.linalg.norm(grad_vec)

# -----------------------------
# LOAD + NORMALIZE IMAGE
# -----------------------------
ops_path = "/data/twophoton/imag025_processed/20260417/000/suite2p/plane0/ops.npy"
ops = np.load(ops_path, allow_pickle=True).item()
mean_img = ops['meanImg']

p2, p98 = np.percentile(mean_img, [2, 98])
mean_img_disp = np.clip((mean_img - p2) / (p98 - p2), 0, 1) ** 0.7

h, w = mean_img.shape

# -----------------------------
# COLOR MAP
# -----------------------------
cmap = mpl.colormaps['viridis']
log_freqs = np.log10(possible_freq)
norm = mpl.colors.Normalize(vmin=log_freqs.min(), vmax=log_freqs.max())

rgb_img = np.stack([mean_img_disp]*3, axis=-1)

# draw all ROIs
for i in inds:
    roi = data2p.stat[i]
    ypix = roi['ypix'].astype(int)
    xpix = roi['xpix'].astype(int)
    color = np.array(cmap(norm(np.log10(best_freq[i])))[:3])
    rgb_img[ypix, xpix, :] = 0.3 * rgb_img[ypix, xpix, :] + 0.7 * color

# -----------------------------
# GRID FOR CONTOURS
# -----------------------------
yy, xx = np.mgrid[0:h, 0:w]
Z = a*xx + b*yy + c
levels_log = np.log10(possible_freq)

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(figsize=(6,6))
ax.imshow(rgb_img)

# contours
cs = ax.contour(xx, yy, Z, levels=levels_log, colors='white', linewidths=1)
fmt = {lvl: f"{(10**lvl)/1000:.1f}" for lvl in levels_log}
ax.clabel(cs, cs.levels, inline=True, fmt=fmt, fontsize=8, colors='red')

# gradient arrow
cx, cy = w/2, h/2
scale = 0.3 * min(h, w)
dx, dy = grad_dir * scale

ax.arrow(cx, cy, dx, dy, color='white', width=2, head_width=10)
ax.text(cx + dx, cy + dy, "High freq", color='red', fontsize=10, fontweight='bold')
ax.text(cx - dx, cy - dy, "Low freq",  color='red', fontsize=10, fontweight='bold')

# -----------------------------
# CORNER LABELS
# -----------------------------
margin = 25
ax.text(margin, margin, "D", color='red', fontsize=14, fontweight='bold')
ax.text(w - margin, margin, "P", color='red', fontsize=14, fontweight='bold', ha='right')
ax.text(w - margin, h - margin, "V", color='red', fontsize=14, fontweight='bold', ha='right', va='bottom')
ax.text(margin, h - margin, "A", color='red', fontsize=14, fontweight='bold', va='bottom')

# -----------------------------
# SCALE BAR
# -----------------------------
L_pix = scalebar_um / um_per_pix
x0 = 40
y0 = h - 110

ax.plot([x0, x0 + L_pix], [y0, y0], color='white', lw=3)
ax.plot([x0, x0], [y0, y0 - L_pix], color='white', lw=3)

ax.text(x0 + L_pix/2, y0 - 10, "100 µm",
        color='white', ha='center', va='top',
        fontsize=11, fontweight='bold')

ax.text(x0 - 12, y0 - L_pix/2, "100 µm",
        color='white', ha='right', va='center',
        fontsize=11, fontweight='bold', rotation=90)

# -----------------------------
# TARGET CELL HIGHLIGHT
# -----------------------------
roi = data2p.stat[cell_idx]
ypix = roi['ypix'].astype(int)
xpix = roi['xpix'].astype(int)

cell_color = np.array(cmap(norm(np.log10(best_freq[cell_idx])))[:3])

ax.plot(xpix, ypix, '.', color='white', markersize=3)
ax.plot(xpix, ypix, '.', color=cell_color, markersize=1.5)

cx_cell = np.mean(xpix)
cy_cell = np.mean(ypix)

ax.plot(cx_cell, cy_cell, 'o',
        markerfacecolor='none',
        markeredgecolor='white',
        markersize=8,
        linewidth=1.5)

ax.text(cx_cell + 5, cy_cell - 5,
        f"Cell {cell_idx}",
        color='white', fontsize=8)

# -----------------------------
# COLORBAR
# -----------------------------
sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
cbar = fig.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Frequency (kHz, log scale)")

tick_vals = np.linspace(log_freqs.min(), log_freqs.max(), 5)
cbar.set_ticks(tick_vals)
cbar.set_ticklabels([f"{10**t/1000:.1f}" for t in tick_vals])

# -----------------------------
# FINAL
# -----------------------------
ax.set_title("Tonotopic map with highlighted cell")
ax.axis('off')

plt.tight_layout()
plt.show()

# -----------------------------
# SAVE (CONDITIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_cell{cell_idx}_tonotopy.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[130]:


# ============================================================
# INTERACTIVE CELL SELECTION + 2-PANEL PLOT
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis

# -----------------------------
# PARAMETERS
# -----------------------------
time_range = [-1, 1.5]
baseline_win = lambda t: t < 0
response_win = lambda t: (t > 0) & (t < 0.5)

min_response = 0.03

# -----------------------------
# PREP DATA
# -----------------------------
data2p.filter_cells(prob_threshold=0.5)

n_trials_2p = len(data2p.event_onset)
n_trials_behavior = len(data2p.bdata['currentFreq'])
if n_trials_2p < n_trials_behavior:
    data2p.bdata['currentFreq'] = data2p.bdata['currentFreq'][:n_trials_2p]
elif n_trials_2p > n_trials_behavior:
    data2p.event_onset = data2p.event_onset[:n_trials_behavior]

eventlocked, tvec, valid_events = data2p.event_locked_average(time_range=time_range, dff=True)
eventlocked = eventlocked[:, valid_events, :]

n_cells, n_trials, _ = eventlocked.shape

# -----------------------------
# FREQUENCY STRUCTURE
# -----------------------------
current_freq = data2p.bdata['currentFreq'][valid_events]
possible_freq = np.unique(current_freq)
n_freq = len(possible_freq)

trials_each_freq = behavioranalysis.find_trials_each_type(current_freq, possible_freq)

# -----------------------------
# TUNING CURVES
# -----------------------------
tuning_curves = np.zeros((n_cells, n_freq))

bwin = baseline_win(tvec)
rwin = response_win(tvec)

for k in range(n_freq):
    trials = trials_each_freq[:, k]
    data_f = eventlocked[:, trials, :]
    
    baseline = np.nanmean(data_f[:, :, bwin], axis=(1,2))
    response = np.nanmean(data_f[:, :, rwin], axis=(1,2))
    
    tuning_curves[:, k] = response - baseline

# -----------------------------
# IDENTIFY RESPONSIVE CELLS
# -----------------------------
peak_response = np.nanmax(tuning_curves, axis=1)
responsive_cells = np.where(peak_response > min_response)[0]

print(f"\nNumber of sound-responsive cells: {len(responsive_cells)}\n")
print("Responsive cell indices:")
print(responsive_cells)

# -----------------------------
# USER INPUT
# -----------------------------
cell_idx = int(input("\nEnter a cell index from the list above: "))

if cell_idx not in responsive_cells:
    raise ValueError("Selected cell is not in responsive set.")

selected_cell_idx = cell_idx
print(f"Stored selected cell: {selected_cell_idx}")

# -----------------------------
# PANEL 1: EVENT-LOCKED RASTER
# -----------------------------
cell_data = eventlocked[cell_idx]

sort_trials = np.argsort(current_freq)
cell_data_sorted = cell_data[sort_trials]

# -----------------------------
# PLOT
# -----------------------------
fig, axes = plt.subplots(2, 1, figsize=(6, 8), sharex=False)

# Top panel
im = axes[0].imshow(
    cell_data_sorted,
    aspect='auto',
    extent=[tvec[0], tvec[-1], 0, len(cell_data_sorted)],
    cmap='viridis',
    interpolation='nearest'
)

axes[0].axvline(0, color='red', lw=1)
axes[0].set_ylabel("Trials (sorted by freq)")
axes[0].set_title(f"Cell {cell_idx} event-locked response")

cbar = plt.colorbar(im, ax=axes[0])
cbar.set_label("dF/F")

# Bottom panel
axes[1].plot(possible_freq, tuning_curves[cell_idx], 'o-', lw=2)
axes[1].set_xscale('log')
axes[1].set_xticks(possible_freq)
axes[1].set_xticklabels([f"{f/1000:.1f}" for f in possible_freq])

axes[1].set_xlabel("Frequency (kHz)")
axes[1].set_ylabel("ΔF/F (resp - baseline)")
axes[1].set_title(f"Tuning (best freq = {possible_freq[np.argmax(tuning_curves[cell_idx])]/1000:.2f} kHz)")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# -----------------------------
# SAVE (CONDITIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_cell{cell_idx}_interactive.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[131]:


# ============================================================
# SINGLE CELL: RESPONSES AT 2.4, 9.8, 30 kHz + BEST FREQ
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# GET BEST FREQUENCY
# -----------------------------
best_idx = np.argmax(tuning_curves[cell_idx])
best_freq = possible_freq[best_idx]

# -----------------------------
# TARGET FREQUENCIES (Hz)
# -----------------------------
target_freqs = np.array([2400, 9800, 30000, best_freq])

# match to nearest presented frequencies
possible_freq = np.unique(current_freq)
matched_freqs = []

for tf in target_freqs:
    idx = np.argmin(np.abs(possible_freq - tf))
    matched_freqs.append(possible_freq[idx])

# remove duplicates while preserving order
matched_freqs = list(dict.fromkeys(matched_freqs))

# -----------------------------
# EXTRACT CELL DATA
# -----------------------------
cell_data = eventlocked[cell_idx]  # (n_trials, time)

# -----------------------------
# PLOT
# -----------------------------
n_plots = len(matched_freqs)
fig, axes = plt.subplots(n_plots, 1, figsize=(6, 2.5*n_plots), sharex=True)

if n_plots == 1:
    axes = [axes]

for ax, freq_val in zip(axes, matched_freqs):
    
    trials = current_freq == freq_val
    data = cell_data[trials]
    
    if data.shape[0] == 0:
        ax.set_title(f"{freq_val/1000:.1f} kHz - no trials")
        continue
    
    mean_trace = np.nanmean(data, axis=0)
    sem_trace = np.nanstd(data, axis=0) / np.sqrt(data.shape[0])
    
    ax.plot(tvec, mean_trace, lw=2)
    ax.fill_between(tvec, mean_trace - sem_trace, mean_trace + sem_trace, alpha=0.3)
    
    ax.axvline(0, color='red', lw=1)
    ax.set_ylabel("dF/F")
    
    label = f"{freq_val/1000:.1f} kHz"
    if np.isclose(freq_val, best_freq):
        label += " (best)"
    
    ax.set_title(f"{label} (n={data.shape[0]} trials)")

axes[-1].set_xlabel("Time from sound onset (s)")

plt.tight_layout()
plt.show()

# -----------------------------
# SAVE (CONDITIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_cell{cell_idx}_multi_freq_best.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[134]:


# ============================================================
# TONOTOPIC MAP + CONTOURS + GRADIENT + SCALEBAR + HIGHLIGHT
# (FINAL, RED TARGET CELL)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# -----------------------------
# PARAMETERS
# -----------------------------
min_response = 0.02
um_per_pix = 1.2
scalebar_um = 100

# -----------------------------
# RESOLVE CELL INDEX
# -----------------------------
if 'selected_cell_idx' in globals():
    cell_idx_use = selected_cell_idx
elif 'cell_idx' in globals():
    cell_idx_use = cell_idx
else:
    raise ValueError("Run the selection cell first.")

print(f"Using cell: {cell_idx_use}")

# -----------------------------
# SELECT RESPONSIVE CELLS
# -----------------------------
peak_response = np.nanmax(tuning_curves, axis=1)
responsive = peak_response > min_response
inds = np.where(responsive)[0]

# -----------------------------
# COMPUTE BEST FREQ FOR ALL CELLS
# -----------------------------
best_freq_all = possible_freq[np.argmax(tuning_curves, axis=1)]

# -----------------------------
# ROI CENTROIDS
# -----------------------------
xpos = np.array([np.mean(data2p.stat[i]['xpix']) for i in inds])
ypos = np.array([np.mean(data2p.stat[i]['ypix']) for i in inds])

# -----------------------------
# FIT TONOTOPIC PLANE
# -----------------------------
z = np.log10(best_freq_all[inds])
X = np.column_stack([xpos, ypos, np.ones_like(xpos)])
(a, b, c), *_ = np.linalg.lstsq(X, z, rcond=None)

grad_vec = np.array([a, b])
grad_dir = grad_vec / np.linalg.norm(grad_vec)

# -----------------------------
# LOAD + NORMALIZE IMAGE
# -----------------------------
ops_path = "/data/twophoton/imag025_processed/20260417/000/suite2p/plane0/ops.npy"
ops = np.load(ops_path, allow_pickle=True).item()
mean_img = ops['meanImg']

p2, p98 = np.percentile(mean_img, [2, 98])
mean_img_disp = np.clip((mean_img - p2) / (p98 - p2), 0, 1) ** 0.7

h, w = mean_img.shape

# -----------------------------
# COLOR MAP
# -----------------------------
cmap = mpl.colormaps['viridis']
log_freqs = np.log10(possible_freq)
norm = mpl.colors.Normalize(vmin=log_freqs.min(), vmax=log_freqs.max())

rgb_img = np.stack([mean_img_disp]*3, axis=-1)
#rgb_img = np.stack([mean_img_disp]*3, axis=-1)*0

# draw all ROIs
for i in inds:
    roi = data2p.stat[i]
    ypix = roi['ypix'].astype(int)
    xpix = roi['xpix'].astype(int)
    color = np.array(cmap(norm(np.log10(best_freq_all[i])))[:3])
    rgb_img[ypix, xpix, :] = 0.3 * rgb_img[ypix, xpix, :] + 0.7 * color

# -----------------------------
# GRID FOR CONTOURS
# -----------------------------
yy, xx = np.mgrid[0:h, 0:w]
Z = a*xx + b*yy + c
levels_log = np.log10(possible_freq)

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(figsize=(6,6))
ax.imshow(rgb_img)

# contours
cs = ax.contour(xx, yy, Z, levels=levels_log, colors='white', linewidths=1)
fmt = {lvl: f"{(10**lvl)/1000:.1f}" for lvl in levels_log}
ax.clabel(cs, cs.levels, inline=True, fmt=fmt, fontsize=8, colors='red')

# gradient arrow
cx, cy = w/2, h/2
scale = 0.3 * min(h, w)
dx, dy = grad_dir * scale

ax.arrow(cx, cy, dx, dy, color='white', width=2, head_width=10)
ax.text(cx + dx, cy + dy, "High freq", color='red', fontsize=10, fontweight='bold')
ax.text(cx - dx, cy - dy, "Low freq",  color='red', fontsize=10, fontweight='bold')

# -----------------------------
# CORNER LABELS
# -----------------------------
margin = 25
ax.text(margin, margin, "D", color='red', fontsize=14, fontweight='bold')
ax.text(w - margin, margin, "P", color='red', fontsize=14, fontweight='bold', ha='right')
ax.text(w - margin, h - margin, "V", color='red', fontsize=14, fontweight='bold', ha='right', va='bottom')
ax.text(margin, h - margin, "A", color='red', fontsize=14, fontweight='bold', va='bottom')

# -----------------------------
# SCALE BAR
# -----------------------------
L_pix = scalebar_um / um_per_pix
x0 = 40
y0 = h - 110

ax.plot([x0, x0 + L_pix], [y0, y0], color='white', lw=3)
ax.plot([x0, x0], [y0, y0 - L_pix], color='white', lw=3)

ax.text(x0 + L_pix/2, y0 + 25, "100 µm",
        color='white', ha='center', va='top',
        fontsize=11, fontweight='bold')

ax.text(x0 - 12, y0 - L_pix/2, "100 µm",
        color='white', ha='right', va='center',
        fontsize=11, fontweight='bold', rotation=90)

# -----------------------------
# TARGET CELL HIGHLIGHT (RED)
# -----------------------------
roi = data2p.stat[cell_idx_use]
ypix = roi['ypix'].astype(int)
xpix = roi['xpix'].astype(int)

# white halo
ax.plot(xpix, ypix, '.', color='white', markersize=3)

# colored outline
cell_color = np.array(cmap(norm(np.log10(best_freq_all[cell_idx_use])))[:3])
ax.plot(xpix, ypix, '.', color=cell_color, markersize=1.5)

# red centroid circle
cx_cell = np.mean(xpix)
cy_cell = np.mean(ypix)
ax.plot(cx_cell, cy_cell, 'o',
        markerfacecolor='none',
        markeredgecolor='red',
        markersize=10,
        linewidth=2)

# red label
ax.text(cx_cell + 6, cy_cell - 6,
        f"Cell {cell_idx_use}",
        color='red', fontsize=9, fontweight='bold')

# -----------------------------
# COLORBAR
# -----------------------------
sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
cbar = fig.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Frequency (kHz, log scale)")

tick_vals = np.linspace(log_freqs.min(), log_freqs.max(), 5)
cbar.set_ticks(tick_vals)
cbar.set_ticklabels([f"{10**t/1000:.1f}" for t in tick_vals])

# -----------------------------
# FINAL
# -----------------------------
ax.set_title("Tonotopic map with highlighted selected cell")
ax.axis('off')

plt.tight_layout()
plt.show()

# -----------------------------
# SAVE (CONDITIONAL)
# -----------------------------
if 'SAVE_OUTPUTS' in globals() and SAVE_OUTPUTS:
    filename = f"{subject}_{date}_{session}_p{plane}_cell{cell_idx_use}_tonotopy_selected.png"
    save_path = OUTPUT_DIR / filename

    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved figure to:\n{save_path}")

# In[104]:


# ============================================================
# VERIFY MULTICHANNEL SUITE2P RUN (GREEN + RED)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# USER INPUT
# -----------------------------
plane_dir = input("Enter path to suite2p plane folder (e.g., .../suite2p/plane0):\n").strip()
plane_dir = Path(plane_dir).expanduser().resolve()

if not plane_dir.exists():
    raise FileNotFoundError(f"Directory not found:\n{plane_dir}")

# -----------------------------
# LOAD FILES
# -----------------------------
ops = np.load(plane_dir / "ops.npy", allow_pickle=True).item()
stat = np.load(plane_dir / "stat.npy", allow_pickle=True)
iscell = np.load(plane_dir / "iscell.npy", allow_pickle=True)

# optional files
F = np.load(plane_dir / "F.npy") if (plane_dir / "F.npy").exists() else None
F_chan2 = np.load(plane_dir / "F_chan2.npy") if (plane_dir / "F_chan2.npy").exists() else None

# -----------------------------
# BASIC CHECKS
# -----------------------------
print("\n=== BASIC INFO ===")
print(f"n ROIs: {len(stat)}")
print(f"n cells (iscell): {iscell[:,0].sum()}")

print("\n=== CHANNEL INFO ===")
print(f"nchannels (ops): {ops.get('nchannels', 'missing')}")
print(f"functional_chan: {ops.get('functional_chan', 'missing')}")
print(f"align_by_chan: {ops.get('align_by_chan', 'missing')}")

# -----------------------------
# CHECK RED CHANNEL
# -----------------------------
has_red_img = 'meanImg_chan2' in ops
has_F_chan2 = F_chan2 is not None
has_chan2_prob = 'chan2_prob' in stat[0]

print("\n=== RED CHANNEL CHECK ===")
print(f"meanImg_chan2 present: {has_red_img}")
print(f"F_chan2.npy present: {has_F_chan2}")
print(f"chan2_prob present: {has_chan2_prob}")

if not has_red_img:
    raise ValueError("No red channel detected (meanImg_chan2 missing).")

# -----------------------------
# LOAD IMAGES
# -----------------------------
green_img = ops['meanImg']
red_img = ops['meanImg_chan2']

def normalize(img):
    p2, p98 = np.percentile(img, [2, 98])
    return np.clip((img - p2) / (p98 - p2), 0, 1)

green_disp = normalize(green_img)
red_disp = normalize(red_img)

# -----------------------------
# PLOT SIDE-BY-SIDE
# -----------------------------
fig, axes = plt.subplots(1, 2, figsize=(10,5))

axes[0].imshow(green_disp, cmap='gray')
axes[0].set_title("Green (functional)")
axes[0].axis('off')

axes[1].imshow(red_disp, cmap='gray')
axes[1].set_title("Red (anatomical)")
axes[1].axis('off')

plt.tight_layout()
plt.show()

# -----------------------------
# OVERLAY ROIS ON RED IMAGE
# -----------------------------
plt.figure(figsize=(6,6))
plt.imshow(red_disp, cmap='gray')

for i, s in enumerate(stat):
    if iscell[i,0]:
        plt.plot(s['xpix'], s['ypix'], '.', color='cyan', markersize=0.5)

plt.title("ROIs (from green) over red image")
plt.axis('off')
plt.tight_layout()
plt.show()

# -----------------------------
# OPTIONAL: RED PROBABILITY DISTRIBUTION
# -----------------------------
if has_chan2_prob:
    red_prob = np.array([s['chan2_prob'] for s in stat])
    
    plt.figure(figsize=(5,4))
    plt.hist(red_prob[iscell[:,0]==1], bins=50)
    plt.xlabel("chan2_prob")
    plt.ylabel("count")
    plt.title("Red probability distribution")
    plt.tight_layout()
    plt.show()

    print("\nExample chan2_prob range:", red_prob.min(), "to", red_prob.max())

# -----------------------------
# OPTIONAL: RAW RED SIGNAL CHECK
# -----------------------------
if has_F_chan2:
    red_mean = F_chan2.mean(axis=1)
    
    plt.figure(figsize=(5,4))
    plt.hist(red_mean[iscell[:,0]==1], bins=50)
    plt.xlabel("Mean red fluorescence")
    plt.ylabel("count")
    plt.title("Red intensity across ROIs")
    plt.tight_layout()
    plt.show()

    print("\nF_chan2 shape:", F_chan2.shape)

print("\n=== DONE ===")

# In[105]:


# ============================================================
# HISTOGRAM OF RED INTENSITY ACROSS GREEN CELLS
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# USER INPUT
# -----------------------------
plane_dir = input("Enter path to suite2p plane folder (e.g., .../suite2p/plane0):\n").strip()
plane_dir = Path(plane_dir).expanduser().resolve()

# -----------------------------
# LOAD DATA
# -----------------------------
ops = np.load(plane_dir / "ops.npy", allow_pickle=True).item()
stat = np.load(plane_dir / "stat.npy", allow_pickle=True)
iscell = np.load(plane_dir / "iscell.npy", allow_pickle=True)

if not (plane_dir / "F_chan2.npy").exists():
    raise ValueError("F_chan2.npy not found — red channel not saved.")

F_red = np.load(plane_dir / "F_chan2.npy")

# -----------------------------
# SELECT GREEN CELLS
# -----------------------------
is_cell = iscell[:,0].astype(bool)

# -----------------------------
# COMPUTE RED INTENSITY
# -----------------------------
red_mean = F_red.mean(axis=1)
red_cells = red_mean[is_cell]

# -----------------------------
# PLOT HISTOGRAM
# -----------------------------
plt.figure(figsize=(5,4))
plt.hist(red_cells, bins=60)

plt.xlabel("Mean red fluorescence (F_chan2)")
plt.ylabel("Number of cells")
plt.title("Red intensity across green ROIs")

plt.tight_layout()
plt.show()

# -----------------------------
# PRINT SUMMARY
# -----------------------------
print("\nSummary:")
print(f"Total ROIs: {len(stat)}")
print(f"Green cells (iscell): {is_cell.sum()}")

print("\nRed intensity stats:")
print(f"min: {red_cells.min():.3f}")
print(f"median: {np.median(red_cells):.3f}")
print(f"max: {red_cells.max():.3f}")

# -----------------------------
# OPTIONAL: SUGGEST THRESHOLDS
# -----------------------------
p90 = np.percentile(red_cells, 90)
p95 = np.percentile(red_cells, 95)

print("\nSuggested thresholds:")
print(f"90th percentile: {p90:.3f}")
print(f"95th percentile: {p95:.3f}")

# In[106]:


# ============================================================
# RED HISTOGRAM (ISCELL ONLY) + OVERLAY ABOVE THRESHOLD
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# USER INPUT
# -----------------------------
plane_dir = input("Enter path to suite2p plane folder (e.g., .../suite2p/plane0):\n").strip()
plane_dir = Path(plane_dir).expanduser().resolve()

# -----------------------------
# LOAD DATA
# -----------------------------
ops = np.load(plane_dir / "ops.npy", allow_pickle=True).item()
stat = np.load(plane_dir / "stat.npy", allow_pickle=True)
iscell = np.load(plane_dir / "iscell.npy", allow_pickle=True)

F_red = np.load(plane_dir / "F_chan2.npy")

green_img = ops['meanImg']
red_img = ops['meanImg_chan2']

# -----------------------------
# NORMALIZE IMAGES
# -----------------------------
def norm_img(img):
    p2, p98 = np.percentile(img, [2, 98])
    return np.clip((img - p2) / (p98 - p2), 0, 1)

green_disp = norm_img(green_img)
red_disp = norm_img(red_img)

# -----------------------------
# SELECT ISCELL
# -----------------------------
is_cell = iscell[:,0].astype(bool)

# -----------------------------
# RED INTENSITY
# -----------------------------
red_mean = F_red.mean(axis=1)
red_cells = red_mean[is_cell]

# -----------------------------
# HISTOGRAM
# -----------------------------
plt.figure(figsize=(5,4))
plt.hist(red_cells, bins=60)

plt.xlabel("Mean red fluorescence (F_chan2)")
plt.ylabel("Number of cells")
plt.title("Red intensity (iscell only)")

plt.tight_layout()
plt.show()

# -----------------------------
# THRESHOLD (95th percentile)
# -----------------------------
thresh = np.percentile(red_cells, 95)
print(f"\nSuggested threshold (95th percentile): {thresh:.3f}")

# -----------------------------
# IDENTIFY RED-POSITIVE CELLS
# -----------------------------
red_positive = np.zeros(len(stat), dtype=bool)
red_positive[is_cell] = red_mean[is_cell] > thresh

print(f"Red-positive cells: {red_positive.sum()} / {is_cell.sum()}")

# -----------------------------
# PLOT GREEN + RED WITH OVERLAY
# -----------------------------
fig, axes = plt.subplots(1, 2, figsize=(10,5))

# LEFT: GREEN
axes[0].imshow(green_disp, cmap='gray')
axes[0].set_title("Green (functional)")
axes[0].axis('off')

# RIGHT: RED
axes[1].imshow(red_disp, cmap='gray')
axes[1].set_title("Red (anatomical)")
axes[1].axis('off')

# overlay ROIs on BOTH
for i, s in enumerate(stat):
    if red_positive[i]:
        xpix = s['xpix']
        ypix = s['ypix']
        
        axes[0].plot(xpix, ypix, '.', color='lime', markersize=1)
        axes[1].plot(xpix, ypix, '.', color='red', markersize=1)

plt.tight_layout()
plt.show()

# In[109]:


# ============================================================
# RED HISTOGRAM (ISCELL ONLY) + OVERLAY ABOVE THRESHOLD
# (RIGHT HIST Y-MAX = SECOND BIN)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# USER INPUT
# -----------------------------
plane_dir = input("Enter path to suite2p plane folder (e.g., .../suite2p/plane0):\n").strip()
plane_dir = Path(plane_dir).expanduser().resolve()

# -----------------------------
# LOAD DATA
# -----------------------------
ops = np.load(plane_dir / "ops.npy", allow_pickle=True).item()
stat = np.load(plane_dir / "stat.npy", allow_pickle=True)
iscell = np.load(plane_dir / "iscell.npy", allow_pickle=True)

F_red = np.load(plane_dir / "F_chan2.npy")

green_img = ops['meanImg']
red_img = ops['meanImg_chan2']

# -----------------------------
# NORMALIZE IMAGES
# -----------------------------
def norm_img(img):
    p2, p98 = np.percentile(img, [2, 98])
    return np.clip((img - p2) / (p98 - p2), 0, 1)

green_disp = norm_img(green_img)
red_disp = norm_img(red_img)

# -----------------------------
# SELECT ISCELL
# -----------------------------
is_cell = iscell[:,0].astype(bool)

# -----------------------------
# RED INTENSITY
# -----------------------------
red_mean = F_red.mean(axis=1)
red_cells = red_mean[is_cell]

# -----------------------------
# THRESHOLD
# -----------------------------
thresh = np.percentile(red_cells, 95)
print(f"\nSuggested threshold (95th percentile): {thresh:.3f}")

# -----------------------------
# HISTOGRAMS
# -----------------------------
fig, axes = plt.subplots(1, 2, figsize=(10,4))

# ---- FULL HIST ----
counts, bins, _ = axes[0].hist(red_cells, bins=60)
axes[0].axvline(thresh, color='red', linestyle='--', linewidth=2)
axes[0].set_xlabel("Mean red fluorescence (F_chan2)")
axes[0].set_ylabel("Number of cells")
axes[0].set_title("Full distribution")

# ---- RIGHT HIST (Y-MAX = SECOND BIN) ----
counts_zoom, bins_zoom, _ = axes[1].hist(red_cells, bins=60)

axes[1].axvline(thresh, color='red', linestyle='--', linewidth=2)

# set y max to second bin count (index 1)
if len(counts_zoom) > 1:
    ymax = counts_zoom[1]
else:
    ymax = counts_zoom.max()

axes[1].set_ylim(0, ymax * 1.05)  # small padding

axes[1].set_xlabel("Mean red fluorescence (F_chan2)")
axes[1].set_ylabel("Number of cells")
axes[1].set_title("Zoomed (y-max = 2nd bin)")

plt.tight_layout()
plt.show()

# -----------------------------
# IDENTIFY RED-POSITIVE CELLS
# -----------------------------
red_positive = np.zeros(len(stat), dtype=bool)
red_positive[is_cell] = red_mean[is_cell] > thresh

print(f"Red-positive cells: {red_positive.sum()} / {is_cell.sum()}")

# -----------------------------
# PLOT GREEN + RED WITH OVERLAY
# -----------------------------
fig, axes = plt.subplots(1, 2, figsize=(10,5))

axes[0].imshow(green_disp, cmap='gray')
axes[0].set_title("Green (functional)")
axes[0].axis('off')

axes[1].imshow(red_disp, cmap='gray')
axes[1].set_title("Red (anatomical)")
axes[1].axis('off')

for i, s in enumerate(stat):
    if red_positive[i]:
        xpix = s['xpix']
        ypix = s['ypix']
        axes[0].plot(xpix, ypix, '.', color='lime', markersize=1)
        axes[1].plot(xpix, ypix, '.', color='red', markersize=1)

plt.tight_layout()
plt.show()

# In[111]:


## ============================================================
# THRESHOLDED RED IMAGE (ROI-BASED) IN TRUE RED
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# USER INPUT
# -----------------------------
plane_dir = input("Enter path to suite2p plane folder (e.g., .../suite2p/plane0):\n").strip()
plane_dir = Path(plane_dir).expanduser().resolve()

# -----------------------------
# LOAD DATA
# -----------------------------
ops = np.load(plane_dir / "ops.npy", allow_pickle=True).item()
stat = np.load(plane_dir / "stat.npy", allow_pickle=True)
iscell = np.load(plane_dir / "iscell.npy", allow_pickle=True)

F_red = np.load(plane_dir / "F_chan2.npy")

if 'meanImg_chan2' not in ops:
    raise ValueError("meanImg_chan2 not found.")

red_img = ops['meanImg_chan2']

# -----------------------------
# NORMALIZE BACKGROUND IMAGE
# -----------------------------
p2, p98 = np.percentile(red_img, [2, 98])
red_disp = np.clip((red_img - p2) / (p98 - p2), 0, 1)

# -----------------------------
# COMPUTE RED INTENSITY (ISCELL ONLY)
# -----------------------------
is_cell = iscell[:,0].astype(bool)

red_mean = F_red.mean(axis=1)
red_cells = red_mean[is_cell]

# threshold (same as previous cell)
thresh = np.percentile(red_cells, 95)
print(f"Using threshold: {thresh:.3f}")

# -----------------------------
# BUILD ROI MASK
# -----------------------------
h, w = red_img.shape
mask = np.zeros((h, w), dtype=float)

for i, s in enumerate(stat):
    if is_cell[i] and red_mean[i] > thresh:
        ypix = s['ypix'].astype(int)
        xpix = s['xpix'].astype(int)
        mask[ypix, xpix] = 1.0

# -----------------------------
# MAKE TRUE RED IMAGE
# -----------------------------
rgb = np.zeros((h, w, 3))
rgb[..., 0] = mask            # red channel only

# optional: faint anatomical background
rgb[..., 0] = np.maximum(rgb[..., 0], 0.2 * red_disp)

# -----------------------------
# PLOT
# -----------------------------
plt.figure(figsize=(6,6))
plt.imshow(rgb)
plt.title("Thresholded Red Cells (ROI-based)")
plt.axis('off')

plt.tight_layout()
plt.show()

# In[113]:


# ============================================================
# RED CELLS (FILLED) + ALL ROI OUTLINES (THIN LIGHT GREEN)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.ndimage import binary_erosion

# -----------------------------
# USER INPUT
# -----------------------------
plane_dir = input("Enter path to suite2p plane folder (e.g., .../suite2p/plane0):\n").strip()
plane_dir = Path(plane_dir).expanduser().resolve()

# -----------------------------
# LOAD DATA
# -----------------------------
ops = np.load(plane_dir / "ops.npy", allow_pickle=True).item()
stat = np.load(plane_dir / "stat.npy", allow_pickle=True)
iscell = np.load(plane_dir / "iscell.npy", allow_pickle=True)

F_red = np.load(plane_dir / "F_chan2.npy")

if 'meanImg_chan2' not in ops:
    raise ValueError("meanImg_chan2 not found.")

red_img = ops['meanImg_chan2']

# -----------------------------
# NORMALIZE RED IMAGE
# -----------------------------
p2, p98 = np.percentile(red_img, [2, 98])
red_disp = np.clip((red_img - p2) / (p98 - p2), 0, 1)

# -----------------------------
# RED CELL THRESHOLD (ISCELL ONLY)
# -----------------------------
is_cell = iscell[:,0].astype(bool)
red_mean = F_red.mean(axis=1)

thresh = np.percentile(red_mean[is_cell], 95)
print(f"Using threshold: {thresh:.3f}")

# -----------------------------
# BUILD RED CELL MASK (FILLED)
# -----------------------------
h, w = red_img.shape
red_mask = np.zeros((h, w), dtype=bool)

for i, s in enumerate(stat):
    if is_cell[i] and red_mean[i] > thresh:
        ypix = s['ypix'].astype(int)
        xpix = s['xpix'].astype(int)
        red_mask[ypix, xpix] = True

# -----------------------------
# BUILD ROI OUTLINE MASK (ALL ROIs)
# -----------------------------
roi_mask = np.zeros((h, w), dtype=bool)

for s in stat:
    ypix = s['ypix'].astype(int)
    xpix = s['xpix'].astype(int)
    roi_mask[ypix, xpix] = True

# thin outlines via erosion
eroded = binary_erosion(roi_mask)
outline_mask = roi_mask & (~eroded)

# -----------------------------
# BUILD RGB IMAGE
# -----------------------------
rgb = np.zeros((h, w, 3))

# faint red background
rgb[..., 0] = 0.2 * red_disp

# filled red cells
rgb[..., 0][red_mask] = 1.0

# light green outlines
rgb[..., 1][outline_mask] = 0.8   # green
rgb[..., 0][outline_mask] = 0.2   # slight yellow tint for visibility

# -----------------------------
# PLOT
# -----------------------------
plt.figure(figsize=(6,6))
plt.imshow(rgb)
plt.title("Red cells (filled) + ROI outlines (light green)")
plt.axis('off')

plt.tight_layout()
plt.show()

# In[114]:


# ============================================================
# RED CELLS AT MULTIPLE THRESHOLDS + ROI OUTLINES
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.ndimage import binary_erosion

# -----------------------------
# USER INPUT
# -----------------------------
plane_dir = input("Enter path to suite2p plane folder (e.g., .../suite2p/plane0):\n").strip()
plane_dir = Path(plane_dir).expanduser().resolve()

# -----------------------------
# LOAD DATA
# -----------------------------
ops = np.load(plane_dir / "ops.npy", allow_pickle=True).item()
stat = np.load(plane_dir / "stat.npy", allow_pickle=True)
iscell = np.load(plane_dir / "iscell.npy", allow_pickle=True)
F_red = np.load(plane_dir / "F_chan2.npy")

red_img = ops['meanImg_chan2']

# -----------------------------
# NORMALIZE RED IMAGE
# -----------------------------
p2, p98 = np.percentile(red_img, [2, 98])
red_disp = np.clip((red_img - p2) / (p98 - p2), 0, 1)

# -----------------------------
# COMPUTE RED INTENSITY
# -----------------------------
is_cell = iscell[:,0].astype(bool)
red_mean = F_red.mean(axis=1)

base_thresh = np.percentile(red_mean[is_cell], 95)

thresholds = [
    base_thresh,
    (2/3) * base_thresh,
    (1/3) * base_thresh
]

titles = [
    f"Threshold = {base_thresh:.3f}",
    f"Threshold = {2/3*base_thresh:.3f}",
    f"Threshold = {1/3*base_thresh:.3f}"
]

# -----------------------------
# BUILD ROI OUTLINE MASK (ONCE)
# -----------------------------
h, w = red_img.shape
roi_mask = np.zeros((h, w), dtype=bool)

for s in stat:
    ypix = s['ypix'].astype(int)
    xpix = s['xpix'].astype(int)
    roi_mask[ypix, xpix] = True

outline_mask = roi_mask & (~binary_erosion(roi_mask))

# -----------------------------
# PLOT 3 PANELS
# -----------------------------
fig, axes = plt.subplots(1, 3, figsize=(15,5))

for ax, thresh, title in zip(axes, thresholds, titles):
    
    # build red mask
    red_mask = np.zeros((h, w), dtype=bool)
    
    for i, s in enumerate(stat):
        if is_cell[i] and red_mean[i] > thresh:
            ypix = s['ypix'].astype(int)
            xpix = s['xpix'].astype(int)
            red_mask[ypix, xpix] = True
    
    # build RGB image
    rgb = np.zeros((h, w, 3))
    
    # faint background
    rgb[...,0] = 0.2 * red_disp
    
    # red cells
    rgb[...,0][red_mask] = 1.0
    
    # light green outlines
    rgb[...,1][outline_mask] = 0.8
    rgb[...,0][outline_mask] = 0.2
    
    # plot
    ax.imshow(rgb)
    ax.set_title(title)
    ax.axis('off')

plt.tight_layout()
plt.show()

# In[115]:


# ============================================================
# HYBRID IMAGE:
# - ROIs: thresholded red cells (filled)
# - OUTSIDE ROIs: full red signal (no threshold)
# - ROI outlines: light green
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.ndimage import binary_erosion

# -----------------------------
# USER INPUT
# -----------------------------
plane_dir = input("Enter path to suite2p plane folder (e.g., .../suite2p/plane0):\n").strip()
plane_dir = Path(plane_dir).expanduser().resolve()

# -----------------------------
# LOAD DATA
# -----------------------------
ops = np.load(plane_dir / "ops.npy", allow_pickle=True).item()
stat = np.load(plane_dir / "stat.npy", allow_pickle=True)
iscell = np.load(plane_dir / "iscell.npy", allow_pickle=True)
F_red = np.load(plane_dir / "F_chan2.npy")

red_img = ops['meanImg_chan2']

# -----------------------------
# NORMALIZE RED IMAGE
# -----------------------------
p2, p98 = np.percentile(red_img, [2, 98])
red_disp = np.clip((red_img - p2) / (p98 - p2), 0, 1)

# -----------------------------
# RED INTENSITY + THRESHOLD
# -----------------------------
is_cell = iscell[:,0].astype(bool)
red_mean = F_red.mean(axis=1)

thresh = np.percentile(red_mean[is_cell], 95)
print(f"Using threshold: {thresh:.3f}")

# -----------------------------
# BUILD ROI MASK (ALL ROIs)
# -----------------------------
h, w = red_img.shape
roi_mask = np.zeros((h, w), dtype=bool)

for s in stat:
    ypix = s['ypix'].astype(int)
    xpix = s['xpix'].astype(int)
    roi_mask[ypix, xpix] = True

# -----------------------------
# BUILD RED-POSITIVE MASK (ROIs ONLY)
# -----------------------------
red_mask = np.zeros((h, w), dtype=bool)

for i, s in enumerate(stat):
    if is_cell[i] and red_mean[i] > thresh:
        ypix = s['ypix'].astype(int)
        xpix = s['xpix'].astype(int)
        red_mask[ypix, xpix] = True

# -----------------------------
# ROI OUTLINES (THIN)
# -----------------------------
outline_mask = roi_mask & (~binary_erosion(roi_mask))

# -----------------------------
# BUILD RGB IMAGE
# -----------------------------
rgb = np.zeros((h, w, 3))

# --- OUTSIDE ROIs: full red signal ---
outside = ~roi_mask
rgb[..., 0][outside] = red_disp[outside]

# --- INSIDE ROIs ---
# start with dark background inside ROIs
rgb[..., 0][roi_mask] = 0.1 * red_disp[roi_mask]

# fill only red-positive cells
rgb[..., 0][red_mask] = 1.0

# -----------------------------
# DRAW ROI OUTLINES (LIGHT GREEN)
# -----------------------------
rgb[..., 1][outline_mask] = 0.8
rgb[..., 0][outline_mask] = 0.2  # slight yellow tint

# -----------------------------
# PLOT
# -----------------------------
plt.figure(figsize=(6,6))
plt.imshow(rgb)
plt.title("Hybrid: thresholded ROIs + full red outside ROIs")
plt.axis('off')

plt.tight_layout()
plt.show()

# In[116]:


import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

plane_dir = input("Enter suite2p plane dir:\n").strip()
plane_dir = Path(plane_dir)

ops = np.load(plane_dir / "ops.npy", allow_pickle=True).item()

green = ops['meanImg']
red = ops.get('meanImg_chan2', None)

print("\n=== CHANNEL CHECK ===")
print("meanImg (green) shape:", green.shape)
print("meanImg_chan2 exists:", red is not None)

def norm(img):
    p2, p98 = np.percentile(img, [2,98])
    return np.clip((img - p2)/(p98-p2), 0, 1)

fig, ax = plt.subplots(1,3, figsize=(12,4))

ax[0].imshow(norm(green), cmap='gray')
ax[0].set_title("meanImg (channel 1)")

if red is not None:
    ax[1].imshow(norm(red), cmap='gray')
    ax[1].set_title("meanImg_chan2 (channel 2)")

    ax[2].imshow(norm(green) - norm(red), cmap='bwr')
    ax[2].set_title("Green - Red difference")

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()

# In[118]:


import numpy as np

ops = np.load("/data/twophoton/imag025_processed/20260417/000/suite2p_red_cl/suite2p/plane0/ops.npy", allow_pickle=True).item()

g = ops['meanImg']
r = ops['meanImg_chan2']

print("Mean abs diff:", np.mean(np.abs(g - r)))

# In[119]:


import numpy as np
import matplotlib.pyplot as plt

ops = np.load("/data/twophoton/imag025_processed/20260417/000/suite2p_red_cl/suite2p/plane0/ops.npy", allow_pickle=True).item()

g = ops['meanImg']
r = ops['meanImg_chan2']

def norm(img):
    p2, p98 = np.percentile(img, [2,98])
    return np.clip((img - p2)/(p98-p2), 0, 1)

g = norm(g)
r = norm(r)

rgb = np.zeros((g.shape[0], g.shape[1], 3))
rgb[...,1] = g   # green channel
rgb[...,0] = r   # red channel

plt.figure(figsize=(6,6))
plt.imshow(rgb)
plt.title("Overlay (Red = anatomical, Green = functional)")
plt.axis('off')
plt.show()
