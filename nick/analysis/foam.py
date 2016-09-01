import numpy as np
import os
from pandas.io.parsers import read_csv

onefile = read_csv('/home/nick/Desktop/NEW_FOL/140213.CSV', header=None)
twofile = read_csv('/home/nick/Desktop/NEW_FOL/14001.CSV', header=None)

nofoam_file='/home/nick/Desktop/NEW_FOL'
num_nofoam=len(os.listdir(nofoam_file))

nofoam_array=np.zeros([num_nofoam, 2500])

for ind, nf in enumerate(os.listdir(nofoam_file)):

    datapath=os.path.join(nofoam_file, nf)
    datafile=read_csv(datapath, header=None)

    nofoam_array[ind]=datafile[4]



foam_file='/home/nick/Desktop/FOAM'
num_foam=len(os.listdir(foam_file))

foam_array=np.zeros([num_foam, 2500])

for ind, nf in enumerate(os.listdir(foam_file)):

    datapath=os.path.join(foam_file, nf)
    datafile=read_csv(datapath, header=None)

    foam_array[ind]=datafile[4]




washout_file='/home/nick/Desktop/REMOVED'
num_washout=len(os.listdir(washout_file))

washout_array=np.zeros([num_washout, 2500])

for ind, nf in enumerate(os.listdir(washout_file)):

    datapath=os.path.join(washout_file, nf)
    datafile=read_csv(datapath, header=None)

    washout_array[ind]=datafile[4]


plot(np.var(nofoam_array, axis=0))
plot(np.var(foam_array, axis=0))
plot(np.var(washout_array, axis=0))


from scipy.signal import hilbert

hnf = hilbert(nofoam_array, axis=0)
from pyo import Server, Follower
hnfi = np.imag(hnf)
hnfi_mean=np.mean(hnfi, axis=0)


nofoam_std=np.std(nofoam_array, axis=0)
foam_std=np.std(foam_array, axis=0)
washout_std=np.std(washout_array, axis=0)

plot(nofoam_std)
plot(foam_std)
plot(washout_std)


from statsmodels.nonparametric.smoothers_lowess import lowess

smooth_nofoam=lowess(nofoam_array)
