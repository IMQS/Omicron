#!/bin/bash python
'''
Created on 19 Jun 2013

@author: S. Schreiber, J. J. Martin
'''
import sys, os
sys.path.append('/home/omicron/Omicron2/code/src/')
import web
import json
import map_plot as mp
from gateway import gateway 
import tempfile
import social_platform as sp
from database import database_handler as db_handler 
import datetime
import urllib
import ast
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()


render = web.template.render('/home/omicron/Omicron2/code/src/web/html')#: Sets the directory for the html files.

class request_handler(object):
    '''
        Handles incoming GET and POST requests. The output may vary between the input.If the heatmap or point tweetlayer function is specified then it can interact with leaflet.   
    '''
    OK = {'success':'True'}
    ERROR = {'success':'False'}
    root="/home/omicron/Omicron2/code/src/"
    def GET_with_user_id(self, raw_data):
        '''
            Handles GET requests received from users with user_id.
            
            @param self: Pointer to the current request_handler instance.
            @type self: L{request_handler}
            @param raw_data: The object returned from web.input() Note: This can also be a normal dictionary.
            @type raw_data: L{web.utils.Storage}
            @return: The return value will change according to the given input. If it's a heapmap a .png file will be return else if the tweet point layer is selected then 
            @rtype: dynamic  
        '''
        return_data_and_status = {}
        
        l_x_y = str(raw_data["directory"]).split("/")[1:]
        user_id = raw_data['user_id']
        
        db = db_handler()
        
        query_data = db.get_social_data_by_id(obj_id=user_id, database_name='omicron', collection_name='request_information')
        db.close_database()
        
        function = query_data['query']['function']
        
        if (function == "heat_map"):
            if str(query_data['data']) == '':
                gateway0 = gateway()
                query_data['data'] = gateway0.execute_requests( query_data['query']['platforms'], query_data['query']['tags'],
                                                                 (float(query_data['query']['location'][0]),float(query_data['query']['location'][1])), radius=float(query_data['query']['location'][2])
                                                                 , selected_properties=['location'], search_region=None, auth_codes=None)
                db.store_social_data_by_id(obj_id=user_id, social_data=query_data['data'],collection_name="request_information")
            total_coords = []
            for platform in query_data['query']['platforms']:
                total_coords = total_coords + query_data['data'][platform]['location']
            try:
                web.header("Content-Type", "png") # Set the Header
                heat_map = mp.heatmap_tile(int(l_x_y[0]), int(l_x_y[1]), int(str(l_x_y[2]).split(".")[0]), total_coords)
                mp.save_heatmap(heat_map, path=self.root+"heatmaps/"+user_id+l_x_y[0] +"_" + l_x_y[1] + "_" + l_x_y[2], colour=True)
                return_data_and_status = open(self.root+"heatmaps/"+user_id+l_x_y[0] +"_" + l_x_y[1] + "_" + l_x_y[2],"rb").read()
            except Exception:
                msg = "The heatmap could not be generated or stored"
                msg = Exception.message
                return_data_and_status = self.ERROR
                return_data_and_status["message"] = msg
        elif (function == "geo_coords"):
            if str(query_data['data']) == '':
                gateway0 = gateway()
                query_data['data'] = gateway0.execute_requests( query_data['query']['platforms'], query_data['query']['tags'],
                                                                 (float(query_data['query']['location'][0]),float(query_data['query']['location'][1])), radius=float(query_data['query']['location'][2])
                                                                 , selected_properties=['location'], search_region=None, auth_codes=None)
                db.store_social_data_by_id(obj_id=user_id, social_data=query_data['data'],collection_name="request_information")
            total_coords = []
            for platform in query_data['query']['platforms']:
                total_coords = total_coords + query_data['data'][platform]['location']
            try:
                return_data_and_status = mp.coords_to_geojson(total_coords)
            except Exception:
                msg = "The points could not be generated."
                msg = Exception.message
                return_data_and_status = self.ERROR
                return_data_and_status["message"] = msg
        else :
            msg = "The function that was specified was not found."
            return_data_and_status = self.ERROR
            return_data_and_status["message"] = msg
        return return_data_and_status
        
    def GET_without_user_id(self, raw_data):
        '''
            Handles GET requests received from users without user_id.
            
            @param self: Pointer to the current request_handler instance.
            @type self: L{request_handler}
            @param raw_data: The object returned from web.input() Note: This can also be a normal dictionary.
            @type raw_data: L{web.utils.Storage}
            @return: The return value will change according to the given input. If it's a heapmap a .png file will be return else if the tweet point layer is selected then 
            @rtype: dynamic  
        '''
        return_data_and_status = {}
        platforms = raw_data["platforms"].lstrip('u').split("_")
        tags = raw_data["tags"].lstrip('u').split("_")
        function = raw_data["function"]
        location_type = raw_data["location_type"]
        location = raw_data["location"].lstrip('u').split("_")
        l_x_y = str(raw_data["directory"]).split("/")[1:]
        auth_codes_ = None
        if(raw_data.__contains__('auth_codes')):
            auth_codes_ = raw_data['auth_codes']
            
        gatewayO = gateway()
        if (function == "heat_map"):
            query_data = gatewayO.execute_requests(platforms, tags, (float(location[0]),float(location[1])),float(location[2]),['location'],auth_codes=auth_codes_)
            total_coords = []
            for platform in platforms:
                total_coords = total_coords + query_data[platform]['location']
            try:
                web.header("Content-Type", "png") # Set the Header
                heat_map = mp.heatmap_tile(int(l_x_y[0]), int(l_x_y[1]), int(str(l_x_y[2]).split(".")[0]), total_coords)
                mp.save_heatmap(heat_map, path=self.root+"heatmaps/"+l_x_y[0] +"_" + l_x_y[1] + "_" + l_x_y[2], colour=True)
                return_data_and_status = open(self.root+"heatmaps/"+l_x_y[0] +"_" + l_x_y[1] + "_" + l_x_y[2],"rb").read()
            except Exception:
                msg = "The heatmap could not be generated or stored"
                msg = Exception.message
                return_data_and_status = self.ERROR
                return_data_and_status["message"] = msg
        elif (function == "geo_coords"):
            query_data = gatewayO.execute_requests(platforms, tags, (float(location[0]),float(location[1])),float(location[2]),['location'],auth_codes=auth_codes_)
            total_coords = []
            for platform in platforms:
                total_coords = total_coords + query_data[platform]['location']
            try:
                return_data_and_status = mp.coords_to_geojson(total_coords)
            except Exception:
                msg = "The points could not be generated."
                msg = Exception.message
                return_data_and_status = self.ERROR
                return_data_and_status["message"] = msg
        else :
            msg = "The function that was specified was not found."
            return_data_and_status = self.ERROR
            return_data_and_status["message"] = msg
        return return_data_and_status
        
    def GET(self):
        '''
            Handles GET call made from the user. Interprets the parameters, gathers the data, run the specified function, if directory is set returns the correct image else returns the level zero tile.
            Note all these parameters gets received via a GET call, web.py handles it. 
            
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
            @param directory: The value that leaflet adds at the end to find a specific tile and it is in the following format </level/x/y.png>
            @type directory: String
            @param user_id: The id that will be used to search the for the search data in the mongo database.
            @type user_id: String
            @param auth_codes: The authorise token/data that can be used to authenticate the selected social platform. {<platform_name>: "data needed"}
            @type auth_codes: L{dict}  
            @return: This will vary between request depending on what processing functions are applied to the social data that was mined.
            @rtype: inconsistent
            
        '''
        return_data_and_status = {}
        raw_data = web.input()
        if raw_data.__contains__('user_id'):
            return_data_and_status = self.GET_with_user_id(raw_data)
        else:
            return_data_and_status = self.GET_without_user_id(raw_data)
        return return_data_and_status
    
    def POST(self):
        '''
            Handles POST call made from the user. Interprets the parameters, gathers the data, run the specified function, if directory is set returns the correct image else returns the level zero tile.
            Note all these parameters gets received via a POST call, web.py handles it. 
            
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
            @param directory: The value that leaflet adds at the end to find a specific tile and it is in the following format </level/x/y.png>
            @type directory: String
            @param user_id: The id that will be used to search the for the search data in the mongo database.
            @type user_id: String
            @param auth_codes: The authorise token/data that can be used to authenticate the selected social platform. {<platform_name>: "data needed"}
            @type auth_codes: L{dict}  
            @return: This will vary between request depending on what processing functions are applied to the social data that was mined.
            @rtype: inconsistent
        '''
        return_data_and_status = {}
        raw_data = web.input()
        if raw_data.__contains__('user_id'):
            return_data_and_status = self.GET_with_user_id(raw_data)
        else:
            return_data_and_status = self.GET_without_user_id(raw_data)
        return return_data_and_status

