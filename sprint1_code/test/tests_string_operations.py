import unittest
import string_operations as so
class test_class_string_operations(unittest.TestCase):
	def setUp(self):
		pass
	def test_string_concationation_hel_lo(self):
		self.assertEqual(so.string_concationation("hel","lo"),"hello")
	def test_string_concationation_4_lo(self):
		self.assertEqual(so.string_concationation(4,"lo"),None)
	def test_string_int_concationation_4_hello(self):
		self.assertEqual(so.string_int_concationation(4,"hello"), None)
	def test_string_int_concationation_hello_4(self):
		self.assertEqual(so.string_int_concationation("hello",4), None)
if __name__ == "__main__":
	unittest_main()
		
