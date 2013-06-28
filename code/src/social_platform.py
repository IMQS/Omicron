'''
Created on 19 Jun 2013

@author: S. Schreiber, J. J. Martin, M. Rozenkrantz
'''
import urllib
import base64
import httplib
import gzip
import StringIO
import ast
import urllib2
import json
from instagram.client import InstagramAPI #downloadable via instagrams dev site

class social_platform(object):
    '''
        Underlying data type which is extended by each social platform to \
        communicate with the social network's API
    ''' 
    def get_platform_name(self):
        '''
            Returns the name of the social platform of the object it is applied to.
 
            @param self: Pointer to the current object.
            @type self: L{social_platform}       
            @return: Returns the current platform's name.
            @rtype: String
        '''
        raise NotImplemented
    def request_center_radius(self, search_tags=None, gps_center=None, radius=None):
        '''
            Queries the underlining social API using a search area defined by a circle. 
            If any of the parameters are not included then the query is rejected 
            and the "some parameters of query are missing" will be returned.
            
            @param self: Pointer to the current object.
            @type self: L{social_platform}
            @param search_tags: A list of tags to search for.
            @type search_tags: List
            @param gps_center: A tuple consisting of longitude and latitude GPS coordinates.
            @type gps_center: A tuple of floats
            @param radius: The radius from the L{gps_center} that forms the circular region to be searched.
            @type radius: Float
            
            @return: result_set a JSON Object containing the resulting data from the request to the API
            @rtype: JSON Object
        '''
        raise NotImplementedError
    def request_region(self, search_tags=None, search_region=None):
        '''
            Queries the underlining social API using a search area defined by a region. 
            If any of the parameters are not included then the query is rejected 
            and the "some parameters of query are missing" will be returned.
            
            @param self: Pointer to the current object.
            @type self: L{social_platform}
            @param search_tags: A list of tags to search for.
            @type search_tags: List
            @param search_region: Name of the search_region - in the following format <country state city>.
            @type search_region: String
            
            @return: result_set a JSON Object containing the resulting data from the request to the API
            @rtype: JSON Object
        '''
        raise NotImplementedError
    def authenticate(self):
        '''
            Authenticates the social platform using token based Oauth authentication and saves the authentication token in self.access_token.

            @param self: Pointer to the current object.
            @type self: L{social_platform}
            @return: True, if the authentication process completed successfully. False, if the authentication process failed. Fails under the following conditions, Connection error, http error code, error if decrypted data doesn't have the correct values. 
            access token in dictionary doesnt exist.
            @rtype: Boolean
        '''
        raise NotImplemented
    def test_connection(self):
        ''' Pings a server to test if it is able to communicate to the network before making any calls to its ReST API
        
            @param self: Pointer to the current object.
            @type self: L{social_platform}
            @return: True, if the social platform is able to connect to its online API. False, if the social platform is unable to connect to its online API.
            @rtype: Boolean
        '''
        print "Testing Connection"
        try:
            urllib2.urlopen(self.test_connection_string, timeout=1)
        except urllib2.URLError:
            print "Exception Caught : connection to "+self.get_platform_name()+" timed out"
            return False
        return True
    def decrypt_response(self, encrypted_data=None, headers=None):
        '''
        Decrypts response from a reST call.
        
        @param self: Pointer to the current object.
        @type self: L{social_platform}
        @param encrypted_data: A encrypted response from a ReST call that needs to be decrypted.
        @type encrypted_data: String
        @param headers: The header response from the server, containing the encryption method.
        @type headers: Dictionary
        @return None: if one or more missing parameters or Unknown decryption method used on the server else it returns the Decrypted data.
        @rtype: String
        '''
        if (encrypted_data == None):
            print "No encrypted data"
            return None
        if (headers == None):
            print "No header data"
            return None
        buffer_data = None
        decrypted_data = None
        for i in headers:
            if(i[0] == "content-encoding"):
                encryption_type = i[1]
                break;
        if(encryption_type == "gzip"):
            buffer_data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(encrypted_data))  # decoding of the data
            decrypted_data = buffer_data.read()
        else:
            print "Unknown decryption method : "+str(encryption_type) 
        return decrypted_data 
    def authenticate_headers(self):
        ''' Returns an authorised headers for a reST call. Uses self.access_token initialised in L{authenticate()}.  
            Note : authenticate() method must first be called 
            @param self: Pointer to the current object.
            @type self: L{social_platform}
            @return: a dictionary with the basic header information of an http request.
            @rtype: Dictionary
        '''
        raise NotImplemented
    def strip_data(self, input_data=None, selected_properties=None):
        '''
            Strips the given raw data so that only the selected properties remain.
            
            @param self: Pointer to the current object.
            @type self: L{social_platform}
            @param input_data: Raw data that needs to be  
            @type input_data: JSON Object
            @param selected_properties: List of strings - either 'tags', 'location' or 'post'.
            @type selected_properties: List
            @return: The stripped data.
            @rtype: JSON Object 
        '''
        raise NotImplemented
    
