import unittest
import map_plot

class HeatMapTest(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	########## Gauss tests ##########
	
	def test_gauss_zero(self):
		self.assertEqual(map_plot.gauss(1, 0), 1)
	
	def test_gauss_large(self):
		self.assertEqual(map_plot.gauss(1, 100), 0) 
	
	def test_gauss_value(self):
		self.assertEqual(int(map_plot.gauss(100,10)*1e16)/1.e16,0.3678794411714423)

	########## Random coordinate tests ##########
	
	
	
	########## Heatmap tests ##########
	
	
	
	########## Saving tests ##########
	
	

if __name__ == '__main__':
	unittest.main()
