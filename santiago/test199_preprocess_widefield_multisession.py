"""
Preprocess all widefield sessions from one animal.
"""

from jaratoolbox import widefieldanalysis
from importlib import reload
reload(widefieldanalysis)

subject = 'imag028'
date = '20260220'
session = '095323'
suffix = 'WG'

# -- Preprocess a single session --
#widefieldanalysis.preprocess_widefield(subject, date, session, suffix=suffix)

# -- Preprocess all sessions from one day --
widefieldanalysis.preprocess_widefield(subject, '20260220')

# -- Preprocess all sessions from one animal --
#widefieldanalysis.preprocess_widefield(subject)

