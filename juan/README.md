# Test scripts by Juan Picón.

* The folder ```scripts/``` contains the code to reproduce the graphs presented on the different reports.
* The folder ```utils/``` contains the functions use the functions described in  [Utils](#Utils) and [Plotting](#Plotting) below.
  
## Utils 🧰 <a name = "Utils"></a>
* `load_behavior_data.py`: Contains functions for processing behavior data from coop_four_port paradigm.
    * `load_data`: It uses `loadbehavior.BehaviorData(behavFile)` to get behavioral data.
    * `collect_behavior_data`: Merge all the behavior data retrieved with `loadbehavior.BehaviorData(behavFile)` into one dataframe.
    * `collect_events`: Merge all the events from the behavior data retrieved with `loadbehavior.BehaviorData(behavFile)` into one dataframe.
    * `filter_and_group`: Filter the data by the outcome of a trial and to group the data by the number of segmentation in time desired (bins).The last part means that if you consider a 60 min. long behavioral session, 3 bin is equal to intervals of 20 min.
    * `correct_data_with_excel`: Using an excel file to correct the data collected from using the function above described `collect_behavior_data`. This was useful
    to correct variables which did not affect the training, for example, the barrier. For example, if in the GUI you set the wrong barrier during the session. 

## Plotting 📊 <a name = "Plotting"></a>

* `plot_for_analysis.py`: Contains functions for plotting graphs useful for data analysis from coop_four_ports paradigm.  
    * `pct_rewarded_trials` : Show  percentage of rewarded trials for each barrier per pair of mice in a categorical scatter graph.
    * `rewarded_trials`: Show  percentage of rewarded trials for each barrier per pair of mice in a categorical scatter graph. 
    * `plot_accum_rewards`: Show accumulated rewarded trials for each barrier per pair of mice in a barplot.
    * `violin_plot_waitTime`: It helps us analyse the wait time parameter of coop_four_ports paradigm by computing how much time passed between the first and the second poke and plotting the data in a violin plot.
    * `report`: Generates different plots for **one** pair of mice that show important information such as percent rewarded trials.
    * `performance_across_time`: Plot the performance for each pair of mice across time.
   
