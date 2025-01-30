"""
Extract a channel map from an Open Ephys settings.xml file.

<NP_PROBE slot="2">
    <CHANNELS CH192="0:0" CH193="0:0"/>
    <ELECTRODE_XPOS CH192="8" CH193="40"/>
    <ELECTRODE_YPOS CH192="720" CH193="720"/>
</NP_PROBE>

See also:
https://github.com/MouseLand/Kilosort/issues/622
https://github.com/jenniferColonell/SGLXMetaToCoords/blob/main/SGLXMetaToCoords.py

"""

import sys
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path

SAVE_PROBE = False

#xmlfile = '/data/neuropixels/test143/2024-07-19_18-12-36/Record Node 101/settings.xml'
xmlfile = '/data/neuropixels/feat018_raw/2024-06-14_11-20-22/Record Node 101/settings.xml'

# Parse the XML file
tree = ET.parse(xmlfile)
root = tree.getroot()

# Initialize empty lists for CHANNELS, XPOS, and YPOS
channels = []
x_positions = []
y_positions = []


probe = root.find('.//NP_PROBE')

channelStr = list(probe.find('.//CHANNELS').attrib.keys())
channelShankStr = list(probe.find('.//CHANNELS').attrib.values())
xposStr = list(probe.find('.//ELECTRODE_XPOS').attrib.values())
yposStr = list(probe.find('.//ELECTRODE_YPOS').attrib.values())
xpos = [int(x) for x in xposStr]
ypos = [int(y) for y in yposStr]
channelID = [int(x.split('CH')[1]) for x in channelStr]
if probe.attrib['probe_name'] == 'Neuropixels 1.0':
    channelShank = np.zeros(len(channelID))
elif probe.attrib['probe_name'] == 'Neuropixels 2.0 - Multishank':
    channelShank = [int(x.split(':')[1]) for x in channelShankStr]
else:
    raise ValueError(f'Unknown probe name: {probe.attrib["probe_name"]}')

# === DEBUG ===
# This part is for debugging
#dframe = pd.DataFrame({'channelID': channelID, 'channelShank': channelShank, 'xpos': xpos, 'ypos': ypos})
#dframe[236:246]
# === DEBUG ===
#probe = pd.DataFrame({'chanMap': channelID, 'xc': xpos, 'yc': ypos})


nActiveChannels = len(channelID)
kcoords = np.zeros(nActiveChannels)

probeMap = {
    'chanMap': channelID,
    'xc': xpos,
    'yc': ypos,
    'kcoords': kcoords,
    'n_chan': nActiveChannels
}

plt.clf()
textOffset = 2
plt.plot(probeMap['xc'], probeMap['yc'], 'o', mfc='none')
for indc, chanID in enumerate(probeMap['chanMap']):
    plt.text(probeMap['xc'][indc]+textOffset,
             probeMap['yc'][indc], '  '+str(channelID[indc]), fontsize=6, ha='left')
plt.axis('equal')
plt.show()


# From kilosort4/lib/python3.10/site-packages/kilosort/io.py
def save_probe(probe_dict, filepath):
    """Save a probe dictionary to a .json text file.

    Parameters
    ----------
    probe_dict : dict
        A dictionary containing probe information in the format expected by
        Kilosort4, with keys 'chanMap', 'xc', 'yc', and 'kcoords'.
    filepath : str or pathlib.Path
        Location where .json file should be stored.

    Raises
    ------
    RuntimeWarning
        If filepath does not end in '.json'
    
    """

    if Path(filepath).suffix != '.json':
        raise RuntimeWarning(
            'Saving json probe to a file whose suffix is not .json. '
            'kilosort.io.load_probe will not recognize this file.' 
        )

    d = probe_dict.copy()
    # Convert arrays to lists, since arrays aren't json-able
    for k in list(d.keys()):
        v = d[k]
        if isinstance(v, np.ndarray):
            d[k] = v.tolist()
    
    with open(filepath, 'w') as f:
        f.write(json.dumps(d))


output_file = '/tmp/probe_NP2_AllShanks96.json'        
if SAVE_PROBE:
    print(f'Saving probe map to {output_file}')
    save_probe(probeMap, output_file)


