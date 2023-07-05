import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from datetime import date
from load_behavior_data import collect_behavior_data

all_data = pd.DataFrame([])
# data_behavior_comp = collect_behavior_data(
#     start_subject=(10, 11),
#     number_of_mice=3,
#     start_date=date(2023, 3, 21),
#     end_date=date(2023, 3, 30),
# )

# data_behavior = collect_behavior_data(
#     start_subject=(12, 13),
#     number_of_mice=1,
#     start_date=date(2023, 5, 4),
#     end_date=date(2023, 5, 15),
# )
# data_behavior.loc[data_behavior["Date"] == "20230515", "BarrierType"] = "solid"
# data_behavior_2 = collect_behavior_data(
#     start_subject=(14, 15),
#     number_of_mice=1,
#     start_date=date(2023, 5, 11),
#     end_date=date(2023, 6, 16),
# )
# data_behavior_2.loc[data_behavior_2["Date"] == "20230512", "BarrierType"] = "solid"
# data_behavior_2 = data_behavior_2[(data_behavior_2['Date'] < "20230517") | (data_behavior_2['Date'] > "20230604")]

data_behavior_3 = collect_behavior_data(
    start_subject=(16, 17),
    number_of_mice=1,
    start_date=date(2023, 5, 12),
    end_date=date(2023, 6, 16),
)
data_behavior_3 = data_behavior_3[
    (data_behavior_3["Date"] < "20230518") | (data_behavior_3["Date"] > "20230604")
]

# data_behavior_4 = collect_behavior_data(
#     start_subject=(18, 19),
#     number_of_mice=1,
#     start_date=date(2023, 5, 8),
#     end_date=date(2023, 5, 19),
# )
# all_data = pd.concat(
#     [data_behavior, data_behavior_2, data_behavior_3, data_behavior_4, all_data], ignore_index=True
# )


def barplot_accu_rewards_time(data: pd.DataFrame):
    """_summary_:
    This function will create axes for each barrier,
    each axes will show bars representing the accumulated rewards for each pair of mice on time.
    In turn, accumulated rewards will be segmented in as many bars as the user want. The default will be 3,
    wich means that for a 60 minute assay, accumulated rewards will be calculated every 20 minutes.

    Args:
        data (pandas.dataframe): Dataframe grouped by 3 columns:
            BarrierType, MiceID and ranges of numerical values (time).
        This dataframe is returned by load_behavior_data.py.filter_and_group
    """

    fig, ax = plt.subplots(nrows=2, figsize=(10, 5))
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
        ax[index].set_title(f"{barrier} barrier")
        ax[index].set_ylabel("Trials count")
        ax[index].set_xticks(x_pos + (width * len(times) - width) / 2, mice_ids)
        ax[index].legend(loc="upper left", ncols=len(times) / 2)
        ax[index].set_ylim(0, max_value + 1000)


