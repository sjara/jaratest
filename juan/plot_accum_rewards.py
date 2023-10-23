import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils.load_behavior_data import collect_behavior_data


def filter_and_group(bins: int, data: pd.DataFrame, sessionLen: int) -> pd.DataFrame:
    """_summary_:
    This function is used to filter the data by the outcome of a trial
    and to group the data by the number of segmentation in time desired (bins)

    Returns:
        data_filtered_grouped: Dataframe with the data filtered and grouped into
        as many segments as chose by the user
    """

    data.set_index(keys=["Date", "MiceID"], inplace=True)
    data_filtered = data[data["Outcome"] == 1]
    data_filtered_grouped = data_filtered.groupby(
        by=[
            "Date",
            "MiceID",
            pd.cut(
                data_filtered[["TimePoke2", "TimePoke1"]].fillna(0).apply(max, axis=1),
                bins=bins,
                labels=[
                    f"{int((sessionLen/bins*i)-(sessionLen/bins))}-{int(sessionLen/bins*i)}"
                    for i in range(1, bins + 1)
                ],
            ),
        ]
    )["Outcome"].count()
    return data_filtered_grouped


def barplot_accu_rewards_time(data: pd.DataFrame, num_dates:list):
    """_summary_:
    This function is used to create axes for each barrier,
    each axes will show bars representing the accumulated rewards for each pair of mice on time.
    In turn, accumulated rewards will be segmented in as many bars as the user want. The default will be 3,
    wich means that for a 60 minute assay, accumulated rewards will be calculated every 20 minutes.

    Args:
        data (pandas.dataframe): Dataframe containing minimun
    """

    fig, ax = plt.subplots(nrows=num_dates, figsize=(10, 5))
    times = data.index.levels[2]
    mice_ids = data.index.levels[1]
    x_pos = np.arange(len(mice_ids))
    width = 0.8 / len(times)
    offset = 0

    for index, barrier in enumerate(data.index.levels[0]):
        max_value = 0
        for time in times:
            bars = ax[index].bar(
                x_pos + offset,
                data.loc[f"{barrier}", :, time].values,
                width,
                label=time,
            )
            ax[index].bar_label(bars, padding=3)
            offset += width
            max_value = (
                max(data.loc[f"{barrier}", :, time].values)
                if max(data.loc[f"{barrier}", :, time].values) > max_value
                else max_value
            )
        offset = 0

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax[index].set_title(f"Date: {barrier}")
        ax[index].set_ylabel("Trials count")
        ax[index].set_xticks(x_pos + (width * len(times) - width) / 2, mice_ids)
        ax[index].legend(loc="upper left", ncols=len(times) / 2)
        ax[index].set_ylim(0, max_value + 100)
        ax[index].set_yticks(np.arange(0, max_value + 1, max_value))


if __name__ == "__main__":
    ## DATA COLLECTION
    data = collect_behavior_data(
        mice_data={"coop026x027": [("2023-08-15", "2023-08-18")]}
    )
    ## RUN
    data_filtered_grouped = filter_and_group(bins=3, data=data, sessionLen=60)
    
    barplot_accu_rewards_time(data_filtered_grouped, len(data.index.get_level_values(0).unique().tolist()))

    # ## SHOW PLOT
    plt.tight_layout()
    plt.show()
    # plt.savefig('trials_on_time_stage4.jpg')
