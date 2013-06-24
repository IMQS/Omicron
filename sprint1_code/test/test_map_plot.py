import unittest
import map_plot

class HeatMapTest(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	########## Gauss tests ##########
	
	def test_gauss_zero(self):
		"""Tests if the Gauss function has value 1 at 0."""
		self.assertEqual(map_plot.gauss(1, 0), 1)
	
	def test_gauss_large(self):
		"""Tests if the Gauss function returns 0 for an extremely large value."""
		self.assertEqual(map_plot.gauss(1, 100), 0) 
	
	def test_gauss_value(self):
		"""Tests if the Gauss functions returns a correct value."""
		self.assertEqual(int(map_plot.gauss(100,10)*1e16)/1.e16,0.3678794411714423)

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
	
	########## Heatmap tests ##########
	
	def test_heatmap_zero_area(self):
		"""Tests if the heatmap function returns None when the area of the bounds is zero."""
		import sys, os
		actualstdout = sys.stdout
		sys.stdout = open(os.devnull,'w')
		hm = map_plot.heatmap([0,0,0,0],[(0,0)])
		sys.stdout = actualstdout
		self.assertIsNone(hm)
	
	def test_heatmap_one_point(self):
		"""Tests if the heatmap function correctly evaluates at a pixel exactly on top of it."""
		from math import sqrt
		import sys, os
		actualstdout = sys.stdout
		sys.stdout = open(os.devnull,'w')
		hm = map_plot.heatmap([0,1,0,1],[(.5,.5)])
		sys.stdout = actualstdout
		self.assertEqual(hm[0][0],map_plot.gauss(.125,0))
	
	def test_heatmap_two_points(self):
		"""Tests if the heatmap function correctly overlays two Gaussian surfaces."""
		from math import sqrt
		import sys, os
		actualstdout = sys.stdout
		sys.stdout = open(os.devnull,'w')
		hm = map_plot.heatmap([0,2,0,2],[(0,0),(1,1)])
		sys.stdout = actualstdout
		self.assertEqual(int(hm[0][0]*1e16)/1.e16,
			int(map_plot.gauss(.25,sqrt(.5))*2*1e16)/1.e16)
	
	########## Saving tests ##########
	
	def test_save_name(self):
		"""Tests if the heatmap saving function produces output files that use the correct nomenclature."""
		import sys, os
		actualstdout = sys.stdout
		sys.stdout = open(os.devnull,'w')
		maxi = 0
		flist = os.listdir('./heatmaps')
		for item in flist:
			if item.startswith('heatmap_') and not (item.startswith('heatmap_color_')):
				num = int(item.__getslice__(8, len(item)-4))
				if num > maxi:
					maxi = num
		num = str(maxi+1)
		while len(num) < 3:
			num = '0'+num
		hm = map_plot.heatmap([0,2,0,2],[(0,0),(1,1)])
		map_plot.save_heatmap(hm)
		sys.stdout = actualstdout
		self.assertTrue(('heatmap_'+str(num)+'.png') in os.listdir('./heatmaps'))
		self.assertTrue(('heatmap_color_'+str(num)+'.png') in os.listdir('./heatmaps'))
		os.remove('./heatmaps/heatmap_'+str(num)+'.png')
		os.remove('./heatmaps/heatmap_color_'+str(num)+'.png')

if __name__ == '__main__':
	unittest.main()

