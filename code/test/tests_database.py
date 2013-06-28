'''
Created on 28 Jun 2013

@author: S. Schreiber
'''
import unittest
import database
import pymongo
from pymongo import MongoClient

class test_database(unittest.TestCase):


    def test_init1(self):
        '''
           Tests the initialization with default parameters.
        '''
        try:
            database.database_handler()
            self.assertTrue(True)
        except:
            self.assertTrue(False)
            
    def test_init2(self):
        '''
            Tests the initialization with parameters superfluous.imqs.co.za and port 27017
        '''
        try:
            database.database_handler("superfluous.imqs.co.za", 27017)
            self.assertTrue(True)
        except:
            self.assertTrue(False)
            
    def test_insert(self):
        '''
            Initializations the connection with parameters superfluous.imqs.co.za and port 27017, adds a basic structure.
        '''
        try:
            connection = database.database_handler("superfluous.imqs.co.za", 27017)
            connection.store_social_data("1234", "Hello", {"test":"Hello World!"}, "test", "test")
            db = connection.client["test"]
            collection = db["test"]
            data = collection.find_one({"time":"1234"})
        except:
            assert False
        self.assertEquals((data["data"])["test"], "Hello World!", "The data that was saved is not the same as what was returned")
        self.assertEqual(data["query"], "Hello", "The query that was saved is not the same as the query that was received")
        
    def test_insert_exception1(self):
        '''
            Tests to see if the correct error is given when there is no or missing parameters.
        '''
        try:
            connection = database.database_handler("superfluous.imqs.co.za", 27017)
            connection.store_social_data()
        except (AttributeError):
            assert True
        except:
            assert False
                       
    def test_get_social_data1(self):
        '''
            Tests when both time_start and time_end equals all
        '''
        try:
            connection = database.database_handler("superfluous.imqs.co.za", 27017)
            cursor = connection.get_social_data('all', 'all', "Hello World!", "test", "test")
            for _ in cursor:
                assert False
            
            cursor = connection.get_social_data('all', 'all', "Hello", "test", "test")
            boolean = False
            for _ in cursor:
                boolean = True
            assert boolean
            
            count = connection.get_social_data('all', 'all', "Hello1", "test", "test").count()
            assert count == 1
        except:
            assert False
            
    def test_get_social_data2(self):
        '''
            Test when time_start has a value and time_end is equal to 'all'.
        '''
        try:
            connection = database.database_handler("superfluous.imqs.co.za", 27017)
            cursor = connection.get_social_data('1234', 'all', "Hello World!", "test", "test")
            for _ in cursor:
                assert False
            
            cursor = connection.get_social_data('1234', 'all', "Hello", "test", "test")
            boolean = False
            for _ in cursor:
                boolean = True
            assert boolean
            
            count = connection.get_social_data('1234', 'all', "Hello1", "test", "test").count()
            assert count == 1
        except:
            assert False

    def test_get_social_data3(self):
        '''
             Test when time_end has a value and time_start is equal to 'all'.
        '''
        try:
            connection = database.database_handler("superfluous.imqs.co.za", 27017)
            cursor = connection.get_social_data('all', '1234', "Hello World!", "test", "test")
            for _ in cursor:
                assert False
            
            cursor = connection.get_social_data('all', '1235', "Hello", "test", "test")
            boolean = False
            for _ in cursor:
                boolean = True
            assert boolean
            
            count = connection.get_social_data('all', '1240', "Hello1", "test", "test").count()
            assert count == 1
        except:
            assert False
        
    def test_get_social_data4(self):
        '''
             Test when both time_end and time_start has a value.
        '''
        try:
            connection = database.database_handler("superfluous.imqs.co.za", 27017)
            cursor = connection.get_social_data('1234', '1234', "Hello World!", "test", "test")
            for _ in cursor:
                assert False
            
            cursor = connection.get_social_data('1233', '1235', "Hello", "test", "test")
            boolean = False
            for _ in cursor:
                boolean = True
            assert boolean
            
            count = connection.get_social_data('1238', '1240', "Hello1", "test", "test").count()
            assert count == 1
        except:
            assert False
        
    def test_get_social_data_exception1(self):
        '''
            Tests to see if the correct error is given when there is no or missing parameters.
        '''
        try:
            connection = database.database_handler("superfluous.imqs.co.za", 27017)
            connection.get_social_data()
        except (AttributeError):
            assert True
        except:
            assert False
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()