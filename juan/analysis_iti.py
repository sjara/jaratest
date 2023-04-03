# The first approach will be to compared if a mouse sticks longer to a port if its partner is there too
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import date
from load_behavior_data import collect_events, collect_behavior_data

# pd.options.display.float_format = "{:.6f}".format

data_events = collect_events(
    start_subject=(14, 15),
    number_of_mice=1,
    start_date=date(2023, 3, 21),
    end_date=date(2023, 3, 21),
)
data_behavior = collect_behavior_data(
    start_subject=(14, 15),
    number_of_mice=1,
    start_date=date(2023, 3, 21),
    end_date=date(2023, 3, 21),
)

def filt_by_event(data_events, events):
    data_filt = data_events[data_events["Events"].isin(events)].copy()
    data_filt.drop_duplicates(subset="Event Time", inplace=True)
    data_filt.reset_index(inplace=True, names="indexOriginal")
    return data_filt

# BY NOW, THE CODE IS ONLY TAKING INTO ACCOUNT COOP014X015 IN A, PROBABLY, UNNECESSARY COMPLEX WAY,
# BUT IT IS REQUIRED, DUE TO THE NECESSITY TO DO THESE ANALYSIS ASAP.

## NOTE: ALL VARIABLES WITH _1 AND _2 SUFFIX MEAN MOUSE TRACK 1 AND MOUSE TRACK 2, RESPECTIVELY.
def get_iti(data_filt_1, data_filt_2):
    ## SAVE DATA FROM POKES ON A TRIAL
    pokes = {"N1in": [], "N2in": [], "S1in": [], "S2in": []}
    print(len(data_filt_1),len(data_filt_2))

    # mouse 1
    if len(data_filt_1):
        first_poke_1 = data_filt_1.index[0]
        for index in data_filt_1.index:
            if (index == data_filt_1.index[-1]) or (data_filt_1.at[index, "Events"] != data_filt_1.at[index + 1, "Events"]) :
                pokes[data_filt_1.at[first_poke_1, "Events"]].append(
                (round(data_filt_1.loc[index, "Event Time"]
                    - data_filt_1.loc[first_poke_1, "Event Time"],3))
                )
                first_poke_1 = index + 1
    # mouse 2
    if len(data_filt_2):
        first_poke_2 = data_filt_2.index[0] 
        for index in data_filt_2.index:
            if (index == data_filt_2.index[-1]) or (data_filt_2.at[index, "Events"] != data_filt_2.at[index + 1, "Events"]):
                pokes[data_filt_2.at[first_poke_2, "Events"]].append(
                    (round(data_filt_2.at[index, "Event Time"]
                    - data_filt_2.at[first_poke_2, "Event Time"],3))
                )
                first_poke_2 = index + 1

    iti = pd.DataFrame(pd.Series(pokes))
    iti=iti.T
    return iti

def get_pokes_on_each_trial(data_trials_events_merge):
    ## NECESITO ITERAR POR CADA TRIAL VALIDO Y SAVE POKES IN N1,S1,N2,S2 DURING A CERTAIN TRIAL
    for indexOriginal in data_trials_events_merge["indexOriginal"]:
        print(indexOriginal)
        num = indexOriginal + 1
        while data_events.at[num, "Events"] != "Forced" or (num != len(data_events)-1):
            num +=1
        else:
            data_to_get_iti = data_events.iloc[indexOriginal + 1 : num].copy()
            data_filt_1 = filt_by_event(data_to_get_iti, ["N1in", "S1in"])
            data_filt_2 = filt_by_event(data_to_get_iti, ["N2in", "S2in"])
            get_iti(data_filt_1, data_filt_2)

### I WANT TO TRY TO DETERMINE HOW MANY TIME MICE SPEND DURING PORTS WHEN THE PORT HAS ONLY ON REWARD
### ALSO I WANT TO DETERMINE I WANT TO SEE IF IS POSSIBLE TO DO THE SAME WHEN THEY TRY ON THE WRONG PORT.
data_trials = filt_by_event(data_events, ["Forced"])
data_behavior.drop_duplicates(subset="TimeTrialStart", inplace=True)
data_trials_events_merge = data_behavior.merge(
    data_trials,
    left_on=["MiceID", "Date", "TimeTrialStart"],
    right_on=["MiceID", "Date", "Event Time"],
)
data_trials_events_merge.dropna(subset=["TimeTrialStart"], inplace=True)

get_pokes_on_each_trial(data_trials_events_merge)