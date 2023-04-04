# The first approach will be to compared if a mouse sticks longer to a port if its partner is there too
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import date
from load_behavior_data import collect_events, collect_behavior_data

# pd.options.display.float_format = "{:.6f}".format

data_events = collect_events(
    start_subject=(10, 11),
    number_of_mice=2,
    start_date=date(2023, 3, 30),
    end_date=date(2023, 3, 30),
)
data_behavior = collect_behavior_data(
    start_subject=(10, 11),
    number_of_mice=2,
    start_date=date(2023, 3, 30),
    end_date=date(2023, 3, 30),
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
    data_filt_1_index = data_filt_1.index
    data_filt_2_index = data_filt_2.index

    # since sometimes the last poke do not have an end it is substract with a forced event
    # mouse 1
    if len(data_filt_1_index):
        first_poke_1 = data_filt_1_index[0]
        for index in data_filt_1_index[:-1]:
            if (index + 1) == data_filt_1_index[-1]:
                pokes[data_filt_1.at[first_poke_1, "Events"]].append(
                    (
                        round(
                            data_filt_1.loc[index + 1, "Event Time"]
                            - data_filt_1.loc[first_poke_1, "Event Time"],
                            3,
                        )
                    )
                )
            elif data_filt_1.at[index, "Events"] != data_filt_1.at[index + 1, "Events"]:
                pokes[data_filt_1.at[first_poke_1, "Events"]].append(
                    (
                        round(
                            data_filt_1.loc[index, "Event Time"]
                            - data_filt_1.loc[first_poke_1, "Event Time"],
                            3,
                        )
                    )
                )
                first_poke_1 = index + 1
    # mouse 2
    if len(data_filt_2):
        first_poke_2 = data_filt_2_index[0]
        for index in data_filt_2_index[:-1]:
            if (index + 1) == data_filt_2_index[-1]:
                pokes[data_filt_2.at[first_poke_2, "Events"]].append(
                    (
                        round(
                            data_filt_2.loc[index + 1, "Event Time"]
                            - data_filt_2.loc[first_poke_2, "Event Time"],
                            3,
                        )
                    )
                )
            elif data_filt_2.at[index, "Events"] != data_filt_2.at[index + 1, "Events"]:
                pokes[data_filt_2.at[first_poke_2, "Events"]].append(
                    (
                        round(
                            data_filt_2.at[index, "Event Time"]
                            - data_filt_2.at[first_poke_2, "Event Time"],
                            3,
                        )
                    )
                )
                first_poke_2 = index + 1

    iti = pd.concat([pd.DataFrame({key: pokes[key]}) for key in pokes.keys()], axis=1)
    return iti


def get_pokes_on_each_trial(data_trials_events_merge):
    ## NECESITO ITERAR POR CADA TRIAL VALIDO Y SAVE POKES IN N1,S1,N2,S2 DURING A CERTAIN TRIAL
    df = pd.DataFrame([])
    for indexOriginal in data_trials_events_merge["indexOriginal"]:
        num = indexOriginal + 1
        while data_events.at[num, "Events"] != "Forced":
            num += 1
        else:
            data_to_get_iti = data_events.iloc[indexOriginal + 1 : num + 1].copy()
            data_filt_1 = filt_by_event(data_to_get_iti, ["N1in", "S1in", "Forced"])
            data_filt_2 = filt_by_event(data_to_get_iti, ["N2in", "S2in", "Forced"])
            data_with_iti = get_iti(data_filt_1, data_filt_2)
            data_with_iti["ActiveSide"] = data_trials_events_merge.loc[
                data_trials_events_merge["indexOriginal"] == indexOriginal, "ActiveSide"
            ].values[0]
            data_with_iti["BarrierType"] = data_trials_events_merge.loc[
                data_trials_events_merge["indexOriginal"] == indexOriginal, "BarrierType"
            ].values[0]
            data_with_iti["MideID"] = data_trials_events_merge.loc[
                data_trials_events_merge["indexOriginal"] == indexOriginal, "MiceID"
            ].values[0]
            df = pd.concat([df, data_with_iti], ignore_index=True)
    return df


### I WANT TO TRY TO DETERMINE HOW MANY TIME MICE SPEND DURING PORTS WHEN THE PORT HAS ONLY ON REWARD
### ALSO I WANT TO DETERMINE I WANT TO SEE IF IS POSSIBLE TO DO THE SAME WHEN THEY TRY ON THE WRONG PORT.
data_trials = filt_by_event(data_events, ["Forced"])
data_behavior.drop_duplicates(subset="TimeTrialStart", inplace=True)
data_trials_events_merge = data_behavior.merge(
    data_trials,
    left_on=["MiceID", "Date", "TimeTrialStart"],
    right_on=["MiceID", "Date", "Event Time"],
)

final = get_pokes_on_each_trial(data_trials_events_merge)
final
