from jaratoolbox import loadbehavior
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date, timedelta

# subject = "coop010x011"
# paradigm = "coop4ports"  # The paradigm name is also part of the data file name
# session = "20230313a"
# behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
# bdata = loadbehavior.BehaviorData(behavFile)

# Objective: Make a group of graphs to show the accumulated rewards every 20 min for each pair of mice, date and barrier


def load_data(subject, session):
    """_summary_

    Args:
        subject (str): The name of the mouse
        session (str): The format is usually YYYYMMDD and a short suffix

    Returns:
        dict{str:np.ndarray}: Dictionary containing results of subject and session given to the function.
    """

    paradigm = "coop4ports"  # The paradigm name is also part of the data file name
    behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
    bdata = loadbehavior.BehaviorData(behavFile)
    return bdata


# Paso 1: I need to accumulate all data taking into account that I started recording the time since 20230313a and
# only the time of stage 1 can be estimated
def merge_data(start_subject, number_of_mice, start_date, end_date):
    # Empty dataframe defining the fields will need
    df_all_data = pd.DataFrame(
        columns=["Outcome", "Time", "BarrierType", "Date", "MiceID"]
    )
    # Break down the tuple to handle each number separetaly
    mouse1, mouse2 = start_subject
    for _ in range(number_of_mice):
        mice_id = f"coop0{mouse1}x0{mouse2}"
        # print(mice_id)
        for days in range(int((end_date - start_date).days) + 1):
            current_date = str(start_date + timedelta(days)).replace("-", "")
            # print(current_date)
            bdata = load_data(mice_id, f"{current_date}a")
            df = pd.DataFrame(
                {
                    "Outcome": bdata["outcome"],
                    "Time": bdata["timeTrialStart"],
                    "BarrierType": bdata["barrierType"],
                }
            )
            df["Date"] = current_date
            df["MiceID"] = mice_id
            df_all_data = pd.concat([df, df_all_data], ignore_index=True)
        mouse1 = mouse2 + 1
        mouse2 = mouse1 + 1

    df_all_data.replace({"BarrierType": bdata.labels["barrierType"]}, inplace=True)
    return df_all_data


data = merge_data(
    start_subject=(10, 11),
    number_of_mice=3,
    start_date=date(2023, 3, 13),
    end_date=date(2023, 3, 14),
)

# Paso 2: I need to group all data by barrier > mice id
data.set_index(keys=["BarrierType", "MiceID"], inplace=True)
data_1 = data[data["Outcome"] == 1]
data_1 = data_1.groupby(
    by=[
        "BarrierType",
        "MiceID",
        pd.cut(data_1["Time"], bins=3, labels=["0-20", "20-40", "40-60"]),
    ]
)["Outcome"].count()

# Paso 3: Creation of bar charts
fig, ax = plt.subplots(layout='constrained',nrows=2)
fig.suptitle(f'Accumulated rewards on time per mice')
times = data_1.loc['perforated'].reset_index().set_index('Time').drop('MiceID',axis=1).index.unique()
x_pos = np.arange(len(times))
mice_ids = data_1.loc['perforated'].index.levels[0].to_list()
width = 0.25
multiplier =0

for index, barrier in enumerate(data_1.index.levels[0]):
    
    for time in times:
        offset = width * multiplier
        bars = ax[0].bar(
            x_pos + offset,
            data_1.loc['perforated',:,time].values,
            width,
            label=time
        )
        ax[0].bar_label(bars, padding=3)
        multiplier +=1


    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax[index].set_title(f"{barrier} barrier")
    ax[index].set_ylabel('Rewards count')
    ax[index].set_xticks(x_pos + 0.25, mice_ids)
    ax[index].legend(loc='upper left', ncols=3)
    ax[index].set_ylim(0, 150)

plt.show()
