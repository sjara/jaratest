'''
This script is makes it easier to concatenate and kilosort data recorded from
multiple different sites in a single day. It requires three arguments and can be run as
follows: "python neuropix_sort_multidepth.py <subject> <dateStr> <probeDepths>" where
<probeDepths> is a comma delimited list of probe depths that you would like to sort. Basically,
it can be run in the same way

Example:
    python neuropix_sort_multidepth.py poni005 2025-08-15 1570,2290,3014,3013


NOTE: Since you will be running multiple instances of kilosort, keep in mind the amount of
time it will take to run! Assume each probe depth will add 1~2 hours of runtime depending on
the size of the concatenated file.
'''

import subprocess
from kilosort import run_kilosort
import jaratoolbox
from jaratoolbox import settings,loadneuropix
import os
import sys
import importlib
import numpy as np
import pandas as pd

subject = sys.argv[1]
dateStr = sys.argv[2]
probeDepths = [int(i) for i in sys.argv[3].split(',')]
debug = True if (len(sys.argv)==5 and sys.argv[4]=='debug') else False


sessionsRootPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject)
remote_dir = f'jarauser@jarastore:/data/neuropixels/{subject}/'
jaraScriptDir = os.path.join(os.path.dirname(jaratoolbox.__file__),'jaratoolbox','scripts')

# -- Load inforec file --
inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
spec = importlib.util.spec_from_file_location('inforec_module', inforecFile)
inforec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inforec)

for pdepth in probeDepths:
    multisessionRawDir = os.path.join(sessionsRootPath , f'multisession_{dateStr}_{pdepth}um_raw')
    multisessionProcessedDir = os.path.join(sessionsRootPath , f'multisession_{dateStr}_{pdepth}um_processed')
    multisessionProcessedDirBash = multisessionProcessedDir.replace('d:','/mnt/d').replace('\\','/')
    rawFilename = os.path.join(multisessionRawDir , 'multisession_continuous.dat')

    # -- Find sessions to concatenate --
    siteToProcess = None
    for experiment in inforec.experiments:
        if experiment.date in dateStr:
            for site in experiment.sites:
                if site.pdepth==pdepth:
                    probeStr = experiment.probe
                    siteToProcess = site
    if siteToProcess is None:
        print(f'Recording for {subject} on {dateStr} at {pdepth}um not found.')
        continue
    sessions = siteToProcess.session_ephys_dirs()

    if not os.path.exists(multisessionRawDir):
        subprocess.run([sys.executable,
                        os.path.join(jaraScriptDir,'neuropix_join_multiday.py'),
                        subject, dateStr, str(pdepth)])


    # -- Get probe map --
    xmlpath = os.path.join(multisessionProcessedDir , sessions[0] , 'info' , 'settings.xml')
    pmap = loadneuropix.ProbeMap(xmlpath)

    probe = {
            'chanMap': pmap.channelID,
            'xc': pmap.xpos,
            'yc': pmap.ypos,
            'kcoords': np.zeros(pmap.nActiveChannels)
        }


    # -- Run kilosort --
    settings = {'n_chan_bin': pmap.nActiveChannels}

    if not debug:
        ops, st, clu, tF, Wall, similar_templates, is_ref, est_contam_rate, kept_spikes = \
            run_kilosort(settings=settings,
                        filename=rawFilename,
                        probe_name=pmap.probeName,
                        probe=probe,
                        results_dir=multisessionProcessedDir)

        if 'win' in sys.platform:
            subprocess.run(['wsl','rsync','-av',
                        multisessionProcessedDirBash + '/{cluster_Amplitude.tsv,cluster_ContamPct.tsv,cluster_group.tsv,cluster_KSlabel.tsv,spike_clusters.npy}',
                        multisessionProcessedDirBash + '_prephy/'])

            subprocess.run(['wsl','rsync','-av',
                            multisessionProcessedDirBash + '*',
                            remote_dir])
            
        else:
            subprocess.run(['rsync','-av',
                        multisessionProcessedDir + '/{cluster_Amplitude.tsv,cluster_ContamPct.tsv,cluster_group.tsv,cluster_KSlabel.tsv,spike_clusters.npy}',
                        multisessionProcessedDir + '_prephy/'])

            subprocess.run(['rsync','-av',
                            multisessionProcessedDir + '*',
                            remote_dir])

    else:
        print(
f'''
run_kilosort(settings={settings},
                filename={rawFilename},
                probe_name={pmap.probeName},
                probe={pmap},
                results_dir={multisessionProcessedDir})
''')
        
        subprocess.run(['wsl','rsync','-av', '--dry-run',
                    multisessionProcessedDirBash + '/{cluster_Amplitude.tsv,cluster_ContamPct.tsv,cluster_group.tsv,cluster_KSlabel.tsv,spike_clusters.npy}',
                    multisessionProcessedDirBash + '_prephy/'])

        subprocess.run(['wsl','rsync','-av', '--dry-run',
                        multisessionProcessedDirBash + '*',
                        remote_dir])


