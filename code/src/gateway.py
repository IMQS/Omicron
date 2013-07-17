'''
Created on 18 Jun 2013

@author: S. Schreiber
'''
import social_platform
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
            @type self: L{gateway}.
            @param names: List of names.
            @type names: L{list} of L{str}.
            @return: List of social_platform objects. 
            @rtype: L{social_platform}.
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
            given keywords on each platform. All parameters except for the auth_codes are required.
            
            @param self: A pointer to the current object.
            @type self: Gateway.
            @param platforms: L{list} of social media platforms (L{social_platforms}).
            @type platforms: L{list} of L{str}.
            @param search_tags: L{list} of key words (tags) that will be used in the search.
            @type search_tags: L{list} of L{str}.
            @param authcodes: A L{dict} of authorisation codes.
            @type auth_codes: L{dict}.
            @return: The raw data that from the social media APIs, Returns False if not all parameters are specified, auth_codes is optional
            @rtype: L{dict}.
        '''
        if(platforms == None or search_tags == None or gps_center == None or radius == None or selected_properties == None or search_region == None  ):
            return False
        is_valid = self._available_social_media(platforms)
        return_data = {}
        if is_valid == None:
            print "One or more platforms were unavailable."
            return False
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
            Only for handling REST calls to the gateway.
            
            Cycles through each variable in the platform list and executes a search with the
            given keywords (tags) on each platform. Parameter platforms and search_tags are encoded into
            the GET call.
            @attention: Not Implemented.
            @param platforms: List of social media platforms.
            @type platforms: String
            @param search_tags: List of key words that will be used in the search.
            @type search_tags: String
            @param self: a Pointer to the current object.
            @type self: gateway
            @return: The raw data that was fetched from the social media API's.
            @rtype: GeoJSON array 
        '''
        return "Not Implemented."
    
    def POST(self):
        '''
            This function is only for handling REST calls to /gateway.
            Cycles through each variable in the platform list and executes a search with the
            given keywords on each platform. Parameter platforms and search_tags are encoded into
            a JSON Object that will be received from a POST call.
            @attention: Not Implemented.
            @param Data: List of social media platforms.
            @type Data: JSON Object
            @param self: a Pointer to the current object.
            @type self: gateway
            @return: The raw data that was fetched from the social media API's.
            @rtype: GeoJSON array 
        '''
        return "Not Implemented."
    
if __name__ == "__main__":
    obj = gateway()
    print obj.execute_requests(['twitter'], ['#snow' ,'#winter'], [(56.7, 86.4)], 5000)
