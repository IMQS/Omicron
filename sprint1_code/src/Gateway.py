'''
Created on 18 Jun 2013

@author: Shaun Schreiber
'''
from social_platform import social_platform as sp

class gateway(object):
    '''
        Extract raw data from the sosial media API's and returns a GeoJSON object. 
    '''
         
    def _select_sosial_media(self, names):
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
        
    def execute_requests(self, platforms, key_words):
        '''
            @param self: a Pointer to the current object.
            @type self: gateway
            @param platforms: List of social media platforms.
            @type platforms: List
            @param key_words: List of key words that will be used in the search.
            @type key_words: List
            @return: The raw data that was fetched from the social media API's.
            @rtype: GeoJSON Array
        '''
        