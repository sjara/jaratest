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
    """__summary__:
        This function is used to load behavior data from social cooperation project

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

def for_stage_1(bdata):
    time = list()
    count = 0
    for i in bdata['outcome']:
        if i in [1,2,3]:
            count += 3
        count+=3
        time.append(count)
    return time

# Paso 1: I need to accumulate all data taking into account that I started recording the time since 20230313a and
# only the time of stage 1 can be estimated
def merge_data(start_subject, number_of_mice, start_date, end_date):
    """_summary_:
    This function is used to merge all the behavior data we want from cosial cooperatio project into one dataframe

    Args:
        start_subject (str): Store the numbers of the first pair of mice we want to start collecting data.
        number_of_mice (int): Store the amount of mice we want to collect data. So, we start iterating number_of_mice mices from start_subject.
        start_date (datetime.date): Store the first date we want to collect the data.
        end_date (datetime.date): Store the last date we want to collect the data.

    Returns:
        pandas.Dataframe: All collected data returned into one Dataframe
    """
    # Empty dataframe defining the fields will need
    df_all_data = pd.DataFrame(
        columns=["Outcome", "Time", "BarrierType", "Date", "MiceID"]
    )
    # Break down the tuple to handle each number separetaly
    mouse1, mouse2 = start_subject

    # Upload a dataframe for each pair of mice and date 
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
                    "Time": for_stage_1(bdata)
                        #bdata["timeTrialStart"]
                        ,
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
    number_of_mice=2,
    start_date=date(2023, 2, 28),
    end_date=date(2023, 3, 3),
)

# Paso 2: I need to group all data by barrier > mice id
data.set_index(keys=["BarrierType", "MiceID"], inplace=True)
data_only_successful = data[data["Outcome"] == 1]
data_only_successful_grouped = data_only_successful.groupby(
    by=[
        "BarrierType",
        "MiceID",
        pd.cut(data_only_successful["Time"], bins=3, #labels=["0-20","20-40","40-60"]
            )
    ]
)["Outcome"].count()

# Paso 3: Creation of bar charts
# paso 4: Compile all in a function to plot both barriers
def barplot_accu_rewards_time(data):
    """_summary_:
    This function is used to create axes for each barrier,
    each axes will show bars representing the accumulated rewards for each pair of mice on time.
    In turn, accumulated rewards will be segmented in as many bars as the user want. The default will be 3,
    wich means that for a 60 minute assay, accumulated rewards will be calculated every 20 minutes.

    Args:
        data (pandas.dataframe): Dataframe containing minimun
    """

    fig, ax = plt.subplots(layout="constrained", nrows=2)
    fig.suptitle(f"Accumulated rewards on time per mice")
    times = data.index.levels[2]
    x_pos = np.arange(len(times))
    print(x_pos)
    mice_ids = data.index.levels[1]
    print(mice_ids)
    width = 0.25
    multiplier = 0
    print(data)
    for index, barrier in enumerate(data.index.levels[0]):
        for time in times:
            offset = width * multiplier
            bars = ax[index].bar(
                x_pos[:-1] + offset,
                data.loc[f"{barrier}", :, time].values,
                width,
                label=time,
            )
            ax[index].bar_label(bars, padding=3)
            multiplier += 1
        multiplier = 0

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax[index].set_title(f"{barrier} barrier")
        ax[index].set_ylabel("Rewards count")
        #ax[index].set_xticks(x_pos + width, mice_ids)
        ax[index].legend(loc="upper left", ncols=3)
        ax[index].set_ylim(0, 150)

barplot_accu_rewards_time(data_only_successful_grouped)
plt.show()