def pct_rewarded_trials(
    data_behavior: pd.DataFrame, colors: list[str] = ["red", "blue"], width_lines=0.1
):
    """_summary_:
    This categorical scatter plot is for analyze the percentage of regarded trials against barriers
    So, for each pair of mice is going to plot a graph with the percentage of rewarded trials for each barrier.

    Args:
        data_behavior (pd.DataFrame): Pandas dataframe with at least 3 columns: BarrierType, Percent rewarded and MiceID
        colors (list[str], optional): List of colors in string type to distinguish points from each barrier. Defaults to ["red", "cyan"].
        width_lines (float, optional): Float type to set the long of the line representing the mean of the points in each barrier. Defaults to 0.1.
    """

    # FIXME: Right now the code plot organizing the dataframes by the barriertype name. This has to be corrected.
    # It is easy to make wrong plots if the isolated and non-isolated barriers do not follow an alphabetical order where isolated are together and same for non-isolated.

    width_lines = width_lines
    miceIds = data_behavior["MiceID"].unique()
    number_of_mice = len(miceIds)
    fig, ax = plt.subplots(1, number_of_mice, sharey=True)

    # Depending on the number of mice we will get list of axes of just one ax.
    # When subplots = (1,1). ax takes only 1 value.
    if number_of_mice > 1:
        for i in range(number_of_mice):
            data_one_pair_mice = data_behavior.loc[
                (data_behavior["MiceID"] == (miceIds[i]))
            ]
            data_one_pair_mice.sort_values(["BarrierType"], inplace=True)
            ax[i].scatter(
                x=data_one_pair_mice["BarrierType"],
                y=data_one_pair_mice["Percent rewarded"],
                c=(data_one_pair_mice["BarrierType"]).apply(
                    lambda x: colors[0] if x == "solid" else colors[1]
                ),
            )
            # This is for getting the positions of the x sticks in order to determine the limites of the lines to plot the mean
            locs = plt.xticks()

            # Horizontal line to represent mean of points of both barriers
            ax[i].hlines(
                y=[
                    int(
                        data_one_pair_mice.loc[
                            (
                                data_one_pair_mice["BarrierType"].isin(
                                    ["perforated", "no_barrier"]
                                )
                            ),
                            "Percent rewarded",
                        ].mean()
                    ),
                    int(
                        data_one_pair_mice.loc[
                            (data_one_pair_mice["BarrierType"] == "solid"),
                            "Percent rewarded",
                        ].mean()
                    ),
                ],
                xmin=[locs[0][0] - width_lines, locs[0][-1] - width_lines],
                xmax=[locs[0][0] + width_lines, locs[0][-1] + width_lines],
                colors=colors[::-1],
            )

            ax[i].set_xlabel(data_behavior["MiceID"].unique()[i])
            ax[i].set_ylabel("Percentage of rewarded trials")

    else:
        data_behavior.sort_values(["BarrierType"], inplace=True)
        ax.scatter(
            x=data_behavior["BarrierType"],
            y=data_behavior["Percent rewarded"],
            c=(data_behavior["BarrierType"]).apply(
                lambda x: colors[0] if x == "solid" else colors[1]
            ),
        )
        # This is for getting the positions of the x sticks in order to determine the limits of the lines to plot the mean
        locs = plt.xticks()

        # Horizontal line to represent mean of points of both barriers
        ax.hlines(
            y=[
                int(
                    data_behavior.loc[
                        data_behavior["BarrierType"] == "solid", "Percent rewarded"
                    ].mean()
                ),
                int(
                    data_behavior.loc[
                        data_behavior["BarrierType"].isin(["perforated", "no_barrier"]),
                        "Percent rewarded",
                    ].mean()
                ),
            ],
            xmin=[locs[0][0] - width_lines, locs[0][-1] - width_lines],
            xmax=[locs[0][0] + width_lines, locs[0][-1] + width_lines],
            colors=colors[::-1],
        )

        ax.set_xlabel(data_behavior["MiceID"].unique()[0])
        ax.set_ylabel("Percentage of rewarded trials")
        ax.set_xlim(-1, 2)

    plt.tight_layout()
    # plt.title("Percentage of rewarded trial per each treatment")
    plt.show()


def rewarded_trials(
    data_behavior: pd.DataFrame,
    outcome: list[int] = [1],
    colors: list[str] = ["red", "blue"],
    width_lines=0.1,
):
    """_summary_:
    This categorical scatter plot is for analyze the number of trials between different barriers. The developer can filter by the outcome of preference.
    0 = total of trials, 1 = both mice pokes, 2=only track 1 mouse poke, 3= only track 2 mouse poke and 4 = None.
    So, for each pair of mice is going to plot a graph with the trials for each barrier.

    Args:
        data_behavior (pd.DataFrame): Pandas dataframe with at least 3 columns: BarrierType, MiceID, Outcome and Date.
        colors (list[str], optional): Distinguish points from each barrier. Defaults to ["red", "cyan"].
        width_lines (float, optional): Set the long of the line representing the mean of the points in each barrier. Defaults to 0.1.
        outcome (list[int], optional): Filter the dataframe by the desired outcome to plot. Defaults to 1.
    """

    width_lines = width_lines
    miceIds = data_behavior["MiceID"].unique()
    number_of_mice = len(miceIds)
    fig, ax = plt.subplots(1, number_of_mice, sharey=True)

    ## Filter the dataframe by the outcome desired.
    ## This will be the dataframe used to plot. "MiceID", "BarrierType", "Date" are the columns to keep (levels=0,1,2) 
    data_behavior_by_outcome = (
        data_behavior[data_behavior["Outcome"].isin(outcome)]
        .groupby(["MiceID", "BarrierType", "Date"])["Outcome"]
        .sum()
    )
    print(data_behavior_by_outcome)

    # FIXME: Right now the code plot organizing the dataframes by the barriertype name. This has to be corrected.
    # It is easy to make wrong plots if the isolated and non-isolated barriers do not follow an alphabetical order where isolated are together and same for non-isolated.

    # Depending on the number of mice we will get list of axes of just one ax
    if number_of_mice > 1:
        for i in range(number_of_mice):
            ## select data from each pair of mice
            data_one_pair_mice = data_behavior.loc[
                (data_behavior["MiceID"] == (miceIds[i]))
            ]
            data_one_pair_mice.sort_values(["BarrierType"], inplace=True)

            ax[i].scatter(
                x=data_one_pair_mice["BarrierType"],
                y=data_one_pair_mice["Percent rewarded"],
                c=(data_one_pair_mice["BarrierType"]).apply(
                    lambda x: colors[0] if x == "solid" else colors[1]
                ),
            )
            # This is for getting the positions of the x sticks in order to determine the limites of the lines to plot the mean
            locs = plt.xticks()

            # Horizontal line to represent mean of points of both barriers
            ax[i].hlines(
                y=[
                    int(
                        data_one_pair_mice.loc[
                            (
                                data_one_pair_mice["BarrierType"].isin(
                                    ["perforated", "no_barrier"]
                                )
                            ),
                            "Percent rewarded",
                        ].mean()
                    ),
                    int(
                        data_one_pair_mice.loc[
                            (data_one_pair_mice["BarrierType"] == "solid"),
                            "Percent rewarded",
                        ].mean()
                    ),
                ],
                xmin=[locs[0][0] - width_lines, locs[0][-1] - width_lines],
                xmax=[locs[0][0] + width_lines, locs[0][-1] + width_lines],
                colors=colors[::-1],
            )

            ax[i].set_xlabel(data_behavior["MiceID"].unique()[i])
            ax[i].set_ylabel("Percentage of rewarded trials")

    else:
        ## set each point
        ax.scatter(
            x=data_behavior_by_outcome.index.get_level_values(1).to_list(),
            y=data_behavior_by_outcome.values,
            c=(data_behavior_by_outcome.index.get_level_values(1)).map(
                lambda x: colors[0] if x == "solid" else colors[1]
            ),
        )
        # This is for getting the positions of the x sticks in order to determine the limits of the lines to plot the mean
        locs = plt.xticks()
        #print("Locations in graph: ", locs)

        # Horizontal line to represent mean of points of both barriers
        ax.hlines(
            y=[
                int(data_behavior_by_outcome.loc[:, barrier].mean())
                for barrier in data_behavior_by_outcome.index.unique(1).to_list()
            ],
            xmin=[locs[0][idx] - width_lines for idx in range(0, len(data_behavior_by_outcome.index.unique(1)))],
            xmax=[locs[0][idx] + width_lines for idx in range(0, len(data_behavior_by_outcome.index.unique(1)))],
            colors=colors[::-1],
        )

        ax.set_xlabel(data_behavior_by_outcome.index.unique(0)[0])
        ax.set_ylabel("Rewarded trials")
        ax.set_xlim(locs[0][0] - 0.5, locs[0][-1] + 0.5)
        ax.set_yticks(np.arange(0,data_behavior_by_outcome.max(),10))

    plt.tight_layout()
    plt.title("Rewarded trial per mice per barrier")
    plt.show()


