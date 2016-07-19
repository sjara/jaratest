from jaratoolbox.test.nick.ephysExperiments import ephys_experiment
reload(ephys_experiment)
from jaratoolbox.test.nick.ephysExperiments.ephys_experiment import RecordingSite
from jaratoolbox.test.nick.ephysExperiments.ephys_experiment import EphysExperiment

site1 = RecordingSite(depth = 2612,
                      noiseburstEphysSession  = '2015-07-01_18-12-05',
                      laserPulseEphysSession  = '2015-07-01_18-06-54',
                      laserTrainEphysSession = None,
                      tuningCurveEphysSession  = '2015-07-01_18-18-47',
                      tuningCurveBehavIdentifier  = 'a',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = '2015-07-01_18-36-00',
                      laserPulseEphysSession1mW = None,
                      goodTetrodes = [6])
site1.sessionList = ['2015-07-01_18-06-54', '2015-07-01_18-12-05', None, '2015-07-01_18-18-47', None, '2015-07-01_18-36-00', None] #site1's noiseburst and laserPulse sessions are reversed
        
site2 = RecordingSite(depth = 2660,
                      noiseburstEphysSession  = '2015-07-01_18-42-37',
                      laserPulseEphysSession  = '2015-07-01_18-45-15',
                      laserTrainEphysSession = '2015-07-01_18-48-18',
                      tuningCurveEphysSession  = '2015-07-01_18-55-15',
                      tuningCurveBehavIdentifier  = 'b',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                      #laserPulseEphysSession3mW  = '2015-07-01_18-51-53',
                      laserPulseEphysSession3mW  = None,
                      laserPulseEphysSession1mW = None,
                      goodTetrodes = [6])


site3 = RecordingSite(depth = 2710,
                      noiseburstEphysSession  = '2015-07-01_19-09-42',
                      laserPulseEphysSession  = '2015-07-01_19-13-36',
                      laserTrainEphysSession = '2015-07-01_19-16-32',
                      tuningCurveEphysSession  = '2015-07-01_19-30-41',
                      tuningCurveBehavIdentifier  = 'c',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = None,
                      #laserPulseEphysSession1mW = '2015-07-01_19-23-35',
                      laserPulseEphysSession1mW  = None,
                      goodTetrodes = [6])


site4 = RecordingSite(depth = 2800,
                      noiseburstEphysSession  = '2015-07-01_19-52-08',
                      laserPulseEphysSession  = '2015-07-01_19-49-07',
                      laserTrainEphysSession = '2015-07-01_19-54-43',
                      tuningCurveEphysSession  = '2015-07-01_19-58-34',
                      tuningCurveBehavIdentifier  = 'd',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = '2015-07-01_20-11-17',
                      laserPulseEphysSession1mW = '2015-07-01_20-14-20',
                      goodTetrodes = [3, 6])
site4.sessionList = ['2015-07-01_19-49-07', '2015-07-01_19-52-08', '2015-07-01_19-54-43', '2015-07-01_19-58-34', None,  '2015-07-01_20-11-17', '2015-07-01_20-14-20']  #site4's noiseburst and laserPulse sessions are reversed

site5 = RecordingSite(depth = 2900,
                      noiseburstEphysSession  = '2015-07-01_20-31-44',
                      laserPulseEphysSession  = '2015-07-01_20-25-09',
                      laserTrainEphysSession = '2015-07-01_20-28-03',
                      tuningCurveEphysSession  = '2015-07-01_20-39-59',
                      tuningCurveBehavIdentifier  = 'e',
                      bfEphysSession  = None,
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = '2015-07-01_20-34-08',
                      laserPulseEphysSession1mW = None,
                      goodTetrodes = [3, 6])
site5.sessionList = ['2015-07-01_20-25-09', '2015-07-01_20-28-03',  '2015-07-01_20-31-44', 
 '2015-07-01_20-39-59', None, None, None] #site5's noiseburst and laserPulse sessions are reversed

site6 = RecordingSite(depth = 3025,
                      noiseburstEphysSession  = '2015-07-01_21-01-24',
                      laserPulseEphysSession  = '2015-07-01_21-03-51',
                      laserTrainEphysSession = '2015-07-01_21-06-10',
                      tuningCurveEphysSession  = '2015-07-01_21-12-07',
                      tuningCurveBehavIdentifier  = 'f',
                      bfEphysSession  = '2015-07-01_21-24-44',
                      bfBehavIdentifier = None,
                      laserPulseEphysSession3mW  = None,
                      laserPulseEphysSession1mW = '2015-07-01_21-09-42',
                      goodTetrodes = [6])
site6.sessionList = ['2015-07-01_21-01-24', '2015-07-01_21-03-51',  '2015-07-01_21-06-10', '2015-07-01_21-12-07', '2015-07-01_21-24-44', None, None]

siteList = [site1, site2, site3, site4, site5, site6]

exp0701 = EphysExperiment('d1pi001', '2015-07-01', experimenter = 'lan')

exp0701.process_site(site5, 5)

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