class redirect_handler:
    '''
        For all redirects from social media logins for user authentication
        @attention: Not Used in Project Omicron
    '''
    OK = {'success':'True'}
    ERROR = {'success':'False'}
    def GET(self):
        '''    @todo: Needs to redirect to the login to social platform page where it should be waiting for a 'code' \
               which twitter/instagram has sent to  this page as a parameter. Needs to redirect with this code to original page 
        '''
        inputs =  web.input()
        if(inputs.__contains__('code') and inputs.__contains__('platform')):
            code = inputs['code']
            platform = inputs['platform']
            raise web.seeother("/user_auth"+"?"+"platform="+platform+"&"+"code="+code)
            return "Authenticating"
            
        #web.Redirect()
        raise web.seeother("/index")
        return "Redirecting to Home page"
    def POST(self):
        return "Not Implemented"
    
class twitter_app_only_authorisation:
    '''
        Application only authorisation method for twitter
        @return: access token used to authenticate with twitter as an application, if failure returns 'Error'
        @rtype: L{str}
    '''
    def GET(self):
        ''' 
            Application only authorisation method for twitter
            @return: access token used to authenticate with twitter as an application, if failure returns 'Error'
            @rtype: L{str}
        '''
        twitterobject = sp.twitter_platform()
        if(twitterobject.authenticate()):
            return twitterobject.access_token
        return "Error"
    def POST(self):
        '''
            Raises Not implemented exception
            @attention: Not Implemented
        '''
        return "Not Implemented"

