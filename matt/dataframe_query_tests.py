import pandas as pd
import numpy as np
from jaratoolbox import celldatabase

df1 = celldatabase.load_hdf("/var/tmp/figuresdata/2019astrpi/direct_and_indirect_cells_with_response_changes.h5")
df2 = celldatabase.load_hdf("/var/tmp/figuresdata/2019astrpi/sorted_cell_index.h5")
newDF = pd.merge(df1, df2, on=['subject', 'tetrode', 'cluster', 'date', 'depth'])
newDF
df2.__len__()

sortedFrame = newDF.query("quality == 'yes'")
sortedFrame.__len__()
latency = sortedFrame.latency
print(np.mean(latency)*1000)
badSortedFrame = newDF.query("quality == 'no'")
badLatency = badSortedFrame.latency
print(np.mean(badLatency)*1000)
print(np.median(badLatency)*1000)
print(np.median(latency)*1000)