import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt

def get_probemap(xmlfile):
    """
    @ Santiago and Jeremy
    Extracts a dictionary of channel probe positions given a neuropixels array's session data.

    Parameters:
        xmlfile (path): A filepath to neuropixels probe settings.xml (ending in /Record Node 101/settings.xml')

    Returns:
        probeMap (dict): A dictionary containing information on individual acquisition channels.
            Keys:
                'chanMap' (list): An ordered list of recorded channels for this session.
                'xc' (list): Ordered list of M channels defining each N's channel's x-position (microns).
                'yc' (list): Ordered list of M channels defining each N's channel's y-position (microns).
                'kcoords' (numpy array): Zeros array of size number of active channels.
                'n_chan' (int): Integer value indicating the number of active channels.
        probeName (str): Probe name (example: 'Neuropixels 1.0')
                
    Raises:
        ValueError: If the probe name is unrecognized.
    """

    # Parse the XML file
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    # Initialize empty lists for CHANNELS, XPOS, and YPOS
    probe = root.find('.//NP_PROBE')

    channelStr = list(probe.find('.//CHANNELS').attrib.keys())
    channelShankStr = list(probe.find('.//CHANNELS').attrib.values())
    xposStr = list(probe.find('.//ELECTRODE_XPOS').attrib.values())
    yposStr = list(probe.find('.//ELECTRODE_YPOS').attrib.values())
    xpos = [int(x) for x in xposStr]
    ypos = [int(y) for y in yposStr]
    channelID = [int(x.split('CH')[1]) for x in channelStr]
    if probe.attrib['probe_name'] not in ['Neuropixels 1.0', 'Neuropixels 2.0 - Multishank']:
        raise ValueError(f'Unknown probe name: {probe.attrib["probe_name"]}')

    nActiveChannels = len(channelID)
    kcoords = np.zeros(nActiveChannels)

    probeMap = {
        'chanMap': channelID,
        'xc': xpos,
        'yc': ypos,
        'kcoords': kcoords,
        'n_chan': nActiveChannels
    }

    probeName = probe.attrib['probe_name']

    return probeMap, probeName

def make_4xN_subplots(arr, time_lower, time_upper, nChannels, sampleRate, titles, amplitude_units = '[units]'):
    '''
    Display all figures in a 4xN subplot with a consistent color scale.

    Parameters:
        arr (np.array): A list of images of shape (# of images, height, width)
        time_lower (float): Lower bound of the time axis
        time_upper (float): Upper bound of the time axis
        nChannels (int): Number of channels
        sampleRate (float): Sampling rate
    
    Returns:
        matplotlib pyplot subplots of all images contained in the stacked array.
    '''
    num_subplots = len(arr)  # Number of subplots needed
    cols = min(num_subplots, 4)  # Maximum 4 subplots in a row
    rows = int(np.ceil(num_subplots / cols))  # Determine rows needed

    fig, axes = plt.subplots(rows, cols, figsize=(16, 2 * rows))  # Adjust figure size
    
    # Flatten axes if there's only one row to avoid indexing issues
    if rows == 1:
        axes = np.reshape(axes, (1, -1))
    
    # Compute global vmin and vmax for consistent color scaling
    vmin = np.min([np.min(img) for img in arr])
    vmax = np.max([np.max(img) for img in arr])
    
    if len(titles)!=len(arr):
        titles = [f"Figure {n}" for n in range(len(arr))]

    for idx, (pull_img, grab_title) in enumerate(zip(arr, titles)):
        row = idx // 4  # Determine row
        col = idx % 4   # Determine column

        im = axes[row, col].imshow(
            pull_img, 
            aspect='auto',
            extent=[-time_lower, time_upper, 0, nChannels],
            vmin=vmin, 
            vmax=vmax
        )
        
        axes[row, col].axvline(x=1/sampleRate, c='r')
        axes[row, col].set_title(f"{grab_title}")
        axes[row, col].set_xlabel("Time evolution (s)")
        axes[row, col].set_ylabel("Channel index")
    
    # Remove unused axes if num_subplots is less than total subplots
    for idx in range(num_subplots, rows * cols):
        fig.delaxes(axes.flatten()[idx])
    
    cbar_ax = fig.add_axes([0.92, 0.2, 0.02, 0.6])  # Position the colorbar correctly
    fig.colorbar(im, cax=cbar_ax, label=f'Amplitude ({amplitude_units})')  # Apply to all subplots

    plt.tight_layout(rect=[0, 0, 0.9, 1])  # Adjust layout to prevent overlap
    plt.show()
