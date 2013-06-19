'''
Created on 19 Jun 2013

@author: evilclam
'''

class social_platform(object):
    '''
        Basic structure that is needed to communicate with a social API
    ''' 
    def request_geographical(self, criteria = None, center = None, radius = None):
        '''
            Queries the underlining social API with the search area defined by a circle. If any of the parameter are none then the query gets rejected 
            and the following error message will be returned "query not suitable".
            
            @param self: Pointer to the current object.
            @type self: social_platform  
            @param criteria: a List of key words.
            @type criteria: List 
            @param center: It is a tuple that consists of longitude and latitude.
            @type center: Tuple of floats
            @param radius: Is the distance from the center that will be covered by the search.
            @type radius: float 
        '''
        raise NotImplementedError
    
    def repuest_area(self, criteria = None, area = None ):
        '''
            Queries the underlining social API with the search area defined by a geographical area e.g. Cape Town. If any of the parameter are none then the query gets rejected 
            and the following error message will be returned "query not suitable".
            
            @param self: Pointer to the current object.
            @type self: social_platform  
            @param criteria: a List of key words.
            @type criteria: List 
            @param area: Name of the area. Will be in the following format (country state city)
            @type area: String 
        '''
        raise NotImplementedError

class twitter_platform(social_platform):
    def request_geographical(self, criteria=None, center=None, radius=None):
        "TODO:"
        
    def repuest_area(self, criteria = None, area = None ):
        "TODO:"
        
class instagram_platform(social_platform):
    def request_geographical(self, criteria=None, center=None, radius=None):
        "TODO:"
        
    def repuest_area(self, criteria = None, area = None ):
        "TODO:"