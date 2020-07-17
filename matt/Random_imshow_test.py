#%%
import matplotlib.pyplot as plt
import numpy as np

array = np.arange(30).reshape(2,15)
plt.imshow(array)
plt.axvline(1.1)
lower = np.log2(2000)
upper = np.log2(40000)
k20 = np.log2(20000)
markerValue = (k20-lower)/(upper-lower)
lineValue = markerValue*15
plt.axvline(lineValue)
plt.show()
