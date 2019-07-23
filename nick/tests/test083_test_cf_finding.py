import numpy as np
from matplotlib import pyplot as plt

#Test freq-response array
fra = np.array([[0,0,0,1,0,0],
                [0,0,1,0,1,0],
                [0,0,1,1,1,0],
                [0,0,0,1,1,0],
                [1,1,1,1,1,1]], dtype=bool)

#Test response array
res = np.array([[0,0,0,6,0,0],
                [0,0,5,0,4,0],
                [0,0,6,5,4,0],
                [0,0,0,5,5,0],
                [5,5,5,5,5,5]])

# plt.clf()
# plt.imshow(arr, interpolation='none')
# plt.show()

def find_cf_inds(fra, resp, threshold=0.85):
    '''
    fra (np.array): boolean array of shape (nInten, nFreq). Higher index = higher intensity
    resp (np.array): response spike number array of shape (nInten, nFreq). Higher index = higher intensity
    threshold (float): At least this proportion of the intensities above must have a response for the freq to be cf
    '''
    results = []
    for indRow, row in enumerate(fra):
        for indCol, column in enumerate(row):
            if column: #Or we do a comparison here
                colAbove = fra[indRow:, indCol]
                if np.mean(colAbove)>0.85:
                # if np.all(colAbove):
                    results.append((indRow, indCol))
    resultIntenInds = [a for a, b in results]
    minResultIntenInd = min(resultIntenInds)
    resultsAtMinInten = [(a, b) for a, b in results if a==minResultIntenInd]
    resultSpikeCounts = [resp[a, b] for a, b in resultsAtMinInten]
    resultWithMaxFiring = resultsAtMinInten[resultSpikeCounts.index(max(resultSpikeCounts))]
    return resultWithMaxFiring

print find_cf(fra, res)

