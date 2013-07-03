'''
Created on 18 June 2013

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
    # the +.5 is to account for pixel center

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
    '''
    coords = []
    for i in range(lim):
        for j in range(10):
            num = i + j / 10.
            print num, gauss(var, num)
            coords.append((num, gauss(var, num)))
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

def heatmap_tile(level=0, x=0, y=0, coords=[]):# the +.5 is to account for pixel center
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
    
    #raise NotImplementedError("Method not finished, please do not use yet.")
    
    import numpy as np
    from time import time
    import globalmaptiles as gmt
    
    world = gmt.GlobalMercator()
    bounds = world.TileBounds(x, y, level) # ( minx, miny, maxx, maxy )
    
    var = 362
    three_stdev = 57 # int(3 * sqrt(var))
    
    if len(coords) == 0:
        print "No points provided. Returned None."
        return None
    print len(coords), "points provided."
    coords_pix = []
    for point in coords:
        point_proj = world.LatLonToMeters(point[0],point[1])
        point_pix = world.MetersToPixels(point_proj[0], point_proj[1], level)
        if (bounds[0]-three_stdev < point_pix[0] < bounds[2]+three_stdev) & (bounds[1]-three_stdev < point_pix[1] < bounds[3]+three_stdev):
            coords_pix.append(point_pix)
    n = len(coords)
    print "Trimmed to "+str(n)+" points."
    if n == 0:
        print "No points close enough to tile. Returned None."
        return None
    
    print "Creating Gauss curve..."
    g = []
    for i in xrange(three_stdev): 
        g.append(gauss(var, float(i)))
    while len(g) <= 362:  # int(sqrt(256*256*2)) = 362 # diagonal length of tile
        g.append(0)
    print "Done."
    
    print "Starting raster generation..."
    heatmap = np.array([[0.] * 256] * 256)
    s = time()
    for i in xrange(256):
        for j in xrange(256):
            for point_pix in coords_pix:
                # Convert all points: GPS > Projected > pixel
                heatmap[i][j] += g[int(heat_dist(point_pix, j, i))]
                # gauss(var, heat_dist(point,j+bounds[0]+.5,i+bounds[2]+.5))
                # the +.5 is to account for pixel center
    e = time()
    print "Done."
    print "Time: " + str(e - s)
    print "Average time per point: " + str((e - s) / n)
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
    heatmap = heatmap[::-1]
    if colour:
        from matplotlib.pyplot import cm
        
        print "Saving colour heatmap to " + path + "..."
    
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
        print "Saving greyscale heatmap to " + path + "..."
        misc.imsave(path, heatmap)
        print "Done."

if __name__ == "__main__":
#     coords = [[20,50],[25,65],[30,75],[35,90],[50,50],[65,10],[80,50]] # Smiley face on [0-100) Euclidean square
    
    # XXX CAUTION! the random point generator makes tuples which matplotlib can interpret as (X, Y)
    # which makes sense on a Euclidean plane, but LAT/LON is in the reverse order!!!
    # Therefore, specify bounds as follows:
    #    > [minx, maxx, miny, maxy] when working in X, Y
    #    > [miny, maxy, minx, maxx] when working in LAT/LON
    
    bounds_lim = [-85, 85, -180, 180]
    bounds_disp = [0, 256, 0, 256]
    coords = random_coords(10, bounds_lim)
#    heatmap = heatmap(bounds, coords)
    tile = heatmap_tile(0,0,0,coords)
#     save_heatmap(heatmap)
#     save_heatmap(heatmap, colour=True)
    show_heatmap(tile, bounds_disp)
#    save_heatmap(tile, colour = True, path = "./special.png")
#     show_3D_heatmap(heatmap)


