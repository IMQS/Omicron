'''	Test case for string_operations.py 
	Created 20 June 2013 09:52 am '''
import unittest
import string_operations as so
'''	Class test_class_string_operations extends unittest.TestCase from unittest'''
class test_class_string_operations(unittest.TestCase):
	'''setUp() passes by default '''
	def setUp(self):
		pass
	''' Tests the concatination of "hel" and "lo" to produce "hello"'''
	def test_string_concatination_hel_lo(self):
		self.assertEqual(so.string_concatination("hel","lo"),"hello")
	'''Tests the concatination of 4 and "lo" the method doesn't allow this and returns None'''
	def test_string_concatination_4_lo(self):
		self.assertEqual(so.string_concatination(4,"lo"),None)
	'''Tests the concatination of 4 and "hello" the method doesn't allow this and returns None'''
	def test_string_int_concatination_4_hello(self):
		self.assertEqual(so.string_int_concatination(4,"hello"), None)
	'''Tests the concatination of "hello" and 4 should return "hello4"'''
	def test_string_int_concatination_hello_4(self):
		self.assertEqual(so.string_int_concatination("hello",4), "hello4")
if __name__ == "__main__":
	unittest_main()
		
