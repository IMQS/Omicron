'''
Created on 18 June 2013

@author: M. Arzul
'''

def plot(coords):
	'''
	Makes a simple scatter plot of given coordinates within a box that in X and Y spans the floor and ceiling integers of the minima and maxima respectively.
	@param coords: The X, Y coordinates of points.
	@type coords: List of 2-tuples of floats
	@rtype: Void
	'''
	import matplotlib.pyplot as plt
	x_coords = []
	y_coords = []
	for point in coords:
		x_coords.append(point[0])
		y_coords.append(point[1])
		print "plotting: ("+str(point[0])+", "+str(point[1])+")"
	plt.xlim(int(min(x_coords)),int(max(x_coords))+1)
	plt.ylim(int(min(y_coords)),int(max(y_coords))+1)
	plt.scatter(x_coords, y_coords, )
	plt.show()

def plot_random(num, bounds):
	'''
	Plots random points.
	@param num: The number of points to generate.
	@type num: Integer
	@param bounds: The bounding coordinates of the points to generate, in the form [left, right, bottom, top].
	@type bounds: List of 4 ints
	@rtype: Void
	'''
	from random import random as r
	points = random_coords(num, bounds)
	plot(points)

def random_coords(num, bounds):
	'''
	Returns random points.
	@param num: The number of points to generate.
	@type num: Integer
	@param bounds: The bounding coordinates of the points to generate, in the form [left, right, bottom, top].
	@type bounds: List of 4 ints
	@return: List of 2-tuples of floats that represents a set of X, Y coordinates.
	@rtype: List of 2-tuples of floats
	'''
	from random import random as r
	points = []
	xdim = bounds[1] - bounds[0]
	ydim = bounds[3] - bounds[2]
	for i in xrange(num):
		x = r()*xdim + bounds[0]
		y = r()*ydim + bounds[2]
		points.append((x, y))
	return points

def heatmap(bounds, coords):
	'''
	Creates a heatmap within the specified bounds for the given coordinates. Variance is adjusted according to point density. If the area of the bounds is zero, None is returned.
	@param bounds: The bounding coordinates of the points to generate, in the form [left, right, bottom, top].
	@type bounds: List of 4 ints
	@param coords: The X, Y coordinates of points.
	@type coords: List of 2-tuples of floats.
	@return: A pixel matrix heatmap for the given points.
	@rtype: Rectangular numpy matrix of floats
	'''
	import numpy as np
	
	rdim = bounds[1] - bounds[0]
	cdim = bounds[3] - bounds[2]
	
	if cdim*rdim == 0:
		print "AREA OF BOUNDS IS ZERO: NO HEATMAP RETURNED"
		return None
	
	n = len(coords)
	print n, "points provided."
	
	heatmap = np.array([[0.]*rdim]*cdim)
	
	print "For bounds "+str(bounds)+", extent is "+str(rdim)+" by "+str(cdim)+" and area is "+str(rdim*cdim)+"."
	
	p_dens = float(n)/(rdim*cdim)
	var = 1 / (8*p_dens)
	print "Point density of "+str(p_dens)+" gives a variance estimate of "+str(var)+"."
	
	for point in coords:
		print "Processing:",str(point)
		for i in xrange(cdim):
			for j in xrange(rdim):
				heatmap[i][j] += gauss(var,
				heat_dist(point,j+bounds[0]+.5,i+bounds[2]+.5))
				# the +.5 is to account for pixel center
	
	return heatmap

def show_heatmap(heatmap, bounds):
	'''
	Displays a heatmap within certain bounds using matplotlib.pyplot.
	@param heatmap: A pixel matrix heatmap.
	@type heatmap: Rectangular numpy matrix of floats
	@param bounds: The bounding coordinates of the points to generate, in the form [left, right, bottom, top].
	@type bounds: List of 4 ints
	@rtype: Void
	'''
	import numpy as np
	import matplotlib.pyplot as plt
	
	print "Displaying heat map..."
	plt.xlim(bounds[0], bounds[1])
	plt.ylim(bounds[2], bounds[3])
	plt.imshow(heatmap, cmap='hot', origin='lower', extent=bounds)
	plt.show()
	print "Done."

def show_3D_heatmap(heatmap):
	'''
	Displays a heatmap in 3D using MayaVi.
	@param heatmap: A pixel matrix heatmap.
	@type heatmap: Rectangular numpy matrix of floats
	@rtype: Void
	'''
	print "Loading 3D modules..."
	import numpy as np
	from mayavi import mlab
	print "Done."
	print "Displaying 3D heatmap..."
	rescale = heatmap * 255. / heatmap.max()
	rescale = rescale[::-1]
	mlab.surf(rescale, colormap='hot', vmin=0, vmax=255)
	mlab.show()
	print "Done."

