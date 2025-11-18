import os, sys
import unittest
from argparse import Namespace

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import detect
from csv2qif import csv2qif

base_dir = os.path.dirname(os.path.abspath(__file__))

class TestStringMethods(unittest.TestCase):
    
    def test_test1(self):
        results = detect(os.path.join(base_dir, 'test1.csv'))
        self.assertEqual(results['header_line'], 0)
        self.assertEqual(results['amount'], 5)
        self.assertEqual(results['category'], 3)
        self.assertEqual(results['credit'], None)
        self.assertEqual(results['date'], 0)
        self.assertEqual(results['description'], 2)
        self.assertEqual(results['negate'], False)

    def test_test2(self):
        results = detect(os.path.join(base_dir, 'test2.csv'))
        self.assertEqual(results['header_line'], 0)
        self.assertEqual(results['amount'], 2)
        self.assertEqual(results['category'], None)
        self.assertEqual(results['credit'], None)
        self.assertEqual(results['date'], 0)
        self.assertEqual(results['description'], 1)
        self.assertEqual(results['negate'], True)

    def test_test3(self):
        results = detect(os.path.join(base_dir, 'test3.csv'))
        self.assertEqual(results['header_line'], 0)
        self.assertEqual(results['amount'], 5)
        self.assertEqual(results['category'], 4)
        self.assertEqual(results['credit'], 6)
        self.assertEqual(results['date'], 0)
        self.assertEqual(results['description'], 3)
        self.assertEqual(results['negate'], True)

    def test_test4(self):
        results = detect(os.path.join(base_dir, 'test4.csv'))
        self.assertEqual(results['header_line'], 6)
        self.assertEqual(results['amount'], 2)
        self.assertEqual(results['category'], None)
        self.assertEqual(results['credit'], None)
        self.assertEqual(results['date'], 0)
        self.assertEqual(results['description'], 1)
        self.assertEqual(results['negate'], False)

    def test_test5(self):
        results = detect(os.path.join(base_dir, 'test5.csv'))
        self.assertEqual(results['header_line'], 0)
        self.assertEqual(results['amount'], 4)
        self.assertEqual(results['category'], None)
        self.assertEqual(results['credit'], 5)
        self.assertEqual(results['date'], 0)
        self.assertEqual(results['description'], 3)
        self.assertEqual(results['negate'], False)
        
    def test_test_qif1(self):
        # Parse the test1.csv file
        csv2qif(Namespace(csvfilename=os.path.join(base_dir, 'test1.csv'),
                          output='/tmp/test1.qif', printcats=False, complain=False))
        # Compare the results
        with open("test1.qif", "r") as f_expected, open("/tmp/test1.qif", "r") as f_actual:
            expected_lines = f_expected.readlines()
            actual_lines = f_actual.readlines()
            self.assertListEqual(actual_lines, expected_lines)

if __name__ == '__main__':
    unittest.main()

