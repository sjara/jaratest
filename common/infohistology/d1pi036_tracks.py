'''
TODO:
- add reference to type of recording device used? e.g. tetrode vs silicon probe, probe geometry, etc.
- 'shank' is very specific to silicon probes, replace with more generic info key?
'''

subject = 'd1pi036'

tracks = [
    {'subject': subject, 'brainArea': 'LeftAstr', 'histImage': 'p2-A3-03',
     'recordingTrack': 'medialDiI', 'shank': 3, 'atlasZ': 220},

    {'subject': subject, 'brainArea': 'RightAstr', 'histImage': 'p1-D6-02',
     'recordingTrack': 'posteriorDiD', 'shank': 1, 'atlasZ': 256},

    {'subject': subject, 'brainArea': 'RightAstr', 'histImage': 'p1-D6-02',
     'recordingTrack': 'posteriorDiD', 'shank': 3, 'atlasZ': 256},
    ]
