import unittest
from jaratest.nick.reports import pinp_report

class TestPinpReport(unittest.TestCase):

    def test_get_session_inds(self):
        cell = {'sessiontype':['am', 'noiseburst', 'lasertrain', 'am']}
        assert pinp_report.get_session_inds(cell, 'noiseburst') == [1]
        assert pinp_report.get_session_inds(cell, 'am') == [0, 3]
        assert pinp_report.get_session_inds(cell, 'lasertrain') == [2]


