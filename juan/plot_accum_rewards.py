import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date
from load_behavior_data import collect_data

# Objective: Make a group of graphs to show the accumulated rewards every 20 min for each pair of mice, date and barrier

# Paso 1: I need to accumulate all data taking into account that I started recording the time since 20230313a and
# only the time of stage 1 can be estimated

data = collect_data(
    start_subject=(10, 11),
    number_of_mice=3,
    start_date=date(2023, 3, 13),
    end_date=date(2023, 3, 16),
)
# data2 = collect_data(
#     start_subject=(14, 15),
#     number_of_mice=1,
#     start_date=date(2023, 3, 5),
#     end_date=date(2023, 3, 7),
# )
# data = pd.concat([data,data2])

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

    fig, ax = plt.subplots( nrows=2,figsize=(10, 5) )
    fig.suptitle(f"Accumulated rewards on time per mice for stage 1")
    times = data.index.levels[2]
    x_pos = np.arange(len(times))
    mice_ids = data.index.levels[1]
    width = 0.25
    multiplier = 0
    for index, barrier in enumerate(data.index.levels[0]):
        for time in times:
            offset = width * multiplier
            bars = ax[index].bar(
                x_pos + offset,
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
        ax[index].set_xticks(x_pos + width, mice_ids)
        ax[index].legend(loc="upper left", ncols=3)
        ax[index].set_ylim(0, 350)

barplot_accu_rewards_time(data_only_successful_grouped)
plt.tight_layout()
plt.savefig('rewards_on_time_stage4.jpg')