"""
Fix inforec by moving recording track info from 'info' to 'recordingTrack'.

Currently, it only works for files in the format that Matt has where
the info argument is in a different line from the Experiment definition.

Santiago Jaramillo
2020-03-16
"""

import re
import os

filename = '/home/spider/src/jaratest/common/inforecordings/d1pi049_inforec.py'
# outputFile = '/tmp/test_inforec.py'

with open(filename) as inFile:
    lines = inFile.read().splitlines()

trackRE = re.compile(r"(.*info=\[)'(\w*)',\s*(.*)")
experimentRE = re.compile(r".*celldatabase.Experiment.*")

for indline, mystr in enumerate(lines):
    matchedTrack = trackRE.match(mystr)
    if matchedTrack:
        recordingTrack = matchedTrack[2]
        matchedExperiment = experimentRE.match(lines[indline-1])
        if matchedExperiment:
            lines[indline-1] = matchedExperiment[0]+" '{}',".format(recordingTrack)
            lines[indline] = '    '+matchedTrack[1]+matchedTrack[3]
            print(lines[indline-1])
            print(lines[indline])
        else:
            print(indline)
            raise ValueError('Warning! could not find experiment line')
            
with open(filename,'w') as outFile:
    outFile.write('\n'.join(lines))
    print('Saved {}'.format(filename))
