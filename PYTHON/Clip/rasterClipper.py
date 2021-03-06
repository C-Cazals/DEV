#!/usr/bin/python 
# -*- coding: utf-8 -*-

import math
from pylab import *
from osgeo import gdal, gdalnumeric, ogr, osr
import Image, ImageDraw
import os, sys
gdal.UseExceptions()
import matplotlib.pyplot as plt

# This function will convert the rasterized clipper shapefile
# to a mask for use within GDAL.
def imageToArray(i):
    """
    Converts a Python Imaging Library array to a
    gdalnumeric image.
    """
    a=gdalnumeric.fromstring(i.tostring(),'b')
    a.shape=i.im.size[1], i.im.size[0]
    return a

def arrayToImage(a):
    """Fcli
    Converts a gdalnumeric array to a
    Python Imaging Library Image.
    """
    i=Image.fromstring('L',(a.shape[1],a.shape[0]),
            (a.astype('b')).tostring())
    return i

def world2Pixel(geoMatrix, x, y):
  """
  Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
  the pixel location of a geospatial coordinate
  """
  ulX = geoMatrix[0]
  ulY = geoMatrix[3]
  xDist = geoMatrix[1]
  yDist = geoMatrix[5]
  rtnX = geoMatrix[2]
  rtnY = geoMatrix[4]
  pixel = int((x - ulX) / xDist)
  line = int((ulY - y) / xDist)
  return (pixel, line)

#
#  EDIT: this is basically an overloaded
#  version of the gdal_array.OpenArray passing in xoff, yoff explicitly
#  so we can pass these params off to CopyDatasetInfo
#
def OpenArray( array, prototype_ds = None, xoff=0, yoff=0 ):
    ds = gdal.Open( gdalnumeric.GetArrayFilename(array) )

    if ds is not None and prototype_ds is not None:
        if type(prototype_ds).__name__ == 'str':
            prototype_ds = gdal.Open( prototype_ds )
        if prototype_ds is not None:
            gdalnumeric.CopyDatasetInfo( prototype_ds, ds, xoff=xoff, yoff=yoff )
    return ds

def histogram(a, bins=range(0,256)):
  """
  Histogram function for multi-dimensional array.
  a = array
  bins = range of numbers to match
  """
  fa = a.flat
  n = gdalnumeric.searchsorted(gdalnumeric.sort(fa), bins)
  n = gdalnumeric.concatenate([n, [len(fa)]])
  hist = n[1:]-n[:-1]
  return hist

def stretch(a):
  """
  Performs a histogram stretch on a gdalnumeric array image.
  """
  hist = histogram(a)
  im = arrayToImage(a)
  lut = []
  for b in range(0, len(hist), 256):
    # step size
    step = reduce(operator.add, hist[b:b+256]) / 255
    # create equalization lookup table
    n = 0
    for i in range(256):
      lut.append(n / step)
      n = n + hist[i+b]
  im = im.point(lut)
  return imageToArray(im)


def boxPlot(histo):

  bilan=(histo)
  boxplot(bilan,0,vert=0,sym="o")
  xlim(-1, 10000)
 
  yticks([])
  xlabel(u'frÃ©quences')

  title(u'Bilan de la simulation')
  text(0.38,6.5,u'Ã©chantillons de')


  savefig('boite.png')
  show()

def main( shapefile_path, raster_path ):
    # Load the source data as a gdalnumeric array
    srcArray = gdalnumeric.LoadFile(raster_path)
    npsrcArray=np.array(srcArray)
    
    # Also load as a gdal image to get geotransform
    # (world file) info
    inDs = gdal.Open(raster_path)

    geoTrans = inDs.GetGeoTransform()
    dataType = gdal.GetDataTypeName(inDs.GetRasterBand(1).DataType)
    imageComplete=[]
    for bi in range(inDs.RasterCount):
        band = inDs.GetRasterBand(bi + 1)
        # Read this band into a 2D NumPy array
        imageComplete.append(band.ReadAsArray())
        print('Importing band ', bi)
    # Create an OGR layer from a boundary shapefile
    shapef = ogr.Open(shapefile_path)
    lyr = shapef.GetLayer( os.path.split( os.path.splitext( shapefile_path )[0] )[1] )

    poly = lyr.GetNextFeature()
    poly2=lyr.GetNextFeature()
    minX, maxX, minY, maxY = lyr.GetExtent()
    print minX, maxX, minY, maxY

    # Convert the layer extent to image pixel coordinates
    minX, maxX, minY, maxY = lyr.GetExtent()
    ulX, ulY = world2Pixel(geoTrans, minX, maxY)
    lrX, lrY = world2Pixel(geoTrans, maxX, minY)

    # Calculate the pixel size of the new image
    pxWidth = int(lrX - ulX)
    pxHeight = int(lrY - ulY)
  
  
    clip = srcArray[ulY:lrY, ulX:lrX]

    #
    # EDIT: create pixel offset to pass to new image Projection info
    #
    xoffset =  ulX
    yoffset =  ulY
    print "Xoffset, Yoffset = ( %f, %f )" % ( xoffset, yoffset )

    # Create a new geomatrix for the image
    geoTrans = list(geoTrans)
    geoTrans[0] = minX
    geoTrans[3] = maxY

    # Map points to pixels for drawing the
    # boundary on a blank 8-bit,
    # black and white, mask image.
    points = []
    pixels = []
    geom = poly.GetGeometryRef()
    pts = geom.GetGeometryRef(0)
    for p in range(pts.GetPointCount()):
      points.append((pts.GetX(p), pts.GetY(p)))
    for p in points:
      pixels.append(world2Pixel(geoTrans, p[0], p[1]))
    rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)
    rasterize = ImageDraw.Draw(rasterPoly)
    rasterize.polygon(pixels, 0)
    mask = imageToArray(rasterPoly)

    # Clip the image using the mask
    clip = gdalnumeric.choose(mask, \
        (clip, 0)).astype(dataType)

    histo = histogram(clip)
    values = clip.ravel()
    va=[]
    for i in range(len(values)):
      if values[i]!=0 :
        va.append(10*(log10(values[i])))

    boxplot(va,0,)
    show()
 
    # This image has 3 bands so we stretch each one to make them
    # visually brighter
   
    # for i in range(3):
    #   clip[i,:,:] = stretch(clip[i,:,:])

    # Save new tiff
    #
    #  EDIT: instead of SaveArray, let's break all the
    #  SaveArray steps out more explicity so
    #  we can overwrite the offset of the destination
    #  raster
    #
    ### the old way using SaveArray
    #
    # gdalnumeric.SaveArray(clip, "OUTPUT.tif", format="GTiff", prototype=raster_path)
    #
    ###
    #
    gtiffDriver = gdal.GetDriverByName( 'GTiff' )
    if gtiffDriver is None:
        raise ValueError("Can't find GeoTiff Driver")
    gtiffDriver.CreateCopy( "OUTPUT.tif",
        OpenArray( clip, prototype_ds=raster_path, xoff=xoffset, yoff=yoffset )
    )

    # Save as an 8-bit jpeg for an easy, quick preview
    clip = clip.astype(dataType)
    gdalnumeric.SaveArray(clip, "OUTPUT.jpg", format="GTiff")




    gdal.ErrorReset()


if __name__ == '__main__':

    #
    # example run : $ python clip.py /<full-path>/<shapefile-name>.shp /<full-path>/<raster-name>.tif
    #
    if len( sys.argv ) < 2:
        print "[ ERROR ] you must two args. 1) the full shapefile path and 2) the full raster path"
        sys.exit( 1 )

    main( sys.argv[1], sys.argv[2] )

