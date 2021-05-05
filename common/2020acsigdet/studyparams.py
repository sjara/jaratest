''' This file contains all mice and behavior data associated with them.'''

STUDY_NAME = '2020acsigdet'

# parameters for data analysis
REACTION_TIME_CUTOFF = 0.0 # in seconds

# mice used for inactivating entire AC
MUSC_MICE = ['band006', 'band008', 'band010']
PV_CHR2_MICE = ['band046', 'band051', 'band052', 'band129', 'band130', 'band132', 'band133', 'band134', 'band135']
CAMKII_ARCH_MICE = ['band011', 'band012']

# mice used for inactivating specific inhibitory cell types in AC
PV_ARCHT_MICE = ['band081', 'band087', 'band091', 'band093', 'band113', 'band116', 'band117', 'band119', 'band120', 'band136', 'band137', 'band141', 'band142']
PV_ARCHT_WT_MICE = ['band143', 'band144']
SOM_ARCHT_MICE = ['band065', 'band069', 'band070', 'band108', 'band110', 'band111', 'band121', 'band124', 'band125', 'band147', 'band149', 'band150']
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

band110_10mW_laser = ['20200615a', '20200616a', '20200618a', '20200619a', '20200621a', '20200622a', '20200625a', '20200626a']
band110_10mW_control = ['20200617a', '20200620a', '20200624a', '20200627a']
band110_15mW_laser = ['20200628a', '20200629a', '20200701a', '20200717a', '20200719a', '20200720a', '20200722a', '20200723a']
band110_15mW_control = ['20200630a', '20200718a', '20200721a', '20200724a']

band111_10mW_laser = ['20200613a', '20200614a', '20200616a', '20200617a', '20200619a', '20200620a', '20200622a', '20200623a']
band111_10mW_control = ['20200615a', '20200618a', '20200621a', '20200624a']
band111_15mW_laser = ['20200625a', '20200626a', '20200628a', '20200629a', '20200701a', '20200713a', '20200715a', '20200716a']
band111_15mW_control = ['20200627a', '20200630a', '20200714a', '20200717a']
band111_5mW_laser = ['20200718a', '20200719a', '20200721a', '20200722a', '20200724a', '20200725a', '20200727a', '20200728a']
band111_5mW_control = ['20200720a', '20200723a', '20200726a', '20200729a']

band112_10mW_laser = ['20200608a', '20200609a', '20200611a', '20200612a', '20200614a', '20200615a', '20200617a', '20200618a']
band112_10mW_control = ['20200610a', '20200613a', '20200616a', '20200619a']
band112_15mW_laser = ['20200620a', '20200621a', '20200623a', '20200624a', '20200626a', '20200627a', '20200629a', '20200630a']
band112_15mW_control = ['20200622a', '20200625a', '20200628a', '20200701a']
band112_5mW_laser = ['20200713a', '20200714a', '20200716a', '20200717a', '20200719a', '20200720a', '20200722a', '20200723a']
band112_5mW_control = ['20200715a', '20200718a', '20200721a', '20200724a']

band113_10mW_laser = ['20200923a', '20200924a', '20200926a', '20200927a', '20200929a', '20200930a', '20201002a', '20201003a']
band113_10mW_control = ['20200922a', '20200925a', '20200928a', '20201001a']
band113_5mW_laser = ['20200823a','20200824a','20200826a','20200827a','20200829a','20200830a','20200906a','20200907a']
band113_5mW_control = ['20200822a','20200825a','20200828a','20200831a']

band116_10mW_laser = ['20200923a', '20200924a', '20200926a', '20200927a', '20200929a', '20200930a', '20201002a', '20201003a']
band116_10mW_control = ['20200922a', '20200925a', '20200928a', '20201001a']
band116_5mW_laser = ['20200823a','20200824a','20200826a','20200827a','20200829a','20200830a','20200906a','20200907a']
band116_5mW_control = ['20200822a','20200825a','20200828a','20200831a']

band117_10mW_laser = ['20201023a', '20201024a', '20201026a', '20201027a', '20201029a', '20201030a', '20201101a', '20201102a']
band117_10mW_control = ['20201025a', '20201028a', '20201031a', '20201103a']