class twitter_platform(social_platform):
    ''' Class for connecting to the Twitter API
    '''
    def __init__(self):
        '''Constructor defines the consumer_key, consumer_secret, HttpsConnection string, the Test connection URL, the httpsOauthstring and the access_token
            @param self: Pointer to the current object.
            @type self: L{social_platform}
        '''
        self.consumer_key = "JqsyRIEqze8MtUXvZ6PtVw"
        self.consumer_secret = "1UW0zoEC5WlLh1TS7EajRbe3W6dD5O4CQ6Jr9gmv4"
        self.https_connection_string = "api.twitter.com:443"
        self.test_connection_string = "http://twitter.com"
        self.https_oauth_string = "/oauth2/token"
        self.access_token = None
    def get_platform_name(self):
        '''
            Returns the name of the social platform of the object it is applied to.
            @param self: Pointer to the current object.
            @type self: L{social_platform}            
            @return: Returns the current platform's name.
            @rtype: String.
        '''
        return "twitter"    
    def request_center_radius(self, search_tags=None, gps_center=None, radius=None):
        ''' Queries the underlining social API with the search area defined by a circle. If any of the parameter are none then the query gets rejected 
            and the following error message will be returned "query not suitable".
            
            @param self: Pointer to the current object.
            @type self: social_platform  
            @param search_tags: A list of key words.
            @type search_tags: List 
            @param gps_center: It is a tuple that consists of longitude and latitude.
            @type gps_center: Tuple of floats
            @param radius: Is the distance from the gps_center that will be covered by the search.
            @type radius: float 
            
            @return: result_set a JSON Object containing the resulting data from the request to the API
            @rtype: JSON Object
        '''
        
        if(search_tags == None):
            print "Tag_list is empty"
            return None
        if(len(search_tags) == 0):
            print "Tag_list is empty"
            return None
        if(self.access_token == None):
            print "Please Request Authorization from Twitter"
            return None
        tags = ""
        for i in search_tags:
            tags = tags + " " + i
        tags = tags.strip()
        """TODO change count back to 100"""
        tags = {"q":tags, "count":10}
        
        if(gps_center != None and len(gps_center) == 2 and radius != None):
            tags['geocode'] = str(gps_center[0]) + " " + str(gps_center[1]) + " " + str(radius) + "km"
        
        
        params = urllib.urlencode(tags)
        conn = httplib.HTTPSConnection(self.https_connection_string)
        head = self.authenticate_headers()
        conn.request("GET", "/1.1/search/tweets.json?" + params, "", head)
        response = conn.getresponse()
        if(response.status != 200):
            print "Error Failed to get Twitter data"
            return None
        result_set = response.read()
 
        result_set = self.decrypt_response(encrypted_data=result_set, headers=response.getheaders())
        conn.close()
        result_set = json.loads(result_set)
        return result_set
    def request_region(self, search_tags=None, search_region=None):
        '''
            @todo: Request tweets from a region
            @param self: Pointer to the current object.
            @type self: L{social_platform}
            
            @return: result_set a JSON Object containing the resulting data from the request to the API
            @rtype: JSON Object
        '''
        return "TODO:"
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
        urllib2.quote(self.consumer_key)  # URL encoding
        urllib2.quote(self.consumer_secret)  # URL encoding
        if(self.test_connection() == False):
            print "Connection Error"
            return False
        encoded = base64.b64encode(str(self.consumer_key) + ":" + str(self.consumer_secret))  # base64 encoding to twitter standards
        headers = { "User-Agent":"TeamOmicron", "Authorization": "Basic %s" % encoded, "Content-type": "application/x-www-form-urlencoded;charset=UTF-8", 'Accept-Encoding': 'gzip,deflate'}  # declear headers
        params = urllib.urlencode({'grant_type':'client_credentials'})  # declear parameters aka body of html
        conn = httplib.HTTPSConnection(self.https_connection_string)  # host api in httpsconnection
        # conn.set_debuglevel(1)
        print "Requesting"
        conn.request("POST", self.https_oauth_string, params, headers)
        print "Request Completed"
        response = conn.getresponse()
        if(str(response.status) != "200"):
            print "Error http request failed status" + str(response.status) + " Reason: " + str(response.reason)
            return False
        encrypted_data = response.read()        
        decrypted_data = self.decrypt_response(encrypted_data, response.getheaders())  # html object of decoded data
        try:
            decrypted_data = ast.literal_eval(decrypted_data)
        except SyntaxError:
            print "Error in converting decrypted data to dictionary "
            return False
        access_token = None  # convert to dictionary
        try:
            access_token = decrypted_data["access_token"]
        except TypeError:
            print "Access Token not assigned by social media"
            return False
        except KeyError:
            print "Access Token not assigned by social media"
            return False
        
        self.access_token = access_token
        return True
    def authenticate_headers(self):
        ''' Returns an authorised header for a reST call. Uses self.access_token initialised in L{authenticate()}.  
            Note : L{authenticate()} method must first be called
            @param self: Pointer to the current object.
            @type self: L{social_platform}
            @return: A dictionary with the basic header information of an http request.
            @rtype: Dictionary
        '''
        headers = { "User-Agent":"TeamOmicron", "Authorization": "Bearer %s" % self.access_token, "Content-type": "application/x-www-form-urlencoded;charset=UTF-8", 'Accept-Encoding': 'gzip,deflate'} 
        return headers

    def strip_data(self, input_data=None, selected_properties=None):
        '''
        Strips the given raw data so that only the selected properties remain.
            
            @param input_data: Raw data that needs to be  
            @type input_data: JSON Object
            @param selected_properties: List of properties that should be kept after stripping. Has to be one or more of the following 'tags', 'location' or 'post'.
            @type selected_properties: List
            @return: The stripped data.
            @rtype: JSON Object 
        '''
        if(selected_properties == None):
            print "There are no properties to strip the data by"
            return None
        
        if(input_data == None):
            print "Result_set undefined"
            return None
        search_set = input_data['statuses']
        result_set = {}
        
        if('post' in selected_properties):
            for tweet in search_set:
                if(tweet['text'] != None):
                    result_set['posts'] = result_set.update({'posts':tweet['text']})

        if('location' in selected_properties):
            for tweet in search_set:
                if(tweet['geo'] != None):
                    result_set.update({'location':tuple([tweet['geo']['coordinates'][0], tweet['geo']['coordinates'][1]])})
            
        
        search_set = input_data['search_metadata']
        if('tags' in selected_properties):
            if(search_set['query']):
                result_set.update({'tags':search_set['query'].replace('%23', '#').split('+')}) 
        
        #return result_set
           
        """ search_set = input_data['search_metadata']
        if('tags' in selected_properties):
            if(input_data['search_metadata']):
                result_set.update({'tags':search_set['query'].replace('%23', '#').replace('+', ' ').split(' ')})         
        
        newset = ''
        for element in result_set['tags']:
                newset = newset+element 
        reset = newset.split('#') 
        print reset"""
        #for i in len(reset):
        #        result_set['tags'][i] = reset[i]
        
        return result_set
