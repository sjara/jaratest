from matplotlib import pyplot as plt

from jaratest.nick.inactivations import muscimolSessions as ms
from jaratest.nick import muscimolBehaviorPlots as mbp
reload(ms)
reload(mbp)

from jaratoolbox.colorpalette import TangoPalette as Tango
import matplotlib.patches as mpatches

#color patches for legend
red_patch = mpatches.Patch(color='red', label='0.25mg/ml')
orange_patch = mpatches.Patch(color=Tango['Orange2'], label='0.125mg/ml')
yellow_patch = mpatches.Patch(color=Tango['Butter2'], label='0.0625mg/ml')
black_patch = mpatches.Patch(color='k', label='Saline for muscimol 0.25mg/ml')
grey_patch = mpatches.Patch(color='0.5', label='Saline for muscimol 0.125mg/ml')



#Adap028 and adap029 dose response curves
plt.clf()
mbp.muscimol_plot('adap028',
                  ms.adap028['muscimol0250'],
                  ms.adap028['saline'])

mbp.muscimol_plot('adap028',
                  ms.adap028['muscimol0125'],
                  ms.adap028['saline_muscimol0125'],
                  mcolor=Tango['Orange2'],
                  msty='-',
                  ssty='-',
                  scolor='0.5')

#Dummy saline sessions, watch out
mbp.muscimol_plot('adap028',
                  ms.adap028['muscimol00625'],
                  ms.adap028['saline_muscimol0125'],
                  mcolor=Tango['Butter2'],
                  msty='-',
                  ssty='-',
                  scolor='0.5')

plt.legend(handles=[red_patch, black_patch, orange_patch, grey_patch, yellow_patch], loc=2)
plt.savefig('/tmp/adap028_doseResponse.png')


#Adap021 plot in progress
'''
plt.clf()
mbp.muscimol_plot('adap021',
                  ms.adap021['muscimol0250'],
                  ms.adap021['saline_muscimol0250'])
mbp.muscimol_plot('adap021',
                  ms.adap021['muscimol0125'],
                  ms.adap021['saline_muscimol0125'],
                  mcolor=Tango['Orange2'],
                  msty='-',
                  ssty='-',
                  scolor='0.5')

plt.legend(handles=[red_patch, black_patch, orange_patch, grey_patch], loc=2)
plt.savefig('/tmp/adap021_doseResponse_20160822a.png')

'''
