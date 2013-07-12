'''
Created on 21 Jun 2013

@author: Javonne Martin
'''
import unittest
import gzip
import social_platform as sp
import StringIO
import pickle_twitter_data as pick
import pickle


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
        #TODO
#        with self.assertRaises(ExceptionError):
#            self.socialObject.test_connection()
        pass

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
        self.assertDictEqual(expected, self.twitterObject.authenticate_headers(),"twitter headers failed")
                               
    def test_twitter_request_center_radius(self):
        self.assertEquals(self.twitterObject.authenticate(),True)
        searchtags = ["#snow"]
        result_set = self.twitterObject.request_center_radius(search_tags=searchtags, gps_center=None, radius=None)
        self.assertIsNotNone(result_set, "")
        self.assertIn('statuses', result_set, "Couldn't find statuses in json")
        self.assertIn('search_metadata', result_set, "Couldn't find search_metadata in json")     
      
    def test_twitter_request_region(self):
        with self.assertRaises(NotImplementedError):
            self.twitterObject.request_region('search_tags', 'search_region')
   
    def test_twitter_strip_data(self):
        data = pickle.load( open( "../../tools/tweets.p", "rb" ) )
        tags_data = self.twitterObject.strip_data(data, ['tags'])
        location_data = self.twitterObject.strip_data(data, ['location']) 
        post_data = self.twitterObject.strip_data(data, ['post']) 
        self.assertIn('location', location_data, 'There is no location data in Twitter data ')
        self.assertIn('posts', post_data, 'There are no posts corresponding to geo-coordinates in the Twitter data')
        self.assertNotIn('posts', location_data, 'There are posts when only location should be contained')
        self.assertIn(pick.hashtag, tags_data['tags'] ,'Incorrect tag returned from Twitter data')
        self.assertIn(pick.hashtag, post_data['posts'], 'Incorrect posts returned.')
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
