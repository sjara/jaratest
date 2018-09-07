import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from scipy import stats
import pandas as pd

from sklearn import mixture
from sklearn import cross_validation

STUDY_NAME = '2018thstr'
FIGNAME = 'figure_am'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

exampleDataPath = os.path.join(dataDir, 'data_am_examples.npz')
exampleData = np.load(exampleDataPath)

exampleFreqEachTrial = exampleData['exampleFreqEachTrial'].item()
exampleSpikeTimes = exampleData['exampleSpikeTimes'].item()
exampleTrialIndexForEachSpike = exampleData['exampleTrialIndexForEachSpike'].item()
exampleIndexLimitsEachTrial = exampleData['exampleIndexLimitsEachTrial'].item()

exampleNames = ['Thal0', 'Thal1', 'AC0', 'AC1']

exampleName = exampleNames[1]
spikeTimes = exampleSpikeTimes[exampleName]
indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
freqEachTrial = exampleFreqEachTrial[exampleName]
# trialsEachCondition = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)

countRange = [0.1, 0.5]
spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimes,indexLimitsEachTrial,countRange)
numSpikesInTimeRangeEachTrial = np.squeeze(spikeCountMat)

if len(numSpikesInTimeRangeEachTrial) == len(freqEachTrial)+1:
    numSpikesInTimeRangeEachTrial = numSpikesInTimeRangeEachTrial[:-1]

# Break up the data into non-overlapping training (75%) and testing (25%) sets.
# From: http://scikit-learn.org/0.15/auto_examples/mixture/plot_gmm_classifier.html

skf = cross_validation.StratifiedKFold(freqEachTrial, n_folds=4)
# Only take the first fold.
train_index, test_index = next(iter(skf))


#The reshape is to get X to (nSpikes, 1) shape which the GMM requires
X_train = numSpikesInTimeRangeEachTrial[train_index].reshape(-1, 1)
y_train = freqEachTrial[train_index]

X_test = numSpikesInTimeRangeEachTrial[test_index].reshape(-1, 1)
y_test = freqEachTrial[test_index]

n_classes = len(np.unique(y_train))

# Try GMMs using different types of covariances.
# classifiers = dict((covar_type, mixture.GMM(n_components=n_classes,
#                     covariance_type=covar_type, init_params='wc', n_iter=20))
#                    for covar_type in ['spherical', 'diag', 'tied', 'full'])

mix = mixture.GMM(n_components=n_classes)
mix.fit(X_train)

# n_classifiers = len(classifiers)

for index, (name, classifier) in enumerate(classifiers.items()):
    # Since we have class labels for the training data, we can
    # initialize the GMM parameters in a supervised manner.
    classifier.means_ = np.array([X_train[y_train == i].mean(axis=0)
                                  for i in xrange(n_classes)])

    # Train the other parameters using the EM algorithm.
    classifier.fit(X_train)

    # h = plt.subplot(2, n_classifiers / 2, index + 1)
    # make_ellipses(classifier, h)

    # for n, color in enumerate('rgb'):
    #     data = iris.data[iris.target == n]
    #     plt.scatter(data[:, 0], data[:, 1], 0.8, color=color,
    #                 label=iris.target_names[n])
    # # Plot the test data with crosses
    # for n, color in enumerate('rgb'):
    #     data = X_test[y_test == n]
        # plt.plot(data[:, 0], data[:, 1], 'x', color=color)

    print "Classifier type: {}".format(name)
    y_train_pred = classifier.predict(X_train)
    train_accuracy = np.mean(y_train_pred.ravel() == y_train.ravel()) * 100
    # plt.text(0.05, 0.9, 'Train accuracy: %.1f' % train_accuracy,
    #          transform=h.transAxes)
    print "Train accuracy: {}".format(train_accuracy)

    y_test_pred = classifier.predict(X_test)
    test_accuracy = np.mean(y_test_pred.ravel() == y_test.ravel()) * 100
    # plt.text(0.05, 0.8, 'Test accuracy: %.1f' % test_accuracy,
    #          transform=h.transAxes)
    print "Test accuracy: {}\n".format(test_accuracy)
