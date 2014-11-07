#!/usr/bin/python
# -*- coding: utf-8

import sys
from libtiff import TIFF
import numpy as np
from osgeo import gdal
from PIL import Image 
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
import scipy
import random
from matplotlib.mlab import PCA
import csv
from mpl_toolkits.mplot3d import Axes3D
from scipy import ndimage
import matplotlib
from numpy import linalg as LA
from scipy import ndimage

def toPolarCoordinates(Ipq, imNorm):
	CentralPoint=[Ipq.shape[0]/2,Ipq.shape[1]/2]
	r=[]
	a=[]
	sigma=ndimage.variance(imNorm)
	for i in range(int(np.around(Ipq.shape[0]/2*np.sqrt(2)))+1):
		r.append([0,0])
	for i in range(0,180,1):
		a.append([0,0])

	for i in range(Ipq.shape[0]):
		for j in range(Ipq.shape[1]/2+1):
			di=i-CentralPoint[0]
			dj=CentralPoint[1]-j
			
			dist=int(np.sqrt(di**2+dj**2))
			r[dist]=[r[dist][0]+1, r[dist][1]+Ipq[i,j]]
			if dj==0 :
				teta=0
			else :
				tmp=2*np.arctan(dj/(di+np.sqrt(di**2+dj**2)))
				teta=int(np.degrees(tmp))
			a[teta]=[a[teta][0]+1, a[teta][1]+Ipq[i,j]]

	radialSpectrum=[]
	angularSpectrum=[]
	for i in range(len(r)):
		if r[i][0]!=0 :
			radialSpectrum.append(r[i][1]/r[i][0])
		else:
			radialSpectrum.append(0)
	for i in range(len(a)):
		if a[i][0]!=0 :
			angularSpectrum.append(a[i][1]/a[i][0])
		else:
			angularSpectrum.append(0)
	return radialSpectrum/sigma**2, angularSpectrum/sigma**2


if (len(sys.argv) != 2) :
	print "Usage : ", sys.argv[0], "imageFile.tif"
	exit()




imageFile=sys.argv[1]

print("DEBUT")

ds = gdal.Open(imageFile)
image = np.array(ds.GetRasterBand(1).ReadAsArray())/100.0
imNorm = image-np.mean(np.mean(image))
[length, width]=imNorm.shape
print length, width

Ipq=length*width*(np.absolute(np.fft.fftshift(np.fft.fft2(imNorm)))**2)

[radialSpectrum, angularSpectrum]=toPolarCoordinates(Ipq, imNorm)


# im=Image.fromarray(Ipq
# im.show()
# exit()
# print "PLOT"

fig = plt.figure()
ax = fig.add_subplot(111)
# plt.xlim([0, 20])
# plt.ylim([0, 1000])
ax.plot(range(len(radialSpectrum)), (radialSpectrum))
plt.xlabel("r")
plt.ylabel("rSpectrum")

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
# plt.xlim([0, 20])
# # plt.ylim([0, 20])
# print len(angle)
# print angle
ax2.plot(range(len(angularSpectrum)), (angularSpectrum))
plt.xlabel("angle")
plt.ylabel("Angular Spectrum")
plt.show()
