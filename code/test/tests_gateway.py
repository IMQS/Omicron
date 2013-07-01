'''
Created on 28 Jun 2013

@author: S. Schreiber
'''
import unittest
import gateway

class test_gateway(unittest.TestCase):
    '''
        Tests the gateway module.
    '''
    def test_available_social_media(self):
        '''
            Tests to make sure the correct object is returned.
        '''
        current_test_obj = gateway.gateway()
        platform_obj = current_test_obj._available_social_media(["twitter"])
        assert "twitter" == platform_obj[0].get_platform_name()
        
        platform_obj = current_test_obj._available_social_media(["instagram"])
        assert "instagram" == platform_obj[0].get_platform_name()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()