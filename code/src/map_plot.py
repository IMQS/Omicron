'''
Created on 18 Jun 2013

@author: M. Arzul

     ____   ____    ___        _    ____    ___   _______
    |    \ |    \  / _ \      | |  /    |  / __\ |__   __|
    | ()_/ | () / | | | |  _  | | | _()_/ | /       | |
    | |    | |\ \ | |_| | | |_/ | | \__   | \___    | |
    |_|    |_| \_\ \___/   \___/   \____|  \___/    |_|
     ______   _____   _   ______   ____    ___    ___    _
    / __   / /     \ \ \ \   ___| |    \  / _ \  |   \  | |
   / /  / / / /| |\ \ \ \ \ \     | () / | | | | | |\ \ | |
  / /__/ / / / | | \ \ \ \ \ \___ | |\ \ | |_| | | | \ \| |
 /______/ /_/  |_|  \_\ \_\ \___/ |_| \_\ \___/  |_|  \___|

A general-purpose plotter for scatter plots and heatmaps in any of the following coordinate systems:
    > Geographic
    > Projected
    > Pixel

CAVEAT: the random point generator makes tuples which matplotlib can interpret as (X, Y)
    which makes sense on a Euclidean plane, but LAT/LON is in the reverse order!!!
    Therefore, specify bounds as follows:
        > [min_x, max_x, min_y, max_y] when working in (X, Y)
        > [min_lat, max_lat, min_lon, max_lon] when working in LAT/LON

CAVEAT: An exported tile is scaled between zero and the maximum of the tile. This will
    result in a patchy appearance unless some function is found to determine a scale that
    will work for the entire tileset.
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
        print "plotting: (" + str(point[0]) + ", " + str(point[1]) + ")"
    plt.xlim(int(min(x_coords)), int(max(x_coords)) + 1)
    plt.ylim(int(min(y_coords)), int(max(y_coords)) + 1)
    plt.scatter(x_coords, y_coords,)
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
    for _ in xrange(num):
        x = r() * xdim + bounds[0]
        y = r() * ydim + bounds[2]
        points.append((x, y))
    return points

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
    return sqrt((point[0] - x-.5) ** 2 + (point[1] - y-.5) ** 2)
    # the -.5 is to account for pixel center

def gauss(var, x):
    '''
    Returns the y value at x for a normal distribution with variance var in the form f(x) = e^(-(x^2)/(2s^2)) where s is the spread. Note: the center of the curve is 0 since no mean is defined, and the maximum value is always 1.
    @param var: The variance to use for this curve.
    @type var: Float
    @param x: The distance from the point.
    @type x: Floatimport numpy as np
        
    @return: The value of the given curve at x.
    @rtype: Float
    '''
    from math import e
    return e ** (-(x * x) / (2 * var))

def plot_gauss(var, lim):
    '''
    Plots a Gaussian distribution.
    @param var: Variance of the curve.
    @type var: Float
    @param lim: Upper limit of plot (lower is 0).
    @type lim: Float
    @rtype: Void
     coords = []
    for i in xrange(lim):
        for j in xrange(10):
            num = i + j / 10.
            print num, gauss(var, num)
            coords.append((num, gauss(var, num)))
    plot(coords)
            
    '''
    
    g = [i+j/10. for i in range(lim) for j in range(10) ]
    coords = map(g, gauss(var, g))
   
    plot(coords)

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
    from time import time
    from math import sqrt
    
    rdim = bounds[1] - bounds[0]
    cdim = bounds[3] - bounds[2]
    
    if cdim * rdim == 0:
        print "AREA OF BOUNDS IS ZERO: NO HEATMAP RETURNED"
        return None
    
    n = len(coords)
    print n, "points provided."
    
    heatmap = np.array([[0.] * rdim] * cdim)
    
    print "For bounds " + str(bounds) + ", extent is " + str(rdim) + " by " + str(cdim) + " and area is " + str(rdim * cdim) + "."
    
    p_dens = float(n) / (rdim * cdim)
    var = 1 / (8 * p_dens)
    print "Point density of " + str(p_dens) + " gives a variance estimate of " + str(var) + "."
    
    three_stdev = int(3 * sqrt(var))
    print "Distance cutoff for influence is " + str(three_stdev) + "."
    
    g = []
    diag_dist = int(sqrt(cdim * cdim + rdim * rdim))
    for i in xrange(three_stdev):
        g.append(gauss(var, i))
    while len(g) <= diag_dist:
        g.append(0)
    
    print "Starting raster generation..."
    s = time()
    for i in xrange(cdim):
        for j in xrange(rdim):
            for point in coords:
                heatmap[i][j] += g[int(heat_dist(point, j + bounds[0], i + bounds[2]))]
                # gauss(var, heat_dist(point,j+bounds[0]+.5,i+bounds[2]+.5))
    e = time()
    print "Done."
    print "Time: " + str(e - s) + " which per point is an average of: " + str((e - s) / n)
    return heatmap

def heatmap_tile(level=0, x=0, y=0, coords=[]):
    '''
    Creates a 256x256 heatmap tile for the specified zoom level and location for the given coordinates. Variance is fixed according to tile size.
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
    from time import time
    import globalmaptiles as gmt
    
    print "Requesting tile ("+str(x)+", "+str(y)+") for level "+str(level)+"..."
    y = 2** level - y -1
    
    world = gmt.GlobalMercator()
    bounds = world.TileBounds(x, y, level) # ( minx, miny, maxx, maxy )
    
    limx = (bounds[2]-bounds[0]) / 4
    limy = (bounds[3]-bounds[1]) / 4
    
    print "\tBounds of tile: "+str(bounds)
    
    heatmap = np.array([[0.] * 256] * 256)
    
    tileTop = 256 * y
    tileLeft = 256 * x    
    
    if len(coords) == 0:
        print "No points provided. Returned blank."
        return heatmap
    print "\t"+str(len(coords)), "points provided."
    coords_proj = []
    coords_pyra = []
    coords_tile = []
    for point in coords:
        point_proj = world.LatLonToMeters(point[0],point[1])
        if (bounds[0]-limx <= point_proj[0] <= bounds[2]+limx) and (bounds[1]-limy <= point_proj[1] <= bounds[3]+limy):
            coords_proj.append(point_proj)
            point_pyra = world.MetersToPixels(point_proj[0], point_proj[1], level)
            coords_pyra.append(point_pyra)
            coords_tile.append((point_pyra[0]-tileLeft, point_pyra[1]-tileTop))
    n = len(coords_proj)
    print "\tTrimmed to "+str(n)+" points."
    if n == 0:
        print "No points close enough to tile. Returned blank."
        return heatmap
    print "\t\tLAT/LON points:"
    print "\t\t"+str(coords)
    print "\t\tProjected points:"
    print "\t\t"+str(coords_proj)
    print "\t\tPyramid points:"
    print "\t\t"+str(coords_pyra)
    print "\t\tTile points:"
    print "\t\t"+str(coords_tile)
    
    print "\tCreating Gauss curve..."
    g = []
    for i in xrange(57): # three_stdev = 57 # int(3 * sqrt(var)) hardcoded for efficiency
        g.append(gauss(362, float(i)))
    while len(g) <= 543:  # int(sqrt((256*1.5)**2)*2) = 543 # diagonal length of one and a half tiles
        g.append(0)
    print "\tDone."
    
    print "\tStarting raster generation..."
    s = time()
    for point_tile in coords_tile:
        heatmap[point_tile[1],point_tile[0]] += 1000.
    from scipy import ndimage
    heatmap = ndimage.gaussian_filter(heatmap, sigma=10)
    e = time()
    print "\tDone."
    print "\tTime: " + str(e - s)
    print "\tAverage time per point: " + str((e - s) / n)
    print "Returning tile."
    return heatmap

