'''
This example shows how to get the spikes from only one cell (after spike sorting)
'''

import allcells_test014 as allcells
from jaratoolbox import ephyscore
#reload(ephyscore)

cellInd = 3

oneCell = allcells.cellDB[cellInd]

print oneCell
print oneCell.get_filename()

spkData = ephyscore.CellData(oneCell)


