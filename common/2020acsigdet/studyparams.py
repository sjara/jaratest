''' This file contains all mice and behavior data associated with them.'''

STUDY_NAME = '2020acsigdet'

# mice used for inactivating entire AC
MUSC_MICE = ['band006', 'band008', 'band010']
PV_CHR2_MICE = ['band046', 'band051', 'band052']
CAMKII_ARCH_MICE = ['band011', 'band012']

# mice used for inactivating specific inhibitory cell types in AC
PV_ARCHT_MICE = ['band081', 'band087', 'band091', 'band093']
PV_ARCHT_WT_MICE = []
SOM_ARCHT_MICE = ['band065', 'band069', 'band070', 'band108', 'band110', 'band111']
SOM_ARCHT_WT_MICE = ['band066', 'band105', 'band112']

# lists of sessions of one type for each mouse
band006_muscimol = ['20161201a', '20161203a', '20161205a', '20161207a']
band006_saline = ['20161130a', '20161202a', '20161204a', '20161206a']

band008_muscimol = ['20161201a', '20161203a', '20161205a', '20161207a']
band008_saline = ['20161130a', '20161202a', '20161204a', '20161206a']

band010_muscimol = ['20161201a', '20161203a', '20161205a', '20161207a']
band010_saline = ['20161130a', '20161202a', '20161204a', '20161206a']

band017_3mW_laser = ['20170228a', '20170226a', '20170224a', '20170222a']

band020_3mW_laser = ['20170228a', '20170226a', '20170224a', '20170222a']

band046_3mW_laser = ['20180523a', '20180525a', '20180528a', '20180530a', '20180601a', '20180603a', '20180605a', '20180607a', '20180609a', '20180611a', '20180613a', '20180615a']
band046_3mW_control = ['20180522a', '20180524a', '20180526a', '20180529a', '20180531a', '20180602a', '20180604a', '20180606a', '20180608a', '20180610a', '20180612a', '20180614a']

band051_3mW_laser = ['20180418a', '20180420a', '20180422a', '20180424a', '20180426a', '20180428a', '20180430a', '20180502a']
band051_3mW_control = ['20180413a', '20180417a', '20180419a', '20180421a', '20180425a', '20180427a', '20180429a', '20180501a']

band052_3mW_laser = ['20180515a', '20180517a', '20180519a', '20180521a', '20180523a', '20180525a', '20180528a', '20180530a', '20180601a', '20180603a', '20180605a', '20180607a']
band052_3mW_control = ['20180513a', '20180516a', '20180518a', '20180520a', '20180522a', '20180524a', '20180526a', '20180529a', '20180531a', '20180602a', '20180604a', '20180606a']

band065_10mW_laser = ['20181018a', '20181020a', '20181021a', '20181023a', '20181024a', '20181026a', '20181027a', '20181029a']
band065_10mW_control = ['20181019a', '20181022a', '20181025a', '20181028a', '20181105a']

band066_10mW_laser = ['20190123a', '20190124a', '20190126a', '20190127a', '20190129a', '20190130a', '20190201a', '20190202a']
band066_10mW_control = ['20190125a', '20190128a', '20190131a', '20190203a']

band069_10mW_laser = ['20190123a', '20190124a', '20190126a', '20190127a', '20190129a', '20190130a', '20190201a', '20190202a']
band069_10mW_control = ['20190125a', '20190128a', '20190131a', '20190203a']

band070_10mW_laser = ['20181020a', '20181021a', '20181023a', '20181024a', '20181026a', '20181027a', '20181029a', '20181030a']
band070_10mW_control = ['20181019a', '20181022a', '20181025a', '20181028a', '20181105a']

band081_10mW_laser = ['20190307a', '20190308a', '20190310a', '20190311a', '20190313a', '20190314a', '20190316a', '20190317a']
band081_10mW_control = ['20190309a', '20190312a', '20190315a', '20190318a']

band087_10mW_laser = ['20190307a', '20190308a', '20190310a', '20190311a', '20190313a', '20190314a', '20190316a', '20190317a']
band087_10mW_control = ['20190309a', '20190312a', '20190315a', '20190318a']