def save_heatmap(heatmap, path, colour):
	'''
	Saves a heatmap to the specified path, in colour if colour is True, or in greyscale if colour is False.
	@param heatmap: A pixel matrix heatmap.
	@type heatmap: Rectangular numpy matrix of floats
	@param path: The file path to save the file into.
	@type path: String
	@param colour: Whether or not the heatmap should be saved in colour.
	@type colour: Boolean
	@rtype: Void
	'''
	heatmap = heatmap[::-1]
	if colour:
		import numpy as np
		from scipy import misc
		from matplotlib.pyplot import cm
		
		print "Saving colour heatmap to "+path+"..."
	
		cmap = cm.ScalarMappable()
		cmap.set_cmap('hot')
		cmap.set_clim(0, heatmap.max())
		heatmap_color = []
		
		for r in xrange(len(heatmap)):
			heatmap_color.append([])
			for c in xrange(len(heatmap[r])):
				heatmap_color[r].append(cmap.to_rgba(heatmap[r][c]))
			
		misc.imsave(path, heatmap_color)
		print "Done."
	else:
		print "Saving greyscale heatmap to "+path+"..."
		misc.imsave(path, heatmap)
		print "Done."

def heat_dist(point, x, y):
	'''
	Returns the Euclidean distance between a point and a pixel on an image.
	@param point: The point's coordinates.
	@type point: 2-tuple of floats.
	@param x: The x-coordinate of the pixel.
	@type x: Integer
	@param y: The y-coordinate of the pixel.
	@type y: Integer
	@return: The Euclidean distance between the point and the pixel.
	@rtype: Float
	'''
	from math import sqrt
	return sqrt((point[0]-x)**2+(point[1]-y)**2)

def gauss(var, x):
	'''
	Returns the y value at x for a normal distribution with variance var in the form f(x) = e^(-(x^2)/(2s^2)) where s is the spread. Note: the center of the curve is 0 since no mean is defined, and the maximum value is always 1.
	@param var: The variance to use for this curve.
	@type var: Float
	@param x: The distance from the point.
	@type x: Float
	@return: The value of the given curve at x.
	@rtype: Float
	'''
	from math import e
	return e ** (-(x*x)/(2*var))

def plot_gauss(var, lim):
	'''
	Plots a Gaussian distribution.
	@param var: Variance of the curve.
	@type var: Float
	@param lim: Upper limit of plot (lower is 0).
	@type lim: Float
	@rtype: Void
	'''
	coords = []
	for i in range(lim):
		for j in range(10):
			num = i+j/10.
			print num, gauss(var, num)
			coords.append((num, gauss(var, num)))
	plot(coords)

def heatmap_tile(level, x, y, coords):
	'''
	Creates a 256x256 heatmap tile for the specified zoom level and location for the given coordinates. Variance is adjusted according to level.
	@param level: The zoom level of the tile, between 0 and 21.
	@type level: int
	@param x: The X coordinate of the tile.
	@type x: int
	@param y: The Y coordinate of the tile.
	@type y: int
	@param coords: The X, Y coordinates of points.
	@type coords: List of 2-tuples of floats
	@return: A pixel matrix heatmap for the given points.
	@rtype: Rectangular numpy matrix of floats
	'''
	import numpy as np
	from math import sqrt
	
	n = len(coords)
	print n, "points provided."
	
	heatmap = np.array([[0.]*256]*256)
	
	var = 1 / (2**level)
	print "Zoom level of "+str(level)+" gives a variance estimate of "+str(var)+"."
	
	lim = 3 * sqrt(var) # limit of meaningful influence is 3 standard deviations.
	print "Limit of meaningful influence is "+str(lim)+" from the tile."
	
#	dim = 
	
	# All point coordinates need to be rescaled to the zoom level (divide by 2^level), then filtered to eleminate all points further than 3 standard deviations away from the boundaries of the bounds of the tile.
	for point in coords:
		point = [point[0]/2**level, point[1]/2**level]
#		if 
	
	
#	for point in coords:
#		print "Processing:",str(point)
#		for i in xrange(256):
#			for j in xrange(256):
#				heatmap[i][j] += gauss(var,
#				heat_dist(point,j+bounds[0]+.5,i+bounds[2]+.5))
				# the +.5 is to account for pixel center
	
	return heatmap

if __name__ == "__main__":
#	plot_random(20, 100)
#	plot_gauss(1, 3)
#	coords = [[20,50],[25,65],[30,75],[35,90],[50,50],[65,10],[80,50]]
	bounds = [-50,50,-50,50]
	coords = random_coords(10, bounds)
	heatmap = heatmap(bounds, coords)
	save_heatmap(heatmap)
	show_heatmap(heatmap, bounds)
#	show_3D_heatmap(heatmap)


