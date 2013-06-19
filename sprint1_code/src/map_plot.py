import numpy as np
import matplotlib.pyplot as plt
from random import random as r
import math
import Image

def plot(coords):
	'''Takes a list of pairs (2-tuples) of floats which represent X/Y coordinates of points and makes a simple scatter plot of them within a box that in X and Y spans the floor and ceiling integers of the minima and maxima respectively.'''
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
	'''Plots num random points with coordinates in the range [0,range)'''
	points = random_coords(num, bounds)
	plot(points)

def random_coords(num, bounds):
	'''Returns num random points with coordinates within the bounds which are in the form [left, right, bottom, top]..'''
	points = []
	xdim = bounds[1] - bounds[0]
	ydim = bounds[3] - bounds[2]
	for i in xrange(num):
		x = r()*xdim + bounds[0]
		y = r()*ydim + bounds[2]
		points.append((x, y))
	return points

def heatmap(n, bounds, coords):
	'''Creates a heatmap for the given coordinates in coords or, if coords is None, n random points with coordinates within bounds. Variance is adjusted according to point density. If coordinates are specified, n is recalculated. The bounds are in the form [left, right, bottom, top].'''
	
	if coords == None:
		coords = random_coords(n, bounds)
	else:
		n = len(coords)
	
	x_coords = []
	y_coords = []
	for point in coords:
		x_coords.append(point[0])
		y_coords.append(point[1])
	
	heatmap = [[]]
	rdim = bounds[1] - bounds[0]
	cdim = bounds[3] - bounds[2]
	for i in xrange(cdim-1):
		heatmap[i] = [0.0]*rdim
		heatmap.append([])
	heatmap[cdim-1] = [0.0]*rdim
	
	var = 1 / ((32.*n)/(rdim*cdim))
	
	for point in coords:
		print "Processing: ("+str(point[0])+", "+str(point[1])+")"
		for i in xrange(cdim):
			for j in xrange(rdim):
				heatmap[i][j] += gauss(var,
				heat_dist(point,j+bounds[0]+.5,i+bounds[2]+.5))
				# the +.5 is to account for pixel center
		
	plt.xlim(bounds[0], bounds[1])
	plt.ylim(bounds[2], bounds[3])
	
	plt.imshow(heatmap, cmap='hot', origin='lower', extent=bounds)
	plt.scatter(x_coords, y_coords)
	plt.show()

def heat_dist(point, x, y):
	'''Returns the Euclidean distance between a point and a pixel on an image.'''
	return math.sqrt((point[0]-x)**2+(point[1]-y)**2)

def gauss(var, x):
	'''Returns the y value at x for a normal distribution with variance var in the form f(x) = e^(-(x^2)/(2s^2)) where s is the spread. Note: the center of the curve is 0 since no mean is defined, and the maximum value is always 1.'''
	#s = math.sqrt(var)
	return math.e ** (-(x*x)/(2*var))

def plot_gauss(var, lim):
	'''Test function. Plots a Gaussian distribution with a variance of var from 0 to lim with increments of 0.1.'''
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
	bounds = [-20,30,-10,25]
	heatmap(10, bounds, None)

