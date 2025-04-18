"""
1. Plot a couple a frames from the video

"""

import tifffile
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import traceback
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis

# -- Load the data --
#Number of sessions 
#date = '20240910'
#date = '20241219' #First session worked 
#date = '20241220'
#date = '20250205' #NO SOUNDS
#date = '20250213'
#date = '20250217' #HIGHFREQ
#date = '20250220' 
#date = '20250225'
#date = '20250226' #IOI
date = '20250227'
#date = '20250228'
#date = '20250306'

#session = '170716' #[0.7, 0.7, 0.7]

#session = '161007' #First session worked #[-0.01, 0.035] [-0.01, 0.09] [-0.01, 0.08]
#session = '164500' #[-0.01, 0.035] [-0.01, 0.1] [-0.01, 0.07]
#session = '165243' #[-0.01, 0.005] [-0.01, 0.02] [-0.01, 0.02]

#session = '103227' #[-0.01, 0.03] [-0.01, 0.06] [-0.01, 0.06]
#session = '104515' #[-0.01, 0.02] [-0.01, 0.055] [-0.01, 0.055]
#session = '105023' #[-0.01, 0.025] [-0.01, 0.035] [-0.01, 0.035]
#session = '110259' #[-0.01, 0.06] [-0.01, 0.05]
#session = '111157' #[-0.01, 0.05] [-0.01, 0.03]

#session = '131832' #NO SOUNDS[-0.01, 0.02] [-0.01, 0.02] [-0.01, 0.01] 
#session = '132511' #[-0.01, 0.03] [-0.01, 0.09] [-0.01, 0.01]
#session = '133846' #[-0.01, 0.01] [-0.01, 0.05] [-0.01, 0.01] 
#session = '134526' #[-0.01, 0.018] [-0.01, 0.05] [-0.01, 0.01] 

#session = '134215' #[-0.01, 0.027] [-0.01, 0.035] [-0.01, 0.005]
#session = '141326' #[-0.01, 0.007] [-0.01, 0.03] [-0.01, 0.005]
#session = '142417' #No am_tuning
#session = '143105' #No am_tuning
#session = '145445' #[-0.01, 0.005] [-0.01, 0.015] [-0.01, 0.005]
#session = '150145' #[-0.01, 0.012] [-0.01, 0.025] [-0.01, 0.008]
#session = '154543' #[-0.01, 0.008] [-0.01, 0.045] [-0.01, 0.008]
#session = '155143' #[-0.01, 0.008] [-0.01, 0.03] [-0.01, 0.012]
#session = '160014' #[-0.01, 0.015] [-0.01, 0.015] [-0.01, 0.01]
#session = '160650' #[-0.01, 0.007] [-0.01, 0.03] [-0.01, 0.01]
#session = '161543' #[-0.01, 0.027] [-0.01, 0.03] [-0.01, 0.009]

#session = '155506' #[-0.01, 0.05] [-0.01, 0.048] [-0.01, 0.05] Very good results
#session = '160230' #[-0.01, 0.03] [-0.01, 0.039] [-0.01, 0.027]
#session = '160909' #~~ Bad session. I don't see anything.
#session = '161625' #[-0.01, 0.013] [-0.01, 0.023]] [-0.01, 0.014]
#session = '162510' #[-0.01, 0.05] [-0.01, 0.05] [-0.01, 0.02] [-0.01, 0.005] No activity in 32 kHz
#session = '163056' #[-0.01, 0.08] [-0.01, 0.08] [-0.01, 0.08] [-0.01, 0.08] Weird session. No activity in any of the frequencies.
#session = '164311' #[-0.01, 0.35] [-0.01, 0.035] [-0.01, 0.03] [-0.01, 0.005] No activity in 32kHz HIGHFREQ
#session = '164855' #[-0.01, 0.035] [-0.01, 0.04] [-0.01, 0.015] No activity in 32 kHz


