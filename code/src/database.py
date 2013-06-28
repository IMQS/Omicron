'''
Created on 27 Jun 2013

@author: S. Schreiber
'''
import pymongo
from pymongo import MongoClient
import datetime

class database_handler(object):
    '''
        Handles all communication between the Mongo database and L{request_handler}. 
    '''
    def __init__(self, IP = 'localhost', port = 27017):
        '''
            Creates a database_handler instance and initializes the connection to the database with the given port and IP-address. 
            
            @param self: Pointer to the current object.
            @type self: L{database_handler}
            @param IP: IP address of where the database is if it is local then leave it.
            @type IP: String
            @param port: Port number with min of 0 and max of 56635
            @type port: int
            @return: Object of type L{database_handler}
            @rtype: L{database_handler}
        '''
        self.ip = IP
        self.port = port  
        self.client = MongoClient(IP, port)
    
    def store_social_data(self, time = None, query = None, social_data = None, database_name = "omicron", collection_name = None):
        '''
            Adds the social data to a specified Mongo database.
            
            @param self: Pointer to the current object.
            @type self: L{database_handler}
            @param time: The time when the request for the social data was made.  
            @type time: L{datetime.datetime} 
            @param query: The parameters used for the search in the same format as a GET command.
            @type query: L{string}
            @param social_data: JSON Object that contains the social platforms and the relevant social data associated with them.
            @type social_data: JSON Object
            @raise AttributeError: If a parameter is missing or None.
            @raise Exception("Connection failure"): Unable to connect to Database.
        '''
        if (time == None or query == None or social_data == None or database_name == None or collection_name == None):
            raise AttributeError
        
        if (self.client.alive()):
            database =  self.client[database_name]
            collection = database[collection_name]
            collection.insert({"time":time, "query":query, "data":social_data})
        else:
            raise Exception("Connection failure")
        
    def get_social_data(self, time_start = None, time_end = None, query = None, database_name = "omicron", collection_name = None):
        '''
            Finds all the entries from time_start to time_end exclusive that has the same query value as the parameter query.
            Note That time_start and time_end can both take a value "'all'". The "'all'" value instructs the search to have no upper or lower bounds or both.
            
            @param self: Pointer to the current object.
            @type self: L{database_handler}
            @param time_start: The time interval the search should start at.
            @type time_start: L{datetime.datetime}
            @param time_end: The time interval the search should end at.
            @type time_end: L{datetime.datetime}
            @param query: The parameters used for what to search. The string must be formated the same as the parameters of a GET command including the ?.
            @type query: L{string}
            @return: The data that meet the criteria of the search parameters.
            @rtype: JSON Object
            @raise AttributeError: If a parameter is missing or None.
            @raise Exception("Connection failure"): Unable to connect to Database.
        '''
        query_result = None
        if time_start == None or time_end == None or query == None or database_name == None or collection_name == None:
            raise AttributeError
        
        if (self.client.alive()):
            database =  self.client[database_name]
            collection = database[collection_name]
            if (time_start == 'all' and time_end == 'all'):
                query_result = collection.find({"query":query})
            elif(time_start == 'all'):
                query_result = collection.find({"query":query, "time":{"$lt":time_end}}) 
            elif(time_end == 'all'):
                query_result = collection.find({"query":query, "time":{"$gt":time_start}})
            else:   
                query_result = collection.find({"query":query, "time":{"$gt":time_start, "$lt":time_end}})
            collection.find()
        else:
            raise Exception("Connection failure")
        return query_result