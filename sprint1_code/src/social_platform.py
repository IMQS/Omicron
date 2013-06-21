'''
Created on 19 Jun 2013

@author: evilclam
'''
import urllib
import base64
import httplib
import gzip
import StringIO
import ast
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
    def authenticate(self):
        '''
            Authenticates the Application "TeamOmicron" for read-only access to the social media platform. Uses the self.consumer_key and self.consumer_secret
            initialize in the social media platform object. Encodes the consumer_key and consumer_secret by encoding to URL encode (RFC 1783), concatinates the two encoded values
            separated by a colon and encodes the concatinated string in base64 binary to text. Uses the base64 encode string and added to the header of the 
            HTTPS request as "'Authorization': 'Basic %s' %EncodedString" with parameters to the request "'grant_type':'client_credentials'".
            A HTTPS POST is made on port 443 with the Headers and Parameters to the websites Authentication api, then a getresponse() call is made by the
            HTTPS connection,read and then decrypted using gzip. With the resulting data a string which is casted into a dictionary for easy access.
            
            @param self: Pointer to the current object.
            @type self: social_platform  s
        '''
        consumer_key           = "JqsyRIEqze8MtUXvZ6PtVw"
        consumer_secret        = "1UW0zoEC5WlLh1TS7EajRbe3W6dD5O4CQ6Jr9gmv4"

        urllib.quote(consumer_key)     #URL encoding
        urllib.quote(consumer_secret)    #URL encoding

        encoded = base64.b64encode(str(consumer_key)+":"+str(consumer_secret))    #base64 encoding to twitter standards
        headers = { "User-Agent":"TeamOmicron","Authorization": "Basic %s" % encoded,"Content-type": "application/x-www-form-urlencoded;charset=UTF-8",'Accept-Encoding': 'gzip,deflate'}         #declear headers
        params = urllib.urlencode({'grant_type':'client_credentials'})        #declear parameters aka body of html
        conn = httplib.HTTPSConnection("api.twitter.com:443")            #host api in httpsconnection
        #conn.set_debuglevel(1)
        print "Requesting"
        conn.request("POST", "/oauth2/token",params, headers)
        print "Request Completed"
        
        
        response = conn.getresponse()
        print response.status, response.reason
        EncryptedData = response.read()
        
        
        print response.getheaders()
        print EncryptedData
        
        Bufferdata = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(EncryptedData))    #decoding of the data
        data = Bufferdata.read()                            #html object of decoded data
        conn.close()
        data = ast.literal_eval(data)                     #convert to dictionary
        Access_Token = data["access_token"]
        return data
    def authenticate_headers(self):

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