#session = '112345' #[-0.01, 0.03] [-0.01, 0.07]] [-0.01, 0.01] #No activity in 32kHz #Last where I can see the 3 spots with PureTones
#session = '115716' #[-0.01, 0.03] [-0.01, 0.049]] [-0.01, 0.01] #No clear spots, but there are differences in activity for 30kHz 
#session = '120527' #[-0.01, 0.025] [-0.01, 0.049] [-0.01, 0.01] #No clear spots in 30 kHz
#session = '121116' #[-0.01, 0.015] [-0.01, 0.04] [-0.01, 0.01] #Cannot differentite the 3 spots in 3 kHz.
#session = '121744' #[-0.01, 0.01] [-0.01, 0.033] [-0.01, 0.015]
#session = '122453' #[-0.01, 0.02] [-0.01, 0.05] [-0.01, 0.009] 

#session = '120544' #[-0.01, 0.02] [-0.01, 0.08] [-0.01, 0.01]
#session = '121651' #[-0.01, 0.025] [-0.01, 0.042] [-0.01, 0.01]
#session = '122913'

#session = '165509'

#session = '143908' # No activity -- 65 dB --
#session = '145322' #[-0.01, 0.014] [-0.01, 0.045] [-0.01, 0.014] # -- 65 dB -- No 3 spots but 2, no HF activity
#session = '150110' #[-0.01, 0.007] [-0.01, 0.03] [-0.01, 0.007] # -- 65 dB -- No 3 spots but 2, no HF activity
#session = '150718' # -- 65 dB -- #[-0.01, 0.0072] [-0.01, 0.035] [-0.01, 0.005] -- Good medium frequency only
#session = '160827' #[-0.01, 0.019] [-0.01, 0.03]] [-0.01, 0.028] # -- 70 dB -- #2 main spots too
#session = '162215' #[-0.01, 0.013] [-0.01, 0.05]] [-0.01, 0.023] # -- 70 dB -- #First spot not clear, others very good
session = '162815' #Very good high frequency #[-0.01, 0.011] [-0.01, 0.03]] [-0.01, 0.01] # -- 70 dB --
#session = '163358' #[-0.01, 0.011] [-0.01, 0.028]] [-0.01, 0.013] #Good results, I think I have an idea of the structure of A1 # -- 70 dB --
#session = '170508' #[-0.01, 0.01] [-0.01, 0.025]] [-0.01, 0.01] # -- 70 dB --
#session = '171051' # -- 70 dB --

#session = '111715' #[-0.01, 0.04] [-0.01, 0.04]] [-0.01, 0.025] # -- 70 dB --
#session = '112308' #[-0.01, 0.013] [-0.01, 0.04]] [-0.01, 0.029] # -- 70 dB --
#session = '165438' #IOI
#session = '170044' #IOI
#session = '170941' #IOI

#session = '104131'
#session = '105548'
#session = '111612'
#session = '112930' #[-0.01, 0.005] [-0.01, 0.03]] [-0.01, 0.013]
#session = '120255'
#session = '121411' #[-0.01, 0.015] [-0.01, 0.02]] [-0.01, 0.015]
#session = '123334'
#session = '124456'
#session = '151211'
#session = '154637' #[-0.01, 0.037] [-0.01, 0.037]] [-0.01, 0.005]


#frames_filename = '/data/widefield/wifi003/20240910/wifi003_' + date + '_' + session + '_LG.tif'
#frames_filename = '/data/widefield/wifi008/20241219/wifi008_' + date + '_' + session + '_LG.tif' #First session worked
#frames_filename = '/data/widefield/wifi008/20241220/wifi008_' + date + '_' + session + '_LG.tif'
#frames_filename = '/data/widefield/wifi008/20250205/wifi008_' + date + '_' + session + '_LG.tif'
#frames_filename = '/data/widefield/wifi008/20250213/wifi008_' + date + '_' + session + '_LG.tif'
#frames_filename = '/data/widefield/wifi008/20250217/wifi008_' + date + '_' + session + '_LG.tif'
#frames_filename = '/data/widefield/wifi008/20250220/wifi008_' + date + '_' + session + '_LG.tif'
#frames_filename = '/data/widefield/wifi008/20250225/wifi008_' + date + '_' + session + '_LG.tif'
#frames_filename = '/data/widefield/wifi008/' + date + '_IOI/wifi008_' + date + '_' + session + '_LG.tif'
frames_filename = '/data/widefield/wifi008/' + date + '/wifi008_' + date + '_' + session + '_LG.tif'

