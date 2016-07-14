from jaratoolbox.test.nick.ephysExperiments import ephys_experiment
reload(ephys_experiment)
from jaratoolbox.test.nick.ephysExperiments.ephys_experiment import RecordingSite
from jaratoolbox.test.nick.ephysExperiments.ephys_experiment import EphysExperiment

site1 = RecordingSite(depth = 3509,
                      noiseburstEphysSession  = '2015-07-06_11-15-56',
                      laserPulseEphysSession  = '2015-07-06_11-18-36',
                      laserTrainEphysSession = '2015-07-06_11-21-26',
                      tuningCurveEphysSession  = '2015-07-06_11-25-58',
                      tuningCurveBehavIdentifier  = 'a',
                      bfEphysSession  = '2015-07-06_11-39-46',
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = '2015-07-06_11-42-37',
                      laserPulseEphysSession1mW = '2015-07-06_11-45-22',
                      goodTetrodes = [3, 6])

site2 = RecordingSite(depth = 3550, 
                      noiseburstEphysSession  = '2015-07-06_11-51-47',
                      laserPulseEphysSession  = '2015-07-06_11-54-51',
                      laserTrainEphysSession = '2015-07-06_11-58-17',
                      tuningCurveEphysSession  = '2015-07-06_12-01-53',
                      tuningCurveBehavIdentifier  = 'b',
                      bfEphysSession  = '2015-07-06_12-14-53',
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = '2015-07-06_12-17-13',
                      laserPulseEphysSession1mW = '2015-07-06_12-19-34',
                      goodTetrodes = [3, 6])
        
site3 = RecordingSite(depth = 3606, 
                      noiseburstEphysSession  = '2015-07-06_12-28-47',
                      laserPulseEphysSession  = '2015-07-06_12-31-21',
                      laserTrainEphysSession = '2015-07-06_12-34-00',
                      tuningCurveEphysSession  = '2015-07-06_12-37-29',
                      tuningCurveBehavIdentifier  = 'c',
                      bfEphysSession  = '2015-07-06_12-50-34',
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = '2015-07-06_12-53-57',
                      laserPulseEphysSession1mW = '2015-07-06_12-56-04',
                      goodTetrodes = [3, 6])

site4 = RecordingSite(depth = 3654, 
                      noiseburstEphysSession  = '2015-07-06_13-06-27',
                      laserPulseEphysSession  = '2015-07-06_13-09-00',
                      laserTrainEphysSession = '2015-07-06_13-11-25',
                      tuningCurveEphysSession  = '2015-07-06_13-15-01',
                      tuningCurveBehavIdentifier  = 'd',
                      bfEphysSession  = '2015-07-06_13-28-12',
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = '2015-07-06_13-30-00',
                      laserPulseEphysSession1mW = '2015-07-06_13-31-58',
                      goodTetrodes = [3, 6])
siteList = [site1, site2, site3, site4]

exp = EphysExperiment('pinp003', '2015-07-06')

exp.process_site(site4, 4)

'''
There are some problems with the current flow.

Good: 
- The document where the sessions are listed can be very concise, seperate from any plotting or processing code. 

- The plotting functions take arrays and bdata dictionaries, so they are easily reusable. UPDATE: funcs now do not need bdata dicts

- There are helper functions for calling the plotting code with a session input. 

Bad: 
 FIXED - The EphysExperiment class should not need to have processing code that is unique to a single expriment. This class should contain methods that are applicable to all experiments. 

 FIXED - The Multisession clustering code should make it possible to go back and examine a single session later (loading the appropriate clusters) without needing to assemble another multisession object together. 

The Plan: 

- Refactor the code that processes each site out of EphysExperiment. 
I should consider this class disposable anyway, since its methods may get moved elsewhere in jaratoolbox

- Idea: for plots that require behavior data, call the get_behavior method automatically before attempting to load the bdata and plot. 

- Add functions to the multisession clustering code to store the clusters for each session in the session's usual (i.e. not multisession) clustering directory. 

- The multisession object should also contain methods to deliver the data for a single cluster, single session. 


'''
