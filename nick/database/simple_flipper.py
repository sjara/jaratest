import os
import scipy.misc
from matplotlib import pyplot as plt
from jaratoolbox.test.nick.database import dataplotter
from jaratoolbox.test.nick.database import cellDB
from jaratoolbox.test.nick.database import dataloader
import itertools
reload(dataplotter)

folder = '/mnt/jarahubdata/histology/test034_jpg'
imageFilenameList = [os.path.join(folder, fn) for fn in sorted(os.listdir(folder))]
imageList = map(scipy.misc.imread, imageFilenameList)


# @dataplotter.FlipThroughData
# def show_img(image):
#     plt.imshow(image)

# flip_image=dataplotter.FlipThroughData(show_img)
# flip_image(imageList)



# # show_img(imageList)

flipper = dataplotter.FlipT(plt.imshow, imageList)


#'-------------------------------------'
# # imageList
# plt.imshow(image)
# flipt(plt.imshow,imageList)
# #----
# def twoplots(spiketimes, events):
#     subplot()
#     plot(spiketimes,events)
#     subplot()
#     plot(mean(spiketimes))

# flipt(twoplots, dataList)
    



'''


dbFn = '/var/tmp/allcells.json'
db = cellDB.CellDB()
db.load_from_json(dbFn)

loader = dataloader.DataLoader('offline', experimenter='nick')
cell0=db[0]
dataNB = cell0.get_data_filenames('noiseBurst')

#Get the filenames for the noiseBurst and laserTrain session
cellDataFilenames = map(cell0.get_data_filenames, ['noiseBurst', 'laserTrain'])

#Get the spikes and events for each of the two sessions
cellDataSpikes = [loader.get_session_spikes(session, cell0.tetrode) for session in cellDataFilenames]
cellDataEvents = [loader.get_session_events(session) for session in cellDataFilenames]

#Make lists of the spiketime arrays and event onset time arrays for each of the raster plots.
cellDataSpiketimes = [d.timestamps for d in cellDataSpikes]
cellDataEventOnsetTimes = [loader.get_event_onset_times(ev) for ev in cellDataEvents]

#Zip the spiketimes and event onset times together into a list of tuples.
dataTuples = zip(cellDataSpiketimes, cellDataEventOnsetTimes)


#Now, make a function that will do what you want with one of the elements in a list
#In this case, the list contains tuples that have (spiketimes, eventOnsetTimes)
#Then when we wrap it with FlipThroughData we can pass it the whole list and it will be
#able to deal with the list.

@dataplotter.FlipThroughData
def simple_raster(cellDataTuple):
    spikeTimestamps = cellDataTuple[0]
    eventOnsetTimes = cellDataTuple[1]
    dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes)
    plt.title('My title')
    plt.xlabel('My X Label')
    plt.ylabel('My Y Label')

simple_raster(dataTuples)

'''