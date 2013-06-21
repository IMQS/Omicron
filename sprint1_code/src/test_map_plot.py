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
	
	def test_random_zero(self):
		c = map_plot.random_coords(0, [0, 1, 0, 1])
		self.assertEqual(len(c), 0)
	
	def test_random_len(self):
		c = map_plot.random_coords(5, [0, 1, 0, 1])
		self.assertEqual(len(c), 5)
	
	def test_random_inbounds(self):
		c = map_plot.random_coords(5, [0, 1, 0, 1])
		for p in c:
			self.assertTrue((0<p[0]<1) & (0<p[1]<1))
	
	def test_random_unique(self):
		c = map_plot.random_coords(5, [0, 1, 0, 1])
		for i in xrange(len(c)):
			for j in xrange(i+1, len(c)):
				self.assertNotEqual(c[i],c[j])
	
	########## Heatmap tests ##########
	
	def test_heatmap_zero(self):
		pass
	
	def test_heatmap_one(self):
		pass
	
	def test_heatmap_two(self):
		pass
	
	########## Saving tests ##########
	
	def test_save_name(self):
		pass

if __name__ == '__main__':
	unittest.main()