band119_10mW_laser = ['20201023a', '20201024a', '20201026a', '20201027a', '20201029a', '20201030a', '20201101a', '20201102a']
band119_10mW_control = ['20201025a', '20201028a', '20201031a', '20201103a']

band120_10mW_laser = ['20201023a', '20201024a', '20201026a', '20201027a', '20201029a', '20201030a', '20201101a', '20201102a']
band120_10mW_control = ['20201025a', '20201028a', '20201031a', '20201103a']

band121_10mW_laser = ['20200729a', '20200730a', '20200801a', '20200802a', '20200804a', '20200805a', '20200807a', '20200808a']
band121_10mW_control = ['20200731a', '20200803a', '20200806a', '20200809a']
band121_15mW_laser = ['20200810a', '20200811a', '20200813a', '20200814a', '20200816a', '20200817a', '20200819a', '20200820a']
band121_15mW_control = ['20200812a', '20200815a', '20200818a', '20200821a']
band121_5mW_laser = ['20200717a', '20200718a', '20200720a', '20200721a', '20200723a', '20200724a', '20200726a', '20200727a']
band121_5mW_control = ['20200719a', '20200722a', '20200725a', '20200728a']

band124_10mW_laser = ['20200729a', '20200730a', '20200801a', '20200802a', '20200804a', '20200805a', '20200807a', '20200808a']
band124_10mW_control = ['20200731a', '20200803a', '20200806a', '20200809a']
band124_15mW_laser = ['20200810a', '20200811a', '20200813a', '20200814a', '20200816a', '20200817a', '20200819a', '20200820a', '20200821a']
band124_15mW_control = ['20200812a', '20200815a', '20200818a', '20200822a']
band124_5mW_laser = ['20200717a', '20200718a', '20200720a', '20200721a', '20200723a', '20200724a', '20200726a', '20200727a']
band124_5mW_control = ['20200719a', '20200722a', '20200725a', '20200728a']

band125_10mW_laser = ['20200729a', '20200730a', '20200801a', '20200802a', '20200804a', '20200805a', '20200807a', '20200808a']
band125_10mW_control = ['20200731a', '20200803a', '20200806a', '20200809a']
band125_15mW_laser = ['20200810a', '20200811a', '20200813a', '20200814a', '20200816a', '20200817a', '20200819a', '20200820a']
band125_15mW_control = ['20200812a', '20200815a', '20200818a', '20200821a']
band125_5mW_laser = ['20200717a', '20200718a', '20200720a', '20200721a', '20200723a', '20200724a', '20200726a', '20200727a']
band125_5mW_control = ['20200719a', '20200722a', '20200725a', '20200728a']

band126_10mW_laser = ['20201020a', '20201023a', '20201025a', '20201028a', '20201030a', '20201101a', '20201102a', '20201104a']
band126_10mW_control = ['20201024a', '20201029a', '20201031a', '20201103a']

band129_3mW_laser = ['20201123a', '20201124a', '20201206a', '20201207a', '20201208a', '20201210a', '20201212a', '20201213a']
band129_3mW_control = ['20201120a', '20201205a', '20201209a', '20201211a']

band130_3mW_laser = ['20201123a', '20201124a', '20201206a', '20201207a', '20201208a', '20201210a', '20201212aa', '20201213a']
band130_3mW_control = ['20201120a', '20201205a', '20201209a', '20201211a']

band132_3mW_laser = ['20201123a', '20201124a', '20201206a', '20201207a', '20201208a', '20201212a', '20201213a', '20201215a', '20210204a', '20210208a', '20210210a', '20210212a', '20210215a', '20210216a']
band132_3mW_control = ['20201120a', '20201205a', '20201211a', '20201214a', '20210207a', '20210209a', '20210213a', '20210217a', '20210218a']

band133_3mW_laser = ['20201002a', '20201003a', '20201005a', '20201006a', '20201008a', '20201009a', '20201018a', '20201019a']
band133_3mW_control = ['20201001a', '20201004a', '20201007a', '20201017a']

