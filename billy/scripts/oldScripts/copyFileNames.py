import os

oldList = os.listdir('/home/billywalker/Pictures/raster_hist/test055/tmpFolder/low_middle_freq')



newList = []
for ind,f in enumerate(oldList):
    fileParts = f.split('_')
    freq = fileParts[5].split('.')[0]
    os.system('cp /home/billywalker/Pictures/raster_hist/test055/%s/rast_test055_%s_%s_%s.png /home/billywalker/Pictures/raster_hist/test055/newTmpFolder/low_middle_freq' % (freq,fileParts[2],freq,fileParts[3]))
