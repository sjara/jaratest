

import subprocess
import jaratoolbox
from jaratoolbox import settings,loadneuropix
import os
import sys
import importlib
import numpy as np
import pandas as pd
import sys
from pathlib import Path
import shutil

import UnitMatchPy.extract_raw_data as erd
from joblib import Parallel, delayed
import matplotlib.pyplot as plt
import json
import UnitMatchPy.default_params as default_params
import UnitMatchPy.utils as util
import UnitMatchPy.overlord as ov
import UnitMatchPy.bayes_functions as bf
import matplotlib.pyplot as plt
import numpy as np

UMpath = '/home/ramzy/src/UnitMatch'

sys.path.insert(0, os.path.join(UMpath,'UnitMatchPy'))
sys.path.insert(0, os.path.join(UMpath))
sys.path.insert(0, os.path.join(UMpath,'UnitMatchPy','DeepUnitMatch'))

from DeepUnitMatch.utils import param_fun
from DeepUnitMatch.testing import test
from DeepUnitMatch.preprocess import split_units
import UnitMatchPy.assign_unique_id as aid
import UnitMatchPy.save_utils as su
from DeepUnitMatch.testing import test
from DeepUnitMatch.utils import helpers


sys.path.insert(0,'/home/ramzy/src/jaratest/ramzy/2025hemisym')
import studyparams
from importlib import reload

reload(erd)



def extract_raw_waveforms(KS_dirs,raw_root=settings.EPHYS_NEUROPIX_RAW_PATH):
    #Set Up Parameters
    sample_amount = 1000 # for both CV, at least 500 per CV
    spike_width = 82 # assuming 30khz sampling, 82 and 61 are common choices (KS1-3, KS4), covers the AP and space around needed for processing
    half_width = np.floor(spike_width/2).astype(int)
    max_width = np.floor(spike_width/2).astype(int) #Size of area at start and end of recording to ignore to get only full spikes
    n_channels = 384 #neuropixels default, the number of channels EXCLUDING sync channels
    extract_good_units_only = True # bool, set to true if you want to only extract units marked as good 

    KS4_data = False #bool, set to true if using Kilosort, as KS4 spike times refer to start of waveform not peak
    if KS4_data:
        samples_before = 20
        samples_after = spike_width - samples_before
        max_width = samples_after #Number of samples on either side of the 

    #List of paths to a KS directory, can pass paths 
    # KS_dirs = [r'path/to/KiloSort/Dir/Session1', r'path/to/KiloSort/Dir/Session2']
    n_sessions = len(KS_dirs) #How many session are being extracted
    spike_ids, spike_times, good_units, all_unit_ids = erd.extract_KS_data(KS_dirs, extract_good_units_only = True)


    #give metadata + Raw data paths
    # data_paths = [r'path/to/Decompressed/data1.dat', r'path/to/Decompressed/data2.dat']
    # meta_paths = [r'path/to/data/structure.oebin', r'path/to/data/structure.oebin']

    data_paths = [os.path.join(raw_root,subject,f'multisession_{date}_{pDepth}um_raw','multisession_continuous.dat') for date in sessionDates]
    meta_paths = [str(next(Path(os.path.join(raw_root,subject,f'multisession_{date}_{pDepth}um_processed')).rglob('structure.oebin'), None)) for date in sessionDates]

    #Extract the units 

    if extract_good_units_only:
        for sid in range(n_sessions):
            #load metadata
            with open(meta_paths[sid], 'r') as file:
                meta = json.load(file)
            n_bytes = os.path.getsize(data_paths[sid])
            n_channels_tot = int(meta['continuous'][0]['num_channels'])
            n_samples = int(n_bytes / (2*n_channels_tot))

            #create memmap to raw data, for that session
            data = np.memmap(data_paths[sid], dtype = 'int16', shape =(n_samples, n_channels_tot))

            # Remove spike which won't have a full waveform recorded
            spike_ids_tmp = np.delete(spike_ids[sid], np.logical_or( (spike_times[sid] < max_width), ( spike_times[sid] > (data.shape[0] - max_width))))
            spike_times_tmp = np.delete(spike_times[sid], np.logical_or( (spike_times[sid] < max_width), ( spike_times[sid] > (data.shape[0] - max_width))))


            #might be slow extracting sample for good units only?
            sample_idx = erd.get_sample_idx(spike_times_tmp, spike_ids_tmp, sample_amount, units = good_units[sid])

            if KS4_data:
                avg_waveforms = Parallel(n_jobs = -1, verbose = 10, mmap_mode='r', max_nbytes=None )(delayed(erd.extract_a_unit_KS4)(sample_idx[uid], data, samples_before, samples_after, spike_width, n_channels, sample_amount)for uid in range(good_units[sid].shape[0]))
                avg_waveforms = np.asarray(avg_waveforms)           
            else:
                avg_waveforms = Parallel(n_jobs = -1, verbose = 10, mmap_mode='r', max_nbytes=None )(delayed(erd.extract_a_unit)(sample_idx[uid], data, half_width, spike_width, n_channels, sample_amount)for uid in range(good_units[sid].shape[0]))
                avg_waveforms = np.asarray(avg_waveforms)

            #Save in file named 'RawWaveforms' in the KS Directory
            erd.save_avg_waveforms(avg_waveforms, KS_dirs[sid], all_unit_ids[sid].T[0], good_units = good_units[sid].T[0], extract_good_units_only = extract_good_units_only)

    else:
        for sid in range(n_sessions):
            #Extracting ALL the Units
            n_units = len(np.unique(spike_ids[sid]))
            #load metadata
            with open(meta_paths[sid], 'r') as file:
                meta = json.load(file)
            n_bytes = os.path.getsize(data_paths[sid])
            n_channels_tot = int(meta['continuous'][0]['num_channels'])
            n_samples = int(n_bytes / (2*n_channels_tot))

            #create memmap to raw data, for that session
            data = np.memmap(data_paths[sid], dtype = 'int16', shape =(n_samples, n_channels_tot))

            # Remove spikes which won't have a full waveform recorded
            spike_ids_tmp = np.delete(spike_ids[sid], np.logical_or( (spike_times[sid] < max_width), ( spike_times[sid] > (data.shape[0] - max_width))))
            spike_times_tmp = np.delete(spike_times[sid], np.logical_or( (spike_times[sid] < max_width), ( spike_times[sid] > (data.shape[0] - max_width))))


            sample_idx = erd.get_sample_idx(spike_times_tmp, spike_ids_tmp, sample_amount, units= np.unique(spike_ids[sid]))
            
            if KS4_data:
                avg_waveforms = Parallel(n_jobs = -1, verbose = 10, mmap_mode='r', max_nbytes=None )(delayed(erd.extract_a_unit_KS4)(sample_idx[uid], data, samples_before, samples_after, spike_width, n_channels, sample_amount)for uid in range(n_units))
                avg_waveforms = np.asarray(avg_waveforms)           
            else:
                avg_waveforms = Parallel(n_jobs = -1, verbose = 10, mmap_mode='r', max_nbytes=None )(delayed(erd.extract_a_unit)(sample_idx[uid], data, half_width, spike_width, n_channels, sample_amount)for uid in range(n_units))
                avg_waveforms = np.asarray(avg_waveforms)

            #Save in file named 'RawWaveforms' in the KS Directory
            erd.save_avg_waveforms(avg_waveforms, KS_dirs[sid], all_unit_ids[sid].T[0], good_units = good_units[sid].T[0], extract_good_units_only = extract_good_units_only)
    del data

    pass


