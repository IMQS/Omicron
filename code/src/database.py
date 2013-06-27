'''
Created on 27 Jun 2013

@author: S. Schreiber
'''
import pymongo
from pymongo import MongoClient
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
    
    def set_coords_data(self, time = None, query=None, data=None):
        '''
            Adds the data to a mongo database.
            
            @param self: Pointer to the current object.
            @type self: L{database_handler}
            @param time: @todo: 
            @type time: @todo
            @param query: The parameters used for the search in the same format as a GET command.
            @type query: L{string}
            @param data: JSON Object that contains the social platform and the coordinates of .
            @type data: JSON Object
        '''
        