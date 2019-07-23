'''
Testing how to reload inforec.
'''

import imp

class EphysInterface(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.inforec = self.load_inforec()
    def load_inforec(self):
        #TODO: make this reload
        inforec = imp.load_source('module.name', self.filepath)
        return inforec

#ep = EphysInterface('/home/sjara/src/jaratest/santiago/temp001.py')
ep = EphysInterface('./temp001.py')

# ep = ephysinterface.EphysInterface('/home/sjara/src/jaratest/santiago/temp001.py')