def run_deep_unit_match(KS_dirs,save_dir):

    # Getting the data the same way as UnitMatch

    # Get default parameters, can add your own before or after!
    param = default_params.get_default_param()

    # Give the paths to the KS directories for each session
    # If you don't have a dir with channel_positions.npy etc look at the detailed example for supplying paths separately
    # KS_dirs = [r'path/to/KSdir/Session1', r'path/to/KSdir/Session2', r'path/to/KSdir/Session3', r'path/to/KSdir/Session4']

    param['KS_dirs'] = KS_dirs
    wave_paths, unit_label_paths, channel_pos = util.paths_from_KS(KS_dirs)
    param = util.get_probe_geometry(channel_pos[0], param)

    # STEP 0 from the UMPy example notebook
    waveform, session_id, session_switch, within_session, good_units, param = util.load_good_waveforms(wave_paths, unit_label_paths, param, good_units_only = True)
    param['good_units'] = good_units


    # Preprocess the DeepUnitMatch way and save as HDF5 files for each session in 'processed_waveforms'.
    snippets, positions = param_fun.get_snippets(waveform, channel_pos, session_id)

    # Load the neural net
    model = test.load_trained_model(device="cpu")

    # We have stored the preprocessed data here (from the get_snippets function)
    data_dir = os.path.join(UMpath, 'UnitMatchPy','DeepUnitMatch', 'processed_waveforms')

    # Pass the preprocessed data through the neural net
    sim_matrix = test.inference(model, data_dir)

    # Optionally, you can remove split units to get cleaner data and results. This detects where spike sorting may have split units and merges them back together.

    merged_sim_matrix, merged_param, merged_session_id, merged_session_switch = split_units.merge_and_remove_splits(param, sim_matrix, session_id, model, data_dir)

    # If you want to go ahead with the results of merging,
    sim_matrix = merged_sim_matrix
    param = merged_param
    session_id = merged_session_id
    session_switch = merged_session_switch

    # If you change your mind, you can also undo the merge:
    # split_units.undo_merge(data_dir)
    # You will need to recompute the above variables if you changed them (sim_matrix, param, session_id, session_switch) after merging.

    # Visualise the similarity matrix
    plt.imshow(sim_matrix, cmap='viridis', aspect='auto')
    plt.colorbar()
    plt.savefig(os.path.join(save_dir,'similarity_matrix.png'),format='png')

    # Extract parameters from waveform. We only need the distance matrix in DeepUnitMatch.
    clus_info = {'good_units' : param['good_units'], 'session_switch' : session_switch, 'session_id' : session_id, 
                'original_ids' : np.concatenate(param['good_units']) }
    extracted_wave_properties = ov.extract_parameters(waveform, channel_pos, clus_info, param)                  # contains spatial locations
    within_session = 1 - (session_id[:, None] == session_id).astype(int)
    distance_matrix, candidate_pairs, scores_to_include, predictors  = ov.extract_metric_scores(extracted_wave_properties, session_switch, within_session, param, 
                                                                                            niter  = 2, to_use=['centroid_dist'])

    # Use the same Naive Bayes as in UnitMatchPy


    sessions = np.unique(session_id)
    match_dfs = []
    probs = np.zeros(sim_matrix.shape)

    for r1 in sessions:
        for r2 in sessions:
            if r1 >= r2:
                continue
            mask = np.isin(session_id, [r1, r2])
            sim_mat = sim_matrix[mask][:, mask]
            dist_mat = distance_matrix[mask][:, mask]
            indices = np.where(np.isin(session_id, [r1, r2]))[0]
            df = helpers.create_dataframe([param['good_units'][r1], param['good_units'][r2]], sim_mat, session_list=[r1, r2])
            matches = test.get_matches(df, sim_mat, session_id[indices], data_dir, positions[indices], dist_thresh=20)
            labels = np.eye(sim_mat.shape[0])
            subsessionid = np.array([r1] * len(param['good_units'][r1]) + [r2] * len(param['good_units'][r2]))
            for (recses1, recses2), group in matches.groupby(by=['RecSes1', 'RecSes2']):
                asmatrix = group['match'].values.reshape(len(param['good_units'][recses1]), len(param['good_units'][recses2])).astype(int)
                labels[np.ix_(subsessionid == recses1, subsessionid == recses2)] = asmatrix
            scores_to_incl = {
                'similarity': sim_mat,
                'distance': dist_mat,
            }
            n_units = int(np.sqrt(len(df)))
            priors = np.array([1 - 2 / n_units, 2 / n_units])
            parameter_kernels = bf.get_parameter_kernels(scores_to_incl, labels, np.unique(labels), param)
            predictors = np.stack([scores for scores in scores_to_incl.values()], axis=2)
            probability = bf.apply_naive_bayes(parameter_kernels, priors, predictors, param, np.unique(labels))
            prob_matrix = probability[:,1].reshape(n_units, n_units)
            probs[np.ix_(mask, mask)] = prob_matrix

    # Visualise the output probability matrix

    plt.imshow(probs, cmap='viridis', aspect='auto')
    plt.colorbar()

    plt.savefig(os.path.join(save_dir,'probability_matrix.png'),format='png')


    # UnitMatchPy evaluation function

    util.evaluate_output(probs, param, within_session, session_switch, match_threshold = 0.9)

    # Process the output probability matrix to get final set of matches (across sessions)
    param['match_threshold'] = 0.1                                          # you should set this to control how conservative you want the matching to be. lower threshold -> more matches
    matches = probs > param['match_threshold']
    within_session = (session_id[:, None] == session_id).astype(bool)
    final_matches = matches.copy()
    final_matches[within_session] = 0
    plt.imshow(final_matches, cmap='viridis')
    plt.colorbar()
    plt.savefig(os.path.join(save_dir,'final_matches.png'),format='png')
    print(f" Found {np.sum(final_matches)} matches in these sessions using the threshold of {param['match_threshold']}. Total number of units: {param['n_units']}")

    # Now we can check performance using the AUC. This tests the agreement between DeepUnitMatch matches and functional scores (in this case, ISI histogram correlations).

    isicorr = test.ISI_correlations(param)
    auc = test.AUC(final_matches, isicorr, session_id)
    print(f"AUC for DeepUnitMatch matches: {auc:.3f}")


    # Finally, we can do tracking using the UnitMatch tracking function. This assigns unique IDs to the neurons that will persist across many sessions.

    UIDs = aid.assign_unique_id(probs, param, clus_info)

    # Save the results
    amplitude = extracted_wave_properties['amplitude']
    spatial_decay = extracted_wave_properties['spatial_decay']
    avg_centroid = extracted_wave_properties['avg_centroid']
    avg_waveform = extracted_wave_properties['avg_waveform']
    avg_waveform_per_tp = extracted_wave_properties['avg_waveform_per_tp']
    wave_idx = extracted_wave_properties['good_wave_idxs']
    max_site = extracted_wave_properties['max_site']
    max_site_mean = extracted_wave_properties['max_site_mean']
    su.save_to_output(save_dir, scores_to_include, np.argwhere(final_matches), probs, avg_centroid, avg_waveform, avg_waveform_per_tp, max_site,
                    distance_matrix, final_matches, clus_info, param, UIDs = UIDs, matches_curated = None, save_match_table = True)

    pass

