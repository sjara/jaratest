'''
Common parameters for figures and data related to these figures.
'''

from jaratoolbox import colorpalette as cp
import matplotlib

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # So font is selectable in SVG

STUDY_NAME = '2016astr'

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

colp = {}
colp['blueLaser'] = cp.TangoPalette['SkyBlue1']
colp['frontStrColor'] = cp.TangoPalette['Chameleon3']
colp['backStrColor'] = cp.TangoPalette['Plum2']

colp['sound'] = cp.TangoPalette['Butter2']

#colp['MidFreqR'] = cp.TangoPalette['ScarletRed1']
#colp['MidFreqL'] = cp.TangoPalette['Chameleon3']
colp['MidFreqR'] = cp.TangoPalette['ScarletRed1']
colp['MidFreqL'] = cp.TangoPalette['SkyBlue2']

#colp['muscimol'] = cp.TangoPalette['Orange2']
colp['muscimol'] = cp.TangoPalette['Chocolate2']

#colp['stimLeft'] = cp.TangoPalette['ScarletRed1']
#colp['stimRight'] = cp.TangoPalette['Chameleon3']
colp['stimLeft'] = cp.TangoPalette['Orange2']
colp['stimRight'] = '#829910'


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
