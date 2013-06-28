#!/bin/bash python
'''
Created on 19 Jun 2013

@author: S. Schreiber
'''
import sys, os
sys.path.append('/var/www/webpy-app/')
import web
import json
import map_plot as mp
from gateway import gateway

class request_handler(object):
    '''
        Handles all incoming GET and POST requests
    '''
    OK = {'success':'True'}
    ERROR = {'success':'False'}
    def GET(self):
        '''
            Handles GET requests received from users.
            
            @param self: Pointer to the current request_handler instance.
            @type self: request_handler
            @param platforms: List of underscore(_) separated values that indicate which social media to use. 
            @type platforms: String 
            @param tags: List of Underscore(_) separated values that is used for the search tags.
            @type tags: String
            @param function: Which processing function to apply after the data has been collected.
            @type function: String
            @param location_type: Either area or radius.
            @type location_type: String
            @param location: If location_type has the value "area" then location must be in the following format "country state city" else \
            if location_type has the value "radius" then location must be in the following format "longitude_latitude_<radius>" 
            @type location: String
            @return: This will vary between request depending on what processing functions are applied to the social data that was mined.
            @rtype: JSON Object
            
        '''
        return_data_and_status = {}
        raw_data = web.input()
        platforms = raw_data["platforms"].lstrip('u').split("_")
        tags = raw_data["tags"].lstrip('u').split("_")
        function = raw_data["function"]
        # For future use
        location_type = raw_data["location_type"]
        location = raw_data["location"].lstrip('u').split("_")
        gatewayO = gateway()
        if (function == "heat_map"):
            query_data = gatewayO.execute_requests(platforms, tags, (float(location[0]),float(location[1])),float(location[2]),['location'])
            total_coords = []
            for platform in platforms:
                for coords in query_data[platform]:
                    total_coords = total_coords + coords
            try:
                #@TODO: FIX the bounding box big problem
                heat_map = mp.heatmap([float(location[0])-5, float(location[0])+5, float(location[1])-5, float(location[1])+5], total_coords)
                mp.save_heatmap(heat_map)
                return_data_and_status = self.OK
            except:
                msg = "The heatmap could not be generated or stored"
                return_data_and_status = self.ERROR
                return_data_and_status["message"] = msg
        else :
            msg = "The function that was specified was not found."
            return_data_and_status = self.ERROR
            return_data_and_status["message"] = msg
        return return_data_and_status
    
    def POST(self):
        '''
            Handles POST requests received from users.
            
            @param self: Pointer to the current request_handler instance.
            @type self: request_handler
            @param platforms: List of hash(#) separated values that indicate which social media to use. 
            @type platforms: String 
            @param tags: List of Underscore(_) separated values that is used for the search tags.
            @type tags: String
            @param function: Which processing function to apply after the data has been collected.
            @type function: String
            @param location_type: Either area or radius.
            @type location_type: String
            @param location: If location_type has the value "area" then location must be in the following format "country state city" else \
            if location_type has the value "radius" then location must be in the following format "longitude#latitude#<radius>" 
            @type location: String
            @return: This will vary between request depending on what processing functions are applied to the social data that was mined.
            @rtype: JSON Object
        '''
        return_data_and_status = {}
        raw_data = web.input()
        platforms = raw_data["platforms"].lstrip('u').split("#")
        tags = raw_data["tags"].lstrip('u').split("_")
        function = raw_data["function"]
        # For future use
        location_type = raw_data["location_type"]
        location = raw_data["location"].lstrip('u').split("#")
        gatewayO = gateway()
        if (function == "heat_map"):
            query_data = gatewayO.execute_requests(platforms, tags, (float(location[0]),float(location[1])),float(location[2]),['location'])
            total_coords = []
            for platform in platforms:
                for coords in query_data[platform]:
                    total_coords = total_coords + coords
            try:
                #@TODO: FIX the bounding box big problem
                heat_map = mp.heatmap([float(location[0])-5, float(location[0])+5, float(location[1])-5, float(location[1])+5], total_coords)
                mp.save_heatmap(heat_map)
                return_data_and_status = self.OK
            except:
                msg = "The heatmap could not be generated or stored"
                return_data_and_status = self.ERROR
                return_data_and_status["message"] = msg
        else :
            msg = "The function that was specified was not found."
            return_data_and_status = self.ERROR
            return_data_and_status["message"] = msg
        return return_data_and_status

class redirect_handler:
    '''
        For all redirects from social media logins
    '''
    OK = {'success':'True'}
    ERROR = {'success':'False'}
    def GET(self):
        '''    @todo: Needs to redirect to the login to social platform page where it should be waiting for a 'code' \
               which twitter/instagram has sent to  this page as a parameter. Needs to redirect with this code to original page 
        '''
        inputs =  web.input()
        code = inputs['code']
        #web.Redirect()
        return "Redirecting"
    
class index:
    '''This class is for testing the authentication
    '''
    def __init__(self):
        self.gateway = gateway()

    def GET(self):
        
        inputs = web.input()
        code = None
        try:
            code = inputs['code']
        except KeyError:
            print "No code given, Phase 1 authentication"
        if(code == None):
            platform = inputs['platform']
            authenticate = inputs['authentication']
            print platform
            print authenticate
            if(authenticate == 'true'):
                print platform
                if(platform == 'instagram'):
                    smlist = self.gateway._available_social_media(['instagram'])
                    if(len(smlist) == 1):
                        raise web.seeother(smlist[0].authenticate(code=None))
                    return False
                elif(platform == 'twitter'):
                    return True
        else:
            smlist = self.gateway._available_social_media(['instagram'])
            if(len(smlist) == 1):
                smlist[0].authenticate(code=code)
                return "authenticated"
        return "5"
            
    def POST(self):
        raise NotImplemented

#:Groups the URL's and their corresponding actions.
urls = ("/request_handler", "request_handler",
        "/redirect", "redirect_handler",
        "/","index")

#:Creates a Application to delegate requests based on path.
app = web.application(urls, globals())

#:Creates the application function that is needed for the swgi mod to work. 
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()