n_frames_files = 1
mouse_name = frames_filename[16:23]
#timestamps_filename = '/data/widefield/wifi003/20240910/wifi003_timestamps_' + date + '_' + session + '.npz'
#timestamps_filename = '/data/widefield/wifi008/20241219/wifi008_timestamps_' + date + '_' + session + '.npz' #First session worked
#timestamps_filename = '/data/widefield/wifi008/20241220/wifi008_timestamps_' + date + '_' + session + '.npz'
#timestamps_filename = '/data/widefield/wifi008/20250205/wifi008_timestamps_' + date + '_' + session + '.npz'
#timestamps_filename = '/data/widefield/wifi008/20250213/wifi008_timestamps_' + date + '_' + session + '.npz'
#timestamps_filename = '/data/widefield/wifi008/20250217/wifi008_timestamps_' + date + '_' + session + '.npz'
#timestamps_filename = '/data/widefield/wifi008/20250220/wiifi008_timestamps_' + date + '_' + session + '.npz' #OJO, TIENE DOBLE i
#timestamps_filename = '/data/widefield/wifi008/20250225/wifi008_timestamps_' + date + '_' + session + '.npz' 
#timestamps_filename = '/data/widefield/wifi008/' + date + '_IOI/wifi008_timestamps_' + date + '_' + session + '.npz'
timestamps_filename = '/data/widefield/wifi008/' + date + '/wifi008_timestamps_' + date + '_' + session + '.npz'

#stimulus_filename = '/mnt/jarahubdata/behavior/wifi003/wifi003_am_tuning_curve_' + date + '_' + session + '.h5'
#stimulus_filename = '/mnt/jarahubdata/behavior/wifi008/wifi008_am_tuning_curve_' + date + '_' + session + '.h5'
stimulus_filename = '/data/widefield/wifi008/wifi008_am_tuning_curve_' + date + '_' + session + '.h5'
#stimulus_filename = '/mnt/jarahubdata/behavior/wifi008/wifi008_am_tuning_curve_' + date + '_' + session + '.h5'

#stimulus_filename = '/mnt/jarahubdata/behavior/test153/test153_am_tuning_curve_' + date + '.h5'

#overlap = '/home/jarauser/Downloads/test164_20250207_noduragelLG_00008.tif'

INTENSITY_SCALE = [-0.01, 0.05]#[None, None]  # [-0.05, 0.1]  # [None, None]  
#INTENSITY_SCALE = [-0.01, 0.09]  # [-0.05, 0.1]  # [None, None]  


# Define directory for cached results
save_dir = f"/data/widefield/processed_data/{mouse_name}/{date}/{session}"
os.makedirs(save_dir, exist_ok=True)

# Filenames for cached data
evoked_file = os.path.join(save_dir, "evoked.npy")
baseline_file = os.path.join(save_dir, "baseline.npy")
signal_change_file = os.path.join(save_dir, "signal_change.npy")
possible_freq_file = os.path.join(save_dir, "possible_freq.npy")
n_freq_file = os.path.join(save_dir, "n_freq.npy")

# Check if data is already processed
if os.path.exists(evoked_file) and os.path.exists(baseline_file) and os.path.exists(signal_change_file) and os.path.exists(possible_freq_file) and os.path.exists(n_freq_file ):
    avg_evoked_each_freq = np.load(evoked_file)
    avg_baseline_each_freq = np.load(baseline_file)
    signal_change_each_freq = np.load(signal_change_file)
    possible_freq = np.load(possible_freq_file)
    n_freq = np.load(n_freq_file)
    print("Loaded precomputed data.")

