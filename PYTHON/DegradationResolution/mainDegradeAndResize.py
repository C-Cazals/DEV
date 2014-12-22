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
	print("Usage : degrade imageIn.tif imageOut.tif range_resolutionI range_resolutionF azimut_resolutionI azimut_resolutionF")
	exit()
else:
	imageIn=sys.argv[1]
	rangeRes1=float(sys.argv[2])
	rangeRes2=float(sys.argv[3])
	azimutRes1=float(sys.argv[4])
	azimutRes2=float(sys.argv[5])

rangeSampling1=0.61
azimutSampling1=0.88

rangeSampling2=1.73
azimutSampling2=2.39

rangeSamplingRatio=rangeSampling1/rangeSampling2
azimutSamplingRatio=azimutSampling1/azimutSampling2

imageOut=imageIn.split('.', 1 )[0]+'_Res_'+str(rangeRes2)+'_'+str(azimutRes2)+'.tif'
rangeRatio=float(rangeRes1)/rangeRes2
azimutRatio=float(azimutRes1)/azimutRes2
print('Resolution range ratio : ' + str(rangeRatio))
print('Resolution azimut ratio : ' + str(azimutRatio))

print('Resampling range ratio : ' + str(rangeSamplingRatio))
print('Resampling azimut ratio : ' + str(azimutSamplingRatio))

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
image1=imageComplete[0][3000:4000,3700:5200]
image2=imageComplete[1][3000:4000,3700:5200]

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

rangeSamplingCut=length/2-length*rangeSamplingRatio/2
azimutSamplingCut=width/2- width*azimutSamplingRatio/2
print(rangeSamplingCut, azimutSamplingCut)
print(imgColumnDegraded.shape)
print()
if rangeSamplingRatio!=1 and azimutSamplingRatio!=1 :
	imgColumnDegradedCut=imgColumnDegraded[azimutSamplingCut:-azimutSamplingCut, rangeSamplingCut:-rangeSamplingCut]
else:
	if rangeSamplingRatio==1 :
		imgColumnDegradedCut=imgColumnDegraded[:, rangeSamplingCut:-rangeSamplingCut]
	if azimutSamplingRatio==1 :
		imgColumnDegradedCut=imgColumnDegraded[ azimutSamplingCut:-azimutSamplingCut, :]


# print(imgColumnDegradedCut.shape)
# DRP.ImagePrint(np.absolute(imgColumnDegradedCut))

imgInvTF=((np.fft.ifft2(np.fft.fftshift(imgColumnDegradedCut))))


imgInvTFAmplitude=(np.absolute(imgInvTF))
DRP.ImagePrint(imgInvTFAmplitude/2)

print('Writing file '+imageOut+'...')
# DRP.WriteComplexImage(imgInvTF, inDs, imageOut)
