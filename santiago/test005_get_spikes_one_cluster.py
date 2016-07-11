'''
This example shows how to get the spikes from only one cell (after spike sorting)
'''

import allcells_test030 as allcells
from jaratoolbox import loadopenephys
from jaratoolbox import ephyscore
reload(ephyscore)

cellInd = 2

oneCell = allcells.cellDB[cellInd]

print oneCell
print oneCell.get_filename()

spkData = ephyscore.CellData(oneCell)


#dataTT=loadopenephys.DataSpikes(oneCell.get_filename())
#SAMPLING_RATE=30000.0 # FIXME: Hardcoded!
#spkTimeStamps=np.array(sp.timestamps)/SAMPLING_RATE