band134_3mW_laser = ['20201003a', '20201004a', '20201006a', '20201007a', '20201009a', '20201017a', '20201019a', '20201020a']
band134_3mW_control = ['20201002a', '20201005a', '20201008a', '20201018a']

band135_3mW_laser = ['20201025a', '20201028a', '20201029a', '20201031a', '20201101a', '20201103a', '20201104a', '20201112a']
band135_3mW_control = ['20201027a', '20201030a', '20201102a', '20201105a']

band136_10mW_laser = ['20201208a', '20201209a', '20201211a', '20201212a', '20201215a']
band136_10mW_control = ['20201207a', '20201210a', '20201214a']

band137_10mW_laser = ['20210126a', '20210127a', '20210129a', '20210130a', '20210201a', '20210202a', '20210203a', '20210205a']
band137_10mW_control = ['20210125a', '20210128a', '20210131a', '20210204a']

band141_10mW_laser = ['20201208a', '20201209a', '20201211a', '20201212a', '20201214a', '20201215a', '20201218a', '20201219a']
band141_10mW_control = ['20201207a', '20201210a', '20201213a', '20201217a']

band142_10mW_laser = ['20201208a', '20201209a', '20201211a', '20201212a', '20201214a', '20201215a', '20201218a', '20201219a']
band142_10mW_control = ['20201207a', '20201210a', '20201213a', '20201217a']

band143_10mW_laser = ['20210120a', '20210121a', '20210123a']
band143_10mW_control = ['20210119a', '20210122a']

band144_10mW_laser = ['20210120a', '20210121a', '20210123a', '20210124a', '20210126a', '20210127a', '20210129a', '20210130a'] # green laser
band144_10mW_control = ['20210119a', '20210122a', '20210125a', '20210128a']
band144_3mW_laser = ['20210212a', '20210213a', '20210215a', '20210216a', '20210218a', '20210219a']
band144_3mW_control = ['20210211a', '20210214a', '20210217a']

band147_10mW_laser = ['20210413a', '20210416a', '20210417a']
band147_10mW_control = ['20210412a', '20210415a', '20210418a']

band149_10mW_laser = ['20210413a', '20210416a', '20210417a', '20210419a', '20210422a','20210423a','20210425a','20210428a','20210429a','20210430a','20210501a']
band149_10mW_control = ['20210409a', '20210412a', '20210415a', '20210418a', '20210424a','20210427a']

