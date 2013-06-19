'''
Created on 18 Jun 2013

@author: Shaun Schreiber
'''
import social_platform
class Gateway(object):
    '''
        Extract raw data from the sosial media API's and returns a GeoJSON object. 
    '''
         
    def select_sosial_media(self, names):
        '''
            Checks to see if the selected social API's are available. If not then the following exception 
            will be raised "NotImplementedError" else it will return a list of social_platform objects.
            @param names: list of string names.
            @type names: List
            @return: List of social_platform objects. 
            @rtype: social_platform
        '''
        
    def