else:
    print("Processing data...")

    # -- Create list of TIFF files --
    frames_filenames = [frames_filename]
    suffix = '_@{0:04g}'
    for indf in range(1, n_frames_files):
        new_suffix = suffix.format(indf)
        new_filename = frames_filename.replace('.tif', new_suffix+'.tif')
        frames_filenames.append(new_filename)

    # -- Load TIFF files --    
    frames = None  # A numpy array to store all frames
    for indf, filename in enumerate(frames_filenames):    
        with tifffile.TiffFile(filename) as tif:
            chunk = tif.asarray()
            # image = tif.asarray()[0] #If I want to see a single image 
            axes = tif.series[0].axes
            if frames is None:
                frames = chunk
            else:
                frames = np.concatenate((frames, chunk), axis=0)
# print('# of frames:',len(frames)) 
# # -> 3000
# # -- See one image --
# plt.imshow(image, cmap='gray')
# plt.title('First image')
# plt.show()

#Meaasure pixels in an image
# from PIL import Image
# image = Image.open('/home/jarauser/Downloads/test164_20250207_noduragelLG_00008.tif')

# # Convert the image to a numpy array for visualization
# #image_data = image.convert('L')  # Convert to grayscale (optional)
# image_array = np.array(image)

# # Plot the image with pixel axes
# plt.imshow(image_array, cmap='gray')  # You can change the colormap
# plt.title('TIFF Image Visualization')
# plt.xlabel('Pixel X')
# plt.ylabel('Pixel Y')

# # Display the image
# plt.colorbar()  # Optional, to show the color scale if grayscale
# plt.show()


    timestamps = np.load(timestamps_filename)
    sound_onset = timestamps['ts_sound_rising']
    sound_offset = timestamps['ts_sound_falling']
    ts_frames = timestamps['ts_trigger_rising']
# print(timestamps)
# print('len timestamps: ')
# print(len(timestamps))

    # -- Load stimulus data --
    bdata = loadbehavior.BehaviorData(stimulus_filename)
    n_trials = min(len(bdata['currentFreq']), len(sound_onset))
    current_freq = bdata['currentFreq'][:n_trials]
    possible_freq = np.unique(current_freq)
    n_freq = len(possible_freq)
    trials_each_freq = behavioranalysis.find_trials_each_type(current_freq, possible_freq)

    sound_onset = sound_onset[:n_trials]

    # -- Load imaging data --
    with tifffile.TiffFile(frames_filename) as tif:
        frames = tif.asarray()
        axes = tif.series[0].axes

    if 0:
    # -- Plot timestamps --
        plt.clf()
        ms = 10
        spos = 0.2
        plt.plot(ts_frames, np.zeros(len(ts_frames)), '|', ms=ms)
        plt.plot(sound_onset, spos*np.ones(len(sound_onset)), 'r|', ms=ms)
        plt.plot(sound_offset, spos*np.ones(len(sound_offset)), 'k|', ms=ms)
        plt.yticks([0, spos], ['frame', 'sound'])
        plt.ylim([-spos, 2*spos])
        plt.xlabel('Time (s)')
        plt.legend(['frame', 'sound onset', 'sound offset'])
        plt.show()

    # -- Estimate average evoked image --
    sound_duration = np.mean(sound_offset[:len(sound_onset)]-sound_onset)
    frame_rate = 1/np.mean(np.diff(ts_frames))
    sound_duration_in_frames = int(round(sound_duration*frame_rate))
    # Find frames corresponding to evoked period
    frame_after_onset = np.searchsorted(ts_frames, sound_onset, side='left')


    #Obtaining the indices of images after a particular sound
    interest_trigger = 50   #The one that I'll use to see the images
    onset_time = sound_onset[interest_trigger]   #Find it in the list
    closer_frame = np.searchsorted(ts_frames, onset_time, side='left')  #Find the frame after the onset sound    
    before_onset = 1   #Quantity of images before the sound onset
    after_onset = sound_duration_in_frames #Quantity of images after the sound onset
    image_indices = np.arange(closer_frame - before_onset, closer_frame + after_onset) #Indices of wanted frames
    #print("Image indices for the trigger sound at index", interest_trigger, ":", image_indices) #Print the images indices 

    #Run just if I want to see the images
    # for i in image_indices:
    #     plt.imshow(frames[i], cmap='gray')
    #     plt.title('Image ' +  str(i))
    #     plt.show()

    # plt.imshow(frames[204], cmap='gray')
    # plt.title('200')
    # plt.show()

    evoked_frames_each_freq = []
    avg_evoked_each_freq = []
    avg_baseline_each_freq = []
    signal_change_each_freq = []

    plt.clf()
    fig = plt.gcf()
    axs = fig.subplots(n_freq, 3, sharex=True, sharey=True) 
    cmap = 'viridis'
    p=0
    for indf, freq in enumerate(possible_freq):
        frame_after_onset_this_freq = frame_after_onset[trials_each_freq[:, indf]] #Get the frames after the sound onset
        evoked_frames_this_freq = np.tile(frame_after_onset_this_freq, (sound_duration_in_frames, 1)) #Repeat the array N times
        evoked_frames_this_freq += np.arange(sound_duration_in_frames)[:,None] #At the end we have the 10 indices of the frames for each sound
        evoked_frames_this_freq = np.sort(evoked_frames_this_freq.ravel()) # Convert to 1 array only ordered
        evoked_frames_each_freq.append(evoked_frames_this_freq)
        
        #If the video is divided into 2 recordings I have to adjust the # of frames
        final_frames = np.searchsorted(evoked_frames_this_freq,len(frames))
        avg_evoked_this_freq = np.mean(frames[evoked_frames_this_freq[0:final_frames]], axis=0) #Frames during the sound 
        
        baseline_frames_this_freq = evoked_frames_this_freq[0:final_frames] - sound_duration_in_frames #Frames before the sound onset (10)
        avg_baseline_this_freq = np.mean(frames[baseline_frames_this_freq], axis=0)

        # -- Estimate change in fluorescence --
        signal_change = (avg_evoked_this_freq-avg_baseline_this_freq)/avg_baseline_this_freq


        avg_evoked_each_freq.append(avg_evoked_this_freq)
        avg_baseline_each_freq.append(avg_baseline_this_freq)
        signal_change_each_freq.append(signal_change)

    # Convert lists to arrays and save them
    avg_evoked_each_freq = np.array(avg_evoked_each_freq)
    avg_baseline_each_freq = np.array(avg_baseline_each_freq)
    signal_change_each_freq = np.array(signal_change_each_freq)
    n_freq = np.array(n_freq)
    possible_freq = np.array(possible_freq)

    np.save(evoked_file, avg_evoked_each_freq)
    np.save(baseline_file, avg_baseline_each_freq)
    np.save(signal_change_file, signal_change_each_freq)
    np.save(n_freq_file, n_freq)
    np.save(possible_freq_file, possible_freq)
    print("Processing complete. Results saved.")

    # ---- Plot the same graph using the loaded or computed data ----

