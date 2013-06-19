def plot(coords):
	'''Makes a simple scatter plot of given coordinates within a box that in X and Y spans the floor and ceiling integers of the minima and maxima respectively.
	@param coords A list of pairs (2-tuples) of floats which represent X/Y coordinates of points.
	'''
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
	'''Plots random points.
	@param num The number of points to generate.
	@param bounds The bounding coordinates of the points to generate, in the form [left, right, bottom, top].
	'''
	from random import random as r
	points = random_coords(num, bounds)
	plot(points)

def random_coords(num, bounds):
	'''Returns random points.
	@param num The number of points to generate.
	@param bounds The bounding coordinates of the points to generate, in the form [left, right, bottom, top].
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

def heatmap(n, bounds, coords):
	'''Creates a heatmap for the given coordinates or random points. Variance is adjusted according to point density..
	@param n Number of points. Only matters when random points are being calculated since it is recalculated if coordinates are provided.
	@param bounds A list of 4 floats that denote the left, right, bottom, and top limits of the extent respectively.
	@param coords List of 2-tuples of floats that represent point coordinates. If None, n random points are generated within bounds.
	'''
	import numpy as np
	from scipy import misc
	import matplotlib.pyplot as plt
	
	if coords == None:
		coords = random_coords(n, bounds)
		print n, "random points generated."
	else:
		n = len(coords)
		print n, "points provided."
	
	rdim = bounds[1] - bounds[0]
	cdim = bounds[3] - bounds[2]

	heatmap = np.array([[0.]*rdim]*cdim)
	
	print "For bounds "+str(bounds)+", extent is "+str(rdim)+" by "+str(cdim)+"."
	
	p_dens = float(n)/(rdim*cdim)
	var = 1 / (32*p_dens)
	print "Point density of "+str(p_dens)+" gives a variance of "+str(var)+"."
	
	for point in coords:
		print "Processing:",str(point)
		for i in xrange(cdim):
			for j in xrange(rdim):
				heatmap[i][j] += gauss(var,
				heat_dist(point,j+bounds[0]+.5,i+bounds[2]+.5))
				# the +.5 is to account for pixel center
		
	plt.xlim(bounds[0], bounds[1])
	plt.ylim(bounds[2], bounds[3])
	
	plt.imshow(heatmap, cmap='hot', origin='lower', extent=bounds)

	x_coords = []
	y_coords = []
	for point in coords:
		x_coords.append(point[0])
		y_coords.append(point[1])
	plt.scatter(x_coords, y_coords)
	
	print "Saving to disk..."
	rescale = heatmap * 255. / heatmap.max()
	rescale = rescale[::-1]
	misc.imsave('test.png', rescale)
	print "Done."

	print "Displaying heat map..."
	plt.show()
	print "Done."
	
def heat_dist(point, x, y):
	'''Returns the Euclidean distance between a point and a pixel on an image.
	@param point The 2-tuple of the point's coordinates.
	@param x The x-coordinate of the pixel.
	@param y The y-coordinate of the pixel.
	'''
	from math import sqrt
	return sqrt((point[0]-x)**2+(point[1]-y)**2)

def gauss(var, x):
	'''Returns the y value at x for a normal distribution with variance var in the form f(x) = e^(-(x^2)/(2s^2)) where s is the spread. Note: the center of the curve is 0 since no mean is defined, and the maximum value is always 1.
	@param var The variance to use for this curve.
	@param x The distance from the point.
	'''
	from math import e
	return e ** (-(x*x)/(2*var))

def plot_gauss(var, lim):
	'''Plots a Gaussian distribution.
	@param var Variance of the curve.
	@param lim Upper limit of plot (lower is 0).'''
	coords = []
	for i in range(lim):
		for j in range(10):
			num = i+j/10.
			print num, gauss(var, num)
			coords.append((num, gauss(var, num)))
	plot(coords)

if __name__ == "__main__":
#	plot_random(20, 100)
#	heatmap([(0.25,0.25),(0.5,0.5),(0.75,0.75)])
#	plot_gauss(1, 3)
#	coords = [[20,50],[25,65],[30,75],[35,90],[50,50],[65,10],[80,50]]
	bounds = [-150,50,-50,100]
	heatmap(10, bounds, None)

