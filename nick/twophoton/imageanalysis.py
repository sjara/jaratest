import os
import numpy as np
from jaratest.nick.twophoton import loadflycap
from matplotlib import pyplot as plt
from matplotlib import widgets
from sklearn import preprocessing
from sklearn import decomposition

class StackPCA(object):
    def __init__(self, imgArr, nComponents=None):

        '''
        Compute PCA on a stack of images and explore the resulting components.

        Args:
           imgArr (np.array): Size (nframes, width, height)
           nComponents (int): Number of components to use. If unspecified,
                              PCA will extract number of components required
                              to explain 95% of variance.
        '''

        self.imgArr = imgArr
        self.nFrames = self.imgArr.shape[0]
        self.imgShape = self.imgArr.shape[1:]
        self.nComponents = nComponents


        #Reshape to an array of shape (nFrames, nFeatures)
        #-1 trick for reshape calculates shape needed based on
        #remaining dimensions
        self.featureArr = self.imgArr.reshape(self.imgArr.shape[0], -1)

        #Scale the resulting feature array
        self.scaler = preprocessing.StandardScaler()
        self.scaler.fit(self.featureArr)
        self.featureArr = self.scaler.transform(self.featureArr)

        #PCA instance to retain components necessary to explain 95% of variance.
        if self.nComponents == None:
            self.pca = decomposition.PCA(0.95)
        else:
            self.pca = decomposition.PCA(n_components=self.nComponents)

        #Compute PCA on the scaled feature array
        self.pca.fit(self.featureArr)

        #Value of each PCA component in each frame. Size (nFrames, nComponents)
        self.X_transform = self.pca.transform(self.featureArr)

        if self.nComponents == None:
            self.nComponents = self.pca.n_components_

        #Re-construct the array of image components (nComponents, width, height)
        self.components = self.pca.components_.reshape(self.nComponents,
                                                       self.imgShape[0],
                                                       self.imgShape[1])

    def plot_component_images(self):
        if self.nComponents>100:
            raise ValueError('Probably too many components to plot this way')

        nRow = int(np.ceil(np.sqrt(self.nComponents)))
        nCol = nRow

        plt.clf()
        for indPlot in range(self.nComponents):
            plt.subplot(nRow, nCol, indPlot+1)
            plt.imshow(self.components[indPlot, :,:])
            plt.gca().axis('off')
            plt.title('{}'.format(indPlot))
        plt.show()

    def plot_traces(self, normalized=False):
        plt.clf()

        #TODO: Normalization
        if normalized:
            X = preprocessing.StandardScaler().fit_transform(self.X_transform)
        else:
            X = self.X_transform
        plt.plot(X)
        plt.show()


class StackICA(object):
    def __init__(self, imgArr, nComponents=None):

        '''
        Compute ICA on a stack of images and explore the resulting components.

        Args:
           imgArr (np.array): Size (nframes, width, height)
           nComponents (int): Number of components to use. If unspecified,
                              PCA will extract number of components required
                              to explain 95% of variance.
        '''

        self.imgArr = imgArr
        self.nFrames = self.imgArr.shape[0]
        self.imgShape = self.imgArr.shape[1:]
        self.nComponents = nComponents


        #Reshape to an array of shape (nFrames, nFeatures)
        #-1 trick for reshape calculates shape needed based on
        #remaining dimensions
        self.featureArr = self.imgArr.reshape(self.imgArr.shape[0], -1)

        #Scale the resulting feature array
        self.scaler = preprocessing.StandardScaler()
        self.scaler.fit(self.featureArr)
        self.featureArr = self.scaler.transform(self.featureArr)

        #PCA instance to retain components necessary to explain 95% of variance.
        if self.nComponents == None:
            self.ica = decomposition.FastICA()
        else:
            self.ica = decomposition.FastICA(n_components=self.nComponents)


class PlotImageStack(object):
    def __init__(self, imgArr):
        '''
        Plot images from a stack, use a slider to move through the stack.

        Args:
            imgArr (np.array): Size (nFrames, width, height)
        '''
        self.imgArr = imgArr
        self.nFrames = imgArr.shape[0]
        self.imgMin = np.min(imgArr.ravel())
        self.imgMax = np.max(imgArr.ravel())
        self.fig = plt.figure()
        plt.clf()
        self.axPlot = self.fig.add_subplot(111)

        im = self.axPlot.imshow(self.imgArr[0, :, :])
        im.set_clim(self.imgMin, self.imgMax)

        plt.subplots_adjust(left=0.25, bottom=0.25)
        self.axSlider = plt.axes([0.25, 0.1, 0.65, 0.03])
        self.slider = widgets.Slider(self.axSlider, 'Frame', 0, self.nFrames-1, valinit=0)
        self.slider.on_changed(self.plot_frame)
        plt.show()

    def plot_frame(self, val):
        indFrame = int(np.floor(self.slider.val))
        self.axPlot.cla()
        im = self.axPlot.imshow(self.imgArr[indFrame,:,:])
        im.set_clim(self.imgMin, self.imgMax)
        plt.draw()
