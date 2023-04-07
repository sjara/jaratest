import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from datetime import date
from load_behavior_data import collect_behavior_data

data_behavior = collect_behavior_data(
    start_subject=(10, 11),
    number_of_mice=3,
    start_date=date(2023, 3, 21),
    end_date=date(2023, 3, 30),
)


def categorical_scatter_plot(
    data_behavior: pd.DataFrame, colors: list[str] = ["red", "blue"], width_lines=0.1
):
    width_lines = width_lines
    number_of_mice = len(data_behavior["MiceID"].unique())
    fig, ax = plt.subplots(1, number_of_mice, sharey=True)
    
    # Depending on the number of mice we will get list of axes of just one ax
    if number_of_mice > 1:
        for i in range(number_of_mice):
            ax[i].scatter(
                x=data_behavior["BarrierType"],
                y=data_behavior["Percent rewarded"],
                c=(data_behavior["BarrierType"]).apply(
                    lambda x: colors[0] if x == "solid" else colors[1]
                ),
            )
            # This is for getting the positions of the x sticks in order to determine the limites of the lines to plot the mean
            locs = plt.xticks()

            # Horizontal line to represent mean of points of both barriers
            ax[i].hlines(
                y=[
                    int(
                        data_behavior.loc[
                            data_behavior["BarrierType"] == "solid", "Percent rewarded"
                        ].mean()
                    ),
                    int(
                        data_behavior.loc[
                            data_behavior["BarrierType"] == "perforated",
                            "Percent rewarded",
                        ].mean()
                    ),
                ],
                xmin=[locs[0][0] - width_lines, locs[0][-1] - width_lines],
                xmax=[locs[0][0] + width_lines, locs[0][-1] + width_lines],
                colors=colors,
            )

            ax[i].set_xlabel(data_behavior["MiceID"].unique()[i])
            ax[i].set_ylabel("Percentage of rewarded trials")
            
    else:
        ax.scatter(
            x=data_behavior["BarrierType"],
            y=data_behavior["Percent rewarded"],
            c=(data_behavior["BarrierType"]).apply(
                lambda x: colors[0] if x == "solid" else colors[1]
            ),
        )
        # This is for getting the positions of the x sticks in order to determine the limites of the lines to plot the mean
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
                        data_behavior["BarrierType"] == "perforated", "Percent rewarded"
                    ].mean()
                ),
            ],
            xmin=[locs[0][0] - width_lines, locs[0][-1] - width_lines],
            xmax=[locs[0][0] + width_lines, locs[0][-1] + width_lines],
            colors=colors,
        )

        ax.set_xlabel(data_behavior["MiceID"].unique()[0])
        ax.set_ylabel("Percentage of rewarded trials")
        ax.set_xlim(-1, 2)

    plt.tight_layout()
    # plt.title("Percentage of rewarded trial per each treatment")


categorical_scatter_plot(data_behavior)
plt.show()
