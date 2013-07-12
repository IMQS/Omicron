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

A general-purpose plotter for heatmaps in any of the following coordinate systems:
    > Geographic
    > Projected
    > Pixel

CAVEAT: the random point generator makes tuples which matplotlib can interpret as (X, Y) which
    makes sense on a Euclidean plane or projected system, but LAT/LON is in the reverse order!!!
    Therefore, specify bounds as follows:
        > [min_x, max_x, min_y, max_y] (l,r,b,t) when working in (X, Y)
        > [min_lat, max_lat, min_lon, max_lon] (s,n,w,e) when working in LAT/LON

CAVEAT: An exported tile is scaled between zero and the maximum of the tile. This will
    result in a patchy appearance unless some function is found to determine a scale that
    will work for the entire tileset.
'''

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
    
    tileTop = 256 * y
    tileLeft = 256 * x    
    
    if len(coords) == 0:
        print "No points provided. Returned blank."
        return np.array([[0.] * 256] * 256)
    
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
        return np.array([[0.] * 256] * 256)
    
    print "\t\tLAT/LON points:"
    print "\t\t"+str(coords)
    print "\t\tProjected points:"
    print "\t\t"+str(coords_proj)
    print "\t\tPyramid points:"
    print "\t\t"+str(coords_pyra)
    print "\t\tTile points:"
    print "\t\t"+str(coords_tile)
    
    print "\tStarting raster generation..."
    s = time()
    heatmap = np.array([[0.] * 512] * 512)
    from scipy import ndimage
    for point_tile in coords_tile:
        heatmap[point_tile[1]+128,point_tile[0]+128] += 1000.
    heatmap = ndimage.gaussian_filter(heatmap, sigma=15)
    heatmap = heatmap[128:384,128:384]
    
    e = time()
    print "\tDone."
    print "\tTime: " + str(e - s)
    print "\tAverage time per point: " + str((e - s) / n)
    print "Returning tile."
    return heatmap

def show_heatmap(heatmap):
    '''
    Displays a heatmap using matplotlib.pyplot.
    @param heatmap: A pixel matrix heatmap.
    @type heatmap: Rectangular numpy matrix of floats
    @rtype: Void2
    '''
    import matplotlib.pyplot as plt
    
    print "Displaying heat map..."
    plt.xlim(0, 256)
    plt.ylim(0, 256)
    plt.imshow(heatmap, cmap='hot', origin='lower', extent=[0,256,0,256])
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

def coords_to_geojson(coords):
    '''
    Converts a set of coordinate pairs to a GeoJSON object.
    @param coords: An array of coordinate pairs.
    @type coords: Array of 2-tuples or length-2 arrays.
    @rtype: GeoJSON object
    '''
    import json
    obj = {u'type':u'FeatureCollection', u'features':{u'type':u'Feature', u'geometry':[]}}
    for point in coords:
        obj[u'features'][u'geometry'].append({u'type':u'Point',u'coordinates':[str(point[0]),str(point[1])]})
    return json.dumps(obj)

if __name__ == "__main__":
    
    from time import time
    s = time()
    
    bounds_geo = [-85, 85, -180, 180]
    
    ten_random = random_coords(10, bounds_geo)
    #smiley = [[25,45], [25,35], [35,25], [45,15], [55,15], [65,25], [75,35], [75,45], [35,75], [35,65], [65,65], [75,65]]
    #stellenbosch = [[-33.9200, 18.8600]]
    #center = [[0,0]]
    #square = [[45,45],[-45,45],[45,-45],[-45,-45]]
    #technopark = [[-33.964807, 18.8372767]]
    #madagascar = [[-20,47]]
    
    #tile = heatmap_tile(level = 2, x = 1, y = 2, coords=stellenbosch*5)
    #show_heatmap(tile)
    #show_3D_heatmap(tile)
    #save_heatmap(tile, path="/home/marzul/test.png", colour=True)
    print coords_to_geojson(ten_random)
    e = time()
    print "total time: "+str(e-s)

