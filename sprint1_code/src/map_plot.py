import numpy as np
import matplotlib.pyplot as plt
from random import random as r
import math

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

def plot_random(num, range):
	'''Plots num random points with coordinates in the range [0,range)'''
	points = random_coords(num, range)
	plot(points)

def random_coords(num, range):
	'''Returns num random points with coordinates in the range [0,range).'''
	points = []
	for i in xrange(num):
		points.append(((r()*range,r()*range)))
	return points

def heatmap(coords):
	x_coords = []
	y_coords = []
	for point in coords:
		x_coords.append(point[0])
		y_coords.append(point[1])
		print "processing: ("+str(point[0])+", "+str(point[1])+")"
	
	heatmap = [[]]
	xdim = (int(max(x_coords))+1-int(min(x_coords))) * 10
	ydim = (int(max(y_coords))+1-int(min(y_coords))) * 10
	for i in xrange(ydim):
		heatmap[i] = [0.0]*xdim
		heatmap.append([])
	heatmap[ydim] = [0.0]*xdim
#	print heatmap
	
	for point in coords:
		for i in xrange(ydim):
			for j in xrange(xdim):
				heatmap[j][i] += gauss(1, dist(point,i,j))
	
	
	
	plt.xlim(int(min(x_coords)),int(max(x_coords))+1)
	plt.ylim(int(min(y_coords)),int(max(y_coords))+1)
#	plt.xlim(0,xdim)
#	plt.ylim(0,ydim)
	plt.imshow(heatmap)
	plt.scatter(x_coords, y_coords)
	plt.show()

def dist(point, x, y):
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
	coords = random_coords(10, 10)
#	plot_random(20, 100)
#	heatmap([(0.25,0.25),(0.5,0.5),(0.75,0.75)])
#	plot_gauss(1, 3)
	heatmap(coords)















