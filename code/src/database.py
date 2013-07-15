'''
Created on 27 Jun 2013

@author: S. Schreiber
'''
import pymongo
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId
import time as Time

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
            @type IP: L{str}
            @param port: Port number with min of 0 and max of 56635
            @type port: int
            @return: Object of type L{database_handler}
            @rtype: L{database_handler}
        '''
        self.ip = IP
        self.port = port
        #TODO: comment why there is a for
        for _ in range(6):
            try:
                self.client = MongoClient(IP, port)
                break
            except Exception, e:
                print "warning", e
                Time.sleep(0.1)
    def close_database(self):
        ''' Tries to close the database, 2 know exceptions ,instance of the database failed to be created,failed to close the database 
            @return: True ,if it is successful otherwise False.
        '''
        try:
            self.client.close();
            return True
        except Exception, e:
            print "database failed to close"
            return False
            
    def store_social_data(self, time = None, query = None, social_data = None, database_name = "omicron", collection_name = None):
        '''
            Adds the social data to a specified Mongo database.
            
            @param self: Pointer to the current object.
            @type self: L{database_handler}
            @param time: The time when the request for the social data was made.  
            @type time: datetime.datetime 
            @param query: The parameters used for the search in the same format as a GET command.
            @type query: L{str}
            @param social_data: JSON Object that contains the social platforms and the relevant social data associated with them.
            @type social_data: JSON Object
            @param database_name: The name of the database.
            @type database_name: string
            @param collection_name: The name of the collection you want to access.
            @type collection_name: string
            @return: The unique id that identifies the search in the database
            @rtype: L{str}
            @raise AttributeError
            @raise Exception("Connection failure")
        '''
        if (time == None or query == None or social_data == None or database_name == None or collection_name == None):
            raise AttributeError
        
        if (self.client.alive()):
            for _ in range(60):
                try:
                    database = self.client[database_name]
                    collection = database[collection_name]
                    user_id = collection.insert({"time":time, "query":query, "data":social_data})
                    return user_id
                except Exception, e:
                    print "waring",e
                    Time.sleep(0.1)
        else:
            raise Exception("Connection failure")
        
    def get_social_data(self, time_start = None, time_end = None, query = None, database_name = "omicron", collection_name = None):
        '''
            Finds all the entries from time_start to time_end inclusive that has the same query value as the parameter query.
            Note That time_start and time_end can both take a value "'all'". The "'all'" value instructs the search to have no upper or lower bounds or both.
            
            @param self: Pointer to the current object.
            @type self: L{database_handler}
            @param time_start: The time interval the search should start at.
            @type time_start: datetime.datetime
            @param time_end: The time interval the search should end at.
            @type time_end: datetime.datetime
            @param query: The parameters used for what to search. The string must be formated the same as the parameters of a GET command including the ?.
            @type query: string
            @return: The data that meet the criteria of the search parameters.
            @rtype: JSON Object
            @param database_name: The name of the database.
            @type database_name: string
            @param collection_name: The name of the collection you want to access.
            @type collection_name: string
            @raise AttributeError
            @raise Exception("Connection failure")
        '''
        query_result = None
        if time_start == None or time_end == None or query == None or database_name == None or collection_name == None:
            raise AttributeError
        
        if (self.client.alive()):
            for _ in range(60):
                try:
                    database =  self.client[database_name]
                    collection = database[collection_name]
                    if (time_start == 'all' and time_end == 'all'):
                        query_result = collection.find({"query":query})
                    elif(time_start == 'all'):
                        query_result = collection.find({"query":query, "time":{"$lte":time_end}}) 
                    elif(time_end == 'all'):
                        query_result = collection.find({"query":query, "time":{"$gte":time_start}})
                    else:   
                        query_result = collection.find({"query":query, "time":{"$gte":time_start, "$lte":time_end}})
                except Exception, e:
                    print "waring",e
                    Time.sleep(0.1)
                return query_result
                    
        else:
            raise Exception("Connection failure")
        
    
    def get_social_data_by_id(self, id = None, database_name = "omicron", collection_name = None):
        '''
            Finds all the entries from time_start to time_end inclusive that has the same query value as the parameter query.
            Note That time_start and time_end can both take a value "'all'". The "'all'" value instructs the search to have no upper or lower bounds or both.
            
            @param self: Pointer to the current object.
            @type self: L{database_handler}
            @return: The data that meet the criteria of the search parameters.
            @rtype: JSON Object
            @param database_name: The name of the database.
            @type database_name: L{str}
            @param collection_name: The name of the collection you want to access.
            @type collection_name: L{str}
            @raise AttributeError
            @raise Exception("Connection failure")
        '''
        query_result = None
        if id == None or database_name == None or collection_name == None:
            raise AttributeError
       
        if (self.client.alive()):
            for _ in range(60):
                try:
                    database =  self.client[database_name]
                    collection = database[collection_name]
                    query_result = collection.find_one({"_id":ObjectId(id)})
                except Exception, e:
                    print "waring",e
                    Time.sleep(0.1)
        else:
            raise Exception("Connection failure")
        return query_result
    def store_social_data_by_id(self, id = None, social_data = None, database_name = "omicron", collection_name = None):
        '''
            Adds the social data to a specified Mongo database.
            
            @param self: Pointer to the current object.
            @type self: L{database_handler}
            TODO:Insert what ID is.
            @param social_data: JSON Object that contains the social platforms and the relevant social data associated with them.
            @type social_data: JSON Object
            @param database_name: The name of the database.
            @type database_name: L{str}
            @param collection_name: The name of the collection you want to access.
            @type collection_name: L{str}
            @return: The unique id that identifies the search in the database
            @rtype: L{str}
            @raise AttributeError
            @raise Exception("Connection failure")
        '''
        if (id == None or social_data == None or database_name == None or collection_name == None):
            raise AttributeError
        
        if (self.client.alive()):
            for _ in range(60):
                try:
                    database =  self.client[database_name]
                    collection = database[collection_name]
                    query_result = collection.update({"_id":ObjectId(id)},{"$set":{'data':social_data}})
                except Exception, e:
                    print "waring",e
                    Time.sleep(0.1)
                return query_result
        else:
            raise Exception("Connection failure")