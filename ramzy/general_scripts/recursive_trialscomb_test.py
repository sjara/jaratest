import numpy as np
import unittest
from jaratoolbox.behavioranalysis import find_trials_each_combination_n,find_trials_each_type,find_trials_each_combination

class TestFindTrialsEachCombinationN(unittest.TestCase):
    def setUp(self):
        # Common test data
        self.nTrials = 10
        self.param1 = np.array([0, 1, 0, 1, 2, 0, 1, 2, 0, 1])
        self.possible1 = [0, 1, 2]
        
        self.param2 = np.array([0, 0, 1, 1, 0, 0, 1, 1, 0, 0])
        self.possible2 = [0, 1]
        
        self.param3 = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        self.possible3 = [0, 1]

    def test_single_parameter(self):
        result = find_trials_each_combination_n([self.param1], [self.possible1])
        expected = find_trials_each_type(self.param1, self.possible1)
        
        self.assertEqual(result.shape, (self.nTrials, 3))
        np.testing.assert_array_equal(result, expected)

    def test_two_parameters(self):
        result = find_trials_each_combination_n([self.param1, self.param2], 
                                               [self.possible1, self.possible2])
        expected = find_trials_each_combination(self.param1, self.possible1, 
                                               self.param2, self.possible2)
        
        self.assertEqual(result.shape, (self.nTrials, 3, 2))
        np.testing.assert_array_equal(result, expected)

    def test_three_parameters(self):
        result = find_trials_each_combination_n([self.param1, self.param2, self.param3],
                                               [self.possible1, self.possible2, self.possible3])
        
        # Manually verify a few combinations
        self.assertEqual(result.shape, (self.nTrials, 3, 2, 2))
        
        # Check specific combinations
        # param1=0, param2=0, param3=0
        expected_trials = (self.param1 == 0) & (self.param2 == 0) & (self.param3 == 0)
        np.testing.assert_array_equal(result[:, 0, 0, 0], expected_trials)
        
        # param1=1, param2=1, param3=1
        expected_trials = (self.param1 == 1) & (self.param2 == 1) & (self.param3 == 1)
        np.testing.assert_array_equal(result[:, 1, 1, 1], expected_trials)

    def test_parameter_length_mismatch(self):
        param_short = np.array([0, 1])
        with self.assertRaises(ValueError):
            find_trials_each_combination_n([self.param1, param_short], 
                                          [self.possible1, self.possible2])

    def test_no_parameters(self):
        with self.assertRaises(ValueError):
            find_trials_each_combination_n([], [])

    def test_four_parameters(self):
        param4 = np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 0])
        possible4 = [0, 1]
        
        result = find_trials_each_combination_n([self.param1, self.param2, self.param3, param4],
                                               [self.possible1, self.possible2, self.possible3, possible4])
        
        self.assertEqual(result.shape, (self.nTrials, 3, 2, 2, 2))
        
        # Verify a specific combination
        expected_trials = ((self.param1 == 0) & (self.param2 == 0) & 
                          (self.param3 == 0) & (param4 == 0))
        np.testing.assert_array_equal(result[:, 0, 0, 0, 0], expected_trials)

    def test_parameter_with_single_value(self):
        param_single = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        possible_single = [0]
        
        result = find_trials_each_combination_n([param_single], [possible_single])
        self.assertEqual(result.shape, (self.nTrials, 1))
        np.testing.assert_array_equal(result[:, 0], np.ones(self.nTrials, dtype=bool))

if __name__ == '__main__':
    unittest.main()