def show_heatmap(heatmap, bounds):
    '''
    Displays a heatmap within certain bounds using matplotlib.pyplot.
    @param heatmap: A pixel matrix heatmap.
    @type heatmap: Rectangular numpy matrix of floats
    @param bounds: The bounding coordinates of the points to generate, in the form [left, right, bottom, top].
    @type bounds: List of 4 ints
    @rtype: Void2
    '''
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
    from mayavi import mlab
    print "Done."
    print "Displaying 3D heatmap..."
    rescale = heatmap * 255. / heatmap.max()
    rescale = rescale[::-1]
    mlab.surf(rescale, colormap='hot', vmin=0, vmax=255)
    mlab.show()
    print "Done."

def save_heatmap(heatmap, path='./image.png', colour=False):
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
    from scipy import misc  
    import numpy as np  
    from time import time
    import Image
    heatmap = heatmap[::-1]
    if colour:
        from matplotlib.pyplot import cm
        
        print "Saving colour heatmap to " + path + "..."
        
        print "\tMapping to colour scale..."
        s = time()
        print "\t\tRescaling..."
        heatmap = heatmap / 5.
        print"\t\tDone."
        
        heatmap_color = Image.fromarray(np.uint8(cm.hot(heatmap, alpha=0.5, bytes=True)))
        e = time()
        
        print "\tTime to convert to colour: " + str(e - s)
        #for r in xrange(len(heatmap)):
        #    heatmap_color.append([])
        #    for c in xrange(len(heatmap[r])):
        #        heatmap_color[r].append(cmap.to_rgba(heatmap[r][c], alpha=0.5, bytes=True))
        #print "\tDone."
        misc.imsave(path, heatmap_color)
        #misc.imsave(path, heatmap)
        print "Done."
    else:
        print "Saving greyscale heatmap to " + path + "..."
        misc.imsave(path, heatmap)
        print "Done."

