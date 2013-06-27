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
    ERROR = {'succes':'False'}
    def GET(self):
        '''
            Handles GET requests received from users.
            
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

#:Groups the URL's and their corresponding actions.
urls = ("/request_handler","request_handler")

#:Creates a Application to delegate requests based on path.
app = web.application(urls, globals())

#:Creates the application function that is needed for the swgi mod to work. 
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()