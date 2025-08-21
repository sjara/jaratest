"""
Prepare neuropixels data for spike-sorting multiple sessions from different days.

Example usage:
python neuropix_join_multiday.py test000 2020-01-01,2020-01-02 3440
                                 SUBJECT      DATE1,DATE2     pDEPTH

To debug (without saving anything), use:
python neuropix_join_multiday.py test000 2020-01-01,2020-01-02 3440 debug
"""

import os
import sys
from jaratoolbox import loadneuropix
from jaratoolbox import settings
import importlib
importlib.reload(loadneuropix)

scriptName = os.path.basename(__file__)

if len(sys.argv)<4:
    print('This command requires a subject, date and probe depth as arguments.\n'+
          f'Example: {scriptName} test000 2020-01-01,2020-01-02 3440')
    sys.exit()

subject = sys.argv[1]
dateStr = sys.argv[2]
pdepth = int(sys.argv[3])
debug = True if (len(sys.argv)==5 and sys.argv[4]=='debug') else False
savedat = False if (len(sys.argv)==5 and sys.argv[4]=='nodat') else True


sessionsRootPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject)
multisessionRawDir = os.path.join(sessionsRootPath, f'multisession_{dateStr}_{pdepth}um_raw')
multisessionProcessedDir = os.path.join(sessionsRootPath, f'multisession_{dateStr}_{pdepth}um_processed')
# multisessionTempDir = os.path.join(sessionsRootPath, f'multisession_{dateStr}_{pdepth}um_tmp')

# -- Load inforec file --
inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
spec = importlib.util.spec_from_file_location('inforec_module', inforecFile)
inforec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inforec)

# -- Find sessions to concatenate --
sitesToProcess = []
probeStr = []
eachDateStr = dateStr.split(',')
for experiment in inforec.experiments:
    for thisDate in eachDateStr:
        if experiment.date==thisDate:
            for site in experiment.sites:
                if site.pdepth==pdepth:
                    if experiment.probe not in probeStr:
                        probeStr.append(experiment.probe)
                    sitesToProcess.append(site)

if len(sitesToProcess)==0:
    print(f'Recording for {subject} on {dateStr} at {pdepth}um not found.')
    sys.exit()
elif len(probeStr) != 1:
    print(f'ERROR: {probeStr} contains multiple unique probes.')
    sys.exit()

probeStr = probeStr[0]
sessions = []
for siteToProcess in sitesToProcess:
    sessions.extend(siteToProcess.session_ephys_dirs())

# -- Create multisession_folders --
if debug:
    print('Running in DEBUG mode. Messages will appear, but nothing will be created/saved.')
if not os.path.isdir(multisessionRawDir):
    if not debug:
        os.mkdir(multisessionRawDir)
    print(f'Created {multisessionRawDir}')
# if not os.path.isdir(multisessionTempDir):
#     if not debug:
#         os.mkdir(multisessionTempDir)
#     print(f'Created {multisessionTempDir}')
if not os.path.isdir(multisessionProcessedDir):
    if not debug:
        os.mkdir(multisessionProcessedDir)
    print(f'Created {multisessionProcessedDir}')

if 'NPv1' in probeStr:
    probeType = 'NPv1'
elif 'NPv2' in probeStr:
    probeType = 'NPv2'
else:
    raise ValueError(f'Unknown probe type: {probeStr}. Please check your inforec file.')


sinfo = loadneuropix.concatenate_sessions(sessionsRootPath, sessions, multisessionRawDir,
                                          probe=probeType, debug=debug, savedat=savedat)

# -- Save a copy of multisession_info.csv to processed folder --
multisessionInfoFilepath = os.path.join(multisessionProcessedDir,'multisession_info.csv')
if not debug:
    sinfo.to_csv(multisessionInfoFilepath)
print(f'Saved {multisessionInfoFilepath}\n')

# -- Copy events and recording info for each session --
for oneSession in sessions:
    sessionDir = os.path.join(sessionsRootPath, oneSession)
    processedSessionSubDir = os.path.join(multisessionProcessedDir, oneSession)
    if not debug:
        try:
            os.mkdir(processedSessionSubDir)
            loadneuropix.copy_events_and_info(sessionDir, processedSessionSubDir)
        except FileExistsError:
            print(f'WARNING! {processedSessionSubDir} already exists. It was not modified.')
    else:
        print(f'DEBUG: Created {processedSessionSubDir}')
        print(f'DEBUG: Copied events and info from {sessionDir} to {processedSessionSubDir}')
