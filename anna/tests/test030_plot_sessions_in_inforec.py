import matplotlib.pyplot as plt

from jaratoolbox import ephysinterface

subject = 'chad009'

ei = ephysinterface.EphysInterface('/home/jarauser/src/jaratest/common/inforecordings/{}_inforec.py'.format(subject))

experiments = range(len(ei.inforec.experiments))

for experiment in experiments:
    sites = range(len(ei.inforec.experiments[experiment].sites))
    for site in sites:
        try:
            ei.plot_array_raster(-1, experiment, site)
            raw_input("Press Enter to continue...")
        except IndexError:
            print("No sessions at this site")
        