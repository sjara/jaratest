from jaratoolbox import loadbehavior
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta

# subject = "coop010x011"  
# paradigm = "coop4ports"  # The paradigm name is also part of the data file name
# session = "20230313a" 
# behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
# bdata = loadbehavior.BehaviorData(behavFile)

# Objective: Make a group of graphs to show the accumulated rewards every 20 min for each pair of mice, date and barrier

def load_data (subject, session):
    """_summary_

    Args:
        subject (str): The name of the mouse
        session (str): The format is usually YYYYMMDD and a short suffix

    Returns:
        dict{str:np.ndarray}: Dictionary containing results of subject and session given to the function. 
    """

    paradigm = 'coop4ports' # The paradigm name is also part of the data file name
    behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
    bdata = loadbehavior.BehaviorData(behavFile)
    return bdata


# Paso 1: I need to accumulate all data taking into account that I started recording the time since 20230313a and
# only the time of stage 1 can be estimated
def merge_data (start_subject, number_of_mice, start_date, end_date):
    # Empty dataframe defining the fields will need
    df_all_data = pd.DataFrame(columns=['Outcome', 'Time', "BarrierType", "Date", "MiceID"])
    # Break down the tuple to handle each number separetaly 
    mouse1,mouse2 = start_subject
    for _ in range(number_of_mice):
        mice_id = f'coop0{mouse1}x0{mouse2}'
        #print(mice_id)
        for days in range(int((end_date - start_date).days)+1):
            current_date = str(start_date + timedelta(days)).replace("-", "")
            #print(current_date)
            bdata = load_data(mice_id, f'{current_date}a')
            df = pd.DataFrame({'Outcome':bdata['outcome'], 'Time': bdata['timeTrialStart'], "BarrierType":bdata['barrierType'] })
            df['Date'] = current_date
            df['MiceID'] = mice_id
            df_all_data= pd.concat([df, df_all_data],ignore_index=True)
        mouse1= mouse2 + 1
        mouse2= mouse1 + 1
    
    df_all_data.replace({'BarrierType':bdata.labels['barrierType']}, inplace=True)
    return df_all_data

data = merge_data(start_subject=(10,11), number_of_mice=3, start_date=date(2023, 3, 13), end_date=date(2023, 3, 14))

# Paso 2: I need to group all data by barrier > mice id 
data.set_index(keys=['BarrierType','MiceID'], inplace=True)


def f ():
    
    # print ("------")
    # print ("Hereunder what matters")
    # # Here I am printing the results. The window time is defined by the "bins" in the pandas function pd.cut
    # print(df_solid.groupby(pd.cut(df_solid['Time'], bins=3))['Outcome'].count())
    print("-----")
    print(df_perforated.groupby(pd.cut(df_perforated['Time'], bins=3))['Outcome'].count())
    df_perforated=df_perforated.groupby(pd.cut(df_perforated['Time'], bins=3))['Outcome'].count()

    # Plotting histogram with seaborn
    plt.bar(df_perforated.index.astype(str), df_perforated.values)

    plt.show()
