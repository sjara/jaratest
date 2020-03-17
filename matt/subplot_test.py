import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
gs = gridspec.GridSpec(2, 2)
gsx = gridspec.GridSpecFromSubplotSpec(1, 2, gs)
ax1 = plt.subplot(gs[0, 0])
ax2 = plt.subplot(gsx[0])
