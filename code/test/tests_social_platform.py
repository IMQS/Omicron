'''
Created on 21 Jun 2013

@author: Javonne Martin
'''
import unittest
import gzip
import social_platform as sp
class test_class_social_platform(unittest.TestCase):


    def setUp(self):
        ''' Tests constructors of social media objects '''
        self.socialObject = sp.social_platform()
        self.twitterObject = sp.twitter_platform()
        self.instagramObject = sp.twitter_platform()
        pass


    def tearDown(self):
        pass

    def test_get_platform_name(self):
        with self.assertRaises(NotImplementedError):
            self.socialObject.get_platform_name()
    def test_request_center_radius(self):
        with self.assertRaises(NotImplementedError):
            self.socialObject.get_platform_name()
      
    def test_request_region(self):
        with self.assertRaises(NotImplementedError):
            self.socialObject.get_platform_name()

    def test_authenticate(self):
        with self.assertRaises(NotImplementedError):
            self.socialObject.get_platform_name()

    def test_connection(self):
        with self.assertRaises(NotImplementedError):
            self.socialObject.get_platform_name()

    def test_decrypt_response(self):
#       test1 = "Hello this is a basic string"
#        test2 = "#%&@(#&$*&*@@(! crazy string"
#        compress1 = test1.encode('zlib')
#        compress2 = test2.encode('zlib')
#        headers = {"content-encoding":"gzip"}
#        self.assertEqual(self.socialObject.decrypt_response(encrypted_data=compress1, headers=headers),test1)
#        self.assertEqual(self.socialObject.decrypt_response(encrypted_data=compress2, headers=headers),test2)
        pass
    def test_authenticate_headers(self):
        with self.assertRaises(NotImplementedError):
            self.socialObject.get_platform_name()
    def test_strip_data(self):
        with self.assertRaises(NotImplementedError):
            self.socialObject.get_platform_name()
    def testName(self):
        with self.assertRaises(NotImplementedError):
            self.socialObject.get_platform_name()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()