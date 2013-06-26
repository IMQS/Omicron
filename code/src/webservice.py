#!/bin/bash python
'''
Created on 19 Jun 2013

@author: S. Schreiber
'''
import sys, os
sys.path.append('/var/www/webpy-app/')
import web
import json
import gateway

class request_handler(object):
    def GET(self):
        '''
            Handles GET requests received from users.
            
            @param self:
            @type self: request_handler 
            @TODO: Figure out how the parameters is going to be handled.
        '''
         
    def POST(self):
        '''
            Handles POST requests received from users.
            
            @param self: a Instance of the current object.
            @type self: request_handler
            @param query: It holds the relevant data needed to perform the request. 
            @rtype query: JSON Object with the following fields; platforms, preset, tags, function, location.
            @TODO: figure out how the parameters are going to be handled.
        '''
        
        
urls = ("/request_handler","request_handler")

app = web.application(urls, globals())
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()