class user_authorisation:
    '''
        Authenticates a user to use the social media sites as authenticated by their profile
        @attention: Not Used in Project Omicron
    '''
    def GET(self):
        '''
            2 Phase authentication for the user 
            @attention: Not implemented in Project Omicron
        '''
        inputs = web.input()
        code = None
        platform = inputs['platform']
        gateway = gateway()
        code = None
        if(input.__contains__('code')):
            code = inputs['code']
        else:
            print "No code given, Phase 1 authentication"
        if(code == None):
            authenticate = inputs['authentication']
            print platform
            print authenticate
            if(authenticate == 'true'):
                print platform
                if(platform != None ):
                    self.smlist = self.gateway._available_social_media([platform])
                    if(len(self.smlist) == 1):
                        raise web.seeother(self.smlist[0].authenticate(code=None))
                    return False
        else:
            smlist = self.gateway._available_social_media([platform])
            if(len(smlist) == 1):
                smlist[0].authenticate(code=code)
                return smlist[0].access_token
        return "Authorisation failed please Re-authorise"
    def POST(self):
        raise NotImplementedError

class index(object):
    '''
        Used to load the index page via a GET call. The POST call is not supported.
    '''
    def GET(self):
        '''
            Returns the index page.
            
            @param self: Pointer to the current L{webservice.index}  instance.
            @type self: L{webservice.index}
            @return: The index webstie.
            @rtype: L{str} 
        '''
        return render.index()
    def POST(self):
        '''
            This function is not supported.
            @return: A dictionary  that contains success:false and msg:POST call not supported. 
        '''
        return {'success':'false','msg':'POST call not supported'}

