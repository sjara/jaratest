import xml.etree.ElementTree as ET
import numpy as np

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