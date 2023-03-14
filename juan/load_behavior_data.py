from jaratoolbox import loadbehavior
import matplotlib.pyplot as plt
import pandas as pd

subject = "coop010x011"  
paradigm = "coop4ports"  # The paradigm name is also part of the data file name
session = "20230313a" 
behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
bdata = loadbehavior.BehaviorData(behavFile)

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

subject = 'coop012x013' 
bdata_solid = load_data(subject, '20230314a') 
bdata_perforated = load_data(subject, '20230313a')

#print(bdata.keys())
#print(bdata.__dict__.keys())

# This is done to explore my hunch
# I need to check using window times, if mice are being more active during certain time of the section
df_solid = pd.DataFrame({'Outcome':bdata_solid['outcome'], 'Time': bdata_solid['timeTrialStart'], "Active side":bdata_solid['activeSide']})
df_perforated = pd.DataFrame({'Outcome':bdata_perforated['outcome'], 'Time': bdata_perforated['timeTrialStart'], "Active side":bdata_perforated['activeSide']})
print (df_solid.head())
print ("-------")
print (df_perforated.head())

print ("------")
print ("Hereunder what matters")
# Here I am printing the results. The window time is defined by the "bins" in the pandas function pd.cut
print(df_solid.groupby(pd.cut(df_solid['Time'], bins=3))['Outcome'].count())
print("-----")
print(df_perforated.groupby(pd.cut(df_perforated['Time'], bins=3))['Outcome'].count())