class main(object):
    '''
        Used to load the main page via a GET or POST call.
    '''
    def GET(self):
        '''
            Returns the main page.
            
            @param self: Pointer to the current L{webservice.main} instance.
            @type self: L{webservice.main}
            @return: The index webstie.
            @rtype: L{str} 
        '''
        return render.main()
    def POST(self):
        '''
            Returns the main page.
            
            @param self: Pointer to the current L{webservice.main} instance.
            @type self: L{webservice.main}
            @return: The index webstie.
            @rtype: L{str} 
        '''
        return render.main()

class request_search_id(object):
    '''
        Returns the search id needed to find and return the correct results from the database. 
    '''
    OK = {'success':'True'}
    ERROR = {'success':'False'}
    def GET(self):
        '''
            Rest call that returns the search id needed to search, find and return data.
            
            @param self: Current instance of the L{request_search_id} object.
            @type self: L{request_search_id}
            @param query: Formated string that contains the follow parameters platforms, location, function, 
            @type query: L{str}
            @return id: The search id. 
            @rtype: L{str}
        '''
        raw_data = web.input()
        db = db_handler()
        user_time = datetime.datetime.now()
        location_type = ''
        user_query = ''
        query_data = ''
        auth_codes_ = ''
        if (raw_data.__contains__("location") and raw_data.__contains__("platforms") and raw_data.__contains__("tags") and raw_data.__contains__("function") and raw_data.__contains__("location_type")):
            platforms = raw_data["platforms"].lstrip('u').split("_")
            tags = raw_data["tags"].lstrip('u').split("_")
            function = raw_data["function"]
            location_type = raw_data["location_type"]
            location = raw_data["location"].lstrip('u').split("_")
            user_query = {'platforms':platforms, 'function':function, 'tags':tags, 'location_type':location_type, 'location':location}
            
        if (raw_data.__contains__('auth_codes')):    
            auth_codes_ =  urllib.unquote(raw_data['auth_codes']).decode('utf8')
            auth_codes_ = ast.literal_eval(auth_codes_)
            user_query['auth_codes'] = auth_codes_
       
        gatewayO = gateway()
        
        if (location_type == 'area'):
            query_data = gatewayO.execute_requests(platforms=platforms, search_tags=tags, selected_properties=['location'], search_region=location[0], auth_codes=auth_codes_ )
        elif (location_type == 'radius'): 
            query_data = gatewayO.execute_requests(platforms=platforms, search_tags=tags, gps_center=(float(location[0]),float(location[1])),radius=float(location[2]),selected_properties=['location'], auth_codes=auth_codes_)

        user_id = db.store_social_data(time=user_time, query=user_query, social_data=query_data, database_name='omicron', collection_name='request_information')
        return_data_and_status = str(user_id)
        return return_data_and_status
        
    def POST(self):
        '''
            Rest call that returns the search id needed to search, find and return data.
            
            @param self: Current instance of the L{request_search_id} object.
            @type self: L{request_search_id}
            @param query: Formated string that contains the follow parameters platforms, location, function, 
            @type query: L{str}
            @return id: The search id. 
            @rtype: L{str}
        '''
        raw_data = web.input()
        db = db_handler()
        user_query = raw_data['query']
        user_time = datetime.datetime.now()
        user_id = db.store_social_data(time=user_time, query=user_query, social_data='', database_name='omicron', collection_name='request_information')
        return_data_and_status = str(user_id)
        return return_data_and_status
    
urls = ("/request_handler", "request_handler",
        "/redirect", "redirect_handler",
        "/authorise", "twitter_app_only_authorisation",
        "/index.*", "index",
        "/main.*", "main",
        "/request_search_id", "request_search_id", 
        "/", "index",
        "/user_auth","user_authorisation")#:Groups the URL's and their corresponding actions.

app = web.application(urls, globals()) #:Creates a Application to delegate requests based on path.


application = app.wsgifunc() #:Creates the application function that is needed for the swgi mod to work.


if __name__ == "__main__":
    app.run()
