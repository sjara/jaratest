import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os

os.chdir('D:/test128/')
df_hi = pd.read_csv(r'D:\test128\ROImeasures_high.csv')
df_lo = pd.read_csv(r'D:\test128\ROImeasures_low.csv')
df_lo2 = pd.read_csv(r'D:\test128\ROImeasures_low2.csv')

#convert raw grey values to percents
hiROI1 = df_hi.ROI1.values
hiROI1 = (hiROI1 - min(hiROI1))/(max(hiROI1) - min(hiROI1))
hiROI2 = df_hi.ROI2.values
hiROI2 = (hiROI2 - min(hiROI2))/(max(hiROI2) - min(hiROI2))
hiROI3 = df_hi.ROI3.values
hiROI3 = (hiROI3 - min(hiROI3))/(max(hiROI3) - min(hiROI3))
hiROI4 = df_hi.ROI4.values
hiROI4 = (hiROI4 - min(hiROI4))/(max(hiROI4) - min(hiROI4))
hiROI5 = df_hi.ROI5.values
hiROI5 = (hiROI5 - min(hiROI5))/(max(hiROI5) - min(hiROI5))
hiROI6 = df_hi.ROI6.values
hiROI6 = (hiROI6 - min(hiROI6))/(max(hiROI6) - min(hiROI6))

loROI1 = df_lo.ROI1.values
loROI1 = (loROI1 - min(loROI1))/(max(loROI1) - min(loROI1))
loROI2 = df_lo.ROI2.values
loROI2 = (loROI2 - min(loROI2))/(max(loROI2) - min(loROI2))
loROI3 = df_lo.ROI3.values
loROI3 = (loROI3 - min(loROI3))/(max(loROI3) - min(loROI3))
loROI4 = df_lo.ROI4.values
loROI4 = (loROI4 - min(loROI4))/(max(loROI4) - min(loROI4))
loROI5 = df_lo.ROI5.values
loROI5 = (loROI5 - min(loROI5))/(max(loROI5) - min(loROI5))
loROI6 = df_lo.ROI6.values
loROI6 = (loROI6 - min(loROI6))/(max(loROI6) - min(loROI6))

lo2ROI1 = df_lo2.ROI1.values
lo2ROI1 = (lo2ROI1 - min(lo2ROI1))/(max(lo2ROI1) - min(lo2ROI1))
lo2ROI2 = df_lo2.ROI2.values
lo2ROI2 = (lo2ROI2 - min(lo2ROI2))/(max(lo2ROI2) - min(lo2ROI2))
lo2ROI3 = df_lo2.ROI3.values
lo2ROI3 = (lo2ROI3 - min(lo2ROI3))/(max(lo2ROI3) - min(lo2ROI3))
lo2ROI4 = df_lo2.ROI4.values
lo2ROI4 = (lo2ROI4 - min(lo2ROI4))/(max(lo2ROI4) - min(lo2ROI4))
lo2ROI5 = df_lo2.ROI5.values
lo2ROI5 = (lo2ROI5 - min(lo2ROI5))/(max(lo2ROI5) - min(lo2ROI5))
lo2ROI6 = df_lo2.ROI6.values
lo2ROI6 = (lo2ROI6 - min(lo2ROI6))/(max(lo2ROI6) - min(lo2ROI6))



#Now we plot
#full time scale
fig1 = plt.figure(1)
ax11 = fig1.add_subplot(611)
ax12 = fig1.add_subplot(612)
ax13 = fig1.add_subplot(613)
ax14 = fig1.add_subplot(614)
ax15 = fig1.add_subplot(615)
ax16 = fig1.add_subplot(616)

ax11.plot(df_hi.time,hiROI1)
ax11.set(title = "ROI1", xlabel = "time (s)", ylabel = "dF/F")

ax12.plot(df_hi.time,hiROI2)
ax12.set(title = "ROI2", xlabel = "time (s)", ylabel = "dF/F")

ax13.plot(df_hi.time,hiROI3)
ax13.set(title = "ROI3", xlabel = "time (s)", ylabel = "dF/F")