band150_10mW_laser = ['20210404a', '20210405a', '20210407a', '20210408a', '20210410a', '20210411a', '20210413a', '20210416a', '20210417a', '20210419a', '20210422a','20210423a','20210425a','20210427a']
band150_10mW_control = ['20210406a', '20210409a', '20210412a', '20210415a', '20210418a', '20210424a']

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

            'band111': {'5mW laser': band111_5mW_laser, '5mW control': band111_5mW_control,
                        '10mW laser': band111_10mW_laser, '10mW control': band111_10mW_control,
                        '15mW laser': band111_15mW_laser, '15mW control': band111_15mW_control},

            'band112': {'5mW laser': band112_5mW_laser, '5mW control': band112_5mW_control,
                        '10mW laser': band112_10mW_laser, '10mW control': band112_10mW_control,
                        '15mW laser': band112_15mW_laser, '15mW control': band112_15mW_control},

            'band113': {'5mW laser': band113_5mW_laser, '5mW control': band113_5mW_control,
                        '10mW laser': band113_10mW_laser, '10mW control': band113_10mW_control},

            'band116': {'5mW laser': band116_5mW_laser, '5mW control': band116_5mW_control,
                        '10mW laser': band116_10mW_laser, '10mW control': band116_10mW_control},

            'band117': {'10mW laser': band117_10mW_laser, '10mW control': band117_10mW_control},

            'band119': {'10mW laser': band119_10mW_laser, '10mW control': band119_10mW_control},

            'band120': {'10mW laser': band120_10mW_laser, '10mW control': band120_10mW_control},

            'band121': {'5mW laser': band121_5mW_laser, '5mW control': band121_5mW_control,
                        '10mW laser': band121_10mW_laser, '10mW control': band121_10mW_control,
                        '15mW laser': band121_15mW_laser, '15mW control': band121_15mW_control},

            'band124': {'5mW laser': band124_5mW_laser, '5mW control': band124_5mW_control,
                        '10mW laser': band124_10mW_laser, '10mW control': band124_10mW_control,
                        '15mW laser': band124_15mW_laser, '15mW control': band124_15mW_control},

            'band125': {'5mW laser': band125_5mW_laser, '5mW control': band125_5mW_control,
                        '10mW laser': band125_10mW_laser, '10mW control': band125_10mW_control,
                        '15mW laser': band125_15mW_laser, '15mW control': band125_15mW_control},

            'band126': {'10mW laser': band126_10mW_laser, '10mW control': band126_10mW_control},

            'band129': {'3mW laser': band129_3mW_laser, '3mW control': band129_3mW_control},

            'band130': {'3mW laser': band130_3mW_laser, '3mW control': band130_3mW_control},

            'band132': {'3mW laser': band132_3mW_laser, '3mW control': band132_3mW_control},

            'band133': {'3mW laser': band133_3mW_laser, '3mW control': band133_3mW_control},

            'band134': {'3mW laser': band134_3mW_laser, '3mW control': band134_3mW_control},

            'band135': {'3mW laser': band135_3mW_laser, '3mW control': band135_3mW_control},

            'band136': {'10mW laser': band136_10mW_laser, '10mW control': band136_10mW_control},

            'band137': {'10mW laser': band137_10mW_laser, '10mW control': band137_10mW_control},

            'band141': {'10mW laser': band141_10mW_laser, '10mW control': band141_10mW_control},

            'band142': {'10mW laser': band142_10mW_laser, '10mW control': band142_10mW_control},

            'band143': {'10mW laser': band143_10mW_laser, '10mW control': band143_10mW_control},

            'band144': {'10mW laser': band144_10mW_laser, '10mW control': band144_10mW_control,
                        '3mW laser': band144_3mW_laser, '3mW control': band144_3mW_control},

            'band147': {'10mW laser': band147_10mW_laser, '10mW control': band147_10mW_control},

            'band149': {'10mW laser': band149_10mW_laser, '10mW control': band149_10mW_control},

            'band150': {'10mW laser': band150_10mW_laser, '10mW control': band150_10mW_control}}

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

band121_unimplanted = ['202006'+str(day)+'a' for day in range(10,21)]
band122_unimplanted = ['202006'+str(day)+'a' for day in range(10,21)]
band124_unimplanted = ['202006'+str(day)+'a' for day in range(10,21)]
band125_unimplanted = ['202006'+str(day)+'a' for day in range(10,21)]

band128_unimplanted = ['2020100'+str(day)+'a' for day in range(1,10)] + ['202010'+str(day)+'a' for day in range(15,24)] + ['202010'+str(day)+'a' for day in range(25,32)]
band129_unimplanted = ['2020100'+str(day)+'a' for day in range(1,10)] + ['202010'+str(day)+'a' for day in range(15,32)]
band130_unimplanted = ['2020100'+str(day)+'a' for day in range(1,10)] + ['202010'+str(day)+'a' for day in range(15,32)]
band132_unimplanted = ['2020100'+str(day)+'a' for day in range(1,10)] + ['202010'+str(day)+'a' for day in range(15,32)]
band133_unimplanted = ['2020080'+str(day)+'a' for day in range(3,10)] + ['202010'+str(day)+'a' for day in range(15,32)]
band134_unimplanted = ['2020080'+str(day)+'a' for day in range(3,10)] + ['202010'+str(day)+'a' for day in range(15,32)]
band135_unimplanted = ['2020080'+str(day)+'a' for day in range(3,10)] + ['202010'+str(day)+'a' for day in range(15,26)] + ['202010'+str(day)+'a' for day in range(27,32)]

