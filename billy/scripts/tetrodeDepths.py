'''Objects and methods to keep information about individual tetrode lengths for each animal. This is all length relative to the longest tetrode'''

class tetLength(object):
    def __init__(self, animalName, tetrodeLengthList=[], depth_range_striatum=[]):
        self.animalName = animalName
        self.tetrodeLengthList = tetrodeLengthList
        self.depth_range_striatum = depth_range_striatum


class tetDatabase(list):
    def __init__(self):
        super(tetDatabase, self).__init__()
    def append_animal(self,tetInfo):
        self.append(tetInfo)
    def findAllTetLength(self,mouseName):
        for ind,animal in enumerate(self):
            if animal.animalName==mouseName:
                return animal.tetrodeLengthList
        return None
    def findOneTetLength(self,mouseName, tetrode, longestTetDepth):
        for ind,animal in enumerate(self):
            if animal.animalName==mouseName:
                return (longestTetDepth - animal.tetrodeLengthList[tetrode-1])
        return None
    def isInStriatum(self, mouseName, tetrode, longestTetDepth):
        for ind,animal in enumerate(self):
            if animal.animalName==mouseName:
                curDepth = (longestTetDepth - animal.tetrodeLengthList[tetrode-1])
                if (animal.depth_range_striatum[0] <= curDepth <= animal.depth_range_striatum[1]):
                    return True
                else:
                    return False
        return None



