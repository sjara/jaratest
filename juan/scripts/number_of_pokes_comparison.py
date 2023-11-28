import common_init
import utils.load_behavior_data as lbd
import utils.plots_for_analysis as pfa
import matplotlib.pyplot as plt

"""
This code is to reproduce the same graphs presented in the question 
"How many “pokes” is the best number?" on the Q&A section.
"""
## First graphs
data = lbd.collect_behavior_data(
    mice_data={
        "coop028x029": [("2023-09-21", "2023-10-04")],
        "coop026x027": [("2023-08-27", "2023-09-07")],
    }
)
data.sort_values(by="MiceID", inplace=True)
data = lbd.correct_data_with_excel(
    fileName="coop_seek_and_find_v2_updated.xlsx",
    sheet_name=data["MiceID"].unique().tolist(),
    data_collected=data,
)


## Second graphs
data2 = lbd.collect_behavior_data(
    mice_data={
        # "coop028x029": [("2023-09-21", "2023-10-04")],
        "coop022x023": [
            ("2023-08-29", "2023-09-13"),
            ("2023-08-08", "2023-08-15"),
            ("2023-08-17", "2023-08-22"),
        ],
    }
)
data2 = lbd.correct_data_with_excel(
    fileName="coop_seek_and_find_v2_updated.xlsx",
    sheet_name=data2["MiceID"].unique().tolist(),
    data_collected=data2,
)

data3 = lbd.collect_behavior_data(
    mice_data={
        # "coop028x029": [("2023-09-21", "2023-10-04")],
        "coop028x029": [
            ("2023-09-21", "2023-10-04"),
            ("2023-11-06", "2023-11-15"),
        ]
    }
)
data3 = lbd.correct_data_with_excel(
    fileName="coop_seek_and_find_v2_updated.xlsx",
    sheet_name=data3["MiceID"].unique().tolist(),
    data_collected=data3,
)


# PLOT
pfa.pct_rewarded_trials(data2, hori_line=(len(data2["BarrierType"].unique()) - 1) / 2)
pfa.pct_rewarded_trials(data3, hori_line=(len(data3["BarrierType"].unique()) - 1) / 2)
pfa.pct_rewarded_trials(
    data,
    custom_title={
        "coop026x027": f" => 10 pokes\n {min(data[data['MiceID'] == 'coop026x027']['Date'].unique())} => {max(data[data['MiceID'] == 'coop026x027']['Date'].unique())} ",
        "coop028x029": f" => 5 pokes\n {min(data[data['MiceID'] == 'coop028x029']['Date'].unique())} => {max(data[data['MiceID'] == 'coop028x029']['Date'].unique())} ",
    },
    custom_labels={},
)
pfa.rewarded_trials(
    data,
    custom_title={
        "coop026x027": f" => 10 pokes\n {min(data[data['MiceID'] == 'coop026x027']['Date'].unique())} => {max(data[data['MiceID'] == 'coop026x027']['Date'].unique())} ",
        "coop028x029": f" => 5 pokes\n {min(data[data['MiceID'] == 'coop028x029']['Date'].unique())} => {max(data[data['MiceID'] == 'coop028x029']['Date'].unique())} ",
    },
)
plt.tight_layout()
plt.show()
