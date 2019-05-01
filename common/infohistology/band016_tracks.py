'''
TODO:
- add reference to type of recording device used? e.g. tetrode vs silicon probe, probe geometry, etc.
- 'shank' is very specific to silicon probes, replace with more generic info key?
'''

subject = 'band016'

tracks = [
    {'subject':subject, 'brainArea':'LeftAC', 'histImage':'p1-D1-03',
     'recordingTrack':'medialDiD', 'shank':1, 'atlasZ':197},

    {'subject':subject, 'brainArea':'LeftAC', 'histImage':'p1-C5-03',
     'recordingTrack':'medialDiD', 'shank':2, 'atlasZ':194},

    {'subject':subject, 'brainArea':'LeftAC', 'histImage':'p1-C1-03',
     'recordingTrack':'medialDiD', 'shank':3, 'atlasZ':188},

    {'subject': subject, 'brainArea': 'RightAC', 'histImage': 'p1-D4-02',
     'recordingTrack': 'medialDiI', 'shank': 1, 'atlasZ': 201},
]