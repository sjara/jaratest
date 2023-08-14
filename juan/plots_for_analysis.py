import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from load_behavior_data import collect_behavior_data, correct_data_with_excel


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
    data_behavior: pd.DataFrame,
    colors: list[str] = ["red", "blue"],
    width_lines=0.3,
    **kwargs,
):
    """_summary_:
    This categorical scatter plot is for analyze the percentage of regarded trials against barriers
    So, for each pair of mice is going to plot a graph with the percentage of rewarded trials for each barrier.

    Args:
        data_behavior (pd.DataFrame): Pandas dataframe with at least 3 columns: BarrierType, Percent rewarded and MiceID
        colors (list[str], optional): List of colors in string type to distinguish points from each barrier. Defaults to ["red", "cyan"].
        width_lines (float, optional): Float type to set the long of the line representing the mean of the points in each barrier. Defaults to 0.1.
    """
    # NOTE
    # Depending on the number of mice we will get list of axes of just one ax.
    # When subplots = (1,1). ax takes only 1 value.

    miceIds = data_behavior["MiceID"].unique()
    number_of_mice = len(miceIds)
    fig, ax = plt.subplots(1, number_of_mice, sharey=True, **kwargs)

    # Colors for barriers
    possible_barriers = data_behavior["BarrierType"].unique()
    colors = {key: np.random.rand(3) for key in possible_barriers}

    ## limit dataframe to the columns we need for comfort
    data_behavior = data_behavior.loc[
        :, ["MiceID", "Date", "BarrierType", "Percent rewarded"]
    ]
    ## Reduce all the session to only one row per session
    data_behavior.drop_duplicates(subset=["MiceID", "Date"], inplace=True)
    ## Set the index for mice selection for each graph
    data_behavior.set_index(keys=["MiceID", "BarrierType"], inplace=True)

    ## Sort the dataframe by miceID and barrier
    data_behavior.sort_index(level=[0, 1], inplace=True)

    if number_of_mice > 1:
        for i in range(number_of_mice):
            ## get the data for each pair of mice
            data_one_pair_mice = data_behavior.loc[miceIds[i]]

            ## get all the barriers which will be plotted
            barriers = data_one_pair_mice.index.unique().to_list()

            ## convert every label to a position in x-axis
            x_data = [barriers.index(barrier) for barrier in data_one_pair_mice.index]
            ax[i].scatter(
                x=x_data,
                y=data_one_pair_mice["Percent rewarded"].values,
                c=(data_one_pair_mice.index).map(
                    lambda x: colors[x]  # colors[0] if x == "solid" else colors[1]
                ),
                alpha=0.5,
            )

            # Horizontal line to represent mean of points of both barriers
            ax[i].hlines(
                y=[
                    int(data_one_pair_mice.loc[barrier]["Percent rewarded"].mean())
                    for barrier in data_one_pair_mice.index.unique()
                ],
                xmin=[idx - width_lines for idx in range(0, len(barriers))],
                xmax=[idx + width_lines for idx in range(0, len(barriers))],
                colors=[
                    colors[barrier] for barrier in barriers
                ],  # [colors[0] if barrier == "solid" else colors[1] for barrier in barriers],
            )

            ax[i].set_xlabel(miceIds[i])
            ax[i].set_xlim(0 - 0.2, max(x_data) + 0.2)
            ax[i].set_xticks(ticks=np.unique(x_data), labels=barriers)
            ax[i].set_yticks(np.arange(0, data_behavior["Percent rewarded"].max(), 5))
        ax[0].set_ylabel("Percentage rewarded trials")

    else:
        ## get all the barriers which will be plotted
        barriers = data_behavior.index.unique(1).to_list()

        ## convert every label to a position in x-axis
        x_data = [
            barriers.index(barrier)
            for barrier in data_behavior.index.get_level_values(1)
        ]
        ax.scatter(
            x=x_data,
            y=data_behavior["Percent rewarded"].values,
            c=(data_behavior.index.get_level_values(1)).map(
                lambda x: colors[x]  # colors[0] if x == "solid" else colors[1]
            ),
            alpha=0.5,
        )

        # Horizontal line to represent mean of points of both barriers
        ax.hlines(
            y=[
                int(data_behavior.loc(axis=0)[:, barrier]["Percent rewarded"].mean())
                for barrier in barriers
            ],
            xmin=[idx - width_lines for idx in range(0, len(barriers))],
            xmax=[idx + width_lines for idx in range(0, len(barriers))],
            colors=[colors[barrier] for barrier in barriers],  # colors[::-1],
        )

        ax.set_xlabel(miceIds[0])
        ax.set_ylabel("Percentage of rewarded trials")
        ax.set_yticks(np.arange(0, data_behavior["Percent rewarded"].max(), 5))
        ax.set_xticks(ticks=np.unique(x_data), labels=barriers)

    plt.tight_layout()
    # Adjust the spacing between the subplots and the top of the figure
    fig.subplots_adjust(top=0.9)
    # Title for the entire figure
    fig.suptitle("Percentage of rewarded trial per each treatment")
    return ax