ax14.plot(df_hi.time,hiROI4,'r')
ax14.set(title = "ROI4", xlabel = "time (s)", ylabel = "dF/F")

ax15.plot(df_hi.time,hiROI5,'r')
ax15.set(title = "ROI5", xlabel = "time (s)", ylabel = "dF/F")

ax16.plot(df_hi.time,hiROI6,'r')
ax16.set(title = "ROI6", xlabel = "time (s)", ylabel = "dF/F")



fig2 = plt.figure(2)
ax21 = fig2.add_subplot(611)
ax22 = fig2.add_subplot(612)
ax23 = fig2.add_subplot(613)
ax24 = fig2.add_subplot(614)
ax25 = fig2.add_subplot(615)
ax26 = fig2.add_subplot(616)

ax21.plot(df_lo.time,loROI1)
ax21.set(title = "ROI1", xlabel = "time (s)", ylabel = "dF/F")

ax22.plot(df_lo.time,loROI2)
ax22.set(title = "ROI2", xlabel = "time (s)", ylabel = "dF/F")

ax23.plot(df_lo.time,loROI3)
ax23.set(title = "ROI3", xlabel = "time (s)", ylabel = "dF/F")

ax24.plot(df_lo.time,loROI4,'r')
ax24.set(title = "ROI4", xlabel = "time (s)", ylabel = "dF/F")

ax25.plot(df_lo.time,loROI5,'r')
ax25.set(title = "ROI5", xlabel = "time (s)", ylabel = "dF/F")

ax26.plot(df_lo.time,loROI6,'r')
ax26.set(title = "ROI6", xlabel = "time (s)", ylabel = "dF/F")



fig3 = plt.figure(3)
ax31 = fig3.add_subplot(611)
ax32 = fig3.add_subplot(612)
ax33 = fig3.add_subplot(613)
ax34 = fig3.add_subplot(614)
ax35 = fig3.add_subplot(615)
ax36 = fig3.add_subplot(616)

ax31.plot(df_lo2.time,lo2ROI1)
ax31.set(title = "ROI1", xlabel = "time (s)", ylabel = "dF/F")

ax32.plot(df_lo2.time,lo2ROI2)
ax32.set(title = "ROI2", xlabel = "time (s)", ylabel = "dF/F")

ax33.plot(df_lo2.time,lo2ROI3)
ax33.set(title = "ROI3", xlabel = "time (s)", ylabel = "dF/F")

ax34.plot(df_lo2.time,lo2ROI4,'r')
ax34.set(title = "ROI4", xlabel = "time (s)", ylabel = "dF/F")

ax35.plot(df_lo2.time,lo2ROI5,'r')
ax35.set(title = "ROI5", xlabel = "time (s)", ylabel = "dF/F")

ax36.plot(df_lo2.time,lo2ROI6,'r')
ax36.set(title = "ROI6", xlabel = "time (s)", ylabel = "dF/F")



#Zoom in on 10s time window
start = 21*15 #define start of time window in frames
stop = 31*15 #define end of time window in frames
fig4 = plt.figure(4)
ax41 = fig4.add_subplot(611)
ax42 = fig4.add_subplot(612)
ax43 = fig4.add_subplot(613)
ax44 = fig4.add_subplot(614)
ax45 = fig4.add_subplot(615)
ax46 = fig4.add_subplot(616)

