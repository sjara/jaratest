'''
This module contains all the animals tested in the reward change paradigm that we have ephys recording either from auditory cortex (AC) or auditory striatum (AStr).
'''

adap012 = ['20160219a','20160223a','20160224a','20160226a','20160227a','20160228a','20160229a'] #some sessions have mid freq
                             
adap005 = ['20151118a','20151119a','20151120a','20151121a','20151122a','20151123a','20151124a'] #same_left_right block transition

adap013 = ['20160216a','20160217a','20160309a','20160310a','20160311a','20160312a','20160313a','20160314a'] #some of them are of same_right_left block transition

adap015 = ['20160302a','20160309a','20160310a','20160311a','20160312a','20160313a','20160314a','20160315a'] #some of them are of same_right_left block transition

adap017 = ['20160219a','20160222a','20160223a','20160224a','20160226a','20160301a','20160302a','20160309a','20160310a','20160311a','20160312a','20160313a','20160314a'] #some of them are of same_right_left block transition
          
adap071 = ['20171002a','20171003a','20171004a','20171005a','20171006a','20171007a']#some sessions have mid freq
                              
adap067 = ['20171023a','20171024a','20171025a','20171026a','20171027a','20171028a']#some sessions have mid freq

gosi004 = ['20170127a','20170128a','20170129a','20170130a','20170131a','20170201a']
           
gosi008 = ['20170210a','20170212a','20170213a','20170214a','20170215a','20170216a']

gosi001 = ['20170406a','20170407a','20170408a','20170409a','20170410a','20170411a']

gosi010 = ['20170406a','20170407a','20170408a','20170409a','20170410a','20170411a']

acAnimals = {'gosi001': gosi001,
             'gosi004': gosi004,
             'gosi008': gosi008,
             'gosi010': gosi010,
             'adap067': adap067,
             'adap071': adap071}

astrAnimals = {'adap005': adap005,
               'adap012': adap012,
               'adap013': adap013,
               'adap015': adap015,
               'adap017': adap017}

animals = {'gosi001': gosi001,
           'gosi004': gosi004,
           'gosi008': gosi008,
           'gosi010': gosi010,
           'adap067': adap067,
           'adap071': adap071,
           'adap005': adap005,
           'adap012': adap012,
           'adap013': adap013,
           'adap015': adap015,
           'adap017': adap017}
