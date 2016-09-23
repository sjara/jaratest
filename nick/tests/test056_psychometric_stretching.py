from jaratest.nick.behavior import soundtypes
from jaratoolbox import behavioranalysis
from matplotlib import pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np

subject = 'amod006'
session = '20160920a'

# from http://www.mail-archive.com/matplotlib-users@lists.sourceforge.net/msg15465.html
def loose_autoscale_view(subplot, margin, tight=False,
scalex=True, scaley=True):
    """
    autoscale the view limits using the data limits. You can
    selectively autoscale only a single axis, eg, the xaxis by
    setting *scaley* to *False*.  The autoscaling preserves any
    axis direction reversal that has already been done.

    """
    # if image data only just use the datalim
    if scalex:
        if not subplot._autoscaleXon: return
        xshared = subplot._shared_x_axes.get_siblings(subplot)
        dl = [ax.dataLim for ax in xshared]
        bb = mtransforms.BboxBase.union(dl)
        xdiff = bb.intervalx[1] - bb.intervalx[0]
        x0 = bb.intervalx[0]-xdiff * margin
        x1 = bb.intervalx[1]+xdiff * margin
    if scaley:
        if not subplot._autoscaleYon: return
        yshared = subplot._shared_y_axes.get_siblings(subplot)
        dl = [ax.dataLim for ax in yshared]
        bb = mtransforms.BboxBase.union(dl)
        y0 = bb.intervaly[0]-(bb.intervaly[1]* margin)
        y1 = bb.intervaly[1]* (1+margin)

    if (tight or (len(subplot.images)>0 and
                    len(subplot.lines)==0 and
                    len(subplot.patches)==0)):
        if scalex:
            subplot.set_xbound(x0, x1)
        if scaley:
            subplot.set_ybound(y0, y1)
        return

    if scalex:
        XL = subplot.xaxis.get_major_locator().view_limits(x0, x1)
        subplot.set_xbound(XL)
    if scaley:
        YL = subplot.yaxis.get_major_locator().view_limits(y0, y1)
        subplot.set_ybound(YL)


(bdataObjs, bdataSoundTypes) = soundtypes.load_behavior_sessions_sound_type(subject, [session]) 

#Not because we are plotting small values...
# bdataObjs[0]['targetFrequency'] = bdataObjs[0]['targetFrequency'] * 1e3

plt.clf()
for indbdata, bdata in enumerate(bdataObjs):
    ax = plt.subplot(1, 2, indbdata+1)
    (pline, pcaps, pbars, pdots) = behavioranalysis.plot_frequency_psycurve(bdata)
    loose_autoscale_view(ax, 0.05, scaley=False)
    # plt.margins(x=0.1, y=0)
    # ax.autoscale(axis='x', tight=True)
plt.show()