ax41.plot(df_hi.time[start:stop],hiROI1[start:stop])
ax41.set(title = "ROI1", xlabel = "time (s)", ylabel = "dF/F")
ax41.set_xlim(21,31) #set ax4es limits to edges of your time window
ax42.plot(df_hi.time[start:stop],hiROI2[start:stop])
ax42.set(title = "ROI2", xlabel = "time (s)", ylabel = "dF/F")
ax42.set_xlim(21,31)
ax43.plot(df_hi.time[start:stop],hiROI3[start:stop])
ax43.set(title = "ROI3", xlabel = "time (s)", ylabel = "dF/F")
ax43.set_xlim(21,31)
ax44.plot(df_hi.time[start:stop],hiROI4[start:stop],'r')
ax44.set(title = "ROI4", xlabel = "time (s)", ylabel = "dF/F")
ax44.set_xlim(21,31)
ax45.plot(df_hi.time[start:stop],hiROI5[start:stop],'r')
ax45.set(title = "ROI5", xlabel = "time (s)", ylabel = "dF/F")
ax45.set_xlim(21,31)
ax46.plot(df_hi.time[start:stop],hiROI6[start:stop],'r')
ax46.set(title = "ROI6", xlabel = "time (s)", ylabel = "dF/F")
ax46.set_xlim(21,31)



fig5 = plt.figure(5)
ax51 = fig5.add_subplot(611)
ax52 = fig5.add_subplot(612)
ax53 = fig5.add_subplot(613)
ax54 = fig5.add_subplot(614)
ax55 = fig5.add_subplot(615)
ax56 = fig5.add_subplot(616)

ax51.plot(df_lo.time[start:stop],loROI1[start:stop])
ax51.set(title = "ROI1", xlabel = "time (s)", ylabel = "dF/F")
ax51.set_xlim(21,31) #set ax5es limits to edges of your time window
ax52.plot(df_lo.time[start:stop],loROI2[start:stop])
ax52.set(title = "ROI2", xlabel = "time (s)", ylabel = "dF/F")
ax52.set_xlim(21,31)
ax53.plot(df_lo.time[start:stop],loROI3[start:stop])
ax53.set(title = "ROI3", xlabel = "time (s)", ylabel = "dF/F")
ax53.set_xlim(21,31)
ax54.plot(df_lo.time[start:stop],loROI4[start:stop],'r')
ax54.set(title = "ROI4", xlabel = "time (s)", ylabel = "dF/F")
ax54.set_xlim(21,31)
ax55.plot(df_lo.time[start:stop],loROI5[start:stop],'r')
ax55.set(title = "ROI5", xlabel = "time (s)", ylabel = "dF/F")
ax55.set_xlim(21,31)
ax56.plot(df_lo.time[start:stop],loROI6[start:stop],'r')
ax56.set(title = "ROI6", xlabel = "time (s)", ylabel = "dF/F")
ax56.set_xlim(21,31)



fig6 = plt.figure(6)
ax61 = fig6.add_subplot(611)
ax62 = fig6.add_subplot(612)
ax63 = fig6.add_subplot(613)
ax64 = fig6.add_subplot(614)
ax65 = fig6.add_subplot(615)
ax66 = fig6.add_subplot(616)

ax61.plot(df_lo2.time[start:stop],lo2ROI1[start:stop])
ax61.set(title = "ROI1", xlabel = "time (s)", ylabel = "dF/F")
ax61.set_xlim(21,31) #set ax6es limits to edges of your time window
ax62.plot(df_lo2.time[start:stop],lo2ROI2[start:stop])
ax62.set(title = "ROI2", xlabel = "time (s)", ylabel = "dF/F")
ax62.set_xlim(21,31)
ax63.plot(df_lo2.time[start:stop],lo2ROI3[start:stop])
ax63.set(title = "ROI3", xlabel = "time (s)", ylabel = "dF/F")
ax63.set_xlim(21,31)
ax64.plot(df_lo2.time[start:stop],lo2ROI4[start:stop],'r')
ax64.set(title = "ROI4", xlabel = "time (s)", ylabel = "dF/F")
ax64.set_xlim(21,31)
ax65.plot(df_lo2.time[start:stop],lo2ROI5[start:stop],'r')
ax65.set(title = "ROI5", xlabel = "time (s)", ylabel = "dF/F")
ax65.set_xlim(21,31)
ax66.plot(df_lo2.time[start:stop],lo2ROI6[start:stop],'r')
ax66.set(title = "ROI6", xlabel = "time (s)", ylabel = "dF/F")
ax66.set_xlim(21,31)

plt.show()
