#!/usr/bin/python
# -*- coding: utf-8

import sys

import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
from osgeo.gdalconst import *
import DegradationResolutionFuctions as DRF
import DegradationResolutionPrints as DRP


if (len(sys.argv) != 6) :
	print("Usage : resample imageIn.tif imageOut.tif range_resolutionI range_resolutionF azimut_resolutionI azimut_resolutionF")
	exit()
else:
	imageIn=sys.argv[1]
	rangeRes1=float(sys.argv[2])
	rangeRes2=float(sys.argv[3])
	azimutRes1=float(sys.argv[4])
	azimutRes2=float(sys.argv[5])

imageOut=imageIn.split('.', 1 )[0]+'_Res_'+str(rangeRes2)+'_'+str(azimutRes2)+'.tif'
rangeRatio=float(rangeRes1)/rangeRes2
azimutRatio=float(azimutRes1)/azimutRes2
print('Resampling range ratio : ' + str(rangeRatio))
print('Resampling azimut ratio : ' + str(azimutRatio))

print('Reading file '+imageIn+'...')
inDs = gdal.Open(imageIn)
imageComplete=[]
for bi in range(inDs.RasterCount):
    band = inDs.GetRasterBand(bi + 1)
    # Read this band into a 2D NumPy array
    imageComplete.append(band.ReadAsArray())
    # print('Band %d has type %s'%(bi + 1, imageComplete[bi].dtype))
    raw = imageComplete[bi].tostring()


# image2=imageComplete[1][1000:1600,1000:1600]
# image1=imageComplete[0][1000:1600,1000:1600]
# image1=imageComplete[0][:,:]
# image2=1=imageComplete[0][:,:]
image1=imageComplete[0][-200:,-200:]
image2=imageComplete[1][-200:,-200:]

print('Computing amplitude... ')
imgAmplitude =(np.sqrt(DRF.square(image1)+DRF.square(image2)))
imgComplex = DRF.MakeComplexImage(image1, image2)

[width, length]=imgAmplitude.shape

DRP.ImagePrint(imgAmplitude/2)
DRP.WriteImage(imgAmplitude, inDs, imageIn.split('.', 1 )[0]+'_Res_'+str(rangeRes1)+'_'+str(azimutRes1)+'.tif')


imgTF=(np.fft.fftshift(np.fft.fft2(imgComplex)))

imgColResampled=np.zeros((imgTF.shape), dtype=complex)



print("Degrading Lines...")
MeanLineSpectra=DRF.ComputeMeanLineSpectra(imgTF)
imgLineDegraded = DRF.CutLineSpectra(imgTF, MeanLineSpectra, rangeRatio)


print("Degrading columns...")
MeanColumnSpectra=DRF.ComputeMeanColumnSpectra(imgLineDegraded)
imgColumnDegraded = DRF.CutColumnSpectra(imgLineDegraded, MeanColumnSpectra, azimutRatio)



imgInvTF=((np.fft.ifft2(np.fft.fftshift(imgColumnDegraded))))
# imgInvTF=((np.fft.ifft2(np.fft.fftshift(imgColumnDegraded))))
print((imgInvTF))

imgInvTFAmplitude=(np.sqrt(DRF.square(imgInvTF.real)+DRF.square(imgInvTF.imag)))
DRP.ImagePrint(imgInvTFAmplitude/2)
print('Writing file '+imageOut+'...')
DRP.WriteComplexImage(imgInvTF, inDs, imageOut)
# # Create a new raster data source
# driver = inDs.GetDriver(imgInvTF)
# outDs = driver.Create('test.tif', length, width, 1, gdal.GDT_UInt16)

# # Write metadata
# outDs.SetGeoTransform(inDs.GetGeoTransform())
# outDs.SetProjection(inDs.GetProjection())

# # Write raster data sets
# outBand = outDs.GetRasterBand(1)
# outBand.WriteArray(imgInvTF)

# # Close raster file
# outDs = None
