"""
Functions for loading and processing FaceMap data.
"""

import numpy as np
import matplotlib.pyplot as plt

def load_data(filepath, runchecks=False):
    """
    Loads data created in FaceMap and saves it to the dictionary 'proc_data'.  User may pass a
    'runchecks=True' argument, to ensure ROIs are placed in the correct order.  If they are not,
    they are reordered in the 'proc_data' dictionary.  'runchecks' is intended to be used on data
    where:
        - The animal is facing to the left of the frame.
        - Whisking is placed above running.
        - The area of the synchronization light ROI is smaller than the whisking ROI area.

    Args:
        filepath (str): Path to the .npy file you would like to load.
        runchecks (bool) (Optional): Boolean operator to enable checks.
    Returns:
        proc_data (dict): Data exported by FaceMap, containing types of ROIs, their locations and
        measurement values.
    """
    # Import data
    proc_data = np.load(filepath, allow_pickle=True).item()

    if runchecks == True:
        # Make lists of running and blinking ROIs with their: position (running) & area (blinking)
        running_rois = [] # Format: (iROI, ymin)
        blink_rois = [] # Format: (iROI, area, ymax)
        counter_run = 0; counter_blink=0
        for i in range(len(proc_data['rois'])):
            if proc_data['rois'][i]['rtype'] == 'running':
                running_rois.append([proc_data['rois'][i]['iROI'], np.min(proc_data['rois'][i]['yrange'])])
                counter_run = counter_run + 1
            if proc_data['rois'][i]['rtype'] == 'blink':
                span_x = np.max(proc_data['rois'][i]['xrange']) - np.min(proc_data['rois'][i]['xrange'])
                span_y = np.max(proc_data['rois'][i]['yrange']) - np.min(proc_data['rois'][i]['yrange'])
                ymax = np.max(proc_data['rois'][i]['yrange'])
                blink_rois.append([proc_data['rois'][i]['iROI'], (span_x * span_y), ymax])
                counter_blink = counter_blink + 1

        # Running: if whisking is placed above running, switch the ROIs in proc_data.
        if running_rois[0][1] > running_rois[1][1]: 
            copy = np.copy(proc_data['rois'][running_rois[0][0]])
            proc_data['rois'][running_rois[0][0]] = proc_data['rois'][running_rois[1][0]]
            proc_data['rois'][running_rois[1][0]] = copy
        
        # Blinks: Make copies
        copy0 = np.copy(proc_data['rois'][blink_rois[0][0]])
        copy1 = np.copy(proc_data['rois'][blink_rois[1][0]])
        copy2 = np.copy(proc_data['rois'][blink_rois[2][0]])
        copy_array = [copy0, copy1, copy2]
        # If the smallest area ROI isn't in pos0, put the smallest area in pos0.
        areas = [blink_rois[0][1], blink_rois[1][1], blink_rois[2][1]]
        minArea_index = np.argmin(areas, axis=0)
        if minArea_index != 0 :
            proc_data['rois'][blink_rois[0][0]] = copy_array[minArea_index]
        # If the highest ROI isn't in pos2, put the higest ROI in pos2.
        ymaxs = [blink_rois[0][2], blink_rois[1][2], blink_rois[2][2]]
        maxY_index = np.argmax(ymaxs, axis=0)
        if maxY_index != 2 :
            proc_data['rois'][blink_rois[2][0]] = copy_array[maxY_index]
        # If either of the past two checks were true, replace pos1 with whatever hasn't moved.
        if np.logical_or(minArea_index != 0, maxY_index != 2) :
            notTouched = [1, 1, 1]
            notTouched[maxY_index]=0; notTouched[minArea_index]=0
            notTouched_index = np.argmax(notTouched, axis=0)
            proc_data['rois'][blink_rois[1][0]] = copy_array[notTouched_index]

    return proc_data

def extract_pupil(proc_data):
    """
    Retrieves the pupil trace created by FaceMap and returns that trace as an np.array.

    Args:
        proc_data (dict): ROI data exported by FaceMap
    Returns:
        pupil_trace (np.array): Trace of pupil area (in pixels) as floats.
    """
    pupil = proc_data['pupil'][0]  # FaceMap exports dict inside a 1-item list, need first element.
    pupil_trace = pupil['area']
    return pupil_trace



def extract_whisking(proc_data, window_width=5):
    """
    Extracts a whisking trace from FaceMap data and turns it into an np.array.
    
    Steps include: a) taking the magnitude of the whisker movement vector and b) smoothing this
    trace by a window_width of default value 5.
    
    The window_width was chosen to combat repeated frames, which in testing videos appeared
    intermittently and lasted for 2-3 frames.  A 5-frame window was chosen to optimally smooth
    this data, and produce a continuous measure of whisking.

    Args:
        proc_data (dict): ROI data exported by FaceMap
        window_width (int): width of moving-average window in units of frames (default = 5)
    Returns:
        whisking_traceSmooth (np.array): Smoothed movement vector (in pixels) of the whisking.
        whisking_trace (np.array): Unsmoothed movement vector (in pixels) of the whisking.
    """
    whisk = proc_data['running'][0] # outputs the dx, dy offsets between frames.
    whisking_raw = np.sqrt(np.square(whisk[:,0]) + np.square(whisk[:,1])) # Convert to mvmt vector.
    whisking_smooth = np.convolve(whisking_raw, np.ones(window_width), 'same') / window_width
    return whisking_smooth, whisking_raw


