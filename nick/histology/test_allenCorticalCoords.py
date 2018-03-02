import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import histologyanalysis as ha
corticalVolume = ha.AllenCorticalCoordinates()

sliceNum = 200
coords = np.array([[383, 52],
                   [398, 66],
                   [411, 81],
                   [422, 98],
                   [354, 74],
                   [370, 89],
                   [381, 105],
                   [389, 119],
                   [405, 74],
                   [400, 79],
                   [396, 84],
                   [392, 89],
                   [387, 93],
                   [382, 97],
                   [378, 100]])
coords = coords.T #Transpose to work with the way we wrote the fxn below
allDepths = corticalVolume.get_cortical_depth_many_xy(coords, sliceNum)

plt.clf()
plt.plot(allDepths)
