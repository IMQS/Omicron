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
import urllib2
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
            
            saves access_token in the object, also returns access_token
            Not all Exceptions have been caught  !
            @param self: Pointer to the current object.
            @type self: social_platform
        '''
        raise NotImplemented
    def test_connection(self):
        print "Testing Connection"
        try:
            print self.HttpsConnectionString
            urllib2.urlopen("http://twitter.com", timeout=1)
        except urllib2.URLError:
            print "Exception Caught : connection to twitter timed out"
            return False
        return True
    def decrypt_response(self,encrypted_data,headers):
        encryption_type = None
        buffer_data = None
        decrypted_data = None
        for i in headers:
            if(i[0] == "content-encoding"):
                encryption_type = i[1]
                break;
        if(encryption_type == "gzip"):
            buffer_data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(encrypted_data))    #decoding of the data
            decrypted_data = buffer_data.read()
        return decrypted_data
    
    def authenticate_headers(self):
        raise NotImplemented
    
class twitter_platform(social_platform):
    def __init__(self):
        self.consumer_key           = "JqsyRIEqze8MtUXvZ6PtVw"
        self.consumer_secret        = "1UW0zoEC5WlLh1TS7EajRbe3W6dD5O4CQ6Jr9gmv4"
        self.HttpsConnectionString  = "api.twitter.com:443"
        self.HttpsOAuthString       = "/oauth2/token"
        self.access_token = None
    def request_geographical(self, criteria=None, center=None, radius=None):
        "TODO:"
        
    def repuest_area(self, criteria = None, area = None ):
        "TODO:"
    def authenticate(self):
        '''
            Authenticates the Application "TeamOmicron" for read-only access to the social media platform. Uses the self.consumer_key and self.consumer_secret
            initialize in the social media platform object. Encodes the consumer_key and consumer_secret by encoding to URL encode (RFC 1783), concatinates the two encoded values
            separated by a colon and encodes the concatinated string in base64 binary to text. Uses the base64 encode string and added to the header of the 
            HTTPS request as "'Authorization': 'Basic %s' %EncodedString" with parameters to the request "'grant_type':'client_credentials'".
            A HTTPS POST is made on port 443 with the Headers and Parameters to the websites Authentication api, then a getresponse() call is made by the
            HTTPS connection,read and then decrypted using gzip. With the resulting data a string which is casted into a dictionary for easy access.
            
            saves access_token in the object, also returns access_token
            Not all Exceptions have been caught  !
            @param self: Pointer to the current object.
            @type self: social_platform
        '''
        urllib2.quote(self.consumer_key)     #URL encoding
        urllib2.quote(self.consumer_secret)    #URL encoding
        if(self.test_connection() == False):
            print "Connection Error"
            return None
        encoded = base64.b64encode(str(self.consumer_key)+":"+str(self.consumer_secret))    #base64 encoding to twitter standards
        headers = { "User-Agent":"TeamOmicron","Authorization": "Basic %s" % encoded,"Content-type": "application/x-www-form-urlencoded;charset=UTF-8",'Accept-Encoding': 'gzip,deflate'}         #declear headers
        params = urllib.urlencode({'grant_type':'client_credentials'})        #declear parameters aka body of html
        conn = httplib.HTTPSConnection(self.HttpsConnectionString)            #host api in httpsconnection
        #conn.set_debuglevel(1)
        print "Requesting"
        conn.request("POST", self.HttpsOAuthString,params, headers)
        print "Request Completed"
        response = conn.getresponse()
        if(str(response.status) != "200"):
            print "Error http request failed status"+str(response.status)+" Reason: "+str(response.reason)
            return None
        encrypted_data = response.read()        
        decrypted_data = self.decrypt_response(encrypted_data,response.getheaders()) #html object of decoded data
        decrypted_data = ast.literal_eval(decrypted_data)
        access_token = None                     #convert to dictionary
        try:
            access_token = decrypted_data["access_token"]
        except TypeError:
            print "Access Token not assigned by social media"
            return None
        except KeyError:
            print "Access Token not assigned by social media"
            return None
        
        self.access_token = access_token
        return access_token
    def authenticate_headers(self):
        ''' Returns headers with Authorzation of the application in the header. Uses self.access_token defined in use of authenticate().  
            authenticate() method must first be called 
        '''
        headers = { "User-Agent":"TeamOmicron","Authorization": "Bearer %s" % self.access_token,"Content-type": "application/x-www-form-urlencoded;charset=UTF-8",'Accept-Encoding': 'gzip,deflate'} 
        return headers
        
class instagram_platform(social_platform):
    def request_geographical(self, criteria=None, center=None, radius=None):
        "TODO:"
        
    def repuest_area(self, criteria = None, area = None ):
        "TODO:"
k = twitter_platform()
k.authenticate()