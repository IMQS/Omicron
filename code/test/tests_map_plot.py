import unittest
import map_plot

class HeatMapTest(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	########## Random coordinate tests ##########
	
	def test_random_zero(self):
		"""Tests if the random point generator returns an empty set if n is zero."""
		c = map_plot.random_coords(0, [0, 1, 0, 1])
		self.assertEqual(len(c), 0)
	
	def test_random_len(self):
		"""Tests if the random point generator returns the correct number of points."""
		c = map_plot.random_coords(5, [0, 1, 0, 1])
		self.assertEqual(len(c), 5)
	
	def test_random_inbounds(self):
		"""Tests if the random point generator returns points all within the specified bounds."""
		c = map_plot.random_coords(5, [0, 1, 0, 1])
		for p in c:
			self.assertTrue((0<p[0]<1) & (0<p[1]<1))
	
	def test_random_unique(self):
		"""Tests if the random point generator returns points sufficiently random so as to never overlay (extremely small statistical chance of failure)."""
		c = map_plot.random_coords(5, [0, 1, 0, 1])
		for i in xrange(len(c)):
			for j in xrange(i+1, len(c)):
				self.assertNotEqual(c[i],c[j])

if __name__ == '__main__':
	unittest.main()

