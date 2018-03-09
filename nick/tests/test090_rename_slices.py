import os
import itertools

passes = ['1', '2', '3']
rows = ['a', 'b', 'c', 'd']
cols = ['1', '2', '3', '4', '5', '6']
chans = ['tl', 'r']

dirToProcess = '/home/nick/data/jarahubdata/jarashare/histology/anat040/2.5_upperRight/'
start = [1, 'a', '4']

result = []
for ps in passes:
    for rw in rows:
        for cl in cols:
            for ch in chans:
                result.append('p{}{}{}{}.czi'.format(ps, rw, cl, ch))

startInd = result.index('p{}{}{}{}.czi'.format(start[0], start[1], start[2], chans[-1]))
namesAfterStart = result[startInd+1:]
origFiles = sorted(os.listdir(dirToProcess))

#First 2 files are named to start
filesToName = origFiles[2:]

TEST_ONLY = False #Make this True to just print the changes, not actually make them
for indFile, fn in enumerate(filesToName):
    print "Changing {} to {}".format(fn, namesAfterStart[indFile])
    if not TEST_ONLY:
        os.rename(os.path.join(dirToProcess, fn), os.path.join(dirToProcess, namesAfterStart[indFile]))


