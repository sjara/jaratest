import os
import itertools


CASE=1
#Count up
if CASE==0:

    passes = ['1', '2', '3']
    rows = ['a', 'b', 'c', 'd']
    cols = ['1', '2', '3', '4', '5', '6']
    chans = ['tl']

    dirToProcess = '/home/nick/data/jarahubdata/jarashare/histology/anat037/5xAC_JPEG/'
    start = [1, 'c', '2']

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

    TEST_ONLY = True #Make this True to just print the changes, not actually make them
    for indFile, fn in enumerate(filesToName):
        print "Changing {} to {}".format(fn, namesAfterStart[indFile])
        if not TEST_ONLY:
            os.rename(os.path.join(dirToProcess, fn), os.path.join(dirToProcess, namesAfterStart[indFile]))

elif CASE==1:
    #Rename one dir following another (Like jpg copies to follow tl images in czi)
    dirToProcess = '/home/nick/data/jarahubdata/jarashare/histology/anat037/5xATh_JPEG/'
    parentDir = '/home/nick/data/jarahubdata/jarashare/histology/anat037/5xATh/'
    parentChan = 'tl'

    parentFiles = sorted(os.listdir(parentDir))
    parentFilesChanFiltered = [fileName.split('.')[0] for fileName in parentFiles if parentChan in fileName]

    filesToProcess = sorted(os.listdir(dirToProcess))

    TEST_ONLY=False
    # TEST_ONLY=True
    if len(filesToProcess)==len(parentFilesChanFiltered):
        for indFile, fn in enumerate(filesToProcess):
            newFn = "{}.jpg".format(parentFilesChanFiltered[indFile])
            print "Changing {} to {}".format(fn, newFn)
            if not TEST_ONLY:
                os.rename(os.path.join(dirToProcess, fn), os.path.join(dirToProcess, newFn))

