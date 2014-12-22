#!/usr/bin/python
# -*- coding: utf-8

import sys

import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
from osgeo.gdalconst import *
from PIL import Image

def square(mat):
  squareMat=np.zeros((mat.shape))
  for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
      squareMat[i,j]=mat[i,j]**2
  return squareMat

def horizontalFlip(mat):
	[width, length]=mat.shape
	mat2=np.zeros((mat.shape))
	for i in range(width):
		idx=width-i-1
		mat2[idx,:]=mat[i,:]
	return mat2

if (len(sys.argv) != 2) :
	print("Usage : Reader imageIn.tif ")
	exit()
else:
	imageIn=sys.argv[1]


print('Reading file '+imageIn+'...')
inDs = gdal.Open(imageIn)
imageComplete=[]


for bi in [0,1]:
    band = inDs.GetRasterBand(bi + 1)
    # Read this band into a 2D NumPy array
    imageComplete.append(band.ReadAsArray())
    print('Band %d has type %s'%(bi + 1, imageComplete[bi].dtype))
    # raw = imageComplete[bi].tostring()


# image2=imageComplete[1][1000:1600,1000:1600]
# image1=imageComplete[0][1000:1600,1000:1600]
# image1=imageComplete[0][:,:]
# image2=imageComplete[0][:,:]
print('Image size : ' + str(imageComplete[0].shape))

image1=imageComplete[0][-2700:-2100,0:1000]
image2=imageComplete[1][-2700:-2100,0:1000]

print('Computing amplitude... ')

imgAmplitude =(np.sqrt(square(image1)+square(image2)))


[width, length]=imgAmplitude.shape
# imgFlip=horizontalFlip(imgAmplitude)
img = Image.fromarray(imgAmplitude/2)
img.show()