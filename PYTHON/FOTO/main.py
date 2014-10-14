#!/usr/bin/python
# -*- coding: utf-8

import sys
from libtiff import TIFF
import numpy as np
from osgeo import gdal
from PIL import Image 
import matplotlib.pyplot as plt

if (len(sys.argv) != 4) :
	print "Usage : ", sys.argv[0], "imageFile.tif", "taille de fenêtre"
	exit()
imageFile=sys.argv[1]
windowSizeMin=int(sys.argv[2])
windowSizeMax=int(sys.argv[3])
windowSizeStep=20
moduleAccuracy=0
print("DEBUT")

ds = gdal.Open(imageFile)
image = np.array(ds.GetRasterBand(1).ReadAsArray())

fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlim([0, 150])
plt.ylim([0, 10])
plt.xlabel("Valeurs des modules de la FFT")
plt.ylabel("Representation des modules en pourcentage du nombre total des pixels")
plt.figure()

[length, width]=image.shape

windowSize=windowSizeMin
while windowSize<=windowSizeMax :
	print "windowSize = ",  windowSize
	imagette=[]
	imagetteFFT=[]
	values=[]
	for l in xrange(0,length/windowSize,windowSize):
		for w in xrange(0,length/windowSize,windowSize):
			mat = image[l:(l+windowSize),w:(w+windowSize)]
			imagette.append(mat)
			matFFT=np.around(np.absolute(np.fft.fft2(mat)), decimals=moduleAccuracy)
			imagetteFFT.append(matFFT)
			for i in range(windowSize):
				for j in range(windowSize):
					if not matFFT[i,j] in values : values.append(matFFT[i,j])
	values.sort()
	occurences=np.zeros(len(values))
	im = Image.fromarray(imagetteFFT[0])
	im.show()
	for mat in imagetteFFT:
		for i in range(windowSize):
			for j in range(windowSize):
				occurences[values.index(mat[i,j])]+=1
	sum=0
	# for i in range(len(occurences)) :
	# 	sum+=occurences[i]
	# print sum
	# print windowSize*windowSize
	
	ax.plot(values, occurences/(windowSize*windowSize)*100)
	windowSize+=windowSizeStep
plt.show()



exit("FIN")