band091_10mW_laser_bad = ['20200206a', '20200207a', '20200209a', '20200210a', '20200213a', '20200214a', '20200216a', '20200217a']
band091_10mW_control_bad = ['20200208a', '20200212a', '20200215a', '20200218a']
band091_10mW_laser = ['20200317a', '20200318a', '20200320a', '20200321a', '20200323a']
band091_10mW_control = ['20200319a', '20200322a', '20200324a']
band091_15mW_laser = ['20200301a', '20200302a', '20200303a', '20200305a', '20200306a', '20200308a', '20200311a', '20200312a']
band091_15mW_control = ['20200304a', '20200307a', '20200309a', '20200310a']
band091_10mW_unilateral = ['20200220a', '20200221a', '20200222a', '20200223a', '20200224a', '20200226a', '20200227a', '20200228a', '20200229a']

band093_5mW_laser = ['20200306a', '20200307a', '20200308a', '20200310a', '20200311a', '20200313a', '20200317a', '20200319a']
band093_5mW_control = ['20200309a', '20200312a', '20200318a', '20200320a']
band093_10mW_laser = ['20200131a', '20200201a', '20200203a', '20200204a', '20200206a', '20200207a', '20200209a', '20200210a']
band093_10mW_control = ['20200202a', '20200205a', '20200208a', '20200211a']
band093_15mW_laser = ['20200115a', '20200116a', '20200117a', '20200119a', '20200120a', '20200122a', '20200123a', '20200128a', '20200129a']
band093_15mW_control = ['20200118a', '20200121a', '20200124a', '20200130a']
band093_10mW_unilateral = ['20200224a', '20200226a', '20200228a', '20200229a', '20200301a', '20200302a', '20200303a', '20200304a', '20200305a']
band093_15mw_unilateral = ['20200212a', '20200213a', '20200214a', '20200216a', '20200217a', '20200218a', '20200220a', '20200221a', '20200222a']
band093_15mW_unilateral_control = ['20200215a', '20200219a', '20200223a']

band105_10mW_laser = ['20200305a', '20200306a', '20200308a', '20200309a', '20200311a', '20200312a', '20200317a', '20200318a']
band105_10mW_control = ['20200307a', '20200310a', '20200313a', '20200319a']
band105_15mW_laser = ['20200320a', '20200321a', '20200323a']
band105_15mW_control = ['20200322a', '20200324a']

band108_10mW_laser = ['20200305a', '20200306a', '20200308a']
band108_10mW_control = ['20200307a']

band110_10mW_laser = ['20200321a', '20200322a']
band110_10mW_control = ['20200323a']

band111_10mW_laser = ['20200321a', '20200322a']
band111_10mW_control = ['20200323a']

band112_10mW_laser = ['20200321a', '20200322a']
band112_10mW_control = ['20200323a']

# dictionaries for assigning sessions to mice
miceDict = {'band006': {'muscimol': band006_muscimol, 'saline': band006_saline},

            'band008': {'muscimol': band008_muscimol, 'saline': band008_saline},

            'band010': {'muscimol': band010_muscimol, 'saline': band010_saline},

            'band017': {'3mW laser': band017_3mW_laser},

            'band020': {'3mW laser': band020_3mW_laser},

            'band046': {'3mW laser': band046_3mW_laser, '3mW control': band046_3mW_control},

            'band051': {'3mW laser': band051_3mW_laser, '3mW control': band051_3mW_control},

            'band052': {'3mW laser': band052_3mW_laser, '3mW control': band052_3mW_control},

            'band065': {'10mW laser': band065_10mW_laser, '10mW control': band065_10mW_control},

            'band066': {'10mW laser': band066_10mW_laser, '10mW control': band066_10mW_control},

            'band069': {'10mW laser': band069_10mW_laser, '10mW control': band069_10mW_control},

            'band070': {'10mW laser': band070_10mW_laser, '10mW control': band070_10mW_control},

            'band081': {'10mW laser': band081_10mW_laser, '10mW control': band081_10mW_control},

            'band087': {'10mW laser': band087_10mW_laser, '10mW control': band087_10mW_control},

            'band091': {'10mW laser': band091_10mW_laser, '10mW control': band091_10mW_control,
                        '10mW unilateral': band091_10mW_unilateral},

            'band093': {'10mW laser': band093_10mW_laser, '10mW control': band093_10mW_control,
                        '15mW laser': band093_15mW_laser, '15mW control': band093_15mW_control,
                        '10mW unilateral': band093_10mW_unilateral},

            'band105': {'10mW laser': band105_10mW_laser, '10mW control': band105_10mW_control,
                        '15mW laser': band105_15mW_laser, '15mW control': band105_15mW_control},

            'band108': {'10mW laser': band108_10mW_laser, '10mW control': band108_10mW_control},

            'band110': {'10mW laser': band110_10mW_laser, '10mW control': band110_10mW_control},

            'band111': {'10mW laser': band111_10mW_laser, '10mW control': band111_10mW_control},

            'band112': {'10mW laser': band112_10mW_laser, '10mW control': band112_10mW_control}}

