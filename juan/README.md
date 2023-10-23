# Test scripts by Juan Picón.

* The folder ```scripts/``` contains the code to reproduce the graphs presented on the different reports.
* The folder ```utils/``` contains the functions use the functions described in  [Utils](#Utils) and [Plotting](#Plotting) below.
  
## Utils 🧰 <a name = "Utils"></a>
* `load_behavior_data.py`: Contains functions for processing behavior data from coop_four_port paradigm.
    * `load_data`:description
    * `collect_behavior_data`: description
    * `collect_events`: description
    * `filter_and_group`: description

## Plotting 📊 <a name = "Plotting"></a>

* `plot_for_analysis.py`: Contains functions for plotting graphs useful for data analysis from coop_four_ports paradigm.  
    * `pct_rewarded_trials` : Show  percentage of rewarded trials for each barrier per pair of mice in a categorical scatter graph. 
    * `plot_accum_rewards`: Show accumulated rewarded trials for each barrier per pair of mice in a barplot.
    * `violin_plot_waitTime`: It helps us analyse the wait time parameter of coop_four_ports paradigm by computing how much time passed between the first and the second poke and plotting the data in a violin plot.
