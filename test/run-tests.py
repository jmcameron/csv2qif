import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from utils import detect

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
        self.assertEqual(results['negate'], True)

    def test_test2(self):
        results = detect(os.path.join(base_dir, 'test2.csv'))
        self.assertEqual(results['header_line'], 0)
        self.assertEqual(results['amount'], 2)
        self.assertEqual(results['category'], None)
        self.assertEqual(results['credit'], None)
        self.assertEqual(results['date'], 0)
        self.assertEqual(results['description'], 1)
        self.assertEqual(results['negate'], False)

    def test_test3(self):
        results = detect(os.path.join(base_dir, 'test3.csv'))
        self.assertEqual(results['header_line'], 0)
        self.assertEqual(results['amount'], 5)
        self.assertEqual(results['category'], 4)
        self.assertEqual(results['credit'], 6)
        self.assertEqual(results['date'], 0)
        self.assertEqual(results['description'], 3)
        self.assertEqual(results['negate'], False)

    def test_test4(self):
        results = detect(os.path.join(base_dir, 'test4.csv'))
        self.assertEqual(results['header_line'], 6)
        self.assertEqual(results['amount'], 2)
        self.assertEqual(results['category'], None)
        self.assertEqual(results['credit'], None)
        self.assertEqual(results['date'], 0)
        self.assertEqual(results['description'], 1)
        self.assertEqual(results['negate'], True)

    def test_test5(self):
        results = detect(os.path.join(base_dir, 'test5.csv'))
        self.assertEqual(results['header_line'], 0)
        self.assertEqual(results['amount'], 4)
        self.assertEqual(results['category'], None)
        self.assertEqual(results['credit'], 5)
        self.assertEqual(results['date'], 0)
        self.assertEqual(results['description'], 3)
        self.assertEqual(results['negate'], True)

if __name__ == '__main__':
    unittest.main()

