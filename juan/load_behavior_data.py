from jaratoolbox import loadbehavior
import pandas as pd
from datetime import date, timedelta

# subject = "coop010x011"
# paradigm = "coop4ports"  # The paradigm name is also part of the data file name
# session = "20230313a"
# behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
# bdata = loadbehavior.BehaviorData(behavFile)


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


def collect_data(
    start_subject: tuple[int], number_of_mice: int, start_date: date, end_date: date
):
    """_summary_:
    This function is used to merge all the behavior data we want from social cooperatio project into one dataframe

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
        columns=[
            "Outcome",
            "Time",
            "BarrierType",
            "Date",
            "MiceID",
            "TimePoke1",
            "TimePoke2",
            "Stage",
        ]
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
                    # "Time": bdata["timeTrialStart"],
                    "BarrierType": bdata["barrierType"],
                    "TimePoke1": bdata["timePoke1"],
                    "TimePoke2": bdata["timePoke2"],
                    "Stage": bdata["taskMode"],
                    "Date": current_date,
                    "MiceID": mice_id,
                }
            )

            df_all_data = pd.concat([df, df_all_data], ignore_index=True)
        mouse1 = mouse2 + 1
        mouse2 = mouse1 + 1

    df_all_data.replace({"BarrierType": bdata.labels["barrierType"]}, inplace=True)
    df_all_data.replace([{"Stage": bdata.labels["taskMode"]}], inplace=True)
    return df_all_data
