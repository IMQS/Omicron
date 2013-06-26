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
            
            @param self: Pointer to the current request_handler instance.
            @type self: request_handler
            @param platforms: List of hash(#) separated values that indicate which social media to use. 
            @type platforms: String 
            @param tags: List of hash(#) separated values that is used for the search criteria.
            @type tags: String
            @param function: Which function to apply after the data has been collected.
            @type function: String
            @param location_type: Either area or radius.
            @type location_type: String
            @param location: If location_type has the value "area" then location must be in the following format "country state city" else \
            if location_type has the value "radius" then location must be in the following format "longitude latitude <radius>km" 
            @type location: String
            @TODO: Figure out how the parameters is going to be handled.
        '''
        user_data = web.input()
        platforms = user_data.platforms
        return user_data
    
    def POST(self):
        '''
            Handles POST requests received from users.
            
            @param self: a Instance of the current object.
            @type self: request_handler
            @param query: It holds the relevant data needed to perform the request. 
            @rtype query: JSON Object with the following fields; platforms, preset, tags, function, location.
            @TODO: figure out how the parameters are going to be handled.
        '''
        data = web.data()
        
        return data
        
urls = ("/request_handler","request_handler")

app = web.application(urls, globals())
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()