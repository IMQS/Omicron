#!/bin/bash python
'''
Created on 19 Jun 2013

@author: S. Schreiber
'''
import sys, os
sys.path.append('/var/www/webpy-app/')
import web
import json
from gateway import gateway

class request_handler(object):
    '''
        Handles all incoming GET and POST requests
    '''
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
            @todo: Figure out what to return.
            
        '''
        data = web.input()
        platforms = data["platforms"].lstrip('u').split("#")
        tags = data["tags"].lstrip('u').split("_")
        function = data["function"]
        location_type = data["location_type"] # For future use
        location = data["location"].lstrip('u').split("#")
        gatewayO = gateway()
        if (function == "heat_map"):
            import map_plot as mp
            query_data = gatewayO.execute_requests(platforms, tags, (float(location[0]),float(location[1])),float(location[2]),['location'])
            print query_data
            total_coords = []
            for platform in platforms:
                for coords in query_data[platform]:
                    print coords
                    print total_coords
                    total_coords = total_coords + coords
            heat_map = {}
            #@TODO: FIX the bounding box big problem
            heat_map['Heat_map'] = mp.heatmap([float(location[0])-5, float(location[0])+5, float(location[1])-5, float(location[1])+5], total_coords)
            return heat_map
        else :
            return "The function that was specified was not found."
        return query_data
    
    def POST(self):
        '''
            Handles POST requests received from users.
            
            @param self: a Instance of the current object.
            @type self: request_handler
            @param query: It holds the relevant data needed to perform the request. It has the following fields; platforms, preset, tags, function, location_type and location.
            @rtype query: JSON Object
            @todo: Figure out what to return.
        '''
        data = web.input()
        platforms = data["platforms"].lstrip('u').split("#")
        tags = data["tags"].lstrip('u').split("_")
        function = data["function"]
        location_type = data["location_type"] # For future use
        location = data["location"].lstrip('u').split("#")
        gatewayO = gateway()
        if (function == "heat_map"):
            import map_plot as mp
            query_data = gatewayO.execute_requests(platforms, tags, (float(location[0]),float(location[1])),float(location[2]),['location'])
            print query_data
            total_coords = []
            for platform in platforms:
                for coords in query_data[platform]:
                    print coords
                    print total_coords
                    total_coords = total_coords + coords
            heat_map = {}
            #@TODO: FIX the bounding box big problem
            heat_map['Heat_map'] = mp.heatmap([float(location[0])-5, float(location[0])+5, float(location[1])-5, float(location[1])+5], total_coords)
            return heat_map
        else :
            return "The function that was specified was not found."
        return query_data

#:Groups the URL's and their corresponding actions.
urls = ("/request_handler","request_handler")

#:Creates a Application to delegate requests based on path.
app = web.application(urls, globals())

#:Creates the application function that is needed for the swgi mod to work. 
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()