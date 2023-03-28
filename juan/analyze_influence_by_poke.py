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

## PARA JUPYTER

# The first approach will be to compared if a mouse sticks longer to a port if its partner is there too
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from load_behavior_data import collect_events, load_data
#%cd ../..
#data = load_data("coop010x011", "20230319a")
data_events = collect_events(
        start_subject=(14, 15),
        number_of_mice=1,
        start_date=date(2023, 3, 21),
        end_date=date(2023, 3, 26),
    )
data_events

# Categorical scatter plot for stage 4 coop014x015
# This to observed if data is enough to start stadistical analysis, not only in quantity, but quality (are they sufficently separated?)
# fig, ax = plt.subplots()
# ax.scatter(x=data["BarrierType"],y=data['Percent reward'],c=(data['BarrierType']=="solid").apply(lambda x:int(x)))
# ax.hlines(y=[int(data.loc[data['BarrierType']=='perforated','Percent reward'].mean()),
#             int(data.loc[data['BarrierType']=='solid','Percent reward'].mean())],xmin=0,xmax=1,colors=['purple','yellow'])

data_events
data_filt = data_events[
    data_events["Events"]
    .isin(["N1in", "S1in"])
]
data_filt

time1 = list()
index =list(data_filt.index)
last_first = ''
for i in range(0, len(index)-2):
    if data_filt.loc[index[i],"Events"] != data_filt.loc[index[i+1],"Events"]:
        time1.append(int( data_filt.loc[index[i+1],"Event Time"]- data_filt.loc[index[i],'Event Time']))
print(time1)