subject = sys.argv[1]
pDepth = int(sys.argv[2])
sessionDates = studyparams.SESSION_DATES_EACH_SITE[pDepth]
debug = 'debug' if (len(sys.argv)==5 and sys.argv[4]=='debug') else ''


sessionsRootPath = os.path.join(settings.EPHYS_NEUROPIX_RAW_PATH, subject)
KSpath = os.path.join(settings.EPHYS_NEUROPIX_PATH)
remote_dir = f'jarauser@jarastore:/data/neuropixels/{subject}/'

# -- Load inforec file --
inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
spec = importlib.util.spec_from_file_location('inforec_module', inforecFile)
inforec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inforec)

for date in sessionDates:
    
    multisessionRawDir = os.path.join(sessionsRootPath , f'multisession_{date}_{pDepth}um_raw')
    multisessionProcessedDir = os.path.join(sessionsRootPath , f'multisession_{date}_{pDepth}um_processed')
    multisessionProcessedDirBash = multisessionProcessedDir.replace('d:','/mnt/d').replace('\\','/')
    rawFilename = os.path.join(multisessionRawDir , 'multisession_continuous.dat')

    # -- Find sessions to concatenate --
    siteToProcess = None
    for experiment in inforec.experiments:
        if experiment.date in date:
            for site in experiment.sites:
                if site.pdepth==pDepth:
                    probeStr = experiment.probe
                    siteToProcess = site
    if siteToProcess is None:
        print(f'No session for {subject} on {date} at {pDepth}um.')
        continue
    sessions = siteToProcess.session_ephys_dirs()

    if not os.path.exists(multisessionRawDir):
        subprocess.run([sys.executable,
                        os.path.join('/home/ramzy/src/jaratoolbox/scripts/neuropix_join_multisession.py'),
                        subject, date, str(pDepth), debug])



        if debug:
            print(f'''To proceed with debugging, please create concatenated files for the sessions on {date} at {pDepth}um (see neuropix_join_multisession.py).''')
        continue
    

KS_dirs = [os.path.join(KSpath,subject,f"multisession_{date}_{pDepth}um_processed") for date in sessionDates]
save_dir = os.path.join(KSpath,subject,f'UnitMatch_{"_".join(sessionDates)}')

if not os.path.exists(save_dir):
    os.mkdir(save_dir)

# extract_raw_waveforms(KS_dirs)
run_deep_unit_match(KS_dirs,save_dir)

if 0:
    for date in sessionDates:
        shutil.rmtree(os.path.join(sessionsRootPath , f'multisession_{date}_{pDepth}um_raw'))
        shutil.rmtree(os.path.join(sessionsRootPath , f'multisession_{date}_{pDepth}um_processed'))

if 0:
    if 'win' in sys.platform:

        subprocess.run(['wsl','rsync','-av',
                        save_dir,
                        remote_dir])

    else:
        subprocess.run(['rsync','-av',
                        save_dir,
                        remote_dir])

# else:
#     subprocess.run(['wsl','rsync','-av', '--dry-run',
#                     save_dir,
#                     remote_dir])