def violin_plot_waitTime(
    data_behavior: pd.DataFrame, outcome: list[int] = [1], figsize: tuple[int] = (15, 5)
):
    """_summary_:
    This violin plot is for analyze the waitTime
    It helps to see the distributions of how long does it take the second mouse to poke after the first mouse poked.
    The function plot the time vs pair of mice. Also, each drawing is colored by the barrier.
    The output are two plots one for those trials in which the next available side is in the oppossite side and one with all the data

    Args:
        data_behavior (pd.DataFrame): Pandas dataframe with at least 4 columns: BarrierType, TimePoke1, TimePoke2, ActiveSide, Outcome and MiceID
        outcome (list[int], optional): List of integers to define what outcomes user want to plot,
                    since the meaning of successful trial will change with the stage of training, for example, for stage 4 successfull trial
                    is only outcome = [1], but for stage 1 successful trial is outcome = [1,2,3]. Defaults to [1].
        figsize (tuple[int], optional): Tuple with two integer to define the size of the figure containing the plots.
    """

    # Filter only successfull outcomes
    success = data_behavior[data_behavior["Outcome"].isin(outcome)].copy()
    success.reset_index(inplace=True, drop=True)

    # Compute the difference in time between first and second poke
    success["timeBetweenPokes"] = abs(success["TimePoke1"] - success["TimePoke2"])

    # Get only those trails where the last active side was in the opposite side
    indexes = list()
    for i in range(1, len(success.index)):
        if success.loc[i, "ActiveSide"] != success.loc[i - 1, "ActiveSide"]:
            indexes.append(i)
    alternate = success.loc[indexes]

    # PLOTS
    fig, axes = plt.subplots(ncols=2, figsize=(15, 5))
    # All data
    sns.violinplot(
        data=success,
        x="MiceID",
        y="timeBetweenPokes",
        hue="BarrierType",
        split=True,
        ax=axes[0],
        cut=0,
    )
    axes[0].set_xlim(-1, 3.5)
    axes[0].set_title("All successful trials")

    # Only alternate sides
    sns.violinplot(
        data=alternate,
        x="MiceID",
        y="timeBetweenPokes",
        hue="BarrierType",
        split=True,
        ax=axes[1],
        cut=0,
    )
    axes[1].set_xlim(-1, 3.5)
    axes[1].set_title("Only trials with the previous trial been in the opposite side")

    plt.tight_layout()
    plt.show()


# pct_rewarded_trials(all_data)
rewarded_trials(data_behavior_3)
