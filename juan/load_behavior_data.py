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
            try:
                bdata = load_data(mice_id, f"{current_date}a")
            except:
                print(f"ERROR FILE {current_date}a FOR {mice_id} MICE DOES NOT EXIST")
                continue
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


def filter_and_group(bins:int, data:pd.DataFrame, sessionLen:int, outcome:list[int] = [1]) -> pd.DataFrame:

    """_summary_:
    This function is used to filter the data by the outcome of a trial
    and to group the data by BarrierType, MiceID and the number of segmentation in time desired (bins).
    Time of each trial is retrieve from the last poke in each trial.

    Args:
    sessionLen (int): How long is the training session.
    bins (int): How many ranges do you want to segment the time session? 
        For example, for a session of 60 min. 6 bins is equal to ranges of 10 min 
    data (pd.DataFrame): pandas dataframe with at least 5 columns: BarrierType, MiceID, Outcome, TimePoke1 and TimePoke2
    outcome (list[int], optional): This is to filter trials by outcome. Defaults to [1]

    Returns:
        data_filtered_grouped: Dataframe with the data filtered and grouped into
        as many segments as chose by the user
    """

    data.set_index(keys=["BarrierType", "MiceID"], inplace=True)
    data_filtered = data[data["Outcome"].isin(outcome)]
    data_filtered_grouped = data_filtered.groupby(
        by=[
            "BarrierType",
            "MiceID",
            pd.cut(
                data_filtered[["TimePoke2", 'TimePoke1']].apply(max, axis=1),
                bins=bins,
                labels=[
                    f"{int((sessionLen/bins*i)-(sessionLen/bins))}-{int(sessionLen/bins*i)}"
                    for i in range(1, bins + 1)
                ],
            ),
        ]
    )["Outcome"].count()
    return data_filtered_grouped


def correct_data_with_excel (fileName:str,  sheet_name:list[str], data_collected:pd.DataFrame=None, **kwargs):
    """_summary_: Using an excel file to correct the data collected from each pair of mice using 
    the function collect_behavior_data which uses loadbehavior from jaratoolbox. This is specially useful
    to correct variables which did not affect the training, for example, the barrier, other parameters error are
    just reported like the waitTime and others. For example, if you set the wrong barrier during the section with this function
    you can use a spreadsheet to correct it.

    Args:
        fileName (str): _description_
        sheetName (list[str]): _description_
        data_collected (pd.DataFrame): _description_
    """
    df_excel = pd.read_excel(io=fileName, sheet_name=sheet_name, **kwargs)
    print(df_excel)
    #data_collected.set_index(keys='MiceID', inplace=True)
    for mice in data_collected['MiceID'].unique():
        df_excel[mice]


correct_data_with_excel('coop_seek_and_find_v2.xlsx',sheet_name='coop016x017')
    