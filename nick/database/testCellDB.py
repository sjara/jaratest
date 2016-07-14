'''
2015-07-24 Nick Ponvert

Test suite for the Jaralab cell database
'''

import unittest
from jaratoolbox.test.nick.database import cellDB
reload(cellDB)

class ImportDB(unittest.TestCase):
    '''
    A simple test to see if we can import the moduel and make a db.
    '''

    def setUp(self):
        self.database = cellDB.CellDB()

    def runTest(self):
        self.assertTrue(isinstance(self.database, list))

class TestRecording(unittest.TestCase):
    '''
    We first need to store information about our recording day
    '''

    def setUp(self):
       self.recording = cellDB.Recording('animal000',
                                         '2015-01-01',
                                         'nick',
                                         '2afc')


    def test_repr(self):
        expectation = '''animalName: pinp003
date: 0000-00-00
experimenter: nick
paradigm: laser_tuning_curve
siteList: []
'''
        self.assertTrue(self.recording.__repr__(), expectation)

    def test_str(self):
        expectation = 'pinp003 recording on 2015-01-01 by nick'

        self.assertTrue(self.recording.__str__(), expectation)

    def add_site_to_list(self):
        site = self.recording.add_site(300, [3,6])
        self.assertEqual(len(self.recording.siteList), 1)


testcase = ImportDB()

#if __name__=="__main__":
    #unittest.main()
