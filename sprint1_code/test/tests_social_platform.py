'''
Created on 21 Jun 2013

@author: Javonne Martin
'''
import unittest
import social_platform as sp
class test_class_social_platform(unittest.TestCase):


    def setUp(self):
        ''' Tests constructors of social media objects '''
        self.twitterObject = sp.twitter_platform()
        self.instagramObject = sp.twitter_platform()
        pass


    def tearDown(self):
        pass

    def test_twitter_authentication(self):
        self.assertNotEquals(self.twitterObject.authenticate(),None)
        pass
    def test_decrypt_response(self):
        
        pass
    def test_twitter_get_data(self):
        self.twitterObject.authenticate()
        self.assertNotEqual(self.twitterObject.get_data(tag_list=["#snow","#winter"]),None)
    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()