def rewarded_trials(
    data_behavior: pd.DataFrame,
    outcome: list[int] = [1],
    colors: list[str] = ["red", "blue"],
    width_lines=0.2,
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

    # NOTE
    # Depending on the number of mice we will get list of axes of just one ax.
    # When subplots = (1,1). ax takes only 1 value.

    # Colors for barriers
    possible_barriers = data_behavior["BarrierType"].unique()
    colors = {key: np.random.rand(3) for key in possible_barriers}

    ## Filter the dataframe by the outcome desired.
    ## This will be the dataframe used to plot. "MiceID", "BarrierType", "Date" are the columns to keep (levels=0,1,2)
    data_behavior_by_outcome = (
        data_behavior[data_behavior["Outcome"].isin(outcome)]
        .groupby(["MiceID", "BarrierType", "Date"])["Outcome"]
        .sum()
    )
    data_behavior_by_outcome.sort_index(level=0,inplace=True,ascending=False)

    miceIds = data_behavior_by_outcome.index.unique(0).to_list()
    number_of_mice = len(miceIds)
    fig, ax = plt.subplots(1, number_of_mice, sharey=True)
    locs = plt.xticks()

    if number_of_mice > 1:
        for i in range(number_of_mice):
            ## select data from each pair of mice
            data_one_pair_mice = data_behavior_by_outcome.loc[miceIds[i]]
            data_one_pair_mice.sort_index(level=0, inplace=True)
            ax[i].scatter(
                x=data_one_pair_mice.index.get_level_values(0).to_list(),
                y=data_one_pair_mice.values,
                c=(data_one_pair_mice.index.get_level_values(0)).map(
                    lambda x: colors[x]
                ),
                alpha=0.3,
            )
            # This is for getting the positions of the x sticks in order to determine the limites of the lines to plot the mean
            locs = plt.xticks()

            # Horizontal line to represent mean of points of both barriers
            ax[i].hlines(
                y=[
                    int(data_one_pair_mice.loc[barrier].mean())
                    for barrier in data_one_pair_mice.index.unique(0).to_list()
                ],
                xmin=[0 - width_lines]
                + [
                    (0 + 1 / idx) - width_lines
                    for idx in range(1, len(data_one_pair_mice.index.unique(0)))
                ],
                xmax=[0 + width_lines]
                + [
                    (0 + 1 / idx) + width_lines
                    for idx in range(1, len(data_one_pair_mice.index.unique(0)))
                ],
                colors=[
                    colors[barrier]
                    for barrier in data_one_pair_mice.index.get_level_values(0).unique()
                ],
            )

            ax[i].set_xlabel(miceIds[i])
            ax[i].set_xlim(locs[0][0] - 0.2, locs[0][-1] + 0.2)
            ax[i].set_yticks(np.arange(0, data_behavior_by_outcome.max(), 10))
        ax[0].set_ylabel("Rewarded trials")

    else:
        ## set each point
        ax.scatter(
            x=data_behavior_by_outcome.index.get_level_values(1).to_list(),
            y=data_behavior_by_outcome.values,
            c=(data_behavior_by_outcome.index.get_level_values(1)).map(
                lambda x: colors[x]
            ),
            alpha=0.3,
        )
        # This is for getting the positions of the x sticks in order to determine the limits of the lines to plot the mean
        locs = plt.xticks()

        # Horizontal line to represent mean of points of both barriers
        ax.hlines(
            y=[
                int(data_behavior_by_outcome.loc[:, barrier].mean())
                for barrier in data_behavior_by_outcome.index.unique(1).to_list()
            ],
            xmin=[
                locs[0][idx] - width_lines
                for idx in range(0, len(data_behavior_by_outcome.index.unique(1)))
            ],
            xmax=[
                locs[0][idx] + width_lines
                for idx in range(0, len(data_behavior_by_outcome.index.unique(1)))
            ],
            colors=[
                colors[barrier]
                for barrier in data_behavior_by_outcome.index.get_level_values(
                    1
                ).unique()
            ],
        )

        ax.set_xlabel(miceIds[0])
        ax.set_ylabel("Rewarded trials")
        ax.set_xlim(locs[0][0] - 0.5, locs[0][-1] + 0.5)
        ax.set_yticks(np.arange(0, data_behavior_by_outcome.max(), 5))

    plt.tight_layout()
    # title for the entire figure
    fig.suptitle("Rewarded trial per mice per barrier")
    # Adjust the spacing between the subplots and the top of the figure
    fig.subplots_adjust(top=0.9)
    return ax


def violin_plot_waitTime(data_behavior: pd.DataFrame, outcome: list[int] = [1]):
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


def hist_time_in_ports(data_behavior: pd.DataFrame):
    """_summary_: histogram for time spent by the mice in ports during a sucessfull trial

    Args:
        data_behavior (pd.DataFrame): Dataframe collected by the function collect_behavior_data in load_behavior_data module
    """
    data_behavior["timeBetweenPokes"] = abs(
        data_behavior["TimePoke1"] - data_behavior["TimePoke2"]
    )
    data_behavior = data_behavior[["BarrierType", "timeBetweenPokes"]]
    fig, ax = plt.subplots()

    ## Possible barriers
    barriers = data_behavior["BarrierType"].unique()
    ## Collect data in a list of arrays where each arrays belongs to a barrier
    data_per_barrier = [
        np.array(
            data_behavior.loc[
                data_behavior["BarrierType"] == barrier, "timeBetweenPokes"
            ].values
        )
        for barrier in barriers
    ]

    # histogran
    ax.hist(
        x=data_per_barrier,
        label=barriers,
        color=[np.random.rand(3), np.random.rand(3)],
        histtype="stepfilled",
        alpha=0.5,
    )
    ax.legend()


def report(
    data_behavior: pd.DataFrame,
    colors: list[str] = ["red", "blue"],
    outcome: list[int] = [1],
    width_lines=0.2,
):
    """_summary_: Generates different plots for one pair of mice showing important information such as
    percent rewarded trials.

    Args:
        data_behavior (pd.DataFrame): Dataframe collected by the function collect_behavior_data in load_behavior_data module
        colors (list[str], optional): Set color for the points. Defaults to ["red", "blue"].
        width_lines (float, optional): Width of horizontal lines representing average. Defaults to 0.3.
    """

    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(12, 7))

    ## GENERAL SETTINGS ##
    ## Colors for barriers
    possible_barriers = data_behavior["BarrierType"].unique()
    colors = {key: np.random.rand(3) for key in possible_barriers}

    data_behavior.sort_values(by="BarrierType", inplace=True)

    ## Get all the barriers which will be plotted
    barriers = data_behavior["BarrierType"].unique().tolist()

    ## PERCENTAGE REWARDED TRIALS PER SESSION PER BARRIER ##
    ## Reduce all sessions to only one row per session
    data_behavior_pct = data_behavior.drop_duplicates(subset=["Date"])

    ## Convert every label to a position in x-axis
    x_data = [barriers.index(barrier) for barrier in data_behavior_pct["BarrierType"]]

    ## Scatter plot
    ax[0, 0].scatter(
        x=x_data,
        y=data_behavior_pct["Percent rewarded"].values,
        c=(data_behavior_pct["BarrierType"]).map(lambda x: colors[x]),
        alpha=0.7,
    )

    # Horizontal line to represent mean of points of both barriers
    ax[0, 0].hlines(
        y=[
            int(
                data_behavior_pct.loc[
                    data_behavior_pct["BarrierType"] == barrier, "Percent rewarded"
                ].mean()
            )
            for barrier in barriers
        ],
        xmin=[idx - width_lines for idx in range(0, len(barriers))],
        xmax=[idx + width_lines for idx in range(0, len(barriers))],
        colors=[colors[barrier] for barrier in barriers],
    )

    ax[0, 0].set_ylabel("Percentage of rewarded trials")
    ax[0, 0].set_yticks(
        np.arange(
            0,
            data_behavior_pct["Percent rewarded"].max()
            + (data_behavior_pct["Percent rewarded"].max() * 0.1),
            2,
        )
    )
    ax[0, 0].set_xticks(ticks=np.unique(x_data), labels=barriers)
    ax[0, 0].set_ylim(
        0,
        data_behavior_pct["Percent rewarded"].max()
        + (data_behavior_pct["Percent rewarded"].max() * 0.1),
    )
    ax[0, 0].set_title("Percentage of rewarded trials")

    ## REWARDED TRIALS PER SESSION PER BARRIER ##
    ## Filter the dataframe by the outcome desired.
    ## This will be the dataframe used to plot. "MiceID", "BarrierType", "Date" are the columns to keep (levels=0,1,2)
    data_behavior_by_outcome = (
        data_behavior[data_behavior["Outcome"].isin(outcome)].groupby(
            ["BarrierType", "Date"]
        )
    )["Outcome"].sum()

    ## Scatter plot
    ax[0, 1].scatter(
        x=x_data,
        y=data_behavior_by_outcome.values,
        c=(data_behavior_by_outcome.index.get_level_values(0)).map(lambda x: colors[x]),
        alpha=0.7,
    )

    # Horizontal line to represent mean of points of both barriers
    ax[0, 1].hlines(
        y=[int(data_behavior_by_outcome.loc[barrier].mean()) for barrier in barriers],
        xmin=[idx - width_lines for idx in range(0, len(barriers))],
        xmax=[idx + width_lines for idx in range(0, len(barriers))],
        colors=[colors[barrier] for barrier in barriers],
    )

    ax[0, 1].set_ylabel("Rewarded trials")
    ax[0, 1].set_xticks(ticks=np.unique(x_data), labels=barriers)
    ax[0, 1].set_yticks(
        np.arange(
            0,
            data_behavior_by_outcome.max() + (data_behavior_by_outcome.max() * 0.1),
            20,
        )
    )
    ax[0, 1].set_ylim(
        0, data_behavior_by_outcome.max() + (data_behavior_by_outcome.max() * 0.1)
    )
    ax[0, 1].set_title("Rewarded trials per session")

    ## TOTAL TRIALS PER SESSION PER BARRIER ##
    sessions = data_behavior["Date"].unique()
    y_data_total_trials = [len(data_behavior[data_behavior["Date"] == date]) for date in sessions]

    ## Scatter plot
    ax[0, 2].scatter(
        x=x_data,
        y=y_data_total_trials,
        c=(data_behavior_by_outcome.index.get_level_values(0)).map(lambda x: colors[x]),
        alpha=0.7,
    )

    # Horizontal line to represent mean of points of both barriers
    # ax[0, 2].hlines(
    #     y=[int(data_behavior_by_outcome.loc[barrier].mean()) for barrier in barriers],
    #     xmin=[idx - width_lines for idx in range(0, len(barriers))],
    #     xmax=[idx + width_lines for idx in range(0, len(barriers))],
    #     colors=[colors[barrier] for barrier in barriers],
    # )

    ax[0, 2].set_ylabel("Total trials")
    ax[0, 2].set_xticks(ticks=np.unique(x_data), labels=barriers)
    ax[0, 2].set_ylim(0, max(y_data_total_trials) + (max(y_data_total_trials) * 0.1))
    ax[0, 2].set_xlim(0 - 1, len(barriers))
    ax[0, 2].set_title("Total trials per session")

    ## ACCUMULATED REWARDED TRIALS ##
    y_data_accumulated_rewarded_trials = [data_behavior_by_outcome.loc[barrier].sum() for barrier in barriers]
    ## Bar plot
    bars = ax[1, 0].bar(
        barriers,
        y_data_accumulated_rewarded_trials,
        label=barriers,
    )
    ax[1, 0].bar_label(bars, padding=3)
    ax[1, 0].set_title("Accumulated rewarded trials")
    ax[1, 0].set_ylim(0, max(y_data_accumulated_rewarded_trials) + (max(y_data_accumulated_rewarded_trials) * 0.2))

    ## ACCUMULATED TOTAL TRIALS ##
    # y_data = [
    #     len(data_behavior.loc[data_behavior["BarrierType"] == barrier])
    #     for barrier in barriers
    # ]
    # ## Bar plot
    # bars = ax[1, 1].bar(
    #     barriers,
    #     y_data,
    #     label=barriers,
    # )
    # ax[1, 1].bar_label(bars, padding=3)
    # ax[1, 1].set_title("Accumulated total trials")
    # ax[1, 1].set_ylim(0, max(y_data) + (max(y_data) * 0.2))

    ## TIME SPEND IN PORTS: TIME BETWEEN THE STARTER POKE AND THE LAST POKE OF A SUCCESSFULL TRIAL ##

    ## Compute the first and last poke
    data_behavior["timeBetweenPokes"] = abs(
        data_behavior["TimePoke1"] - data_behavior["TimePoke2"]
    )
    ## Collect data in a list of arrays where each arrays belongs to a barrier
    data_per_barrier = [
        np.array(
            data_behavior.loc[
                data_behavior["BarrierType"] == barrier, "timeBetweenPokes"
            ].values
        )
        for barrier in barriers
    ]

    ## Histogram
    ax[1, 2].hist(
        x=data_per_barrier,
        label=barriers,
        color=[np.random.rand(3) for _i in barriers],
        histtype="stepfilled",
        alpha=0.5,
    )
    ax[1, 2].legend()
    ax[1, 2].set_title("Time spent in ports")
    ax[1, 2].set_xlabel("Time (sec)")

    fig.suptitle(f"{data_behavior['MiceID'][0]} \n {data_behavior['Date'].min()} => {data_behavior['Date'].max()} " )
    fig.tight_layout()


# data = collect_behavior_data(
#     mice_data={
#         #"coop014x015": [("2023-07-17", "2023-07-21"), ("2023-07-23", "2023-07-27")],
#         # 'coop016x017':[('2023-07-10','2023-07-14'),('2023-07-16','2023-07-21'),('2023-07-23','2023-07-27')],
#         'coop022x023':[('2023-07-29','2023-08-09')]
#     }
# )
# data = correct_data_with_excel(
#     fileName="coop_seek_and_find_v2.xlsx",
#     sheet_name=["coop022x023"],
#     data_collected=data,
# ) 

# report(data)
# plt.show()
