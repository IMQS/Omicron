'''
Created on 11 Jul 2013

@author: javonne
'''
import unittest
import web
import webservice as ws

class test_webservice(unittest.TestCase):
    '''
        Tests the webservice and all of its classes.
    '''
    
    def test_request_handler_without_id_1(self):
        '''
            
        '''
        pass
    
    def test_reqeust_with_id(self):
        '''
        '''
        pass
    
    def test_authorisation(self):
        '''
        '''
        pass
    
    def test_request_search_id_get(self):
        '''
        '''
        pass
    
    def test_request_search_id_post(self):
        '''
        '''
        pass

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