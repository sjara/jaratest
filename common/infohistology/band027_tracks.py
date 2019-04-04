'''
TODO:
- add reference to type of recording device used? e.g. tetrode vs silicon probe, probe geometry, etc.
- 'shank' is very specific to silicon probes, replace with more generic info key?
'''

subject = 'band015'

tracks = [
    {'subject':subject, 'brainArea':'LeftAC', 'histImage':'p2-A2-02',
     'recordingTrack':'posteriormedialDiD', 'shank':4, 'atlasZ':214},

    {'subject':subject, 'brainArea':'LeftAC', 'histImage':'p2-B1-02',
     'recordingTrack':'medialDiI', 'shank':4, 'atlasZ':228},

    {'subject':subject, 'brainArea':'LeftAC', 'histImage':'p2-B2-02',
     'recordingTrack':'middleDiD', 'shank':4, 'atlasZ':231},

    {'subject': subject, 'brainArea': 'LeftAC', 'histImage': 'p2-B2-02',
     'recordingTrack': 'posteriormedialDiD', 'shank': 2, 'atlasZ': 231},

    {'subject': subject, 'brainArea': 'LeftAC', 'histImage': 'p2-B4-02',
     'recordingTrack': 'medialDiI', 'shank': 3, 'atlasZ': 234},

    {'subject': subject, 'brainArea': 'LeftAC', 'histImage': 'p2-B6-02',
     'recordingTrack': 'middleDiD', 'shank': 3, 'atlasZ': 238},