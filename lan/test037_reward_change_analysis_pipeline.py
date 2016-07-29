'''
Analysis pipeline for wild-type mice, reward-change freq discrimination paradigm. Includes: 

#Calculate sound response Z score (test013). 

#Calculate proportion of ISI violation (test029).

#Calculate modulation index and modulation significance (test026), specifying alignment type ('sound','center-out','side-in'), start of countTimeRange, end of countTimeRange, and animalName.

#ISI-checked:plot histogram with counts of total cells and significantly modulated cells (test033), specifying alignment type ('sound','center-out','side-in'), start of countTimeRange, end of countTimeRange, and animalName. write significantly modulated cells to text file.

#Without ISI check: plot histogram with counts of total cells and significantly modulated cells (test031), specifying alignment type ('sound','center-out','side-in'), start of countTimeRange, end of countTimeRange, and animalName. write significantly modulated cells to text file.

#ISI-checked: Plot activity during behavior for significantly modulated cells (test034).

#Without ISI check: Plot activity during behavior for significantly modulated cells (sound,0-0.15s:test015; center-out,0-0.4s:test024; side-in,0-0.6s:test025). ##Can modify test034 for both with and without ISI check plotting.

#Calculate movement response Z score (test038).

#Calculate modulation due to leftward vs rightward movement (test039).

#ISI-checked:plot histogram with counts of total movement-modulated cells (from analysis done with test039) and significantly reward-modulated cells after mouse leaves center port (test040).

#ISI-checked: plot histogram with counts of total movement-responsive cells (from movement Z score calculated in test038) and significantly reward-modulated cells after mouse leaves center port (test042).

'''
from subprocess import call 
###########Using adap005 as an example, can give multiple animal names in sys.arg to do multiple animals' analysis at once#############

call("python test013_write_maxZ_sound_response_stat.py adap005".split())
#call("python test013_write_maxZ_sound_response_stat.py adap005 adap012".split()) #processes data from multiple mice with one call

call("python test029_add_ISIViolations.py adap005".split())


call("python test026_add_ModIndex_difOnset_reward_change.py sound 0 0.1 adap005".split())
#call("python test026_add_ModIndex_difOnset_reward_change.py center-out 0 0.1 adap005".split())
#call("python test026_add_ModIndex_difOnset_reward_change.py side-in -0.1 0 adap005".split())

call("python test033_plot_ModHist_difAlign_difWin_withISIcheck.py sound 0 0.1 adap005".split())

call("python test034_plot_SigMod_difWin_difAlign_withISIcheck.py sound 0 0.1 adap005".split())
