from inforecordings import test098_inforec as inforec

sessions = []
for experiment in inforec.test098.experiments:
    for site in experiment.sites:
        sessions.extend(site.session_ephys_dirs())


