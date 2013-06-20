'''
Created on 18 Jun 2013

@author: Shaun Schreiber
'''
import social_platform
import json
import web

class gateway(object):
    '''
        Extract raw data from the sosial media API's and returns a GeoJSON object. 
    '''
         
    def _available_sosial_media(self, names):
        '''
            Checks to see if the selected social API's are available. If not then the following exception 
            will be raised "NotImplementedError" else it will return a list of social_platform objects.
            
            @param self: a Pointer to the current object.
            @type self: gateway
            @param names: list of string names.
            @type names: List
            @return: List of social_platform objects. 
            @rtype: social_platform
        '''
        available_platforms = {}
        platform_objects = []
        
        available_platforms['twitter'] = social_platform.twitter_platform()
        available_platforms['instagram'] = social_platform.instagram_platform()
        
        for current_platform in names:
            if (not available_platforms.has_key(current_platform)):
                raise NotImplementedError
            else:
                platform_objects.append(available_platforms[current_platform])
        return platform_objects
                
    def execute_requests(self, platforms, key_words):
        '''
            Cycles through each variable in the platform list and executes a search with the
            given keywords on each platform.
            
            @param self: a Pointer to the current object.
            @type self: gateway
            @param platforms: List of social media platforms.
            @type platforms: List
            @param key_words: List of key words that will be used in the search.
            @type key_words: List
            @return: The raw data that was fetched from the social media API's.
            @rtype: GeoJSON Array
        '''
        
    def GET(self):
        '''
            This function is only for handling rest calls to /gateway.
            Cycles through each variable in the platform list and executes a search with the
            given keywords on each platform. Parameter platforms and key_words are encoded into
            the GET call.
            
            @param platforms: List of social media platforms.
            @type platforms: String
            @param key_words: List of key words that will be used in the search.
            @type key_words: String
            @param self: a Pointer to the current object.
            @type self: gateway
            @return: The raw data that was fetched from the social media API's.
            @rtype: GeoJSON array 
        '''
        user_data = web.input()
        return "Selected platforms : " + str(user_data.platforms) + " , Key_words: " +  str(user_data.key_words)
    
    def POST(self):
        '''
            This function is only for handling rest calls to /gateway.
            Cycles through each variable in the platform list and executes a search with the
            given keywords on each platform. Parameter platforms and key_words are encoded into
            a JSON Object that will be received from a POST call.
            
            @param Data: List of social media platforms.
            @type Data: JSON Object
            @param self: a Pointer to the current object.
            @type self: gateway
            @return: The raw data that was fetched from the social media API's.
            @rtype: GeoJSON array 
        '''
        
if __name__ == "__main__":
    pass