'''
Save speech files
'''

import speechsynth
reload(speechsynth)

speechsynth.BaPaRange(3, freqFactor=1, sampFreq=96000, outputDir='/var/tmp/speechsounds/')
speechsynth.BaDaRange(3, freqFactor=1, sampFreq=96000, outputDir='/var/tmp/speechsounds/')