band136_unimplanted = ['2020110'+str(day)+'a' for day in range(1,6)] + ['202011'+str(day)+'a' for day in range(11,16)]
band137_unimplanted = ['2020110'+str(day)+'a' for day in range(1,6)] + ['202011'+str(day)+'a' for day in range(11,16)]
band139_unimplanted = ['2020110'+str(day)+'a' for day in range(3,6)] + ['202011'+str(day)+'a' for day in range(11,15)]+ ['202011'+str(day)+'a' for day in range(21,24)]
band140_unimplanted = ['2020110'+str(day)+'a' for day in range(1,6)] + ['202011'+str(day)+'a' for day in range(11,24)]
band141_unimplanted = ['2020110'+str(day)+'a' for day in range(1,6)] + ['202011'+str(day)+'a' for day in range(11,20)]
band142_unimplanted = ['2020110'+str(day)+'a' for day in range(1,6)] + ['202011'+str(day)+'a' for day in range(11,20)]
band143_unimplanted = ['2020120'+str(day)+'a' for day in range(4,10)] + ['202012'+str(day)+'a' for day in range(10,16)]
band144_unimplanted = ['2020120'+str(day)+'a' for day in range(4,10)] + ['202012'+str(day)+'a' for day in range(10,16)]

band146_unimplanted = ['2021030'+str(day)+'a' for day in range(2,9)]
band147_unimplanted = ['2021030'+str(day)+'a' for day in range(5,9)]
band148_unimplanted = ['2021030'+str(day)+'a' for day in range(1,9)]
band149_unimplanted = ['2021030'+str(day)+'a' for day in range(4,9)]
band150_unimplanted = ['2021030'+str(day)+'a' for day in range(1,9)]


unimplanted_PVCHR2 = {'band046': band046_unimplanted, 'band047': band047_unimplanted, 'band048': band048_unimplanted,
                      'band049': band049_unimplanted, 'band051': band051_unimplanted, 'band052': band052_unimplanted,
                      'band053': band053_unimplanted, 'band128': band128_unimplanted, 'band129': band129_unimplanted,
                      'band130': band130_unimplanted, 'band132': band132_unimplanted, 'band133': band133_unimplanted,
                      'band134': band134_unimplanted, 'band135': band135_unimplanted}

unimplanted_PVARCHT = {'band078': band078_unimplanted, 'band079': band079_unimplanted, 'band080': band080_unimplanted,
                       'band081': band081_unimplanted, 'band082': band082_unimplanted, 'band083': band083_unimplanted,
                       'band084': band084_unimplanted, 'band085': band085_unimplanted, 'band086': band086_unimplanted,
                       'band087': band087_unimplanted, 'band088': band088_unimplanted, 'band089': band089_unimplanted,
                       'band090': band090_unimplanted, 'band091': band091_unimplanted, 'band092': band092_unimplanted,
                       'band093': band093_unimplanted, 'band094': band094_unimplanted, 'band095': band095_unimplanted,
                       'band096': band096_unimplanted, 'band113': band113_unimplanted, 'band114': band114_unimplanted,
                       'band115': band115_unimplanted, 'band116': band116_unimplanted, 'band117': band117_unimplanted,
                       'band118': band118_unimplanted, 'band119': band119_unimplanted, 'band120': band120_unimplanted,
                       'band136': band136_unimplanted, 'band137': band137_unimplanted, 'band141': band141_unimplanted,
                       'band142': band142_unimplanted}

unimplanted_SOMARCHT = {'band065': band065_unimplanted, 'band068': band068_unimplanted, 'band069': band069_unimplanted,
                        'band070': band070_unimplanted, 'band107': band107_unimplanted, 'band108': band108_unimplanted,
                        'band110': band108_unimplanted, 'band111': band108_unimplanted, 'band121': band121_unimplanted,
                        'band122': band122_unimplanted, 'band124': band124_unimplanted, 'band125': band125_unimplanted,
                        'band146': band146_unimplanted, 'band147': band147_unimplanted, 'band148': band148_unimplanted,
                        'band149': band149_unimplanted, 'band150': band150_unimplanted}

unimplanted_SOMCRE = {'band066': band066_unimplanted, 'band067': band067_unimplanted, 'band071': band071_unimplanted,
                      'band105': band105_unimplanted, 'band109': band109_unimplanted, 'band112': band112_unimplanted}

unimplanted_PVCRE = {'band139': band139_unimplanted, 'band140': band140_unimplanted, 'band143': band143_unimplanted,
                     'band144': band144_unimplanted}
