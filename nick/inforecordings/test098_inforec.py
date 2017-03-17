import sys; sys.path.append('/home/nick/src')
from jaratoolbox import celldatabase as celldb
reload(celldb)

test098 = celldb.InfoRecording('test098')

## First experiment, 2016-07-26 ##
## Pipette is loaded with 0.25mg/ml muscimol
exp0 = test098.add_experiment('2016-07-26')
exp0.add_site(3100)

# First baseline session
exp0.add_session('12-38-47', 'a', 'noisebursts', 'am_tuning_curve')

# 2min session right before the injection
exp0.add_session('13-06-15', 'b', 'noisebursts', 'am_tuning_curve')

# 30min session after injecting ##UNKNOWN## amt of muscimol - see wiki
exp0.add_session('13-11-17', 'c', 'noisebursts', 'am_tuning_curve')

# 2min recordings every 10 mins
exp0.add_session('13-49-09', 'd', 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-00-26', 'e', 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-10-52', 'f', 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-22-31', 'g', 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-33-16', 'h', 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-42-42', 'i', 'noisebursts', 'am_tuning_curve')
exp0.add_session('14-52-07', 'j', 'noisebursts', 'am_tuning_curve')

## Second experiment, 2016-07-28 ##
## Pipette loaded with 0.125mg/ml muscimol

exp1 = test098.add_experiment('2016-07-28')
exp1.add_site(3200)

# First baseline session
exp1.add_session('15-05-26', 'a', 'noisebursts', 'am_tuning_curve') #20min

#2min session right before injection
exp1.add_session('15-26-35', 'b', 'noisebursts', 'am_tuning_curve') #2min

#30min post-injection session
exp1.add_session('15-30-20', 'c', 'noisebursts', 'am_tuning_curve') #30min

#2min sessions every 10 mins

exp1.add_session('16-10-14', 'd', 'noisebursts', 'am_tuning_curve') #2min
exp1.add_session('16-20-16', 'e', 'noisebursts', 'am_tuning_curve') #2min
exp1.add_session('16-30-18', 'f', 'noisebursts', 'am_tuning_curve') #2min
exp1.add_session('16-40-22', 'g', 'noisebursts', 'am_tuning_curve') #2min
exp1.add_session('16-50-12', 'h', 'noisebursts', 'am_tuning_curve') #2min
exp1.add_session('17-00-06', 'i', 'noisebursts', 'am_tuning_curve') #2min
