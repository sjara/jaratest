from jaratoolbox import loadbehavior
import matplotlib.pyplot as plt
import pandas as pd

def load_data (subject, session):
    paradigm = 'coop4ports' # The paradigm name is also part of the data file name
    behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
    bdata = loadbehavior.BehaviorData(behavFile)
    #print(len(bdata['outcome']))
    return bdata

subject = 'coop014x015'
bdata = load_data(subject, '20230314a')

df = pd.DataFrame({'eventCode':bdata.events['eventCode'],'eventTime':bdata.events['eventTime']})
df.replace(bdata.stateMatrix['eventsNames'], inplace=True)
df_pokes = df[df['eventCode'].isin(['S1in','S2in', "N1in", "N2in"])]
df_pokes['eventCode'].describe()