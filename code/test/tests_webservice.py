'''
Created on 11 Jul 2013

@author: javonne
'''
import unittest
import web
import webservice as ws
import webservice

class test_webservice(unittest.TestCase):
    '''
        Tests the webservice and all of its classes.
    '''
    
    def test_request_handler_without_id_1(self):
        '''
            Test a basic call to L{webservice.request_handler} to make shore it can handle a call with a full set of parameters and not just the search id.
        '''
        self.set_up_webinput()
        web.ctx.env = {'QUERY_STRING':'tags=%23imqs_%23nolights&location=-33.96_18.83_2000&location_type=radius&platforms=twitter&function=heat_map&directory=/0/0/0.png','REQUEST_METHOD':'GET'}
        #try:    
        redirectObj = ws.request_handler()
        dict_ = {}
        answer = redirectObj.GET()
        if dict_.__class__ == answer.__class__:
            assert False
        else:
            assert True
        #except:
        #    assert False
        
        
    def test_reqeust_with_id(self):
        '''
             Test a basic call to L{webservice.request_handler} to make shore it can handle a call with just the search id.
        '''
        self.set_up_webinput()
        web.ctx.env = {'QUERY_STRING':'user_id=51e3ee88922e5618149b610a&directory=/0/0/0.png','REQUEST_METHOD':'GET'}
        try:    
            redirectObj = ws.request_handler()
            dict_ = {}
            answer = redirectObj.GET()
            if dict_.__class__ == answer.__class__:
                assert False
            else:
                assert True
        except:
            assert False
    
    def test_request_search_id_get(self):
        '''
            Test basic functionality that should not error with GET call
        '''
        self.set_up_webinput()
        web.ctx.env = {'QUERY_STRING':'','REQUEST_METHOD':'GET'}
        try:
            redirectObj = ws.request_search_id()
            redirectObj.GET()
            assert True
        except:
            assert False
    def test_request_search_id_get_full(self):
        '''
            Test basic functionality that should not error with GET call
        '''
        self.set_up_webinput()
        web.ctx.env = {'QUERY_STRING':'tags=%23imqs_%23nolights&location=-33.96_18.83_2000&location_type=radius&platforms=twitter&function=heat_map','REQUEST_METHOD':'GET'}
        try:
            redirectObj = ws.request_search_id()
            redirectObj.GET()
            assert True
        except:
            assert False
    

    def test_redirect_handler1(self):
        '''
            tests the redirect handler should redirect the user to /authorise?platform=instagram&code=1234567890
            if provided with a code and platform as parameters it will redirect to that page
        '''
        self.set_up_webinput()
        web.ctx.env = {'QUERY_STRING':'code=1234567890&platform=instagram&pl=jacl','REQUEST_METHOD':'GET'}
        redirectObj = ws.redirect_handler() 
        with self.assertRaises(web.SeeOther):
            redirectObj.GET()
        self.assertEqual(web.ctx.headers[2][1],"/user_auth?platform=instagram&code=1234567890")
        reload(web)
    def test_redirect_handler2(self):
        '''
            tests the redirect handler should redirect the user to /index
            since no code and platform was given
        '''
        self.set_up_webinput()
        web.ctx.env = {'QUERY_STRING':'','REQUEST_METHOD':'GET'}
        redirectObj = ws.redirect_handler() 
        with self.assertRaises(web.SeeOther):
            redirectObj.GET()
        self.assertEqual(web.ctx.headers[2][1],"/index")
        reload(web)
    def test_redirect_handler3(self):
        '''
            tests the redirect handler should redirect the user to /index
            since no code and platform was given
        '''
        self.set_up_webinput()
        web.ctx.env = {'QUERY_STRING':'code=1234567890','REQUEST_METHOD':'GET'}
        redirectObj = ws.redirect_handler() 
        with self.assertRaises(web.SeeOther):
            redirectObj.GET()
        self.assertEqual(web.ctx.headers[2][1],"/index")
        reload(web)
    def test_redirect_handler4(self):
        '''
            tests the redirect handler should redirect the user to /index
            since no code and platform was given
        '''
        self.set_up_webinput()
        web.ctx.env = {'QUERY_STRING':'platform=twitter','REQUEST_METHOD':'GET'} 
        redirectObj = ws.redirect_handler() 
        with self.assertRaises(web.SeeOther):
            redirectObj.GET()
        self.assertEqual(web.ctx.headers[2][1],"/index")
        reload(web)
        
    def test_redirect_handler5(self):
        '''
            tests the redirect handler should redirect the user to /index
            since no code and platform was given
        '''
        self.set_up_webinput()
        web.ctx.env = {'QUERY_STRING':'platform=twitter','REQUEST_METHOD':'POST'} 
        redirectObj = ws.redirect_handler() 
        self.assertEqual(redirectObj.POST(),"Not Implemented")
        reload(web)
        
    def set_up_webinput(self):
        web.ctx.env = {}
        web.ctx.headers = [('content',"test")]
        web.ctx.home = ''
        web.ctx.path = '/'

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()