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


def for_stage_1(bdata):
    time = list()
    count = 0
    for i in bdata["outcome"]:
        if i in [1, 2, 3]:
            count += 3
        count += 3
        time.append(count)
    return time


def normalize_time(df):
    """_summary_
    This function is to "normalized" data, since the timer of the GUI for cooperation project most of the time does not start
    at second 0. In other words, this function is to asure that data are between 0 and 3600 (60 min) or 0 and 2400 (40 min) depending on the long
    of the session.
    Args:
        df (pd.Dataframe): Dataframe with all the data collected in collect_data function

    Returns:
        pd.Dataframe:  Dataframe with all the data collected in collect_data function normalized between the range of time the session was performed
    """
    df["TimeTrialStart"] = df["TimeTrialStart"] - df.loc[0, "TimeTrialStart"]
    return df


def collect_behavior_data(
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
            "TimeTrialStart",
            "BarrierType",
            'ActiveSide',
            "Date",
            "MiceID",
            "TimePoke1",
            "TimePoke2",
            "Stage",
            "Percent rewarded"
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
            try:
                
                bdata = load_data(mice_id, f"{current_date}a")
            except:
                print(f"ERROR FILE {current_date}a FOR {mice_id} MICE DOES NOT EXIST")
                continue
            
            df = pd.DataFrame(
                {
                    "Outcome": bdata["outcome"],
                    "TimeTrialStart": bdata["timeTrialStart"],  # for_stage_1(bdata)
                    "BarrierType": bdata["barrierType"],
                    "ActiveSide":bdata['activeSide'],
                    "TimePoke1": bdata["timePoke1"],
                    "TimePoke2": bdata["timePoke2"],
                    "Stage": bdata["taskMode"],
                    "Date": current_date,
                    "MiceID": mice_id,
                }
            )

            ## "Normalize" data since GUI has a problem and most of the time the timer does not start at second 0
            #df = normalize_time(df)
            df["Percent rewarded"]= len(bdata["outcome"][bdata['outcome']==1])/len(bdata['outcome']) * 100
            df_all_data = pd.concat([df, df_all_data], ignore_index=True)
        mouse1 = mouse2 + 1
        mouse2 = mouse1 + 1

    df_all_data.replace({"BarrierType": bdata.labels["barrierType"], "ActiveSide": bdata.labels["activeSide"]}, inplace=True)
    df_all_data.replace([{"Stage": bdata.labels["taskMode"]}], inplace=True)
    return df_all_data


def collect_events(
    start_subject: tuple[int], number_of_mice: int, start_date: date, end_date: date
):
    """_summary_:
    This function is used to merge all the events of the behavior data we want from social cooperatio project into one dataframe

    Args:
        start_subject (str): Store the numbers of the first pair of mice we want to start collecting data.
        number_of_mice (int): Store the amount of mice we want to collect data. So, we start iterating number_of_mice mices from start_subject.
        start_date (datetime.date): Store the first date we want to collect the data.
        end_date (datetime.date): Store the last date we want to collect the data.

    Returns:
        pandas.Dataframe: All collected events returned into one Dataframe
    """
    # Empty dataframe defining the fields will need
    df_all_data = pd.DataFrame(
        columns=[
            "MiceID",
            "Date",
            "Events",
            "Event Time",
        ]
    )
    # Break down the tuple to handle each number separetaly
    mouse1, mouse2 = start_subject

    # Upload a dataframe for each pair of mice and date
    for _ in range(number_of_mice):
        mice_id = f"coop0{mouse1}x0{mouse2}"
        for days in range(int((end_date - start_date).days) + 1):
            current_date = str(start_date + timedelta(days)).replace("-", "")
            bdata = load_data(mice_id, f"{current_date}a")
            df = pd.DataFrame(
                {
                    "MiceID": mice_id,
                    "Date": current_date,
                    "Events": bdata.events["eventCode"],
                    "Event Time":bdata.events["eventTime"],
                }
            )
            df.replace({"Events":bdata.stateMatrix["eventsNames"]}, inplace=True)
            df_all_data = pd.concat([df, df_all_data], ignore_index=True)
        mouse1 = mouse2 + 1
        mouse2 = mouse1 + 1
    return df_all_data