"""        search_set = input_data['search_metadata']
        if('tags' in selected_properties):
            for instapost in search_set:

                result_set.update({'tags':search_set['query']}) 
        newset = ''
        s = result_set['tags'].split(' ')
        for element in s:
            if ('#' in element):
                newset = newset+element
        reset = newset.split('#')
        
        result_set['tags'] = reset # = reset.pop(0)        
                
        print reset """
        
    
class instagram_platform(social_platform):
    def __init__(self):
        '''Constructor defines the client_id, client_secret, HttpsConnection string, the Test connection URL, the httpsOauthstring and the access_token
            @param self: Pointer to the current object.
            @type self: L{social_platform}
        '''
        self.client_id = "209d4256fd0540f6b23e6ee4c82821f4"
        self.client_secret = "6bbde185375e4ec4b4178555a0387cf8"
        self.https_connection_string = "api.instagram.com:443"
        self.test_connection_string = "http://instagram.com"
        self.https_oauth_string = "/oauth2/token"
        
        self.access_token = None
        
        self.redirect = "http://www.superfluous.imqs.co.za/Omicron/redirect"
        self.api = InstagramAPI(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect)
        self.redirect = self.api.get_authorize_login_url(scope = "")
        
    def get_platform_name(self):
        '''
            Returns the name of the social platform of the object it is applied to.
            @param self: Pointer to the current object.
            @type self: L{social_platform}            
            @return: Returns the current platform's name.
            @rtype: String.
        '''
        return "instagram"    
    def request_center_radius(self, criteria=None, center=None, radius=None):
        "TODO:"     
        raise NotImplemented
    def request_region(self, criteria=None, area=None):
        "TODO:"
        raise NotImplemented        
    def authenticate(self,code=None):
        ''' Instagram authentication, must be called twice to authenticate completely, first call of authentication takes no parameters and requests \
            authentication to the instagram server by being redirected to the instagram site requesting a code.
            Once the code has been requested instagram will redirect to the servers redirect site 'superfluous.imqs.co.za/Omicron/redirect' with parameters \
            platform=instagram and code="some code" such that the site would be 'superfluous.imqs.co.za/Omicron/redirect?platform=instagram&code="some code"' \
            at this redirect site you must call this method again but with the code as the parameter to complete the authentication for the instance of this object
            
            @param code: A code generated by Instagrams servers, on first call for authentication this must be None.
            @type code: String
            
            @return: Returns a redirect string to retrieve an authentication code from on the first call if code is None, if code is not None \
                        it will exchange the code for an access token and store the access token in self.access_token and return True
        '''
        if(code == None):
            return self.redirect
        else:
            self.access_token = self.api.exchange_code_for_access_token(code)
        return True
            
        
    def authenticate_headers(self):
        raise NotImplemented    
    
    def strip_data(self, input_data=None, selected_properties=None):
        '''
        Strips the given raw data so that only the selected properties remain.
            
            @param input_data: Raw data that needs to be  
            @type input_data: JSON Object
            @param selected_properties: List of properties that should be kept after stripping.
            @type selected_properties: List of strings - either 'tags', 'location' or 'post'.
            @return: The stripped data.
            @rtype: JSON Object 
        '''
        if(selected_properties == None):
            print "There are no properties to strip the data by"
            return None
        
        if(input_data == None):
            print "Result_set undefined"
            return None
        search_set = input_data['data']
        result_set = {}
        
        if('post' in selected_properties):
            for instapost in search_set:
                if(instapost['link'] != None):
                    result_set.update({'posts':{'link': instapost['link'], 'caption' : instapost['caption']['text']}})
    
        if('location' in selected_properties):
            for instapost in search_set:
                if(instapost['location'] != None):
                    result_set.update({'location':tuple([instapost['location']['latitude'], instapost['location']['longitude']])})
            
        if('tags' in selected_properties):
            for instapost in search_set:
                if(instapost['caption'] != None):
                    result_set.update({'tags':instapost['text']}) 
        newset = ''
        s = result_set['tags'].split(' ')
        for element in s:
            if ('#' in element):
                newset = newset+element
        reset = newset.split('#')
        reset.pop(0)
        result_set['tags'] = reset.pop(0)
        
        return result_set 
    
if __name__ == '__main__':
    k = twitter_platform()
    k.authenticate()
    search_set = k.request_center_radius(["#snow #winter"])
    print k.strip_data(search_set, ['tags'])

    
    
    
