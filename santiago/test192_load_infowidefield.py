"""
Test loading widefield data using infowidefield files.
"""

import os
import glob
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import loadbehavior

subject = 'wifi003'
dataDir = settings.WIDEFIELD_PATH

infoWidefieldFile = os.path.join(settings.INFOWIDEFIELD_PATH, f'{subject}_widefield.py')

infoWidefield = celldatabase.read_inforec(infoWidefieldFile)

indSession = 0  # Index of session to load
sessionInfo = infoWidefield.sessions[indSession]
sessionDate = sessionInfo['date'].replace('-', '')
sessionTime = sessionInfo['time'].replace(':', '')
paradigm = sessionInfo['paradigm']

# -- Load the data --
frames_dir = os.path.join(dataDir, subject, sessionDate)
#frames_filename = os.path.join(frames_dir, f'{subject}_{date}_{session}_{experimenter}.tif')
frames_filenames = sorted(glob.glob(os.path.join(frames_dir, f'*{sessionTime}*.tif')))
timestamps_filename = os.path.join(frames_dir, f'{subject}_timestamps_{sessionDate}_{sessionTime}.npz')
stimulus_filename = loadbehavior.path_to_behavior_data(subject, paradigm,
                                                       f'{sessionDate}_{sessionTime}')