if __name__ == "__main__":
    
    from time import time
    s = time()
    # XXX CAUTION! the random point generator makes tuples which matplotlib can interpret as (X, Y)
    # which makes sense on a Euclidean plane, but LAT/LON is in the reverse order!!!
    # Therefore, specify bounds as follows:
    #    > [minx, maxx, miny, maxy] when working in X, Y
    #    > [miny, maxy, minx, maxx] when working in LAT/LON
    
    #sine = [[20,50],[25,65],[30,75],[35,90],[50,50],[65,10],[80,50]] # Sine curve on [0-100) Euclidean square
    #smiley = [[25,45], [25,35], [35,25], [45,15], [55,15], [65,25], [75,35], [75,45], [35,75], [35,65], [65,65], [75,65]]
    stellenbosch = [[-33.9200, 18.8600]]
    #center = [[0,0]]
    #square = [[45,45],[-45,45],[45,-45],[-45,-45]]
    #dummy = [[45,45],[-45,45],[0,-45],[0,-45],[0,-45]]
    #technopark = [[-33.964807, 18.8372767]]
    #madagascar = [[-20,47]]
    #south_pole = [[-85,30]]
    #north_pole = [[85,30]]
    
    bounds_lim = [-85, 85, -180, 180]
    bounds_disp = [0, 256, 0, 256]
    #coords = random_coords(10, bounds_lim)
    #heatmap = heatmap(bounds, coords)
    tile = heatmap_tile(level = 0, x = 0, y = 0, coords=stellenbosch*2)
    #save_heatmap(tile, colour = True, path = "./special.png")
    #show_heatmap(tile, bounds_disp)
    save_heatmap(tile, path="/home/marzul/0_0_0.png", colour=True)
    #save_heatmap(tile, path="./yes.png", colour=True)
    #show_3D_heatmap(heatmap)
    e = time()
    print "total time: "+str(e-s)

