import matplotlib.pyplot as plt
import numpy as np
import importlib
import os
from jaratoolbox import celldatabase
studyparams = importlib.import_module('jaratest.common.2019astrpi.studyparams')


def normalized_hist_dataframe(data_column, bin_number=50, output_dir='/var/tmp/'):
    db = celldatabase.load_hdf("/var/tmp/figuresdata/2019astrpi/direct_and_indirect_cells.h5")
    # dbTuned = db.query(studyparams.TUNING_FILTER)
    D1DB = db.query(studyparams.D1_CELLS)
    nD1DB = db.query(studyparams.nD1_CELLS)
    D1DB = D1DB.replace([np.inf, -np.inf], np.nan)
    nD1DB = nD1DB.replace([np.inf, -np.inf], np.nan)
    D1DB = D1DB[D1DB[data_column].notnull()]
    nD1DB = nD1DB[nD1DB[data_column].notnull()]
    D1Hist, D1bins = np.histogram(D1DB[data_column], bins=bin_number, density=True)
    nD1Hist, nD1bins = np.histogram(nD1DB[data_column], bins=bin_number, density=True)
    center = (D1bins[:-1] + D1bins[1:])/2
    width = 0.7 * (D1bins[1] - D1bins[0])

    fig = plt.gcf()
    fig.clf()

    ax = fig.add_subplot()
    ax.bar(center, D1Hist, width=width, align='center', label='D1', alpha=0.5)
    ax.bar(center, nD1Hist, width=width, align='center', label='nD1', alpha=0.5)
    ax.legend()
    ax.set_xlabel('{} value'.format(data_column))
    ax.set_ylabel('Frequency')
    ax.set_title(data_column)
    fig.savefig(os.path.join(output_dir + "{}.png".format(data_column)))
    plt.show()
    return fig, ax


def normalized_hist(data1, data2, ax, color1, color2, bin_number=50):
    D1Hist, D1bins = np.histogram(data1, bins=bin_number, density=True)
    nD1Hist, nD1bins = np.histogram(data2, bins=bin_number, density=True)
    center = (D1bins[:-1] + D1bins[1:])/2
    width = 0.7 * (D1bins[1] - D1bins[0])
    medianD1 = np.median(data1)
    medianD2 = np.median(data2)

    ax.bar(center, D1Hist, width=width, align='center', label='D1', alpha=0.5, color=color1)
    ax.bar(center, nD1Hist, width=width, align='center', label='nD1', alpha=0.5, color=color2)
    ax.legend()
    ymin, ymax = ax.get_ybound()
    ax.vlines(medianD1, ymin, ymax, color=color1)
    ax.vlines(medianD2, ymin, ymax, color=color2)
    return ax
