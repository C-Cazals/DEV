#!/usr/bin/python
# -*- coding: utf-8

from PIL import Image
from osgeo import gdal
from osgeo.gdalconst import *
import DegradationResolutionFuctions as DRF

def ImagePrint(img):
   img = Image.fromarray(img)
   img.show()


def WriteImage(img, inDs, filename):
   [width, length]=img.shape
   # Create a new raster data source
   driver = inDs.GetDriver()
   outDs = driver.Create(filename, length, width, 2, gdal.GDT_UInt16)

   # Write metadata
   outDs.SetGeoTransform(inDs.GetGeoTransform())
   outDs.SetProjection(inDs.GetProjection())

   # Write raster data sets
   outBand = outDs.GetRasterBand(1)
   outBand.WriteArray(img)

   # Close raster file
   outDs = None


def WriteComplexImage(img, inDs, filename):
   [width, length]=img.shape
   # Create a new raster data source
   driver = inDs.GetDriver()
   outDs = driver.Create(filename, length, width, 2, gdal.GDT_UInt16)

   # Write metadata
   outDs.SetGeoTransform(inDs.GetGeoTransform())
   outDs.SetProjection(inDs.GetProjection())

   [intensite, phase] = DRF.UnMakeComplexImage(img)

   # print(intensite)
   # print(phase)
   # exit()
   # Write raster data sets
   outBand = outDs.GetRasterBand(1)

   outBand.WriteArray(intensite)

   # Write raster data sets
   outBand = outDs.GetRasterBand(2)
   outBand.WriteArray(phase)

   # Close raster file
   outDs = None