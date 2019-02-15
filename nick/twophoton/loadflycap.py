'''
2019-02-13 Nick Ponvert
Loading class for epifluorescence imaging data saved by FlyCap.
Expected save format is a folder containing individual .PGM images for each frame.
'''
import os
import numpy as np
import re
from skimage import measure
from jaratest.nick.utils import progressbar

def read_pgm(filename, byteorder='>', headerDict=True, returnType='uint16'):
    """
    Return image data from a raw PGM file as numpy array.
    Adapted from: https://stackoverflow.com/questions/7368739/numpy-and-16-bit-pgm/7369986
    Format specification: http://netpbm.sourceforge.net/doc/pgm.html

    Args:
        filename (str): Full path to the PGM image to open
        byteorder (str): Either '>' or '<', endian-ness
        headerDict (bool): Whether to return dict with header info

    Returns:
        img (np.array): Image data as a numpy array.
        headerDict (dict): Header information, shape, and max value.
    """

    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    img = np.frombuffer(buffer,
                        dtype='u1' if int(maxval) < 256 else byteorder+'u2',
                        count=int(width)*int(height),
                        offset=len(header)).reshape((int(height), int(width)))
    img = img.astype(returnType)
    headerDict = {'header':header,
                  'width': width,
                  'height':height,
                  'maxval':maxval}
    # if headerDict:
    #     return img, headerDict
    # else:
    return img

def bin_image(img, binX, binY):
    '''
    Doing my best here. A fxn to bin images.
    NOTE: Waaay too slow. Use skimage.measure.block_reduce instead

    Args:
        img (np.array): A 2d array
        binX (int): Number of pixels to bin in X
        binY (int): Number of pixels to bin in Y

    '''
    returnX = int(np.ceil(img.shape[0] / float(binX)))
    returnY = int(np.ceil(img.shape[1] / float(binY)))
    returnImg = np.empty((returnX, returnY))
    for (indX, indY), _ in np.ndenumerate(returnImg):
        startX = indX*binX
        endX = startX+binX
        startY = indY*binY
        endY = startY+binY
        try:
            chunk = img[startX:endX, startY:endY]
        except IndexError:
            #Problem was with X range?
            try:
                chunk = img[startX:, startY:endY]
            except IndexError:
                #Problem was with Y range?
                try:
                    chunk = img[startX:endX, startY:]
                except IndexError:
                    #Problem was both X and Y
                    chunk = img[startX:, startY:]
        #TODO: Support different metrics here
        returnImg[indX, indY] = np.mean(chunk.ravel())
    return returnImg

class LoadFlyCap(object):

    def __init__(self, dataDir, skipBy=1, binX=1, binY=1, binFunc=None):
        '''
        Load a folder of PGM images saved by FlyCap.

        Args:
            dataDir (str): The directory containing the image files.
            skipBy (int): Which frames to load. 1 loads every frame,
                          2 loads every other frame, etc.
            binX (int): Number of pixels over which to bin in X. 1=no binning.
            binY (int): Number of pixels over which to bin in Y. 1=no binning.

        '''

        self.skipBy = skipBy
        self.dataDir = dataDir
        self.binX = binX
        self.binY = binY
        if binFunc is None:
            self.binFunc = np.mean

        #Filenames of all frames in the directory
        frameFns = sorted(os.listdir(self.dataDir))

        #Read first image to get width and height
        im0 = read_pgm(os.path.join(dataDir,
                                    frameFns[0]),
                       headerDict=False)

        #Which file indices to read, based on skipBy value
        indsToRead = range(0, len(frameFns), self.skipBy)
        self.nFrames = len(indsToRead)
        self.width, self.height = np.shape(bin_image(im0, self.binX, self.binY))

        #Empty array to hold image data
        self.imgArr = np.empty((self.nFrames, self.width, self.height))

        for indFrame, indFile in enumerate(indsToRead):
            frameFn = os.path.join(dataDir, frameFns[indFile])
            rawImg = read_pgm(frameFn, headerDict=False)

            #Soooooooooooo slow...
            #Have to use skimage implementation instead
            # self.imgArr[indFrame, :, :] = bin_image(rawImg,
            #                                         self.binX,
            #                                         self.binY)
            self.imgArr[indFrame, :, :] = \
                         measure.block_reduce(rawImg,
                                              block_size=(self.binX, self.binY),
                                              func=self.binFunc)

            #Just for fun
            progressbar.progress_bar(indFrame, self.nFrames, "Loading frames")

if __name__=="__main__":
    #Run some tests of the binning function

    #Test 1 and 2
    binX = 2
    binY = 2
    testImg = np.array([[1, 2, 3, 4],
                        [2, 3, 4, 5],
                        [3, 4, 5, 6],
                        [4, 5, 6, 7]])
    desiredImg = np.array([[2., 4.],
                           [4., 6.]])
    assert np.all(bin_image(testImg, binX, binY) == desiredImg)

    testImg = np.array([[1, 2, 3, 4, 5],
                        [2, 3, 4, 5, 7],
                        [3, 4, 5, 6, 9],
                        [4, 5, 6, 7, 11]])
    desiredImg = np.array([[2., 4., 6.],
                           [4., 6., 10.]])
    assert np.all(bin_image(testImg, binX, binY) == desiredImg)

    #Test 3
    binX = 3
    binY = 3
    testImg = np.array([[1, 2, 3, 4],
                        [2, 3, 4, 5],
                        [3, 4, 5, 6],
                        [4, 5, 6, 7]])
    desiredImg = np.array([[3., 5.],
                           [5., 7.]])
    assert np.all(bin_image(testImg, binX, binY) == desiredImg)

    #Test 4
    binX = 1
    binY = 1
    testImg = np.array([[1, 2, 3, 4],
                        [2, 3, 4, 5],
                        [3, 4, 5, 6],
                        [4, 5, 6, 7]])
    assert np.all(bin_image(testImg, binX, binY) == testImg)

    #Test the loader on an image set
    dataDir = '/home/nick/data/1pdata/imag003/20181217_noiseburst/'
    flc = LoadFlyCap(dataDir, skipBy=2, binX=10, binY=10)

