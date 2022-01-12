import numpy as np
import pandas as pd
import h5py
from matplotlib import pyplot as plt
from jaratoolbox import settings
from jaratoolbox import behavioranalysis


# Add the subject(s)
#subject = 'bili034'
#subject = 'bili035'
subject = 'bili036'
#subject = 'bili037'
#subject = 'bili038'
#subject = 'bili039'
#subject = 'bili040'
#subject = 'bili041'
#subject = 'bili042'
#subject = ['bili034', 'bili035']

paradigm = '2afc_speech'

# Add the dates
sessions = ['20220111a', '20220112a']


bdata = behavioranalysis.load_many_sessions(subject,sessions,paradigm)

sessionID = bdata['sessionID'] 
unique_sessionID = np.unique(sessionID)
outcomeMode = bdata['outcomeMode']
sidesDirect = bdata['outcomeMode'] == bdata.labels['outcomeMode']['sides_direct']
direct = bdata['outcomeMode'] == bdata.labels['outcomeMode']['direct']

