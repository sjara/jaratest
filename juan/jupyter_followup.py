# from jaratoolbox import loadbehavior
# import matplotlib.pyplot as plt
# import pandas as pd

# def load_data (subject, session):
#     paradigm = 'coop4ports' # The paradigm name is also part of the data file name
#     behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
#     bdata = loadbehavior.BehaviorData(behavFile)
#     #print(len(bdata['outcome']))
#     return bdata

# subject = 'coop014x015'
# bdata = load_data(subject, '20230314a')

#### PARA JUPYTER #####

# The first approach will be to compared if a mouse sticks longer to a port if its partner is there too
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import date
from load_behavior_data import collect_events, collect_behavior_data

#pd.options.display.float_format = "{:.6f}".format

data_events = collect_events(
    start_subject=(14, 15),
    number_of_mice=1,
    start_date=date(2023, 3, 21),
    end_date=date(2023, 3, 26),
)
data_behavior = collect_behavior_data(
    start_subject=(14, 15),
    number_of_mice=1,
    start_date=date(2023, 3, 21),
    end_date=date(2023, 3, 26),
)



####

# Categorical scatter plot for stage 4 coop014x015
# This to observed if data is enough to start stadistical analysis, not only in quantity, but quality (are they sufficently separated?)
# fig, ax = plt.subplots()
# ax.scatter(x=data["BarrierType"],y=data['Percent rewarded'],c=(data['BarrierType']=="solid").apply(lambda x:int(x)))
# ax.hlines(y=[int(data.loc[data['BarrierType']=='perforated','Percent rewarded'].mean()),
#             int(data.loc[data['BarrierType']=='solid','Percent rewarded'].mean())],xmin=0,xmax=1,colors=['purple','yellow'])

####
data_filt_1 = data_events[data_events["Events"].isin(["N1in", "S1in"])]
data_filt_1.reset_index(inplace=True,names='indexOriginal')
data_filt_2 = data_events[data_events["Events"].isin(["N2in", "S2in"])]
data_filt_2.reset_index(inplace=True,names='indexOriginal')
data_trials = data_events[data_events["Events"].isin(["Forced"])]
data_filt_1

#####

# Analyzing the Wait time

- Here I am trying to determine the time it takes to move from one port to the other one.

- Of course index have to take into account that sometimes the mice do not go inmediatly to the port
Also, here a doubt arise, The average will change depending on what value I take since sometimes mice are into the task and sometimes they are not.

- However, I will check How much time elapsed between the first and second poke on successful trials.

- **So what value to take?**

* Since what I want to know is if the wait time is been enough for the changes between ports, I have to filter the data_1 only to those changes that were equivalent to go from one port to the other one, which are all values equal or lower than 1 sec. since that is the wait time set right now.

##### Conclusions

- Aparently mice are extremely fast. We can try reducing in a factor of 10 times, that is to a value of 0.1 seconds

######
#FIRST PART
# How much time elapsed between the first and second poke?

success = data_behavior[data_behavior['Outcome'] == 1].copy()
success.reset_index(inplace=True,drop=True)
success["timeBetweenPokes"] = abs(success['TimePoke1'] - success['TimePoke2'])
indexes = list()
for i in range (1, len(success.index)):
    if success.loc[i,'ActiveSide'] != success.loc[i-1,'ActiveSide']:
        indexes.append(i)
        
alternate = success.loc[indexes]
#alternate.groupby(by=['BarrierType'])['timeBetweenPokes'].describe()
alternate
data_events

#####
# BY NOW, THE CODE IS ONLY TAKING INTO ACCOUNT COOP014X015 IN A, PROBABLY, UNNECESSARY COMPLEX WAY,
# BUT IT IS REQUIRED, DUE TO THE NECESSITY TO DO THESE ANALYSIS ASAP.