plt.clf()
n_freq = int(n_freq) #When I save the images, I also save this variable.
fig = plt.gcf()
axs = fig.subplots(n_freq, 3, sharex=True, sharey=True) 
cmap = 'viridis'
p=0

for indf, freq in enumerate(possible_freq):
    if p==0:
        INTENSITY_SCALE = [-0.01, 0.011] #[-0.01, 0.05] [-0.01, 0.075]] [-0.01, 0.01]
    elif p==1:
        INTENSITY_SCALE = [-0.01, 0.03]
    elif p==2:
        INTENSITY_SCALE = [-0.01, 0.01]
    elif p==3:
        INTENSITY_SCALE = [-0.01, 0.006]
    elif p==4:
        INTENSITY_SCALE = [-0.01, 0.008]

    plt.sca(axs[indf, 0])
    plt.imshow(avg_evoked_each_freq[indf], cmap=cmap)
    plt.colorbar()
    plt.title(f'Evoked')
    plt.ylabel(f'{freq:g} Hz')

    plt.sca(axs[indf, 1])
    plt.imshow(avg_baseline_each_freq[indf], cmap=cmap)
    plt.colorbar()
    plt.title('Baseline')

    plt.sca(axs[indf, 2])
    plt.imshow(signal_change_each_freq[indf], cmap=cmap, vmin=INTENSITY_SCALE[0], vmax=INTENSITY_SCALE[1])
    plt.colorbar()
    plt.title('Signal change: (E-B)/B')

    fig.suptitle(f"{mouse_name} / {date} / {session}", fontsize=13)
    p += 1

