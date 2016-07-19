from jaratoolbox.test.nick.ephysExperiments import ephys_experiment
reload(ephys_experiment)
from jaratoolbox.test.nick.ephysExperiments.ephys_experiment import RecordingSite
from jaratoolbox.test.nick.ephysExperiments.ephys_experiment import EphysExperiment

site1 = RecordingSite(depth = 2750,
                      noiseburstEphysSession  = '2015-07-07_14-10-13',
                      laserPulseEphysSession  = '2015-07-07_14-11-42',
                      laserTrainEphysSession = '2015-07-07_14-14-00',
                      tuningCurveEphysSession  = '2015-07-07_14-17-54',
                      tuningCurveBehavIdentifier  = 'a',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = None,
                      laserPulseEphysSession1mW = None,
                      goodTetrodes = [3])

        
site2 = RecordingSite(depth = 2900,
                      noiseburstEphysSession  = '2015-07-07_15-12-17',
                      laserPulseEphysSession  = '2015-07-07_15-14-12',
                      laserTrainEphysSession = '2015-07-07_15-16-18',
                      tuningCurveEphysSession  = '2015-07-07_15-18-44',
                      tuningCurveBehavIdentifier  = 'b',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = None,
                      laserPulseEphysSession1mW = None,
                      goodTetrodes = [3])


site3 = RecordingSite(depth = 3025,
                      noiseburstEphysSession  = '2015-07-07_16-04-26',
                      laserPulseEphysSession  = '2015-07-07_16-06-32',
                      laserTrainEphysSession = '2015-07-07_16-08-28',
                      tuningCurveEphysSession  = '2015-07-07_16-12-41',
                      tuningCurveBehavIdentifier  = 'c',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = None,
                      laserPulseEphysSession1mW  = None,
                      goodTetrodes = [3,6])
#the clustering was only run on tetrode 3?

site4 = RecordingSite(depth = 3075,
                      noiseburstEphysSession  = '2015-07-07_16-34-24',
                      laserPulseEphysSession  = '2015-07-07_16-36-42',
                      laserTrainEphysSession = '2015-07-07_16-38-59',
                      tuningCurveEphysSession  = '2015-07-07_16-42-17',
                      tuningCurveBehavIdentifier  = 'd',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                     #laserPulseEphysSession3mW  = '2015-07-07_16-57-40',
                     #laserPulseEphysSession1mW = '2015-07-07_16-55-51',
                      laserPulseEphysSession3mW  = None,
                      laserPulseEphysSession1mW = None,
                      goodTetrodes = [3, 6])


site5 = RecordingSite(depth = 3125,
                      noiseburstEphysSession  = '2015-07-07_17-02-39',
                      laserPulseEphysSession  = '2015-07-07_17-05-02',
                      laserTrainEphysSession = '2015-07-07_17-07-13',
                      tuningCurveEphysSession  = '2015-07-07_17-10-30',
                      tuningCurveBehavIdentifier  = 'e',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                      #laserPulseEphysSession3mW  = '2015-07-07_17-26-58',
                      #laserPulseEphysSession1mW = '2015-07-07_17-25-32',
                      laserPulseEphysSession3mW  = None,
                      laserPulseEphysSession1mW = None,
                      goodTetrodes = [3, 6])


site6 = RecordingSite(depth = 3200,
                      noiseburstEphysSession  = '2015-07-07_17-31-32',
                      laserPulseEphysSession  = '2015-07-07_17-33-53',
                      laserTrainEphysSession = '2015-07-07_17-36-05',
                      tuningCurveEphysSession  = '2015-07-07_17-39-12',
                      tuningCurveBehavIdentifier  = 'f',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = '2015-07-07_17-52-09',
                      laserPulseEphysSession1mW = '2015-07-07_17-54-00',
                      goodTetrodes = [3,6])


site7 = RecordingSite(depth = 3275,
                      noiseburstEphysSession  = '2015-07-07_18-01-55',
                      laserPulseEphysSession  = '2015-07-07_18-03-53',
                      laserTrainEphysSession = '2015-07-07_18-05-36',
                      tuningCurveEphysSession  = '2015-07-07_18-08-36',
                      tuningCurveBehavIdentifier  = 'g',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = '2015-07-07_18-22-56',
                      laserPulseEphysSession1mW = '2015-07-07_18-24-20',
                      goodTetrodes = [3,4,6])

site8 = RecordingSite(depth = 3325,
                      noiseburstEphysSession  = '2015-07-07_18-29-42',
                      laserPulseEphysSession  = '2015-07-07_18-32-16',
                      laserTrainEphysSession = '2015-07-07_18-34-54',
                      tuningCurveEphysSession  = '2015-07-07_18-42-14',
                      tuningCurveBehavIdentifier  = 'h',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = '2015-07-07_18-53-39',
                      laserPulseEphysSession1mW = None,
                      goodTetrodes = [3,4,6])

siteList = [site1, site2, site3, site4, site5, site6, site7, site8]

exp0707 = EphysExperiment('d1pi001', '2015-07-07', experimenter = 'lan')

exp0707.process_site(site8, 8)

'''
There are some problems with the current flow.

Good: 
- The document where the sessions are listed can be very concise, seperate from any plotting or processing code. 

- The plotting functions take arrays and bdata dictionaries, so they are easily reusable

- There are helper functions for calling the plotting code with a session input. 

Bad: 
 - The EphysExperiment class should not need to have processing code that is unique to a single expriment. This class should contain methods that are applicable to all experiments. 

- The Multisession clustering code should make it possible to go back and examine a single session later (loading the appropriate clusters) without needing to assemble another multisession object together. 

The Plan: 

- Refactor the code that processes each site out of EphysExperiment. 
I should consider this class disposable anyway, since its methods may get moved elsewhere in jaratoolbox

- Idea: for plots that require behavior data, call the get_behavior method automatically before attempting to load the bdata and plot. 

- Add functions to the multisession clustering code to store the clusters for each session in the session's usual (i.e. not multisession) clustering directory. 

- The multisession object should also contain methods to deliver the data for a single cluster, single session. 


'''
