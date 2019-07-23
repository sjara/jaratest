import os
from jaratoolbox import settings
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

muscimolSessions = ['20160413a', '20160415a', '20160417a']
salineSessions = ['20160412a', '20160414a', '20160416a']
animal = 'amod002'

muscimolData = behavioranalysis.load_many_sessions(animal, muscimolSessions)
salineData = behavioranalysis.load_many_sessions(animal, salineSessions)