def extract_running(proc_data, window_width=5):
    """
    Retrieves the running trace created by FaceMap and returns it as an np.array.
    
    Steps include a) taking the magnitude of the running movement vector and b) smoothing this
    trace by a window_width of default value 5.
    
    The window_width was chosen to combat repeated frames, which in testing videos appeared
    intermittently and lasted for 2-3 frames.  A 5-frame window was chosen to optimally smooth
    this data, and produce a continuous measure of running.

    Args:
        proc_data (dict): ROI data exported by FaceMap
        window_width (int): width of moving-average window in units of frames (default = 5)
    Returns:
        running_trace (np.array) floats: Movement vector of running (in pixels).
        running_raw (np.array) floats: Unsmoothed movement vector of the running (in pixels).
    """
    run = proc_data['running'][1]
    running_raw = np.sqrt(np.square(run[:,0]) + np.square(run[:,1])) # Convert to movement vector
    running_smooth = np.convolve(running_raw, np.ones(window_width), 'same') / window_width
    return running_smooth, running_raw


def extract_sync(proc_data,threshold = None):
    """
    Extract a boolean of the syncronizaition light in FaceMap, using a threshold set by the user.
    The threshold can be manually set using the optional argument 'threshold=True'.  If not
    passed, the user will be asked to identify a y-value threshold on a graph of the sync light.
    
    Args:
        proc_data (dict): ROI data exported by FaceMap.
        threshold (float) (Optional): Y-threshold of the light's brightness to determine
        on/off.
    Returns:
        sync_bool (np.array): A boolean array that indicates when the synchronization light was on.
        sync_timings (np.array): An array of frame timings, for when the synchronization light turned on.
        sync_trace (np.array): An array of floats that contains the raw trace from the sync light (values =
        # of non-white pixels observed in the ROI).
    """
    sync_raw = proc_data['blink'][0] #CHANGE THIS BACK to 1!!! Or, change wiki documentation.
    if threshold == None:
        # USE A THRESHOLD FROM A PLOT
#        fig = plt.figure()
#        fig.set_figwidth(18)
#        fig.set_figheight(4)
#        plt.plot(sync_raw)
#        plt.title('Click to select a y-value threshold for the Synchronization Light')
        threshold = (np.max(sync_raw) + np.min(sync_raw)) / 2
        print('Sync Threshold set: %.2f' % threshold)
#        plt.axhline(threshold, color='r')
#        plt.title('Synch light threshold set. Does this look OK? Click again to close the window')
#        plt.ginput(1)
#        plt.close(fig)
    
    threshold = (np.max(sync_raw) + np.min(sync_raw)) / 2
    sync_bool = sync_raw < threshold # Trigger when it is below threshold
    sync_bool = np.diff(sync_bool, prepend=0) # Only sudden changes (threshold crosses)
    sync_bool = (sync_bool==1) # Only when it's turning on (discard off)
    sync_timings = np.flatnonzero(sync_bool==1)
    
    return sync_bool, sync_timings, sync_raw, threshold
    # Add to return: Timings, threshold
    # Remove from return: Boolean



def extract_groom(proc_data, threshold = None):

    """
    Extract a boolean of grooming behavior in FaceMap, using a threshold set by the user.
    The threshold can be manually set using the optional argument 'threshold=True'.  If not
    passed, the user will be asked to identify a y-value threshold on a plot of the grooming.

    Args:
        proc_data (dict): ROI data exported by FaceMap.
        threshold (float) (Optional): Y-threshold of the grooming output, to determine where
        grooming is occuring.
    Returns:
        groom_bool (np.array): A boolean array that indicates when the animal was grooming.
        groom_trace (np.array): An array of floats that gives the raw trace of grooming.
        Values = the # of non-white pixels observed in the ROI.
    """

    groom_trace = proc_data['blink'][2]
    if threshold == None:
        # USE A THRESHOLD FROM A PLOT
        fig = plt.figure()
        fig.set_figwidth(18)
        fig.set_figheight(4)    
        plt.plot(groom_trace)
        plt.ylim((0,np.max(groom_trace)+1000))
        plt.title('Click to select a y-value threshold for grooming')
        threshold = plt.ginput(1)[0][1]
        print('Groom Threshold set: %.2f' % threshold)
        plt.axhline(threshold, color='r')
        plt.title('Threshold set. Click again to close the window')
        plt.ginput(1)
        plt.close(fig)
    groom_bool = groom_trace < threshold
    return groom_bool, groom_trace, threshold



def extract_blink(proc_data, threshold = None):

    """
    Extract a boolean of eye blinking behavior in FaceMap, using a threshold set by the user.
    The threshold can be manually set using the optional argument 'threshold = True'.  If not
    passed, the user will be asked to identify a y-value threshold on a plot of the blinking.

    Args:
        proc_data (dict): ROI data exported by FaceMap.
        threshold (float) (Optional): Y-threshold of the blinking output, to determine where
        blinks are occuring.
    Returns:
        blink_bool (np.array): A boolean array that indicates when the animal was blinking.
        blink_trace (np.array): An array of floats that gives the size of the visible eye,
        in pixels.
    """

    blink_trace = proc_data['blink'][1] ## CHANGE THIS BACK TO 0!! Or, change wiki documentation.
    if threshold == None:
        # USE A THRESHOLD FROM A PLOT
        fig = plt.figure()
        fig.set_figwidth(18)
        fig.set_figheight(4)        
        plt.plot(blink_trace)
        plt.ylim((0,np.max(blink_trace)+1000))
        plt.title('Click to select a y-value threshold for blinking')
        threshold = plt.ginput(1)[0][1]
        print('Blink Threshold set: %.2f' % threshold)
        plt.axhline(threshold, color='r')
        plt.title('Threshold set. Click again to close the window')
        plt.ginput(1)
        plt.close(fig)
    blink_bool = blink_trace < threshold
    return blink_bool, blink_trace, threshold




