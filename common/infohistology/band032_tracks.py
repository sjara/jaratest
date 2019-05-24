'''
TODO:
- add reference to type of recording device used? e.g. tetrode vs silicon probe, probe geometry, etc.
- 'shank' is very specific to silicon probes, replace with more generic info key?
'''

#These images are pretty zoomed in so there are not many features to compare to the atlas. A best guess was made for choosing an atlas image bassed off thalamus/hippocampus
subject = 'band032'

tracks = [
    {'subject':subject, 'brainArea':'LeftAC', 'histImage':'p1-B2-03',
     'recordingTrack':'medialDiI', 'shank':4, 'atlasZ':220},

    {'subject':subject, 'brainArea':'LeftAC', 'histImage':'p1-B3-03',
     'recordingTrack':'medialDiI', 'shank':3, 'atlasZ':222},

    {'subject':subject, 'brainArea':'LeftAC', 'histImage':'p1-B4-03',
     'recordingTrack':'medialDiI', 'shank':2, 'atlasZ':224},

    {'subject':subject, 'brainArea':'LeftAC', 'histImage':'p1-B5-03',
     'recordingTrack':'medialDiI', 'shank':1, 'atlasZ':226},

    {'subject':subject, 'brainArea':'LeftAC', 'histImage':'p1-B6-03',
     'recordingTrack':'middleDiD', 'shank':2, 'atlasZ':228},

    {'subject':subject, 'brainArea':'LeftAC', 'histImage':'p1-C1-03',
     'recordingTrack':'middleDiD', 'shank':1, 'atlasZ':230},

    {'subject':subject, 'brainArea':'RightAC', 'histImage':'p1-B2-02',
     'recordingTrack':'medialDiI', 'shank':4, 'atlasZ':220},

    {'subject':subject, 'brainArea':'RightAC', 'histImage':'p1-B4-02',
     'recordingTrack':'medialDiI', 'shank':3, 'atlasZ':224},

    {'subject':subject, 'brainArea':'RightAC', 'histImage':'p1-B6-02',
     'recordingTrack':'medialDiI', 'shank':2, 'atlasZ':228},

    {'subject':subject, 'brainArea':'RightAC', 'histImage':'p1-C2-02',
     'recordingTrack':'medialDiI', 'shank':1, 'atlasZ':232},
]
