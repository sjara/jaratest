from jaratoolbox import loadbehavior

subject = 'chad029'    # The name of the mouse
paradigm = 'twochoice' # The paradigm name is also part of the data file name
session = '20200317a'  # The format is usually YYYYMMDD and a short suffix
behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
bdata = loadbehavior.BehaviorData(behavFile)
