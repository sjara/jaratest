# Scripts for generating 2025hemisym figures

* [database_laser_analysis.py](./database_laser_analysis.py)
    * Creates initial cell databases for a subject
    * ```$ python database_laser_analysis.py <subject>``` to run for experimental datasets
    * ```$ python database_laser_analysis.py <subject> optoShamAMtone``` to run for sham sessions
    * Takes 5~10 minutes to run depending on the number of cells

* [figure_sessions_comparison.py](./figure_sessions_comparison.py)
    * Generates summary figure(s) and (optionally) cell reports 
        * Set ```plotCellReports=True``` to generate the cell reports
        * Set ```BAR_CHARTS=True``` to generate bar charts with between-group comparisons
        * run with ```$ python figure_sessions_comparison.py <sessionType> <eventKey> ``` (e.g., ) ```$ python figure_sessions_comparison.py optoTuningAMtone Evoked ```. 
            * Use ```$ python figure_sessions_comparison.py optoTuningAMtone BTR ``` to have it use only the "best" time range for each cell
            * Use ```$ python figure_sessions_comparison.py optoShamAMtone Evoked ``` to run it on the sham sessions
            * Use ```$ python figure_sessions_comparison.py optoTuningFreq Evoked ``` to run it on the unmodulated pure tone sessions



    


