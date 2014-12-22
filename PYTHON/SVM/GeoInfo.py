#!/usr/bin/python 

import numpy as np
import gdal
from gdalconst import *
from osgeo import osr

def CopyMetadata(imgSrc, imgDest, band):

  # Open the original file
  FileName = imgSrc    # This is the ISIS3 cube file
                                    # It's an infra-red photograph
                                    # taken by the 2001 Mars Odyssey orbiter.
  DataSet = gdal.Open(FileName, GA_ReadOnly)
  # Get the first (and only) band.
  Band = DataSet.GetRasterBand(1)
  # Open as an array.
  Array = Band.ReadAsArray()
  # Get the No Data Value
  NDV = Band.GetNoDataValue()
  # Convert No Data Points to nans
  Array[Array == NDV] = np.nan

  # Now I do some processing on Array, it's pretty complex 
  # but for this example I'll just add 20 to each pixel.
  NewArray = Array + 20  # If only it were that easy

  # Now I'm ready to save the new file, in the meantime I have 
  # closed the original, so I reopen it to get the projection
  # information...
  # Set up the GTiff driver
  Sourcesrc=gdal.Open(FileName, GA_ReadOnly)
  driver = gdal.GetDriverByName('GTiff')
  xsize = Sourcesrc.RasterXSize
  ysize = Sourcesrc.RasterYSize
  DataSet = driver.Create( imgDest, xsize, ysize, band, gdal.GDT_Byte)
      
              # the '1' is for band 1.
  DataSet.SetGeoTransform(Sourcesrc.GetGeoTransform())
  Projection = osr.SpatialReference()

  DataSet.SetProjection(Sourcesrc.GetProjectionRef())
  # Write the array
  #DataSet.GetRasterBand(1).WriteArray( Array )

  DataSet.GetRasterBand(1).SetNoDataValue(0)
  return DataSet
