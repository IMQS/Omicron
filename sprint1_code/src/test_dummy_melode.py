'''
Created on 18 Jun 2013

@author: meloder
'''
import unittest
import experiement as ex

class Test(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_add_5_6(self):
        self.assertEqual(ex.add_five(6), 11)

    def test_add_5_25(self):
        self.assertEqual(ex.add_five(25), 30)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()