# lists of sessions before implantation for characterising behaviour
band046_unimplanted = ['20180'+str(day)+'a' for day in range(402,427)]
band047_unimplanted = ['20180'+str(day)+'a' for day in range(402,407)]+['20180'+str(day)+'a' for day in range(408,427)]
band048_unimplanted = ['20180'+str(day)+'a' for day in range(402,427)]
band049_unimplanted = ['20180'+str(day)+'a' for day in range(402,427)]
band051_unimplanted = ['20180'+str(day)+'a' for day in range(305,312)]
band052_unimplanted = ['20180'+str(day)+'a' for day in range(402,427)]
band053_unimplanted = ['20180'+str(day)+'a' for day in range(402,427)]

band065_unimplanted = ['2018100'+str(day)+'a' for day in range(1,9)]
band066_unimplanted = ['2018'+str(day)+'a' for day in range(1001,1032)]+['20181'+str(day)+'a' for day in range(101,121)]
band067_unimplanted = ['2018'+str(day)+'a' for day in range(1001,1032)]+['20181'+str(day)+'a' for day in range(101,121)]
band068_unimplanted = ['2018'+str(day)+'a' for day in range(1001,1032)]+['20181'+str(day)+'a' for day in range(101,121)]
band069_unimplanted = ['2018'+str(day)+'a' for day in range(1001,1032)]+['20181'+str(day)+'a' for day in range(101,109)]+['20181'+str(day)+'a' for day in range(110,121)]
band070_unimplanted = ['2018100'+str(day)+'a' for day in range(1,9)]
band071_unimplanted = ['2018'+str(day)+'a' for day in range(1001,1032)]+['20181'+str(day)+'a' for day in range(101,106)]+['20181'+str(day)+'a' for day in range(107,121)]

band078_unimplanted = ['201902'+str(day)+'a' for day in range(18,27)]+['20190'+str(day)+'a' for day in range(301,318)]
band079_unimplanted = ['201902'+str(day)+'a' for day in range(18,27)]+['20190'+str(day)+'a' for day in range(301,318)]
band080_unimplanted = ['201902'+str(day)+'a' for day in range(18,27)]+['20190'+str(day)+'a' for day in range(301,318)]
band081_unimplanted = ['201902'+str(day)+'a' for day in range(11,27)]
band082_unimplanted = ['201902'+str(day)+'a' for day in range(20,27)]+['20190'+str(day)+'a' for day in range(301,318)]
band083_unimplanted = ['201902'+str(day)+'a' for day in range(18,27)]+['20190'+str(day)+'a' for day in range(301,318)]
band084_unimplanted = ['201902'+str(day)+'a' for day in range(18,27)]+['20190'+str(day)+'a' for day in range(301,318)]
band085_unimplanted = ['201902'+str(day)+'a' for day in range(20,27)]+['20190'+str(day)+'a' for day in range(301,318)]
band086_unimplanted = ['201902'+str(day)+'a' for day in range(20,27)]+['20190'+str(day)+'a' for day in range(301,318)]
band087_unimplanted = ['201902'+str(day)+'a' for day in range(10,27)]

band088_unimplanted = ['201911'+str(day)+'a' for day in range(11,26)]+['2019120'+str(day)+'a' for day in range(2,6)]
band089_unimplanted = ['201911'+str(day)+'a' for day in range(11,26)]+['2019120'+str(day)+'a' for day in range(2,6)]
band090_unimplanted = ['201911'+str(day)+'a' for day in range(11,26)]+['2019120'+str(day)+'a' for day in range(2,6)]
band091_unimplanted = ['201911'+str(day)+'a' for day in range(11,26)]+['2019120'+str(day)+'a' for day in range(2,6)]
band092_unimplanted = ['201911'+str(day)+'a' for day in range(11,26)]+['2019120'+str(day)+'a' for day in range(2,6)]
band093_unimplanted = ['201911'+str(day)+'a' for day in range(11,26)]+['2019120'+str(day)+'a' for day in range(2,6)]
band094_unimplanted = ['201911'+str(day)+'a' for day in range(11,26)]+['2019120'+str(day)+'a' for day in range(2,6)]
band095_unimplanted = ['201911'+str(day)+'a' for day in range(11,26)]+['2019120'+str(day)+'a' for day in range(2,6)]
band096_unimplanted = ['201911'+str(day)+'a' for day in range(11,26)]+['2019120'+str(day)+'a' for day in range(2,6)]

