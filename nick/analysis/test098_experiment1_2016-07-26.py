import sys; sys.path.append('/home/nick/data')
import os
from inforecordings import test098_inforec as inforec
reload(inforec)
from jaratoolbox import loadopenephys
from jaratoolbox import settings
from matplotlib import pyplot as plt

tetrodes = range(1, 9)
sessions = inforec.test098.experiments[0].sites[0].sessions

for session in sessions:
    for tetrode in tetrodes:
        fullPath = session.full_ephys_path()
        fullFn = os.path.join(fullPath, 'Tetrode{}.spikes'.format(tetrode))
        dataSpikes = loadopenephys.DataSpikes(fullFn)




from jaratest.nick.database import ephysinterface
ei = ephysinterface.EphysInterface('test098', '2016-07-26', '', defaultParadigm='am_tuning_curve')

sessions = ['12-38-47', '13-06-15', '13-11-17', '13-49-09', '14-00-26', '14-10-52', '14-22-31', '14-33-16', '13-42-42', '14-52-07']

for session in sessions:
    ei.plot_array_raster(session, replace=1, tetrodes=range(1, 9))
    plt.waitforbuttonpress()
