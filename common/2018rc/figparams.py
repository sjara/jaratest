'''
Common parameters for figures and data related to these figures.
'''

from jaratoolbox import colorpalette as cp
import matplotlib

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # So font is selectable in SVG

STUDY_NAME = '2018rc'

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

colp = {}
#colp['blueLaser'] = cp.TangoPalette['SkyBlue1']
colp['acColor'] = cp.TangoPalette['Chameleon3']
colp['astrColor'] = cp.TangoPalette['Plum2']

colp['sound'] = cp.TangoPalette['Butter2']

colp['MoreRewardR'] = cp.TangoPalette['ScarletRed1']
colp['MoreRewardL'] = cp.TangoPalette['SkyBlue2']

colp['MoveLeft'] = cp.TangoPalette['Orange2']
colp['MoveRight'] = cp.TangoPalette['Plum2'] #'#829910'


#7570B3 - blupurp
#E7298A  - pink
#C51A8A  - pink
#D95F02  - orange
#BCBD22  - olive
#829910  - olive/citron

'''
# To avoid converting text to paths
matplotlib.rcParams['svg.fonttype'] = 'none'

matplotlib.rcParams['axes.color_cycle'] = ???

colp = {}
colp['LowFreq'] = cp.TangoPalette['Orange2']

colp['HighFreq'] = cp.TangoPalette['SkyBlue2']


'''
