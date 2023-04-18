salineHighFreq = {
    "runStart": ["2:13", "4:58"],
    "runStop": ["2:25", "5:00"]
}

salineLowFreq = {
    "runStart": ["0:00", "0:21", "1:04"],
    "runStop": ["0:12", "0:38", "1:23"]
}

salineFMDown = {
    "runStart": ["1:08", "1:30", "5:46"],
    "runStop": ["1:24", "1:49", "5:51"]
}

salineFMUp = {
    "runStart": ["1:54", "2:25", "3:45", "4:06"],
    "runStop": ["2:22", "2:45", "4:00", "4:20"]
}

'''
Potential for adding multiple days later with nested dictionaries

salineFreq = {
    "2022-01-01": {
        "runStart": ["2:13", "4:58"],
        "runStop": ["2:25", "5:00"]
    },
    "2022-01-02": {
        "runStart": ["3:13", "6:58"],
        "runStop": ["3:25", "6:00"]
    },
    "2022-01-03": {
        "runStart": ["1:13", "2:58"],
        "runStop": ["1:25", "3:00"]
    }
}


accessing later would look like:

date = "2022-01-01"
salineHighFreq = salineFreq[date]

'''


