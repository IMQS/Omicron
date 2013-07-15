'''
Created on 18 Jun 2013

@author: S. Schreiber
'''
import social_platform
import json
import web
import urllib

class gateway(object):
    '''
        Extracts raw data from the social media's APIs and returns a GeoJSON object. 
    '''
         
    def _available_social_media(self, names):
        '''
            Checks to see if the selected social API's are available. If not then a "NotImplementedError" exception 
            will be raised, otherwise it will return a list of social_platform objects.
            
            @param self: A pointer to the current object.
            @type self: Gateway.
            @param names: List of names.
            @type names: List of strings.
            @return: List of social_platform objects. 
            @rtype: social_platform.
        '''
        available_platforms = {}
        platform_objects = []
        
        available_platforms['twitter'] = social_platform.twitter_platform()
        available_platforms['instagram'] = social_platform.instagram_platform()
        
        for current_platform in names:
            if (not available_platforms.has_key(current_platform)):
                return None
            else:
                platform_objects.append(available_platforms[current_platform])
        return platform_objects
                
    def execute_requests(self, platforms=None, search_tags=None, gps_center=None, radius=None, selected_properties=None, search_region=None,auth_codes=None):
        '''
            Cycles through each variable in the platform list and executes a search with the
            given keywords on each platform.
            
            @param self: A pointer to the current object.
            @type self: Gateway.
            @param platforms: List of social media platforms.
            @type platforms: List of strings.
            @param search_tags: List of key words (tags) that will be used in the search.
            @type search_tags: List of strings.
            @param authcodes: A dictionary of authorisation codes.
            @type auth_codes: dictionary.
            @return: The raw data that from the social media APIs.
            @rtype: GeoJSON Array.
        '''
        "TODO: Add a check to see which parameters = None"
        is_valid = self._available_social_media(platforms)
        return_data = {}
        if is_valid == None:
            "TODO: change that it returns a JSONobject"
            return "One or more platforms were unavailable."
        else :
            for social_plat in is_valid:
                if(auth_codes==None or auth_codes == '' ):
                    social_plat.authenticate()
                elif(not auth_codes.__contains__(social_plat.get_platform_name)):
                    social_plat.authenticate()                    
                else:
                    social_plat.access_token = urllib.quote(auth_codes[social_plat.get_platform_name])
                    
                data = social_plat.request_center_radius(search_tags, gps_center, radius)
                return_data[social_plat.get_platform_name()] = social_plat.strip_data(data, selected_properties)
        return return_data
    
    def GET(self):
        '''
            Only for handling reST calls to the gateway.
            
            Cycles through each variable in the platform list and executes a search with the
            given keywords (tags) on each platform. Parameter platforms and search_tags are encoded into
            the GET call.
            
            @param platforms: List of social media platforms.
            @type platforms: String
            @param search_tags: List of key words that will be used in the search.
            @type search_tags: String
            @param self: a Pointer to the current object.
            @type self: gateway
            @return: The raw data that was fetched from the social media API's.
            @rtype: GeoJSON array 
        '''
        return "Not in use."
    
    def POST(self):
        '''
            This function is only for handling rest calls to /gateway.
            Cycles through each variable in the platform list and executes a search with the
            given keywords on each platform. Parameter platforms and search_tags are encoded into
            a JSON Object that will be received from a POST call.
            
            @param Data: List of social media platforms.
            @type Data: JSON Object
            @param self: a Pointer to the current object.
            @type self: gateway
            @return: The raw data that was fetched from the social media API's.
            @rtype: GeoJSON array 
        '''
        return "Not in use."
    
if __name__ == "__main__":
    obj = gateway()
    print obj.execute_requests(['twitter'], ['#snow' ,'#winter'], [(56.7, 86.4)], 5000)