## Separate the two waitTime in different variables for ease. just for now.
## NOTE: ALL VARIABLES WITH _1 AND _2 SUFFIX MEAN MOUSE TRACK 1 AND MOUSE TRACK 2, RESPECTIVELY.
def get_iti_wt(data_filt_1, data_filt_2):
    
    data_indexed_date_1 = data_filt_1.set_index("Date")
    data_indexed_date_2 = data_filt_2.set_index("Date")

    ## this is the final dataframe with all the data collected
    ## regarding with how long is it taking to the waitTime to achieve the other port
    waitTime = pd.DataFrame()

    ## this is the final dataframe with all the data collected
    ## regarding with how long waitTime spend on each port
    iti = pd.DataFrame()

    ## Iteration through dates to separate by session and therefore by treatment (barrier)
    for date in data_indexed_date_1.index.unique():
        # Mouse 1
        data_1 = data_indexed_date_1.loc[date].reset_index()
        index_curr_date_1 = data_1.index
        times_wt_curr_date_1 = list()
        times_iti_curr_date_1 = list()
        port_1 = index_curr_date_1[0]

        # Mouse 2
        data_2 = data_indexed_date_2.loc[date].reset_index()
        index_curr_date_2 = data_2.index
        times_wt_curr_date_2 = list()
        times_iti_curr_date_2 = list()
        port_2 = index_curr_date_2[0]

        # mouse 1
        for index in index_curr_date_1[:-1]:
            if data_1.loc[index, "Events"] != data_1.loc[index + 1, "Events"]:
                times_wt_curr_date_1.append(
                    data_1.loc[index + 1, "Event Time"] - data_1.loc[index, "Event Time"], #data_1.at[index, "indexOriginal"]),
                )

                times_iti_curr_date_1.append(
                    data_1.loc[index, "Event Time"] - data_1.loc[port_1, "Event Time"],
                )

                port_1 = index + 1
        

        # mouse 2
        for index in index_curr_date_2[:-1]:
            if data_2.loc[index, "Events"] != data_2.loc[index + 1, "Events"]:
                times_wt_curr_date_2.append(
                    data_2.loc[index + 1, "Event Time"] - data_2.loc[index, "Event Time"],#data_2.at[index, "indexOriginal"]),
                )
                times_iti_curr_date_2.append(
                    data_2.loc[index, "Event Time"] - data_2.loc[port_2, "Event Time"],
                )
                port_2 = index + 1

        waitTime = pd.concat(
            [
                pd.DataFrame(
                    {
                        "time": times_wt_curr_date_1,
                        "track": 1,
                        "date": date,
                        "BarrierType": data_1["BarrierType"][0],
                    }
                ),
                pd.DataFrame(
                    {
                        "time": times_wt_curr_date_2,
                        "track": 2,
                        "date": date,
                        "BarrierType": data_2["BarrierType"][0],
                    }
                ),
                waitTime,
            ]
        )
        iti = pd.concat(
            [
                pd.DataFrame(
                    {
                        "time": times_iti_curr_date_1,
                        "track": 1,
                        "date": date,
                        "BarrierType": data_1["BarrierType"][0],
                    }
                ),
                pd.DataFrame(
                    {
                        "time": times_iti_curr_date_2,
                        "track": 2,
                        "date": date,
                        "BarrierType": data_2["BarrierType"][0],
                    }
                ),
                iti,
            ]
        )

#waitTime = waitTime[waitTime['time']<=1]
#waitTime.groupby(by=['BarrierType', 'track',pd.cut(iti['time'], bins=[-1, 1, waitTime['time'].max()])])['time'].describe()
#waitTime[waitTime['time']==waitTime['time'].min()]

## BUGS PORTS IN THE SAME TRACK WITH THE SAME TIME!!
# a = waitTime[waitTime['time'].apply(lambda x:x[0] == waitTime['time'].min()[0])]
# data_events.loc[a['time'].apply(lambda x:x[1])]

######
## PLOT
violin = sns.violinplot(data=waitTime[waitTime['time']<= 0.1], x="date", y="time", hue="waitTime",split=True)
plt.yticks(np.arange(start=0,stop=0.1,step=0.1/10))

#####

# Analyzing the ITI

- Here I want to determine how long the waitTime are spending in the ports.

- This will help to know if ITI is being too short that is unsignificant.

- Mice have gotten rewards in a row. So, I need to compute in a successful trial how long mice stick there, but on succesful trials where the next port to be selected is the other port, no the same.

##### Conclusions

#####
### I WANT TO TRY TO DETERMINE HOW MANY TIME MICE SPEND DURING PORTS WHEN THE PORT HAS ONLY ON REWARD
### ALSO I WANT TO DETERMINE I WANT TO SEE IF IS POSSIBLE TO DO THE SAME WHEN THEY TRY ON THE WRONG PORT.
trials_in_events = data_events[data_events['Events'] == 'Forced'].reset_index()
alternate_in_events = trials_in_events.loc[alternate.index]
for i in alternate_in_events['index'][:1]:
    for j in range(i+1, len(data_events)):
        if data_events.at[j,'Events'] == 'Forced':
            data_to_get_iti = data_events.loc[i+1:j-1]
            print(data_to_get_iti)
            break

#####
## PLOT
violin = sns.violinplot(
    data=iti[iti["time"] <= 10], x="date", y="time", hue="track", split=True
)
plt.yticks(np.arange(start=0, stop=10, step=10 / 10))
plt.show()