band105_unimplanted = ['202002'+str(day)+'a' for day in range(18,24)]
band107_unimplanted = ['202002'+str(day)+'a' for day in range(16,24)]
band108_unimplanted = ['202002'+str(day)+'a' for day in range(16,24)]
band109_unimplanted = ['202002'+str(day)+'a' for day in range(16,24)]
band110_unimplanted = ['202002'+str(day)+'a' for day in range(24,30)]+['2020030'+str(day)+'a' for day in range(1,10)]
band111_unimplanted = ['202002'+str(day)+'a' for day in range(24,30)]+['2020030'+str(day)+'a' for day in range(1,10)]
band112_unimplanted = ['202002'+str(day)+'a' for day in range(24,30)]+['2020030'+str(day)+'a' for day in range(1,10)]
band113_unimplanted = ['202002'+str(day)+'a' for day in range(24,30)]+['2020030'+str(day)+'a' for day in range(1,10)]
band114_unimplanted = ['202002'+str(day)+'a' for day in range(24,30)]+['2020030'+str(day)+'a' for day in range(1,10)]
band115_unimplanted = ['202002'+str(day)+'a' for day in range(24,30)]+['2020030'+str(day)+'a' for day in range(1,10)]
band116_unimplanted = ['202002'+str(day)+'a' for day in range(24,30)]+['2020030'+str(day)+'a' for day in range(1,10)]
band117_unimplanted = ['202002'+str(day)+'a' for day in range(24,30)]+['2020030'+str(day)+'a' for day in range(1,10)]
band118_unimplanted = ['202002'+str(day)+'a' for day in range(24,30)]+['2020030'+str(day)+'a' for day in range(1,10)]
band119_unimplanted = ['202002'+str(day)+'a' for day in range(24,30)]+['2020030'+str(day)+'a' for day in range(1,10)]
band120_unimplanted = ['202002'+str(day)+'a' for day in range(24,30)]+['2020030'+str(day)+'a' for day in range(1,10)]

unimplanted_PVCHR2 = {'band046': band046_unimplanted, 'band047': band047_unimplanted, 'band048': band048_unimplanted,
                      'band049': band049_unimplanted, 'band051': band051_unimplanted, 'band052': band052_unimplanted,
                      'band053': band053_unimplanted}

unimplanted_PVARCHT = {'band078': band078_unimplanted, 'band079': band079_unimplanted, 'band080': band080_unimplanted,
                       'band081': band081_unimplanted, 'band082': band082_unimplanted, 'band083': band083_unimplanted,
                       'band084': band084_unimplanted, 'band085': band085_unimplanted, 'band086': band086_unimplanted,
                       'band087': band087_unimplanted, 'band088': band088_unimplanted, 'band089': band089_unimplanted,
                       'band090': band090_unimplanted, 'band091': band091_unimplanted, 'band092': band092_unimplanted,
                       'band093': band093_unimplanted, 'band094': band094_unimplanted, 'band095': band095_unimplanted,
                       'band096': band096_unimplanted, 'band113': band113_unimplanted, 'band114': band114_unimplanted,
                       'band115': band115_unimplanted, 'band116': band116_unimplanted, 'band117': band117_unimplanted,
                       'band118': band118_unimplanted, 'band119': band119_unimplanted, 'band120': band120_unimplanted}

unimplanted_SOMARCHT = {'band065': band065_unimplanted, 'band068': band068_unimplanted, 'band069': band069_unimplanted,
                        'band070': band070_unimplanted, 'band107': band107_unimplanted, 'band108': band108_unimplanted,
                        'band110': band108_unimplanted, 'band111': band108_unimplanted}

unimplanted_wt = {'band066': band066_unimplanted, 'band067': band067_unimplanted, 'band071': band071_unimplanted,
                  'band105': band105_unimplanted, 'band109': band109_unimplanted, 'band112': band112_unimplanted}
