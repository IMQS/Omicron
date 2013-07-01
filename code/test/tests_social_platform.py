'''
Created on 21 Jun 2013

@author: Javonne Martin
'''
import unittest
import gzip
import social_platform as sp
import StringIO

k = sp.twitter_platform()
k.test_connection()
k.authenticate()

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
            self.socialObject.request_center_radius(None, None, None)
      
    def test_request_region(self):
        with self.assertRaises(NotImplementedError):
            self.socialObject.request_region(None, None)

    def test_authenticate(self):
        with self.assertRaises(NotImplementedError):
            self.socialObject.authenticate()

    def test_connection(self):
        with self.assertRaises(AttributeError):
            self.socialObject.test_connection()

    def test_decrypt_response(self):
        test1 = "Hello this is a basic string"
        test2 = "#%&@(#&$*&*@@(! crazy string"
        out = StringIO.StringIO()
        f = gzip.GzipFile(fileobj=out, mode='w')
        f.write(test1)
        f.close()
        compress1 = out.getvalue()
        
        out = StringIO.StringIO()
        f = gzip.GzipFile(fileobj=out, mode='w')
        f.write(test2)
        f.close()
        compress2 = out.getvalue()

        headers = [tuple(["content-encoding","gzip"])]
        self.assertEqual(self.socialObject.decrypt_response(encrypted_data=compress1, headers=headers),test1)
        self.assertEqual(self.socialObject.decrypt_response(encrypted_data=compress2, headers=headers),test2)
        pass
    def test_authenticate_headers(self):
        with self.assertRaises(NotImplementedError):
            self.socialObject.authenticate_headers()
    def test_strip_data(self):
        with self.assertRaises(NotImplementedError):
            self.socialObject.strip_data(None, None)

            
            
            
    def test_twitter_get_platform_name(self):
        self.assertEqual(self.twitterObject.get_platform_name(),'twitter')
        
    def test_twitter_connection(self):
        self.assertEqual(self.twitterObject.test_connection(),True)
        
    def test_twitter_authenticate(self):
        self.assertEqual(self.twitterObject.authenticate(),True)
        self.assertIsNotNone(self.twitterObject.access_token,"Access Token is None")
    def test_twitter_decrypt_response(self):
        test1 = "Hello this is a basic string"
        test2 = "#%&@(#&$*&*@@(! crazy string"
        out = StringIO.StringIO()
        f = gzip.GzipFile(fileobj=out, mode='w')
        f.write(test1)
        f.close()
        compress1 = out.getvalue()
        
        out = StringIO.StringIO()
        f = gzip.GzipFile(fileobj=out, mode='w')
        f.write(test2)
        f.close()
        compress2 = out.getvalue()

        headers = [tuple(["content-encoding","gzip"])]
        self.assertEqual(self.twitterObject.decrypt_response(encrypted_data=compress1, headers=headers),test1)
        self.assertEqual(self.twitterObject.decrypt_response(encrypted_data=compress2, headers=headers),test2)
        pass
    def test_twitter_authenticate_headers(self):
        expected ={ "User-Agent":"TeamOmicron", "Authorization": "Bearer %s" % self.twitterObject.access_token, "Content-type": "application/x-www-form-urlencoded;charset=UTF-8", 'Accept-Encoding': 'gzip,deflate'} 
        self.assertDictEqual(expected, self.twitterObject.authenticate_headers(),"twitter headers")
                               
    def test_twitter_request_center_radius(self):
        pass
        #self.twitterObject.request_center_radius(search_tags=["#snow"], gps_center=None, radius=None)
        #self.twitterObject.request_center_radius(search_tags=["#snow"], gps_center=tuple([]), radius=None)        
      
    def test_twitter_request_region(self):
        with self.assertRaises(NotImplementedError):
            self.twitterObject.get_platform_name()
    def test_twitter_strip_data(self):
        with self.assertRaises(NotImplementedError):
            self.twitterObject.get_platform_name()





          

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()