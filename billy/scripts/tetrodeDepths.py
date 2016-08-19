'''Objects and methods to keep information about individual tetrode lengths for each animal. This is all length relative to the longest tetrode'''

class tetLength(object):
    def __init__(self, animalName, ap_coord, ml_coord, brain_side, tetrodeLengthList=[], depth_range_striatum=[]):
        self.animalName = animalName
        self.tetrodeLengthList = tetrodeLengthList #relative to longest tetrode which is at 0.0mm
        self.depth_range_striatum = depth_range_striatum #range in mm where longest tetrode was in striatum
        self.ap_coord = ap_coord #AP coordinate in mm
        self.ml_coord = ml_coord #tells if you were medial, lateral, or in the middle of the striatum. 'inside' means in the striatum, 'medial' means you missed the striatum medially, 'lateral' means you missed the striatum laterally
        self.brain_side = brain_side #this says what side of the brain the implant was on, 'right' or 'left'

class tetDatabase(list):
    def __init__(self):
        super(tetDatabase, self).__init__()
    def append_animal(self,tetInfo):
        self.append(tetInfo)
    def findAllTetLength(self,mouseName):
        '''
        This will return the relative lengths of the tetrodes in mm
        findAllTetLength(self,mouseName)
        '''
        for ind,animal in enumerate(self):
            if animal.animalName==mouseName:
                return animal.tetrodeLengthList
        return None
    def findOneTetLength(self,mouseName, tetrode, longestTetDepth):#use tetrode numbers starting at 1 to 8
        '''
        This will return the depth of a particular tetrode in mm
        findOneTetLength(self,mouseName, tetrode, longestTetDepth) #use tetrode numbers starting at 1 to 8
        '''
        for ind,animal in enumerate(self):
            if animal.animalName==mouseName:
                return (longestTetDepth - animal.tetrodeLengthList[tetrode-1])
        return None
    def striatumRange(self, mouseName):
        '''
        This will return the range of depths of the striatum in mm for that animal
        striatumRange(self, mouseName)
        '''
        range = []
        for ind,animal in enumerate(self):
            if animal.animalName==mouseName:
                 range = animal.depth_range_striatum
        return range
    def isInStriatum(self, mouseName, tetrode, longestTetDepth):#use tetrode numbers starting at 1 to 8
        '''
        This will return a boolean that is true if the cell is in the striatum depth range and false otherwise
        isInStriatum(self, mouseName, tetrode, longestTetDepth) #use tetrode numbers starting at 1 to 8
        '''
        if tetrode not in range(1,9):
            return False
        for ind,animal in enumerate(self):
            if animal.animalName==mouseName:
                curDepth = (longestTetDepth - animal.tetrodeLengthList[tetrode-1])
                if (animal.depth_range_striatum[0] <= curDepth <= animal.depth_range_striatum[1]) and (animal.ap_coord > 0):
                    return True
                else:
                    return False
        return None