plt.show()



def new_func(INTENSITY_SCALE, frames, possible_freq, n_freq, trials_each_freq, sound_duration_in_frames, frame_after_onset):
    evoked_frames_each_freq = []
    plt.clf()
    fig = plt.gcf()
    axs = fig.subplots(n_freq, 6, sharex=True, sharey=True) 
    cmap = 'viridis'
    
    frame_after_onset = np.searchsorted(ts_frames, sound_onset, side='left')

    for indf, freq in enumerate(possible_freq):
        frame_after_onset_this_freq = frame_after_onset[trials_each_freq[:, indf]]
        evoked_frames_this_freq = np.tile(frame_after_onset_this_freq, (sound_duration_in_frames, 1))
        evoked_frames_this_freq += np.arange(sound_duration_in_frames)[:, None]
        evoked_frames_this_freq = np.sort(evoked_frames_this_freq.ravel())
        evoked_frames_each_freq.append(evoked_frames_this_freq)

    # Adjust the number of frames
        final_frames = np.searchsorted(evoked_frames_this_freq, len(frames))
        print('Final frames: ', final_frames)

    # Split into set1 and set2
        set1_indices = np.arange(final_frames)[::2]
        #print(set1_indices)
        set2_indices = np.arange(final_frames)[1::2]
        #print(set2_indices)

    # Average for set1
        avg_evoked_set1 = np.mean(frames[evoked_frames_this_freq[set1_indices]], axis=0)
        #print(avg_evoked_set1)
        baseline_frames_set1 = evoked_frames_this_freq[set1_indices] - sound_duration_in_frames
        avg_baseline_set1 = np.mean(frames[baseline_frames_set1], axis=0)

    # Average for set2
        avg_evoked_set2 = np.mean(frames[evoked_frames_this_freq[set2_indices]], axis=0)
        baseline_frames_set2 = evoked_frames_this_freq[set2_indices] - sound_duration_in_frames
        avg_baseline_set2 = np.mean(frames[baseline_frames_set2], axis=0)

    # Differences
        signal_change_set1 = (avg_evoked_set1 - avg_baseline_set1) / avg_baseline_set1
        signal_change_set2 = (avg_evoked_set2 - avg_baseline_set2) / avg_baseline_set2
        difference_signal = signal_change_set1 - signal_change_set2

    # Plotting
        plt.sca(axs[indf, 0])
        plt.imshow(avg_evoked_set1, cmap=cmap)
        plt.colorbar()
        plt.title('Evoked Set 1')
        plt.ylabel(f'{freq:g} Hz\n({len(set1_indices)} trials)')

        plt.sca(axs[indf, 1])
        plt.imshow(avg_baseline_set1, cmap=cmap)
        plt.colorbar()
        plt.title('Baseline Set 1')

        plt.sca(axs[indf, 2])
        plt.imshow(signal_change_set1, cmap=cmap, vmin=INTENSITY_SCALE[0], vmax=INTENSITY_SCALE[1])
        plt.colorbar()
        plt.title('Signal change Set 1')

        plt.sca(axs[indf, 3])
        plt.imshow(avg_evoked_set2, cmap=cmap)
        plt.colorbar()
        plt.title('Evoked Set 2')

        plt.sca(axs[indf, 4])
        plt.imshow(avg_baseline_set2, cmap=cmap)
        plt.colorbar()
        plt.title('Baseline Set 2')

        plt.sca(axs[indf, 5])
        plt.imshow(signal_change_set2, cmap=cmap, vmin=INTENSITY_SCALE[0], vmax=INTENSITY_SCALE[1])
        #plt.imshow(difference_signal, cmap=cmap, vmin=INTENSITY_SCALE[0], vmax=INTENSITY_SCALE[1])
        plt.colorbar()
        plt.title('Signal change Set 2')
        #plt.title('Difference Signal Change (Set1 - Set2)')

    plt.show()

#new_func(INTENSITY_SCALE, frames, possible_freq, n_freq, trials_each_freq, sound_duration_in_frames, frame_after_onset)

